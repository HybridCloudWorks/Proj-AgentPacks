---
name: azure-verified-modules
description: Develop or review Azure Terraform modules against current Azure Verified Modules requirements, with focused checks for registry references, providers, interfaces, tests, documentation, and upgrade safety.
---

# Azure Verified Modules

Use this Skill when an Azure Terraform module is intended to consume or meet Azure Verified Modules (AVM) requirements. This is a focused specialization, not a replacement for the core Terraform and state Skills.

## Verify current requirements

Read the current AVM Terraform specification and the specific module's repository instructions before asserting compliance. The supplied AVM references are consolidated guidance; exact provider version ranges, test tooling, naming, and certification checks are drift-prone.

## High-value checks

- Reference AVM modules from the Terraform Registry with pinned versions and do not silently substitute arbitrary Git modules or non-AVM modules when certification is the goal.
- Declare required_version and required_providers with source and compatible constraints. Use only providers permitted by the current AVM requirement for the module.
- Keep child modules free of provider configuration except supported aliases and pass provider configurations from the caller.
- Use lower snake_case, stable for_each keys, precise variable types and descriptions, non-sensitive defaults only, and accurate sensitive outputs.
- Avoid whole-resource outputs, blanket enabled switches, module_depends_on controls, unnecessary nullable values, and unreviewed ignore_changes.
- Keep terraform.tf, variables, locals, outputs, and resource ordering consistent with the current AVM style requirements; run terraform fmt.
- Include module documentation, examples, changelog, tests, and upgrade notes appropriate to the module's release process.
- Use feature toggles for newly introduced optional resources when the current AVM spec requires them to avoid surprise creation.

## Review result

Report each requirement as pass, fail, not applicable, or unable to verify. Distinguish AVM style compliance from Terraform correctness, provider API behavior, security posture, and official certification. Never claim certification from a local static review alone.
