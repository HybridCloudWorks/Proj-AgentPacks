---
description: "Refactor or restructure a Terraform module without recreating resources or breaking consumers"
agent: terraform-expert-engineer
---

# Refactor a Terraform module safely

## Inputs

- The module and the intended change: rename, split, extract into a child module, `count` to `for_each`, or an interface change.
- Its consumers: root configurations in this repository, and registry or Git consumers if the module is published.
- Current state addresses for every affected environment, from `terraform state list` or a plan, when the user authorizes reading state.
- Each environment's variable files, because `moved` blocks are static and must map the same way in every environment.

## Workflow

1. Apply terraform-modules-and-refactoring. Before editing, map every current address to its new address, with dependencies, consumers and the plan impact you expect.
2. Keep the interface small and documented; let the root module configure providers; do not add an `enabled` or `module_depends_on` switch for a whole module.
3. Record each address change as a `moved` block. Chain historical moves rather than rewriting them, and keep existing `moved` blocks: removing one breaks users who have not yet crossed that transition.
4. Validate with terraform-core-and-style and terraform-testing-and-validation, then run `terraform plan` for each authorized environment. Every affected object must show as moved, not destroyed and created. Fix the configuration and plan again until it does.
5. State-only moves (`terraform state mv`, `terraform state replace-provider`) are exceptional. Use terraform-state-backends-and-imports, and only with a backup, an exact address map, the state lock, a recovery path and explicit authorization. Never use `state rm`, `state push` or forced replacement to get past an unclear refactor.
6. For a published module, run the release gate: interface compatibility, Terraform and provider constraints, changelog, migration notes, examples, tests and downstream plans. Label the release patch, minor or breaking from consumer and state behaviour, not from diff size.

## Expected output

The diff with its `moved` blocks; the address map; per-environment plan summaries showing zero unintended replace or destroy; the release label and its reason; consumer migration notes; and a completion report. Applying the moves changes state and needs authorization. Follow the `terraform-expert-engineer-contract` instruction.
