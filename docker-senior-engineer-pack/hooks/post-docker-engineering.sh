#!/usr/bin/env bash
# Manual completion check: validates a completion report's shape; executes none of the commands it claims.
set -euo pipefail
script_dir="$(cd "$(dirname "$0")" && pwd)"
python3 -I -B "$script_dir/../tooling/hook_runner.py" completion --report "${1:?Pass the completion JSON path}"
