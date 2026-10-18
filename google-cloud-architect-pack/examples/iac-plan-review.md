# Worked example: reviewing a Terraform plan before apply

Synthetic scenario for the `validate-iac.prompt.md` workflow.

## Request

"Check this Terraform before I apply it to `billing-prod`." The user provided the root module, named the project and authorized `plan` with their own credentials. They did not authorize `apply`.

## Steps and evidence

| Command | Target | Exit code | Result |
|---|---|---|---|
| `terraform fmt -check -recursive` | local workspace | 0 | passed |
| `terraform init -backend=false` then `terraform validate` | local workspace | 0 | passed |
| `terraform plan -input=false -out=tfplan` | billing-prod (remote state) | 0 | 3 to add, 2 to change, 1 to replace, 1 to destroy |
| `terraform show -json tfplan > tfplan.json` then `python scripts/plan_summary.py tfplan.json` (from the gcp-iac-validation skill) | local file | 1 | Critical and High risks found |

Each command was rated by the gcp-estate-discovery classifier first: all Level 1.

## Plan summary (excerpt)

| Severity | Address | Reason |
|---|---|---|
| Critical | `google_sql_database_instance.ledger` | replace of a stateful resource: the `region` argument changed, which forces a new instance |
| High | `google_project_iam_policy.billing` | authoritative IAM policy would remove every binding not in the code, including service agents |
| High | `google_compute_firewall.debug` | ingress from 0.0.0.0/0 on port 22 |
| High | `google_project_service.sqladmin` | API disabled on destroy |

## Response to the user

The agent explained that the database replacement would create an empty instance in a new region and delete the existing one, recommended reverting the region change and planning a migration instead, recommended `google_project_iam_member` resources in place of the authoritative policy, IAP TCP forwarding instead of the open SSH rule, and `disable_on_destroy = false` on the API resource. It did not apply, and noted that a clean plan would still not prove that IAM, quotas or organization policies allow the apply.

Status CHANGES_REQUIRED.
