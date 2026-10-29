#!/usr/bin/env bash
# Portable, read-only pre-commit verification helper. Does not git add/commit/push.
# Copy to <project>/scripts/agent-verify.sh and run from the project root.
set -euo pipefail
exec python3 - "$@" <<'PY'
import argparse
import json
import re
import shutil
import subprocess
import sys
from pathlib import Path

parser = argparse.ArgumentParser(description="Risk-adaptive repository gate (supplemental; not a sandbox)")
parser.add_argument("--risk", choices=("low", "medium", "high"), default="medium")
parser.add_argument("--allow-project-scripts", action="store_true", help="Explicitly permit inspected npm script execution")
parser.add_argument("--dry-run", action="store_true", help="Inspect only; NOT a verified pass")
parser.add_argument("--timeout", type=int, default=180, help="Timeout per npm script, seconds (1..1800)")
args = parser.parse_args()
if not 1 <= args.timeout <= 1800:
    parser.error("--timeout must be within 1..1800")


def run(cmd, timeout=30):
    try:
        return subprocess.run(cmd, text=True, capture_output=True, timeout=timeout, check=False)
    except (FileNotFoundError, subprocess.TimeoutExpired, OSError) as e:
        print(f"UNAVAILABLE {' '.join(cmd[:2])}: {type(e).__name__}")
        return None


bad = False
root = run(["git", "rev-parse", "--show-toplevel"])
if not root or root.returncode != 0:
    print("FAIL not in a Git repository")
    sys.exit(2)
if Path(root.stdout.strip()).resolve() != Path.cwd().resolve():
    print("FAIL run from Git repository root")
    sys.exit(2)
if not run(["git", "rev-parse", "--verify", "HEAD"]) or run(["git", "rev-parse", "--verify", "HEAD"]).returncode:
    print("UNAVAILABLE no baseline HEAD; cannot perform pre-commit comparison")
    sys.exit(2)

for argv in (["git", "diff", "--check"], ["git", "diff", "--cached", "--check"]):
    result = run(argv)
    if result is None or result.returncode != 0:
        print(f"FAIL whitespace check: {' '.join(argv)}")
        bad = True
    else:
        print(f"PASS {' '.join(argv)}")

status = run(["git", "status", "--porcelain=v1", "--untracked-files=normal"])
if status is None or status.returncode != 0:
    print("FAIL cannot read Git status")
    sys.exit(2)
if any(line.startswith("??") for line in status.stdout.splitlines()):
    print("WARNING untracked files are NOT included in the diff/secret scan; review and stage separately")

result = run(["git", "diff", "--no-ext-diff", "--no-textconv", "--unified=0", "HEAD"], timeout=60)
if not result or result.returncode != 0:
    print("FAIL cannot inspect Git diff")
    sys.exit(2)
pattern = re.compile(r"AKIA[0-9A-Z]{16}|-----BEGIN (?:RSA |EC |OPENSSH )?PRIVATE KEY-----|(?:password|api[_-]?key|secret[_-]?key|access[_-]?token)\s*[:=]\s*['\"]?[^\s'\"{}$]{8,}", re.I)
flagged = False
for line in result.stdout.splitlines():
    if line.startswith("+++ b/"):
        path = line[6:]
        if re.search(r"(^|/)\.env(?:\.|$)|\.(?:pem|key|p12)$", path, re.I):
            flagged = True
    elif line.startswith("+") and not line.startswith("+++") and pattern.search(line[1:]):
        flagged = True
if flagged:
    print("FAIL potential credential or sensitive file in tracked diff (details intentionally redacted)")
    bad = True
else:
    print("PASS heuristic tracked-diff secret scan (NOT a comprehensive scanner)")

pkg = Path("package.json")
scripts = {}
if pkg.is_file():
    try:
        package = json.loads(pkg.read_text(encoding="utf-8"))
        scripts = package.get("scripts", {})
        if not isinstance(scripts, dict):
            raise ValueError("scripts must be an object")
    except (OSError, UnicodeError, json.JSONDecodeError, ValueError) as exc:
        print(f"FAIL malformed package scripts: {type(exc).__name__}")
        sys.exit(2)

required = []
optional = []
if args.risk == "low":
    optional = ["test", "lint", "typecheck"]
else:
    required = ["test"] + (["build"] if args.risk == "high" else [])
    optional = ["lint", "typecheck"]

for task in required + optional:
    if task not in scripts:
        print(f"{'FAIL' if task in required else 'UNAVAILABLE'} npm run {task}: no script defined")
        if task in required:
            bad = True
        continue
    if args.dry_run:
        print(f"SKIPPED (dry-run) npm run {task}; script definition MUST be inspected separately")
        continue
    if not args.allow_project_scripts:
        print(f"{'FAIL' if task in required else 'SKIPPED'} npm run {task}: script execution not authorized; inspect package.json then use --allow-project-scripts")
        if task in required:
            bad = True
        continue
    if not shutil.which("npm"):
        print(f"{'FAIL' if task in required else 'UNAVAILABLE'} npm missing")
        if task in required:
            bad = True
        continue
    print(f"RUN npm run {task} (timeout {args.timeout}s)", flush=True)
    completed = run(["npm", "run", task], timeout=args.timeout)
    if not completed or completed.returncode != 0:
        print(f"FAIL npm run {task} (exit={completed.returncode if completed else 'timeout/unavailable'})")
        bad = True
    else:
        print(f"PASS npm run {task}")

print("NOTE Baseline failures, user-owned changes, scope, and script side effects require separate human/agent review.")
if args.dry_run:
    print("NOT VERIFIED: dry-run cannot authorize a commit")
    sys.exit(3)
if bad:
    print("FAIL quality gate; do not autonomously commit")
    sys.exit(1)
print("PASS available risk checks; this is not proof of complete regression/security coverage")
PY
