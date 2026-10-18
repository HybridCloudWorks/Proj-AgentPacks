# Review handoff

The Handoff section that closes every review report (`.apm/skills/review-infrastructure-pr/assets/review-report-template.md`). It tells the PR author what to fix and in what order, and tells the human approver what they still have to decide. The reviewer stays read-only, so everything here is work for someone else.

## Required corrections

One line per open finding, most severe first:

- F-nn (<Severity>): <the correction, in one sentence> — <path>:<line>

## Suggested work order

Order by dependency, not only by severity. Fix target and identity selection before anything that runs under that identity; fix state or ownership migration before regenerating plans; regenerate evidence last.

1.
2.

## Validation required after fixes

For each correction, the evidence that will show it works, generated from the new head:

| Finding | Evidence required | Commit, inputs, target and identity it must use |
|---|---|---|
| | | |

Include a second-run idempotence check, an existing-state plan or a what-if when the change depends on current state.

## Human decisions or approvals

Decisions the reviewer cannot make: accepting a destructive action, a cost increase, a maintenance window, an exception to policy, or ownership of a new failure mode. Name who is expected to decide when the repository shows it, for example through CODEOWNERS.

## Configuration and operational dependencies

Controls the review relied on but could not see, checked against `.apm/skills/review-infrastructure-pr/assets/repository-enforcement-checklist.md`:

- [ ] Protected environment and accountable approval for <environment>
- [ ] Required checks that run on the reviewed files
- [ ] State, target and pipeline concurrency controls
- [ ] Deployment consumes the reviewed immutable artifact
- [ ] Re-review on new pushes

Runbook, monitoring or ownership updates that the change makes necessary.
