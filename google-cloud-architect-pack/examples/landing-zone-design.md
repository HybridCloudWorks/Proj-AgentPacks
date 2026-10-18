# Worked example: landing zone for a regulated EU company

Synthetic scenario for the `design-landing-zone.prompt.md` workflow.

## Context

A payments company with two business units has just created its Google Cloud organization, federated to Microsoft Entra ID. Obligations: EU residency for all workload data, immutable audit evidence for seven years, separation between production and everything else.

## Read-only discovery and a permission gap

The user authorized Level 1 discovery on organization `123456789012` through impersonation of `lz-reader@acme-admin.iam.gserviceaccount.com`. The agent classified each command with the gcp-estate-discovery classifier before running it:

- `gcloud resource-manager folders list --organization=123456789012` → Level 1, ran, no folders yet.
- `gcloud org-policies list --organization=123456789012` → Level 1, failed with `Permission Denied`.

The agent did not grant itself a role and did not retry with the user's own credentials. It reported: "The reader identity lacks `orgpolicy.policies.list`; the least-privileged role that grants it is Organization Policy Viewer (`roles/orgpolicy.policyViewer`) on the organization. An organization administrator can grant it; I will continue the design and mark current-policy state as unverified."

## Design highlights

- Hierarchy (ADR-001, Day-0): environment first. `common` (logging, monitoring, network hosts, security, CI and artifacts, keys), `production`, `non-production`, `development`, each with business-unit subfolders only where delegated administration is needed.
- Naming: `<bu>-<env>-<app>-<4 random chars>`; mandatory labels environment, application, owner, cost-centre, data-classification.
- Policy baseline with rollout order: dry-run first, then enforce at the root, with folder exceptions only through tags. `gcp.resourceLocations` restricted to EU locations; `iam.allowedPolicyMemberDomains` applied last after confirming the deployment identity, break-glass accounts and Google service agents are inside the allowed set.
- Logging: organization aggregated sink including children to a log bucket in an EU location in the logging project, retention seven years, bucket locked after a test period (ADR-002, irreversible once locked). Data Access logs enabled for data projects only, with a volume estimate.
- Billing: export to BigQuery in the billing project; budgets with 50%, 90% and 100% alerts per project.
- Groups: organization, billing, network, security, logging and monitoring administrators and platform operators, each mapped to predefined roles; super administrator accounts separate and protected with hardware keys.
- IaC stages: bootstrap, organization, environments, networks, project factory; each stage planned separately.

## Result

Status DESIGN_READY_FOR_REVIEW with one unverified item (current organization policies, pending the viewer role). Every organization change is listed as a Level 2 step for the platform team.
