---
name: review-ansible-automation
description: Review Ansible playbooks, roles, collections, inventories, variables, templates, handlers, plugins, vault integration, and execution pipelines for target selection, precedence, idempotency, failure semantics, rollout, privilege, secrets, and dependency integrity. Use when a PR changes Ansible YAML, roles, collections, inventory, ansible.cfg, requirements, or commands that run Ansible. Treat check and diff mode as incomplete evidence.
---

# Objective

Prove that Ansible selects the intended hosts and privilege context, converges safely on repeated runs, reports changes and failures accurately, and preserves availability and secrets.

## Inputs

- Playbook entry points, includes/imports, roles, collections, inventory, host patterns, limits, tags, variables, vault sources, controller identity, and become behavior.
- Tasks, handlers, templates, files, commands, rollout controls, dependencies, and pipeline invocation.
- Syntax, lint, limited check/diff, Molecule or integration, and second-run idempotence evidence when safe and available.

## Workflow

1. Identify entry points, inventory sources, host patterns, limits, tags, strategy, forks, controller and connection identities, become context, delegation, and runtime dependencies.
2. Trace variable precedence across defaults, vars, inventory, group/host data, facts, registered results, includes, environment lookups, vault, and extra vars.
3. Review undefined, null, empty, false, zero, scalar/list, boolean-like, and host-specific values. Require early validation for critical inputs.
4. Review module idempotency, command/shell guards, `changed_when`, `failed_when`, exit codes, partial-failure reruns, and second-run behavior.
5. Review conditions, loops, includes/imports, tags, `run_once`, delegation, blocks/rescue/always, handlers, restart timing, and validation-before-restart.
6. Review ignored errors, failure thresholds, serial rollout, retries, unreachable hosts, cancellation, file modes, templates, diff exposure, `no_log`, and privilege boundaries.
7. Review collection/role versions, custom executable plugins, dependency installation, syntax/lint output, limited check/diff evidence, and disposable integration results.
8. Return confirmed findings and evidence gaps to `review-infrastructure-pr`.

## Decision Rules

- Prefer idempotent modules when an appropriate module exists and the behavior matters.
- A clean check-mode run does not prove idempotency or production safety.
- Broad `ignore_errors` or inaccurate changed status is high scrutiny because it can hide failure or trigger unsafe handlers.
- Do not automatically run check mode against real targets during review.

## Output Contract

Return technology-specific findings and evidence gaps to `review-infrastructure-pr` with an anchor, trigger, affected target, impact, remediation, and verification evidence. Do not repeat universal gates or create another final report.

## Validation and Stop Conditions

Use `references/review-checklist.md`; verify uncertain semantics through `references/official-sources.md`. Stop when decisive target state, identity, versions, generated output, or safe access is unavailable. Never mutate targets or expose sensitive values.

## Resources

- Read `references/review-checklist.md` for the complete technology adapter.
- Read `references/official-sources.md` when behavior is version-specific, uncertain, or current verification is required.
