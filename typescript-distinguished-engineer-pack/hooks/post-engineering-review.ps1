param([string]$Report = 'engineering-completion-report.md')
$ErrorActionPreference = 'Stop'
if (-not (Test-Path -LiteralPath $Report)) { Write-Error "Report not found: $Report" }
python (Join-Path $PSScriptRoot '..\tooling\validate_engineering_report.py') $Report
Write-Host "Post-review complete. Report validation does not prove runtime behavior."
