---
description: "Assess whether an infrastructure change is safe against the existing environment: identity, ownership, replacement, deletion and rollback"
agent: infrastructure-pr-reviewer
---

# Assess existing-environment impact

Use this workflow when a pull request renames, moves, re-keys, imports, removes or transfers ownership of managed objects, or changes a deployment mode, prune setting, immutable property, backend, workspace or state key.

## Inputs

- The diff with base and head revisions, and the environment the user is worried about.
- Plans, what-if results, rendered output or check-mode results generated from the head commit against representative existing state, when the author supplied them.
- State, deployment-history, inventory or controller ownership facts that the repository or the attached evidence establishes.

## Workflow

1. Apply the `review-infrastructure-pr` Skill and build full changed-line coverage. A focused question does not narrow coverage; every changed line still receives a disposition.
2. Use the existing-environment reasoning in that Skill's `references/review-protocol.md` and the ownership, state, drift and lifecycle gates in `references/universal-gates.md`.
3. For each affected object, establish which tool owns it before and after the change, whether its identity stays stable, and whether the transition creates, updates, replaces, deletes, detaches or adopts it.
4. Activate the technology Skill for each mechanism: `review-terraform-opentofu` for addresses, keys, `moved`, `import` and `removed` blocks and backends; `review-bicep-arm` for scope, deployment mode and deployment stacks; `review-kubernetes-packaging` for selectors, release or namespace changes and prune; `review-ansible-automation` for convergence on repeated runs; `review-powershell-automation` for imperative current-state checks.
5. Apply `verify-infrastructure-evidence` to every plan, what-if or render. A clean plan against empty state, or evidence from another target, does not clear an upgrade.
6. Raise a defect when the change can recreate, orphan, duplicate or destroy an existing object without a migration path. Raise an evidence gap when it may be safe but proof against existing state is missing.

Stay read-only. Do not run plan, what-if, server-side dry-run or check mode against real environments.

## Expected output

The review report in the structure of the `review-infrastructure-pr` Skill's `assets/review-report-template.md`. In Review Scope, list the targets, state and ownership considered. In Evidence Gaps, name the exact artifact, commit, inputs, target and identity needed. In Handoff, give the migration or rollback evidence required before approval.

Follow the `infrastructure-pr-reviewer-contract` instruction. Never describe an unexecuted check as passed.
