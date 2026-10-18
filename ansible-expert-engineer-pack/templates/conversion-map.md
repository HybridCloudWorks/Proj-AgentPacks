# Conversion map

Produced by the `ansible-convert-imperative-automation` skill. Read the whole source procedure before filling this in, and do not translate commands one-for-one.

## Source

- Procedure and location (script, runbook, Dockerfile, cloud-init):
- Target platforms it ran on:
- Observable end state that proves equivalence:

## Source inventory

| Step | Source lines | Intent | Privilege | Destructive | Secret | External dependency |
|---|---|---|---|---|---|---|
| 1 | | | root / user | yes / no | yes / no | |

## Mapping

| Step | Module (FQCN) | Idempotency boundary | Failure condition | Notes |
|---|---|---|---|---|
| 1 | | module state / `creates` / `removes` / `changed_when` | | |

Every remaining `command` or `shell` task has a row explaining why no module fits, and why `shell` rather than `command` if so.

## Variable contract

| Variable | Type | Default | Required | Replaces in source |
|---|---|---|---|---|
| | | | | hard-coded version, path, user or port |

## Secrets boundary

Which values move to Ansible Vault or an external provider, their variable names, and which tasks get `no_log: true` and `diff: false`.

## Ordering, handlers and recovery

- Order dependencies made explicit (for example: account before owned files; configuration before service notify; validation before cleanup):
- Handlers replacing inline restarts:
- Rollback: only where the source has a defensible rollback state; otherwise "none in source".

## Collections required

| Collection | Version or range | Why |
|---|---|---|

## Not safely convertible or ambiguous

| Step | Problem | Proposed handling | Needs decision from |
|---|---|---|---|

## Intentional deviations

Changes in behavior relative to the source that the user must accept, such as tighter file ownership or an added checksum.

## Validation plan

Lint, syntax check, `--list-tasks`, check/diff on an approved target (with the tasks check mode cannot evaluate), a real run on a disposable host, and the second-run convergence check.
