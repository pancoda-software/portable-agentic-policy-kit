#!/usr/bin/env bash
# Framework-independent, read-only verification helper. No package manager assumptions.
# Run from the Git repository root. Does not add, commit, push, or install anything.
set -euo pipefail
exec python3 - "$@" <<'PY'
import argparse
import json
import re
import subprocess
import sys
from pathlib import Path

parser = argparse.ArgumentParser(description='Framework-neutral agent verification (supplemental, not a sandbox)')
parser.add_argument('--risk', choices=('low','medium','high'), default='medium')
parser.add_argument('--checks-file', type=Path, default=Path('.agentic/checks.json'), help='Optional project-owned JSON command list')
parser.add_argument('--allow-checks', action='store_true', help='Authorize execution of reviewed project check commands')
parser.add_argument('--dry-run', action='store_true', help='Print planned checks; never reports PASS')
parser.add_argument('--timeout', type=int, default=180, help='Maximum seconds per check (1-1800)')
args = parser.parse_args()
if not 1 <= args.timeout <= 1800:
    parser.error('--timeout must be in 1..1800')

def run(argv, timeout=30):
    try:
        return subprocess.run(argv, capture_output=True, text=True, check=False, timeout=timeout)
    except (FileNotFoundError, subprocess.TimeoutExpired, OSError) as exc:
        print(f'UNAVAILABLE command: {type(exc).__name__}')
        return None

root = run(['git','rev-parse','--show-toplevel'])
if root is None or root.returncode != 0:
    print('FAIL not in a Git repository'); sys.exit(2)
if Path(root.stdout.strip()).resolve() != Path.cwd().resolve():
    print('FAIL run from Git repository root'); sys.exit(2)
head = run(['git','rev-parse','--verify','HEAD'])
if head is None or head.returncode:
    print('UNAVAILABLE no committed Git baseline'); sys.exit(2)
failed = False
for command in (['git','diff','--check'], ['git','diff','--cached','--check']):
    result = run(command)
    if result is None or result.returncode:
        print('FAIL whitespace check'); failed=True
    else:
        print('PASS ' + ' '.join(command))
status = run(['git','status','--porcelain=v1','--untracked-files=normal'])
if status is None or status.returncode:
    print('FAIL cannot inspect Git status'); sys.exit(2)
if any(line.startswith('??') for line in status.stdout.splitlines()):
    print('WARNING untracked files are NOT checked; review independently')
diff = run(['git','diff','--no-ext-diff','--no-textconv','--unified=0','HEAD'],60)
if diff is None or diff.returncode:
    print('FAIL cannot inspect Git diff'); sys.exit(2)
pattern = re.compile(r'AKIA[0-9A-Z]{16}|-----BEGIN (?:RSA |EC |OPENSSH )?PRIVATE KEY-----|(?:password|api[_-]?key|secret[_-]?key|access[_-]?token)\s*[:=]\s*[\'\"]?[^\s\'\"{}$]{8,}', re.I)
secret_found = False
for line in diff.stdout.splitlines():
    if line.startswith('+++ b/') and re.search(r'(^|/)\.env(?:\.|$)|\.(?:pem|key|p12)$', line[6:],re.I):
        secret_found=True
    elif line.startswith('+') and not line.startswith('+++') and pattern.search(line[1:]):
        secret_found=True
if secret_found:
    print('FAIL potential sensitive material in tracked diff (details redacted)');failed=True
else:
    print('PASS heuristic tracked-diff secret scan (not comprehensive)')

checks = {}
if args.checks_file.exists():
    if args.checks_file.is_symlink() or not args.checks_file.is_file():
        print('FAIL checks file must be a regular file, not a symlink');sys.exit(2)
    try:
        obj=json.loads(args.checks_file.read_text(encoding='utf-8'))
        if not isinstance(obj,dict) or obj.get('schema') != 1 or not isinstance(obj.get('checks'),dict):
            raise ValueError('wrong checks schema')
        checks=obj['checks']
        if any(not isinstance(k,str) or not re.fullmatch(r'[a-z][a-z0-9_-]{0,39}',k) or not isinstance(v,list) or not v or any(not isinstance(x,str) or not x or '\x00' in x for x in v) for k,v in checks.items()):
            raise ValueError('check commands must be arrays of argument strings')
    except (OSError,UnicodeError,ValueError) as exc:
        print(f'FAIL invalid checks file: {type(exc).__name__}');sys.exit(2)

# Required verification is defined by risk, but not by a specific language, build system or package manager.
required = [] if args.risk == 'low' else ['test']
for name in required:
    if name not in checks:
        print(f'FAIL required {name} check UNAVAILABLE: configure .agentic/checks.json')
        failed = True
for name, command in sorted(checks.items()):
    if args.dry_run:
        print(f'SKIPPED {name}: dry-run; inspect checks-file commands before approval')
        continue
    if not args.allow_checks:
        print(f"{'FAIL' if name in required else 'SKIPPED'} {name}: command execution not authorized; inspect checks-file and use --allow-checks")
        failed = failed or name in required
        continue
    result=run(command,timeout=args.timeout)
    if result is None or result.returncode:
        print(f'FAIL {name}: check failed / timed out (exit {result.returncode if result else "UNAVAILABLE"})')
        failed=True
    else:
        print(f'PASS {name}')
print('NOTE Scope, existing failures, untracked files and command side effects need separate review.')
if args.dry_run:
    print('NOT VERIFIED: dry-run cannot authorize a commit'); sys.exit(3)
if failed:
    print('FAIL verification; do not autonomously commit');sys.exit(1)
print('PASS available checks; not proof of full regression or security coverage')
PY
