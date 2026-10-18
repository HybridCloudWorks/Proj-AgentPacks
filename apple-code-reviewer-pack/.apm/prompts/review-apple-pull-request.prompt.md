---
description: "Review an Apple-platform pull request or branch diff and recommend whether it can merge"
agent: apple-code-reviewer
---

# Review an Apple-platform pull request

## Inputs

- The review target: a pull-request number or link, a branch or commit range, or a pasted diff. When only a branch is named, resolve its merge base with read-only git commands and state the base and head commits you reviewed.
- Target platforms and minimum OS versions. Read them from the project settings or package manifest when the user does not state them.
- Evidence the user supplies or the host exposes: CI runs, build or test logs, crash reports, screenshots or performance traces.
- The goal of the change and any acceptance criteria in the pull-request description.

Feature, bug-fix and refactor reviews all use this prompt; record the change type in the scope.

Record every input you could not obtain before you write any finding.

## Workflow

1. Activate `review-apple-code` and give it the target, constraints and evidence. It owns scope, architecture and code-quality review, routing, de-duplication and the report.
2. Let it route each changed area to its domain Skill, and activate only the ones that apply:
   - `inspect-swift-correctness` for Swift or Objective-C behavior, state, ARC, async code and actors.
   - `assess-apple-ui-accessibility` for SwiftUI, UIKit or AppKit views, navigation, layout, localization and accessibility.
   - `assess-apple-security-privacy` for identity, credentials, storage, networking, deep links, WebKit, entitlements and privacy declarations.
   - `assess-apple-runtime-quality` for main-actor work, rendering, resource lifetime, retries, logging and telemetry.
   - `verify-apple-build-tests` for project, package, dependency, configuration, test and CI files, and whenever the recommendation depends on build or test evidence.
3. Run only non-destructive validation that the detected toolchain and the repository support. Record each command exactly, with its exit status.
4. Keep the review read-only. Do not edit files, push commits, post review comments, or approve or merge on the hosting service.

## Expected output

One Apple code review report containing every section the contract requires: findings numbered `ACR-001` onward in severity order, severity counts, one of the four allowed recommendations with its justification, and engineer handoff notes. Name every check that was not run or could not run, and never present it as passed. Follow the `apple-code-reviewer-contract` instruction.
