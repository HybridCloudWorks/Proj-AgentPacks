## Change contract

<!-- Given these inputs, identities, prior state, and targets, what must this PR change, and what must it never change? -->

## Technologies and execution order

<!-- Example: GitHub Actions -> Bicep -> PowerShell -> Ansible -> smoke test -->

- Technologies changed:
- Entry points:
- Execution order:
- Generated artifacts and consumers:

## Targets and identity

- Environments:
- Tenant/account/subscription/project:
- Region/resource group/cluster/namespace/inventory/workspace/state key:
- Deployment or configuration identity:
- Service connection / federation / runner:

## Lifecycle and ownership

- Creates:
- Updates:
- Replaces or restarts:
- Deletes, purges, detaches, or stops managing:
- Imports, adopts, moves, or transfers ownership:
- Shared or data-bearing resources affected:

## Validation evidence

<!-- Attach artifacts generated from this commit with the declared target and inputs. -->

- Format / parser / lint:
- Terraform/OpenTofu plan:
- Bicep/ARM build and what-if:
- PowerShell PSScriptAnalyzer / Pester:
- Ansible syntax / lint / limited check-diff / idempotence:
- Rendered Helm/Kustomize/Kubernetes output:
- Policy / security / dependency / secret scans:
- Pipeline or template validation:

## Failure and recovery

- Partial-failure behavior:
- Retry and rerun behavior:
- Concurrency or locking:
- Rollback or recovery procedure:
- Backup and restore evidence:
- Operator/owner:

## Security, availability, and cost impact

- Permissions / roles / service accounts:
- Secrets / sensitive output:
- Network exposure:
- Encryption / retention:
- Availability / capacity / quotas:
- Cost impact:

## Reviewer focus

<!-- Call out migrations, known limitations, expected destructive actions, and evidence gaps. -->
