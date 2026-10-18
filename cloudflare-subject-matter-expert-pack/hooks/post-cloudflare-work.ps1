# Manual completion check: validate a completion report JSON against the pack's report contract.
param([Parameter(Mandatory = $true)][string]$Report)
$ErrorActionPreference = 'Stop'
python (Join-Path $PSScriptRoot '..\tooling\hook_runner.py') completion --report $Report
exit $LASTEXITCODE
