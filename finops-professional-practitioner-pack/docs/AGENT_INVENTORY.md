# Agent inventory

| Agent | Responsibility | Invocation | Declared intent | Why it exists |
|---|---|---|---|---|
| finops-professional-practitioner | Runs every FinOps workflow end to end, integrates specialist results and owns completion | User-facing primary (`user-invocable: true`) | read, edit, shell, web, delegate | The role's single accountable agent |
| finops-data-analyst | Scoped read-only queries, data-health and reconciliation checks over assigned billing data; returns aggregates with queries and row counts | Optional specialist (`user-invocable: false`) | read, shell | Keeps large exploratory query work out of the primary's context, with narrower permissions |
| finops-evidence-reviewer | Independent review of figures, savings claims, forecasts, allocations and commitment recommendations; returns located findings | Optional specialist (`user-invocable: false`) | read | Independence: the author of a number should not be its only auditor |

All three profiles live in the host's agent folder; "specialist" describes how an agent is invoked, not where it is stored. Specialists set `include-custom-instructions: true` (so Copilot subagents receive the contract instruction) and preload `focus-billing-data-analysis` through the Claude Code `skills` field.

## Activation

- Data analyst: many exploratory queries over large exports, a reconciliation pass, a conformance check, or segment queries for an anomaly.
- Evidence reviewer: before figures, savings claims, forecasts or commitment recommendations reach Finance, leadership or a purchase decision, and whenever the primary produced the numbers itself.

## Boundaries

- The data analyst does not edit files, change cloud state, add data sources or run unbounded scans. Its shell could do some of these, so the limit is behavioural; run it with read-only credentials and the host sandbox.
- The evidence reviewer does not edit, run commands or queries, or bring in data it was not given.
- Neither approves a Level 2 action or its own scope expansion. The primary reconciles their output and owns the result.

## Host notes

Canonical agents declare no `tools`. APM-generated agents inherit the host's tools; the intents above are what an installer that writes vendor files should apply (see TOOL_PERMISSION_MATRIX.md). Gemini CLI receives no agents from APM, so on Gemini the primary's workflows run through skills and commands and the fallback applies: same skills, review not independent.
