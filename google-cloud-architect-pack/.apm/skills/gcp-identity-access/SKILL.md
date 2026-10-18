---
name: gcp-identity-access
description: "Design Google Cloud identity and access - workforce onboarding and federation, group-based IAM, least-privilege role design, conditions, deny policies, just-in-time elevation, workload identity without keys, and end-user access with IAP or Identity Platform. Use when deciding how people, pipelines, workloads or agents authenticate to Google Cloud and what they may do."
---

# Google Cloud Identity and Access

## Purpose and activation

Make every principal identifiable and every permission justified: humans through a managed or federated identity, workloads through attached or federated service identities, and no long-lived keys. Activate for identity onboarding, IAM design or review, service account strategy, CI/CD authentication, cross-cloud workload access, application user authentication, or an access incident.

## Scope and exclusions

In scope: workforce identity sources, federation and provisioning, groups and role design, IAM conditions, deny policies, Privileged Access Manager, emergency access, service accounts and their usage patterns, Workload Identity Federation (external and for GKE), impersonation, OIDC between services, IAP and Identity Platform choices, API key restrictions. Out of scope: running IAM changes (Level 2), and in-application authorization logic.

## Inputs

Identity provider and source of truth (Active Directory, Microsoft Entra ID, Okta, another IdP, or none), user populations (employees, contractors, partners, customers), existing consumer accounts using corporate addresses, teams and their duties, workloads and where they run (Google Cloud, other clouds, on-premises, CI systems), and compliance requirements for access reviews.

## Dependencies and tools

[Authentication overview](https://docs.cloud.google.com/docs/authentication), [identity onboarding decision](https://docs.cloud.google.com/architecture/landing-zones/decide-how-to-onboard-identities.md.txt), [federation best practices](https://docs.cloud.google.com/architecture/identity/best-practices-for-federating.md.txt), [service account best practices](https://docs.cloud.google.com/iam/docs/best-practices-service-accounts.md.txt), [Workload Identity Federation best practices](https://docs.cloud.google.com/iam/docs/best-practices-for-using-workload-identity-federation.md.txt), [Privileged Access Manager best practices](https://docs.cloud.google.com/iam/docs/pam-best-practices.md.txt). Read-only `get-iam-policy`, `gcloud asset search-all-iam-policies` and IAM Recommender listings for evidence.

## Workflow

1. Clarify who authenticates (human, script, workload, external system, agent), where the code runs, and what it calls (a Google API or a custom application).
2. Workforce identity:
   - Managed accounts in Cloud Identity or Workspace, federated to the corporate IdP for single sign-on, with users and groups provisioned from the authoritative source (Google Cloud Directory Sync for Active Directory, provisioning connectors for Entra ID or Okta).
   - Workforce Identity Federation when users must not be synchronized into Google; check that every product the users need supports federated principals.
   - Plan the eviction or migration of consumer accounts that use corporate addresses before enforcing federation.
3. Role design: grant roles to groups, not individuals; grant at the lowest level that works (resource, project, then folder); start from predefined roles, add custom roles only when predefined roles are materially too broad; never grant basic roles (Owner, Editor, Viewer) for daily work. Use IAM conditions for time-bound or tag-scoped access, deny policies for guardrails that must survive later grants, and Privileged Access Manager for just-in-time elevation with approval and expiry.
4. Emergency access: documented break-glass accounts outside the federated IdP, protected with hardware-backed two-step verification, alerting on use, and tested periodically; a plan for IdP outage.
5. Workload identity:
   - One user-managed service account per workload and environment with only the roles it needs; never the Compute Engine default service account in production.
   - Attach the service account to the resource (Compute Engine, Cloud Run, Cloud Run functions) so the metadata server issues short-lived tokens.
   - GKE: Workload Identity Federation for GKE, mapping Kubernetes service accounts to IAM principals.
   - Outside Google Cloud (other clouds, on-premises, CI such as GitHub Actions or GitLab): Workload Identity Federation with attribute conditions that pin the repository, branch or account; no exported keys.
   - Humans and pipelines that need a service account's permissions use impersonation (`roles/iam.serviceAccountTokenCreator` on that one account), not keys.
   - Legacy VMs and Standard node pools still apply OAuth access scopes on top of IAM; check them when an attached account fails unexpectedly.
6. Service-to-service: a caller presents a Google-signed OIDC ID token to a private Cloud Run service whose invoker role it holds; API keys only for APIs that require them, restricted to specific APIs and referrers or IPs and stored in Secret Manager.
7. End users of applications: IAP for workforce and partner access to internal web apps and VM admin access, with context-aware access levels; Identity Platform for customer sign-up and sign-in inside the application.
8. Agents and automation, including this one: run under a dedicated, impersonated service account with viewer-type roles for discovery, separate from the human's broad access, so actions are scoped and audited under the agent's own identity.
9. Plan continuous hygiene: IAM Recommender to remove excess permissions, periodic access reviews, alerting on primitive-role grants and on service account key creation.

## Output

Identity architecture (sources, federation, provisioning), a role matrix (group or service account, role, scope, justification), service account inventory design with naming, the workload identity pattern per runtime, emergency access design, decision records for federation and hierarchy-level grants, and the change list for the user to apply.

## Validation

For a named project or organization, at Level 1: summarize bindings with `gcloud projects get-iam-policy PROJECT_ID --format="json(bindings)"` and `gcloud asset search-all-iam-policies --scope=organizations/ORG_ID --query="policy:roles/owner"`, list user-managed keys with `gcloud iam service-accounts keys list --iam-account=SA_EMAIL --managed-by=user`, and read IAM Recommender findings. Report bindings by role and principal type; never paste whole policies. Confirm with gcp-landing-zone that the key-creation and domain-restriction constraints are enforced.

## Failure handling and escalation

A requirement that seems to need a key (a third-party tool that only accepts JSON keys): document the risk, look for federation support first, and if a key is unavoidable escalate it as an exception with rotation, scope and owner. A product that does not support workforce-federated principals: present the gap and the alternatives. `Permission Denied` while inspecting: report the missing permission; do not escalate privileges.

## Permissions and guardrails

Any IAM binding, role, condition, deny policy, PAM entitlement, workload identity pool, key or federation setting change is Level 2. Never grant a role to the identity you are running as, never create or download a service account key, and never print access or ID tokens. Without the pack's contract installed, treat every IAM change as needing explicit approval.

## Connection to the pack

gcp-landing-zone uses this skill for administrative groups and identity onboarding; gcp-security-reviewer applies it in independent reviews; the platform skills apply its workload patterns. Installed on its own, this skill still works and the guardrails above still apply. Installed with the pack, it follows the always-on `google-cloud-architect-contract` instruction for approval levels, handoffs and the completion report.
