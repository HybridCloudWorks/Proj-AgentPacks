---
description: "Choose the right mechanism for an automation request and design a bounded agentic workflow before any code is written"
agent: hypervelocity-engineer
---

# Design an agent-assisted mechanism

## Inputs

- The outcome wanted, who consumes it, and how often.
- Trigger or cadence, repository, and data sources.
- Risk boundary: what may be read, what may be changed, and who approves changes.
- Existing automation in the repository: CI workflows, scripts, GitHub Agentic Workflows, MCP servers.

Discover local facts before asking. Ask only for decisions that change the design, such as who owns an approval.

## Workflow

1. Apply `agent-delegation-and-composition`: split the request into steps and pick one executor per step (deterministic script or ordinary CI, MCP tool, agent, subagent, or human). Record why each rejected executor was rejected.
2. When a GitHub Agentic Workflow is the chosen executor, apply `agentic-workflows` on its design route. Design only; do not write workflow source in this task.
3. Apply `agent-governance-and-guardrails`: for each capability record actor, data, tool, permission, destination, mutation, approval point, failure behavior and rollback, and mark each control as enforced by the platform, enforced by repository policy, advisory, or missing.
4. For each delegate define objective, input paths, excluded data, tools, permissions, output schema, evidence requirement, timeout, retry rule and owner. Bound fan-out, budget and retries.
5. Name the acceptance criteria an evaluation would use, following `workflow-observability-and-evaluation`, without running one.

## Expected output

A mechanism table (step, executor, reason, rejected alternatives), delegate contracts, the guardrail decision record, approval gates with owners, evaluation criteria, and the next safe action. No files are written and no workflow is run unless the user asks. Follow the `hypervelocity-engineer-contract` instruction for the completion report; existing authorization persists only within its scope.
