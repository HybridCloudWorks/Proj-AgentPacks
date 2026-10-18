---
name: iac-policy-and-identity-review
description: Reviews Terraform, Bicep, ARM, Azure Policy, RBAC, managed identity, tags, naming, and infrastructure governance changes for correctness and least privilege.
---

# IaC, Policy, and Identity Review

For Terraform inspect provider/module constraints, lock files, state backend, resource addresses, lifecycle, replacements, imports/moved blocks, variables, outputs, sensitive values, and plan assumptions. For Bicep/ARM inspect scope, API versions, modules, parameters, dependencies, conditions, deployment mode, and what-if interpretation.

For Azure Policy inspect definition/initiative, assignment scope, parameters, effect, exclusions/exemptions, managed identity, remediation, and whether the policy is `audit`, `modify`, `deployIfNotExists`, `deny`, or `denyAction`. For RBAC inspect principal, role, scope, data-plane need, PIM/OIDC, and bootstrap ownership.

Require mandatory tags, allowed regions/SKUs, secure defaults, private access where required, deletion protection, diagnostic settings, and documented exceptions. Never infer live compliance from static IaC.
