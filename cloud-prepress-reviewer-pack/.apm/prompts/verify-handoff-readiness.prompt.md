---
description: "Verify that the next actor can safely continue: roles, authority, ownership, required inputs, documentation and explicit next action"
agent: cloud-prepress-reviewer
---

# Verify handoff readiness

## Inputs

- The work being handed over: a pre-press report, a change awaiting a pull request approver, or a change awaiting a deployment operator.
- The intended next actor and the approval gate they sit behind.
- If the change itself defines agent roles, tool permissions or automation, those definitions.
- The repository's documentation contracts: where it keeps setup (`README.md`), released work (`CHANGELOG.md`), human-only blockers (`REVIEW.md`), engineering work (`TODO.md`), required inputs and secret references (`CHECKLIST.md`), and ADRs.

## Workflow

1. Apply role-authority-and-handoff-review to check that each agent or workflow has the right role, tools and authorization boundary, and to detect role drift where a reviewer could silently implement, deploy, publish or change policy. Verify the handoff inputs: changed-file list, requirements, architecture or ADR, environment, preview or test evidence, findings, unresolved risks, required inputs, rollback, owner and explicit next action. Do not claim that the implementer or deployment operator completed work they have not reported.
2. Apply documentation-inputs-and-repository-contracts to check that each item lives in the artifact the repository uses for it, that new inputs appear by name and secret reference only, and that no credential, real variable value, state file, saved plan or private identifier was added to documentation.
3. Apply review-report-and-pr-gate to write or update the engineer handoff.

A missing owner, approval, credential owner, architecture decision or required input is a human blocker. Actionable engineering remediation belongs in work items, not hidden in a human-only section.

## Expected output

A pre-press report, or an updated engineer handoff when a report already exists, that names the next actor, the approval gate, the explicit next action, the evidence the next actor receives, each human blocker with its owner, and each engineering work item. If a handoff input is missing and nothing else is wrong, recommend `BLOCKED_ON_HUMAN_DECISION` when a person must supply it and `NOT_VERIFIED` when evidence is what is missing.

Follow the `cloud-prepress-reviewer-contract` instruction. Never describe an unexecuted check as passed.
