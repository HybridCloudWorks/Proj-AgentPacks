---
description: "Bootstrap an Ansible project connection-first, validating one boundary at a time"
agent: ansible-expert-engineer
---

# Bootstrap an Ansible project

## Inputs

- Host names or count, OS families, and the environments to manage (lab, staging, production).
- SSH user and key method, or the approved alternative, and the sudo/become model per host group.
- Mandated collections, the secret source (Ansible Vault or an approved external provider), and the desired end state.
- Which hosts are disposable or explicitly approved for connectivity tests and dry runs.

Discover what the repository already holds before asking. Record any unanswered item as an assumption with a safe default; never invent production topology and never ask for passwords, keys or vault secrets in chat.

## Workflow

1. Apply `ansible-bootstrap-interactive`. First confirm that no other control plane (image pipeline, VM extension, policy-based guest configuration, Terraform provisioner) already owns guest configuration for these hosts.
2. Propose only the files the end state needs: `ansible.cfg`, `requirements.yml`, one inventory per environment, `group_vars`/`host_vars`, playbooks, roles and tests. Keep `host_key_checking` enabled.
3. Shape inventories and variable scopes with `ansible-inventory-and-variable-design`, pin collections with `ansible-collections-supply-chain`, and place secrets with `ansible-vault-secrets`.
4. Prove connectivity before behavior. Inspect the inventory locally, then, with approval, run `ansible.builtin.ping` against one approved host and a separate become `whoami` check. Classify each failure (inventory, DNS/network, SSH identity, host key, target Python, sudo policy) with `ansible-debug-runtime-failures` before writing playbook logic.
5. Add one behavior per increment and validate each with `ansible-validate-content`: lint, syntax check, inventory inspection, `--list-hosts`/`--list-tasks`, then `--check --diff` on a limited, approved target.

## Expected output

At the end of every phase: what is known, what passed, what was skipped, and the next safe action. At the end of the bootstrap: the created or proposed file tree, connectivity and become evidence per approved host, open assumptions, and any failure classification still unresolved. A real run and the second-run convergence check happen only after explicit authorization.

Follow the `ansible-expert-engineer-contract` instruction for the completion report: keep observed facts apart from inference, skipped checks apart from passed ones, local validation apart from remote proof, and dry runs apart from real execution.
