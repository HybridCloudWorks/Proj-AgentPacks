param([Parameter(Mandatory=$true)][string]$Report)
$ErrorActionPreference = 'Stop'
python (Join-Path $PSScriptRoot '..\tooling\hook_runner.py') completion --report $Report
exit $LASTEXITCODE
