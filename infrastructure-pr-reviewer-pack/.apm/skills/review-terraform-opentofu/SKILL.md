---
name: review-terraform-opentofu
description: Review Terraform and OpenTofu pull request changes for state identity, provider and module contracts, lifecycle transitions, expressions, sensitive data, and plan/apply integrity. Use when a diff contains .tf, .tfvars, .tftest.hcl, .terraform.lock.hcl, OpenTofu equivalents, state migration declarations, or pipelines that run Terraform or OpenTofu. Do not use for Bicep, ARM, or unrelated application code.
---

# Objective

Determine whether Terraform or OpenTofu changes preserve the intended remote-object identity and produce a safe, reproducible transition against representative existing state.

## Inputs

- Root and child modules, callers, providers, aliases, backend, workspace, state key, variables, outputs, and dependency lock.
- The complete diff plus a plan tied to the reviewed commit, target, identity, variables, state, and provider set when risk requires it.
- CI plan/apply workflow, approvals, concurrency, and saved-plan provenance.

## Workflow

1. Identify root modules, execution context, CLI constraints, provider sources and aliases, backend, state selection, variable precedence, and plan/apply entry points.
2. Compare old and new resource and module addresses. Inspect renames, count/for_each transitions, key changes, imports, moves, removals, backend changes, workspace changes, and tool-to-tool ownership transfer.
3. Review every planned create, update, replacement, delete, import, move, and no-op that conflicts with intent. Require representative existing-state evidence for replacement-sensitive or data-bearing changes.
4. Trace expressions through null, unknown, empty, duplicate, reordered, conditional, and collection-conversion cases. Check key stability and values used for identity, count, provider settings, and scope.
5. Review module input, output, sensitivity, provider alias, source, and version contracts across all callers and consumers.
6. Review lifecycle controls, direct state operations, targeting, replacement flags, locking, drift suppression, sensitive state or plan data, and least-privilege CI identity.
7. Verify that validation, approval, and apply use the same revision, lock file, variables, state, workspace, target identity, and approved artifact.
8. Return confirmed findings and evidence gaps to `review-infrastructure-pr`; do not duplicate universal gates or final reporting.

## Decision Rules

- A clean plan against empty state does not prove upgrade safety.
- Address or key changes without an explicit migration path are blocking when they can recreate, orphan, duplicate, or destroy an existing object.
- Sensitivity markings do not remove secrets from state or plan artifacts.
- Do not recommend `-target`, `-replace`, disabled locking, or direct state manipulation as routine workflow.

## Output Contract

Return technology-specific findings and evidence gaps to `review-infrastructure-pr` with an anchor, trigger, affected target, impact, remediation, and verification evidence. Do not repeat universal gates or create another final report.

## Validation and Stop Conditions

Use `references/review-checklist.md`; verify uncertain semantics through `references/official-sources.md`. Stop when decisive target state, identity, versions, generated output, or safe access is unavailable. Never mutate targets or expose sensitive values.

## Resources

- Read `references/review-checklist.md` for the complete technology adapter.
- Read `references/official-sources.md` when behavior is version-specific, uncertain, or current verification is required.
