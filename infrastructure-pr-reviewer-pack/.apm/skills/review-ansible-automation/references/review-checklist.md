# Ansible Review Adapter

Apply this adapter to playbooks, roles, collections, inventories, group and host variables, templates, handlers, plugins, vault integration, and pipelines that run Ansible.

## 1. Entry points and target selection

Identify:

- Playbook entry points and imported or included playbooks, roles, and tasks.
- Inventory sources, groups, host patterns, dynamic inventory, and environment overlays.
- `--limit`, tags, skip-tags, extra vars, check mode, diff mode, forks, and strategy settings used by CI.
- Connection user, `become` behavior, delegated hosts, local actions, and controller identity.
- Collections and roles required at runtime.

Verify that the host pattern and inventory cannot silently select the wrong environment. Review empty-group and unmatched-host behavior rather than assuming a failure.

## 2. Variable sources and precedence

Trace changed values through:

- Role defaults and vars.
- Inventory, group vars, host vars, play vars, task vars, facts, registered values, include vars, environment lookups, and extra vars.
- Vault files and external secret stores.
- Jinja defaults, omitted values, filters, and type conversions.

Verify:

- The intended source wins under Ansible precedence.
- Required variables fail early with `assert` or equivalent validation.
- Undefined, null, empty, false, zero, scalar, and list values behave intentionally.
- Boolean-like strings are not treated as booleans accidentally.
- Secrets are not exposed through debug, diff, failure messages, facts, or artifacts.

## 3. Idempotency and change reporting

Prefer idempotent modules over `command`, `shell`, `raw`, or custom scripts when an appropriate module exists and the behavior matters.

When imperative commands are justified, verify:

- `creates`, `removes`, current-state checks, or equivalent guards.
- Accurate `changed_when` and `failed_when` conditions.
- Correct exit-code handling.
- Safe quoting and shell selection.
- Re-run behavior after partial failure.

Review whether a second run reports no unintended changes. Incorrect `changed` status can trigger handlers, hide drift, or make deployment evidence unreliable.

## 4. Tasks, conditions, loops, and includes

Verify:

- `when` conditions handle undefined and false values correctly.
- Registered results are available on every branch and host where consumed.
- Loops preserve stable item identity and do not create duplicate or multiplicative changes.
- `include_*` versus `import_*` behavior matches the desired parse-time or runtime semantics.
- Tags propagate as intended through includes and roles.
- `run_once`, `delegate_to`, `delegate_facts`, `local_action`, and `bypass_host_loop` target the correct host and variable context.
- Blocks, rescue, and always sections preserve the original failure and do not perform destructive cleanup incorrectly.

## 5. Handlers and service lifecycle

Verify:

- Tasks notify the correct handlers only when a real change occurs.
- Handler names or listen topics remain compatible across roles.
- Handler ordering, deduplication, and flush points match operational needs.
- A failed play does not skip a required safety action or restart unexpectedly.
- Restarts, reloads, drains, and health checks preserve availability.
- Configuration validation happens before a handler restarts a service.

## 6. Failure, rollout, and blast radius

Review:

- `ignore_errors`, `failed_when`, `any_errors_fatal`, `max_fail_percentage`, `serial`, `throttle`, strategy, retries, delay, and `until`.
- Whether ignored or rescued failures still leave hosts in a safe and observable state.
- Whether rolling batches retain enough healthy capacity.
- Whether failure on one host should stop other hosts.
- Whether retries repeat non-idempotent actions.
- Whether unreachable hosts are distinguished from task failures.
- Whether cancellation or controller failure leaves locks, maintenance mode, drained nodes, or partial configuration.

Broad `ignore_errors: true` is a high-scrutiny signal because it can hide real failures. Review the exact acceptable failure condition instead.

## 7. Check mode and diff mode

Use check and diff evidence carefully:

- Modules vary in check-mode and diff-mode support.
- Tasks with `check_mode: false` can still make changes during a check run.
- Registered values from skipped check-mode tasks can alter later conditions.
- Diff output can expose secrets or sensitive configuration.
- Commands and external scripts may not model changes accurately.

A clean check-mode run is not proof of idempotency or production safety. Use a limited disposable target and follow with a second real test run when risk permits.

## 8. Files, templates, permissions, and secrets

Verify:

- File owner, group, mode, SELinux context, ACL, and atomic-write behavior.
- Numeric-looking modes are represented safely.
- Templates render valid configuration for all environments.
- Validation commands run before replacement when supported.
- Temporary files and backups do not expose secrets.
- `no_log` is applied narrowly to sensitive tasks; it must not hide all evidence for unrelated failures.
- Vault passwords and decrypted values never enter logs, diffs, facts, caches, or committed files.

## 9. Privilege and command safety

Verify:

- `become` is limited to tasks that require it.
- The intended become user and method are explicit where ambiguity is dangerous.
- Shell commands avoid injection from variables and use `argv` or native modules where possible.
- Environment variables, PATH, working directory, and executable are controlled.
- Downloads and package repositories are trusted and version constrained.
- Host-key or TLS verification is not disabled without a compensating control.

## 10. Collections, roles, and dependencies

Verify:

- Fully qualified collection names are used where ambiguity or shadowing matters.
- Collection and role versions are intentionally constrained.
- `requirements.yml` changes match the code change.
- Mutable branches or unpinned sources are not used for production-critical automation.
- Custom plugins, filters, modules, and callbacks are reviewed as executable code.
- The CI environment installs the same dependencies used by validation and execution.

## 11. Validation evidence

Use, when safe and available:

```text
ansible-lint --offline
ansible-playbook <playbook> --syntax-check
ansible-playbook <playbook> --check --diff --limit <safe-target>
```

Cautions:

- Syntax checks may require inventories, variables, roles, and collections.
- Check mode is a simulation and can be incomplete.
- Diff mode can reveal sensitive data.
- Do not automatically run check mode against real targets during review.
- Molecule or integration tests can create or modify infrastructure; use disposable environments.
