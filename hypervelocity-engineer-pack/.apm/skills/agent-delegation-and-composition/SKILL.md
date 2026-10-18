---
name: agent-delegation-and-composition
description: Select and compose agents, subagents, deterministic scripts, MCP tools, and human review so each task has a bounded owner and reliable handoff.
---

# Agent Delegation and Composition

Use this skill when work could be split across agents, subagents, scripts, MCP tools, ordinary CI, or human decisions.

## Select the right executor

- Use a deterministic script or ordinary CI for stable transforms, schema checks, formatting, and repeatable tests.
- Use an MCP tool when the authoritative system of record is external and the tool has a clear read or write contract.
- Use an agent for ambiguous synthesis, planning, review, or bounded reasoning over repository context.
- Use a subagent only when parallelism, isolation, or a genuinely distinct expertise boundary improves the result.
- Keep approvals, policy exceptions, irreversible actions, and ambiguous ownership with a human.

## Compose safely

For each delegate define: objective, input paths, excluded data, tools, permissions, expected output schema, evidence requirement, timeout, retry rule, and owner. Pass the minimum context needed. Do not duplicate repository-wide discovery in multiple delegates or allow a delegate to expand the parent permissions.

Use a stable source of truth for shared state. Return structured summaries with facts, decisions, changed files, tests, risks, and unresolved questions. Make handoffs idempotent and include correlation identifiers where the platform supports them.

## Failure containment

- Bound recursion, fan-out, token budget, runtime, and retry count.
- Fail closed for unsafe writes and fail visibly for missing evidence.
- Do not retry non-idempotent mutations without checking the prior result.
- If a delegate disagrees with another, preserve both findings and route the conflict to the owner rather than averaging away the risk.
- Reconcile parallel results before a final mutation or release decision.
