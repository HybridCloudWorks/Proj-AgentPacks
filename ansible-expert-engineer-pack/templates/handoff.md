# Operator handoff

Use this when the agent stops at an approval boundary and an authorized person must act: a production run, a secret rotation, a dependency installation into a shared environment, or the next phase of a bootstrap. The agent prepares and validates; the operator executes and returns the evidence. The agent remains responsible for integrating the returned evidence into the completion report.

## Goal and scope

- Goal:
- Repository and commit or branch:
- Playbook and entrypoint:
- Inventory source and environment:
- Out of scope:

## State at handoff

| Item | Status | Evidence |
|---|---|---|
| Lint and syntax | | |
| Selection proof (`--list-hosts`) | | host count and names |
| Dry run | | where it ran; modules not modelled by check mode |
| Non-production real run | | where it ran; second-run result |

## Authority required

- Action needing approval:
- Who can approve it:
- Change record or window, if the organization requires one:

## Preconditions

Each one must be true before starting; check it, do not assume it.

1.
2.

## Execution

The exact commands, in order, with secrets supplied out of band (for example `--vault-id env@prompt` or a runner-mounted file, never a password on the command line).

```text
ansible-playbook -i <inventory> <playbook> --list-hosts
ansible-playbook -i <inventory> <playbook> --limit <first batch or host>
```

## Stop conditions

Stop and do not continue to the next batch if any of these happen:

- A host fails or is unreachable.
- A health check does not pass within its retries.
- The recap shows changes on hosts that should not have been selected.

## Recovery

The rollback or forward-recovery steps for this change, and the evidence that the recovered state is correct. State plainly if no defensible rollback exists.

## Return to the agent

- The full `PLAY RECAP` for each run.
- Any failed task output, with secrets redacted.
- The second-run recap, if convergence is part of acceptance.
- Anything that differed from this handoff.

## Not verified by the agent

What remains unproven at handoff: for example production reachability, delegated calls not modelled by check mode, or behavior on hosts outside the dry-run sample.
