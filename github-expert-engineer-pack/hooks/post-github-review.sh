#!/usr/bin/env bash
set -euo pipefail
[[ -n "${1:-}" ]] || { echo "usage: post-github-review.sh REPORT.md" >&2; exit 2; }
python3 "$(dirname "$0")/../tooling/validate_github_review.py" "$1"
