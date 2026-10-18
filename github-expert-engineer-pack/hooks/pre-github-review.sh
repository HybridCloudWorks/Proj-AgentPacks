#!/usr/bin/env bash
set -euo pipefail
out="github-review-inventory.json"
if [[ "${1:-}" == "--out" ]]; then out="$2"; fi
python3 "$(dirname "$0")/../tooling/github_inventory.py" --root "$PWD" --out "$out"
echo "Pre-review inventory written to $out. No GitHub API call was made."
