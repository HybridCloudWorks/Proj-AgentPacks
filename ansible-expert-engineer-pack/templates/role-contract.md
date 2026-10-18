# Role contract

Produced by the `ansible-role-collection-engineering` skill as the role's `README.md`, alongside `meta/argument_specs.yml`. Keep the two in step: every input documented here is declared in the argument spec, and nothing internal is.

## Purpose

What the role configures, and what it deliberately does not.

## Supported platforms

| OS family | Versions | Tested by | Status |
|---|---|---|---|
| | | Molecule scenario / VM / none | exercised / declared only |

## Requirements

- `ansible-core` range:
- Collections, with version ranges:
- Managed-node Python:
- Privilege: which tasks need `become`, and why.

## Inputs

| Variable | Type | Default | Required | Description |
|---|---|---|---|---|
| | | | | |

Required inputs have no default. Secrets are never given defaults or example values; reference a Vault variable instead.

## Outputs and side effects

Files, packages, services, users and firewall rules the role manages; facts it sets; anything it removes.

## Tags

| Tag | Covers |
|---|---|

## Handlers

| Handler | Triggered by | Effect |
|---|---|---|

## Idempotency

A second run with the same inputs reports `changed=0`. List any task that intentionally changes on every run, and why.

## Example playbook

```yaml
- name: Apply the role
  hosts: <group>
  become: true
  roles:
    - role: <namespace.collection.role or role name>
      vars:
        <required_input>: <value>
```

## Testing

| Scenario | Driver | Platforms | Sequence | Last result |
|---|---|---|---|---|
| default | | | converge, idempotence, verify | passed / failed / skipped (reason) |

State what the scenarios cannot prove, for example kernel or clock behavior inside unprivileged containers.

## Argument spec skeleton

```yaml
# meta/argument_specs.yml
argument_specs:
  main:
    short_description: <one line>
    options:
      <required_input>:
        type: str
        required: true
        description: <what it controls>
      <optional_input>:
        type: bool
        default: true
        description: <what it controls>
```

## Changelog

Record each release with its version, date and any change to inputs, defaults or supported platforms.
