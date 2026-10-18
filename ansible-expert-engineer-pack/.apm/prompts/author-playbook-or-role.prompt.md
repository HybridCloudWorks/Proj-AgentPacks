---
description: "Create, change or review an Ansible playbook or role as idempotent, validated desired state"
agent: ansible-expert-engineer
---

# Author a playbook or role

## Inputs

- The desired end state and the user-visible acceptance test.
- Target OS families and versions, inventory shape and groups, controller and managed-node Python.
- Required collections, privilege boundaries, and any secrets the automation will consume.
- Whether the request is to create, change or review. A review-only request stays read-only and returns findings.

Read the existing playbooks, roles, inventories and `ansible.cfg` before proposing structure. Do not invent target hosts or credentials.

## Workflow

1. Apply `ansible-playbook-development`: model desired state, prefer the narrowest FQCN module over `command`, `shell` or `raw`, put user-tunable values in role defaults or documented inventory variables, use native YAML types and `ansible_facts[...]`, and use handlers for reloads and restarts.
2. Write `when`, `failed_when`, `changed_when`, `until` and `assert.that` as bare expressions that evaluate to booleans. Give every unavoidable command an idempotency boundary (`creates`, `removes`, or a defensible `changed_when`) and an explicit failure condition.
3. For a reusable role, provide the minimum role contract: defaults, tasks, handlers when needed, templates or files, `meta/main.yml`, documentation and `meta/argument_specs.yml`. Move to `ansible-role-collection-engineering` when the role will be distributed or needs Molecule or `ansible-test` coverage.
4. Place variables with `ansible-inventory-and-variable-design`; handle any credential with `ansible-vault-secrets` (`no_log: true`, `diff: false` on sensitive tasks).
5. Validate with `ansible-validate-content`: `ansible-lint`, `--syntax-check`, inventory inspection, `--list-hosts --list-tasks`, and `--check --diff --limit` on one approved host. Refresh version-specific behavior from the official Ansible release and porting guides before asserting compatibility.

## Expected output

Changed or proposed files, the public variable contract, validation evidence per command, check/diff limitations for the modules used, and convergence status. A real run and the second, zero-change run happen only on a disposable or explicitly approved target. For a review: located findings with impact and remediation, and the checks actually run.

Follow the `ansible-expert-engineer-contract` instruction for the completion report, including which checks were skipped and why a dry run is not proof of real execution.
