# Check a FinOps completion report against the pack's report contract. Exit 0 valid, 1 invalid.
param([Parameter(Mandatory = $true)][string]$Report)
$ErrorActionPreference = 'Stop'
python (Join-Path $PSScriptRoot '..\tooling\hook_runner.py') completion --report $Report
exit $LASTEXITCODE
