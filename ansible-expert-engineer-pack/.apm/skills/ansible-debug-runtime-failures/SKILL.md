---
name: ansible-debug-runtime-failures
description: Diagnose Ansible UNREACHABLE, SSH, authentication, become, module, templating, variable, version, idempotency, or performance failures from commands and evidence. Use when a playbook or inventory fails or behaves unexpectedly.
---

# Debug Runtime Failures

Classify first, then reduce scope to one inventory host, one play, and one task where possible. Preserve the exact Ansible/core version, invocation, inventory source, target OS, and relevant error text. Never paste credentials, private keys, vault passwords, or secret task output.

## Triage order

1. **Parse/config:** `ansible --version`, config source, YAML line, `ansible-playbook --syntax-check`.
2. **Inventory/selection:** `ansible-inventory --graph`, `--host`, `--list`, `--list-hosts`, `--limit`, tags, and host pattern.
3. **Connection:** `ansible host -m ansible.builtin.ping -vvv`; verify DNS, port, SSH user/key, host-key policy, target Python, and `ansible_connection`.
4. **Authentication/become:** separate SSH identity from sudo/become. Test `ansible host -m ansible.builtin.command -a 'whoami' --become -K` only on an approved safe host.
5. **Module/collection:** confirm FQCN with `ansible-doc`, collection installation/version, option names, target libraries, and platform support.
6. **Templating/variables:** inspect variable origin and type, use `assert`, and avoid `{{ }}` in conditionals. Prefer `ansible_facts[...]` and explicit `default` behavior.
7. **Runtime semantics:** inspect registered result, `rc`, `stdout`, `stderr`, `failed_when`, `changed_when`, handlers, delegation, and loop item.
8. **Performance:** inspect fact gathering, forks, strategy, serial, package locks, SSH pipelining, network calls, and tasks waiting on services.

Start with `-v`; use `-vvv` only when connection or traceback detail is needed because it can reveal sensitive inputs. Use `--start-at-task`, `--step`, `--list-tasks`, and `--limit` to narrow a reproduction.

## Version drift

When an upgrade is involved, read the relevant official porting guide before changing code. Current-baseline checks commonly include boolean conditionals, removal of embedded templating in expressions, lazy evaluation, collection/core compatibility, changed failure-result fields, and configuration deprecations. Do not assume a warning is harmless: identify the release, supported behavior, and migration path.

## Evidence discipline

Separate confirmed cause, contributing factor, hypothesis, and missing evidence. A successful syntax check does not prove target connectivity; `--check` does not exercise every module path; a passing first run does not prove convergence. Recommend the smallest safe reproduction and state exactly what it may change.
