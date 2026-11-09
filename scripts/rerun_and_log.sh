#!/usr/bin/env bash
# Independent re-run of the v4.1.1 artifact on your own machine.
# Usage (from the repository root):  bash scripts/rerun_and_log.sh "Your Name"
# Needs: python3.12 (or python3 >= 3.11), Java 11 or later, internet access for pip and the TLC jar.
# Produces reruns/rerun_<name>_<date>.log and prints its SHA-256. Send the log file back.
set -uo pipefail
export PIP_DISABLE_PIP_VERSION_CHECK=1   # keeps local paths out of the log
NAME="${1:-anonymous}"
SLUG=$(printf '%s' "$NAME" | tr -cs 'A-Za-z0-9' '_' | sed 's/_*$//')
STAMP=$(date -u +%Y%m%dT%H%M%SZ)
ROOT=$(cd "$(dirname "$0")/.." && pwd)
mkdir -p "$ROOT/reruns"
LOG="$ROOT/reruns/rerun_${SLUG}_${STAMP}.log"
PY=$(command -v python3.12 || command -v python3)
JAVA=$(command -v java || true)
{
  echo "== who: $NAME"
  echo "== when (UTC): $STAMP"
  echo "== commit: $(git -C "$ROOT" rev-parse HEAD 2>/dev/null || echo 'not a git checkout')"
  echo "== os: $(uname -srm)"
  echo "== python: $($PY -c 'import sys,platform; print(sys.version.split()[0], platform.platform())')"
  echo "== java: $([ -n "$JAVA" ] && "$JAVA" -version 2>&1 | head -1 || echo 'NOT FOUND')"
  echo "== artifact SHA-256 check"
  (cd "$ROOT" && grep '  artifact/' SHA256SUMS | shasum -a 256 -c --quiet 2>&1 && echo "artifact/ matches SHA256SUMS")
  cd "$ROOT/artifact"
  "$PY" -m venv .venv && .venv/bin/pip install -q -r requirements.txt
  echo "== cryptography: $(.venv/bin/python -c 'import cryptography; from cryptography.hazmat.backends.openssl.backend import backend; print(cryptography.__version__, backend.openssl_version_text())')"
  "$PY" fetch_tlc.py
  echo "== reproduce_all.py"
  .venv/bin/python reproduce_all.py --java "$JAVA" --jar .tools/tla2tools.jar
  echo "== exit status: $?"
} 2>&1 | tee "$LOG"
echo
echo "Log written to: reruns/$(basename "$LOG")"
shasum -a 256 "$LOG"
