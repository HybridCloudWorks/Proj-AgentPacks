[CmdletBinding()]
param([Parameter(Mandatory=$true)][string]$ReportPath)
$ErrorActionPreference = 'Stop'
$script = Join-Path $PSScriptRoot '..\tooling\validate_github_review.py'
python $script $ReportPath
