# Worked example: reusable chrony role, Molecule unavailable

Prompt: `engineer-role-or-collection.prompt.md`. Skills: `ansible-role-collection-engineering`, `ansible-playbook-development`, `ansible-validate-content`.

Synthetic scenario. Repository names are illustrative.

## Request

> Three of our project repos each have their own copy-pasted chrony tasks. Build one proper role they can all consume, with tests. RHEL 9 and Ubuntu 24.04. Make it a collection if that's the right thing.

Authorization in scope: create the role in a new repository the user has created, and run local tests. Not authorized: installing software on the workstation, publishing.

## 1. Choose the boundary

The skill says to choose the boundary first. There is one role, no modules or plugins, and three internal consumers. A collection would add `galaxy.yml`, a namespace, `ansible-test` sanity and a release pipeline without adding a contract the role does not already have. Decision: a **standalone role repository**, consumed through `requirements.yml` pinned to a Git tag. Revisit a collection when a second role or a plugin appears.

```yaml
# consumer requirements.yml
roles:
  - name: chrony
    src: git+https://git.example.internal/platform/ansible-role-chrony.git
    version: v1.0.0
```

No credentials go in the URL. The consumers' Git client already authenticates.

## 2. Contract

The README is written from `templates/role-contract.md`. The public inputs, all prefixed `chrony_`:

| Variable | Type | Default | Required |
|---|---|---|---|
| `chrony_servers` | list of str | none | yes |
| `chrony_allow_networks` | list of str | `[]` | no |
| `chrony_makestep_threshold` | float | `1.0` | no |
| `chrony_makestep_limit` | int | `3` | no |
| `chrony_service_enabled` | bool | `true` | no |

Platform differences are internal and live in `vars/`, which consumers must not override. They are loaded with `ansible.builtin.include_vars` and `first_found` on `ansible_facts['os_family']`:

```yaml
# vars/RedHat.yml
__chrony_config_path: /etc/chrony.conf
__chrony_service: chronyd

# vars/Debian.yml
__chrony_config_path: /etc/chrony/chrony.conf
__chrony_service: chrony
```

The double-underscore prefix marks them as internal and keeps them out of the argument spec.

```yaml
# meta/argument_specs.yml
argument_specs:
  main:
    short_description: Configure chrony time synchronisation
    options:
      chrony_servers:
        type: list
        elements: str
        required: true
        description: NTP servers or pools to use.
      chrony_allow_networks:
        type: list
        elements: str
        default: []
        description: Client networks allowed to query this host. Empty means serve no clients.
      chrony_makestep_threshold:
        type: float
        default: 1.0
        description: Offset in seconds above which chrony steps the clock.
      chrony_makestep_limit:
        type: int
        default: 3
        description: Number of initial updates during which stepping is allowed.
      chrony_service_enabled:
        type: bool
        default: true
        description: Whether the chrony service is enabled and running.
```

The tasks use `ansible.builtin.package`, `ansible.builtin.template` (`mode: "0644"`, notifying `Restart chrony`) and `ansible.builtin.systemd_service`. Every module is in `ansible.builtin`, so the role needs no collection.

## 3. Tests

The Molecule `default` scenario uses the Docker driver from `molecule-plugins`, with two platforms: a UBI 9 image and an Ubuntu 24.04 image. Its sequence is converge, idempotence, verify, destroy. `verify.yml` asserts that the rendered configuration contains every `chrony_servers` entry and that the service is enabled.

**What the container scenario can never prove.** An unprivileged container cannot discipline the system clock, so chronyd may refuse to adjust time or fail to start there. The scenario proves rendering, packaging and idempotence, not time synchronization. Synchronization needs a VM scenario, which this environment does not have.

**What happened when the agent tried to run it** (output abridged):

```text
$ molecule --version
molecule ... using python 3.12
    ansible: ...
    default: ... from molecule
$ docker info
bash: docker: command not found
$ podman info
bash: podman: command not found
```

No container runtime is installed. Installing one is outside the authorized scope, so the agent does not install it. `molecule test` is **skipped**.

What did run locally, with no host changes:

| Check | Command | Result |
|---|---|---|
| Lint | `ansible-lint` (role repository root) | passed |
| Syntax, converge playbook | `ansible-playbook --syntax-check molecule/default/converge.yml` | passed |
| Argument spec, negative case | `ansible-playbook -i localhost, -c local tests/argspec-missing.yml --check` | failed as intended: "missing required arguments: chrony_servers", before any task ran |

`tests/argspec-missing.yml` applies the role to localhost without `chrony_servers`, with `gather_facts: false`. Role argument validation runs before the role's tasks, so the run stops before touching the workstation's packages or services. Check mode is a second safeguard.

## Completion report

### Result

Prepared, unverified. The `chrony` role, its argument spec, README contract and Molecule scenario are written. Static checks and the argument-spec negative test passed. The Molecule scenario was skipped because no container runtime is available, so neither platform has been exercised.

### Evidence

| # | Check | Ran where | Kind | Status |
|---|---|---|---|---|
| 1 | `ansible-lint` | local | structural | passed |
| 2 | `--syntax-check` on the converge playbook | local | structural | passed |
| 3 | Argument spec rejects a missing `chrony_servers` | localhost, check mode | local test | passed (expected failure observed) |
| 4 | `molecule test`, UBI 9 and Ubuntu 24.04 | — | local test | skipped: no Docker or Podman, and installing one is not authorized |
| 5 | Idempotence | — | local test | skipped: part of 4 |
| 6 | Time synchronization on a real host | — | real execution | not run: needs a VM; out of scope for containers anyway |

- **Observed fact vs inference.** Observed: the lint, syntax and argument-spec output, and the missing container runtimes. Inferred, not tested: the per-OS paths and service names in `vars/`. They follow each distribution's packaging, but no target has confirmed them.
- **Skipped check vs passed check.** Molecule converge, idempotence and verify are all skipped. The supported-platforms table in the README marks both platforms "declared only", not "exercised".
- **Local validation vs remote proof.** Nothing has run on RHEL 9 or Ubuntu 24.04. The argument-spec test proves input validation only.
- **Dry run vs real execution.** The only execution is the localhost negative test, in check mode, which stopped at argument validation. The role's tasks have not executed anywhere.

### Changed files or proposal

| Path | Change | Status |
|---|---|---|
| `ansible-role-chrony/defaults/`, `tasks/`, `handlers/`, `templates/`, `vars/`, `meta/` | role content and argument spec | committed on `main` of the new repository; not tagged |
| `ansible-role-chrony/README.md` | contract from the role-contract template | committed |
| `ansible-role-chrony/molecule/default/` | scenario: two platforms, verify assertions | committed, never run |
| `ansible-role-chrony/tests/argspec-missing.yml` | negative test | committed |
| Consumer `requirements.yml` entry pinned to `v1.0.0` | | proposed only; tag not created until Molecule passes |

### Unresolved risks

- The per-OS `vars/` values are unconfirmed on real images.
- The chronyd behavior in containers may make the `verify` step's "service running" assertion flaky. The scenario asserts "enabled" for that reason, and that choice is also untested.
- The three consumer repositories still carry their copies. The migration of each consumer is not part of this task.

### Next safe action

Run `molecule test` on a machine or CI runner that already has Docker or Podman, for example the platform team's CI. Tag `v1.0.0` only after both platforms pass converge and idempotence. That run creates and destroys local containers only.
