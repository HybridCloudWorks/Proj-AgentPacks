# Approval handoff

Use when the next step is an operation the agent must not take on its own: apply, destroy, import, `state mv`, `state rm`, `state push`, force-unlock, backend migration, HCP Terraform permission or variable changes, policy enforcement changes, provider release, or any production work. The agent fills this in, hands it to the person who can authorize, and stops. One handoff covers one operation on one target.

## Operation

- Exact command or console action:
- Configuration directory:
- Why it is needed now:

## Target

| Item | Value |
|---|---|
| Environment | |
| Account, subscription or HCP organization and workspace | |
| Backend and state key | |
| Identity that will run it | |

## Inputs this approval is bound to

The approval lapses if any of these changes; the agent then plans again and issues a new handoff.

| Input | Value |
|---|---|
| Commit | |
| Saved plan file SHA-256, or HCP run ID | |
| Variable sources | |
| `.terraform.lock.hcl` SHA-256 | |
| Policy and run-task result | |

## Expected impact

- Plan counts (import, add, change, destroy, moved):
- Every replace and destroy, by address:
- Sensitive values involved, named by address only:
- Expected downtime or user impact:

## Preconditions checked

| Check | Result | Evidence class |
|---|---|---|
| State lock is free, or the holder and its run are identified | | |
| Backup or backend version history exists and is readable | | |
| Change window and on-call owner | | |
| For force-unlock only: lock ID, holder, run status, and why the lock is proven stale | | |

## Recovery

How to undo or contain the operation if it goes wrong, and who can do it. Write "none" if there is no recovery; that is itself a reason to reconsider.

## Not verified

What the agent could not check before asking.

## Approver's reply

- [ ] Approved as written, single use
- [ ] Approved with changes:
- [ ] Declined

Name, date, and any limit on time or scope.

## After execution

The agent records the result in the completion report: command, exit code, plan or apply summary, state serial before and after, and any deviation from this handoff.
