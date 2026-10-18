#!/usr/bin/env bash
# Check a Google Cloud Architect completion report against the pack's report contract.
# Usage: hooks/post-gcp-architecture.sh path/to/completion.json
set -euo pipefail
script_dir="$(cd "$(dirname "$0")" && pwd)"
python3 "$script_dir/../tooling/completion_contract.py" --report "${1:?Pass the completion JSON path}"
