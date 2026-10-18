# Optimization plan and evaluation record

Produced by `optimize-agentic-workflow`, which requires a plan before editing, and `workflow-observability-and-evaluation`, which requires the evaluation contract and experiment record. Present the first four sections for approval before changing anything.

## Baseline

| Field | Value | Source | Label |
|---|---|---|---|
| Workflow | | | |
| Run ID or URL | | | |
| Guardrail exceeded | <AI credits / daily budget / tool denials / timeout or max turns> | | |
| Input tokens | | `gh aw audit <run-id> --json` | observed / unavailable |
| Output tokens | | | |
| Cached tokens | | | |
| Agent-usage tokens | | | |
| Tool calls, denials, failures | | | |
| Duration | | | |
| Outcome and output quality | | | |

## Cost classification

| Area | Share | Recurring or one-time | Evidence | Label |
|---|---|---|---|---|
| Context assembly | | | | |
| Prompt generation | | | | |
| Tool interaction | | | | |
| Orchestration | | | | |
| Memory | | | | |
| Output handling | | | | |

Three largest drivers: <1, 2, 3>

## Proposed changes

| # | Change | Driver | Expected effect | Risk |
|---|---|---|---|---|
| | | | | |

Explicitly unchanged unless approved here: model, permissions, cadence, safe outputs.

## Evaluation contract (fixed before editing)

| Item | Value |
|---|---|
| Task set | |
| Acceptance criteria | |
| How inputs are kept equivalent | |
| Negative cases included | |
| Rollback | <revert source and lock together> |
| Authorized runs and budget | |

## Experiment log

Change one major variable at a time where practical.

| Hypothesis | Variable changed | Metric | Sample | Result | Uncertainty |
|---|---|---|---|---|---|
| | | | | | |

## Comparison

| Metric | Before | After | Observed or projected |
|---|---|---|---|
| Acceptance criteria met | | | |
| Safety and policy | | | |
| Input tokens | | | |
| Tool calls | | | |
| Duration | | | |

## Decision

<keep / revise / revert>, decided by <owner>. Stop or revert when quality or safety regresses, even if cost improves.
