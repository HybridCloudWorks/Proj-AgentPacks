param([string]$RepoRoot = (Get-Location).Path)
$ErrorActionPreference = 'Stop'
Write-Host "Pre-review: repository inventory for $RepoRoot"
python (Join-Path $PSScriptRoot '..\tooling\repository_inventory.py') $RepoRoot
Write-Host "Pre-review complete. Inventory is static; no external mutation was performed."
