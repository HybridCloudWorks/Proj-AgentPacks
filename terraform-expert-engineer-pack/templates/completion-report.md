# Terraform completion report

Use at the end of every task. The eight sections, their names and their order come from the always-on `terraform-expert-engineer-contract` instruction, which is what an installed agent actually follows; this file is the human-readable form. Keep every section. Where one has nothing to say, write "none" and why.

Open with one line of outcome in plain words, for example: "Done and verified by plan", "Prepared; apply not authorized", "Blocked: recovery evidence for the destination backend is missing".

## objective

What was asked, in one or two sentences, and what was delivered against it.

## scope_and_authorization

| Item | Value |
|---|---|
| Configuration directories (root or child) | |
| Environment, account or subscription, region | |
| Terraform CLI: installed version and `required_version` | |
| Providers and versions (from `.terraform.lock.hcl`) | |
| Backend and state key, or HCP Terraform workspace or Stack | |
| Execution mode (local CLI, CI, HCP remote run) | |
| Authorization given, by whom, and its limits | |
| Requested actions that were not authorized | |

## changed_files

| File | Change |
|---|---|

Write "none" for a review or diagnosis.

## commands_and_results

| Command | Directory | Exit | Result |
|---|---|---|---|

List the commands that were not run, and why, under the table. A command that did not run is never reported as passed.

## plan_or_state_impact

- Plan counts: to import, to add, to change, to destroy; moved addresses.
- Every replace and destroy, by address, with its cause.
- Provider and lock-file changes.
- State addresses added, moved or removed.
- Sensitive values present in the plan or state, named by address and never printed.
- Policy and run-task results, with enforcement level.
- Whether state was written, with serial before and after when it was.

## evidence_classification

| Claim | Class | Evidence |
|---|---|---|

Classes:

- **static**: read from source, diffs or documentation; nothing executed.
- **local**: a command run on this machine that read no live cloud, backend or HCP state, such as `fmt`, `validate`, `init -backend=false`, mocked tests or `go test`.
- **live-cloud**: a command or API call that read or changed a real cloud account, a remote backend or HCP Terraform, such as `plan` with refresh, `state list` against a remote backend, a cloud CLI query or retrieved run history.
- **inferred**: concluded from evidence but not observed directly.
- **unavailable**: could not be obtained; say what blocked it.

Apply, lock, policy enforcement, HCP behaviour, AVM certification and provider acceptance are claimed only with live-cloud or retrieved evidence.

## risks_and_limitations

What remains unverified, what could go wrong next, and what each check did not prove.

## next_safe_action

One action: who performs it, the exact command or step, and the authorization it needs.

## Redaction check before sending

- [ ] No state contents, plan values, credentials, sensitive variables or backend secrets.
- [ ] Account, subscription and tenant IDs shortened or replaced where the reader does not need them.
- [ ] Plan excerpts trimmed to addresses and actions.
