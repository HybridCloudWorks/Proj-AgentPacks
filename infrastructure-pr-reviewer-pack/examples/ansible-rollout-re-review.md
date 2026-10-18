# Worked example: re-review of an nginx TLS rollout after fixes

Synthetic walkthrough. The repository, SHAs, line numbers and command output are illustrative; nothing was run against real infrastructure.

- Prompt: `re-review-infrastructure-pull-request.prompt.md`
- Skills: `review-infrastructure-pr` (Re-review), `review-ansible-automation`, `verify-infrastructure-evidence`
- Outcome: Ready with conditions

## Request

> I pushed fixes for your three findings on PR #140 in `edge-proxies`. All conversations are resolved. Can you take another look?

## Previous review

At head `a1b2c3d` the review raised:

- **F-01 (High)** `roles/nginx/tasks/main.yml:12`: the template task replaced `/etc/nginx/nginx.conf` with no validation, and the play had no `serial`, so a bad template would restart nginx on all 40 edge proxies at the end of the play.
- **F-02 (Medium)** `roles/nginx/tasks/main.yml:19`: `ignore_errors: true` on a separate `nginx -t` command task hid validation failures.
- **F-03 (Medium)** `roles/nginx/templates/nginx.conf.j2:1`: a header comment rendered `{{ ansible_date_time.iso8601 }}`, so every run changed the file and notified the restart handler on every host.
- **Evidence gap (Medium):** no second-run idempotence evidence.

## Walkthrough

1. **Rebuild the ledger.** `change_manifest.py --base 3e0f9a1 --head d4e5f6a` covers the full PR, not just the fix commit: 4 files, 31 changed lines, 12 of them new since `a1b2c3d` (`templates/re-review-reconciliation.md` records both counts).
2. **F-01 at the new head.** The template task now reads:

   ```yaml
   - name: Render nginx main configuration
     ansible.builtin.template:
       src: nginx.conf.j2
       dest: /etc/nginx/nginx.conf
       owner: root
       group: root
       mode: "0644"
       validate: nginx -t -c %s
     notify: reload nginx
   ```

   `validate` runs against the rendered temporary file before it replaces the live one, and a failure leaves the old file in place. This works here for two reasons the reviewer checked: the task renders the complete main configuration, not a `conf.d` fragment that `nginx -t -c` could not parse on its own, and every `include` in `nginx.conf.j2` uses an absolute path, so includes still resolve when nginx reads the configuration from a temporary location. `playbooks/edge.yml` now sets `serial: "25%"` and `max_fail_percentage: 0`, so at most 10 proxies change per batch, handlers run at the end of each batch, and any failure stops later batches. Status: fixed.
3. **F-02 at the new head.** The separate `nginx -t` task and its `ignore_errors` are deleted; validation lives in the template task. Deleting the task removes no other control. Status: fixed.
4. **F-03 at the new head.** The header is now the static comment `# Managed by Ansible: roles/nginx`. Status: fixed. The resolved conversations were not counted as evidence; each status cites the code above.
5. **Newly changed lines (`review-ansible-automation`).** The handler changed from `state: restarted` to `state: reloaded`. Reload replaces worker processes gracefully instead of dropping connections, which suits a TLS certificate and cipher change. `max_fail_percentage: 0` aborts the remaining batches as soon as any host in a batch fails, which is the intended behavior for a fleet behind a load balancer. All 12 new lines verified.
6. **Evidence (`verify-infrastructure-evidence`).** `ansible-lint --offline` pass and `ansible-playbook playbooks/edge.yml --syntax-check` pass at `d4e5f6a`. The author attached Molecule output, but only the `converge` stage ran; the `idempotence` stage is not in the log. Earlier evidence from `a1b2c3d` no longer counts. No check mode was run against real proxies.

## Completion report

### Executive Summary

- Overall assessment: All three earlier findings are fixed in code; idempotence is still unproven.
- Highest-risk finding: None open.
- Reviewed transition: nginx main configuration and TLS settings on the edge proxy fleet, rolled out in 25% batches with reload.
- Release or merge readiness: Ready once the idempotence evidence is attached.

### Review Scope

- Base and head: `3e0f9a1` → `d4e5f6a` (previous review at `a1b2c3d`)
- Files and technologies: `playbooks/edge.yml`, `roles/nginx/tasks/main.yml`, `roles/nginx/handlers/main.yml`, `roles/nginx/templates/nginx.conf.j2` (Ansible)
- Entry points and execution order: `ansible-playbook -i inventories/prod playbooks/edge.yml` from the `deploy-edge` pipeline; template → validate → notify → reload per batch
- Targets, identities, state, and ownership: group `edge` in `inventories/prod` (40 hosts); controller identity `svc-ansible` with `become: true`; Ansible owns `/etc/nginx/nginx.conf`
- Evidence reviewed: Molecule converge log from `d4e5f6a`
- Constraints and exclusions: no access to proxies; no check mode against real targets

### Coverage and Evidence

- Changed lines: 31 / 31 (12 new since the previous review)
- Deletions, renames, generated artifacts, mode, or binary changes: the `nginx -t` command task deleted, its control moved into `validate`
- Cross-tool handoffs reviewed: none; Ansible only
- Existing-environment evidence: None beyond Molecule converge
- Missing or non-authoritative evidence: Molecule idempotence stage
- Earlier findings: F-01 fixed (`roles/nginx/tasks/main.yml:8-16`, `playbooks/edge.yml:4-5`); F-02 fixed (task deleted); F-03 fixed (`roles/nginx/templates/nginx.conf.j2:1`)
- Checks: `ansible-lint --offline` pass; `ansible-playbook --syntax-check` pass; Molecule converge (attached) pass; Molecule idempotence not run

### Findings Summary

`Critical: 0 · High: 0 · Medium: 0 · Low: 0 · Evidence gaps: 1`

### Findings

None.

### Evidence Gaps

```text
[Medium evidence gap] Provide a second-run idempotence result
Artifact: Molecule test output including the idempotence stage, or a second converge reporting changed=0
Commit: d4e5f6a
Inputs, target, identity: the default Molecule scenario with the prod group_vars for edge
Risk it resolves: whether any task still reports changed on every run and reloads nginx fleet-wide
```

### Residual Risk

No actionable defects found in the reviewed diff. Residual risk: fleet behavior still depends on the idempotence result above, and on the first production batch, which is the first run against real certificates.

### Disposition

Ready with conditions

### Handoff

- Required corrections: none.
- Suggested work order: attach the idempotence result; then request human approval.
- Validation required after fixes: Molecule idempotence stage at `d4e5f6a` reporting no changed tasks.
- Human decisions or approvals: approval of the production rollout window by the edge platform owners.
- Configuration and operational dependencies: re-review applies again if any further push changes the role.
