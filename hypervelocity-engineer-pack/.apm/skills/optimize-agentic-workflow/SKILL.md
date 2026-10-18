---
name: optimize-agentic-workflow
description: Measure and reduce token use, AI credits, tool denials, timeouts, context waste, and run frequency in GitHub Agentic Workflows while preserving safe-output behavior and equivalent result quality.
---

# Optimize Agentic Workflow

Measure before editing. Ask for a run URL or ID, workflow name, guardrail exceeded, baseline output, and quality criteria. Do not claim savings from prompt shortening alone.

## Analysis sequence

1. Collect `gh aw audit <run-id> --json` or equivalent evidence.
2. Inspect input, output, cached, and agent-usage token fields plus tool-call and failure data.
3. Classify cost across context assembly, prompt generation, tool interaction, orchestration, memory, and output handling.
4. Identify the three largest drivers and distinguish one-time setup from recurring cost.
5. Apply the smallest safe change: narrow context, DataOps pre-step, proxy/query, early exit, batching, caching, cheaper model for triage, or bounded delegation.
6. Re-run a comparable evaluation and compare safety, correctness, latency, and cost.

## Guardrail-specific diagnosis

- AI-credit limit -> trim context, remove repeated extraction, cache stable inputs, and split work.
- Daily budget -> reduce cadence, add event filters, batch inputs, and add no-op exits.
- Tool denials -> inspect the denied tool and policy; avoid repeated forbidden calls rather than broadening permissions automatically.
- Timeout or max turns -> decompose, precompute deterministic data, reduce loops, and bound delegation before raising limits.

Prompt caching requires stable instructions before dynamic content. Subagents are justified only for independent, repetitive, or context-heavy work with a defined return contract. Preserve task features, configuration deltas, outcomes, cost, and diagnosis only when cross-run reuse is valuable and approved.

Present an optimization plan before editing. Validate equivalent safe-output quality, not just fewer tokens. Do not silently alter model, permissions, cadence, or output behavior.
