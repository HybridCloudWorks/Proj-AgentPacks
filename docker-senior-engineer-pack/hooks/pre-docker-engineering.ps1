# Manual preflight: container file inventory and static-check summary. Reads files only.
param([string]$Repository = (Get-Location).Path)
$ErrorActionPreference = 'Stop'
python -I -B (Join-Path $PSScriptRoot '..\tooling\hook_runner.py') preflight --root $Repository
exit $LASTEXITCODE
