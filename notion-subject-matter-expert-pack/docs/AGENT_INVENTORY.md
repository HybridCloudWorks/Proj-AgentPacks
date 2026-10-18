# Agent inventory

| Profile | Responsibility | Invocation | Declared intent (see TOOL_PERMISSION_MATRIX.md) |
|---|---|---|---|
| notion-subject-matter-expert | Notion subject matter expert that designs workspaces and databases, captures knowledge, prepares meeting materials, synthesizes research, turns specs into tracked tasks and builds Notion integrations, with approval-gated writes. | User-facing primary | read, edit, shell, web, delegate; Notion read and write |
| notion-governance-reviewer | Read-only independent reviewer of Notion sharing exposure, internal and external content separation, and the safety of schema, move and bulk changes. | Optional specialist; hidden from the Copilot picker; sets `include-custom-instructions: true` so Copilot gives it the contract | read; Notion read only |

## Why one specialist

The prompt's section 3 allows a specialist only where separate expertise, context, permissions or independent review add concrete value. The governance reviewer meets two of those tests: it needs fewer permissions than the primary (no Notion writes, no shell), and it provides an independent look at exactly the actions that are hardest to undo in Notion, which are sharing, moves, schema changes and external publication. Splitting the content workflows (meetings, research, specs) into specialists would only reproduce an organization chart; they share the same tools, context and approval rules, so they stay as skills used by the primary.

## Activation and boundaries

- The primary delegates before a Level 2 action, before external or wider publication, and for audits, when delegation is available.
- The handoff carries the fields in HANDOFF_CONTRACT.md; the reviewer returns located findings and a proceed, proceed-with-changes or stop recommendation.
- The primary integrates findings, decides with the user and owns completion. Without delegation (Gemini CLI, or a host that cannot launch subagents) the primary performs the review itself and reports that it was not independent.

Both profiles live in the host's agent directory; there is no separate subagents folder. Canonical agents declare no `tools` field. APM-generated agents inherit the host's tools, so the reviewer's read-only boundary is enforced only when an installer applies `compatibility/tool-permissions.yml` or the user restricts its tools in the host.
