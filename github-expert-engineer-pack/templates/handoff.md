# GitHub handoff template

Use this when the next step belongs to someone other than the agent: an organization owner, a repository admin, the security owner, a cloud identity owner, a release manager, or a maintainer who must authorize a live change. The pack has no specialist subagents, so handoffs go to people or teams. The agent keeps ownership of integrating the result and of the completion report.

## Goal and context

- Original request: <the user's words, shortened>
- Repository, organization and ref: <owner/repo, branch or tag, SHA>
- Reason for the handoff: <authority | access | ownership outside GitHub | decision or exception>
- Completion report this belongs to: <title and date>

## Facts already established

| Label | Fact | Source |
|---|---|---|
| CONFIRMED | <fact> | <command, endpoint or file:line> |
| INFERRED | <fact> | <basis> |

## Requested action

- Owner: <team or role, not a guessed individual>
- Exact change: <UI path and field, or API method and endpoint>
- Payload preview: <inline or a file name; redacted>
- Preconditions: <what must be true first>
- Change window: <approved window, or "to be agreed">
- Out of scope for this handoff: <what the owner should not change>

## Risk and rollback

- Blast radius: <repositories, users, workflows or environments affected>
- Rollback: <exact reversal, and how long it stays possible>
- Stop condition: <signal that means halt and roll back>

## Read-back and return

- Read-back after the change: <read-only command or UI check>
- Evidence to return: <fields, timestamps, run IDs>
- What happens next: <how the agent folds the evidence into the report and what it re-checks>

## Never included

Secret values, tokens, private keys, webhook secrets and session cookies are never written into a handoff. Name the secret and its owner instead.
