#!/usr/bin/env bash
# Manual preflight: container file inventory and static-check summary. Reads files only.
set -euo pipefail
script_dir="$(cd "$(dirname "$0")" && pwd)"
python3 -I -B "$script_dir/../tooling/hook_runner.py" preflight --root "${1:-.}"
