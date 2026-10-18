---
description: "Plan or review a rolling Ansible change with host-selection proof, batching, failure policy and recovery"
agent: ansible-expert-engineer
---

# Plan a rolling change

## Inputs

- The change, the playbook that applies it, and the inventory source and host pattern.
- Whether the run is dry, disposable, staged or production, and the change window.
- Capacity that must stay in service, delegation targets (load balancers, APIs, monitoring), locks, rate limits and migrations involved.
- The acceptable failure threshold and the expected rollback or forward-recovery path.

The agent plans, validates and, with explicit approval, runs against non-production targets. It does not run against production without explicit authorization for that run.

## Workflow

1. Prove selection with `ansible-inventory-and-variable-design`: inventory graph for the play's groups and delegation targets, `--list-hosts`, `--list-tasks`, and the effect of `--limit` and tags.
2. Apply `ansible-execution-control`. Choose `serial` from the capacity constraint; set `max_fail_percentage` or `any_errors_fatal` and explain what happens when a batch fails.
3. Check concurrency: `forks` and strategy for the controller, `throttle` for task-level pressure, `run_once` (once per batch under `serial`), `delegate_to` and `delegate_facts`, and whether a delegated task can race or repeat a control-plane mutation.
4. Check handlers and failure: when handlers flush, whether `force_handlers` or `meta: flush_handlers` is genuinely needed, and how narrow any `ignore_errors` or `ignore_unreachable` is. Define bounded retries, async timeouts and cleanup.
5. Define recovery evidence before any destructive or irreversible step. Validate syntax and a dry run with `ansible-validate-content`, and record what check mode cannot model: delegated calls, handlers and remote side effects.

## Expected output

A rollout plan: host-selection proof, batch and strategy rationale, concurrency controls, failure behavior, recovery plan, and the exact safe validation command. When execution belongs to an authorized operator, add a handoff with the exact command, preconditions, stop conditions and the output to return. A single-host dry run is never presented as proof of a fleet rollout.

Follow the `ansible-expert-engineer-contract` instruction for the completion report.
