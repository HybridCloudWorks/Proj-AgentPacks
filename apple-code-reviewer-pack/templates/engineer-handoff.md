# Engineer handoff

Use this when the Engineer Handoff Notes of a review are passed to the engineer who will fix the change, or when a review stops before it can complete. It expands the handoff fields of the completion report so the next engineer can work without repeating the review. It does not replace the report.

## Review reference

- Report: `<title or link of the Apple code review report>`
- Target and head commit: `<pull request, branch or range; short hash>`
- Recommendation: `<Approved | Approved with comments | Changes requested | Blocked>`
- Reviewed on: `<date>`

## Current state

One line per fact, each with its evidence.

- Builds: `<where, which command, exit status; or "not built: reason">`
- Tests: `<where, which command or CI run, result; or "not run: reason">`
- Open findings: `<counts by severity>`

## Highest risks

| ID | Severity | Title | Why it matters |
|---|---|---|---|
| | | | |

## Required fixes

| ID | Smallest defensible correction | Files | Done when |
|---|---|---|---|
| | | | |

## Suggested work order

1. `<ID>`: `<reason it goes first, such as another fix depends on it>`
2. `<ID>`

## Validation requirements

Where it must run: this environment, macOS with the Xcode version the repository selects, CI, a physical device, or protected infrastructure.

| Check | Command or method | Where it must run | Expected result | Covers |
|---|---|---|---|---|
| | | | | |

## Human blockers

Only decisions an engineer cannot make alone: approval, requirements, access, credential ownership, business, architecture, vendor, legal or compliance. Write "None" when empty.

| Decision needed | Owner role | Finding | Blocked until decided |
|---|---|---|---|
| | | | |

## Configuration dependencies

Never write a value. Expected formats use only `X` for letters, `0` for numbers and `!` for symbols.

| Name | Consumer | Source | Expected format | Validation status |
|---|---|---|---|---|
| | | | | |

## Not verified

List every check that did not run, and why: no macOS or Xcode, CI cancelled, no device, backend not inspectable, requirement missing.
