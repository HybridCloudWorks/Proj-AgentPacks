---
name: review-bicep-arm
description: Review Bicep, Bicep parameter, ARM JSON, deployment-stack, template-spec, and related pipeline changes for deployment scope, resource identity, deletion behavior, API versions, module contracts, secrets, and what-if integrity. Use when a PR changes .bicep, .bicepparam, ARM templates, deployment stacks, template specs, or commands that build, preview, or deploy them. Do not apply Terraform state rules to these templates.
---

# Objective

Prove that the exact Bicep or ARM deployment command selects the intended scope and identity, preserves resource ownership, and produces the reviewed lifecycle effects.

## Inputs

- Entry Bicep or ARM files, module graph, parameter sources, targetScope, deployment command, name, mode, scope, identity, and target.
- Compiled ARM JSON and target-scoped what-if output for the reviewed revision and parameters when risk requires them.
- Downstream consumers of outputs and any ownership transition to or from another tool.

## Workflow

1. Identify entry points, targetScope, actual CLI or pipeline scope, tenant/subscription/resource group/location, deployment name, parameter sources, and identity.
2. Trace resource identity through type, name, scope, parent, loop keys, deterministic IDs, `existing` declarations, symbolic references, and API-version changes.
3. Determine create, update, replacement-like, delete, detach, purge, complete-mode, or deployment-stack behavior from the exact command and API rather than source text alone.
4. Review module registry references, aliases, restore behavior, input/output contracts, secure values, conditions, loops, runtime values, and downstream consumers.
5. Inspect lint output and compiled ARM JSON. Require target-specific what-if evidence for high-risk changes and review every delete or unexplained no-change result.
6. Review networking, identity, role assignment, policy, locks, public exposure, cross-scope assumptions, and deterministic role-assignment identity.
7. Verify that approval and deployment consume the same reviewed source or immutable compiled artifact with identical parameters and identity.
8. Return confirmed findings and evidence gaps to `review-infrastructure-pr`.

## Decision Rules

- A symbolic-name rename alone does not necessarily change deployed identity; type, name, parent, scope, or deterministic-ID changes can.
- Compilation proves translation, not target correctness.
- What-if is evidence, not absolute proof; label provider/runtime uncertainty explicitly.
- Do not infer deletion behavior without the exact deployment mechanism, mode, and target scope.

## Output Contract

Return technology-specific findings and evidence gaps to `review-infrastructure-pr` with an anchor, trigger, affected target, impact, remediation, and verification evidence. Do not repeat universal gates or create another final report.

## Validation and Stop Conditions

Use `references/review-checklist.md`; verify uncertain semantics through `references/official-sources.md`. Stop when decisive target state, identity, versions, generated output, or safe access is unavailable. Never mutate targets or expose sensitive values.

## Resources

- Read `references/review-checklist.md` for the complete technology adapter.
- Read `references/official-sources.md` when behavior is version-specific, uncertain, or current verification is required.
