# Worked example: blocked Terraform change for production

Synthetic scenario. The repository, commits and identities are illustrative. Prompt: `review-iac-and-deployment-plan.prompt.md`. This example ends **blocked**.

## Request

"Review PR 142 in contoso/tracking-infra and apply it to production tonight."

Supplied: the PR diff, `plan.txt` attached to the PR by the pipeline, the workflow file `.github/workflows/terraform.yml`, and the repository, which includes `bootstrap/identity.tf` (the deployment identities and their federated credentials). No Azure credentials were offered to the agent.

The request combines a read-only review with a production apply. The agent did the review first. The apply is handled in section 4.

## 1. Evidence gathered (read-only)

- PR head is `e4f5a6b`. Pipeline run 8812, which produced `plan.txt`, checked out `a1b2c3d`, the PR's first commit. Two later commits changed `sql.tf` [observed: run summary and commit list].
- Local checks, which need no cloud credentials:

```text
> terraform fmt -check -recursive
(exit 0)
> terraform init -backend=false
Terraform has been successfully initialized!
> terraform validate
Success! The configuration is valid.
```

These are [structurally-validated]. No plan was run: that needs backend and subscription access, which was not granted.

## 2. Findings

From `azure-iac-avm-and-repo-standardization`, `azure-deployment-and-lifecycle` and `azure-security-identity-and-compliance`:

| ID | Severity | Location | Finding | Evidence | Blocks |
|---|---|---|---|---|---|
| F1 | Critical | `main.tf:41`, `sql.tf:3` | The module is renamed from `module.sql` to `module.sql_server` with no `moved` block, and the server `name` changes from `sql-tracking-prod-weu` to `sqls-tracking-prod-weu` to follow a new naming convention. The plan destroys the production SQL server and its databases and creates new ones. | `plan.txt`: `module.sql.azurerm_mssql_server.this will be destroyed`, `module.sql_server.azurerm_mssql_server.this will be created`, `Plan: 7 to add, 0 to change, 7 to destroy.` [observed] | Yes |
| F2 | High | Pipeline run 8812 | The plan is for `a1b2c3d`, not the head `e4f5a6b`. No plan exists for the code that would be applied. | Run summary [observed] | Yes |
| F3 | High | `.github/workflows/terraform.yml:18`, `bootstrap/identity.tf:27` | The PR plan job and the production apply job use the same identity. Its federated credential subject is `repo:contoso/tracking-infra:pull_request` and it holds Contributor on `sub-tracking-prod`, so any pull-request run can obtain a production write token. | Workflow file and bootstrap code [observed]; the live federated credential was not inspected [not-verified] | Yes |
| F4 | Medium | `versions.tf:9` | The `azurerm` provider constraint moves from `~> 3.116` to `~> 4.0` in the same PR as the state refactor. A major provider upgrade and a refactor in one plan make each change hard to attribute. | Diff [observed]; upgrade notes for 4.x not retrieved [not-verified] | No; split recommended |
| F5 | Medium | `modules/sql/main.tf` | No `prevent_destroy` on the server or databases, so nothing in the code stops F1. | Diff [observed] | No |
| F6 | Low | Repository | No CHANGELOG entry or ADR for the naming convention change; `tflint` is not in CI. | Repository tree [observed] | No |

## 3. Remediation for the author

The fixes belong to the PR author; the agent proposes them and does not push.

```hcl
moved {
  from = module.sql
  to   = module.sql_server
}
```

- Revert the server name to `sql-tracking-prod-weu`. Record a naming exception in `CONSTRAINTS.json`: the existing server keeps its name and the new convention applies to new servers. A live, globally unique resource is not renamed to chase a convention.
- Add `lifecycle { prevent_destroy = true }` to the server and databases in the local module. A `CanNotDelete` management lock is a separate decision for the platform team.
- Move the provider upgrade to its own PR with its own plan.
- Split identities: a plan identity federated to `pull_request`, with read access to the subscription and only the state access the backend needs for locking; an apply identity federated to `environment:prod`, with Contributor on the tracking resource groups only, behind the GitHub environment's required reviewers.
- Add `tflint` to CI and a CHANGELOG entry (additive standardization, not blocking).

## 4. The apply request

Not performed. The user asked for it, but the evidence makes it unsafe:

1. F1 would destroy the production database.
2. F2 means there is no plan for the code that would run.
3. F3 means the pipeline path is over-privileged.

The agent also holds no credentials for the production scope, and a production apply belongs in the pipeline behind its environment gate, not in an agent shell. Before an apply can be considered, the agent asked for:

- a plan for the fixed head commit showing no destroy or replace on any stateful resource
- a confirmed restore point for the production database
- the named approver for the `prod` environment and the change window
- explicit confirmation that the apply runs through the pipeline after those three exist

## Completion report

- Pack: azure-cloud-architect
- Workflow: `review-iac-and-deployment-plan.prompt.md`
- Outcome: **blocked**. The review is complete. The production apply was not performed, because the plan would destroy the production SQL server, the plan is stale, and the deployment identity is over-privileged.

### scope_and_inputs

PR 142 in contoso/tracking-infra (head `e4f5a6b`), the attached plan from run 8812, the workflow file and the bootstrap identity code. Authority: review. A production apply was requested without credentials, plan evidence for the head, or a rollback point.

### business_outcomes_and_requirements

Adopt the new naming convention and refactor the SQL module without losing data or availability (REQ-NFR-01, 99.9 % SLO; AC-DEP-01, every change through the pipeline with plan evidence).

### source_facts_and_evidence

Plan output, run summary, diff and repository files [observed]. Live federated credential configuration [not-verified]. azurerm 4.x upgrade notes not retrieved [not-verified].

### framework_alignment

Reliability: F1 is a data-loss path. Security: F3 is a privilege-escalation path from any PR. Operational Excellence: F2 and F4 break the link between reviewed plan and applied change. Cost and Performance: no material effect.

### proposed_architecture

No architecture change. Recommended change: `moved` block, name reverted with a recorded exception, `prevent_destroy`, provider upgrade split out, and separate plan and apply identities [designed].

### assumptions_and_tradeoffs

Assumed `bootstrap/identity.tf` matches the live identity configuration (F3); it was not checked live. Keeping the legacy server name trades naming consistency for zero data migration.

### implementation_and_operating_implications

The author updates the PR. The platform team changes the federated credentials and role assignments (GATE-02). The pipeline produces a new plan for the head commit. The production apply runs only through the `prod` environment gate.

### security_resilience_cost_and_sustainability

Security: F3 must be fixed before any production apply from this repository. Resilience: a restore point is required before apply, and `prevent_destroy` guards against a repeat. Cost: none. Sustainability: none.

### output_files

| File | Purpose | Status and label |
|---|---|---|
| Review findings F1 to F6 | Located findings with remediation | delivered in this report [observed] |
| REQ.md, TOPOLOGY.json, ADR.md | Unchanged by this review | not applicable: no architecture decision changed |
| CONSTRAINTS.json | Naming exception for the legacy server name | change proposed to the author, not written [designed] |

### live_or_external_checks

| Check | Command or source | Result | Label |
|---|---|---|---|
| Format | `terraform fmt -check -recursive` | exit 0 | structurally-validated |
| Configuration validity | `terraform init -backend=false`, `terraform validate` | exit 0 | structurally-validated |
| Plan for head commit | not run: no credentials, not authorized | none | not-verified |
| Live federated credential subjects | not run: no Entra access | none | not-verified |
| Database restore point | not run | none | not-verified |

### unresolved_risks

If someone applies `plan.txt` or the current head through the pipeline as it stands, the production database is destroyed. F3 stays exploitable until the identities are split.

### next_safe_action

The PR author adds the `moved` block, reverts the server name and splits out the provider upgrade; the pipeline then produces a plan for the new head, which comes back for review. No apply until that plan shows no destroy on stateful resources and the platform team has fixed F3.
