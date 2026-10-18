# Rollout plan

Produced by the `ansible-execution-control` skill, with selection proof from `ansible-inventory-and-variable-design`. Every section is required; write "not applicable" with a reason rather than deleting one.

## Change

- What changes on each host:
- Playbook and commit:
- Run type: dry / disposable / staged / production
- Change window:

## Host-selection proof

| Item | Value | Evidence |
|---|---|---|
| Inventory source | | static file or plugin; freshness if dynamic |
| Host pattern | | play `hosts:` value |
| `--limit` and tags | | |
| Selected hosts | count and names | `--list-hosts` output |
| Delegation targets | | `ansible-inventory --graph <group>` |
| Privilege | | `become` scope |

## Batching and strategy

- `serial`:
- Resulting batches (sizes in order):
- Capacity constraint this satisfies:
- `max_fail_percentage` or `any_errors_fatal`, and what happens when a batch fails:
- Strategy (`linear` unless independent host progress is safe), and why:

## Concurrency controls

- `forks`:
- `throttle` on specific tasks:
- `run_once` tasks: note that `run_once` runs once per batch under `serial`; move once-per-rollout work to its own play.
- `delegate_to` tasks, and whether any can race or repeat a control-plane mutation:
- `delegate_facts`:

## Handlers and failure behavior

- Handlers notified, and the section boundary where they flush:
- `force_handlers` or `meta: flush_handlers`, only if a dependent step needs it:
- `ignore_errors` or `ignore_unreachable`, if any, with the recovery contract that justifies it:
- State a failed host is left in (for example, drained and out of service):

## External state

Locks, rate limits, package managers, shared files, APIs, load balancers and database migrations the run touches, with bounded retries for each.

## Async work

Timeout, polling, retry, cleanup, and whether the remote operation can outlive the playbook. "Not applicable" if there is none.

## Recovery

- Rollback or forward-recovery steps:
- Evidence that recovery worked:
- Steps with no defensible rollback:

## Validation

| Step | Command | Target | Kind | Result |
|---|---|---|---|---|
| Syntax | | local | structural | |
| Selection | | local | structural | |
| Dry run | | | dry run | |
| Non-production run | | | real execution | |

What check mode cannot model in this plan: delegated calls, handlers, remote side effects, modules without check-mode support.

## Approval and handoff

Who approves the production run, and the operator handoff that carries the exact commands and stop conditions.
