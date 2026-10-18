---
name: terraform-state-backends-and-imports
description: Design and operate Terraform remote state, S3 and Azure Storage backends, locking, migrations, state recovery, Terraform Search, and safe imports.
---

# Terraform State, Backends, and Imports

Use this Skill whenever a task mentions state, backend, locking, S3, Azure Storage, azurerm backend, remote backend, Terraform Search, import, state migration, state mv, state rm, or force-unlock.

## Backend design

Choose a backend based on execution ownership, cloud boundary, access model, locking support, recovery, audit, and environment separation. Keep backend configuration free of long-lived secrets; use approved environment, workload identity, or secret-manager mechanisms.

- S3: use a dedicated bucket/key layout, versioning, least-privilege object access, and current S3 locking guidance. Treat legacy DynamoDB locking as compatibility material and verify the installed Terraform version before using it.
- Azure Storage: use a dedicated storage account and container, secure transport, identity-based access where supported, private network controls when required, soft delete/versioning or equivalent recovery, and lease-based locking behavior as documented for the installed azurerm backend.
- HCP Terraform or the remote backend: distinguish workspace state, local CLI workspaces, run permissions, state access, and remote execution. State can contain sensitive values even when configuration does not.

## Lock and recovery

Never disable locking to get past contention. Inspect the active run and owner first. Use force-unlock only for a lock you can prove is stale and only with the exact lock ID. Back up or rely on backend version history before state modifications. Do not expose state in chat, logs, artifacts, or commits.

## Import and search

Confirm provider support and resource identity format before discovery. Prefer declarative import blocks when imports should be repeatable or reviewed; CLI import only binds an existing object to an address and does not author complete configuration. Ensure each remote object maps to one address. Review generated configuration, clean it into a maintainable module interface, run plan, and reconcile drift before apply.

For Terraform Search, verify the installed Terraform version and provider-supported list resources. Treat generated configuration as a draft. Use provider-native discovery or a narrow manual import path when Search does not support the resource.

## Migration gate

Record source and destination backend, state identity, lock behavior, credentials, backup/recovery, workspace mapping, expected serial/lineage, and rollback. Run migration with explicit authorization and reinitialize only in the intended configuration directory.
