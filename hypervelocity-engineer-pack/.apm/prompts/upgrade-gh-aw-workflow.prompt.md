---
description: "Upgrade GitHub Agentic Workflows or fix deprecations, recompile, and confirm the lock diff does not widen permissions"
agent: hypervelocity-engineer
---

# Upgrade GitHub Agentic Workflows

## Inputs

- Workflows in scope and the deprecation warnings or upgrade goal.
- Installed gh-aw extension version (`gh extension list`) and the target version, if known.
- Whether this task may apply fixes or only report them.

## Workflow

1. Apply `agentic-workflows` on its upgrade route and load only the matching upgrade or `gh aw fix` procedure.
2. Apply `workflow-lifecycle-and-release`: list available fixes before applying any, apply only what is authorized, recompile every affected workflow, run `gh aw validate`, and review each lock diff.
3. Apply `agent-governance-and-guardrails` to every lock diff: permissions, tools, MCP servers, network, safe outputs, secrets and runner labels must not change silently. Flag any change for the owner.
4. Check the release gate in `workflow-lifecycle-and-release` before calling the upgraded workflows ready.

## Expected output

A per-workflow table of fixes proposed and applied, extension versions before and after, a permission and capability delta (expected to be empty, otherwise justified), validation results, rollback (revert each source and lock pair together), live behavior marked unverified unless an authorized run was observed, and the completion report required by the `hypervelocity-engineer-contract` instruction.
