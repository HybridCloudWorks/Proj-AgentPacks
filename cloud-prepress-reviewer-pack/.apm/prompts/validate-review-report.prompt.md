---
description: "Run the non-mutating pre-review inventory, then validate the finished pre-press report before it goes to the pull request owner"
agent: cloud-prepress-reviewer
---

# Inventory the change and validate the review report

## Inputs

- The repository under review.
- The location of the finished or draft report (`REVIEW.md`), outside the source tree unless the user names another place.
- Whether the pack's pre-review and post-review helpers are available on this machine.

## Workflow

1. Apply review-hooks-and-automation. Before analysis, run the pre-review inventory. It is read-only and reports changed paths, path classifications, likely sensitive files and the local tools available. Compare its changed-file list with the actual diff and record any difference: the inventory compares the working tree with `HEAD`, so committed branch changes need the base comparison from change-scope-and-impact.
2. After the report is written, run the post-review validation. When it fails, correct the report text and run it again. Never edit the validator, its thresholds or its path exclusions to make the gate pass.
3. Apply review-report-and-pr-gate to check what the validator does not: every contract section is present, every finding carries all nine fields, findings are ranked by severity, evidence carries the contract's labels, skipped checks are listed, and the report ends with exactly one recommendation.
4. If a helper is unavailable or fails to run, record it as skipped with the reason. A skipped helper is not a pass.

## Expected output

The validator's result line, quoted exactly, and a list of the corrections made to the report. The report itself states the inventory result and any difference from the actual diff, and lists each helper that was skipped. The helpers are advisory: a passing validation proves the report's shape, not the change's safety, and it does not move the recommendation.

Follow the `cloud-prepress-reviewer-contract` instruction. Never describe an unexecuted check as passed.
