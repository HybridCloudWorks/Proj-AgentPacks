---
description: "Build or review a Terraform CI/CD pipeline with ordered quality gates and a protected apply"
agent: terraform-expert-engineer
---

# Build a Terraform pipeline

## Inputs

- The CI platform (GitHub Actions, GitLab CI or another) and the existing pipeline, if any.
- The root configurations, environments, backends and state keys, and the modules they share.
- How the pipeline authenticates (prefer short-lived federated identity), the repository's action and tool pinning policy, and who approves applies.

## Workflow

1. Apply terraform-ci-cd-and-quality and order the stages: identify changed roots, install the pinned Terraform version, authenticate with short-lived identity, initialize the intended backend (backend-disabled for module-only checks), check formatting, validate, run lint and security checks, run unit or mock tests, plan, check policy, review, then apply only through a protected gate.
2. Make path filtering safe: changes to shared modules, backends, providers, the lock file, policies or the pipeline itself must trigger the checks they affect.
3. Keep state and plan files out of logs and ordinary artifacts. Restrict artifact access and retention, or use the platform's secure plan and apply mechanism. Publish plan summaries by address and action, not full plans.
4. Use one concurrency group per state so two writers never meet, and never cancel an apply in progress.
5. Tie apply to an approved plan from the same commit, backend, workspace or state key, variables, provider lock and policy result. Plan again when any of them changes. Do not auto-apply production unless the repository owner has designed, protected and approved that.
6. Add tests with terraform-testing-and-validation, policy gates with terraform-policy-and-governance, and HCP-driven runs with terraform-cloud-and-stacks.

Do not push, trigger pipeline runs, or change branch protection, environments or secrets without authorization.

## Expected output

The pipeline diff; a stage table saying what each stage proves and what it does not; the identity and permission scope of each job; plan artifact handling; the apply gate; which checks were executed locally and which run only on the CI platform; and a completion report. A pipeline that has not run is not reported as green. Follow the `terraform-expert-engineer-contract` instruction.
