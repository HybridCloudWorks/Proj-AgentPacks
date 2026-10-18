# Worked example: Terraform plans for fork pull requests

Synthetic walkthrough. The repository, SHAs, line numbers and command output are illustrative; nothing was run against real infrastructure.

- Prompt: `review-deployment-pipeline.prompt.md`
- Skills: `review-infrastructure-pr`, `review-cicd-deployment`, `review-terraform-opentofu`, `verify-infrastructure-evidence`
- Outcome: Changes requested

## Request

> Contributors from forks never get a plan comment. PR #233 in `network-core` fixes that. I tested it in my fork and it works. Review it before we merge.

## The change

Base `71ad0c4`, head `0e93b5f`. One file, `.github/workflows/terraform-plan.yml`, 14 added and 5 deleted lines. The core of the diff, with new-file line numbers on the left:

```diff
 1  on:
 2 -  pull_request:
 2 +  pull_request_target:
 3      paths: ['terraform/**']
 4  permissions:
 5    id-token: write
 6    contents: read
 7    pull-requests: write
 8 +concurrency:
 9 +  group: terraform-plan-${{ github.ref }}
10 +  cancel-in-progress: true
11  jobs:
12    plan:
13      runs-on: ubuntu-latest
14      environment: prod-plan
15      steps:
16        - uses: actions/checkout@v4
17 +        with:
18 +          ref: ${{ github.event.pull_request.head.sha }}
19        - uses: hashicorp/setup-terraform@v3
       - uses: azure/login@v2
         with:
           client-id: ${{ vars.PLAN_CLIENT_ID }}
           tenant-id: ${{ vars.TENANT_ID }}
           subscription-id: ${{ vars.PROD_SUBSCRIPTION_ID }}
       - run: terraform -chdir=terraform init -backend-config=backends/prod.hcl
       - run: terraform -chdir=terraform plan -no-color -out=tfplan
```

The remaining changed lines rewrite the plan-comment step and are covered in the ledger.

## Walkthrough

1. **Trust map (`review-cicd-deployment`).** Before: `pull_request` from a fork receives no OIDC token and no secrets, so fork plans failed at `azure/login`, which is the symptom the PR addresses. After: `pull_request_target` runs the workflow definition from the base branch with the base repository's permissions, including `id-token: write`, for every pull request, forks included. The new checkout step then puts the fork's head commit in the workspace.
2. **What runs from the fork.** `terraform init` and `terraform plan` evaluate the fork's configuration. A fork can add a `data "external"` source, which runs an arbitrary program during plan, or a provider of its choosing. That code runs after `azure/login`, so it can use the federated token.
3. **Identity reach.** `infra/identity/plan-federation.tf` defines the federated credential for `PLAN_CLIENT_ID` with subject `repo:<org>/network-core:environment:prod-plan`, which this job satisfies because it declares `environment: prod-plan`. The same file grants the identity `Reader` on the production subscription and `Storage Blob Data Reader` on the state container. Terraform state for `prod` contains the VPN pre-shared keys that `terraform/vpn.tf` marks sensitive; sensitivity markings do not remove values from state.
4. **Why the fork test proves nothing here.** The attached log is from the author's fork, where the workflow file is on the default branch and the identity, environment and variables are the fork's own. It is evidence from another repository and identity (`verify-infrastructure-evidence`, artifact integrity) and does not show behavior in `network-core`. It also cannot show the risk, because the attack needs a third party's fork.
5. **Concurrency.** Under `pull_request_target`, `github.ref` is the base branch, so every PR's plan shares the group `terraform-plan-refs/heads/main`, and `cancel-in-progress` cancels one PR's plan when another starts. `terraform plan` takes the state lock by default. A plan cancelled while holding the lock may release it on interrupt, but a runner that is stopped before Terraform exits leaves the lock held, and the next apply on `main` fails until someone force-unlocks.
6. **Not a finding.** `actions/checkout@v4`, `hashicorp/setup-terraform@v3` and `azure/login@v2` use major-version tags, which is unchanged by this PR and below the threshold for a new finding.
7. **Checks.** actionlint skip (not installed); YAML lint pass. Neither evaluates trust boundaries.

## Completion report

### Executive Summary

- Overall assessment: The change runs untrusted fork code with a federated identity that can read production state containing secrets.
- Highest-risk finding: F-01, Keep fork pull-request code out of jobs that hold the production plan identity.
- Reviewed transition: plan workflow moved from `pull_request` to `pull_request_target` with a head-commit checkout.
- Release or merge readiness: Not ready; a Critical finding.

### Review Scope

- Base and head: `71ad0c4` → `0e93b5f`
- Files and technologies: `.github/workflows/terraform-plan.yml` (GitHub Actions running Terraform)
- Entry points and execution order: pull request event → `plan` job → `azure/login` (OIDC) → `terraform init` with the production backend → `terraform plan` → plan comment
- Targets, identities, state, and ownership: production subscription; `PLAN_CLIENT_ID` federated identity with Reader and state-read roles; state container from `backends/prod.hcl`
- Evidence reviewed: workflow diff, `infra/identity/plan-federation.tf`, `terraform/vpn.tf`, the author's fork run log
- Constraints and exclusions: `prod-plan` environment protection rules are repository settings and are not visible in the code

### Coverage and Evidence

- Changed lines: 19 / 19
- Deletions, renames, generated artifacts, mode, or binary changes: the deleted `pull_request` trigger and plain checkout, both replaced
- Cross-tool handoffs reviewed: workflow identity → Terraform backend and providers
- Existing-environment evidence: not required for these findings
- Missing or non-authoritative evidence: the fork run log is from a different repository and identity
- Checks: actionlint skip (not installed); yamllint pass

### Findings Summary

`Critical: 1 · High: 0 · Medium: 1 · Low: 0 · Evidence gaps: 0`

### Findings

```text
Finding ID: F-01
Severity: Critical
Confidence: High
File: .github/workflows/terraform-plan.yml
Location: line 2 (new trigger) with lines 17-18 (head checkout)
Technology: GitHub Actions, Terraform
Category: Security and secrets
Title: Keep fork pull-request code out of jobs that hold the production plan identity
Execution path or trigger: Any pull request from any fork that touches terraform/** after this workflow reaches main.
Description: pull_request_target grants the base repository's id-token permission and the prod-plan environment, and the job then checks out and runs terraform plan on the fork's code, which can execute arbitrary programs through external data sources or providers.
Impact: An outside contributor obtains the production plan identity and can read production state, including the VPN pre-shared keys.
Remediation direction: Keep untrusted plans on pull_request without credentials, or split the flow so a privileged job runs only after a maintainer approves a specific commit, against a read identity that cannot read sensitive state. Never combine pull_request_target with a checkout of the pull request head in a job that has credentials.
Verify with: workflow diff showing no credentialed job checks out pull-request code, and the federated credential subject no longer satisfiable from a pull-request event.
```

```text
Finding ID: F-02
Severity: Medium
Confidence: Medium
File: .github/workflows/terraform-plan.yml
Location: lines 8-10 (new)
Technology: GitHub Actions, Terraform state locking
Category: Concurrency and locking
Title: Scope plan concurrency per pull request and do not cancel jobs holding the state lock
Execution path or trigger: Two pull requests updated within the duration of one plan.
Description: github.ref resolves to the base branch for pull_request_target, so all plans share one group and cancel each other; a plan stopped before Terraform exits can leave the production state lock held.
Impact: Plans for unrelated PRs are lost, and a stranded lock blocks the next production apply until a force-unlock.
Remediation direction: Key the group on the pull request number and avoid cancel-in-progress for jobs that take the state lock.
Verify with: two concurrent PR updates producing two completed plans and no lock left in the state backend.
```

### Evidence Gaps

None. The fork log was set aside as non-authoritative rather than requested again, because no artifact would clear F-01.

### Residual Risk

Whether `prod-plan` has required reviewers is a repository setting that was not visible; F-01 stands either way, because a reviewer approving the environment for a fork's run cannot see what the fork's plan executes.

### Disposition

Changes requested

### Handoff

- Required corrections: F-01 (Critical) lines 2 and 17-18; F-02 (Medium) lines 8-10.
- Suggested work order: redesign the trust split for F-01 first; F-02's concurrency key depends on the event the final design uses.
- Validation required after fixes: workflow review of the new design; a test PR from a fork showing the credentialed step does not run without maintainer approval.
- Human decisions or approvals: whether fork contributors should receive production-backed plans at all is a policy decision for the repository owners.
- Configuration and operational dependencies: confirm `prod-plan` environment protection, and install actionlint in the review environment.
