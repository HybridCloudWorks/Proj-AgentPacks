#!/usr/bin/env bash
# Manual pre-publication check: pre-notion-publish.sh DRAFT.md [--audience external] [--kind agenda]
set -euo pipefail
script_dir="$(cd "$(dirname "$0")" && pwd)"
python3 -I -B "$script_dir/../tooling/notion_draft_check.py" "$@"
