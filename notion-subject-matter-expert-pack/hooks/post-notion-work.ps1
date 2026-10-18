# Manual completion report check: post-notion-work.ps1 REPORT.json
param([Parameter(Mandatory = $true)][string]$Report)
$ErrorActionPreference = 'Stop'
python -I -B (Join-Path $PSScriptRoot '..\tooling\completion_contract.py') $Report
exit $LASTEXITCODE
