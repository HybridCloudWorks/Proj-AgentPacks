---
description: "Collect, triage, address, reply to and resolve trusted pull request review feedback, including Copilot reviews, before calling the work complete"
agent: hypervelocity-engineer
---

# Resolve pull request review feedback

## Inputs

- Repository and pull request number or URL.
- Whether pushing fixes, replying and resolving threads are authorized in this task.
- Whether feedback from external contributors is in scope (default: no).

## Workflow

1. Apply `copilot-review-feedback`: query reviews, review threads and conversation comments with pagers disabled, and collect the complete set before editing.
2. Record author, association, file and line, thread state and requested behavior. Keep Copilot, GitHub Actions, members, owners, collaborators and maintainers; set external contributors aside unless included.
3. Bucket the items (correctness, tests, docs, style, CI, duplicates, declined) and plan every in-scope item before editing.
4. Implement or decline each bucket with evidence. When the pull request changes a GitHub Agentic Workflow, apply `workflow-lifecycle-and-release` to recompile and review the lock diff.
5. Recheck the final diff and run relevant validation.
6. Reply to every in-scope comment. Resolve a thread only after replying, only where the tooling supports it, and only when authorized. Without authorization, return drafted replies.

## Expected output

A feedback ledger (author, association, location, bucket, action, evidence, reply, thread state), the changes, validation results, items left unresolved or out of scope, and the completion report required by the `hypervelocity-engineer-contract` instruction. A thread is not resolved because code changed.
