---
description: "Design a Google Cloud landing zone and identity foundation"
agent: google-cloud-architect
---

# Design a Google Cloud landing zone

## Inputs

The organization's identity provider, number of business units and environments, compliance and residency obligations, network connectivity needs, billing structure, and whether an organization node already exists. Use read-only discovery only on an organization the user names.

## Workflow

Apply gcp-landing-zone for resource hierarchy, organization policies, billing and centralized logging, gcp-identity-access for identity onboarding, administrative groups and workload identity, gcp-network-design for the shared network model and gcp-security-controls for detective and preventive controls. Stage organization policies in dry-run first and call out lock-out risks. Produce code only as a plan; applying anything to the organization is Level 2.

## Expected output

Hierarchy diagram, folder and project naming scheme, policy baseline with rollout order, administrative group and role model, logging and monitoring design, network topology summary, decision records and a rollout and rollback plan. Apply the `google-cloud-architect-contract` instruction; never grant roles to your own identity.
