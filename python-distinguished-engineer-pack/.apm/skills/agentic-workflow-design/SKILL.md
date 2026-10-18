---
name: agentic-workflow-design
description: Design Python tool-using workflows, state, memory, budgets and optional specialist handoffs. Use when a Python agent application or multi-step tool workflow needs design or change.
---

# Agentic Workflow Design

## Activation and scope

A Python agent application or multi-step tool workflow needs design or change. Do not add multi-agent orchestration merely to reproduce an organization chart.

## Inputs and dependencies

- Inputs: User outcome, stable/uncertain decisions, tool contracts, identities, state/memory, latency/cost constraints.
- Dependencies: Repository orchestration stack and policy enforcement boundary.
- Owner: the primary Python Distinguished Engineer; use a specialist only when its isolated evidence helps the task.

## Workflow

1. Prefer deterministic workflow steps where requirements are stable. Begin with one capable agent; add specialists only for bounded expertise, independent evidence or useful concurrency.
2. Model states, transitions, completion, retry/recovery and termination. Bound elapsed time, model/tool/browser calls, parallelism, tokens, context and estimated spend.
3. Define tools with typed arguments and validated outputs; enforce identities, authorization and approvals outside the model. Keep untrusted content distinct from instructions.
4. Separate run state, preferences, repository facts, retrieval, durable memory and audit. Attach provenance/time, tenant scope, purpose, expiry and deletion; never promote speculation or poisoned retrieval into authoritative memory.

## Output and validation

Workflow/state design, tool and handoff contracts, budgets, failure/escalation path and evaluation cases. Record exact checks run, observed failures and unavailable evidence. A draft, static check or local mock does not establish live behavior.

## Failure and guardrails

Nonterminating loop, cross-user context, self-approval, ungrounded memory or unnecessary agent hierarchy. Preserve existing user work; stop only the dependent operation when a material input or required approval is missing, and continue useful authorized work. A specialist cannot self-approve or expand the assignment.

## Workflow connection

Within the complete pack, the optional `evaluate-agent.prompt.md` recipe connects this Skill to the primary workflow. This Skill is self-contained when installed individually; no external prompt or specialist is required. With the full pack installed, the `python-engineering-contract` instruction supplies the approval, handoff and completion rules.
