---
description: "Convert a shell script, runbook, Dockerfile or cloud-init into idempotent Ansible"
agent: ansible-expert-engineer
---

# Convert imperative automation to Ansible

## Inputs

- The complete source procedure: shell script, manual runbook, Dockerfile `RUN` steps, or cloud-init.
- Target platforms, which steps run with elevated privilege, external endpoints the procedure calls, and secrets it uses.
- The observable end state that proves the conversion is equivalent.

Read the whole procedure before converting anything. Ask only when a step's intent cannot be inferred from the source.

## Workflow

1. Apply `ansible-convert-imperative-automation`. Mark prerequisites, inputs, phases, privilege changes, destructive operations, secrets, external dependencies and the end state. Do not translate commands one-for-one.
2. Map in the skill's order: users and groups, packages and repositories, files and configuration, services with handlers, downloads with checksums, APIs with explicit status codes and timeouts, Git content pinned to a tag or commit, then validation with `assert`.
3. Triage every remaining `command` or `shell` task: search for a module first, prefer `command` over `shell`, and give each an idempotency boundary and a failure condition. Never use `ignore_errors` to make a conversion pass.
4. Preserve semantics: boolean conditionals without `{{ }}`, data-driven `loop`, handlers for restarts, explicit ordering. Model rollback only where the source has a defensible rollback state. For Dockerfiles, separate image-build state from host state.
5. Write the converted content with `ansible-playbook-development`, add any collection the mapped modules need with `ansible-collections-supply-chain`, move secrets with `ansible-vault-secrets`, and validate with `ansible-validate-content`.

## Expected output

The proposed project layout; the variable contract; a step-by-step conversion map (source step, chosen module, idempotency boundary, notes); handler and recovery behavior; the secrets boundary; the validation plan and results; and every source step that could not be converted safely or whose original semantics are ambiguous. Intentional deviations from the source, such as tighter ownership, are listed for the user to accept.

Follow the `ansible-expert-engineer-contract` instruction for the completion report. A check-mode run of converted content is a dry run and does not prove the end state.
