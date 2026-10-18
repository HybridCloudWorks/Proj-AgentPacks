# Manual completion check: validates a completion report's shape; executes none of the commands it claims.
param([Parameter(Mandatory = $true)][string]$Report)
$ErrorActionPreference = 'Stop'
python -I -B (Join-Path $PSScriptRoot '..\tooling\hook_runner.py') completion --report $Report
exit $LASTEXITCODE
