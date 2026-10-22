import copy
import importlib.util
import json
import os
from pathlib import Path
import subprocess
import sys
import tempfile
import unittest
from unittest import mock

SCRIPTS = Path(__file__).resolve().parents[1] / "skills/install-minisamantha/scripts"
with mock.patch.object(sys, "path", [str(SCRIPTS), *sys.path]):
    SPEC = importlib.util.spec_from_file_location("check_install", SCRIPTS / "check_install.py")
    checker = importlib.util.module_from_spec(SPEC)
    SPEC.loader.exec_module(checker)


def result(data, code=0):
    return subprocess.CompletedProcess([], code, json.dumps(data), "")


def clean_report(kind):
    return copy.deepcopy({
        "config_schema": {"valid": True, "warnings": []},
        "secret_resolution": {
            "status": "clean", "findings": [],
            "resolution": {"refsChecked": 1, "skippedExecRefs": 0, "resolvabilityComplete": True},
            "summary": {k: 0 for k in ("plaintextCount", "unresolvedRefCount", "shadowedRefCount",
                                      "storeResidueCount", "legacyResidueCount")}},
        "doctor_lint": {"ok": True, "checksRun": 36, "findings": []},
        "security_audit": {"summary": {"critical": 0, "warn": 0, "info": 0}, "findings": []},
    }[kind])


class LocalCheckTests(unittest.TestCase):
    def run_check(self, node="v24.22.1\n", version="OpenClaw 2026.10.6 (fe06181)\n",
                  override=None, inspect=None):
        calls, roots = [], []

        def runner(argv, env, cwd):
            calls.append(argv)
            roots.append(cwd)
            if inspect:
                inspect(argv, env, cwd)
            if len(argv) == 2:
                return subprocess.CompletedProcess(argv, 0, node, "")
            if argv[-1] == "--version":
                return subprocess.CompletedProcess(argv, 0, version, "")
            kind = {"config": "config_schema", "secrets": "secret_resolution",
                    "doctor": "doctor_lint", "security": "security_audit"}[argv[2]]
            return override(kind, cwd) if override else result(clean_report(kind))

        with tempfile.TemporaryDirectory() as tmp:
            report = checker.check_install(Path("/synthetic/bin/node"), Path("/synthetic/openclaw.mjs"),
                                           tmp, runner=runner)
            self.assertEqual(list(Path(tmp).iterdir()), [])
        self.assertTrue(all(not root.exists() for root in roots))
        return report, calls

    def test_success_keeps_live_boundaries_not_run(self):
        report, calls = self.run_check()
        self.assertEqual(report["result"], "PASS")
        self.assertEqual(report["versions"], {"node": "24.22.1", "openclaw": "2026.10.6"})
        self.assertEqual(len(calls), 6)
        self.assertEqual([c["check"] for c in report["checks"] if c["status"] == "NOT RUN"],
                         list(checker.NOT_RUN))
        self.assertNotIn("--deep", sum(calls, []))
        self.assertNotIn("--fix", sum(calls, []))

    def test_unpatched_or_unsupported_node_stops_before_openclaw(self):
        for version in ("v24.22.0", "v26.12.0", "v22.23.4", "v25.0.0", "v26.12.1-rc.1", "unknown"):
            with self.subTest(version=version):
                report, calls = self.run_check(node=version)
                self.assertEqual(report["result"], "FAIL")
                self.assertEqual(len(calls), 1)
        self.assertEqual(self.run_check(node="v26.12.1")[0]["result"], "PASS")

    def test_old_or_prerelease_openclaw_stops_before_checks(self):
        for version in ("OpenClaw 2026.10.3", "OpenClaw 2026.10.6-beta.1", "unknown"):
            with self.subTest(version=version):
                report, calls = self.run_check(version=version)
                self.assertEqual(report["result"], "FAIL")
                self.assertEqual(len(calls), 2)

    def test_isolated_environment_and_existing_profile_untouched(self):
        with tempfile.TemporaryDirectory() as tmp:
            existing = Path(tmp) / "existing.json"
            original = b'{"canary":"unrelated profile"}\n'
            existing.write_bytes(original)
            inherited = {"OPENCLAW_CONFIG_PATH": str(existing), "OPENCLAW_LOAD_SHELL_ENV": "1",
                         "NODE_OPTIONS": "--require /synthetic/injected.js", "HTTPS_PROXY": "synthetic",
                         "OPENAI_API_KEY": "synthetic-credential"}

            def inspect(argv, env, root):
                for key in inherited:
                    if key != "OPENCLAW_CONFIG_PATH":
                        self.assertNotIn(key, env)
                self.assertNotIn("HOME", env)
                self.assertNotIn("CODEX_HOME", env)
                self.assertTrue(Path(env["OPENCLAW_CONFIG_PATH"]).is_relative_to(root))
                self.assertTrue(Path(env["OPENCLAW_HOME"]).is_relative_to(root))
                config = json.loads(Path(env["OPENCLAW_CONFIG_PATH"]).read_text())
                self.assertFalse(config["channels"]["whatsapp"]["enabled"])
                self.assertEqual(len(config["agents"]["entries"]), 4)

            with mock.patch.dict(os.environ, inherited):
                self.run_check(inspect=inspect)
            self.assertEqual(existing.read_bytes(), original)

    def test_invalid_schema_stops_remaining_checks(self):
        report, calls = self.run_check(override=lambda kind, root: result({"valid": False}, 1))
        self.assertEqual(report["result"], "FAIL")
        self.assertEqual(len(calls), 3)

    def test_secret_resolution_requires_complete_clean_results(self):
        for key, value in (("refsChecked", 0), ("skippedExecRefs", 1), ("resolvabilityComplete", False)):
            data = clean_report("secret_resolution")
            data["resolution"][key] = value
            self.assertEqual(checker.assess("secret_resolution", result(data), "canary")["status"], "FAIL")
        data = clean_report("secret_resolution")
        data["summary"]["plaintextCount"] = 1
        self.assertEqual(checker.assess("secret_resolution", result(data), "canary")["status"], "FAIL")

    def test_doctor_exit_zero_does_not_hide_failed_checks(self):
        for code in (0, 1):
            data = clean_report("doctor_lint")
            data.update(ok=False, findings=[{"checkId": "core/doctor/example", "severity": "error"}])
            self.assertEqual(checker.assess("doctor_lint", result(data, code), "canary")["status"], "FAIL")
        data = clean_report("doctor_lint")
        self.assertEqual(checker.assess("doctor_lint", result(data, 1), "canary")["status"], "FAIL")

    def test_security_counts_and_severities_must_agree(self):
        for summary, findings in (
            ({"critical": 1, "warn": 0, "info": 0}, [{"severity": "critical"}]),
            ({"critical": 0, "warn": 0, "info": 0}, [{"severity": "critical"}]),
            ({"critical": 0, "warn": 0, "info": 0}, [{"severity": "unknown"}]),
        ):
            data = {"summary": summary, "findings": findings}
            self.assertEqual(checker.assess("security_audit", result(data), "canary")["status"], "FAIL")

    def test_warning_requires_review_and_no_raw_output_is_disclosed(self):
        canary = "synthetic-secret-canary"

        def override(kind, root):
            data = clean_report(kind)
            if kind == "doctor_lint":
                token = (root / "profile/secrets/gateway-token").read_text().strip()
                data.update(ok=False, findings=[
                    {"checkId": "core/doctor/example", "severity": "warning", "message": canary},
                    {"checkId": token, "severity": "warning", "message": token}])
                answer = result(data, 1)
                answer.stderr = canary
                return answer
            return result(data)

        report, _ = self.run_check(override=override)
        self.assertEqual(report["result"], "REVIEW")
        self.assertNotIn(canary, json.dumps(report))
        doctor = next(c for c in report["checks"] if c["check"] == "doctor_lint")
        self.assertEqual(doctor["finding_ids"], ["core/doctor/example"])

    def test_malformed_json_and_timeout_fail_without_leaking_output(self):
        for fault in ("invalid json with synthetic-secret", subprocess.TimeoutExpired(["synthetic"], 60)):
            def override(kind, root):
                if isinstance(fault, Exception):
                    raise fault
                return subprocess.CompletedProcess([], 0, fault, fault)

            report, _ = self.run_check(override=override)
            self.assertEqual(report["result"], "FAIL")
            self.assertNotIn("synthetic-secret", json.dumps(report))


if __name__ == "__main__":
    unittest.main()
