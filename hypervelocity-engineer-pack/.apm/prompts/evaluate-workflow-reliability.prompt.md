---
description: "Evaluate whether an agentic workflow, or a change to it, is correct, safe, reliable and affordable enough to operate"
agent: hypervelocity-engineer
---

# Evaluate an agentic workflow

## Inputs

- The workflow and the change or operating decision being evaluated.
- Representative inputs or past runs, acceptance criteria, and the owner who decides.
- Authorization and budget for evaluation runs.

## Workflow

1. Apply `workflow-observability-and-evaluation`: fix the task set and acceptance criteria before any change. Include negative, ambiguous, oversized, malicious, permission-denied, timeout and duplicate-event cases.
2. Collect evidence with `gh aw logs` and `gh aw audit` where authorized, and keep step summaries and artifacts.
3. Measure correctness and completion; safety violations and unauthorized mutations; latency, retries and human-review burden; cost only where the platform exposes it; and reproducibility across comparable runs.
4. Apply `agent-governance-and-guardrails` to any safety violation or policy escape found.
5. Compare before and after on equivalent inputs, one major variable at a time, with a rollback ready.

## Expected output

The case table with results, metrics labeled observed, inferred or unavailable, uncertainty and sample size, a recommendation (operate, fix, or revert) for the human owner, and the completion report required by the `hypervelocity-engineer-contract` instruction. A model score or a clean exit never replaces the owner's decision.
