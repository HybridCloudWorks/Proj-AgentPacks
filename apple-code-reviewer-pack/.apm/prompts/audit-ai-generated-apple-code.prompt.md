---
description: "Audit AI-generated Swift or Apple-platform code for defects, unsupported claims and missing tests"
agent: apple-code-reviewer
---

# Audit AI-generated Apple code

## Inputs

- The generated files or diff, and the task the generator was asked to perform when the user can supply it.
- Every claim that came with the code, such as "builds", "all tests pass", "handles every edge case" or "works on iOS and macOS".
- The repository around the change: the code it calls, existing helpers it may duplicate, and the targets and minimum OS versions it ships in.

## Workflow

1. Activate `review-apple-code` with the change type set to an audit of AI-generated code. Treat each generator claim as unverified until you observe evidence for it.
2. Apply `inspect-swift-correctness` to every generated Swift or interoperability path. Give extra attention to empty, failure, cancellation and repeated-call paths; forced unwraps and `try!`; `@unchecked Sendable` and other suppressed compiler checks; continuations; and APIs that may not exist at the declared deployment target. Check version-sensitive API claims against the official sources the Skill lists.
3. Apply `verify-apple-build-tests` to establish what can be built and tested in this environment, whether the claimed tests exist, and whether they assert the behavior they are named for.
4. Apply `assess-apple-ui-accessibility`, `assess-apple-security-privacy` or `assess-apple-runtime-quality` only where the generated code reaches their areas. Placeholder credentials and sample keys are security findings; write any such value as `[REDACTED_POSSIBLE_SECRET]`.
5. Compare the generated code with nearby repository patterns. Report duplication or drift only where it creates a correctness or maintenance risk.
6. Do not fix the code or add tests yourself; this is a read-only audit.

## Expected output

The full review report the contract requires. In Review Scope, list each generator claim with its status: observed, contradicted, or not verifiable here. Label findings that depend on unobserved behavior `Requires Validation`. Follow the `apple-code-reviewer-contract` instruction.
