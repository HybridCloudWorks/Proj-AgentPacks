---
name: ansible-execution-control
description: Design or review Ansible rollout safety, host selection, serial batches, strategies, delegation, run_once, throttle, async work, handlers, failure policy, and blast-radius controls.
---

# Execution Control and Rollout Safety

Treat an Ansible invocation as a distributed change with identity, ordering, concurrency, and recovery semantics. Establish the exact host pattern, inventory source, `--limit`, tags, delegation targets, privilege, and whether the run is dry, disposable, staged, or production.

## Scope and batching

Use `--list-hosts` and `--list-tasks` before execution. For rolling changes, choose `serial` deliberately, define `max_fail_percentage` or `any_errors_fatal` where appropriate, and explain what happens when a batch fails. Do not assume `serial` protects delegated tasks or external APIs. Use `throttle` for task-level pressure and `forks`/strategy for controller concurrency.

`run_once` is once per play batch, not necessarily once for the entire inventory when `serial` is used. `delegate_to` changes where a task executes but does not automatically change variable ownership; use `delegate_facts` intentionally. Check that a delegated task cannot race or repeat a control-plane mutation.

## Strategies and async

Use the default linear strategy when cross-host ordering matters. Use `free` only when independent host progress is safe. For `async`/polling, define timeout, retry, failure, cleanup, and whether the remote operation can outlive the playbook. Do not use async to hide a long or unsafe operation.

## Handlers and failure

Handlers run at the end of a play by default and can be skipped after failure. Use `force_handlers` only when a changed configuration must be reconciled despite later failure and the host remains reachable. Use `meta: flush_handlers` only when an immediate dependent step requires it. Keep `ignore_errors` and `ignore_unreachable` narrow and explain the recovery contract; neither repairs an unsafe rollout.

## External state and recovery

Identify locks, rate limits, package managers, service restarts, shared files, APIs, and database migrations. Make retries bounded and safe. Define rollback or forward-recovery evidence before changing a destructive or irreversible step. Check mode may not model remote side effects, handlers, delegated calls, or modules that do not support it.

## Output

Return the host-selection proof, batch/strategy rationale, concurrency controls, failure behavior, recovery plan, and the exact safe validation command. Never present a single-host dry run as proof of a fleet rollout.

Reference: https://docs.ansible.com/projects/ansible/latest/playbook_guide/playbooks_execution.html
