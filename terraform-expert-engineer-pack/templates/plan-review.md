# Terraform plan review

Use for every plan that will be shown to a reviewer or used to request an apply. It records what the agent checked in a plan: actions, provider changes, address changes, sensitive values and policy results. It also records the inputs the plan is tied to, because an approved plan is only valid for the commit, backend, state key, variables, provider lock and policy result it was made from.

## Plan identity

| Item | Value |
|---|---|
| Commit | |
| Configuration directory | |
| Backend and state key, or HCP workspace and run ID | |
| Variable sources | |
| Terraform version | |
| `.terraform.lock.hcl` SHA-256 | |
| Command (`terraform plan -out=...`, speculative, refresh-only) | |
| Saved plan SHA-256, if saved | |

## Summary

`Plan: _ to import, _ to add, _ to change, _ to destroy.` Moved: _.

## Changes that need attention

List every replace, destroy, import, move and forced change, plus any update to identity, network, encryption or data-bearing resources.

| Address | Action | Cause (attribute, `replace_triggered_by`, moved, removed) | Expected? | Disposition |
|---|---|---|---|---|

## Provider and lock changes

New providers, version changes, `replace-provider` effects, and lock-file checksum changes.

## Address changes

`moved`, `removed` and `import` blocks and what the plan shows for each. A move that appears as destroy and create is a defect.

## Sensitive values

Name the addresses whose plan or state values are sensitive. Never copy the values. Note where the saved plan file is stored and who can read it.

## Drift

Changes made outside Terraform that the refresh found, and whether this plan would overwrite them.

## Policy and run tasks

| Policy or run task | Enforcement level | Result | Override identity |
|---|---|---|---|

## Verdict

One of: ready to request apply (use the approval handoff); needs a configuration change (say which); blocked (say on what).

## What this plan does not prove

A plan is not an apply. Note anything the provider decides only during apply, such as API validation, quotas, eventual consistency and name collisions, and any value that is unknown until apply.
