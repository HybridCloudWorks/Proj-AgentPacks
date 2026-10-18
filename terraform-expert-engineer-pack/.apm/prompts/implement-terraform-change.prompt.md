---
description: "Implement or fix a Terraform configuration change, validate it and review its plan"
agent: terraform-expert-engineer
---

# Implement or fix a Terraform change

## Inputs

- The requested change, or the failing command and its error output.
- The root or child module it affects. Discover from the repository before asking: `required_version`, `required_providers`, `.terraform.lock.hcl`, the backend block, per-environment variable files, and the CI definition that runs Terraform.
- The environment, cloud account or subscription, execution mode (local CLI, CI, or HCP Terraform remote run) and state owner.
- The authorization given: edit only, local validation, a plan against a named backend, or more. Do not invent credentials, backends or variable values.

## Workflow

1. Apply terraform-core-and-style to establish the contract: installed and required Terraform version, provider sources and constraints, root versus child module, and the repository's own style, security, policy and CI rules.
2. For a failure, classify it first (syntax, initialization or provider installation, configuration type, dependency graph, backend or state, provider API, policy), confirm the exact installed Terraform and provider versions, and reduce it to a minimal reproducer. If the user asked only for a diagnosis, stop at the cause and the proposed fix.
3. Make the smallest reviewable change. Keep credentials out of HCL, variable files and outputs; mark sensitive variables and outputs accurately; prefer `for_each` with stable keys; keep provider configuration in the root module; preserve the dependency lock file.
4. Route by what the change touches: module interfaces or resource addresses to terraform-modules-and-refactoring; backends, state or imports to terraform-state-backends-and-imports; tests to terraform-testing-and-validation; HCP Terraform workspaces or Stacks to terraform-cloud-and-stacks; pipelines to terraform-ci-cd-and-quality; policy to terraform-policy-and-governance; an AVM module to azure-verified-modules.
5. Validate in order: `terraform fmt -check`, `terraform init -backend=false` and `terraform validate` where backend access is not needed, the repository's configured lint and tests, then `terraform plan` only against an authorized backend with real variables.
6. Review the plan for create, update, replace and destroy actions, provider changes, address changes, sensitive values and policy results. An unexpected replace or destroy stops the work until it is explained or removed.

Never solve a state or provider error by broadening permissions, disabling locking or deleting state.

## Expected output

The diff; each command with its directory, exit code and result; the plan summary with every replace or destroy named by address; what each check does not prove; and a completion report. Apply, destroy, import, state commands, force-unlock and production work need explicit authorization first. Follow the `terraform-expert-engineer-contract` instruction; authorization already given holds only within its stated scope.
