---
description: "Review Apple-platform changes for responsiveness, memory, energy, retry and logging risk"
agent: apple-code-reviewer
---

# Review Apple runtime quality

## Inputs

- The changed runtime path, how often it runs, and its lifecycle: per launch, per screen, per list cell, per keystroke, foreground or background.
- Scale assumptions such as data volume, device classes and network conditions, when the user or repository states them.
- Optional: performance requirements, Instruments traces, MetricKit payloads, crash logs, telemetry and earlier measurements.

## Workflow

1. Activate `review-apple-code` and state that the review focuses on runtime behavior.
2. Apply `assess-apple-runtime-quality`. Trace CPU, allocation, I/O, network, persistence, decoding and rendering work on the changed path; main-actor blocking; the lifetime of tasks, timers, observers and caches; background execution and energy; failure paths, retries and backoff; and whether logs and signposts would let someone diagnose a failure.
3. Apply the Skill's evidence threshold. Record a performance finding only for an expensive operation on a frequent or latency-sensitive path, unbounded work or storage with a credible growth path, a resource that is never closed or cancelled, a measured regression, or a clear platform violation. Everything else becomes a measurement suggestion with no severity.
4. When the root cause is an ARC or concurrency defect, bring in `inspect-swift-correctness` and report one merged finding.
5. Never invent a measurement. Name the trace or metric that would confirm each plausible risk.

## Expected output

The review report the contract requires. Each runtime finding states its trigger, frequency or scale assumption, evidence, user or operational impact, recommendation, trade-off and validation method, and says whether the impact was measured or still needs profiling. Measurement suggestions appear under Performance and Energy in Category Results, not as findings. Follow the `apple-code-reviewer-contract` instruction.
