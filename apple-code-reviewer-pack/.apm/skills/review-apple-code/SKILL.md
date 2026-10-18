---
name: review-apple-code
description: Review an Apple-platform code change end to end and produce a severity-classified, evidence-based, handoff-ready report. Use for Swift, SwiftUI, UIKit, AppKit, Objective-C interoperability, Xcode, SwiftPM, Apple CI, pull requests, branch diffs, feature or bug-fix reviews, refactors, security or performance changes, and audits of AI-generated Apple code; do not use for implementing fixes or broad documentation cleanup.
---

# Objective

Run the complete code-review SOP once, route Apple-specific analysis to focused Skills, and return actionable findings without duplicated commentary or unsupported claims.

# Inputs

Use the diff or requested files, repository instructions, nearby code, target platforms, OS deployment targets, and available build, test, CI, crash, security, or performance evidence. Record unavailable evidence before making findings.

# Workflow

## 1. Establish scope

Identify the review target, change type, languages and frameworks, target platforms, runtime and deployment constraints, primary risk areas, exclusions, and unverifiable items. Output the scope summary before detailed findings.

LOAD `references/core-review-checklist.md` for scope, architecture, quality, evidence, and dot-folder rules.

## 2. Understand architecture and code quality

Trace the changed behavior through callers, state owners, dependencies, and external boundaries. Evaluate responsibility placement, dependency direction, coupling, cohesion, naming, complexity, duplication, hidden side effects, safe changeability, and consistency with nearby patterns.

If no architecture concern is supported, state: `No architecture concerns were identified from the available context.`

## 3. Run applicable domain reviews

Activate only the Skills relevant to the change:

| Changed area | Required Skill |
|---|---|
| Swift or Objective-C behavior, state, ARC, async code, actors, protocol or API design | `inspect-swift-correctness` |
| SwiftUI, UIKit, AppKit, navigation, lifecycle, layout, localization, input, accessibility | `assess-apple-ui-accessibility` |
| Data, identity, permissions, storage, network, WebKit, Keychain, entitlements, privacy | `assess-apple-security-privacy` |
| Responsiveness, rendering, energy, resource lifetime, retries, logging, telemetry | `assess-apple-runtime-quality` |
| Xcode, SwiftPM, dependencies, schemes, signing inputs, tests, CI, release validation | `verify-apple-build-tests` |

A finding belongs to one owning category. If several Skills observe the same root cause, merge it and cite all affected consequences.

## 4. Check direct documentation impact

LOAD `references/severity-labels-routing.md`. Recommend only documentation changes directly caused by the reviewed code. Do not perform repository-wide consolidation.

LOAD `references/repository-overrides.md` only when its named files or conditions exist in the repository.

## 5. Validate and de-duplicate

Before reporting:

1. Remove duplicate symptoms and merge shared root causes.
2. Confirm each severity against demonstrated impact.
3. Confirm each finding has evidence, location, trigger, impact, correction, and validation.
4. Separate confirmed issues from potential risks and missing evidence.
5. Separate human blockers from engineering work.
6. Confirm no secret or realistic sensitive value appears.
7. Confirm dot-prefixed folders were handled only when justified.
8. Remove style-only comments that do not create material risk.

## 6. Produce the report

Use `assets/review-report-template.md` exactly, omitting no required section. Keep findings ordered by severity, then dependency order. Use stable IDs such as `ACR-001`.

# Severity and Labels

Use only the severity definitions and labels in `references/severity-labels-routing.md`. Do not inflate severity to make a recommendation more prominent.

# Evidence Standard

For every finding include:

- The concrete code, configuration, test, log, or official-document evidence.
- File and line or nearest stable symbol.
- Trigger or reproduction condition.
- Expected behavior and observed or likely behavior.
- User, data, security, operational, or maintenance impact.
- Smallest defensible correction.
- Validation needed after correction.
- Confidence: high, medium, or low.

When evidence is insufficient, report `Requires Validation` rather than asserting a defect.

# Review Posture

- Remain read-only unless the user starts a separate implementation task.
- Run only non-destructive validation.
- Never imply Xcode, simulator, device, signing, or XCTest success without observed macOS toolchain output.
- Redact suspected secrets as `[REDACTED_POSSIBLE_SECRET]`.
- Prefer current official Apple and Swift sources for version-sensitive claims.

# Completion Criteria

Complete only when:

1. Scope and limitations are explicit.
2. Architecture and code quality are addressed.
3. Correctness, security, performance, error handling, tests, dependencies, configuration, and documentation impact are addressed or marked not applicable with a reason.
4. Findings are de-duplicated and severity-counted.
5. A merge or release recommendation is justified.
6. Handoff notes identify current state, highest risks, work order, validation, human blockers, and configuration dependencies.
