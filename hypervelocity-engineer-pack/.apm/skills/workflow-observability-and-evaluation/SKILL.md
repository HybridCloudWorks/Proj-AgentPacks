---
name: workflow-observability-and-evaluation
description: Observe agentic workflow runs and evaluate quality, safety, cost, latency, and reliability with reproducible evidence.
---

# Workflow Observability and Evaluation

Use this skill when a user asks why an agentic workflow behaved a certain way, whether an optimization helped, or whether a workflow is reliable enough to operate.

## Evidence model

- Collect run URL or identifier, commit, workflow source, generated artifact, trigger, inputs, tools, model or engine, timestamps, outputs, errors, and approvals when available.
- Use `gh aw logs` and `gh aw audit` for GitHub Agentic Workflow evidence when authorized. Preserve step summaries and artifacts rather than relying on the final chat response.
- Use OpenTelemetry traces or repository telemetry only when configured; redact prompt content, secrets, tokens, and sensitive identifiers.
- Label each conclusion as observed, inferred, unavailable, or requiring a live-system check.

## Evaluation contract

Define the task set and acceptance criteria before changing the workflow. Measure at least:

- correctness and task completion;
- safety violations, unauthorized mutations, and policy escapes;
- latency, retries, failures, and human-review burden;
- token or cost data only when the platform exposes it; and
- reproducibility across comparable runs.

Compare before and after on equivalent inputs. Include negative, ambiguous, oversized, malicious, permission-denied, timeout, and duplicate-event cases. Do not treat more output, fewer tokens, or a successful process exit as proof of better quality.

## Optimization gate

Change one major variable at a time where practical, retain a rollback, and record the hypothesis, metric, sample, result, and uncertainty. Stop or revert when quality or safety regresses even if throughput improves.
