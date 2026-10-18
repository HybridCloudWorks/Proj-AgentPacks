# Worked example: count to for_each on log storage accounts

Synthetic walkthrough. The repository, SHAs, line numbers and command output are illustrative; nothing was run against real infrastructure.

- Prompt: `assess-existing-environment-impact.prompt.md`
- Skills: `review-infrastructure-pr`, `review-terraform-opentofu`, `verify-infrastructure-evidence`
- Outcome: Changes requested

## Request

> PR #412 in `platform-infra` switches our log storage accounts from `count` to `for_each`. The plan in CI is clean. Is it safe for prod?

## The change

Base `9f3c2e1`, head `4b7d0a8`. The core of the diff:

```diff
--- a/modules/log-storage/main.tf
+++ b/modules/log-storage/main.tf
@@ -1,9 +1,9 @@
 resource "azurerm_storage_account" "logs" {
-  count                    = length(var.regions)
-  name                     = "stlogs${var.env}${count.index}"
-  location                 = var.regions[count.index]
+  for_each                 = toset(var.regions)
+  name                     = "stlogs${var.env}${local.region_short[each.key]}"
+  location                 = each.key
   resource_group_name      = var.resource_group_name
   account_tier             = "Standard"
   account_replication_type = "GRS"
```

`modules/log-storage/variables.tf` adds a `validation` block requiring every region to be a key of `local.region_short`, and `modules/log-storage/outputs.tf` changes `account_ids` from a splat to a `for` expression keyed by region.

## Walkthrough

1. **Inventory.** Terraform only. Root module `envs/prod` calls `modules/log-storage` with `regions = ["eastus2", "westus2"]`. The backend is `azurerm`, key `prod/logging.tfstate`, from `backends/prod.hcl`. `.github/workflows/terraform.yml` plans on pull requests and applies on `main`.
2. **Coverage.** `change_manifest.py --base 9f3c2e1 --head 4b7d0a8 --format markdown` lists 3 files, 15 added and 9 deleted lines. Each of the 24 lines receives a disposition in the ledger (`templates/coverage-ledger.md`).
3. **Change contract.** Intent from the PR description: "same accounts, keyed by region instead of index". It must never delete or recreate the existing archive accounts, which the repository's `runbooks/log-retention.md` describes as the 400-day audit log store.
4. **Address trace (`review-terraform-opentofu`).** Today's instances are `module.logs.azurerm_storage_account.logs[0]` (eastus2, `stlogsprod0`) and `[1]` (westus2, `stlogsprod1`). The new addresses are `logs["eastus2"]` and `logs["westus2"]`. The diff adds no `moved` block, and a repository search finds none elsewhere. Terraform does not map `count` indexes to `for_each` keys by itself, so it plans to destroy both index instances and create two keyed ones.
5. **Identity beyond the address.** Even with `moved` blocks, `name` changes from `stlogsprod0` to `stlogsprodeus2`. The provider documentation for the version pinned in `.terraform.lock.hcl` marks `name` as forcing a new resource. Address migration alone cannot preserve these accounts.
6. **Evidence (`verify-infrastructure-evidence`).** The attached plan says `Plan: 2 to add, 0 to change, 0 to destroy`. The CI log shows it was initialized with `-backend-config=backends/sandbox.hcl`, whose state holds no log accounts. It is an empty-state plan for a different target, so it cannot clear the upgrade. Local checks: `terraform fmt -check -diff -recursive` passed; `terraform validate` was skipped because the module is not initialized and downloads were not permitted.
7. **Cleared during the adversarial pass.** The new `validation` block makes an unmapped region fail at plan time, which fails closed. The `account_ids` output keeps its `map(string)` type; the only consumer, `envs/prod/monitoring.tf`, already indexes by region name. Both were recorded as verified.

## Completion report

### Executive Summary

- Overall assessment: The change replaces both production log archive storage accounts instead of re-keying them.
- Highest-risk finding: F-01, Preserve the existing log storage accounts across the for_each migration.
- Reviewed transition: two `count`-indexed storage accounts in `prod/logging.tfstate` to two `for_each`-keyed accounts with new names.
- Release or merge readiness: Not ready; the attached plan does not cover production state.

### Review Scope

- Base and head: `9f3c2e1` → `4b7d0a8`
- Files and technologies: 3 Terraform files (`modules/log-storage/main.tf`, `variables.tf`, `outputs.tf`)
- Entry points and execution order: (1) PR workflow plans `envs/prod` against the sandbox backend; (2) the `main` workflow applies `envs/prod` against `backends/prod.hcl`
- Targets, identities, state, and ownership: production subscription, resource group `rg-logging-prod`, state key `prod/logging.tfstate`, apply identity `terraform-prod-apply`; Terraform is the only owner of both accounts
- Evidence reviewed: CI plan from run on `4b7d0a8` (sandbox backend), provider lock file, `runbooks/log-retention.md`
- Constraints and exclusions: no access to production state; no provider downloads, so `terraform validate` did not run

### Coverage and Evidence

- Changed lines: 24 / 24
- Deletions, renames, generated artifacts, mode, or binary changes: 9 deleted lines, all replaced by the `for_each` form; no renames, generated files or mode changes
- Cross-tool handoffs reviewed: `account_ids` output to `envs/prod/monitoring.tf`, compatible
- Existing-environment evidence: None; the attached plan used sandbox state
- Missing or non-authoritative evidence: production-state plan
- Checks: `terraform fmt -check -diff -recursive`, Terraform CLI 1.9.8, pass; `terraform validate`, skip (module not initialized, downloads not permitted)

### Findings Summary

`Critical: 0 · High: 1 · Medium: 0 · Low: 0 · Evidence gaps: 1`

### Findings

```text
Finding ID: F-01
Severity: High
Confidence: High
File: modules/log-storage/main.tf
Location: lines 2-3 (new)
Technology: Terraform, azurerm provider
Category: Lifecycle and destructive impact
Title: Preserve the existing log storage accounts across the for_each migration
Execution path or trigger: The next apply on main against prod/logging.tfstate, which holds logs[0] and logs[1].
Description: Switching from count to for_each changes the instance addresses with no moved blocks, and the new name expression changes both account names, which forces replacement even if the addresses were moved.
Impact: Terraform destroys stlogsprod0 and stlogsprod1, the 400-day audit log archive, and creates empty accounts. Data loss for a retention-bound store.
Remediation direction: Add moved blocks from logs[0] and logs[1] to the region keys, and keep the existing account names for existing regions (for example a per-region name map that defaults to the new scheme only for new regions). If a rename is required, plan a data migration as a separate change.
Verify with: a plan against prod/logging.tfstate from the fixed head that shows 0 to destroy and no replacement of either account.
```

### Evidence Gaps

```text
[High evidence gap] Provide a plan against the production state
Artifact: terraform plan output (saved plan and text rendering)
Commit: the head that contains the fix for F-01
Inputs, target, identity: envs/prod with backends/prod.hcl, the production tfvars, read-capable plan identity
Risk it resolves: whether any storage account is destroyed or replaced in production
```

### Residual Risk

Once F-01 is fixed, the outcome still depends on the production plan above being generated from the fixed commit with the production backend and variables.

### Disposition

Changes requested

### Handoff

- Required corrections: F-01 (High): keep the existing account addresses and names, `modules/log-storage/main.tf:2-3`.
- Suggested work order: (1) add `moved` blocks and the name-preservation map; (2) regenerate the plan against production state; (3) attach it to the PR.
- Validation required after fixes: production-state plan showing 0 to destroy and no replacement.
- Human decisions or approvals: none, unless the team decides to rename the accounts; that needs an owner for the data migration.
- Configuration and operational dependencies: the PR workflow plans only against the sandbox backend, so every production-impacting Terraform PR needs a manually attached production plan until that changes.
