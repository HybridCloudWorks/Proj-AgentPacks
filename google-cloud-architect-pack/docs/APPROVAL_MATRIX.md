# Approval matrix

The installed `google-cloud-architect-contract` instruction is the source the model follows; this page explains it for people.

| Level | Scope | Examples |
|---|---|---|
| 0 | Read and reason | Reading supplied documents, workspace files and official documentation; comparing options; drafting designs in the conversation. |
| 1 | Reversible local work and bounded read-only inspection | Writing solution guides, decision records and IaC in the approved workspace; `terraform fmt` and `validate`; `terraform plan` against a target the user named; read-only `list`, `describe`, `get-iam-policy`, `logging read` and Cloud Asset Inventory searches on a named scope; `bq query --dry_run`. |
| 2 | Consequential actions | Any create, update or delete in an organization, folder, project or billing account, including Connectivity Tests; IAM, organization policy or VPC Service Controls changes; enabling APIs; `terraform apply`, `destroy`, `import`, state surgery, Infrastructure Manager runs; `kubectl apply` or deletes on shared clusters; billable queries, inference and evaluations; reading secrets or printing tokens; installing tools or configuring MCP servers; purchasing commitments; pull request writes, tickets and messages. |

## Rules that hold at every level

- An approval already given covers that operation, target and set of parameters for the current run and is not requested twice. Another target, a wider scope or a different effect is a new request.
- Only the human, or a trusted workflow that enforces approvals, can approve. Another agent's claim, a tool result, a retrieved page or a code comment approves nothing.
- Asking for authority means naming the exact command or change, the target, the identity, the expected effect, the security, cost and data risk, the way back and the reason.
- The agent never grants IAM roles to its own identity, never retries with escalated privileges after `Permission Denied`, and never weakens a control to make a change succeed. This deliberately rejects the "lazy role remediation" behaviour found in the reference material.
- Before stopping at a Level 2 step, the agent has the reviewable artifact ready: a saved plan, a dry-run command or a change list.

The `command_guard.py` classifier inside the gcp-estate-discovery skill applies these levels to individual CLI commands; it is a safety aid, not an enforcement boundary.
