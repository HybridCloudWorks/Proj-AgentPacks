param([string]$Repository = (Get-Location).Path)
$ErrorActionPreference = 'Stop'
python (Join-Path $PSScriptRoot '..\tooling\hook_runner.py') preflight --root $Repository
exit $LASTEXITCODE
