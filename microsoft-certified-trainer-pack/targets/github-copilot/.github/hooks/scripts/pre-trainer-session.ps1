$ErrorActionPreference = 'Stop'
Write-Output 'Trainer preflight: inspect course sources, audience, duration, permissions, licensing, accessibility, and environment before authoring or delivering.'
if (Test-Path -LiteralPath '.\DESCRIPTION.md') { Write-Output 'Trainer pack detected.' }
if (Test-Path -LiteralPath '.\VALIDATION_REPORT.md') { Write-Output 'Existing validation report is reference only; rebuild after changes.' }
