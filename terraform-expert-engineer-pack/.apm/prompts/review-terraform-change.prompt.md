---
description: "Review a Terraform change and its plan without modifying code, state or remote systems"
agent: terraform-expert-engineer
---

# Review a Terraform change

## Inputs

- The exact base and head, a branch, or the supplied diff. Resolve it before reviewing; do not review a guessed range.
- Plan output if supplied (`terraform show` text or JSON), with the commit, root module, backend or workspace, and variables it was produced from.
- The repository's style, CI and policy rules, and any acceptance criteria the user states.

## Workflow

1. Apply terraform-core-and-style to every changed `.tf`, `.tfvars` and `.terraform.lock.hcl` file: version constraints, provider sources, naming, variable types and validation, sensitive marking, `for_each` keys, lifecycle rules, dynamic blocks and data sources.
2. Add the Skills the diff calls for: terraform-modules-and-refactoring for module interfaces, `moved` blocks and address changes; terraform-state-backends-and-imports for backend, `import` or `removed` blocks; terraform-testing-and-validation for test files; terraform-ci-cd-and-quality for pipeline files; terraform-policy-and-governance for policy code or results; terraform-cloud-and-stacks for HCP Terraform or Stack files; azure-verified-modules when an AVM module is consumed or compliance is claimed.
3. Review the plan for create, update, replace and destroy actions, provider and lock-file changes, state address changes, sensitive values and policy results. Check that the plan was produced from the reviewed commit; a plan from other inputs is not evidence for this diff.
4. Run only local, read-only checks such as `terraform fmt -check`, `terraform init -backend=false` and `terraform validate`. Do not run a plan against shared state unless the user authorizes it.

Keep the review read-only: no edits, no state commands, no comments posted, no approval or merge. Summarize a supplied plan by address and action; never paste values from it.

## Expected output

Findings ordered by severity, each with file and line, evidence, impact, remediation and whether it blocks; a plan impact summary; the checks actually run; what was not reviewed; and a completion report. Follow the `terraform-expert-engineer-contract` instruction.
