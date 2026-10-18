#!/usr/bin/env bash
# Manual static check of Dockerfiles and Compose files. Heuristic; never builds or runs anything.
set -euo pipefail
script_dir="$(cd "$(dirname "$0")" && pwd)"
python3 -I -B "$script_dir/../tooling/hook_runner.py" lint --root "${1:-.}"
