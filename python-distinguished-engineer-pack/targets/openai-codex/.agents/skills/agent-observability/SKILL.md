---
name: agent-observability
description: Instrument Python services and agent runs with useful metrics, traces, provenance and redaction. Use when operational diagnostics, service telemetry, agent tracing or run-cost visibility changes.
---

# Agent Observability

## Activation and scope

Operational diagnostics, service telemetry, agent tracing or run-cost visibility changes. Telemetry success does not prove business correctness or authorize broad collection.

## Inputs and dependencies

- Inputs: Service/run boundaries, operators/SLOs, existing telemetry/version and data classification.
- Dependencies: Existing logging/metrics/tracing stack; approved collector/export destination.
- Owner: the primary Python Distinguished Engineer; use a specialist only when its isolated evidence helps the task.

## Workflow

1. Map request/correlation/trace IDs, errors/latency/throughput/saturation, queues/retries, dependency health, resources, deployment version and approved business outcomes.
2. For agents add run/session identity, model/prompt/tool/Skill/evaluation versions, handoffs, retrieval provenance, policy/approval outcomes, token/cost budgets and termination reason.
3. Design redaction and retention before exporting telemetry. Exclude tokens, cookies, raw documents, source, sensitive prompts/outputs and unredacted arguments; control high-cardinality labels.
4. Use supported OpenTelemetry-compatible conventions where available, with bounded export overhead and failure isolation. Test redaction, correlation across async/tool boundaries, sampling and collector outage.

## Output and validation

Signal/alert design or instrumentation patch with redaction tests, operator actions, export costs and limits. Record exact checks run, observed failures and unavailable evidence. A draft, static check or local mock does not establish live behavior.

## Failure and guardrails

Sensitive export, missing correlation, high-cardinality explosion, telemetry-caused request failure or false live-health claim. Preserve existing user work; stop only the dependent operation when a material input or required approval is missing, and continue useful authorized work. A specialist cannot self-approve or expand the assignment.

## Workflow connection

Within the complete pack, the optional `debug-python-issue.prompt.md` recipe connects this Skill to the primary workflow. This Skill is self-contained when installed individually; no external prompt or specialist is required. Consult shared instruction, handoff and completion contracts when the full pack is available.
