# Worked example: convert a shell install script into a role

Prompt: `convert-imperative-automation.prompt.md`. Skills: `ansible-convert-imperative-automation`, `ansible-playbook-development`, `ansible-collections-supply-chain`, `ansible-validate-content`.

Synthetic scenario. Host names, paths and the repository are illustrative. The version numbers show the technique and are not recommendations.

## Request

> We install the Prometheus node exporter on our RHEL 9 hosts with `install-node-exporter.sh`. Turn it into an Ansible role. You can edit the repo on a branch and dry-run against `mon-lab-01`, which is a throwaway lab VM. Don't run it for real yet.

Authorization in scope: repository edits on a branch; check mode against `mon-lab-01` only. Not authorized: a real run, any other host.

## Source procedure

```bash
#!/usr/bin/env bash
set -e
VERSION=1.8.2
useradd --system --no-create-home --shell /usr/sbin/nologin node_exporter || true
cd /tmp
curl -sLO https://github.com/prometheus/node_exporter/releases/download/v${VERSION}/node_exporter-${VERSION}.linux-amd64.tar.gz
tar xzf node_exporter-${VERSION}.linux-amd64.tar.gz
cp node_exporter-${VERSION}.linux-amd64/node_exporter /usr/local/bin/
chown node_exporter:node_exporter /usr/local/bin/node_exporter
cat > /etc/systemd/system/node_exporter.service <<EOF
[Unit]
Description=Node Exporter
After=network-online.target
[Service]
User=node_exporter
ExecStart=/usr/local/bin/node_exporter --web.listen-address=:9100
Restart=on-failure
[Install]
WantedBy=multi-user.target
EOF
systemctl daemon-reload
systemctl enable --now node_exporter
firewall-cmd --permanent --add-port=9100/tcp
firewall-cmd --reload
```

## 1. Read the whole procedure first

The agent marks what the script does before mapping anything:

- **End state:** a `node_exporter` system account; the binary at `/usr/local/bin/node_exporter`; a systemd unit, enabled and running; TCP 9100 open in firewalld.
- **Privilege:** every step runs as root.
- **External dependency:** a GitHub release download with **no integrity check**.
- **Hidden failure:** `|| true` after `useradd` swallows every error, not only "user exists".
- **Destructive steps:** none, but the unit file is overwritten on every run, and `daemon-reload` and `enable --now` run every time.
- **Secrets:** none.
- **Platforms:** the user confirms RHEL 9 only. Ubuntu is out of scope, so `ufw` is not modelled.

## 2. Map in the skill's order

The result is recorded with `templates/conversion-map.md`; the mapping table is reproduced here.

| Step | Source | Module | Idempotency boundary | Notes |
|---|---|---|---|---|
| 1 | `useradd ... \|\| true` | `ansible.builtin.user` | module state | `system: true`, `create_home: false`, `shell: /usr/sbin/nologin`. The `\|\| true` disappears; real failures now fail. |
| 2 | `curl -sLO` | `ansible.builtin.get_url` | `checksum` plus versioned `dest` | Checksum taken from the release's published `sha256sums.txt` by URL. The agent does not invent a hash. |
| 3 | `tar xzf` and `cp` | `ansible.builtin.unarchive` (`remote_src: true`) and `ansible.builtin.file` (`state: link`) | `creates:` on the versioned binary; link state | Unpacks to `/opt/node_exporter/<version>/` and links `/usr/local/bin/node_exporter`, so upgrades change one link. |
| 4 | `chown node_exporter:...` | `ansible.builtin.file` | module state | **Intentional deviation**, see below. |
| 5 | heredoc unit file | `ansible.builtin.template` | content comparison | `notify: Restart node_exporter` |
| 6 | `daemon-reload`, `enable --now` | `ansible.builtin.systemd_service` | module state | `enabled: true`, `state: started`, `daemon_reload: true` |
| 7 | `firewall-cmd` x2 | `ansible.posix.firewalld` | module state | `port: 9100/tcp`, `permanent: true`, `immediate: true`, `state: enabled`. Gated by `node_exporter_manage_firewall`. |

No `command` or `shell` task remains.

**Intentional deviation.** The script makes the service account own its own binary, so a compromised exporter could replace the file it runs. The role installs the binary as `root:root` with mode `"0755"`. The service still runs as `node_exporter`. This is listed for the user to accept rather than applied silently.

**Ambiguity kept, not resolved.** `--web.listen-address=:9100` binds every interface. The role keeps that as the default of `node_exporter_listen_address` so behavior is unchanged, and flags it as a risk.

## 3. Variable contract and dependencies

```yaml
# roles/node_exporter/defaults/main.yml
node_exporter_version: "1.8.2"
node_exporter_arch: "linux-amd64"
node_exporter_checksum_url: "https://github.com/prometheus/node_exporter/releases/download/v{{ node_exporter_version }}/sha256sums.txt"
node_exporter_listen_address: ":9100"
node_exporter_manage_firewall: true
node_exporter_firewall_port: "9100/tcp"
```

`ansible.posix.firewalld` needs the `ansible.posix` collection, which the repository did not declare. Following `ansible-collections-supply-chain`, the agent adds a bounded range rather than an unpinned entry:

```yaml
# requirements.yml
collections:
  - name: ansible.posix
    version: ">=2.0.0,<3.0.0"
```

Installing it is a dependency installation, so the agent asks first. The user approves a project-local install: `ansible-galaxy collection install -r requirements.yml -p ./collections`. The project's `ansible.cfg` already sets `collections_path = ./collections`, so `ansible-doc ansible.posix.firewalld` then resolves.

## 4. Key tasks

```yaml
# roles/node_exporter/tasks/main.yml (excerpt)
- name: Download node_exporter release archive
  ansible.builtin.get_url:
    url: "https://github.com/prometheus/node_exporter/releases/download/v{{ node_exporter_version }}/node_exporter-{{ node_exporter_version }}.{{ node_exporter_arch }}.tar.gz"
    dest: "/opt/node_exporter/node_exporter-{{ node_exporter_version }}.tar.gz"
    checksum: "sha256:{{ node_exporter_checksum_url }}"
    owner: root
    group: root
    mode: "0644"

- name: Unpack node_exporter
  ansible.builtin.unarchive:
    src: "/opt/node_exporter/node_exporter-{{ node_exporter_version }}.tar.gz"
    dest: "/opt/node_exporter/{{ node_exporter_version }}"
    remote_src: true
    extra_opts: ["--strip-components=1"]
    creates: "/opt/node_exporter/{{ node_exporter_version }}/node_exporter"

- name: Install node_exporter unit
  ansible.builtin.template:
    src: node_exporter.service.j2
    dest: /etc/systemd/system/node_exporter.service
    owner: root
    group: root
    mode: "0644"
  notify: Restart node_exporter

- name: Open the exporter port
  ansible.posix.firewalld:
    port: "{{ node_exporter_firewall_port }}"
    permanent: true
    immediate: true
    state: enabled
  when: node_exporter_manage_firewall
```

The version directory is created by an earlier `ansible.builtin.file` task with `state: directory`.

## 5. Validate

| Check | Command | Ran where | Result |
|---|---|---|---|
| Lint | `ansible-lint roles/node_exporter playbooks/monitoring.yml` | local | passed, no violations at the `production` profile |
| Syntax | `ansible-playbook --syntax-check playbooks/monitoring.yml` | local | passed |
| Selection | `ansible-playbook -i inventories/lab/hosts.yml playbooks/monitoring.yml --limit mon-lab-01 --list-hosts --list-tasks` | local | 1 host, 9 tasks, as expected |
| Dry run | `... --check --diff --limit mon-lab-01` | `mon-lab-01` (approved) | partial, see below |

**Check-mode result.** The user, directory and download tasks report `changed`. In check mode `get_url` reports the download without performing it, so the next task, `unarchive`, fails with "Source ... does not exist". This is a check-mode limitation, not a defect. The agent does **not** add `ignore_errors`, and does not set `check_mode: false` on the download, because that would write to the lab host during a dry run the user asked to be read-only. The link, ownership, unit, service and firewall tasks were therefore not evaluated by the dry run, and `unarchive` was evaluated only up to the missing archive.

## Completion report

### Result

Prepared, unverified. The `node_exporter` role, `requirements.yml` entry and playbook are on branch `convert/node-exporter`. Static checks passed. The dry run on `mon-lab-01` stopped at the unarchive step, as expected in check mode. No real run was made.

### Evidence

| # | Check | Ran where | Kind | Status |
|---|---|---|---|---|
| 1 | `ansible-lint` | local | structural | passed |
| 2 | `--syntax-check` | local | structural | passed |
| 3 | `--list-hosts --list-tasks` | local, static inventory | structural | passed: 1 host, 9 tasks |
| 4 | `ansible-doc ansible.posix.firewalld` after project-local install | local | structural | passed |
| 5 | `--check --diff --limit mon-lab-01` | `mon-lab-01` | dry run | partial: 3 tasks changed, `unarchive` failed as expected, 5 not evaluated |
| 6 | Real run | — | real execution | not run: not authorized |
| 7 | Second-run convergence | — | real execution | not run: depends on 6 |

- **Observed fact vs inference.** Observed: the lint, syntax and selection output; the check-mode failure text on `mon-lab-01`. Inferred: the unarchive failure comes from the download being simulated, because the archive path is the `get_url` destination. This was not proven by a real download.
- **Skipped check vs passed check.** Skipped: the real run and convergence run (not authorized), and the check-mode evaluation of the 5 tasks after `unarchive` (blocked by the simulated download). None of these is reported as passed.
- **Local validation vs remote proof.** Lint, syntax and selection prove structure only. Nothing here proves that the exporter starts, listens on 9100, or is reachable through the firewall.
- **Dry run vs real execution.** One dry run against one lab host. No task has executed for real anywhere.

### Changed files or proposal

| Path | Change | Status |
|---|---|---|
| `roles/node_exporter/` (defaults, tasks, handlers, templates, meta) | added | committed on branch |
| `playbooks/monitoring.yml` | added | committed on branch |
| `requirements.yml` | `ansible.posix` `>=2.0.0,<3.0.0` added | committed on branch |
| `install-node-exporter.sh` | unchanged; retire after acceptance | proposed only |

Decisions for the user: accept `root:root` ownership of the binary; decide whether the exporter should bind a single interface.

### Unresolved risks

- The exporter listens on all interfaces, as the script did. Closing this needs the monitoring network's address.
- The download depends on GitHub availability at run time. An internal mirror would remove that. Not requested.
- Behavior on hosts with firewalld stopped is unverified; `ansible.posix.firewalld` with `immediate: true` needs a running daemon.

### Next safe action

The user authorizes one real run on `mon-lab-01`: `ansible-playbook -i inventories/lab/hosts.yml playbooks/monitoring.yml --limit mon-lab-01`, followed by the same command again, expecting `changed=0`. The first run creates the account, files, unit and firewall rule on that lab host only.
