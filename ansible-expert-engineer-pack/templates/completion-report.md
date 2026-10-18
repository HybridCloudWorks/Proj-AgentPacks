# Completion report

Use this at the end of every task. The five sections and four distinctions come from the always-on `ansible-expert-engineer-contract` instruction; this template only gives them a fixed shape. Never describe an unexecuted check as passed.

## Result

One or two sentences: what was delivered and its status, using one of these plain words:

- **verified locally**: every listed check ran and passed, and nothing beyond local or fixture evidence is claimed.
- **verified on approved target**: the change also ran for real on a named disposable or approved host, including a second, convergence run.
- **prepared, unverified**: content exists but at least one required check was skipped or could not run.
- **blocked**: the work cannot proceed without a named input, approval or owner.

State the scope: repository paths, inventory, environment and hosts.

## Evidence

| # | Check | Command (secrets redacted) | Ran where | Kind | Status | What it shows |
|---|---|---|---|---|---|---|
| 1 | Lint | `ansible-lint` | local | structural | passed / failed / skipped / not run | |
| 2 | Syntax | `ansible-playbook --syntax-check ...` | local | structural | | |
| 3 | Inventory and selection | `ansible-inventory ... --graph`, `--list-hosts` | local (static inventory) | structural | | |
| 4 | Dry run | `ansible-playbook ... --check --diff --limit ...` | approved host name | dry run | | |
| 5 | Real run | `ansible-playbook ... --limit ...` | approved host name | real execution | | |
| 6 | Convergence | same command, second run | approved host name | real execution | | `changed=0` expected unless the task is intentionally changing |

Kind is one of: structural, local test, dry run, real execution. Remove rows that do not apply; never remove a row only because the check was skipped. Write the reason in "What it shows".

Then state each distinction explicitly:

- **Observed fact vs inference.** List what was seen in command output or files. List separately what is inferred from it, and why.
- **Skipped check vs passed check.** Name every skipped or unavailable check and the reason (tool missing, no approved target, not authorized).
- **Local validation vs remote proof.** Say what local checks cannot prove here: reachability, target state, authorization, production safety.
- **Dry run vs real execution.** Say whether anything executed for real, where, and which modules do not fully support check or diff mode.

## Changed files or proposal

| Path | Change | Status |
|---|---|---|
| | added / modified / proposed only | committed on branch / uncommitted / not written |

Note intentional deviations from the source or the request, and decisions the user must accept.

## Unresolved risks

Each risk with its impact and the evidence that would close it. Include assumptions that were not confirmed.

## Next safe action

The single smallest next step, who must take it, and the exact command or decision, with what it may change. If the next step needs authorization, say whose.
