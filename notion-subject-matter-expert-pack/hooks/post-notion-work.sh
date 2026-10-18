#!/usr/bin/env bash
# Manual completion report check: post-notion-work.sh REPORT.json
set -euo pipefail
script_dir="$(cd "$(dirname "$0")" && pwd)"
python3 -I -B "$script_dir/../tooling/completion_contract.py" "$1"
