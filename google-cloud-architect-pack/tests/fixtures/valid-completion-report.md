# Completion-report fixture

The machine-readable form of this report is `valid-completion.json` in the same folder. In prose:

- Status: DESIGN_READY_FOR_REVIEW
- Outcome: a three-tier serverless design and its Terraform skeleton are prepared for the decision owner's review.
- Acceptance criteria: AC-1 passed (traceability matrix); AC-2 unverified (runtime ingress check written for the user, nothing deployed).
- Decisions: ADR-001 primary region, Proposed.
- Cloud changes: none.
- Checks: `terraform validate` on the local workspace, exit code 0, passed.
- Unverified: runtime ingress and WAF behaviour.

Invented test data for the report checker. Nothing here describes a real design, deployment or command run.
