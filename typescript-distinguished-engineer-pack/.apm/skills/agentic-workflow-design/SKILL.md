---
name: agentic-workflow-design
description: Design bounded, auditable agentic workflows and tool-calling loops that use autonomy only where it adds value.
---

# Agentic Workflow Design

Start with a deterministic workflow when the process is known. Introduce an agent only where adaptation, retrieval, or tool selection provides measurable value. Prefer one capable agent with clear tools before multi-agent orchestration.

Define goal, state, context sources, tools, handoffs, policies, approvals, termination conditions, step/time/token/cost budgets, retries, cancellation, failure recovery, and observable success criteria. Use structured outputs and version prompts, tools, models, and Skills. Keep human approval at consequential boundaries.

Test happy paths, ambiguity, tool errors, malformed outputs, prompt injection, unauthorized requests, cancellation, budget exhaustion, partial completion, recovery, and rollback. Never accept a generated narrative as evidence of success.
