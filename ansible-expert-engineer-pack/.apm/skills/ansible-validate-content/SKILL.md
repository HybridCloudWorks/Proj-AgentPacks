---
name: ansible-validate-content
description: Validate Ansible playbooks, roles, collections, inventories, and CI with ansible-lint, syntax checks, inventory inspection, check/diff mode, idempotency evidence, and targeted tests. Use before execution or when remediating validation failures.
---

# Validate Ansible Content

Validation is layered evidence, not a single green command. Detect the repository shape first and do not run commands that require real hosts unless the user explicitly approves the target and risk.

## Order

1. Confirm controller/runtime and dependency inputs without exposing secrets.
2. Install or resolve declared collections in an isolated environment; do not silently broaden requirements.
3. Run `ansible-lint` and fix syntax/YAML errors before semantic warnings.
4. Run `ansible-playbook --syntax-check` for each entrypoint.
5. Inspect inventory with `ansible-inventory --graph`, `--list`, and `--host` for representative targets.
6. Inspect selection with `--list-hosts`, `--list-tasks`, tags, limits, and delegation.
7. Run `--check --diff` against localhost, a fixture, or an explicitly approved disposable host. Mark modules that do not fully support check/diff.
8. Run Molecule, `ansible-test`, or focused unit/integration checks for reusable content.
9. If an approved real run occurs, use a single host or batch first and run again to measure convergence.

## High-signal rules

- Replace short module names with FQCNs.
- Replace command/shell with a module where possible; otherwise add `creates`, `removes`, `changed_when`, and `failed_when`.
- Set explicit quoted file modes and protect secret tasks with `no_log: true` and often `diff: false`.
- Avoid `latest` unless continual upgrade is the stated contract.
- Do not disable broad lint rules to hide a defect; use a narrow, justified exception.
- Treat skipped checks, unavailable tools, and target-dependent checks as evidence gaps, not passes.

## CI

Pin the controller Python and dependency strategy in CI. Install the declared collections before lint. Exercise supported Ansible/core ranges where the project promises them. Include syntax, lint, role/collection tests, and secret scanning; keep deployment/apply steps behind protected approvals.

Reference: https://docs.ansible.com/projects/ansible-core/devel/playbook_guide/playbooks_intro.html and https://docs.ansible.com/projects/dev-tools/user-guide/testing/
