[CmdletBinding()]
param([string]$OutputPath = 'documentation-inventory.json')
$ErrorActionPreference = 'Stop'
$script = Join-Path $PSScriptRoot '..\tooling\documentation_inventory.py'
if (-not (Get-Command python -ErrorAction SilentlyContinue)) { throw 'python is required' }
python $script --root (Get-Location).Path --out $OutputPath
Write-Output "Pre-documentation inventory written to $OutputPath. No publication or network call was made."
