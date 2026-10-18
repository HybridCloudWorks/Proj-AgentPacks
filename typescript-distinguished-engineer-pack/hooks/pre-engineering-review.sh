#!/usr/bin/env sh
set -eu
repo_root="${1:-.}"
python3 "$(dirname "$0")/../tooling/repository_inventory.py" "$repo_root"
echo "Pre-review complete. Inventory is static; no external mutation was performed."
