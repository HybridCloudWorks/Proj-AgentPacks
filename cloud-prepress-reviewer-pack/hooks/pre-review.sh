#!/usr/bin/env bash
set -euo pipefail

repo="${1:-.}"
output="${2:-}"
script_dir="$(CDPATH= cd -- "$(dirname -- "$0")" && pwd)"
echo "Cloud Pre-Press pre-review inventory: ${repo}"
echo "Read-only: no Azure, deployment, state, policy, identity, or PR mutation."
if [[ -n "$output" ]]; then
  python3 "$script_dir/../tooling/review_inventory.py" "$repo" --output "$output"
else
  python3 "$script_dir/../tooling/review_inventory.py" "$repo"
fi
