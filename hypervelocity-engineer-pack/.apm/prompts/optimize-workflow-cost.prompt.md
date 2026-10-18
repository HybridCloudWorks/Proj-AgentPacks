---
description: "Measure and reduce token use, AI credits, tool denials or timeouts in a GitHub Agentic Workflow while keeping output quality equivalent"
agent: hypervelocity-engineer
---

# Optimize an agentic workflow's cost

## Inputs

- Run URL or ID, workflow name, and the guardrail exceeded: AI credits, daily budget, tool denials, timeout or max turns.
- A baseline output and the quality criteria it must keep meeting.
- Whether edits and comparable re-runs are authorized, and any run budget.

Ask for the run ID if it is missing; do not optimize from the prompt text alone.

## Workflow

1. Apply `optimize-agentic-workflow`: collect `gh aw audit <run-id> --json`, inspect token, tool-call and failure fields, classify cost, name the three largest drivers, and separate one-time from recurring cost.
2. Apply `prompt-token-efficiency` to the workflow body and any agent instructions it carries. Keep stable instructions before dynamic content.
3. Present the optimization plan and wait for approval before editing. Never change model, permissions, cadence or safe outputs silently.
4. Apply `workflow-observability-and-evaluation`: fix the task set and acceptance criteria first, change one major variable at a time, and compare correctness, safety, latency and cost on equivalent inputs. Revert when quality or safety regresses.
5. Apply `workflow-lifecycle-and-release` to recompile and validate after edits.

## Expected output

Baseline evidence, a cost-driver table, the approved plan, the changes, a before and after comparison that labels each figure observed or projected, quality-equivalence evidence, rollback, and the completion report required by the `hypervelocity-engineer-contract` instruction. Savings without a comparable re-run are projected, not achieved.
