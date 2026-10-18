# Worked example: Key Vault diagnostics with verified evidence (no finding)

Synthetic walkthrough. The repository, SHAs, line numbers and command output are illustrative; nothing was run against real infrastructure.

- Prompt: `verify-review-evidence.prompt.md`, inside a full review
- Skills: `review-infrastructure-pr`, `review-bicep-arm`, `verify-infrastructure-evidence`
- Outcome: Ready for human approval

This example shows the no-finding path: every check is interpreted narrowly, the what-if is tied to the exact commit, target and identity, and the conclusion still names what remains.

## Request

> PR #301 in `shared-keyvaults` sends Key Vault audit logs to the central Log Analytics workspace. The prod what-if is attached. Run whatever checks you safely can and tell me if the evidence holds up.

## The change

Base `e17a4c3`, head `b8c2d90`. Four files, 19 added lines, no deletions. The new resource in `modules/keyvault/main.bicep`:

```bicep
@description('Resource ID of the central Log Analytics workspace.')
param logAnalyticsWorkspaceId string

resource kvDiagnostics 'Microsoft.Insights/diagnosticSettings@<version pinned by modules/diagnostics>' = {
  name: 'kv-audit-to-law'
  scope: vault
  properties: {
    workspaceId: logAnalyticsWorkspaceId
    logs: [
      {
        category: 'AuditEvent'
        enabled: true
      }
    ]
  }
}
```

`main.bicep` passes the new parameter through, and `params/dev.bicepparam` and `params/prod.bicepparam` each set the workspace resource ID owned by the `central-logging` repository.

## Walkthrough

1. **Inventory and contract.** Bicep only. Intent: create one diagnostic setting per vault; never modify the vault itself. The parameter has no default, so a parameter file that omits it fails at deployment time instead of falling back to a wrong workspace.
2. **Identity and scope (`review-bicep-arm`).** The diagnostic setting is an extension resource scoped to the existing `vault` symbol; its name is constant, so reruns update the same object instead of adding settings. The API version matches the one `modules/diagnostics` already pins. No role assignment, network or policy change.
3. **Safe checks (`verify-infrastructure-evidence`).** The reviewer ran the Skill's script from the repository root with downloads not permitted:

   ```text
   Infrastructure review static checks
   detected: terraform/opentofu=0, bicep=6, powershell=0, ansible-related=0, workflows=2, shell=0, kubernetes-related=0, json=1

   [PASS] Git whitespace validation
   command: git diff --check
   [PASS] JSON parser validation
   parsed 1 JSON file(s)
   [PASS] Bicep lint: modules/keyvault/main.bicep
   [PASS] Bicep build: modules/keyvault/main.bicep
   ... (10 more Bicep lint and build results, all PASS)
   [SKIP] YAML lint
   yamllint not installed
   [SKIP] GitHub Actions validation
   actionlint not installed

   Summary: passed=14, failed=0, skipped=2
   ```

   Read narrowly: `git diff --check` with no arguments inspects only uncommitted changes, so on a clean checkout of the head it says nothing about the PR. The JSON check parsed `bicepconfig.json` only. Lint and build establish that the templates compile under the repository's linter rules, not that the target accepts them.
4. **What-if integrity.** The attached what-if comes from CI run 4471, job `what-if-prod`. Its log shows checkout of `b8c2d90`, `params/prod.bicepparam`, scope `rg-kv-prod` and the OIDC identity bound to the `prod` environment, which are the same commit, parameters, scope and identity the deployment job uses. The output:

   ```text
   Scope: /subscriptions/<prod subscription>/resourceGroups/rg-kv-prod

     + Microsoft.KeyVault/vaults/kv-shared-prod/providers/Microsoft.Insights/diagnosticSettings/kv-audit-to-law
     = Microsoft.KeyVault/vaults/kv-shared-prod

   Resource changes: 1 to create, 1 no change.
   ```

   No delete, no modify, no unexplained no-change.
5. **Artifact chain.** `deploy.yml` (unchanged) builds `main.json` once, uploads it, and the deploy job downloads that artifact from the same run. The artifact previewed is the artifact deployed.
6. **Existing environment and cost.** `policy/assignments.bicep` has no policy that deploys Key Vault diagnostic settings. The PR description attaches a seven-day measurement from the dev vault and estimates under 1 GB a month of `AuditEvent` ingestion for prod; the reviewer checked the query against the dev parameter file.

## Completion report

### Executive Summary

- Overall assessment: The change adds one diagnostic setting per vault and modifies nothing else; the evidence matches the reviewed commit and target.
- Highest-risk finding: None.
- Reviewed transition: Key Vault `kv-shared-prod` without diagnostic settings to one setting sending `AuditEvent` to the central workspace.
- Release or merge readiness: Ready for human approval.

### Review Scope

- Base and head: `e17a4c3` → `b8c2d90`
- Files and technologies: `modules/keyvault/main.bicep`, `main.bicep`, `params/dev.bicepparam`, `params/prod.bicepparam` (Bicep)
- Entry points and execution order: `deploy.yml` builds `main.json` → what-if on pull request → deployment on `main` using the same artifact
- Targets, identities, state, and ownership: `rg-kv-prod` and `rg-kv-dev`; OIDC identities bound to the `prod` and `dev` environments; this repository owns the diagnostic setting, `central-logging` owns the workspace
- Evidence reviewed: CI run 4471 what-if and log; dev ingestion measurement in the PR description
- Constraints and exclusions: no Azure access; management-group policy assignments are outside this repository

### Coverage and Evidence

- Changed lines: 19 / 19
- Deletions, renames, generated artifacts, mode, or binary changes: none; `main.json` is generated in CI and not committed
- Cross-tool handoffs reviewed: parameter file → module parameter (resource ID string), compatible
- Existing-environment evidence: production what-if from `b8c2d90`
- Missing or non-authoritative evidence: none material; `git diff --check` and the JSON check do not cover the PR
- Checks: `run_review_checks.py` — Git whitespace pass (working tree only), JSON parser pass (`bicepconfig.json`), Bicep lint pass ×6, Bicep build pass ×6, yamllint skip (not installed), actionlint skip (not installed)

### Findings Summary

`Critical: 0 · High: 0 · Medium: 0 · Low: 0 · Evidence gaps: 0`

### Findings

None.

### Evidence Gaps

None.

### Residual Risk

No actionable defects found in the reviewed diff. Residual risk: what-if does not show management-group policies or settings created outside this repository; if one already sends `AuditEvent` from this vault to the same workspace, Azure rejects the duplicate destination and the deployment fails without affecting the vault.

### Disposition

Ready for human approval

### Handoff

- Required corrections: none.
- Suggested work order: not applicable.
- Validation required after fixes: after deployment, confirm `AuditEvent` records from `kv-shared-prod` arrive in the central workspace.
- Human decisions or approvals: normal approval; the `central-logging` owners accept the new ingestion source.
- Configuration and operational dependencies: install yamllint and actionlint in the review environment so workflow files are covered next time.
