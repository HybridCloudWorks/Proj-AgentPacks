---
name: ansible-playbook-development
description: Create or review Ansible playbooks, roles, tasks, handlers, templates, inventories, and variables using FQCN modules, explicit contracts, idempotency, and current Ansible validation. Use when the task is authoring or changing reusable Ansible automation.
---

# Ansible Playbook Development

Model desired state, not a shell transcript. Start by identifying target OSes, inventory shape, controller and node Python versions, privilege boundaries, collections, secrets, and the user-visible acceptance test.

## Design rules

- Prefer the narrowest FQCN module over `command`, `shell`, or `raw`.
- Put user-tunable values in role defaults or documented inventory variables; reserve `vars/` for values that must not be overridden.
- Use native YAML booleans, numbers, lists, and mappings. Do not hide type conversion in string interpolation.
- Use `ansible_facts[...]` in new content. Avoid relying on injected top-level facts.
- Use handlers for service reload/restart and decide whether `force_handlers` is required when later failure must not suppress a safety-critical restart.
- Set explicit file ownership and quoted modes for managed files. Use `default(omit)` for optional module arguments.
- Prefer `block`/`rescue`/`always` for real recovery or cleanup, not as a blanket error suppressor.

## Expressions and idempotency

`when`, `failed_when`, `changed_when`, `until`, and `assert.that` are already Jinja expressions. Do not wrap their values in `{{ }}`. Make conditions evaluate to booleans and convert types explicitly.

Every task must converge. If a command is unavoidable, add `creates`/`removes` or a registered result with defensible `changed_when` and `failed_when`. Explain any intentional non-idempotence. The second controlled run is the acceptance test; a zero-change result is expected unless the task represents an intentionally changing operation.

## Minimum role contract

For a reusable role, provide `defaults/main.yml`, `tasks/main.yml`, `handlers/main.yml` when needed, templates/files, `meta/main.yml`, documentation, and `meta/argument_specs.yml` for supported inputs. Keep the role's public variables small and validate required values early with `assert` or argument specifications.

## Validation

Run the narrowest applicable set:

```text
ansible-lint .
ansible-playbook --syntax-check playbooks/site.yml
ansible-inventory -i inventories/staging/hosts.yml --list
ansible-playbook -i inventories/staging/hosts.yml playbooks/site.yml --list-hosts --list-tasks
ansible-playbook -i inventories/staging/hosts.yml playbooks/site.yml --check --diff --limit one_host
```

Run against a disposable or explicitly approved target only after the dry run and inspect the second run for convergence. Check mode and diff mode have module-specific limitations; state skipped or unverified behavior.

Refresh exact version behavior from the official Ansible release and porting guides before asserting compatibility: https://docs.ansible.com/projects/ansible/latest/reference_appendices/release_and_maintenance.html
