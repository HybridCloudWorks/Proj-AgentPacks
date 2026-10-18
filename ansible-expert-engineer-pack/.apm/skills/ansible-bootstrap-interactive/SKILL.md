---
name: ansible-bootstrap-interactive
description: Guide a connection-first Ansible project bootstrap or hands-on build by gathering hosts, OS, SSH, become, environment, collections, and secrets constraints before writing automation.
---

# Interactive Bootstrap

Use a staged conversation and validate one boundary at a time. Explain what a command will do before running it, ask before touching remote systems, and keep examples pointed at disposable or explicitly approved hosts.

## Gather first

Establish server count and names, OS families, SSH user/key or approved alternative, sudo/become model, environments, host groups, target Python, collections, secret sources, desired end state, and whether a different control plane already owns the work. If the user cannot answer, mark the assumption and choose a safe default rather than inventing production topology.

## Minimal shape

Propose only the files needed: `ansible.cfg`, `requirements.yml`, environment inventories, `group_vars`/`host_vars`, playbooks, roles, and tests. Keep `host_key_checking` enabled except for disposable labs with an explicit reason. Do not use the removed/deprecated `transport = smart` setting.

## Connectivity before behavior

Inspect the inventory and run a safe ping against an approved target. If privilege is needed, test `whoami` with become separately. Classify failures as inventory, DNS/network, SSH identity, host-key, target Python, or sudo policy before adding playbook logic.

## Incremental loop

Add one behavior at a time: facts or platform detection, packages, users, files/templates, handlers/services, and validation. After each increment run lint, syntax, inventory inspection, list-hosts/list-tasks, and check/diff on a limited target. A real run and second-run convergence require explicit authorization.

## Secrets

Use Vault or an approved external secret provider. Do not ask for passwords in chat. Suppress task output and diffs where secrets could appear.

End each phase with what is known, what passed, what was skipped, and the next safe action.
