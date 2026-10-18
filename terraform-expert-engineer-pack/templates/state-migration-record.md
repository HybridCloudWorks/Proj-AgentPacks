# State migration record

Use before any backend change or state migration. It holds the fields the terraform-state-backends-and-imports Skill requires before a migration may run: source and destination backend, state identity, lock behaviour, credentials, backup and recovery, workspace mapping, expected serial and lineage, and rollback. Fill everything in before asking for authorization. Leave a field blank and the migration is blocked; that is the point of the record.

## Backends

| Item | Source | Destination |
|---|---|---|
| Backend type (local, s3, azurerm, HCP Terraform or remote) | | |
| Location (bucket and key, account and container and key, organization and workspace) | | |
| Owner of the storage | | |
| Locking mechanism, as documented for the installed Terraform version | | |
| Encryption at rest and in transit | | |
| Versioning, soft delete or state history | | |
| Network controls | | |

Backend blocks hold no access keys, SAS tokens or client secrets. Credentials come from the run-time identity.

## State identity

| Item | Before | Expected after |
|---|---|---|
| Serial | | same as before |
| Lineage | | same as before |
| Resource count (`terraform state list`) | | same as before |
| `terraform_version` recorded in state | | |

Taken from `terraform state pull`, selecting only these fields. Never paste state contents.

## Workspace mapping

| CLI workspace | Destination key or HCP workspace |
|---|---|

## Identity and access

- Identity that runs the migration, and how it authenticates:
- Permissions it needs at the destination, at minimum:
- Who else can read the destination state (state can hold secrets even when configuration does not):

## Locks

- Current lock holder, if any, and its run:
- How the destination lock was tested, or why it could not be:

## Backup and recovery

- Backup of the source state: location, encryption, who can read it, when it is deleted:
- Recovery from the destination: version history or soft delete, and who can restore:

## Pre-checks

| Check | Command | Result | Evidence class |
|---|---|---|---|

## Migration steps

Exact commands, in order, with the directory each runs in. The usual core is `terraform init -migrate-state` in the configuration directory, with the backend change committed on a branch.

## Verification

- Serial and lineage after migration match the record.
- `terraform plan` shows no changes.
- The destination lock is taken and released by a plan.

## Rollback

How to return to the source backend, and the point after which rollback means restoring from backup.

## Authorization

- Approver, change window, and the approval handoff reference:
- Status: prepared / authorized / migrated and verified / rolled back
