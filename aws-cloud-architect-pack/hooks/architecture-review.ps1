param(
    [Parameter(Mandatory = $true)]
    [string]$HandoffPath
)

$required = @('REQ.md', 'TOPOLOGY.json', 'CONSTRAINTS.json', 'ADR.md')
$missing = @($required | Where-Object { -not (Test-Path -LiteralPath (Join-Path $HandoffPath $_)) })
if ($missing.Count -gt 0) {
    Write-Error ("Missing architecture handoff artifacts: " + ($missing -join ', '))
    exit 1
}

Write-Output "Architecture handoff contract present: $HandoffPath"
Write-Output "This hook performs no AWS calls and makes no file changes."
exit 0
