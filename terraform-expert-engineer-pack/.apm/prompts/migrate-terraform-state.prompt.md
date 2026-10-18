---
description: "Design a Terraform backend and prepare a gated state migration to S3, Azure Storage or HCP Terraform"
agent: terraform-expert-engineer
---

# Migrate Terraform state to a new backend

## Inputs

- Source and destination backend, the configuration directory and the CLI workspaces involved.
- The identity that will run the migration and how it authenticates, with no static keys in the backend block.
- The destination's locking, versioning or soft delete, encryption and network controls, as far as they can be read.
- Who authorizes the migration and in which change window.

## Workflow

1. Apply terraform-state-backends-and-imports to design the backend from execution owner, cloud boundary, access model, locking, recovery, audit and environment separation.
   - S3: dedicated bucket and key layout, versioning, least-privilege object access, and the S3 locking documented for the installed Terraform version. Treat DynamoDB locking as legacy compatibility, used only after checking the installed version.
   - Azure Storage: dedicated account and container, secure transport, identity-based access where supported, private network controls when required, soft delete or versioning, and lease-based locking as documented for the installed `azurerm` backend.
   - HCP Terraform or the remote backend: map CLI workspaces to HCP workspaces with terraform-cloud-and-stacks, and confirm who can read state there.
2. Check locks before anything else. Never disable locking. If a lock is held, identify its owner and active run; propose `force-unlock` only for a lock proven stale, with its exact lock ID, and only with authorization.
3. Fill the migration record: source and destination, state identity (serial and lineage), lock behaviour, credentials mechanism, backup or version history, workspace mapping, expected serial and lineage after migration, and rollback.
4. Prepare the backend configuration. Stop and ask before `terraform init -migrate-state` or any state write. Missing recovery evidence or missing access is a blocker to report, not a reason to proceed.
5. After an authorized migration, initialize only in the intended directory, confirm serial and lineage, and confirm that a plan shows no changes.

Do not print state, keys or backend secrets; quote only serial, lineage and addresses.

## Expected output

The backend configuration diff; the completed migration record; the pre-checks and their results; the exact authorization requested; after an authorized run, the verification results; and a completion report that states whether state was moved. Follow the `terraform-expert-engineer-contract` instruction.
