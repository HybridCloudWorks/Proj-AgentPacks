# Build and test evidence record

The record `verify-apple-build-tests` returns. It feeds the Tests and the Dependencies and Configuration sections of the completion report, and the validation requirements in the handoff. Record only what actually happened.

## Environment

- Detector command: `python3 scripts/detect_apple_toolchain.py --root <repository> --format markdown`, run from the `verify-apple-build-tests` Skill directory
- OS and architecture: `<from the detector>`
- Capabilities: `can_run_xcodebuild <yes|no>`, `can_run_swift_package_commands <yes|no>`, `can_run_apple_ui_tests <yes|no>`, `can_validate_signing_or_archive <yes|no>`
- Limitations reported by the detector: `<copy them>`
- Xcode and Swift versions the repository or CI selects: `<value and source, or "not stated">`

## Project inventory

- Projects and workspaces: `<names>`
- Schemes and destinations named by the repository or CI: `<names and source; never guessed>`
- Packages, dependency managers and lockfiles: `<names>`
- Test targets: `<unit, UI, Swift Testing, XCTest>`
- CI files: `<paths>`

## Commands run

| # | Command | Working directory | Exit status | Result summary | Tree unchanged afterwards |
|---|---|---|---|---|---|
| 1 | | | | | |

## Results

- Verified passes: `<command or CI job, and what it proves>`
- Observed failures: `<command or job, error summary>`
- Unavailable validation: `<check, and the reason it could not run here>`

## CI evidence

Use the conclusion exactly as the CI reports it: success, failure, cancelled, timed out, skipped, neutral. A cancelled or timed-out job is not a pass; find out whether it hit a time limit, ran out of resources, was superseded or was cancelled by hand.

| Workflow and job | Run | Commit | Conclusion | Duration | Notes |
|---|---|---|---|---|---|
| | | | | | |

## Test coverage of the change

| Test type | Scenario | Setup | Action | Expected assertion | Why it matters | Regression it catches | Exists |
|---|---|---|---|---|---|---|---|
| | | | | | | | |

## Dependency and configuration findings

Kind: build setting, xcconfig variable, Info.plist key, entitlement, capability, privacy manifest entry, package, certificate reference or placeholder. Never record a value.

| Name | Kind | Source | Consumer | Expected format | Validation | Owner |
|---|---|---|---|---|---|---|
| | | | | | | |

## Still required

| Validation | Where it must run | Owner | Blocks |
|---|---|---|---|
| | | | |
