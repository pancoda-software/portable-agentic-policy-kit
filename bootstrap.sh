#!/usr/bin/env bash
# Optional remote one-command setup. Review before piping downloaded code to bash.
set -euo pipefail

REPO='pancoda-software/portable-agentic-policy-kit'
REF="${POLICY_KIT_REF:-main}"
if [[ "${1:-}" == '--ref' ]]; then
  [[ $# -ge 2 ]] || { echo 'Missing value for --ref' >&2; exit 2; }
  REF="$2"; shift 2
fi
[[ "$REF" =~ ^[A-Za-z0-9._/-]+$ ]] || { echo 'Invalid ref' >&2; exit 2; }
command -v python3 >/dev/null || { echo 'Python 3 required' >&2; exit 1; }
command -v mktemp >/dev/null || exit 1
TMP=$(mktemp -d)
trap 'rm -rf -- "$TMP"' EXIT
mkdir -p "$TMP/kit"

if command -v gh >/dev/null && gh auth status >/dev/null 2>&1; then
  echo 'Fetching policy kit via authenticated GitHub CLI...'
  gh repo clone "$REPO" "$TMP/kit" -- --quiet --depth 1
  # Explicit non-default refs require a fetch; never run an untrusted checkout hook.
  if [[ "$REF" != main ]]; then
    git -C "$TMP/kit" fetch --quiet --depth 1 origin "$REF"
    git -C "$TMP/kit" checkout --quiet --detach FETCH_HEAD
  fi
else
  command -v curl >/dev/null || { echo 'Install GitHub CLI and run gh auth login, or install curl.' >&2; exit 1; }
  command -v tar >/dev/null || { echo 'tar is required' >&2; exit 1; }
  echo 'Downloading policy kit from GitHub (public access required)...'
  curl --fail --location --silent --show-error --retry 2 \
    "https://api.github.com/repos/$REPO/tarball/$REF" -o "$TMP/source.tgz" || {
      echo 'Download failed. For a private repository, authenticate: gh auth login' >&2
      exit 1
    }
  tar -xzf "$TMP/source.tgz" --strip-components=1 -C "$TMP/kit"
fi
python3 "$TMP/kit/tooling/install.py" "$@"
