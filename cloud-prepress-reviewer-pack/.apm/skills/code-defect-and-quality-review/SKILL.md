---
name: code-defect-and-quality-review
description: Performs evidence-first code review for defects, logic, maintainability, error handling, observability, performance, and safe behavior across changed application code.
---

# Code, Defect, and Quality Review

Review changed code in context. Trace normal and failure paths, null/empty/invalid inputs, state transitions, concurrency, retries, cleanup, side effects, user-visible errors, and downstream contracts. Inspect tests for meaningful behavior, edge cases, negative paths, and regressions.

Review quality only when it changes correctness, safety, operability, or future change risk. Consider complexity, duplication, hidden coupling, configuration ownership, resource leaks, unbounded work, N+1 I/O, and misleading comments. Do not turn style preference into a blocking finding.

Each finding needs stable ID, severity, file and line, trigger or reproduction, expected versus actual behavior, impact, concrete fix, and verification step. If it cannot be proven from available evidence, label it as a validation hypothesis.
