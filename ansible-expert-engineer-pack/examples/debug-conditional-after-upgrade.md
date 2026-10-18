# Worked example: two hosts fail after a controller upgrade

Prompt: `debug-ansible-failure.prompt.md`. Skills: `ansible-debug-runtime-failures`, `ansible-inventory-and-variable-design`, `ansible-validate-content`.

Synthetic scenario. Host names and paths are illustrative. The error text is abridged.

## Request

> We moved the CI controller from Ansible 11 to Ansible 13 last night. `site.yml` now fails on web-07 and web-11 only; the other ten web hosts are fine. Find out why. Do not run anything against prod. If you find the fix, put it on a branch.

Authorization in scope: read the repository and CI logs the user pasted, run local commands, commit a fix on a branch. Not authorized: any connection to production hosts.

## 1. Preserve the evidence

The user pastes the failing CI excerpt (abridged, nothing sensitive in it):

```text
TASK [app : Remove host from pool during maintenance] *************************
fatal: [web-07]: FAILED! => {"msg": "Conditional result (True) was derived from value of type 'str' at 'inventories/prod/host_vars/web-07.yml:4:23'. Conditionals must have a boolean result."}
fatal: [web-11]: FAILED! => {"msg": "Conditional result (True) was derived from value of type 'str' at 'inventories/prod/host_vars/web-11.yml:6:23'. Conditionals must have a boolean result."}
```

`ansible --version` on a local checkout that matches the new controller reports the Ansible 13 package with ansible-core 2.20, and the repository's `ansible.cfg` as the config file in use.

## 2. Classify and reduce

Following the triage order in `ansible-debug-runtime-failures`:

1. **Parse/config:** `ansible-playbook --syntax-check playbooks/site.yml` passes locally. Not a parse failure.
2. **Inventory/selection:** the failing hosts are correctly selected, so this is not a selection problem. But the error points at `host_vars`, so variable origin is the lead.
3. **Connection and become:** the task reached evaluation on both hosts, so connection and become worked. Those layers are excluded by the evidence itself, without connecting to anything.
4. **Templating/variables:** the failing layer.

The failing task:

```yaml
- name: Remove host from pool during maintenance
  ansible.builtin.include_tasks: drain.yml
  when: app_maintenance_mode
```

Scope reduced to one variable on two hosts. The inventory is a static YAML file, so inspecting it makes no remote call:

```text
ansible-inventory -i inventories/prod/hosts.yml --host web-07   ->  "app_maintenance_mode": "false"
ansible-inventory -i inventories/prod/hosts.yml --host web-03   ->  "app_maintenance_mode": false
```

`inventories/prod/host_vars/web-07.yml` line 4 and `web-11.yml` line 6 both contain `app_maintenance_mode: "false"`, a quoted string. The role default is the boolean `false`. `git log -p` shows both lines added in one hand edit during an incident.

## 3. Version drift

The jump from ansible-core 2.18 (Ansible 11) to 2.20 crosses the 2.19 release. Its porting guide is where conditional results became required to be booleans. That is one of the current-baseline checks the skill names ("boolean conditionals"). The non-empty string `"false"` is truthy, so the expression yields `True` from a `str`, and the newer core rejects it.

The agent did **not** reproduce the old controller's behavior, so how Ansible 11 treated this string is not established. If it evaluated the string as truthy, these two hosts may have been drained from the pool on every run. That would be a separate incident, and the previous run logs can confirm or rule it out.

## 4. Smallest safe reproduction

A localhost-only fixture, with no inventory and no remote connection:

```yaml
# debug/repro-conditional.yml (not committed)
- name: Reproduce string conditional
  hosts: localhost
  connection: local
  gather_facts: false
  tasks:
    - name: Conditional on the variable
      ansible.builtin.debug:
        msg: would drain
      when: app_maintenance_mode
```

```text
ansible-playbook debug/repro-conditional.yml -e '{"app_maintenance_mode": "false"}'   -> same error
ansible-playbook debug/repro-conditional.yml -e '{"app_maintenance_mode": false}'     -> task skipped
```

Both runs change nothing anywhere. The JSON form of `-e` is used so the boolean case really is a boolean.

## 5. Fix

Options considered:

| Option | Decision |
|---|---|
| Fix the data: native `false` in both `host_vars` files | **chosen** |
| Guard the role: `ansible.builtin.assert` that `app_maintenance_mode is boolean`, at the start of the role | **chosen**: the next bad value fails with a clear message instead of a type error deep in the play |
| `when: app_maintenance_mode \| bool` | rejected as the only fix: it would hide bad data instead of correcting it; acceptable later as defense in depth |
| The porting guide's compatibility setting for broken conditionals | rejected: it restores the behavior that hid the defect |

```yaml
# roles/app/tasks/main.yml (first task)
- name: Validate maintenance flag type
  ansible.builtin.assert:
    that:
      - app_maintenance_mode is boolean
    fail_msg: "app_maintenance_mode must be a YAML boolean (true/false), not a quoted string"
```

**Similar latent defects.** A key-only search lists file, line and key without values: `git grep -nE ':\s*"(true|false|yes|no)"\s*$' -- inventories roles`. It finds three more quoted booleans: `inventories/prod/group_vars/db/vars.yml` (`db_backup_enabled`), `inventories/staging/host_vars/web-02.yml` (`app_maintenance_mode`), and `roles/app/defaults/main.yml` (`app_tls_redirect`). Each is reported. Only the two named in the request are changed, because the others may be consumed as strings.

## 6. Validate the fix locally

| Check | Ran where | Result |
|---|---|---|
| `ansible-lint roles/app inventories/prod` | local | passed |
| `ansible-playbook --syntax-check playbooks/site.yml` | local | passed |
| `ansible-inventory --host web-07` and `--host web-11` | local, static file | both now show `false` (boolean) |
| Fixture with the role's assert task prepended, string value | localhost | the assert fails with the custom message |
| Same fixture, boolean value | localhost | assert passes, task skipped |

## Completion report

### Result

Verified locally. Cause confirmed: two production `host_vars` files define `app_maintenance_mode` as the string `"false"`, which ansible-core 2.20 rejects in a conditional. The fix is on branch `fix/maintenance-flag-type`. Production has not been re-run.

### Evidence

| # | Check | Ran where | Kind | Status |
|---|---|---|---|---|
| 1 | Pasted CI error output | CI (user-supplied) | real execution, before the fix | observed |
| 2 | `ansible-inventory --host` for web-07, web-11, web-03 | local, static inventory | structural | passed: type difference shown |
| 3 | Localhost fixture, string and boolean | localhost | local test | passed: reproduced, then skipped |
| 4 | `ansible-lint`, `--syntax-check` after the fix | local | structural | passed |
| 5 | `site.yml --check --diff --limit web-07` | — | dry run | not run: production connection not authorized |
| 6 | `site.yml` real run on web-07, web-11 | — | real execution | not run: not authorized |

- **Observed fact vs inference.** Observed: the error text, the quoted values and their Git history, the fixture behavior under core 2.20. Inferred: that the 2.19 conditional change is why this surfaced only after the upgrade. Not established: how the old controller evaluated the string.
- **Skipped check vs passed check.** The production dry run and real run were not run. They are not counted as passed.
- **Local validation vs remote proof.** The fixture proves the expression behavior on this core version. It does not prove the play now succeeds on web-07 and web-11, or that `drain.yml` behaves correctly there.
- **Dry run vs real execution.** The only real execution is the pre-fix CI run the user supplied. Nothing has executed against production since the fix.

### Changed files or proposal

| Path | Change | Status |
|---|---|---|
| `inventories/prod/host_vars/web-07.yml` | `"false"` to `false` | committed on branch |
| `inventories/prod/host_vars/web-11.yml` | `"false"` to `false` | committed on branch |
| `roles/app/tasks/main.yml` | added type assert as first task | committed on branch |
| Three other quoted booleans | reported, not changed | proposed only |

The failure diagnosis is recorded with `templates/failure-diagnosis.md`.

### Unresolved risks

- If the old controller treated `"false"` as truthy, web-07 and web-11 may have been drained on every previous run. Check the previous CI logs for that task on those hosts.
- `inventories/staging/host_vars/web-02.yml` has the same defect and will fail the next staging run.
- The new assert makes any other host with a quoted value fail fast. That is intended, but it can stop a run that previously "worked".

### Next safe action

Merge after review, then have CI run `ansible-playbook -i inventories/prod/hosts.yml playbooks/site.yml --check --diff --limit web-07,web-11` under the team's normal production approval. That dry run connects to the two hosts but changes nothing.
