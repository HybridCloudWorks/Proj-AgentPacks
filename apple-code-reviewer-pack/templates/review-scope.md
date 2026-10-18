# Review scope and evidence plan

Complete this before writing any finding. It records the scope summary that `review-apple-code` produces in its first step, and its contents become the Review Scope section of the completion report. Replace each `<...>` field; write "none" or "not determined" rather than leaving a field blank.

## Target

- Review target: `<pull request, branch and base, commit range, release candidate, or supplied diff>`
- Base and head commits reviewed: `<short hashes, or "supplied diff, no commits">`
- Change type: `<pull request | feature | bug fix | refactor | security | performance | release | audit of AI-generated code>`
- Goal and acceptance criteria: `<from the request or pull-request description, or "none stated">`
- Claims to check: `<for AI-generated code or a release: each claim made about the change, such as "tests pass">`

## Technology and platforms

- Languages and frameworks: `<Swift, Objective-C, SwiftUI, UIKit, AppKit, ...>`
- Targets, packages and extensions in scope: `<names>`
- Platforms and minimum OS versions: `<for example "iOS 17.0, read from the project build settings">`
- Swift language mode and strict-concurrency setting: `<value and the file it came from, or "not determined">`
- Build system and dependency managers: `<Xcode project or workspace, SwiftPM, CocoaPods, Carthage, Tuist, XcodeGen>`

## Evidence inventory

Record what exists and what does not before analysis. Missing evidence is a limitation to report, not a defect.

| Evidence | Available | Source | Notes |
|---|---|---|---|
| Diff and changed files | | | |
| Repository instructions | | | |
| Toolchain detector report | | | |
| Local build or test commands | | | |
| CI runs for the head commit | | | |
| Crash logs, traces, telemetry | | | |
| Product or design requirements | | | |
| Backend or server behavior | | | |

## Routing plan

Activate only the Skills the changed code reaches. Give a reason for every Skill not activated; it becomes the "not applicable" line in Category Results.

| Changed area | Files | Skill | Activated | Reason |
|---|---|---|---|---|
| Swift behavior, state, ARC, concurrency, interoperability | | `inspect-swift-correctness` | | |
| Views, navigation, layout, localization, accessibility | | `assess-apple-ui-accessibility` | | |
| Identity, data, storage, network, entitlements, privacy | | `assess-apple-security-privacy` | | |
| Responsiveness, resources, retries, logging, telemetry | | `assess-apple-runtime-quality` | | |
| Project, packages, configuration, tests, CI, release | | `verify-apple-build-tests` | | |

## Boundaries

- Primary risk areas: `<list>`
- Exclusions: `<what was not reviewed and why>`
- Dot-prefixed folders inspected: `<none, or the folder and the condition that justified it>`
- Repository overrides that apply: `<none, or the condition found, such as a Linux environment or a cancelled CI run>`
- Not verifiable from available context: `<list>`
