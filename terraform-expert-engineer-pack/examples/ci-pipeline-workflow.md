# Worked example: GitHub Actions plan on pull request, gated apply on main

Prompt: `build-terraform-pipeline.prompt.md`. Skills: terraform-ci-cd-and-quality, terraform-testing-and-validation.

This is a synthetic walkthrough. The organization, roles and versions are illustrative. Commands and outputs show what the agent would run and see; they are not results recorded by this pack's validation. Part of the outcome is unverified: the workflow has never run on GitHub.

## Request

> Add a GitHub Actions workflow to `example-org/infra`. Plan on pull requests for the environments that changed, and apply to prod after someone approves. No long-lived AWS keys.

## 1. Establish the contract

| Fact | Value |
|---|---|
| Roots | `envs/staging`, `envs/prod`; both call `modules/*` |
| Backends | S3 with lockfile locking; keys `infra/staging.tfstate` and `infra/prod.tfstate` |
| Terraform | `required_version = "~> 1.9"`; CI pins 1.9.8 |
| Identity | AWS roles `gha-tf-plan` (read, state read, lock write) and `gha-tf-apply`. Their trust policies live in another repository the agent cannot read |
| Repository policy | actions pinned to full commit SHAs; tflint already configured |
| Authorization | write the workflow on a branch; run local checks; no push, no settings changes |

## 2. Stage design

| Stage | Proves | Does not prove |
|---|---|---|
| Changed roots | which roots to plan; any change outside `envs/<root>/` plans every root | that unchanged roots have no drift |
| `terraform fmt -check -recursive` | formatting | correctness |
| `terraform init` (real backend) and `terraform validate` | the configuration is consistent and the providers match the lock file | API behaviour |
| `tflint --recursive` | the configured lint rules | anything the rules do not cover |
| `terraform test` (mocked unit tests) | module logic | provider or API behaviour |
| `terraform plan -out=tfplan` | the change set for this commit, state and variables | the apply result |
| Plan summary | addresses and actions for reviewers | values (they are deliberately left out) |
| Environment approval | a named person accepted this plan | that the plan is safe; the reviewer must still read it |
| `terraform apply tfplan` | the reviewed plan, applied, or rejected as stale if state moved | anything beyond this run |

Path filtering is deliberately coarse. A change to `modules/`, `.terraform.lock.hcl`, the workflow file or the tflint configuration plans both roots, so a shared change cannot skip checks.

## 3. Workflow (excerpt)

The steps for checkout, Terraform setup, AWS credentials and artifacts use SHA-pinned actions copied from the repository's existing `release.yml`. The agent looked up no SHAs online. Those steps are left out here.

```yaml
name: terraform
on:
  pull_request:
  push:
    branches: [main]

permissions:
  contents: read

jobs:
  plan:
    needs: changes
    strategy:
      matrix:
        root: ${{ fromJSON(needs.changes.outputs.roots) }}
    concurrency:
      group: tf-state-${{ matrix.root }}
      cancel-in-progress: false
    permissions:
      contents: read
      id-token: write
    defaults:
      run:
        working-directory: envs/${{ matrix.root }}
    steps:
      # checkout, setup-terraform (1.9.8), configure-aws-credentials (gha-tf-plan): SHA-pinned, omitted
      - run: terraform fmt -check -recursive
      - run: terraform init -input=false
      - run: terraform validate
      - run: tflint --recursive
      - run: terraform test
      - run: terraform plan -input=false -out=tfplan
      - name: Plan summary without values
        run: |
          terraform show -json tfplan \
            | jq -r '.resource_changes[] | select(.change.actions != ["no-op"]) | "\(.change.actions | join(",")) \(.address)"' \
            >> "$GITHUB_STEP_SUMMARY"
          sha256sum tfplan > tfplan.sha256
      # upload tfplan and tfplan.sha256 only on push to main, retention-days: 1

  apply:
    if: >-
      github.event_name == 'push' && github.ref == 'refs/heads/main' &&
      contains(fromJSON(needs.changes.outputs.roots), 'prod')
    needs: [changes, plan]
    environment: production
    concurrency:
      group: tf-state-prod
      cancel-in-progress: false
    permissions:
      contents: read
      id-token: write
    defaults:
      run:
        working-directory: envs/prod
    steps:
      # checkout, setup-terraform, configure-aws-credentials (gha-tf-apply), download artifact: omitted
      - run: sha256sum -c tfplan.sha256
      - run: terraform init -input=false
      - run: terraform apply -input=false tfplan
```

Design points:

- **Identity.** OIDC only, so there are no secrets in the repository. `id-token: write` is granted per job, not workflow-wide. Fork pull requests get no OIDC token. The workflow does not use `pull_request_target`, which would run untrusted Terraform code with credentials.
- **Plan and apply are tied together.** On main, apply uses the saved plan from the same workflow run, so the commit, variables, lock file and backend are the same. The checksum guards the artifact. If state changed after the plan, Terraform rejects the saved plan as stale, and the next push plans again.
- **Concurrency.** The plan for prod and the apply share the group `tf-state-prod`. An apply in progress is never cancelled. A newer pending run replaces an older pending one, which is acceptable because the older plan would be stale anyway.
- **Plan artifact.** It holds sensitive values. It is uploaded only on main, kept one day, and readable by anyone with read access to this private repository. That residual risk is recorded below.
- **Summaries.** Plan summaries go to the job summary, by action and address. Posting PR comments would need `pull-requests: write` and would invite pasting full plans.

## Completion report

Outcome: workflow written and locally linted. It has not run on GitHub, and the protections it relies on are not configured yet.

### objective

Plan changed environments on pull requests, and apply prod only after approval, with no long-lived AWS keys.

### scope_and_authorization

| Item | Value |
|---|---|
| Configuration directories | `envs/staging`, `envs/prod`, `modules/*` |
| Environments | staging and prod accounts (synthetic) |
| Terraform | 1.9.8 pinned in CI |
| Providers | unchanged; the lock file is honoured by `init` |
| Backend | S3, `infra/staging.tfstate` and `infra/prod.tfstate` |
| Execution mode | GitHub Actions |
| Authorization | write the workflow on branch `ci/terraform`; local checks |
| Not authorized | push, triggering runs, creating the `production` environment or its reviewers, changing IAM trust |

### changed_files

| File | Change |
|---|---|
| `.github/workflows/terraform.yml` | new; jobs `changes`, `plan`, `apply` |

### commands_and_results

| Command | Directory | Exit | Result |
|---|---|---|---|
| `actionlint .github/workflows/terraform.yml` | repository root | 0 | no findings |
| `terraform fmt -check -recursive` | repository root | 0 | clean |
| `terraform init -backend=false` then `terraform validate` | `envs/staging`, `envs/prod` | 0 | valid |
| `tflint --recursive` | repository root | 0 | no findings |
| `terraform test` | `modules/log-bucket` | 0 | 5 passed |

Not run: the workflow itself on GitHub; `terraform plan` with `gha-tf-plan` (no OIDC token is available locally); any apply.

### plan_or_state_impact

None. No plan was produced against either backend, and no state was read or written.

### evidence_classification

| Claim | Class | Evidence |
|---|---|---|
| Workflow syntax and expressions are valid | local | `actionlint` |
| The Terraform checks the workflow runs pass today | local | the same commands run locally |
| Jobs authenticate through OIDC with the intended roles | unavailable | trust policies not readable; workflow not run |
| The `production` environment requires a reviewer | unavailable | not configured; repository settings are out of scope |
| A stale saved plan is rejected at apply | inferred | documented Terraform behaviour; not exercised here |

### risks_and_limitations

Until a repository admin creates the `production` environment with required reviewers, the apply job has no human gate. The workflow must not merge before then. The plan artifact is readable by anyone with repository read access for one day. Staging has no apply job yet; it was outside the request.

### next_safe_action

A repository admin creates the `production` environment with required reviewers, and restricts it to `main`. The platform team confirms that the `gha-tf-plan` and `gha-tf-apply` trust policies are scoped to `repo:example-org/infra`, with the apply role limited to the `production` environment. Then the requester pushes the branch and opens a pull request, so the plan job runs for the first time.
