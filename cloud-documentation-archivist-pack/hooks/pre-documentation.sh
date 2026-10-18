#!/usr/bin/env bash
set -euo pipefail
out="documentation-inventory.json"
if [[ "${1:-}" == "--out" ]]; then out="$2"; fi
python3 "$(dirname "$0")/../tooling/documentation_inventory.py" --root "$PWD" --out "$out"
echo "Pre-documentation inventory written to $out. No publication or network call was made."
