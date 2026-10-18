---
description: "Validate Ansible content with layered lint, syntax, inventory, check/diff and test evidence"
agent: ansible-expert-engineer
---

# Validate Ansible content

## Inputs

- The repository paths in scope and their entrypoint playbooks.
- Inventories, declared `requirements.yml`, and CI configuration.
- Which targets are approved for check mode: localhost, a fixture, or a named disposable host.
- Whether remediation is authorized, or the request is report-only.

Detect the repository shape before running anything. Do not run commands that need real hosts unless the target and risk are explicitly approved.

## Workflow

1. Apply `ansible-validate-content` in order: confirm controller runtime and dependency inputs without exposing secrets; resolve declared collections in an isolated path without broadening requirements; run `ansible-lint`; run `ansible-playbook --syntax-check` for each entrypoint.
2. Inspect inventory with `ansible-inventory --graph`, `--list` and `--host` for representative hosts, then selection with `--list-hosts`, `--list-tasks`, tags, limits and delegation.
3. Run `--check --diff` only against an approved target, and mark every module that does not fully support check or diff mode.
4. For reusable roles and collections, apply `ansible-role-collection-engineering` for Molecule scenarios and `ansible-test`.
5. Remediate the high-signal rules when authorized: FQCNs, modules instead of command/shell, idempotency boundaries, quoted file modes, `no_log` and `diff: false` on secret tasks, no unjustified `latest`. Use narrow, justified lint exceptions only.
6. For CI, check that the controller Python is pinned, collections are installed before lint, supported core ranges are exercised, and apply steps sit behind protected approvals.

## Expected output

An evidence ledger with one row per layer: command, where it ran (local, fixture, approved host), result (passed, failed, skipped, not run) and the evidence. Then located findings with remediation, changes made if authorized, and the check/diff limitations that remain. Unavailable tools and target-dependent checks are evidence gaps, not passes.

Follow the `ansible-expert-engineer-contract` instruction for the completion report.
