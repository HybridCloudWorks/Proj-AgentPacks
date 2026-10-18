---
description: "Identify the risk-proportional evidence an infrastructure pull request must attach before it can be reviewed safely, and draft the request"
agent: infrastructure-pr-reviewer
---

# Request review evidence

Use this workflow before or during a review when the pull request lacks the plans, previews, renders, tests or recovery details needed to clear its risk.

## Inputs

- The diff with base and head revisions, and the PR description.
- Evidence already attached, if any.
- The environments the change can reach, as far as the repository shows them.

## Workflow

1. Apply the `review-infrastructure-pr` Skill far enough to inventory technologies, targets, identities, lifecycle effects and execution order for every changed line.
2. Use the risk escalation and technology matrix in the `verify-infrastructure-evidence` Skill's `references/evidence-matrix.md` to decide which evidence each risk needs.
3. Map each need to a field of the `review-infrastructure-pr` Skill's `assets/infrastructure-pull-request-template.md`: change contract, targets and identity, lifecycle and ownership, validation evidence, failure and recovery, and security, availability and cost impact.
4. For each request, name the artifact, the commit it must be generated from, the inputs, target and identity it must use, and the risk it resolves.
5. Do not request evidence the diff does not need. Do not ask for production credentials or for the reviewer to generate target-specific evidence.

Stay read-only. Draft the request for the user to send; do not post it to the pull request unless the user explicitly authorizes that write.

## Expected output

The review report in the structure of the `review-infrastructure-pr` Skill's `assets/review-report-template.md`, with each requested artifact listed under Evidence Gaps and the drafted request under Handoff. Disposition is normally Insufficient evidence for a safe recommendation until the evidence arrives. Report any confirmed defect already visible in the diff as a finding.

Follow the `infrastructure-pr-reviewer-contract` instruction. Never describe an unexecuted check as passed.
