# Classify a proposed Google Cloud or Kubernetes command by approval level without running it.
# Usage: hooks\pre-gcp-command.ps1 "gcloud compute instances list --project=my-project"
param([Parameter(Mandatory = $true)][string]$Command)
$ErrorActionPreference = 'Stop'
$guard = Join-Path $PSScriptRoot '..\.apm\skills\gcp-estate-discovery\scripts\command_guard.py'
python $guard classify -- $Command
exit $LASTEXITCODE
