---
name: inspect-swift-correctness
description: Inspect Swift and Objective-C-interoperable code for behavioral defects, unsafe state, optional and error misuse, ARC ownership problems, concurrency violations, API-design hazards, and data-integrity risks. Use when reviewing Swift source, async or actor code, closures, protocols, persistence models, collection or string logic, or Objective-C and C boundaries; do not use for UI-only layout or build-system analysis.
---

# Objective

Trace changed Swift behavior through success, failure, cancellation, and boundary paths, then report only defects or material risks supported by code or test evidence.

# Inputs

Required: changed Swift or interoperability code, its callers or diff context, and applicable repository instructions.

Optional: target Swift and OS versions, tests, compiler diagnostics, crash logs, persistence schemas, generated interfaces, and concurrency settings.

# Workflow

1. Identify entry points, state owners, callers, side effects, and external boundaries.
2. Trace normal, empty, invalid, error, cancellation, and repeated-invocation paths.
3. Evaluate type assumptions, optionals, defaults, conversions, collection and string indexing, and state transitions.
4. Evaluate ownership and lifetime: strong references, closure captures, delegates, observers, timers, tasks, continuations, and cleanup.
5. Evaluate concurrency: isolation, `Sendable`, actor reentrancy, main-actor use, task hierarchy, cancellation, priority, ordering, and unsafe shared state.
6. Evaluate errors: preservation of cause, typed failures when used, recovery, fallbacks, and misleading success.
7. Evaluate API shape at the call site using Swift naming and protocol conventions.
8. Evaluate Objective-C, C, C++, unsafe pointer, and dynamic-runtime boundaries when present.
9. Check tests for the changed behavior and the failure mode behind each finding.
10. Return findings to the parent review; do not repeat architecture, security, UI, or build findings owned by adjacent Skills.

LOAD `references/swift-correctness-checklist.md` for detailed checks when the changed code reaches any listed area.

LOAD `references/official-sources.md` before making a version-sensitive language, concurrency, or API-design claim.

# Finding Contract

For each finding provide severity, label, file and stable location, trigger, expected behavior, observed or likely behavior, impact, smallest correction, validation, and confidence.

Use `Potential Risk` plus `Requires Validation` when a race, lifetime failure, or edge case is plausible but not provable from the available execution evidence.

# Ownership Boundaries

- This Skill owns behavioral correctness of ARC and concurrency constructs.
- `assess-apple-runtime-quality` owns measurable responsiveness, energy, leak, retry, and telemetry impact. Merge shared root causes rather than reporting twice.
- `assess-apple-ui-accessibility` owns UI lifecycle, presentation state, interaction, layout, and accessibility semantics.
- `assess-apple-security-privacy` owns trust, confidentiality, authorization, privacy, and secret exposure.

# Stop Conditions

State insufficient evidence when generated code, macros, build flags, Objective-C headers, persistence schemas, or caller context required to establish behavior is unavailable. Do not infer compilation or runtime success from syntax alone.
