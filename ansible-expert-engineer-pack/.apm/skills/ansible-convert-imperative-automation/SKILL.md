---
name: ansible-convert-imperative-automation
description: Convert shell scripts, manual runbooks, Dockerfile RUN steps, cloud-init, or imperative host setup into idempotent Ansible playbooks and roles. Use when replacing repeated command sequences with declarative configuration management.
---

# Convert Imperative Automation

Read the whole procedure first. Mark prerequisites, inputs, phases, target platforms, privilege changes, external dependencies, destructive operations, secrets, and the observable end state. Do not translate each command one-for-one.

## Mapping order

1. Users/groups and ownership -> `ansible.builtin.user` / `group`.
2. Packages and repositories -> platform package modules or `package`; pin repositories and verify signing.
3. Directories/files/configuration -> `file`, `copy`, `template`, `lineinfile`, `replace`.
4. Services -> `systemd_service` or `service`, with handlers for changes.
5. Downloads and archives -> `get_url` with checksum and `unarchive`.
6. APIs -> `uri` with explicit status codes, timeouts, authentication boundaries, and no secret logging.
7. Git content -> `git` with a tag or commit, not an unpinned moving branch.
8. Validation -> `assert`, service checks, and a safe idempotency test.

Use variables for versions, paths, users, ports, and environment differences. Put secrets in Vault or an external secret provider, not in defaults, examples, templates, or command lines.

## Command triage

Before using `command` or `shell`, search for a module. Prefer `command` when shell syntax is unnecessary. Use `shell` only for pipes, redirection, globbing, shell built-ins, or required expansion. Always specify an idempotency boundary (`creates`, `removes`, or state-derived `changed_when`) and a failure condition. Never use `ignore_errors` merely to make a conversion pass.

## Preserve semantics

Convert conditionals to boolean expressions without `{{ }}`. Convert loops to data-driven `loop` values. Replace restarts with handlers. Represent ordering explicitly: create a service account before files owned by it, render configuration before notifying a service, and validate before cleanup. Model rollback only when the original procedure has a defensible rollback state; do not invent one.

For Dockerfiles, distinguish image-build state from host state: `COPY` may become `copy` or `template`, `ENV` becomes variables or a service environment file, `USER` becomes service ownership or `become_user`, and `EXPOSE` is documentation unless the host firewall is intentionally managed.

## Output

Return the proposed project layout, variable contract, converted tasks, handler and recovery behavior, secrets boundary, and validation plan. Call out any source step that cannot be safely converted or whose original semantics are ambiguous.
