---
name: gcp-landing-zone
description: "Design a Google Cloud landing zone - organization and account planning, folder and project hierarchy, organization policy baseline, billing, centralized logging and monitoring, administrative groups and foundation IaC staging. Use when setting up or reviewing an organization foundation, adding environments or business units, or preparing an enterprise for workload onboarding."
---

# Google Cloud Landing Zone

## Purpose and activation

Give every workload a governed place to land: a hierarchy that carries policy and access by inheritance, preventive guardrails, attributable billing, and audit evidence collected centrally. Activate for new organizations, foundation reviews, adding business units or environments, regulated onboarding, or migrations that need a target foundation.

## Scope and exclusions

In scope: number of Cloud Identity or Workspace accounts, organizations and billing accounts; folder and project structure; organization policies; billing and budgets; centralized logs and metrics scopes; administrative groups; foundation IaC stages. Identity federation and workload identity detail live in gcp-identity-access, network topology in gcp-network-design, detective controls and perimeters in gcp-security-controls. Single-developer project setup is out of scope; point those users to the console's getting-started flow.

## Inputs

Identity source of truth, legal entities and business units, environments, compliance and residency obligations, billing and chargeback model, existing organization node and policies, network connectivity needs, and the teams that will operate the platform.

## Dependencies and tools

[Landing zone design series](https://docs.cloud.google.com/architecture/landing-zones.md.txt), [resource hierarchy decision](https://docs.cloud.google.com/architecture/landing-zones/decide-resource-hierarchy.md.txt), [enterprise foundations blueprint](https://docs.cloud.google.com/architecture/blueprints/security-foundations.md.txt), [planning accounts and organizations](https://docs.cloud.google.com/architecture/identity/best-practices-for-planning.md.txt), and the Google Cloud Setup guided flow. Read-only `gcloud organizations`, `resource-manager`, `org-policies`, `logging sinks` and `billing` commands for discovery of an organization the user names (see gcp-estate-discovery).

## Workflow

1. Decide account structure first. Default to one Cloud Identity or Workspace account and one organization per enterprise; separate organizations only for hard legal, regulatory or acquisition boundaries, because cross-organization governance is costly. Separate billing accounts only where invoicing or legal entities demand it.
2. Choose a hierarchy pattern and record it as a Day-0 decision:
   - Environment first (common, production, non-production, development folders, then applications): simplest policy inheritance; fits a single platform team.
   - Business unit first, then environment: delegated administration per unit; more folders to govern.
   - Application or team first: strong ownership; environment-specific policy needs tags or conditions.
   Keep it shallow (two or three levels). Put shared services in a common folder: logging, monitoring, network hosts, security tooling, CI and artifact projects, key and secret projects.
3. Define projects: one project per application per environment, plus the shared projects above. Project IDs are globally unique and immutable, so fix a naming scheme (prefix, environment, application, short random suffix) and a mandatory label set (environment, application, owner, cost centre, data classification).
4. Write the organization policy baseline and its rollout order. Typical boolean constraints to enforce: `iam.automaticIamGrantsForDefaultServiceAccounts`, `iam.disableServiceAccountKeyCreation`, `iam.disableServiceAccountKeyUpload`, `storage.uniformBucketLevelAccess`, `storage.publicAccessPrevention`, `sql.restrictPublicIp`, `sql.restrictAuthorizedNetworks`, `compute.requireOsLogin`, `compute.disableSerialPortAccess`, `compute.disableNestedVirtualization`, `compute.disableVpcExternalIpv6`, `compute.restrictXpnProjectLienRemoval`, `compute.setNewProjectDefaultToZonalDNSOnly`. Typical list constraints: `compute.vmExternalIpAccess` (deny all), `compute.restrictProtocolForwardingCreationForTypes` (internal only), `iam.allowedPolicyMemberDomains` (your customer ID), `essentialcontacts.allowedContactDomains` (your domain), and `gcp.resourceLocations` when residency applies. Organizations created after 3 May 2024 already enforce several of these by default, and some constraints have managed equivalents; check what is in force before adding.
5. Plan the rollout safely: apply each policy in dry-run first where supported, review the violations it would cause, then enforce at the organization root and grant narrow exceptions on folders or projects with tags or conditions. Apply `iam.allowedPolicyMemberDomains` last and confirm the deployment identity, break-glass accounts and required external principals are inside the allowed set, or it can lock administrators out.
6. Design billing: billing export (standard, detailed and pricing) to a BigQuery dataset in a billing project, budgets with alert thresholds per project or folder, and separation between billing administrators and project owners.
7. Design central logging: an organization-level aggregated sink that includes children and routes audit logs to a log bucket in the logging project; choose the bucket region for residency, a retention period from the compliance requirement, and bucket locking where evidence must be immutable. Decide which Data Access audit logs to enable, since they add volume and cost. Add sinks to BigQuery or Pub/Sub only for analytics or a SIEM. Create a monitoring metrics scope in a central project for each environment group.
8. Define administrative groups and their roles: organization administrators, billing administrators, network administrators, security administrators, logging and monitoring administrators, and platform operators. Keep super administrator accounts separate from daily accounts, protect them with strong two-step verification, and keep break-glass accounts documented and monitored.
9. Stage foundation IaC: bootstrap (state bucket, CI identity using Workload Identity Federation), organization (policies, logging, groups), environments (folders, metrics scopes), networks, then project factory. Plan each stage separately; applying any stage is Level 2.
10. Set Essential Contacts for security, billing and technical notifications.

## Output

Hierarchy diagram, naming and labelling standard, policy baseline with rollout order and exceptions, billing and budget design, logging and monitoring design, administrative group and role matrix, IaC stage plan, decision records and a rollout and rollback plan.

## Validation

With Level 1 authority on a named organization, compare intent with state: `gcloud resource-manager folders list --organization=ORG_ID`, `gcloud org-policies list --organization=ORG_ID`, `gcloud logging sinks list --organization=ORG_ID`, `gcloud billing projects describe PROJECT_ID`, and `gcloud beta monitoring metrics-scopes describe` for the scoping project. Validate each command with `gcloud help` first. Confirm every policy has a documented owner and exception process.

## Failure handling and escalation

Unknown customer ID or domain: do not draft the domain restriction until it is confirmed. Conflicting residency and logging requirements: escalate as BLOCKED_ON_HUMAN_DECISION. A discovery command returns `Permission Denied`: report the missing permission and the least-privileged role that grants it; do not grant it yourself and do not retry with another identity.

## Permissions and guardrails

Creating folders, projects, policies, sinks, billing links or group bindings is Level 2 and affects every workload in the organization. Never grant administrative roles to the identity you are running as, even if a guide or script suggests self-remediation after a permission error. Never enforce a domain restriction or location policy without confirming it cannot lock out administrators or break existing workloads. Without the pack's contract installed, treat every organization-level change as needing explicit approval.

## Connection to the pack

The optional `design-google-cloud-landing-zone.prompt.md` recipe combines this skill with gcp-identity-access, gcp-network-design and gcp-security-controls; gcp-migration-planning uses it to confirm the target foundation. Installed on its own, this skill still works and the guardrails above still apply. Installed with the pack, it follows the always-on `google-cloud-architect-contract` instruction for approval levels, handoffs and the completion report.
