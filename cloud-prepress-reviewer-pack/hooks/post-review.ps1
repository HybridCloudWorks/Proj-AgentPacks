param(
    [Parameter(Mandatory = $true)]
    [string]$Report
)

$validator = Join-Path $PSScriptRoot '..\tooling\validate_review_report.py'
Write-Output "Cloud Pre-Press post-review report validation: $Report"
python $validator $Report
exit $LASTEXITCODE
