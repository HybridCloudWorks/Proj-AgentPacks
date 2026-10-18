---
description: "Review changed Swift for concurrency, ARC, optional, error-handling and interoperability defects"
agent: apple-code-reviewer
---

# Review Swift correctness

## Inputs

- The changed Swift or Objective-C-interoperable code and its callers.
- The Swift language mode, compiler version and strict-concurrency setting from the project or package, when they can be read.
- Optional: tests for the changed behavior, compiler diagnostics, crash logs, persistence schemas and generated interfaces.

## Workflow

1. Activate `review-apple-code` and state that the user asked for a correctness-focused review.
2. Apply `inspect-swift-correctness`. Trace the normal, empty, invalid, error, cancellation and repeated-invocation paths. Check isolation and `Sendable` boundaries, actor state across each `await`, continuation resumption, closure captures and cleanup, and any Objective-C, C or unsafe-pointer boundary.
3. Where a defect also has a measurable runtime cost, bring in `assess-apple-runtime-quality` and report one merged finding that cites both impacts.
4. Do not report a strict-concurrency diagnostic as a build error until you have confirmed the active language mode and settings.
5. When a race or lifetime failure is plausible but not provable from the evidence, label it `Potential Risk` and `Requires Validation`, and name the test or experiment that would settle it.

## Expected output

The review report the contract requires. Category Results covers every category; mark the ones outside the requested focus as not reviewed and say why. Each correctness finding names its trigger, expected and likely behavior, smallest correction, and the test that would catch a regression. Follow the `apple-code-reviewer-contract` instruction.
