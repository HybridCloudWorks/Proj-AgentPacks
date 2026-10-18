---
name: assess-apple-runtime-quality
description: Assess Apple-platform changes for UI stalls, excessive work, memory or resource leaks, rendering churn, unbounded growth, network and storage inefficiency, battery or thermal risk, unsafe retries, weak failure handling, sensitive or noisy logging, and missing observability. Use when reviewing hot paths, main-actor work, lists, media, networking, persistence, background tasks, timers, notifications, logging, metrics, or performance-sensitive code.
---

# Objective

Identify plausible, material runtime and operational failures without recommending speculative micro-optimizations.

# Inputs

Required: changed runtime path, its frequency and lifecycle context, and the code or configuration that controls work and resources.

Optional: scale assumptions, device classes, performance requirements, Instruments traces, MetricKit data, crash logs, telemetry, and network conditions.

# Workflow

1. Identify latency-sensitive paths, expected data volume, frequency, concurrency, foreground or background state, and resource constraints.
2. Trace CPU, allocation, I/O, network, persistence, image or media, serialization, and rendering work.
3. Evaluate main-actor blocking, repeated computation, invalidation breadth, batching, pagination, caching, streaming, backpressure, and cancellation.
4. Evaluate memory and resource lifetime: tasks, timers, observers, file handles, sockets, database contexts, subscriptions, image buffers, and caches.
5. Evaluate background execution, energy, thermal, network, location, animation, and wake-up behavior.
6. Trace failure paths, error propagation, retries, backoff, idempotency, fallbacks, user messaging, and recovery.
7. Evaluate logs, privacy annotations, signposts, metrics, crash context, and whether important failures can be diagnosed.
8. Correlate findings with tests, measurements, traces, or a concrete scale model when available.
9. Return trigger, impact, evidence, recommendation, trade-off, validation, and confidence.

LOAD `references/runtime-quality-checklist.md` for detailed checks.

LOAD `references/official-sources.md` before making version-sensitive performance, background-execution, or logging claims.

# Evidence Threshold

Record a performance finding only when one of these exists:

- A demonstrably expensive operation on a frequent or latency-sensitive path.
- Unbounded work or storage with a credible growth path.
- A resource lifetime that is not closed or cancelled.
- A measured regression or failed performance requirement.
- A clear platform violation such as blocking UI work.

Otherwise note a measurement suggestion without assigning defect severity.

# Finding Contract

For each finding state trigger, frequency or scale assumption, affected path or resource, evidence, user or operational impact, recommendation, trade-off, validation method, and confidence. Distinguish measured regressions from plausible risks that still require profiling.

# Ownership Boundaries

- This Skill owns runtime impact, error handling, retry behavior, logging, telemetry, and resource use.
- `inspect-swift-correctness` owns the underlying ARC or concurrency correctness defect. Merge one root cause with both impacts.
- `assess-apple-ui-accessibility` owns UI state and accessibility semantics.
- `assess-apple-security-privacy` owns sensitive logging and confidentiality impact; this Skill owns diagnostic quality and volume.

# Stop Conditions

State missing evidence when production scale, device class, network conditions, performance requirements, Instruments traces, crash logs, or telemetry are needed to establish impact. Never invent measurements.
