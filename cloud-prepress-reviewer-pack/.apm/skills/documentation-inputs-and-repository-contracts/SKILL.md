---
name: documentation-inputs-and-repository-contracts
description: Reviews whether changed behavior, inputs, secrets references, runbooks, ADRs, review records, checklists, and repository contracts are documented in the correct artifact.
---

# Documentation, Inputs, and Repository Contracts

Check only documentation impact caused by the change. Keep repository purpose and setup in `README.md`; released work in `CHANGELOG.md`; human-only blockers in `REVIEW.md`; actionable engineering work in `TODO.md`; required inputs and secret references without values in `CHECKLIST.md`; architecture decisions in ADRs; and deployment evidence in the plan or review report.

For infrastructure changes, verify resources, environments, stateful impact, expected destroy/create, cost ceiling, new inputs for `REVIEW.md` Part 4, validation evidence, rollback, acceptance criteria, and required approvals. Missing documentation is a finding only when it changes safe implementation, operation, approval, or recovery.

Never add credentials, real variable values, state files, saved plans, private identifiers, or sensitive evidence to documentation.
