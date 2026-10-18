#!/usr/bin/env bash
set -euo pipefail

if [[ $# -ne 1 ]]; then
  echo "Usage: $0 REVIEW.md" >&2
  exit 2
fi
script_dir="$(CDPATH= cd -- "$(dirname -- "$0")" && pwd)"
echo "Cloud Pre-Press post-review report validation: $1"
python3 "$script_dir/../tooling/validate_review_report.py" "$1"
