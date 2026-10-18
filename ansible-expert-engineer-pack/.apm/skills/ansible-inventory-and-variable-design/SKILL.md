---
name: ansible-inventory-and-variable-design
description: Design or troubleshoot Ansible inventories, inventory plugins, host/group variables, precedence, facts, caching, environment separation, and target selection without accidental cross-environment or cross-host changes.
---

# Inventory and Variable Design

Inventory is the execution boundary. Before authoring tasks, prove which hosts, groups, variables, connection settings, and environment are selected. Treat dynamic inventory and generated variables as untrusted inputs until their source, identity, freshness, and scope are known.

## Inventory shape

Use separate environment inventories or an explicit environment selector. Keep group names meaningful and stable. Put connection details and non-secret host/group variables in the appropriate inventory scope; keep secrets in Vault or an external provider. For inventory plugins, document authentication, cache behavior, filters, rate limits, and the source-of-truth owner.

Inspect with:

```text
ansible-inventory -i inventories/staging/hosts.yml --graph
ansible-inventory -i inventories/staging/hosts.yml --list
ansible-inventory -i inventories/staging/hosts.yml --host one_host
ansible-playbook -i inventories/staging/hosts.yml playbooks/site.yml --list-hosts --list-tasks
```

## Variables and precedence

Prefer role defaults for user inputs, inventory vars for environment/host facts, and play/task vars only for local orchestration. Avoid `vars` or extra vars as an accidental override mechanism. Make types explicit and validate required values with `assert` or role argument specs. Remember that extra vars override almost everything; never allow an untrusted caller to inject arbitrary paths, commands, module names, or credentials.

## Facts and caching

Decide whether facts are required, which subset is enough, and whether cached facts can be stale or cross environment boundaries. Use `ansible_facts[...]` in new content. Do not use fact caching as a secret store. If `gather_facts: false`, prove that every consumed fact is supplied another way.

## Safety review

Check host patterns, `--limit`, tags, `serial`, delegation, `run_once`, and `delegate_facts` together. A correct task applied to the wrong inventory is still a production incident. Report the exact selection proof and any missing inventory freshness or authorization evidence.
