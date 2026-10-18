# Severity, Labels, and Documentation Routing

## Severity

- **Critical** - Demonstrated or highly credible security compromise, data loss, production outage, privilege escalation, compliance violation, or incorrect behavior in a core workflow with immediate severe impact.
- **High** - Significant correctness, reliability, security, performance, or maintainability failure with material impact, but immediate catastrophic impact is not established.
- **Medium** - A real issue that should be fixed for correctness, reliability, performance, or safe maintenance but is not immediately dangerous.
- **Low** - Non-blocking cleanup, readability, minor refactor, or convention mismatch with a concrete maintenance benefit.

Do not classify missing evidence itself as a defect. Classify the supported risk and label it `Requires Validation`.

## Labels

Use one primary label and optional secondary labels:

- `Confirmed Issue`
- `Potential Risk`
- `Requires Validation`
- `Human Blocker`
- `Recommended Improvement`
- `Documentation Impact`
- `Configuration Dependency`
- `Security Sensitive`

## Documentation Routing

Recommend updates only when directly caused by the reviewed code.

| File | Owns |
|---|---|
| `README.md` | Repository purpose, installation, quick start, configuration overview, and navigation. |
| `CHANGELOG.md` | Completed features, fixes, enhancements, security fixes, and released changes. |
| `REVIEW.md` | Blockers only a human can resolve: approval, requirement, access, credential ownership, business, architecture, vendor, legal, or compliance decisions. |
| `TODO.md` | Actionable engineering work: defects, refactors, debt, tests, remediation, cleanup, validation, and directly caused documentation work. |
| `CHECKLIST.md` | Required input inventory: variables, placeholders, secret references, APIs, keys, certificates, deployment inputs, and configuration dependencies. |

If an engineer can resolve an item without human input, it does not belong in `REVIEW.md`.

## CHECKLIST Entry Contract

Each recommended entry contains:

- Variable Name
- Purpose
- Required
- Source
- Consumer
- Expected Format
- Validation Status
- Notes

Never include actual values. Expected formats use only `X` for letters, `0` for numbers, and `!` for symbols, for example `XXXXX00000!!!!!XXXXX`. Do not use realistic tokens, keys, URLs, GUIDs, tenant or subscription IDs, passwords, certificates, or connection strings.
