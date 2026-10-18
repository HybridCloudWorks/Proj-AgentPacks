---
description: "Develop or review an Azure Terraform module against current Azure Verified Modules requirements"
agent: terraform-expert-engineer
---

# Review an Azure Terraform module against AVM requirements

## Inputs

- The module path or repository, and the commit or version under review.
- The goal: consuming AVM modules correctly, or building a module that meets AVM requirements.
- The current AVM Terraform specification and the module repository's own instructions. Retrieve the specification when web access is available; otherwise record that it was not retrieved.
- Whether the user wants findings only (the default) or authorized fixes.

## Workflow

1. Apply azure-verified-modules. Read the current specification and the repository's instructions before asserting compliance; exact provider ranges, test tooling, naming and certification checks drift.
2. Check the high-value requirements:
   - Terraform Registry sources with pinned versions.
   - `required_version` and `required_providers` with sources and compatible constraints, using only permitted providers.
   - No provider configuration in child modules beyond supported aliases.
   - Lower snake_case, stable `for_each` keys, precise variable types and descriptions, non-sensitive defaults, and accurate sensitive outputs.
   - No whole-resource outputs, blanket enabled switches, `module_depends_on`, unnecessary nullable values or unreviewed `ignore_changes`.
   - File layout and ordering.
   - Documentation, examples, changelog, tests and upgrade notes.
   - Feature toggles for new optional resources where the specification requires them.
3. Use terraform-core-and-style for Terraform correctness, terraform-modules-and-refactoring for interface and upgrade safety, and terraform-testing-and-validation for tests.
4. Run local checks only: `terraform fmt -check`, `terraform init -backend=false` and `terraform validate`.
5. When fixes are authorized, change one requirement at a time and keep consumers compatible.

## Expected output

A requirement table marking each item pass, fail, not applicable or unable to verify, with evidence and remediation; findings with file and line; a separate statement of what lies outside AVM style (Terraform correctness, provider API behaviour, security posture and official certification); and a completion report. Never claim certification from a local review. Follow the `terraform-expert-engineer-contract` instruction.
