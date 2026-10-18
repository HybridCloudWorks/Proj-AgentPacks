---
description: "Review an infrastructure or automation pull request end to end and return line-anchored findings, evidence gaps and a disposition"
agent: infrastructure-pr-reviewer
---

# Review an infrastructure pull request

## Inputs

- The pull request, branch or diff to review, with base and head revisions. Resolve them from the repository when the user gives only a PR number or branch name.
- PR title, description, linked issue and acceptance criteria. Treat them as claims to verify.
- Any attached plans, what-if results, compiled or rendered output, test, policy or scan results, and CI logs.
- Repository and path-specific instructions, module or role documentation and runbooks that the repository already contains.

Do not invent targets, identities, state, inventories or organizational policy. Record what is unavailable.

## Workflow

1. Apply the `review-infrastructure-pr` Skill. Inventory every changed technology, file, rename, deletion, generated artifact, mode and binary change.
2. Build changed-line coverage with that Skill's `scripts/change_manifest.py --base <base> --head <head> --format markdown` when Git refs are available; otherwise build the same ledger from the full diff.
3. State the change contract, then trace inputs, targets, identities, ownership and execution order across tools as that Skill's `references/review-protocol.md` describes.
4. Evaluate the universal gates in `references/universal-gates.md`.
5. Activate only the technology Skills the routing table names for the changed stack: `review-terraform-opentofu`, `review-bicep-arm`, `review-powershell-automation`, `review-ansible-automation`, `review-cicd-deployment`, `review-kubernetes-packaging`. Activate all that apply to a cross-tool chain.
6. Activate `verify-infrastructure-evidence` when safe local checks can run or review artifacts are attached. Never apply, deploy, destroy, run target-side configuration or execute untrusted workflow code.
7. Run the adversarial pass, merge findings by root cause, separate confirmed defects from evidence gaps, and stop with insufficient evidence when a stop condition in `review-infrastructure-pr` applies.

Stay read-only. Do not edit files, post comments, approve or request changes on the pull request unless the user explicitly authorizes that write.

## Expected output

The review report in the structure of the `review-infrastructure-pr` Skill's `assets/review-report-template.md`: Executive Summary, Review Scope, Coverage and Evidence (changed lines inspected out of total), Findings Summary, Findings with every required field, Evidence Gaps, Residual Risk, Disposition and Handoff. Use the no-finding language from `references/severity-and-output.md` when nothing meets the finding threshold.

Follow the `infrastructure-pr-reviewer-contract` instruction for severities, finding fields and dispositions. Never describe an unexecuted check as passed, and never imply that the review approves or blocks the merge.
