[CmdletBinding()]
param([Parameter(Mandatory=$true)][string[]]$Path)
$ErrorActionPreference = 'Stop'
$script = Join-Path $PSScriptRoot '..\tooling\validate_documentation.py'
python $script @Path
