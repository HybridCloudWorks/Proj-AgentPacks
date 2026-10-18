# Worked example: rolling release behind HAProxy

Prompt: `plan-rolling-change.prompt.md`. Skills: `ansible-execution-control`, `ansible-inventory-and-variable-design`, `ansible-validate-content`.

Synthetic scenario. Host names, groups and the application are illustrative.

## Request

> Plan the rollout of app release 4.12 to the eight prod app servers behind our two HAProxy nodes. We must keep at least six serving at all times. You can run it for real in staging; prod goes through the change window on Thursday with the on-call operator.

Authorization in scope: plan, validate, and run for real against the staging inventory. Not authorized: any production run.

## 1. Host-selection proof

Both inventories are static YAML files, so these commands make no remote calls.

```text
ansible-inventory -i inventories/prod/hosts.yml --graph app   -> @app: app-01 ... app-08 (8 hosts)
ansible-inventory -i inventories/prod/hosts.yml --graph lb    -> @lb: lb-01, lb-02
ansible-playbook  -i inventories/prod/hosts.yml playbooks/app-release.yml --list-hosts
    play #1 (localhost): Record release start     hosts (1): localhost
    play #2 (app):       Roll app release         hosts (8): app-01 ... app-08
```

Staging is three app hosts (`app-stg-01..03`) and one load balancer (`lb-stg-01`).

The agent confirms `app_release_version` comes only from `inventories/<env>/group_vars/app.yml`. It does not come from extra vars in the CI job, so a caller cannot redirect the release by passing `-e`.

## 2. Batching and failure policy

The constraint is six of eight serving, so at most two hosts may be out at once. One host goes first as a canary:

```yaml
- name: Roll app release
  hosts: app
  serial: [1, 2]           # batches of 1, 2, 2, 2, 1; the last list value repeats
  max_fail_percentage: 0   # any failed host stops all later batches
  order: inventory
```

When a batch fails, Ansible does not start the next batch. The hosts in the failed batch stay drained (see section 4), so capacity never drops below six.

Strategy stays `linear`, because the load-balancer steps for one host must finish before the next host's.

## 3. Concurrency and delegation

```yaml
  pre_tasks:
    - name: Drain host from every load balancer
      community.general.haproxy:
        state: disabled
        drain: true
        host: "{{ inventory_hostname }}"
        backend: app_backend
        socket: /run/haproxy/admin.sock
        wait: true
      delegate_to: "{{ item }}"
      loop: "{{ groups['lb'] }}"

  roles:
    - role: app_release        # installs the package, renders config, notifies "Restart app"

  post_tasks:
    - name: Wait for health endpoint
      ansible.builtin.uri:
        url: "http://127.0.0.1:8080/healthz"
        status_code: 200
        timeout: 5
      register: app_health
      until: app_health.status == 200
      retries: 24
      delay: 5

    - name: Return host to every load balancer
      community.general.haproxy:
        state: enabled
        host: "{{ inventory_hostname }}"
        backend: app_backend
        socket: /run/haproxy/admin.sock
        wait: true
      delegate_to: "{{ item }}"
      loop: "{{ groups['lb'] }}"
```

Points the agent checked:

- **Dependency:** `community.general.haproxy` comes from `community.general`, which `requirements.yml` already pins to a bounded range. No new dependency is added.
- **`delegate_to`:** the HAProxy calls run on each `lb` host using that host's connection variables, while `inventory_hostname` remains the app host being drained. That is intended. `delegate_facts` is not used because no facts are gathered on the load balancers.
- **Races:** two app hosts in the same batch drain concurrently through the same admin socket. Each call names a different server, so they do not conflict. No `throttle` is needed at a batch size of two.
- **`run_once`:** the original draft had a `run_once: true` "post release start to chat" task inside the rolling play. Under `serial` that runs once per batch, which would post five times. The agent moved it to play #1 on `localhost`, which runs once per rollout.

## 4. Handlers and failure behavior

- `Restart app` is notified inside `roles:`. Handlers notified in a section are flushed at the end of that section, so the restart happens before `post_tasks` begins. No `meta: flush_handlers` is needed.
- No `force_handlers`. If the role fails after rendering the new configuration, the restart is skipped and the host stays drained with the old process running. That is the safe state, and the failed host stops the rollout.
- No `ignore_errors` or `ignore_unreachable`. If either load balancer is unreachable, the drain fails, the host fails, and the rollout stops before anything changes on it.
- The health check is bounded: 24 attempts, 5 seconds apart, about two minutes. A host that never becomes healthy fails and stays drained.

## 5. Recovery

- **Forward recovery:** fix and re-run with `--limit` set to the failed host.
- **Rollback:** set `app_release_version` back to 4.11 and run the same play. The `app_release` role passes `allow_downgrade: true` to `ansible.builtin.dnf`. Package 4.11 is still in the internal repository: `dnf --showduplicates list app` was run on `app-stg-01` during the approved staging session.
- **Schema:** the release notes state that 4.12 has no database migration. The agent did not verify this independently; it is recorded as an inference from the vendor's notes.

## 6. Validate

| Step | Command | Target | Kind | Result |
|---|---|---|---|---|
| Lint | `ansible-lint playbooks/app-release.yml roles/app_release` | local | structural | passed |
| Syntax | `ansible-playbook --syntax-check playbooks/app-release.yml` | local | structural | passed |
| Selection, prod | `--list-hosts`, `--list-tasks` against the prod inventory | local, static file | structural | passed: 8 app, 2 lb |
| Dry run, staging | `-i inventories/staging/hosts.yml ... --check --diff` | staging | dry run | passed; see limits below |
| Real run, staging | `-i inventories/staging/hosts.yml playbooks/app-release.yml` | staging | real execution | passed: 2 batches (1 host, then 2), each host drained, restarted, healthy and re-enabled |
| Second run, staging | same command | staging | real execution | `app_release` tasks `changed=0`; drain and enable report `changed`, as expected |

**What the staging dry run did not show.** Check mode does not drain anything through the HAProxy socket, and a health check that follows a simulated restart proves nothing about the new release. The drain, health and re-enable sequence is proven only by the real staging run.

**Convergence.** The drain and enable pair is an intentionally changing operation and reports `changed` on every run. Convergence is judged on the `app_release` role's tasks only, which reported zero changes on the second run.

The plan is recorded with `templates/rollout-plan.md`. The Thursday run is handed to the on-call operator with `templates/handoff.md`: exact commands, the stop conditions (any failed host, any health check timeout, any unexpected host in the recap), and the recaps to send back.

## Completion report

### Result

Prepared, unverified for production. The rollout plan and playbook ran for real in staging, including a second run. The production run is handed to the on-call operator for the change window and has not been executed.

### Evidence

| # | Check | Ran where | Kind | Status |
|---|---|---|---|---|
| 1 | Lint and syntax | local | structural | passed |
| 2 | Prod selection proof | local, static inventory | structural | passed: 8 app hosts, 2 lb hosts |
| 3 | Staging `--check --diff` | staging | dry run | passed, with the limits above |
| 4 | Staging real run | staging | real execution | passed |
| 5 | Staging second run | staging | real execution | passed: role tasks `changed=0` |
| 6 | Production run | — | real execution | not run: reserved for the change window |

- **Observed fact vs inference.** Observed: inventory graphs, list-hosts output, the staging recaps, and 4.11 available in the repository. Inferred: no schema migration in 4.12 (taken from the release notes, not verified), and that prod HAProxy uses the same socket path as staging (the configuration templates match, but no prod host was inspected).
- **Skipped check vs passed check.** The production run is not run. Nothing in this report counts it as passed.
- **Local validation vs remote proof.** The prod selection proof is local and shows which hosts will be targeted. It does not prove that prod hosts are reachable or that the prod load balancers accept admin-socket commands.
- **Dry run vs real execution.** Staging has both a dry run and two real runs. Production has neither.

### Changed files or proposal

| Path | Change | Status |
|---|---|---|
| `playbooks/app-release.yml` | rolling play with `serial: [1, 2]`, drain and enable delegation, health gate; `run_once` task moved to its own play | committed on branch `release/4.12-rollout` |
| `inventories/*/group_vars/app.yml` | `app_release_version: "4.12.0"` | committed on branch |
| Rollout plan and operator handoff | written from the templates | attached to the change record |

### Unresolved risks

- The prod HAProxy socket path is unconfirmed. If it differs, the first drain fails, which is safe but stops the rollout at the canary.
- Staging has one load balancer and prod has two. The two-LB loop has not been exercised against two real load balancers.
- "No schema migration" rests on the release notes.

### Next safe action

The on-call operator runs `ansible-playbook -i inventories/prod/hosts.yml playbooks/app-release.yml --list-hosts` in the window, confirms the eight expected hosts, then runs the play and sends back both recaps. The first batch changes only `app-01`.
