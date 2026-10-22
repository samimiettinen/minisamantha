#!/usr/bin/env python3
"""Check a disposable starter with installed Node/OpenClaw; never start a gateway."""

import argparse
import hashlib
import json
import os
from pathlib import Path
import re
import shutil
import signal
import subprocess
import tempfile

from scaffold import scaffold

POLICY_DATE = "2026-10-22"
GROUPS = [
    {"slug": "sample-t2", "jid": "111111111111111111@g.us", "tier": "T2"},
    {"slug": "sample-t3", "jid": "222222222222222222@g.us", "tier": "T3"},
]
NOT_RUN = ("running_gateway_runtime", "model_authentication", "live_channel_and_mentions",
           "sandbox_execution", "backup_restore")


def isolated_environment(root, node):
    # Allow only these settings. Inherited credentials, NODE_OPTIONS, proxy URLs,
    # profile overrides and shell-env loading must not enter this synthetic run.
    env = {"PATH": str(Path(node).parent) + os.pathsep + os.defpath,
           "OPENCLAW_HOME": str(root / "home"),
           "OPENCLAW_STATE_DIR": str(root / "profile"),
           "OPENCLAW_CONFIG_PATH": str(root / "profile" / "openclaw.json"),
           "XDG_CONFIG_HOME": str(root / "xdg-config"),
           "XDG_CACHE_HOME": str(root / "cache"), "TMPDIR": str(root / "tmp"),
           "NO_COLOR": "1", "TERM": "dumb"}
    for name in ("home", "xdg-config", "cache", "tmp"):
        (root / name).mkdir(mode=0o700)
    return env


def run_command(argv, env, cwd):
    with subprocess.Popen(argv, env=env, cwd=cwd, stdin=subprocess.DEVNULL,
                          stdout=subprocess.PIPE, stderr=subprocess.PIPE,
                          text=True, start_new_session=True) as process:
        try:
            stdout, stderr = process.communicate(timeout=60)
        except subprocess.TimeoutExpired:
            # macOS/Linux: retire CLI children before deleting their temporary state.
            try:
                os.killpg(process.pid, signal.SIGKILL)
            except ProcessLookupError:
                pass
            process.communicate()
            raise
        return subprocess.CompletedProcess(argv, process.returncode, stdout, stderr)


def assess(kind, result, token):
    """Return only status/counts/check IDs, never raw CLI text or config values."""
    data = json.loads(result.stdout)
    if not isinstance(data, dict):
        raise ValueError("Expected an object")
    findings = data.get("findings", [])
    if not isinstance(findings, list) or any(not isinstance(f, dict) for f in findings):
        raise ValueError("Invalid findings")
    ids = []
    for finding in findings:
        value = finding.get("checkId", finding.get("code", ""))
        if (isinstance(value, str) and token not in value
                and re.fullmatch(r"[A-Za-z][A-Za-z0-9_./-]{0,127}", value)):
            ids.append(value)
    entry = {"check": kind, "status": "FAIL", "finding_ids": sorted(set(ids))}
    if kind == "config_schema":
        if result.returncode == 0 and data.get("valid") is True:
            entry["status"] = "WARN" if data.get("warnings") else "PASS"
    elif kind == "secret_resolution":
        resolution = data.get("resolution", {})
        counts = data.get("summary", {})
        required = ("plaintextCount", "unresolvedRefCount", "shadowedRefCount",
                    "storeResidueCount", "legacyResidueCount")
        if (result.returncode == 0 and data.get("status") == "clean"
                and resolution.get("resolvabilityComplete") is True
                and type(resolution.get("refsChecked")) is int and resolution["refsChecked"] >= 1
                and resolution.get("skippedExecRefs") == 0
                and all(type(counts.get(k)) is int and counts[k] == 0 for k in required)
                and not findings):
            entry["status"] = "PASS"
    elif kind == "doctor_lint":
        severities = [f.get("severity") for f in findings]
        if (result.returncode in (0, 1) and type(data.get("checksRun")) is int
                and data["checksRun"] > 0 and isinstance(data.get("ok"), bool)
                and all(s in ("info", "warning") for s in severities)):
            if "warning" in severities:
                entry["status"] = "WARN"
            elif result.returncode == 0 and data["ok"]:
                entry["status"] = "PASS"
        entry["checks_run"] = data.get("checksRun") if type(data.get("checksRun")) is int else 0
        entry["checks_skipped"] = data.get("checksSkipped") if type(data.get("checksSkipped")) is int else None
        entry["findings_count"] = len(findings)
    elif kind == "security_audit":
        counts = data.get("summary", {})
        if all(type(counts.get(k)) is int and counts[k] >= 0 for k in ("critical", "warn", "info")):
            entry["counts"] = {k: counts[k] for k in ("critical", "warn", "info")}
            actual = {k: sum(f.get("severity") == k for f in findings) for k in counts}
            if (result.returncode == 0 and not counts["critical"]
                    and all(f.get("severity") in ("critical", "warn", "info") for f in findings)
                    and all(actual[k] == counts[k] for k in ("critical", "warn", "info"))):
                entry["status"] = "WARN" if counts["warn"] else "PASS"
    return entry


def check_install(node, openclaw, scratch_dir=None, runner=run_command):
    scripts = Path(__file__).parent
    digest = hashlib.sha256((scripts / "scaffold.py").read_bytes() + Path(__file__).read_bytes()).hexdigest()
    report = {"scope": "disposable CLI checks; no running installation inspected",
              "policy_date": POLICY_DATE, "scripts_sha256": digest, "versions": {}, "checks": []}
    checks = report["checks"]
    with tempfile.TemporaryDirectory(prefix="minisamantha-check-", dir=scratch_dir) as folder:
        root = Path(folder).resolve()
        env = isolated_environment(root, node)
        scaffold(root / "profile", "+15555550100", GROUPS)
        token = (root / "profile/secrets/gateway-token").read_text().strip()
        try:
            result = runner([str(node), "--version"], env, root)
            match = re.fullmatch(r"v(\d+)\.(\d+)\.(\d+)\s*", result.stdout)
            version = tuple(map(int, match.groups())) if match else ()
            patched = (version and ((version[0] == 24 and version >= (24, 22, 1))
                                    or (version[0] == 26 and version >= (26, 12, 1))))
            checks.append({"check": "node_cli_baseline", "status": "PASS" if result.returncode == 0 and patched else "FAIL"})
            if version:
                report["versions"]["node"] = ".".join(map(str, version))
            if checks[-1]["status"] == "PASS":
                result = runner([str(node), str(openclaw), "--version"], env, root)
                match = re.fullmatch(r"OpenClaw (\d{4})\.(\d+)\.(\d+)(?: \([a-f0-9]+\))?\s*", result.stdout)
                version = tuple(map(int, match.groups())) if match else ()
                checks.append({"check": "openclaw_cli_baseline", "status": "PASS" if result.returncode == 0 and version >= (2026, 10, 6) else "FAIL"})
                if version:
                    report["versions"]["openclaw"] = ".".join(map(str, version))
            if checks[-1]["status"] == "PASS":
                for kind, args in (
                    ("config_schema", ["config", "validate", "--json"]),
                    ("secret_resolution", ["secrets", "audit", "--check", "--json"]),
                    ("doctor_lint", ["doctor", "--lint", "--json"]),
                    ("security_audit", ["security", "audit", "--json"]),
                ):
                    result = runner([str(node), str(openclaw), *args], env, root)
                    checks.append(assess(kind, result, token))
                    if kind == "config_schema" and checks[-1]["status"] == "FAIL":
                        break
        except (OSError, ValueError, TypeError, AttributeError, subprocess.SubprocessError):
            checks.append({"check": "cli_execution", "status": "FAIL",
                           "note": "Command unavailable, timed out, or returned an unexpected report; raw output withheld."})
    for check in ("node_cli_baseline", "openclaw_cli_baseline", "config_schema", "secret_resolution", "doctor_lint", "security_audit", *NOT_RUN):
        if not any(entry["check"] == check for entry in checks):
            checks.append({"check": check, "status": "NOT RUN"})
    report["result"] = "FAIL" if any(c["status"] == "FAIL" for c in checks) else (
        "REVIEW" if any(c["status"] == "WARN" for c in checks) else "PASS")
    return report


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--node", default=shutil.which("node"), help="Installed Node executable")
    parser.add_argument("--openclaw", default=shutil.which("openclaw"), help="Installed npm-style OpenClaw JavaScript entry point")
    parser.add_argument("--scratch-dir", type=Path, help="Existing parent for disposable files")
    parser.add_argument("--json", action="store_true", help="Print the bounded JSON report")
    args = parser.parse_args()
    if not args.node or not args.openclaw:
        parser.exit(2, "Install reviewed Node/OpenClaw first, or select them with --node and --openclaw. Nothing was installed.\n")
    try:
        report = check_install(Path(args.node).resolve(), Path(args.openclaw).resolve(), args.scratch_dir)
    except OSError:
        parser.exit(2, "Could not prepare disposable files. Check the scratch directory privately.\n")
    if args.json:
        print(json.dumps(report, indent=2))
    else:
        print("MiniSamantha local check:", report["result"])
        print("Node:", report["versions"].get("node", "unverified"),
              "OpenClaw:", report["versions"].get("openclaw", "unverified"))
        for entry in report["checks"]:
            print(entry["status"] + ": " + entry["check"])
            for finding_id in entry.get("finding_ids", []):
                print("  " + finding_id)
        print("Review warnings using references/local-check.md; do not relax controls to clear them.")
        print("This did not test a running gateway, messages, Docker containment, or restore.")
    return 0 if report["result"] == "PASS" else 1


if __name__ == "__main__":
    raise SystemExit(main())
