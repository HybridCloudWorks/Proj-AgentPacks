# Worked example: GitHub Actions to Bicep to PowerShell to Ansible

Synthetic walkthrough. The repository, SHAs, line numbers and command output are illustrative; nothing was run against real infrastructure.

- Prompt: `trace-cross-tool-handoffs.prompt.md`
- Skills: `review-infrastructure-pr`, `review-cicd-deployment`, `review-bicep-arm`, `review-powershell-automation`, `review-ansible-automation`, `verify-infrastructure-evidence`
- Outcome: Changes requested

## Request

> PR #88 in `web-tier-deploy` wires the new Bicep outputs into our Ansible inventory so the web VMs get configured in the same run. Staging run is green. Please check the whole chain.

## Execution sequence

Written before reading any line in detail, per `references/review-protocol.md` section 3:

1. `.github/workflows/deploy-web.yml`, job `deploy`, logs in with OIDC and runs `pwsh ./scripts/Deploy-WebTier.ps1 -Environment staging`.
2. `Deploy-WebTier.ps1` runs `az deployment group create` with `infra/web.bicep` and `infra/web.staging.bicepparam` and captures `properties.outputs`.
3. `infra/web.bicep` deploys the VMs and returns a new `hosts` array output and a new `storageConnection` output.
4. The script converts `hosts` into `inventory/staging.json` and prints the outputs for troubleshooting.
5. `ansible-playbook -i inventory/staging.json playbooks/web.yml` configures the group `web`.

## The change

Base `c41e9a0`, head `e8f2b17`. Four files, 47 added and 6 deleted lines. The lines that matter:

```bicep
// infra/web.bicep (new lines 58-62)
output hosts array = [for (name, i) in vmNames: {
  name: name
  privateIp: nics[i].properties.ipConfigurations[0].properties.privateIPAddress
}]
output storageConnection string = 'DefaultEndpointsProtocol=https;AccountName=${sa.name};AccountKey=${sa.listKeys().keys[0].value}'
```

```powershell
# scripts/Deploy-WebTier.ps1 (new lines 31-48)
$ErrorActionPreference = 'Stop'
$outputs = az deployment group create `
    --resource-group "rg-web-$Environment" `
    --template-file infra/web.bicep `
    --parameters "infra/web.$Environment.bicepparam" `
    --query properties.outputs --output json | ConvertFrom-Json
Write-Host "Deployment outputs: $($outputs | ConvertTo-Json -Depth 5)"

$hostVars = @{}
foreach ($h in $outputs.hosts.value) {
    $hostVars[$h.name] = @{ ansible_host = $h.privateIp }
}
$inventory = @{ all = @{ children = @{ web = @{ hosts = $hostVars } } } }
$inventory | ConvertTo-Json | Set-Content -Path "inventory/$Environment.json"
```

## Walkthrough

1. **Coverage.** `change_manifest.py` lists 4 files and 53 changed lines; all receive dispositions.
2. **Boundary 2→3 (`review-bicep-arm`).** `storageConnection` embeds `listKeys()` output in a deployment output. Deployment outputs are stored in the resource group's deployment history, where anyone with read access can retrieve them. `bicep lint` reported rule `outputs-should-not-contain-secrets` on line 62 as a warning; the evidence record shows the lint check as pass because only warning-level diagnostics were emitted, so the reviewer read the diagnostic rather than the result.
3. **Boundary 3→4 (`review-powershell-automation`).** Line 37 prints all outputs with `Write-Host`. The attached staging log for run 9120 on `e8f2b17` shows the connection string in clear text, because the value is not a registered secret and GitHub does not mask it. The reviewer reproduces it only as `[REDACTED_POSSIBLE_SECRET]`.
4. **Boundary 4→5 (`review-powershell-automation`).** Line 44 calls `ConvertTo-Json` without `-Depth`. The documented default depth is 2. The inventory nests `all → children → web → hosts → <host> → ansible_host`, so `web` is serialized as the string `System.Collections.Hashtable` instead of a mapping. PowerShell 7 emits only a warning when it truncates. The `inventory/staging.json` artifact from run 9120 confirms the string value.
5. **Native exit status (`review-powershell-automation`).** `$ErrorActionPreference = 'Stop'` does not make a failing `az` call terminate unless native-command error handling is enabled, and the script never checks `$LASTEXITCODE`. When the deployment fails, `az` writes nothing to stdout, `ConvertFrom-Json` receives no input, `$outputs` is `$null`, and the script continues and exits 0.
6. **Step 5 (`review-ansible-automation`).** With no usable `web` group, `ansible-playbook` warns that the host pattern `web` matched no hosts and exits 0. Run 9120 shows exactly that: `skipping: no hosts matched`. The "green staging run" configured nothing.
7. **Pipeline (`review-cicd-deployment`).** OIDC subject, permissions and environment are unchanged and correct for staging; `deploy-web-prod.yml` calls the same script with `-Environment production`, so findings F-02 and F-03 reach production on the next release.
8. **Evidence (`verify-infrastructure-evidence`).** PowerShell parser pass; PSScriptAnalyzer skip (module not installed); Bicep lint and build pass; actionlint skip (not installed); ansible-lint pass. None of these detects the depth or exit-code defect.

## Completion report

### Executive Summary

- Overall assessment: The chain exposes a storage key and reports success while configuring no hosts.
- Highest-risk finding: F-01, Remove the storage account key from deployment outputs and logs.
- Reviewed transition: deployment of web VMs extended with automatic Ansible configuration from Bicep outputs.
- Release or merge readiness: Not ready; three defects, two of which reach production through the shared script.

### Review Scope

- Base and head: `c41e9a0` → `e8f2b17`
- Files and technologies: `.github/workflows/deploy-web.yml` (GitHub Actions), `infra/web.bicep` (Bicep), `scripts/Deploy-WebTier.ps1` (PowerShell 7), `playbooks/web.yml` (Ansible)
- Entry points and execution order: workflow → script → `az deployment group create` → inventory generation → `ansible-playbook`
- Targets, identities, state, and ownership: `rg-web-staging` and, through `deploy-web-prod.yml`, `rg-web-production`; OIDC identities per environment; Bicep owns VMs and storage, Ansible owns guest configuration
- Evidence reviewed: run 9120 log and `inventory/staging.json` artifact from `e8f2b17`
- Constraints and exclusions: no cloud access; PSScriptAnalyzer and actionlint not installed

### Coverage and Evidence

- Changed lines: 53 / 53
- Deletions, renames, generated artifacts, mode, or binary changes: 6 deleted lines in the workflow (old manual inventory step), replaced; `inventory/staging.json` is generated at run time and not committed
- Cross-tool handoffs reviewed: workflow→script (parameters, identity) compatible; Bicep outputs→script (types) compatible; script→inventory (serialization) F-02; script exit status→workflow F-03; inventory→Ansible (empty match) contributes to F-02 and F-03
- Existing-environment evidence: run 9120 against staging
- Missing or non-authoritative evidence: none needed to establish the findings
- Checks: PowerShell parser pass; PSScriptAnalyzer skip (not installed); `bicep lint` pass with 1 warning; `bicep build` pass; actionlint skip (not installed); `ansible-lint --offline` pass

### Findings Summary

`Critical: 0 · High: 1 · Medium: 2 · Low: 0 · Evidence gaps: 0`

### Findings

```text
Finding ID: F-01
Severity: High
Confidence: High
File: infra/web.bicep
Location: line 62 (new); consumer scripts/Deploy-WebTier.ps1 line 37
Technology: Bicep, PowerShell
Category: Security and secrets
Title: Remove the storage account key from deployment outputs and logs
Execution path or trigger: Every deployment of web.bicep; every run of Deploy-WebTier.ps1.
Description: The storageConnection output embeds listKeys() output, so the account key is stored in deployment history, and line 37 prints it to the CI log, where run 9120 shows it unmasked ([REDACTED_POSSIBLE_SECRET]).
Impact: Anyone with read access to the resource group or the workflow logs obtains a full-access storage key for staging, and for production once the release runs.
Remediation direction: Do not output secrets; have consumers read the key from Key Vault or use managed identity. Remove the outputs dump or print only non-sensitive fields.
Verify with: bicep lint showing no outputs-should-not-contain-secrets diagnostic, and a new run log containing no connection string.
```

```text
Finding ID: F-02
Severity: Medium
Confidence: High
File: scripts/Deploy-WebTier.ps1
Location: line 44 (new)
Technology: PowerShell 7, Ansible inventory
Category: Inputs, types, and validation
Title: Serialize the inventory at its full depth and fail when it has no hosts
Execution path or trigger: Every run; the inventory nests five levels and ConvertTo-Json defaults to depth 2.
Description: The web group is written as the string "System.Collections.Hashtable", so the playbook's hosts: web pattern matches nothing and ansible-playbook exits 0.
Impact: New web VMs are deployed but never configured, while the pipeline reports success.
Remediation direction: Pass an explicit -Depth large enough for the structure, and assert before running the playbook that the web group contains the same number of hosts as the hosts output.
Verify with: a Pester test that converts a three-host output and asserts all.children.web.hosts is a mapping with three entries, plus a run log showing three hosts configured.
```

```text
Finding ID: F-03
Severity: Medium
Confidence: High
File: scripts/Deploy-WebTier.ps1
Location: lines 32-36 (new)
Technology: PowerShell 7, Azure CLI
Category: Error handling and exit status
Title: Fail the job when az deployment group create fails
Execution path or trigger: Any failed deployment, such as a quota, policy or validation error.
Description: The native command's exit status is never checked, and $ErrorActionPreference does not make it terminate, so a failed deployment yields $null outputs and the script exits 0.
Impact: A failed staging or production deployment is reported as successful, and the following Ansible step silently does nothing.
Remediation direction: Check $LASTEXITCODE immediately after the az call (or enable native-command error handling for the script) and throw with the failed resource group named.
Verify with: a Pester test that mocks az with exit code 1 and asserts the script throws.
```

### Evidence Gaps

None.

### Residual Risk

After the fixes, the review still depends on the production run using `infra/web.production.bicepparam` with the same output shape; that file is unchanged in this PR and was read, not exercised.

### Disposition

Changes requested

### Handoff

- Required corrections: F-01 (High) `infra/web.bicep:62` and `scripts/Deploy-WebTier.ps1:37`; F-02 (Medium) `scripts/Deploy-WebTier.ps1:44`; F-03 (Medium) `scripts/Deploy-WebTier.ps1:32-36`.
- Suggested work order: F-01 first, because the key is already exposed; then F-03, so failures surface; then F-02.
- Validation required after fixes: Pester tests named in F-02 and F-03; a staging run on the fixed head whose log shows three hosts configured and no connection string.
- Human decisions or approvals: the staging storage key printed in run 9120 should be treated as exposed; rotating it and deciding whether to delete the run log is a human action outside this review.
- Configuration and operational dependencies: install PSScriptAnalyzer in the review environment so the static checks cover these scripts.
