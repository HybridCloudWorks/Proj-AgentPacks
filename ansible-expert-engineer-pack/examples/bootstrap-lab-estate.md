# Worked example: connection-first bootstrap of a lab estate

Prompt: `bootstrap-ansible-project.prompt.md`. Skills: `ansible-bootstrap-interactive`, `ansible-inventory-and-variable-design`, `ansible-debug-runtime-failures`, `ansible-validate-content`.

Synthetic scenario. Host names and addresses are illustrative.

## Request

> I want to start managing our four lab VMs with Ansible. Nothing exists yet. Walk me through it and set up the repo.

## Phase 1: gather

The agent asks for what it cannot discover, and asks once:

| Question | Answer | Recorded as |
|---|---|---|
| Hosts and OS | `web-lab-01..03` Ubuntu 24.04; `db-lab-01` RHEL 9 | fact (user) |
| Does anything else configure them? | Hand-built VMs; no image pipeline, cloud-init or config agent after install | fact (user) |
| SSH | user `ops`, key loaded in the user's ssh-agent | fact (user) |
| Become | passwordless sudo on Ubuntu; sudo **with password** on RHEL | fact (user) |
| Environments | lab only for now; staging later | fact (user) |
| Collections required | none | fact (user) |
| Secrets | none yet | fact (user) |
| End state | baseline tools (`rsync`, `tmux`) and a lab message of the day | fact (user) |
| Disposable? | yes; all four may be pinged, dry-run and changed | authorization (user) |

> **Phase 1 summary.** Known: the table above. Passed: nothing yet. Skipped: nothing. Next safe action: write the minimal project files, with no remote contact.

## Phase 2: minimal shape

Only the files the end state needs. There is no `requirements.yml`, because every module is in `ansible.builtin`, and no role until there is something worth reusing.

```text
ansible.cfg
inventories/lab/hosts.yml
inventories/lab/group_vars/all.yml
playbooks/baseline.yml
```

```ini
# ansible.cfg
[defaults]
host_key_checking = True
interpreter_python = auto_silent
```

`ansible.cfg` deliberately sets no default `inventory`. Once staging exists, a forgotten `-i` must fail instead of silently targeting whichever environment was the default.

```yaml
# inventories/lab/hosts.yml
all:
  children:
    web:
      hosts:
        web-lab-01: { ansible_host: 10.20.0.11 }
        web-lab-02: { ansible_host: 10.20.0.12 }
        web-lab-03: { ansible_host: 10.20.0.13 }
    db:
      hosts:
        db-lab-01: { ansible_host: 10.20.0.21 }
```

```yaml
# inventories/lab/group_vars/all.yml
ansible_user: ops
baseline_packages: [rsync, tmux]
baseline_motd: "Lab host managed by Ansible. Changes made by hand will be overwritten."
```

`ansible-inventory -i inventories/lab/hosts.yml --graph` shows `@web` with three hosts and `@db` with one.

> **Phase 2 summary.** Known: four files written, inventory graph as expected. Passed: inventory parse. Skipped: no remote contact yet. Next safe action: ping all four approved lab hosts.

## Phase 3: connectivity before behavior

```text
$ ansible -i inventories/lab/hosts.yml all -m ansible.builtin.ping
web-lab-01 | SUCCESS => {"changed": false, "ping": "pong"}
web-lab-02 | SUCCESS => {"changed": false, "ping": "pong"}
web-lab-03 | SUCCESS => {"changed": false, "ping": "pong"}
db-lab-01 | UNREACHABLE! => {"changed": false, "msg": "Failed to connect to the host via ssh: Host key verification failed.", "unreachable": true}
```

**Classification: host key.** SSH stopped before authentication, so this is not an identity or sudo problem. The user confirms `db-lab-01` was rebuilt last week, which would explain a changed key, but the agent treats that as a hypothesis until the fingerprint is checked. It does **not** disable `host_key_checking` or pass `StrictHostKeyChecking=no`. Instead:

1. On the VM console, the user runs `ssh-keygen -lf /etc/ssh/ssh_host_ed25519_key.pub`.
2. On the controller, the user runs `ssh-keyscan -t ed25519 10.20.0.21 | ssh-keygen -lf -`.
3. The fingerprints match. The user removes the stale entry with `ssh-keygen -R 10.20.0.21` and accepts the new key with one interactive `ssh ops@10.20.0.21`.

The `db-lab-01` ping then returns `pong`.

Become is tested separately from SSH:

```text
$ ansible -i inventories/lab/hosts.yml web -m ansible.builtin.command -a whoami --become
web-lab-0[1-3] | CHANGED | rc=0 >> root
$ ansible -i inventories/lab/hosts.yml db -m ansible.builtin.command -a whoami --become
db-lab-01 | FAILED! => {"msg": "Missing sudo password"}
```

**Classification: sudo policy**, as the user described in phase 1. There are two options: `-K` (`--ask-become-pass`), where the user types the password into Ansible's own prompt, or a Vault-encrypted `ansible_become_password` for unattended runs. The user picks `-K` for the lab, and never types the password into this conversation. With `-K`, `whoami` on `db-lab-01` returns `root`.

(`command` always reports `CHANGED`; `whoami` changes nothing.)

> **Phase 3 summary.** Known: all four hosts reachable as `ops`; become works on all four, with a password prompt for `db`. Passed: ping ×4, become ×4. Skipped: nothing. Next safe action: add the first behavior and dry-run it.

## Phase 4: one behavior, validated

```yaml
# playbooks/baseline.yml
- name: Lab baseline
  hosts: all
  become: true
  tasks:
    - name: Install baseline tools
      ansible.builtin.package:
        name: "{{ baseline_packages }}"
        state: present

    - name: Set message of the day
      ansible.builtin.copy:
        content: "{{ baseline_motd }}\n"
        dest: /etc/motd
        owner: root
        group: root
        mode: "0644"
```

| Check | Command | Result |
|---|---|---|
| Lint | `ansible-lint playbooks/baseline.yml` | passed |
| Syntax | `ansible-playbook --syntax-check playbooks/baseline.yml` | passed |
| Selection | `ansible-playbook -i inventories/lab/hosts.yml playbooks/baseline.yml --list-hosts --list-tasks` | 4 hosts, 2 tasks |
| Dry run | `... --check --diff -K` | package task `changed` on `db-lab-01` (`tmux` absent from the minimal RHEL install), `ok` on the three Ubuntu VMs; MOTD diff shown on all 4 |

The user then authorizes a real run on the lab:

| Run | Recap |
|---|---|
| First real run | `changed=1` on web-lab-01..03, `changed=2` on db-lab-01, `failed=0` |
| Second real run | `changed=0` on all four, `failed=0` |

> **Phase 4 summary.** Known: baseline converges on all four lab hosts. Passed: lint, syntax, dry run, real run, convergence. Skipped: nothing in scope. Next safe action: decide how unattended runs will supply the `db` become password before adding a scheduler or CI.

## Completion report

### Result

Verified on approved target. The project skeleton and baseline playbook are in place, and they converge on the four disposable lab hosts, `web-lab-01..03` and `db-lab-01`.

### Evidence

| # | Check | Ran where | Kind | Status |
|---|---|---|---|---|
| 1 | `ansible-inventory --graph` | local | structural | passed |
| 2 | `ansible.builtin.ping` | 4 lab hosts | real execution (read-only) | passed after the host-key fix on `db-lab-01` |
| 3 | become `whoami` | 4 lab hosts | real execution (read-only) | passed; `db` needs `-K` |
| 4 | `ansible-lint`, `--syntax-check`, `--list-hosts --list-tasks` | local | structural | passed |
| 5 | `--check --diff` | 4 lab hosts | dry run | passed |
| 6 | Real run | 4 lab hosts | real execution | passed |
| 7 | Second run | 4 lab hosts | real execution | passed: `changed=0` |

- **Observed fact vs inference.** Observed: every command output above, and the matching fingerprints, compared by the user. Inferred: that the rebuild caused the key change. The user's account is consistent with it, but the old key was not examined.
- **Skipped check vs passed check.** No in-scope check was skipped. Unattended (non-interactive) runs were not tested, because no unattended become mechanism exists yet.
- **Local validation vs remote proof.** Remote proof exists for these four lab hosts only. Nothing here applies to the future staging environment.
- **Dry run vs real execution.** One dry run, then two real runs, all on the lab hosts the user approved in phase 1.

### Changed files or proposal

| Path | Change | Status |
|---|---|---|
| `ansible.cfg` | added: host key checking on, no default inventory | committed |
| `inventories/lab/hosts.yml` | added | committed |
| `inventories/lab/group_vars/all.yml` | added | committed |
| `playbooks/baseline.yml` | added | committed |
| Controller `~/.ssh/known_hosts` | stale `db-lab-01` key replaced, by the user | outside the repository |

### Unresolved risks

- `db-lab-01` needs an interactive become password, so a scheduled or CI run will fail there until a Vault-backed `ansible_become_password` or a narrower sudo rule exists.
- Rebuilt lab VMs will keep producing host-key failures. Recording keys at build time would remove that friction, but disabling the check would not be a safe alternative.

### Next safe action

Decide the unattended become mechanism for `db`, either a Vault-encrypted `ansible_become_password` delivered through `--vault-id` or a sudo rule scoped to the automation account. Then add `inventories/staging/` as its own inventory. Neither step touches a host until the next dry run.
