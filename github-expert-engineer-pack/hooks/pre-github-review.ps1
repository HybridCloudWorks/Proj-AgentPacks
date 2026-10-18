[CmdletBinding()]
param([string]$OutputPath = 'github-review-inventory.json')
$ErrorActionPreference = 'Stop'
$script = Join-Path $PSScriptRoot '..\tooling\github_inventory.py'
if (-not (Get-Command python -ErrorAction SilentlyContinue)) { throw 'python is required' }
python $script --root (Get-Location).Path --out $OutputPath
Write-Output "Pre-review inventory written to $OutputPath. No GitHub API call was made."
