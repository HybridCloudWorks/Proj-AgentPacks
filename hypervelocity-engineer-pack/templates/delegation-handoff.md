# Delegation handoff

Produced by `agent-delegation-and-composition` whenever work is split across agents, subagents, scripts, MCP tools, ordinary CI or people. Fill one delegate block per executor. The parent keeps ownership of integration and completion.

## Executor choice

| Step | Executor (script or CI / MCP tool / agent / subagent / human) | Reason | Alternatives rejected, and why |
|---|---|---|---|
| | | | |

Subagent justification, if any: <parallelism, isolation or a distinct expertise boundary that improves the result>

## Delegate: <name>

| Field | Value |
|---|---|
| Objective | |
| Owner | |
| Input paths | |
| Excluded data | |
| Tools | |
| Permissions | <never more than the parent holds> |
| Expected output schema | |
| Evidence requirement | |
| Timeout | |
| Retry rule | <non-idempotent mutations are not retried without checking the prior result> |
| Budget | <tokens, runtime, fan-out, recursion depth> |
| Correlation ID | <where the platform supports one> |
| Shared state source of truth | |

## Return format

The delegate returns a structured summary:

- Facts, each with its source
- Decisions made
- Changed files
- Tests or checks run, with results
- Risks
- Unresolved questions

## Reconciliation

| Item | Value |
|---|---|
| Conflicting findings | <both preserved, routed to: owner> |
| Results reconciled before | <the mutation or release decision they feed> |
| Unsafe write behavior | fail closed |
| Missing evidence behavior | fail visibly |
