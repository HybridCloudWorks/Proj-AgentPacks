---
name: gcp-iac-validation
description: "Structure, review and validate Google Cloud infrastructure code in Terraform or OpenTofu - module and state layout, provider pinning, Google-specific review rules for IAM, exposure, encryption and deletion, static checks, policy validation, plan-only validation with a risk summary, drift detection and CI design. Use when writing, reviewing or checking Google Cloud Terraform, reading a plan before apply, or designing an infrastructure pipeline."
---

# Google Cloud Infrastructure-as-Code Validation

## Purpose and activation

Catch the change that would delete a database, open a port to the internet or hand out Owner before anyone runs `apply`, and make infrastructure changes reviewable and repeatable. Activate when Google Cloud Terraform or OpenTofu is written or reviewed, when a plan needs reading, or when an infrastructure delivery pipeline is designed.

## Scope and exclusions

In scope: repository and module structure, state backend design, provider and module pinning, review rules, static and policy checks, plan generation against a named target, plan risk analysis, drift detection, Infrastructure Manager and CI pipeline design. Out of scope: `apply`, `destroy`, `import`, state surgery and lock removal, which are Level 2; non-Google providers beyond their interaction with Google resources.

## Inputs

The root module and modules, variable files (without secrets), backend configuration, the target project or environment and the identity for planning, the design the code implements, and the organization's policy library if one exists.

## Dependencies and tools

Terraform or OpenTofu already installed, the `google` and `google-beta` providers, and optional tools only if already present (tflint with the Google ruleset, a policy engine, an IaC scanner); this skill never installs tools. `scripts/plan_summary.py` in this skill folder reads `terraform show -json` output and reports risky changes offline (Python 3.10 or later, standard library only). Vetted module sources: Google's Cloud Foundation Toolkit modules (`terraform-google-modules`) and Cloud Foundation Fabric.

## Workflow

1. Structure: one root module per environment and stage (foundation stages, network, project factory, workloads), shared modules versioned by tag, a state bucket in a dedicated project with versioning, uniform bucket-level access and narrow access, and a separate state per root module. Pin `required_version`, providers and modules.
2. Review the code against these rules:
   - IAM: `_member` adds one binding; `_binding` is authoritative for one role; `_policy` replaces the whole policy and can remove existing owners and service agents. Flag `google_project_iam_policy`, `google_folder_iam_policy` and `google_organization_iam_policy` unless the module truly owns the policy. Flag basic roles, `allUsers`, `allAuthenticatedUsers` and `google_service_account_key`.
   - Exposure: firewall rules with `0.0.0.0/0` sources, Cloud Run ingress set to all traffic, public IPs on Cloud SQL or VMs, buckets without public access prevention.
   - Data safety: `deletion_protection` on databases and clusters, `prevent_destroy` lifecycle on irreplaceable resources, backups and point-in-time recovery, CMEK settings, location values that satisfy residency.
   - Lifecycle: `google_project_service` with `disable_on_destroy = false` so removing code does not disable an API in use; resources whose changes force replacement (for example cluster networking fields).
   - Hygiene: labels on every resource, typed and described variables, no secrets in variables, outputs or locals, sensitive outputs marked.
3. Static checks: `terraform fmt -check -recursive`, then `terraform init -backend=false` and `terraform validate` for an offline syntax and schema check; tflint and the policy engine if installed. Google's Terraform policy validation (`gcloud beta terraform vet` with a constraint library) checks a plan against organization rules where available; confirm the command exists with `gcloud help` first.
4. Plan, only against a target the user named and with the identity they provided: `terraform init`, then `terraform plan -input=false -out=tfplan`, then `terraform show -json tfplan > tfplan.json`, then `python scripts/plan_summary.py tfplan.json`. Planning reads live resources and takes the state lock; it does not change resources, but data sources and external programs in the code can run, so read the code first.
5. Read the plan: list deletes and replacements first, then IAM and policy changes, then exposure changes, then everything else. Any delete or replace of a stateful resource is a blocking finding until the user confirms it is intended and a backup exists.
6. Drift: `terraform plan -refresh-only` shows changes made outside the code; report drift rather than overwriting it.
7. Pipeline design: plan on every pull request with the plan output attached; apply only from the main branch after human approval of that exact plan; separate identities for plan (read-mostly) and apply (write), both through Workload Identity Federation with attribute conditions pinned to the repository and branch; Infrastructure Manager as a managed option for Terraform runs.

## Output

Findings in the contract's format with file and line locations, the plan summary (counts of creates, updates, replacements and deletes; the list of risky changes), commands run with targets and exit codes, drift report, and what the plan cannot prove: IAM permission sufficiency at apply time, quota availability, organization policy denials, and runtime behaviour.

## Validation

`fmt` and `validate` pass; `scripts/plan_summary.py` reports no unacknowledged Critical or High risk; every delete or replace has an explicit user confirmation; every finding has a location and a recommendation. A plan is evidence of intended changes only, never of a successful apply.

## Failure handling and escalation

No credentials or no named target: run offline checks only and report PREPARED_NOT_VERIFIED with the fallback sentence. Plan fails with permission errors: report the missing permissions; do not switch identities or grant roles. State lock held by someone else: stop and report; never force-unlock. Plan shows unexpected replacements: stop and explain the attribute that forces replacement.

## Permissions and guardrails

Writing and editing code in the approved workspace and offline checks are Level 1; `plan` against a named target with the user's identity is Level 1; `apply`, `destroy`, `import`, `state rm`, `state mv`, `force-unlock`, Infrastructure Manager deployments and previews are Level 2. Never accept or create service account key files for planning. Without the pack's contract installed, treat every apply or state operation as needing explicit approval.

## Connection to the pack

The optional `validate-iac.prompt.md` recipe runs this skill; gcp-security-reviewer reads its plan summaries for independent review; gcp-solution-architecture and gcp-landing-zone use it for deployment guidance. Installed on its own, this skill still works and the guardrails above still apply. Installed with the pack, it follows the always-on `google-cloud-architect-contract` instruction for approval levels, handoffs and the completion report.
