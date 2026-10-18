[CmdletBinding()]
param([Parameter(Mandatory=$true)][string]$Event)
$ErrorActionPreference = 'Stop'
$inputText = [Console]::In.ReadToEnd()
if (-not (Get-Command python -ErrorAction SilentlyContinue)) { throw 'python is required' }
$script = Join-Path $PSScriptRoot 'codex_event.py'
$inputText | python $script --event $Event
