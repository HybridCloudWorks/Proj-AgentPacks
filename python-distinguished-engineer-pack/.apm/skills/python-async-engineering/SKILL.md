---
name: python-async-engineering
description: Build and diagnose Python async workers and services with bounded concurrency, cancellation and deterministic cleanup. Use when async I/O, worker lifecycle, task leaks, throughput, timeouts or concurrent shared state is affected.
---

# Python Async Engineering

## Activation and scope

Async I/O, worker lifecycle, task leaks, throughput, timeouts or concurrent shared state is affected. Load tests against shared systems require scoped authorization; performance claims require measurements.

## Inputs and dependencies

- Inputs: Task/queue lifecycle, client APIs, deadlines, retry policy, capacity and shutdown requirements.
- Dependencies: Supported asyncio APIs or repository concurrency framework and isolated tests.
- Owner: the primary Python Distinguished Engineer; use a specialist only when its isolated evidence helps the task.

## Workflow

1. Classify CPU and I/O work; find blocking SDK, database, filesystem and subprocess calls in event-loop paths. Use existing async clients or a controlled offload boundary.
2. Specify task ownership, total deadline versus per-attempt timeout, bounded semaphore/queue/pool sizes, backpressure and overload response. Use supported structured concurrency when it matches repository lifecycle.
3. Propagate cancellation after cleanup. Do not swallow CancelledError or shield whole workflows. State whether partial work is drained, checkpointed or cancelled at shutdown.
4. Retry only transient, safe operations with bounded backoff/jitter and an overall budget. Explain duplicate-delivery/idempotency effects. Test timeout, cancellation during I/O, saturated queue, exception propagation and connection release.

## Output and validation

Lifecycle design or patch with cancellation/timeout regression tests, capacity limits and graceful-shutdown evidence. Record exact checks run, observed failures and unavailable evidence. A draft, static check or local mock does not establish live behavior.

## Failure and guardrails

Leaked tasks, swallowed cancellation, unbounded queues/retries, blocking I/O or inability to stop shared test workloads. Preserve existing user work; stop only the dependent operation when a material input or required approval is missing, and continue useful authorized work. A specialist cannot self-approve or expand the assignment.

## Workflow connection

Within the complete pack, the optional `debug-python-issue.prompt.md` recipe connects this Skill to the primary workflow. This Skill is self-contained when installed individually; no external prompt or specialist is required. With the full pack installed, the `python-engineering-contract` instruction supplies the approval, handoff and completion rules.
