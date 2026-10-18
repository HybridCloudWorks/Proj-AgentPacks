#!/usr/bin/env bash
# Manual completion check: validate a completion report JSON against the pack's report contract.
set -euo pipefail
if [ "$#" -ne 1 ]; then
  echo "usage: $0 <completion-report.json>" >&2
  exit 2
fi
script_dir="$(cd "$(dirname "$0")" && pwd)"
python3 "$script_dir/../tooling/hook_runner.py" completion --report "$1"
