param(
    [string]$Repository = (Get-Location).Path,
    [string]$Output
)

$tool = Join-Path $PSScriptRoot '..\tooling\review_inventory.py'
$args = @($tool, $Repository)
if ($Output) { $args += @('--output', $Output) }

Write-Output "Cloud Pre-Press pre-review inventory: $Repository"
Write-Output "Read-only: no Azure, deployment, state, policy, identity, or PR mutation."
python @args
exit $LASTEXITCODE
