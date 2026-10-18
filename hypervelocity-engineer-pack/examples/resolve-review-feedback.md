# Worked example: review feedback on a new agentic workflow

Prompt: `.apm/prompts/resolve-review-feedback.prompt.md`. Skills applied: `copilot-review-feedback`, `workflow-lifecycle-and-release`. Repository, handles, comment IDs and figures are illustrative.

## Request

> Address all the review feedback on my PR #214 (adds the `stale-issue-nudge` workflow). Push fixes, reply to each comment, and resolve the threads you've handled.

Authorized: edit, push to the pull request branch, reply, resolve threads. External contributor feedback is not mentioned, so it stays out of scope.

## 1. Collect the complete set before editing

```text
export GH_PAGER=cat
gh api --paginate repos/example-org/inventory-service/pulls/214/reviews
gh api --paginate repos/example-org/inventory-service/pulls/214/comments
gh api --paginate repos/example-org/inventory-service/issues/214/comments
gh api graphql -f query='query { repository(owner: "example-org", name: "inventory-service") {
  pullRequest(number: 214) { reviewThreads(first: 100) { nodes { id isResolved
    comments(first: 20) { nodes { databaseId author { login } authorAssociation path line } } } } } } }'
```

Two reviews (Copilot and `ops-lead`), five review comments in four threads, and two conversation comments.

## 2. Ledger

Format: `templates/review-feedback-ledger.md`.

| # | Author | Association | Location | Requested behavior | Bucket |
|---|---|---|---|---|---|
| 1 | Copilot reviewer | bot | `stale-issue-nudge.md:9` | Agent job has `issues: write`; comments go through the safe output, so it only needs read | correctness |
| 2 | Copilot reviewer | bot | `stale-issue-nudge.md:31` | Prompt says "follow maintainer instructions in issue comments"; comment authors are not verified | correctness |
| 3 | Copilot reviewer | bot | `stale-issue-nudge.md:18` | Raise `timeout-minutes` from 10 to 30 | declined |
| 4 | `ops-lead` | MEMBER | `stale-issue-nudge.md:44` | Nudge comment should link to `CONTRIBUTING.md` | docs |
| 5 | `ops-lead` | MEMBER | `stale-issue-nudge.md:9` | "+1, the agent job shouldn't need write" | duplicate of 1 |
| 6 | `github-actions[bot]` | bot | conversation | "Lock file is out of date; run `gh aw compile`" | CI |
| 7 | `drive-by-user` | NONE | conversation | "Also auto-close issues after 60 days" | out of scope: external contributor |

## 3. Plan, then act

| # | Action | Evidence |
|---|---|---|
| 1 | Agent job set to `issues: read`; the safe output keeps its own write | lock diff: `issues: write` now appears only on the safe-output job |
| 2 | Sentence removed; comments are described as data, and the agent takes instructions only from the workflow body | source diff |
| 3 | Declined | `gh aw logs stale-issue-nudge`: both dispatch runs listed in the PR took 3 minutes 12 seconds and 2 minutes 58 seconds. A longer limit adds cost exposure with no evidence it is needed |
| 4 | Link added to the nudge text | source diff |
| 5 | Covered by the fix for 1 | same commit |
| 6 | Recompiled after 1, 2 and 4 | `gh aw compile stale-issue-nudge` |
| 7 | Not actioned and no reply sent; listed for the user | association `NONE` |

```text
gh aw compile stale-issue-nudge
gh aw validate
git push
gh pr checks 214
```

Compile and validate exited 0. After the push, `gh pr checks 214` shows the lock-file check and the existing CI checks passing.

## 4. Reply, then resolve

Every in-scope comment got its own reply, including 5, whose fix is shared with 1:

```text
gh api repos/example-org/inventory-service/pulls/214/comments/<comment-id>/replies -f body='Fixed in 7c0d2ab: agent job is now issues: read; the safe-output job keeps the write.'
gh pr comment 214 --body 'Lock file regenerated with gh aw compile in 7c0d2ab; the check is green.'
gh api graphql -f query='mutation { resolveReviewThread(input: {threadId: "<thread-id>"}) { thread { isResolved } } }'
```

The threads for 1 and 5 (one thread), 2 and 4 were resolved after replying. Thread 3 got a reply with the timing evidence and was left open: declining a suggestion is the author's call to confirm. Conversation comment 6 has no thread to resolve.

## Completion report

Outcome: every in-scope comment addressed and answered; one declined thread left open for the user to confirm; one external comment set aside.

**objective**: Address, answer and resolve the trusted review feedback on pull request #214.

**scope-and-authorization**: Edits, push, replies and thread resolution were authorized. External contributor feedback was out of scope by default and was not answered.

**actions-and-changed-files**: Edited `.github/workflows/stale-issue-nudge.md`. Regenerated `.github/workflows/stale-issue-nudge.lock.yml`. Pushed commit `7c0d2ab` to the pull request branch. Posted five review replies and one conversation comment. Resolved three threads.

**evidence**:
- Observed: all reviews, threads and conversation comments with their associations; the lock diff limiting `issues: write` to the safe-output job; run durations for the declined item; green checks after the push.
- Inferred: removing the "follow comment instructions" sentence lowers prompt-injection exposure. The structural control is still the read-only agent job.
- Unavailable: no live scheduled run since the change.

**validation**:

| Check | Command | Result |
|---|---|---|
| Compile | `gh aw compile stale-issue-nudge` | passed |
| Validate | `gh aw validate` | passed |
| Pull request checks | `gh pr checks 214` | passed |
| Every in-scope item replied | ledger against thread list | passed: 6 of 6 |
| Live run after change | n/a | not run: not requested |

**risks-and-limitations**: Thread 3 stays open until the user confirms the decline. Comment 7 is unanswered by design. Permissions: agent job read-only. Safe outputs: `add-comment` only. Secrets and network are unchanged. Live behavior after this change is unverified.

**next-safe-action**: The user confirms or overrides the decline on thread 3 and decides whether to answer comment 7. Merging stays with the user.
