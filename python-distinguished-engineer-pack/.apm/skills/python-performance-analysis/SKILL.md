---
name: python-performance-analysis
description: Measure Python service, worker, data and agent latency, throughput, memory and cost bottlenecks. Use when a measurable performance issue or explicit performance/cost objective exists.
---

# Python Performance Analysis

## Activation and scope

A measurable performance issue or explicit performance/cost objective exists. Do not report faster code from intuition or a single unrepresentative timing.

## Inputs and dependencies

- Inputs: Representative workload/data, environment, baseline, SLOs, resource and cost limits.
- Dependencies: Configured profiler/benchmark tooling and approved isolated workload generator.
- Owner: the primary Python Distinguished Engineer; use a specialist only when its isolated evidence helps the task.

## Workflow

1. State workload, percentiles, throughput/memory/cost objective, environment and repeatability. Profile before choosing optimization.
2. Review algorithms/allocation, serialization, network/DB round trips, N+1, pooling, batching, queueing, event-loop blocking and concurrency saturation.
3. For agent workloads measure redundant retrieval/model/tool calls, context length, caching correctness/invalidation and bounded budgets; do not trade correctness or isolation for cost.
4. Compare before/after with warm-up/repetitions and variability; run correctness/security regression checks and identify production-representativeness limits. Shared-system load/capacity changes need scoped approval.

## Output and validation

Measured bottleneck, experiment/patch, before/after results and variance, trade-offs, rollback and remaining uncertainty. Record exact checks run, observed failures and unavailable evidence. A draft, static check or local mock does not establish live behavior.

## Failure and guardrails

No representative baseline, noisy experiment, changed workload, cost overrun or unsafe shared load. Preserve existing user work; stop only the dependent operation when a material input or required approval is missing, and continue useful authorized work. A specialist cannot self-approve or expand the assignment.

## Workflow connection

Within the complete pack, the optional `debug-python-issue.prompt.md` recipe connects this Skill to the primary workflow. This Skill is self-contained when installed individually; no external prompt or specialist is required. With the full pack installed, the `python-engineering-contract` instruction supplies the approval, handoff and completion rules.
