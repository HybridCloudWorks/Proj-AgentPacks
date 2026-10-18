#!/usr/bin/env sh
set -eu
report="${1:-engineering-completion-report.md}"
test -f "$report"
python3 "$(dirname "$0")/../tooling/validate_engineering_report.py" "$report"
echo "Post-review complete. Report validation does not prove runtime behavior."
