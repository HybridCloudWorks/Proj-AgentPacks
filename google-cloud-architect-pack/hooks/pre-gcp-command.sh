#!/usr/bin/env bash
# Classify a proposed Google Cloud or Kubernetes command by approval level without running it.
# Usage: hooks/pre-gcp-command.sh gcloud compute instances list --project=my-project
set -euo pipefail
script_dir="$(cd "$(dirname "$0")" && pwd)"
if [ "$#" -eq 0 ]; then
  echo "usage: pre-gcp-command.sh COMMAND [ARGS...]" >&2
  exit 3
fi
python3 "$script_dir/../.apm/skills/gcp-estate-discovery/scripts/command_guard.py" classify -- "$@"
