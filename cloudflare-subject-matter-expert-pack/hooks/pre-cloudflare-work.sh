#!/usr/bin/env bash
# Manual preflight: summarize Wrangler and Terraform Cloudflare configuration in a project folder.
set -euo pipefail
script_dir="$(cd "$(dirname "$0")" && pwd)"
python3 "$script_dir/../tooling/hook_runner.py" preflight --root "${1:-.}"
