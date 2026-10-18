# Worked example: Terraform change before deployment review

Prompt: `.apm/prompts/review-before-deployment.prompt.md`, with `.apm/prompts/assess-operability-rollback-and-cost.prompt.md` for the rollback and cost checks. Outcome: `READY_FOR_DEPLOYMENT_REVIEW`.

Skills applied: cloud-prepress-orchestration, change-scope-and-impact, iac-policy-and-identity-review, deployment-preview-and-environment-review, azure-evidence-and-mcp-review, tests-build-and-dependency-review, operability-resilience-and-rollback-review, cost-allocation-and-governance-review, documentation-inputs-and-repository-contracts, review-report-and-pr-gate.

The repository, subscription, identities and figures are fictional.

## Request

> `feature/reports-private-endpoint` moves the reports storage account into a module, turns off public access and adds a private endpoint. CI already ran `plan-test`. Review it before the test deployment review. You can read the CI logs; nothing else in Azure.

## 1. Fix scope and boundary (cloud-prepress-orchestration)

- Target: `platform-infra`, head `9f3c2a1`, base `main`.
- Environment: `test`; subscription alias `sub-reports-test`; region `eastus2`; resource group `rg-reports-test`; state in the azurerm backend under key `reports/test.tfstate`.
- Authorization: read the repository and the CI logs. No live read-only queries, no plan run by the reviewer, and no apply.
- Design inputs: `CONSTRAINTS.md` (allowed regions, required tags, a USD 150/month ceiling for `test`), `TOPOLOGY.md`, and the runbook `docs/runbooks/reports-storage.md`.

## 2. Scope and blast radius (change-scope-and-impact)

```text
$ git diff --name-status main...feature/reports-private-endpoint
M       envs/test/main.tf
A       envs/test/moved.tf
M       envs/test/variables.tf
A       modules/private-storage/main.tf
A       modules/private-storage/variables.tf
A       modules/private-storage/outputs.tf
M       docs/runbooks/reports-storage.md
```

The storage account is stateful: per the runbook, it holds report history. The address change is the main risk, so the reviewer reads `envs/test/moved.tf` first:

```hcl
moved {
  from = azurerm_storage_account.reports
  to   = module.reports_storage.azurerm_storage_account.this
}
```

To find consumers, the reviewer searches the repository for the account name. The only hits are the module and `envs/test/app.tf`, which is unchanged but inspected for this reason. In that file, `reports-api` has `virtual_network_subnet_id` set and `vnet_route_all_enabled = true`, so it reaches the account through the spoke VNet. No workflow in the repository writes to the account.

## 3. IaC, policy and identity (iac-policy-and-identity-review)

- The provider constraint stays `~> 4.0`, and `.terraform.lock.hcl` is unchanged.
- The module sets `public_network_access_enabled = false`. It creates `azurerm_private_endpoint.blob`, whose DNS zone group points at the hub `privatelink.blob.core.windows.net` zone, read through a data source. It also creates `azurerm_monitor_diagnostic_setting.blob`, which sends the `allLogs` category group to Log Analytics.
- Tags come from `local.tags` and carry `owner`, `cost-center` and `env`, as `CONSTRAINTS.md` requires.
- The account has neither `lifecycle { prevent_destroy = true }` nor a delete lock.
- The diff and the plan contain no role assignments, no policy assignments and no exemptions.
- Per `CONSTRAINTS.md`, the subscription carries an `audit` assignment requiring storage accounts to disable public network access, and the management group carries a `deny` allowed-locations assignment. By design the change satisfies both. Live assignment state and compliance are not verified, because static IaC cannot prove them.

## 4. Preview (deployment-preview-and-environment-review)

The reviewer reads the plan from the CI job log, where Terraform prints sensitive values as `(sensitive value)`. The saved plan file is not downloaded, because saved plans can carry sensitive values. The log header shows run 4812 of `plan-test` at commit `9f3c2a1`, using the `id-tf-plan-test` identity against key `reports/test.tfstate`.

```text
  # module.reports_storage.azurerm_monitor_diagnostic_setting.blob will be created
  # module.reports_storage.azurerm_private_endpoint.blob will be created

  # module.reports_storage.azurerm_storage_account.this will be updated in-place
  # (moved from azurerm_storage_account.reports)
  ~ resource "azurerm_storage_account" "this" {
        name                          = "streportstest01"
      ~ public_network_access_enabled = true -> false
        # (34 unchanged attributes hidden)
    }

Plan: 2 to add, 1 to change, 0 to destroy.
```

The preview matches the reviewed head, environment, backend and scope. Every change traces to the diff, and the move produces no destroy.

One question the preview cannot answer: the CI runner is a GitHub-hosted runner outside the VNet. If the pinned provider reads data-plane properties of the account during refresh, the next `plan-test` run would be refused once public access is off. The reviewer cannot prove this from the evidence available, so it is recorded as a validation hypothesis with a cheap check, not as a confirmed defect.

## 5. Tests and build (tests-build-and-dependency-review)

The checks ran in a scratch copy of the repository, so `.terraform/` never appeared in the working tree:

```text
$ terraform fmt -check -recursive
$ echo $?
0
$ terraform init -backend=false -input=false >/dev/null && terraform validate
Success! The configuration is valid.
```

The repository defines neither tflint nor an IaC scanner, so both are recorded as skipped.

## 6. Rollback, operations and cost

- **Rollback (operability-resilience-and-rollback-review).** A plain `git revert` would take the `moved` block away with the module and plan a destroy and re-create of the storage account. The updated runbook avoids that: its rollback is a forward change, kept on branch `rollback/reports-public-access`, that keeps the module address and re-enables public access. That branch has no captured plan, so the rollback is labelled `designed`. No data migration is involved, so there is no point of no return.
- **Cost (cost-allocation-and-governance-review).** The pull request description estimates the current spend at about USD 112/month, and the private endpoint at about USD 8/month plus data processing. Both figures are the author's estimates and were not checked against current pricing. Log Analytics ingestion for `allLogs` is missing from the estimate. The total stays under the USD 150 ceiling unless that ingestion exceeds roughly USD 30/month.

## 7. Report and gate (review-report-and-pr-gate)

There is no confirmed defect. The Medium item is a hypothesis with a post-deployment check, and two Low follow-ups are left for the deployment reviewer to accept or fix. The gate is `READY_FOR_DEPLOYMENT_REVIEW`. It is not apply authorization, and the reviewer does not run apply.

## Completion report

### Scope and inputs

| Item | Value |
|---|---|
| Repository and refs | `platform-infra`, base `main`, head `feature/reports-private-endpoint` at `9f3c2a1` |
| Change intent | Move the reports storage account into a module, disable public network access, add a private endpoint and diagnostics |
| Change class | infrastructure, networking |
| Target environment | `test`, subscription `sub-reports-test`, `eastus2`, resource group `rg-reports-test`, backend key `reports/test.tfstate` |
| Requirements and design | `CONSTRAINTS.md`, `TOPOLOGY.md`, `docs/runbooks/reports-storage.md` |
| Owner | Change: platform team. Resource: reports team (`owner` tag). |
| Authorization boundary | Read-only review of the repository and CI logs. No live read-only queries, no reviewer-run plan, no apply, import, force-unlock, RBAC or policy change. |
| Report location | `../reviews/platform-infra/reports-private-endpoint/REVIEW.md` |

### Changed paths and methods

| Path | Change class | Review method |
|---|---|---|
| `envs/test/moved.tf` (added) | infrastructure | Read; matched against the plan's move line |
| `envs/test/main.tf`, `envs/test/variables.tf` | infrastructure | Read diff; traced the module call and inputs |
| `modules/private-storage/*.tf` (added) | infrastructure, networking | Read in full; checked network, tags, diagnostics and lifecycle |
| `docs/runbooks/reports-storage.md` | documentation | Checked rollback against Terraform address semantics |

Paths inspected outside the diff, and why:

- `envs/test/app.tf`: the only consumer of the account; checked its VNet integration.
- `CONSTRAINTS.md`, `TOPOLOGY.md`: regions, tags, cost ceiling, policy assignments, hub DNS link.

### Evidence ledger

| Evidence | Label | Source, command or capture | Bound to |
|---|---|---|---|
| Seven changed files and a `moved` block | observed | `git diff --name-status main...feature/reports-private-endpoint` | `9f3c2a1` |
| Formatting and configuration validity | structurally-validated | `terraform fmt -check -recursive`, `terraform validate`, both exit 0 | `9f3c2a1` |
| Plan: 2 add, 1 change, 0 destroy; move without replacement | preview-verified | CI `plan-test` run 4812 log, identity `id-tf-plan-test` | `9f3c2a1`, `rg-reports-test` |
| Consumer reaches the account through the VNet | observed | `envs/test/app.tf` VNet integration settings | `9f3c2a1` |
| Hub private DNS zone linked to the spoke VNet | designed | `TOPOLOGY.md` | not bound |
| Policy assignments as documented | designed | `CONSTRAINTS.md` | not bound |
| Live policy compliance and DNS resolution | not-verified | No live read authorized | not bound |
| Rollback branch plan | designed | Runbook; no captured plan | not bound |
| Cost figures | designed | Author's estimate in the pull request description | not bound |

### Findings

#### Next plan from the hosted runner may be refused once public access is off

| id | severity | status | file | line |
|---|---|---|---|---|
| F1 | Medium | validation-hypothesis | `modules/private-storage/main.tf` | 14 |

- **scenario:** `plan-test` runs on a GitHub-hosted runner outside the VNet. If the pinned provider reads data-plane properties of the account during refresh, every plan after this deployment would be refused with an authorization error.
- **impact:** Later changes to this environment could not be planned from CI. Data and the running application are unaffected.
- **recommendation:** Check the behavior after the test deployment. If plans are refused, run `plan-test` from the self-hosted runner pool in the spoke VNet before this change goes to other environments.
- **verification:** The first `plan-test` run after deployment completes and shows no changes.

#### Diagnostic setting sends all log categories with no cost line

| id | severity | status | file | line |
|---|---|---|---|---|
| F2 | Low | confirmed | `modules/private-storage/main.tf` | 41 |

- **scenario:** The diagnostic setting enables the `allLogs` category group for the blob service. Read-heavy report downloads generate a `StorageRead` record per request, and the cost estimate has no Log Analytics line.
- **impact:** Ingestion cost is unbounded in the estimate and could push `test` toward the ceiling.
- **recommendation:** Limit categories to `StorageWrite` and `StorageDelete`, or add an ingestion estimate to the cost note.
- **verification:** The cost note includes a Log Analytics figure with its source, or the plan shows the narrowed categories.

#### Stateful storage account has no deletion protection

| id | severity | status | file | line |
|---|---|---|---|---|
| F3 | Low | confirmed | `modules/private-storage/main.tf` | 3 |

- **scenario:** The account holds report history. Neither `prevent_destroy` nor a `CanNotDelete` lock protects it, so a future address change without a `moved` block would plan a destroy.
- **impact:** Plan review is the only safeguard against losing report history. Rated Low for `test`; it rises to Medium before production.
- **recommendation:** Add `lifecycle { prevent_destroy = true }` to the account in the module, or a management lock.
- **verification:** A plan of a branch that removes the `moved` block fails on `prevent_destroy`.

### Skipped checks and limits

| Check | Why skipped or limited | Effect on the recommendation |
|---|---|---|
| Reviewer-run plan or live read | Not authorized; CI plan used instead | Preview evidence is the CI capture only |
| tflint and IaC scanner | The repository defines neither | Static coverage limited to `fmt` and `validate` |
| Live policy compliance | Static review cannot prove it | Post-deployment check handed to the operator |
| Rollback branch plan | Not captured | Rollback stays `designed` |
| Pre-review and post-review helpers | Not installed on the review machine | Report checked by reading against the contract |

### Architecture and ADR status

Aligned with `TOPOLOGY.md`, which shows reports storage behind a private endpoint with the hub DNS zone. No ADR is contradicted, and none is needed.

### Security, IaC, policy and identity status

- Public network access is disabled, and access moves to a private endpoint. That narrows exposure.
- No identity, role assignment, policy assignment or exemption changes.
- The state address moves through a `moved` block. The plan confirms no destroy or replace.
- The provider constraint and lock file are unchanged.
- Policy: by design the change satisfies the documented public-access audit and allowed-locations deny assignments. Live compliance is not verified.

Secret handling: the diff and the CI log were read for keys, tokens and connection strings. Sensitive plan values appear only as `(sensitive value)`, the saved plan file was not downloaded, and no secret value appears in this report.

### Tests, build and preview status

| Check | Command or source | Result | Label |
|---|---|---|---|
| Format | `terraform fmt -check -recursive` | exit 0 | structurally-validated |
| Validate | `terraform validate` after `init -backend=false` | exit 0 | structurally-validated |
| Plan | CI `plan-test` run 4812 | 2 add, 1 change, 0 destroy | preview-verified |

Preview change counts: create 2, modify 1, delete 0, replace 0, moved 1. Captured at `9f3c2a1` against `rg-reports-test` with backend key `reports/test.tfstate`.

### Operations, rollback, cost and inputs

- Observability and ownership: diagnostics go to the environment's Log Analytics workspace. The reports team owns the account.
- Rollback boundary: a forward rollback on `rollback/reports-public-access` keeps the module address and re-enables public access. A plain revert is unsafe, because it removes the `moved` block. There is no point of no return: no data moves. Label: designed.
- Cost: about USD 120/month by the author's estimate, against a USD 150 ceiling. Log Analytics ingestion is not estimated (the Low diagnostics finding).
- New required inputs: `private_endpoint_subnet_id` and `log_analytics_workspace_id`, both resource IDs, neither a secret.

### Unresolved risks and human blockers

| Item | Type | Owner | Needed to clear |
|---|---|---|---|
| Live policy compliance after deployment | open risk | platform on-call | Compliance shows the account as compliant after the next evaluation |
| Private DNS resolution from `reports-api` | open risk | platform on-call | Post-deployment lookup returns a private address |
| Two Low follow-ups | open risk | deployment reviewer | Accepted for `test`, or fixed before apply |

No human decision blocks the deployment review.

### Recommendation

READY_FOR_DEPLOYMENT_REVIEW

The preview matches the reviewed commit and scope, the move causes no destroy, and no confirmed defect remains. This is not apply authorization: the deployment reviewer and the `apply-test` environment gate decide.

### Engineer handoff

- Next actor: the `test` deployment reviewer on the platform team.
- Actions, in order: accept or fix the two Low follow-ups; approve `apply-test` through its environment gate; after apply, confirm DNS resolution from `reports-api`, a successful report download, policy compliance, and a clean next `plan-test` run, which settles the Medium hypothesis.
- Evidence the next actor receives: this report, the CI `plan-test` run 4812 log, and the runbook.
- Re-review trigger: new commits on the branch, a new plan, or a decision to promote the change beyond `test`.
- Not done by this review: no plan run by the reviewer, no apply, no live read.
