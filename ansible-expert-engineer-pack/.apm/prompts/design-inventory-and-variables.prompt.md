---
description: "Design or troubleshoot Ansible inventories, variable precedence, facts and environment separation"
agent: ansible-expert-engineer
---

# Design inventory and variables

## Inputs

- The environments, and where hosts come from: static files, an inventory plugin, or a CMDB.
- The current group taxonomy, `group_vars`/`host_vars`, and any variable whose value is surprising.
- Which facts the content needs, current fact-caching settings, and who may pass extra vars.

Querying a dynamic inventory source is a remote call that needs its own credentials and approval. Treat generated inventory and variables as untrusted until their source, identity, freshness and scope are known.

## Workflow

1. Apply `ansible-inventory-and-variable-design`. Use separate environment inventories or an explicit environment selector, and stable, meaningful group names. For inventory plugins, document authentication, cache behavior, filters, rate limits and the source-of-truth owner.
2. Inspect with `ansible-inventory --graph`, `--list` and `--host` for representative hosts, and `ansible-playbook --list-hosts --list-tasks` for each entrypoint.
3. Place each variable deliberately: role defaults for user inputs, inventory variables for environment and host facts, play and task vars only for local orchestration. Make types explicit and validate required values with `assert` or argument specs. Never let an untrusted caller inject paths, commands, module names or credentials through extra vars.
4. Decide which facts are needed, whether cached facts can be stale or cross an environment boundary, and prove every consumed fact is supplied when `gather_facts: false`.
5. Review host patterns, `--limit`, tags, `serial`, delegation, `run_once` and `delegate_facts` together with `ansible-execution-control`. Keep secrets out of inventory with `ansible-vault-secrets`, and validate with `ansible-validate-content`.

## Expected output

The proposed inventory layout; a variable placement table (variable, scope, file, type, owner); a precedence analysis for every conflicting variable; selection proof per environment; fact and caching decisions; and any missing inventory freshness or authorization evidence.

Follow the `ansible-expert-engineer-contract` instruction for the completion report.
