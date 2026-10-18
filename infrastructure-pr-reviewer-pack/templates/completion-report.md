# Infrastructure review completion report

Schema version 1.0. This is the annotated, human-facing form of the report that the `infrastructure-pr-reviewer-contract` instruction requires and that `.apm/skills/review-infrastructure-pr/assets/review-report-template.md` lays out. If this file and those two ever disagree, the installed instruction and asset win.

Keep the nine sections in this order. Write "None" in a section that has nothing to report; do not delete it.

## Executive Summary

- Overall assessment: <one sentence on whether the transition is correct, safe, repeatable and recoverable on the evidence reviewed>
- Highest-risk finding: <Finding ID and title, or "None">
- Reviewed transition: <from what managed state to what proposed state>
- Release or merge readiness: <the disposition, restated in plain words; never "approved">

## Review Scope

- Base and head: <full SHAs>
- Files and technologies: <count of files, and each technology present>
- Entry points and execution order: <numbered sequence, one tool per step>
- Targets, identities, state, and ownership: <each environment, scope, identity, state key, inventory, namespace, and the tool that owns each object>
- Evidence reviewed: <each artifact, with the commit it was generated from>
- Constraints and exclusions: <what was out of reach and why: no downloads, no cluster access, files outside the diff not read, and so on>

## Coverage and Evidence

- Changed lines: <inspected> / <total>, from the changed-line manifest or an equivalent ledger
- Deletions, renames, generated artifacts, mode, or binary changes: <each one and its disposition>
- Cross-tool handoffs reviewed: <each boundary and the result>
- Existing-environment evidence: <what proves behavior against current state, or "None">
- Missing or non-authoritative evidence: <each item; skips stay skips>
- Checks: <one line per check: name, command, tool version, result (pass, fail, skip, not applicable)>

## Findings Summary

`Critical: X · High: X · Medium: X · Low: X · Evidence gaps: X`

## Findings

One block per root cause, most severe first. Every field is required.

```text
Finding ID: F-01
Severity: <Critical | High | Medium | Low>
Confidence: <High | Medium>   (Low-confidence concerns go to Evidence Gaps)
File: <repository-relative path>
Location: <narrowest changed line or range, new-file numbering; for a deletion, the nearest changed line and the removed control>
Technology: <the parser, engine or runtime that interprets the line>
Category: <universal gate name, such as Target and identity, Lifecycle and destructive impact, Security and secrets>
Title: <imperative correction>
Execution path or trigger: <inputs, event or environment that makes it fail>
Description: <the exact defect>
Impact: <effect on security, correctness, state, reliability, availability, recovery or cost>
Remediation direction: <what must change, without prescribing an unnecessarily narrow implementation>
Verify with: <the artifact or check that will show the fix works>
```

## Evidence Gaps

One entry per material gap:

```text
[<Severity> evidence gap] <imperative title>
Artifact: <plan, what-if, render, check-mode diff, log, test>
Commit: <head SHA it must be generated from>
Inputs, target, identity: <parameter set, environment, scope, identity>
Risk it resolves: <what cannot be cleared without it>
```

Do not phrase a gap as a confirmed defect.

## Residual Risk

Material risk that remains after the reviewed evidence. With no actionable finding, use the no-finding statement: "No actionable defects found in the reviewed diff. Residual risk: <the specific dependency that remains>."

## Disposition

Exactly one of:

- Ready for human approval
- Ready with conditions
- Changes requested
- Blocked by a human or external decision
- Insufficient evidence for a safe recommendation

The disposition is advice to a human approver. It does not approve, block or satisfy a required review.

## Handoff

Fill this section from `templates/handoff.md`.

- Required corrections:
- Suggested work order:
- Validation required after fixes:
- Human decisions or approvals:
- Configuration and operational dependencies:
