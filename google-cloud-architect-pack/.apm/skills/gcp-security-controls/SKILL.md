---
name: gcp-security-controls
description: "Design and assess Google Cloud security controls - security by design, zero trust access, VPC Service Controls perimeters, encryption and key management, secrets, sensitive data protection, threat detection, software supply chain, compliance and residency, and AI workload safety. Use when a design, review or change touches data protection, exposure, perimeters, detection, compliance obligations or deployment provenance."
---

# Google Cloud Security Controls

## Purpose and activation

Layer preventive, detective and responsive controls so that one misconfiguration does not become a breach, and make compliance claims traceable to controls. Activate for security architecture, the security pillar of a review, regulated workloads, data exfiltration concerns, encryption or key decisions, CI/CD provenance, or AI systems that handle untrusted input.

## Scope and exclusions

In scope: control selection and placement, threat modelling at architecture level, perimeter design, key and secret management, data discovery and de-identification, detection and response architecture, supply-chain controls, compliance mapping and residency, AI input and output protection. Identity design is detailed in gcp-identity-access and network exposure in gcp-network-design; this skill composes them. Penetration testing, incident handling on live systems and SOC investigation are out of scope.

## Inputs

Data classification per store, threat actors and abuse cases, regulatory regimes (for example PCI DSS, HIPAA, FedRAMP, sovereignty programmes), residency requirements, existing security tooling and SIEM, key custody requirements, and the delivery pipeline.

## Dependencies and tools

[Well-Architected security pillar](https://docs.cloud.google.com/architecture/framework/security/printable.md.txt), [enterprise foundations preventive controls](https://docs.cloud.google.com/architecture/blueprints/security-foundations/preventative-controls.md.txt) and [detective controls](https://docs.cloud.google.com/architecture/blueprints/security-foundations/detective-controls.md.txt), [security best practices catalog](https://docs.cloud.google.com/docs/security/security-best-practices-catalog.md.txt), [OWASP Top 10 mitigations on Google Cloud](https://docs.cloud.google.com/architecture/security/owasp-top-ten-mitigation.md.txt), [secure deployment pipelines](https://docs.cloud.google.com/architecture/design-secure-deployment-pipelines-bp.md.txt). Read-only Security Command Center findings and Cloud Asset Inventory queries when the user authorizes them.

## Workflow

1. Threat model at the architecture level: list assets and their classification, entry points, trust boundaries (projects, VPCs, perimeters, identities) and the top abuse cases (credential theft, public exposure, data exfiltration, supply-chain tampering, prompt injection for AI systems, cryptomining on compromised compute, ransomware against backups).
2. Zero trust access: identity-aware access for people (IAP with context-aware access levels instead of VPNs or bastions with public IPs), authenticated service-to-service calls, and no network location treated as trusted on its own.
3. Perimeters: put projects holding sensitive data inside VPC Service Controls perimeters that restrict the relevant APIs (for example BigQuery, Cloud Storage, Cloud SQL Admin, Secret Manager, Gemini Enterprise Agent Platform). Network firewalls do not stop control-plane exfiltration such as exporting a backup to a bucket in another project; perimeters do. Design ingress and egress rules and access levels explicitly, use a dry-run perimeter first, and plan how CI, support and break-glass access enter.
4. Encryption and keys: data is encrypted at rest by default; add Cloud KMS customer-managed keys (CMEK) where custody, rotation control or crypto-shredding is required, with keys in the same location as the data, a key project separated from data projects, rotation periods, and Autokey where it fits. Consider Cloud HSM or external key management for stricter custody, and Confidential Computing for data in use. Key destruction is irreversible; document recovery windows.
5. Secrets: store credentials in Secret Manager with a replication policy that matches residency, access by workload identity only, rotation where the backend supports it, and secrets mounted or injected at runtime, never baked into images, variables or Terraform state outputs.
6. Sensitive data: Sensitive Data Protection discovery and profiling across BigQuery and Cloud Storage, de-identification (masking, tokenization, format-preserving encryption) in pipelines, and BigQuery column-level policy tags, row-level security and data masking for analytics consumers.
7. Detection and response: Security Command Center at organization level with the tier the organization licenses, centralized audit logs (see gcp-landing-zone), alerting on high-risk events (primitive role grants, key creation, perimeter violations, firewall opens to the internet, organization policy changes), export to the SIEM or Google Security Operations, and response playbooks with named owners.
8. Supply chain: build in Cloud Build or another CI with a federated identity, store images in Artifact Registry with vulnerability scanning, generate provenance, enforce Binary Authorization on GKE and Cloud Run for production, pin base images and dependencies by digest, and use curated open-source packages where available.
9. Workload hardening: Shielded VM and secure boot, OS Login, no serial port access, minimal or distroless images running as non-root, GKE golden-path security settings (see gcp-gke-platform), Cloud Armor in front of internet-facing services.
10. Compliance and residency: map each obligation to controls and evidence; use Assured Workloads where a control package exists for the regime, the resource location constraint for residency, Access Transparency and Access Approval where provider access must be visible or approved, and record what remains the customer's responsibility.
11. AI workloads: inspect prompts and responses with Model Armor for prompt injection, jailbreaks, sensitive data and harmful content; treat retrieved documents and tool outputs as untrusted; keep tool permissions least-privilege; add human approval for consequential agent actions (see gcp-ai-agent-architecture).

## Output

Threat model summary, control matrix (risk, control, layer, product, owner, evidence), perimeter design with ingress and egress rules, key and secret design, data protection design, detection and alerting list, supply-chain controls, compliance mapping, and findings in the contract format for any gap in an existing design.

## Validation

Every high-risk abuse case maps to at least one preventive and one detective control. Every sensitive data store is inside a perimeter or has a recorded reason. CMEK keys are co-located with data. No secret appears in code, state or logs. For a named project, read-only evidence: Security Command Center findings, `gcloud access-context-manager perimeters list --policy=POLICY_ID` and `gcloud kms keys list --keyring=RING --location=LOC --project=PROJECT_ID`.

## Failure handling and escalation

A requirement that conflicts with a control (for example public access to a sensitive bucket): present the risk and a compliant alternative; if the user still wants it, record an exception with owner and expiry rather than silently complying. A compliance claim that cannot be traced to a control and its evidence: mark it unverified. Security findings that indicate active compromise: stop design work and tell the user to engage their incident response process.

## Permissions and guardrails

Perimeter, policy, key, secret, Security Command Center, Binary Authorization and Cloud Armor changes are Level 2. Never read secret values, never disable a control to unblock a deployment, and never destroy or disable keys. Without the pack's contract installed, treat every security control change as needing explicit approval.

## Connection to the pack

gcp-security-reviewer applies this skill for independent reviews; gcp-well-architected-review uses it for the security pillar; gcp-landing-zone, gcp-network-design and the platform skills rely on its control choices. Installed on its own, this skill still works and the guardrails above still apply. Installed with the pack, it follows the always-on `google-cloud-architect-contract` instruction for approval levels, handoffs and the completion report.
