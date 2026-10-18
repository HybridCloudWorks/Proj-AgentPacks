# Google Cloud architecture completion report

A machine-readable report is a JSON object whose keys are the field names listed in `tests/report-contract.yml`; run `tooling/completion_contract.py --report <file>` to check one.

- Status: one of COMPLETE_VERIFIED, DESIGN_READY_FOR_REVIEW, PREPARED_NOT_VERIFIED, ANALYSIS_ONLY, CHANGES_REQUIRED, BLOCKED_ON_HUMAN_DECISION.
- Outcome: one or two sentences. For PREPARED_NOT_VERIFIED include exactly: "The design is prepared, but completion is not verified."
- Acceptance criteria: each with an ID, a status of passed, failed or unverified, and the evidence.
- Deliverables: files produced or changed.
- Decisions: each decision record with ID, title and status (Proposed, Accepted, Superseded, Rejected).
- Assumptions.
- Security posture, reliability posture, cost estimate (basis and confidence), sustainability impact, operational impact, performance impact, compliance and residency.
- Cloud changes: normally none. Each entry needs target, action and the approval that covered it.
- Checks: command, target, exit code, status and evidence. A check that did not run is unverified, never passed.
- Unverified items, remaining risks, rollback, follow-ups.

Rules: COMPLETE_VERIFIED needs every criterion and check passed, nothing unverified and no Proposed decision. DESIGN_READY_FOR_REVIEW needs no failed criterion or check and a named decision owner. A plan, a static check or an estimate never proves live behaviour.
