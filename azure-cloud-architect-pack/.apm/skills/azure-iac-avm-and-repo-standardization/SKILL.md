---
name: azure-iac-avm-and-repo-standardization
description: Designs and reviews Azure IaC with Bicep, ARM, Terraform, AzAPI, AzureRM, AVM, module interfaces, repository standards, policy gates, and safe remote state.
---

# Azure IaC, AVM, and Repository Standardization

Choose Bicep/ARM, Terraform, AVM, or composition from ownership, ecosystem, lifecycle, state, testing, and platform scope. Keep provider/module versions pinned, state remote and locked, secrets out of repositories and state where possible, and deployment identity federated with least privilege.

For current Terraform AVM work, start with the official AVM specification: new modules are AzAPI-first; AzureRM is a narrow documented exception for unsupported operations; module interfaces, parent scope, submodules, tests, docs, examples, and provider requirements must follow the current spec. Do not assume older attached provider guidance is current.

Standardize additively: README, ownership, security, CI validation, formatting, linting, policy scans, lock files, examples, changelog, ADRs, runbooks, bootstrap preflight, and ALZ absorption notes. Never rename live addresses/resources without a migration plan, moved/import strategy, and plan evidence.
