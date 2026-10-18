---
description: "Re-review an infrastructure pull request after a new push, verifying earlier findings against the new head"
agent: infrastructure-pr-reviewer
---

# Re-review an infrastructure pull request after a new push

## Inputs

- The new head revision, the head revision of the previous review, and the base revision.
- The previous review's findings and evidence gaps, by Finding ID, with their file and location anchors.
- Author replies and any new or regenerated plans, what-if results, rendered output, test results or CI logs.

Resolved conversations, author replies and a green pipeline are claims, not proof that a finding is fixed.

## Workflow

1. Apply the `review-infrastructure-pr` Skill's Re-review rules. Rebuild the changed-line ledger against the new head with `scripts/change_manifest.py`, covering the full PR diff, not only the latest commit.
2. For each earlier finding, read the code at the new head and classify it as fixed, partially fixed, not fixed or superseded. Cite the line or artifact that establishes the status.
3. Review every line that changed since the previous review with the technology Skills that match it, and re-check cross-tool handoffs that the fix touches.
4. Apply `verify-infrastructure-evidence` to regenerated artifacts. Earlier evidence no longer counts once the commit, inputs, target or dependency set has changed.
5. Do not repeat a finding whose root cause is fixed. Raise a new finding only for a new root cause that meets the finding threshold.

Stay read-only. Do not resolve conversations, post comments or change review state on the pull request unless the user explicitly authorizes that write.

## Expected output

The full review report in the structure of the `review-infrastructure-pr` Skill's `assets/review-report-template.md`. In Coverage and Evidence, list each earlier Finding ID with its status at the new head and the evidence for it. Findings contains only open and new root causes. Disposition reflects the new head alone.

Follow the `infrastructure-pr-reviewer-contract` instruction. Never describe an unexecuted check as passed.
