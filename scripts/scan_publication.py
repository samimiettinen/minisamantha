#!/usr/bin/env python3
"""Scan a full Git checkout without printing secrets or private metadata."""

import argparse
import json
import os
from pathlib import Path
import subprocess
import tempfile

SCANNER_VERSION = "8.30.1"


def git(repo, *args):
    return subprocess.run(["git", "-C", str(repo), *args], check=True,
                          stdout=subprocess.PIPE, stderr=subprocess.PIPE).stdout


def private_email_count(metadata):
    """Project publication policy: author/committer email must be GitHub noreply."""
    return sum(not address.lower().endswith(b"@users.noreply.github.com")
               for address in metadata.split(b"\0") if address.strip())


def scan(repo, executable):
    repo = Path(repo).resolve()
    if Path(git(repo, "rev-parse", "--show-toplevel").decode().strip()).resolve() != repo:
        raise ValueError("Run against the repository root, not a parent project or subdirectory")
    if git(repo, "rev-parse", "--is-shallow-repository").strip() != b"false":
        raise ValueError("Full history required; fetch all branches/tags without shallow depth")
    head = git(repo, "rev-parse", "HEAD").decode().strip()
    count = int(git(repo, "rev-list", "--all", "--count"))
    env = {key: value for key, value in os.environ.items() if not key.startswith("GITLEAKS_")}
    version = subprocess.run([executable, "version"], check=True, capture_output=True,
                             env=env, timeout=30).stdout.decode().strip()
    if version != SCANNER_VERSION:
        raise ValueError("Use the pinned Gitleaks version documented in PUBLICATION.md")
    metadata = git(repo, "log", "--all", "--format=raw", "--no-show-signature")
    emails = git(repo, "log", "--all", "--format=%ae%x00%ce%x00", "-z")
    # Empty tokens/newlines separate commits; do not publish actual email values.
    emails = b"\0".join(part.strip() for part in emails.split(b"\0"))
    checks = {}
    with tempfile.TemporaryDirectory(prefix="minisamantha-scan-") as folder:
        private = Path(folder)
        config = private / "rules.toml"
        config.write_text("[extend]\nuseDefault = true\n", encoding="utf-8")
        ignore = private / "empty-ignore"
        ignore.touch()
        # Explicit defaults, no repository allowlists, baseline, or inline exemptions.
        common = ["--config", str(config), "--gitleaks-ignore-path", str(ignore),
                  "--ignore-gitleaks-allow", "--redact=100", "--no-banner", "--no-color",
                  "--report-format=json", "--exit-code=1", "--timeout=120"]
        commands = {
            "history": (["git", "--log-opts=--all --full-history -m --no-ext-diff", str(repo)], None),
            "working_tree": (["dir", str(repo)], None),
            "commit_metadata": (["stdin"], metadata),
        }
        for label, (args, payload) in commands.items():
            report = private / (label + ".json")
            result = subprocess.run([executable, *args, *common, "--report-path", str(report)],
                                    input=payload, capture_output=True, cwd=private, env=env,
                                    timeout=150)
            if result.returncode not in (0, 1) or not report.is_file():
                raise ValueError("Scanner failed; no clean result is claimed")
            findings = json.loads(report.read_text(encoding="utf-8"))
            checks[label] = {"pass": result.returncode == 0 and not findings,
                             "findings": len(findings)}
    email_count = private_email_count(emails)
    checks["commit_email_policy"] = {"pass": email_count == 0, "findings": email_count}
    return {"scanner": "gitleaks", "version": version, "head": head,
            "reachable_commits": count, "checks": checks,
            "pass": all(check["pass"] for check in checks.values())}


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--repo", type=Path, default=Path.cwd())
    parser.add_argument("--gitleaks", default="gitleaks", help="Path to verified Gitleaks 8.30.1")
    args = parser.parse_args()
    try:
        result = scan(args.repo, args.gitleaks)
    except (ValueError, OSError, subprocess.SubprocessError):
        # Tool stderr, file contents and exception messages may contain private data.
        print("Publication scan ERROR: check full checkout, pinned scanner and local prerequisites privately.")
        return 2
    print(json.dumps(result, indent=2))
    return 0 if result["pass"] else 1


if __name__ == "__main__":
    raise SystemExit(main())
