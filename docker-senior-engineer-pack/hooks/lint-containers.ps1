# Manual static check of Dockerfiles and Compose files. Heuristic; never builds or runs anything.
param([string]$Repository = (Get-Location).Path)
$ErrorActionPreference = 'Stop'
python -I -B (Join-Path $PSScriptRoot '..\tooling\hook_runner.py') lint --root $Repository
exit $LASTEXITCODE
