---
description: "Pre-press review of a built application or mixed change before the pull request is opened or approved"
agent: cloud-prepress-reviewer
---

# Review a built change before the pull request

## Inputs

- The repository and the exact change: base and head refs, a branch, a staged diff, or a supplied file list. A ticket, summary or agent claim is not the diff.
- The intended behavior, acceptance criteria, and any architecture brief or ADR the change implements.
- Evidence already produced: test, lint and build output, CI logs, generated artifacts.
- The authorization boundary. This review is read-only: it does not edit source, push, comment on, approve or merge the pull request.

Discover missing local facts from the repository before asking. Ask only for what cannot be found and would change the recommendation, such as the base ref or the acceptance criteria.

## Workflow

1. Apply cloud-prepress-orchestration to fix the target, baseline, intent and authorization boundary, and to select only the review domains this change needs.
2. Apply change-scope-and-impact to resolve the actual diff, classify each changed path, and record why any path outside the diff was inspected.
3. Apply code-defect-and-quality-review to trace normal and failure paths through the changed code. Label anything the evidence cannot prove as a validation hypothesis.
4. Apply tests-build-and-dependency-review to map changed behavior to tests and to check build, lock-file and dependency evidence. Run only local, non-mutating checks the repository already defines, and record every skipped check with its reason.
5. Apply security-secrets-and-supply-chain-review when the change touches external input, identity, secrets, logging, shell or network calls, dependencies or CI.
6. Apply documentation-inputs-and-repository-contracts only for documentation the change makes necessary.
7. If the change also touches infrastructure, policy or identity, add iac-policy-and-identity-review and state in the handoff that deployment readiness needs a separate pre-deployment review.
8. Apply review-report-and-pr-gate to write the report. If the pack's pre-review and post-review helpers are available, apply review-hooks-and-automation around the review; otherwise record both helpers as skipped.

## Expected output

A pre-press report containing every section the contract requires: scope and inputs, changed paths and methods, an evidence ledger using the contract's evidence labels, located findings carrying all nine finding fields, skipped checks and limits, the architecture, security, tests and operations status sections, unresolved risks and human blockers, exactly one recommendation, and the engineer handoff. A clean static review ends at `READY_FOR_PR`, which is not deployment approval.

Follow the `cloud-prepress-reviewer-contract` instruction. Never describe an unexecuted check as passed.
