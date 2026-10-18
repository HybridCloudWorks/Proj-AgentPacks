# Worked example: local state to an S3 backend, blocked before migration

Prompt: `migrate-terraform-state.prompt.md`. Skills: terraform-state-backends-and-imports, terraform-core-and-style.

This is a synthetic walkthrough. The bucket, account and identities are illustrative. Commands and outputs show what the agent would run and see; they are not results recorded by this pack's validation. This example shows a blocked outcome: the migration is prepared, and it does not run.

## Request

> The `payments` root still uses local state on my laptop. Move it to S3 with locking. The platform team's bucket is `example-tfstate-prod` in eu-west-1.

The request asks for the migration. It does not name an approver or a change window for writing production state, and the bucket belongs to another team. The agent treats design and preparation as authorized, and treats the state write as still needing explicit authorization.

## 1. Establish the contract

- `envs/payments` has no backend block, so Terraform uses the local backend. `terraform.tfstate` is git-ignored.
- `required_version` and the installed CLI agree. The S3 backend documentation for the installed version describes lockfile-based locking (`use_lockfile`). The team wiki's DynamoDB lock table is legacy compatibility material, and the agent does not add it.
- The CI workflows do not run this root, so the laptop copy is the only writer. The user confirms there are no other copies.
- The root manages an `aws_db_instance` with a master password. The state therefore holds that password in plain text. The destination must be encrypted, and readable only by the people who run this root.

State identity, selecting only non-sensitive fields:

```text
$ terraform state pull | jq '{serial, lineage}'
{ "serial": 214, "lineage": "3f9c2e1a-…" }
$ terraform state list | wc -l
37
```

## 2. Check the destination with the identity that would migrate

```text
$ aws sts get-caller-identity --query Arn
"arn:aws:sts::111122223333:assumed-role/payments-admin/…"
$ aws s3api head-bucket --bucket example-tfstate-prod
(exit 0)
$ aws s3api list-objects-v2 --bucket example-tfstate-prod --prefix payments/ --max-items 1
(exit 0, no objects: the key is free)
$ aws s3api get-bucket-versioning --bucket example-tfstate-prod
An error occurred (AccessDenied) when calling the GetBucketVersioning operation
(exit 254)
$ aws s3api get-bucket-encryption --bucket example-tfstate-prod
An error occurred (AccessDenied) when calling the GetBucketEncryption operation
(exit 254)
```

The bucket exists and the key is free. The identity cannot see whether versioning or default encryption is on. Without versioning, an overwritten or deleted state object can be recovered only from the local copy.

## 3. Prepare, on a branch

```hcl
# envs/payments/backend.tf
terraform {
  backend "s3" {
    bucket       = "example-tfstate-prod"
    key          = "payments/prod/terraform.tfstate"
    region       = "eu-west-1"
    encrypt      = true
    use_lockfile = true
  }
}
```

The block holds no credentials; the identity comes from `AWS_PROFILE` at run time. The change stays on a branch. Once it merges, anyone who runs `terraform init` in this directory is prompted to migrate.

The agent fills in the state migration record (excerpt):

| Field | Value |
|---|---|
| Source | local, `envs/payments/terraform.tfstate`, serial 214, lineage `3f9c2e1a-…`, 37 resources |
| Destination | S3 `example-tfstate-prod`, key `payments/prod/terraform.tfstate`, owned by the platform team |
| Locking | lockfile next to the state key, as documented for the installed version |
| Credentials | `payments-admin` role via profile; no keys in configuration |
| Minimum permissions | `s3:ListBucket` on prefix `payments/`; `s3:GetObject` and `s3:PutObject` on the state key; `s3:GetObject`, `s3:PutObject` and `s3:DeleteObject` on the lock object |
| Backup | encrypted copy from `terraform state pull`, held by the user outside the repository until verification passes |
| Destination recovery | **unknown**: versioning not readable |
| Encryption at rest | **unknown**: default encryption not readable; `encrypt = true` covers the object Terraform writes |
| Expected after | serial 214, lineage `3f9c2e1a-…`, 37 resources, plan shows no changes |
| Rollback | before verification: remove the backend block and keep using the local file. After: `terraform init -migrate-state` back to local from the S3 object, or restore the backup |

## 4. Stop

The migration gate is not met:

1. **Recovery is unverified.** The skill requires backup or recovery before a state write, and versioning on the destination cannot be read.
2. **Encryption is unverified** for a state that holds a database password.
3. **The state write is not authorized.** There is no approver and no change window for production state.

`terraform init -migrate-state` was not run. The agent prepares an approval handoff for the migration, and hands it over with the two questions for the platform team.

## Completion report

Outcome: blocked. Migration prepared on a branch; state not moved.

### objective

Move the `payments` root's state from the local backend to S3 with locking.

### scope_and_authorization

| Item | Value |
|---|---|
| Configuration directory | `envs/payments` |
| Environment | prod, account 111122223333 (synthetic), eu-west-1 |
| Terraform | installed version matches `required_version` |
| Backend | local, moving to S3 `example-tfstate-prod` |
| Authorization | design and preparation, from the request |
| Not authorized | `terraform init -migrate-state` (a production state write with no approver or window) |

### changed_files

| File | Change |
|---|---|
| `envs/payments/backend.tf` | new S3 backend block on branch `state/payments-s3`; not merged |

### commands_and_results

| Command | Directory | Exit | Result |
|---|---|---|---|
| `terraform state pull \| jq '{serial, lineage}'` | `envs/payments` | 0 | serial 214, lineage recorded |
| `terraform state list \| wc -l` | `envs/payments` | 0 | 37 |
| `aws sts get-caller-identity` | n/a | 0 | `payments-admin` role |
| `aws s3api head-bucket` | n/a | 0 | bucket reachable |
| `aws s3api list-objects-v2 --prefix payments/` | n/a | 0 | key free |
| `aws s3api get-bucket-versioning` | n/a | 254 | AccessDenied |
| `aws s3api get-bucket-encryption` | n/a | 254 | AccessDenied |

Not run: `terraform init -migrate-state`, the post-migration plan, and the lock test against S3.

### plan_or_state_impact

No state written. Local state remains at serial 214. No plan was run, because the configuration did not change apart from the backend.

### evidence_classification

| Claim | Class | Evidence |
|---|---|---|
| State identity and size | local | `state pull` and `state list` on the local backend |
| Bucket exists and the key is free | live-cloud | `head-bucket`, `list-objects-v2` |
| Versioning and default encryption | unavailable | AccessDenied for `payments-admin` |
| Lockfile locking works for this bucket and role | unavailable | not exercised before migration |
| State holds a database password | static | `aws_db_instance.password` in configuration |
| The laptop copy is the only writer | inferred | CI does not run this root; the user confirmed no other copies |

### risks_and_limitations

Until the migration runs, the local file is the only copy of production state, on one laptop. That is a standing risk, so this should not wait long. The S3 permission list is the minimum the agent derived; the platform team may require more, such as KMS permissions for a customer-managed key.

### next_safe_action

The platform team confirms versioning and default encryption on `example-tfstate-prod`, or grants `payments-admin` read access to those settings, and applies the scoped object permissions. The requester then names an approver and a window, and authorizes `terraform init -migrate-state` in `envs/payments` through the approval handoff.
