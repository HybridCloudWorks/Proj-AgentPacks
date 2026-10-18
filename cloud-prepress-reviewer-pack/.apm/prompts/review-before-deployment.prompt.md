---
description: "Pre-deployment review of a Terraform, Bicep, ARM, Azure Developer CLI, Azure Policy or RBAC change"
agent: cloud-prepress-reviewer
---

# Review an infrastructure change before deployment review

## Inputs

- The exact change: base and head refs or a supplied file list, including modules, parameter or variable files, lock files and pipeline definitions.
- The intended target: environment, tenant, subscription, region, resource group or management group scope, state backend, and deployment identity.
- Preview evidence already captured (Terraform plan, Bicep what-if, `azd provision --preview`), with the command, commit and scope it was captured at. If none exists, whether the operator authorizes a read-only preview at a named scope.
- The architecture brief, ADRs, constraints, cost assumptions, budget ceiling, owner and rollback plan, where they exist.

Secrets arrive as references, never as values. Ask before any live read-only Azure query unless that authorization is already explicit for the named scope.

## Workflow

1. Apply cloud-prepress-orchestration to fix the target and authorization boundary and to select the domains the change needs.
2. Apply change-scope-and-impact to classify the change and find stateful resources, renames, replacements, `moved` or import blocks, state boundaries and consumers.
3. Apply iac-policy-and-identity-review: Terraform by state, address, plan and lifecycle; Bicep and ARM by deployment scope, API version, dependencies and what-if evidence; Azure Policy by scope and effect; RBAC by principal, role, scope and operation.
4. Apply deployment-preview-and-environment-review to confirm that the preview targets the intended scope at the reviewed commit, and to review create, modify, delete and replace counts, unexplained drift, state lock risk, policy denials and missing permissions.
5. Apply azure-evidence-and-mcp-review to ground drift-prone claims in current official sources and to label every item of evidence.
6. Apply architecture-and-adr-consistency when topology, boundaries, data flows or environment placement change.
7. Apply operability-resilience-and-rollback-review and cost-allocation-and-governance-review for rollout, rollback boundary, recovery, tags, budgets, quotas and policy exceptions.
8. Apply tests-build-and-dependency-review for formatting, validation, compilation, provider and module locks, and unresolved template variables.
9. Apply review-report-and-pr-gate to write the report, with review-hooks-and-automation around it when the pack's helpers are available.

Hard stop: never run `terraform apply`, `azd up`, `azd deploy`, `azd down`, ARM create, update or delete, force-unlock, import, or any RBAC, policy or secret change, even when asked. Report that review evidence is not deployment authorization.

## Expected output

A pre-press report with every contract section, including preview change counts and the commit and scope they were captured at, policy and RBAC status, rollback boundary, and cost against any documented ceiling. Recommend `READY_FOR_DEPLOYMENT_REVIEW` only when the preview matches the reviewed commit and intended scope and no blocking finding remains; without preview evidence the deployment gate is `NOT_VERIFIED`.

Follow the `cloud-prepress-reviewer-contract` instruction. Never describe an unexecuted check as passed.
