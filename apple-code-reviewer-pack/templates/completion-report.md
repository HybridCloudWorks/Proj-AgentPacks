# Apple Code Review Report

<!--
Completion report for every workflow in this pack. The canonical template is the
`review-apple-code` Skill asset `assets/review-report-template.md`; this copy adds the allowed
values and fill-in guidance. If the two ever differ, the Skill asset wins. Keep every section,
even when its content is "None" or "Not applicable", with a reason.
Severity: Critical | High | Medium | Low.
Labels (one primary, optional secondary): Confirmed Issue, Potential Risk, Requires Validation,
Human Blocker, Recommended Improvement, Documentation Impact, Configuration Dependency,
Security Sensitive.
Recommendation: Approved | Approved with comments | Changes requested | Blocked.
Never reproduce a secret: write [REDACTED_POSSIBLE_SECRET].
Never present a check that did not run as passed.
-->

## Executive Summary

- Overall code health: `<one or two sentences>`
- Highest-risk findings: `<IDs and severities, or "None">`
- Release readiness: `<ready, not ready, or not established, with the reason>`
- Evidence limitations: `<toolchain, CI, device, backend or requirement evidence that was unavailable>`

## Review Scope

- Review target: `<pull request, branch, commit range or diff; base and head commits>`
- Files and components reviewed: `<changed files, plus context files read>`
- Technologies and platforms: `<languages, frameworks, platforms and minimum OS versions>`
- Change type: `<pull request | feature | bug fix | refactor | security | performance | release | audit of AI-generated code>`
- Primary risk areas: `<list>`
- Constraints and exclusions: `<read-only, folders or areas excluded and why>`
- Not verifiable from available context: `<list>`

## Findings Summary

`Critical: 0 | High: 0 | Medium: 0 | Low: 0`

## Detailed Findings

<!-- Order by severity, then dependency order. One finding per root cause; cite every consequence. -->

### ACR-001 - `<concise finding title>`

- **Severity:** `<Critical | High | Medium | Low>`
- **Label:** `<primary label; secondary labels>`
- **File:** `<path>`
- **Location:** `<line range or nearest stable symbol>`
- **Category:** `<Architecture | Code Quality | Correctness and Logic | UI and Accessibility | Security and Privacy | Performance and Energy | Error Handling and Observability | Tests | Dependencies and Configuration>`
- **Confidence:** `<High | Medium | Low>`
- **Description:** `<what is wrong>`
- **Evidence:** `<code, configuration, test, log or official-document evidence>`
- **Trigger or reproduction:** `<condition or steps>`
- **Expected behavior:** `<what should happen>`
- **Observed or likely behavior:** `<what happens or will happen>`
- **Impact:** `<user, data, security, operational or maintenance impact>`
- **Recommendation:** `<direction of the fix>`
- **Suggested fix:** `<smallest defensible correction>`
- **Validation needed:** `<test, command or check, and where it must run>`
- **Risk if unfixed:** `<consequence of merging or releasing as is>`

## Category Results

<!-- For each category: finding IDs, what was verified, or "Not applicable" / "Not reviewed" with a reason. -->

### Architecture

<!-- When nothing is supported, write exactly: No architecture concerns were identified from the available context. -->

### Code Quality

### Correctness and Logic

### UI and Accessibility

### Security and Privacy

### Performance and Energy

<!-- Measurement suggestions that do not meet the evidence threshold go here, with no severity. -->

### Error Handling and Observability

### Tests

<!-- Commands actually run: command, exit status, result. CI runs: workflow, job, commit, conclusion.
Missing tests: type, scenario, setup, action, expected assertion, why it matters, regression caught. -->

### Dependencies and Configuration

## Documentation Impact

- `README.md` updates: `<or "None">`
- `CHANGELOG.md` entries: `<or "None">`
- `REVIEW.md` human blockers: `<or "None">`
- `TODO.md` engineering actions: `<or "None">`
- `CHECKLIST.md` input entries: `<or "None">`

## Merge or Release Recommendation

`<Approved | Approved with comments | Changes requested | Blocked>` - `<justification tied to finding IDs and evidence>`

## Engineer Handoff Notes

- Current state: `<what builds, passed, failed or did not run>`
- Highest risks: `<IDs>`
- Required fixes: `<IDs>`
- Suggested work order: `<ordered IDs and why>`
- Validation requirements: `<checks and where each must run>`
- Human blockers: `<decision and owner role, or "None">`
- Configuration dependencies: `<names, or "None">`
