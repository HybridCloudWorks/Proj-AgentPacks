# Manual pre-publication check: pre-notion-publish.ps1 DRAFT.md [-Audience external] [-Kind agenda]
param(
    [Parameter(Mandatory = $true)][string]$Draft,
    [ValidateSet('internal', 'external')][string]$Audience = 'internal',
    [string]$Kind = 'any'
)
$ErrorActionPreference = 'Stop'
python -I -B (Join-Path $PSScriptRoot '..\tooling\notion_draft_check.py') $Draft --audience $Audience --kind $Kind
exit $LASTEXITCODE
