# List billing exports in a folder by detected schema; reads CSV header lines only.
param([string]$Workspace = (Get-Location).Path)
$ErrorActionPreference = 'Stop'
python (Join-Path $PSScriptRoot '..\tooling\hook_runner.py') preflight --root $Workspace
exit $LASTEXITCODE
