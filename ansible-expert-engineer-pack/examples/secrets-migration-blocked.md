# Worked example: plaintext secrets migration, blocked

Prompt: `secure-ansible-secrets.prompt.md`. Skills: `ansible-vault-secrets`, `ansible-inventory-and-variable-design`, `ansible-validate-content`.

Synthetic scenario. Paths and variable names are illustrative. No secret value appears anywhere in this walkthrough, and none appeared in the agent's output.

## Request

> Our prod group_vars still have the DB password and the SMTP token in plain text. Move them into Vault and make CI work with it. Go ahead and change the repo on a branch.

Authorization in scope: repository edits on a branch. Not authorized, and not requested: rotating credentials, changing CI secret settings, rewriting Git history.

## 1. Locate without printing values

The search prints file, line and key name only. The `awk` split drops everything after the YAML key's colon, so values never reach the terminal.

```text
git grep -nE '^\s*[A-Za-z_]*(password|passwd|token|secret|api_key)[A-Za-z_]*\s*:' -- inventories roles \
  | awk -F: '{print $1":"$2":"$3}'
```

```text
inventories/prod/group_vars/all.yml:12:db_password
inventories/prod/group_vars/all.yml:13:smtp_api_token
roles/app/defaults/main.yml:9:db_password
```

The role default on line 9 is an empty string, not a secret. History is checked by commit list only, with no patch output: `git log --oneline -S db_password -- inventories/prod`. Both production values have been in Git history for about 14 months.

Exposure paths found while reading, again without printing values:

- `roles/app/templates/app.env.j2` renders `DB_PASSWORD={{ db_password }}`. The task deploying it has no `diff: false`.
- The CI pipeline file runs `ansible-playbook ... --check --diff` on every pull request. So the rendered value can appear in CI job logs. The agent has no access to those logs, so whether it did appear is **not verified**.
- `roles/app/tasks/db_user.yml` registers the result of a `community.postgresql.postgresql_user` task with no `no_log`.

## 2. Rotation comes first

Both values may have been exposed through Git history and possibly CI logs. Encrypting them now does not revoke what was already readable, so the skill's migration rule applies: **rotate**. Rotation is a secret change. It needs the secret owners and explicit authorization. The user does not know who owns the SMTP token, and the DBA team owns the database credential. The agent does not rotate anything and does not rewrite history. Rewriting history would not revoke the values either.

## 3. Prepared changes

Layout, following the skill's public/encrypted split with a production Vault ID:

```text
inventories/prod/group_vars/all/vars.yml     # public; was all.yml
inventories/prod/group_vars/all/vault.yml    # encrypted with --vault-id prod; NOT CREATED, see below
```

```yaml
# inventories/prod/group_vars/all/vars.yml (secret-bearing lines only)
db_password: "{{ vault_db_password }}"
smtp_api_token: "{{ vault_smtp_api_token }}"
```

Moving `all.yml` into an `all/` directory keeps the same group scope and precedence. The agent confirms this with `ansible-inventory -i inventories/prod/hosts.yml --host app-01`, which still lists every non-secret variable. It shows the two secret variables as their unrendered `{{ vault_... }}` references.

Output protection:

```yaml
# roles/app/tasks/main.yml
- name: Render application environment file
  ansible.builtin.template:
    src: app.env.j2
    dest: /etc/app/app.env
    owner: root
    group: app
    mode: "0640"
  diff: false
  no_log: true

# roles/app/tasks/db_user.yml
- name: Ensure application database user
  community.postgresql.postgresql_user:
    name: app
    password: "{{ db_password }}"
  no_log: true
```

Proposed CI password delivery: the pipeline passes `--vault-id prod@/run/secrets/ansible-vault-prod`, a file mounted by the CI secret store at job start. No password file is committed, and `ansible.cfg` gains no `vault_password_file` pointing into the repository.

## 4. Why the agent stops here

Creating `vault.yml` needs the production vault password. The skill forbids asking for it in chat, and no out-of-band channel has been supplied: there is no CI secret yet and no runner-mounted file. Even if the agent chose a password itself, it would be outside the secret owner's control. So:

- `vault.yml` is **not created**. The branch is not mergeable: any play that uses `db_password` would fail on an undefined `vault_db_password`.
- Decryption cannot be validated.
- `--check --diff` is not run, because it would fail on the undefined variable and prove nothing about the migration.

## Completion report

### Result

Blocked. The public variable layout, output protection and CI design are prepared on branch `secrets/prod-vault`. The work is blocked on three inputs: a production vault password delivered out of band, the secret owners for rotation, and authorization to rotate. The branch must not be merged until `vault.yml` exists.

### Evidence

| # | Check | Ran where | Kind | Status |
|---|---|---|---|---|
| 1 | Key-only secret search, working tree and history | local | structural | passed: 2 production secrets located, values not printed |
| 2 | `ansible-lint` on changed files | local | structural | passed |
| 3 | `ansible-playbook --syntax-check playbooks/site.yml` | local | structural | passed; this does not resolve variables, so it says nothing about the undefined vault names |
| 4 | `ansible-inventory --host app-01` after the move | local, static inventory | structural | passed: scope unchanged; secrets show as references |
| 5 | Vault decryption with the `prod` ID | — | local test | not run: no vault password supplied |
| 6 | `--check --diff` | — | dry run | not run: would fail on the undefined variables |
| 7 | CI log review for leaked values | — | — | not run: no access |

- **Observed fact vs inference.** Observed: the two plaintext keys, their age in history, the template task without `diff: false`, and the CI job that runs `--diff`. Inferred: that CI logs may contain the rendered database password. That follows from the job and the template, but no log was inspected.
- **Skipped check vs passed check.** Checks 5 to 7 did not run, and none is counted as passed. The passing syntax check does not cover them.
- **Local validation vs remote proof.** Every check ran locally. Nothing shows the new layout works on a host, or that CI can read the mounted vault file.
- **Dry run vs real execution.** No dry run and no real execution happened. The plaintext values remain in effect in `main` until the branch merges.

### Changed files or proposal

| Path | Change | Status |
|---|---|---|
| `inventories/prod/group_vars/all.yml` to `all/vars.yml` | moved; secret lines now reference `vault_` names | committed on branch |
| `inventories/prod/group_vars/all/vault.yml` | encrypted secret values | **not created**: blocked |
| `roles/app/tasks/main.yml` | `diff: false` and `no_log: true` on the env template | committed on branch |
| `roles/app/tasks/db_user.yml` | `no_log: true` | committed on branch |
| CI pipeline | `--vault-id prod@/run/secrets/ansible-vault-prod` | proposed only; needs the CI secret created |

### Unresolved risks

- Both production values must be treated as exposed until they are rotated. This is the most important risk, and migration alone does not remove it.
- CI logs from past pull requests may hold the database password. Someone with CI admin access must review and purge them.
- The output-protection changes are on the branch, not in `main`, so every pull request run still prints the template diff.

### Next safe action

The user names the owners. The DBA team rotates the database credential and the SMTP owner rotates the token. One of them creates the CI secret file and sends the new values straight into `ansible-vault create --vault-id prod@prompt inventories/prod/group_vars/all/vault.yml` on their own workstation. The agent then validates decryption with the password supplied out of band. As an interim step, the agent can split the two `roles/app/tasks` changes into their own pull request. Those changes do not depend on `vault.yml`, and merging them stops further leakage through CI logs today.
