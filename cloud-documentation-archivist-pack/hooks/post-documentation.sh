#!/usr/bin/env bash
set -euo pipefail
[[ $# -gt 0 ]] || { echo "usage: post-documentation.sh DOCUMENT.md [DOCUMENT.md...]" >&2; exit 2; }
python3 "$(dirname "$0")/../tooling/validate_documentation.py" "$@"
