# Check a Google Cloud Architect completion report against the pack's report contract.
# Usage: hooks\post-gcp-architecture.ps1 -Report path\to\completion.json
param([Parameter(Mandatory = $true)][string]$Report)
$ErrorActionPreference = 'Stop'
python (Join-Path $PSScriptRoot '..\tooling\completion_contract.py') --report $Report
exit $LASTEXITCODE
