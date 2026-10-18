---
description: "Bring existing cloud resources under Terraform with reviewed import blocks and a clean plan"
agent: terraform-expert-engineer
---

# Import existing resources into Terraform

## Inputs

- The remote objects to adopt: resource type, identifier, account or subscription, and region.
- The root module and target addresses, the Terraform and provider versions, and the backend that will hold the imported state.
- Whether Terraform Search is available for these resources in the installed Terraform version and provider.

## Workflow

1. Apply terraform-state-backends-and-imports. Confirm the provider supports import for each type, and the exact import ID format for the locked provider version.
2. Prefer declarative `import` blocks so the import is reviewed and repeatable. CLI `terraform import` only binds an object to an address, writes state immediately and authors no configuration; it needs authorization like any state change.
3. Map each remote object to exactly one address. Use Terraform Search only when the installed version and the provider's list resources support it, and treat what it generates as a draft; otherwise take the narrow manual path.
4. Draft configuration with `terraform plan -generate-config-out=generated.tf` where useful, then clean it with terraform-core-and-style and terraform-modules-and-refactoring into a maintainable interface: drop defaults and computed attributes, replace literals with typed variables where they vary, keep secrets out.
5. Plan until the import is pure: every object shows as imported, with no unintended update, replace or destroy. Reconcile drift by matching the real configuration first, and propose hardening as a separate reviewed change.
6. Imported objects can bring sensitive attributes, such as access keys, into state; confirm the backend's access controls fit them.

## Expected output

The `import` blocks and cleaned configuration; the object-to-address map; the plan summary with import, change and destroy counts; the drift found and how it was reconciled; and a completion report. Applying the import writes state and needs authorization. Follow the `terraform-expert-engineer-contract` instruction.
