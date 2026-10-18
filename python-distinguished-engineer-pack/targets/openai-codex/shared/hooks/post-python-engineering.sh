#!/usr/bin/env bash
set -euo pipefail
script_dir="$(cd "$(dirname "$0")" && pwd)"
python3 "$script_dir/../tooling/hook_runner.py" completion --report "${1:?Pass the completion JSON path}"
