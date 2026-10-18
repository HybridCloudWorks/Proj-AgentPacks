# Engineer handoff: <change title>

Use this when the handoff travels separately from the pre-press report, for example into a pull request description, a work item, or a message to the deployment operator. It carries the inputs that role-authority-and-handoff-review requires the next actor to have. When the handoff is the last section of `REVIEW.md`, use that section instead and refer to findings by severity and subject, not by ID.

## Who acts next

| Item | Value |
|---|---|
| Next actor | <implementer, pull request approver, deployment operator, decision owner> |
| Approval gate they sit behind | <pull request review, environment approval, change advisory, ADR acceptance> |
| Pre-press recommendation | <the one recommendation from the report> |
| Report | <path to REVIEW.md> |

## What the next actor receives

| Input | Where it is | Evidence label |
|---|---|---|
| Changed-file list | <report section, or diff ref> | observed |
| Requirements and acceptance criteria | <link or path> | <label> |
| Architecture and ADR | <ADR IDs and status> | <label> |
| Environment and scope | <environment, subscription, region, scope> | <label> |
| Preview or test evidence | <CI run, capture file, command output> | <label> |
| Findings | <report section; IDs allowed here because this is a separate document> | observed |
| Unresolved risks | <list> | <label> |
| Required inputs | <names and secret references only> | <label> |
| Rollback | <rollback boundary and procedure location> | <designed, or rehearsal evidence> |
| Owner | <resource owner and change owner> | <label> |

## Actions

Engineering work goes to the work tracker the repository uses (for example `TODO.md` or work items). Human-only blockers go to the human review record (for example `REVIEW.md`). Do not mix them.

| Action | Type | Owner | Done when |
|---|---|---|---|
| <fix or decision> | <engineering work or human blocker> | <person or role> | <verification step from the finding, or decision recorded> |

## Boundaries

- This review did not: <implement fixes, deploy, merge, publish, run live queries, rotate credentials>.
- The next actor must not assume: <for example, that a preview proves deployment success, or that static review proves live policy compliance>.
- Return to pre-press review when: <new commits to reviewed paths, a new preview, a changed ADR, a changed target scope>.
