# Worked example: multi-account landing zone for a healthcare provider

Workflow: `design-landing-zone.prompt.md`. Skills applied: `aws-architecture-foundations`, `aws-caf-landing-zones-and-governance`, `aws-security-identity-and-compliance`, `aws-networking-hybrid-and-edge`, `aws-cost-sustainability-and-finops`, `aws-well-architected-and-frameworks`, `aws-docs-mcp-and-evidence`, `aws-iac-deployment-and-lifecycle`, `aws-architecture-handoff-and-adr`.

The organization and figures are fictional.

## Request

> Harbor Health Network runs everything in one AWS account. Before we onboard three new clinical applications, design a multi-account landing zone with Control Tower. We use Terraform and a corporate SAML identity provider.

## Inputs and discovery

Discovery was read-only. The user exported an IAM credential report, an AWS Config recorder status and a VPC inventory from the existing account and shared the files.

| Fact | Value | Label |
|---|---|---|
| Current estate | One account holding production and development. Two VPCs, 10.20.0.0/16 and 10.21.0.0/16 | observed (VPC export) |
| IAM users | 118 IAM users; 74 have active access keys, 23 of them unused for over 90 days | observed (credential report) |
| AWS Config | A recorder and delivery channel are already configured in the existing account | observed (Config export) |
| Regions | us-east-1 primary, us-west-2 for recovery | observed (brief) |
| Compliance | HIPAA. The user states a Business Associate Addendum is in place | inferred (user statement, not seen) |
| Log retention | Seven years, by internal policy | observed (policy excerpt) |
| Growth | About 35 accounts within 24 months | observed (brief) |
| Network | Site-to-Site VPN to the data center today, Direct Connect planned. 10.128.0.0/12 reserved for AWS | observed (network plan) |
| Teams | Platform team of three, a separate security team, central finance with cost centers per clinic group | observed (brief) |

## Account and OU model

`aws-caf-landing-zones-and-governance` separated accounts wherever billing, access, compliance or blast radius differ:

| OU | Accounts | Isolation reason |
|---|---|---|
| Root | New management account (billing, Organizations, Control Tower only) | The management account must not run workloads, so the existing account cannot become it |
| Security | Log Archive, Audit (security tooling delegated administrator) | Write-once evidence; separate access for the security team |
| Infrastructure | Network Hub, Shared Services, Identity (Identity Center delegated administration), AFT Management | Shared platform components with their own change control |
| Workloads/Prod | One account per clinical application, plus `legacy-prod` (the existing account, invited) | Protected health information boundaries and blast radius |
| Workloads/NonProd | One account per application for dev and test | Developers get broader access without touching production data |
| Sandbox | Short-lived experimentation accounts with budgets | No connectivity to the hub |
| Policy-Staging | One test account | Guardrails are proven here before NonProd and Prod |
| Suspended | Closed accounts awaiting removal | Deny-all SCP |

The existing account joins as `legacy-prod` under Workloads/Prod with a time-boxed exception (owner: platform lead, expiry 2027-06-30). Its workloads move to dedicated accounts in later waves.

**ADR-001.** Account vending uses Control Tower Account Factory for Terraform (AFT) in its own AFT Management account. The rejected option, console Account Factory with Customizations for Control Tower, does not match the team's Terraform skills or its review workflow.

## Identity and guardrails

`aws-security-identity-and-compliance` designed the identity model:

- IAM Identity Center federated to the corporate identity provider through SAML, with SCIM provisioning.
- Permission sets mapped to job roles: platform-admin, security-audit, app-deployer, app-readonly, billing.
- The 74 access keys retire in three phases. Workloads move to roles first, people move to Identity Center second, and remaining keys are disabled and then deleted after a 30-day watch.
- Break-glass access: two IAM users in the management account with hardware MFA. Credentials are held under a dual-control procedure, and an EventBridge rule alerts the security team on any sign-in. This is defined **before** any SCP is enforced.

Guardrails are kept as three distinct kinds of control:

- **Preventive (SCPs).** An SCP limits the maximum permissions and never grants any.
  - Deny leaving the organization.
  - Deny stopping or deleting CloudTrail, Config, GuardDuty and Security Hub, except for the security administrator role.
  - Deny Regions other than us-east-1 and us-west-2, with exemptions for global services.
  - Deny root user actions in member accounts.
  - Deny creating IAM users and access keys in Workloads OUs, with an exception path.
- **Detective.** Control Tower detective controls; AWS Config conformance packs aggregated in Audit; Security Hub standards; GuardDuty and Macie (for buckets tagged `data-classification=phi`) delegated to Audit.
- **Corrective.** Automated remediation that re-enables S3 Block Public Access, applied first in NonProd.

The organization trail goes to an S3 bucket in Log Archive with S3 Object Lock and seven-year retention. Its KMS key is owned by the security team, and read access is limited to the security-audit permission set.

## Network hub

`aws-networking-hybrid-and-edge` designed the hub:

- An IPAM pool carved from 10.128.0.0/12, split by Region, then environment, then account.
- The existing 10.20.0.0/16 and 10.21.0.0/16 ranges sit outside the pool and are recorded as exceptions until they are renumbered or retired.
- A Transit Gateway in Network Hub, shared through AWS RAM, with separate route tables for Prod, NonProd and Shared. Prod and NonProd do not route to each other.
- Centralized egress and inspection with AWS Network Firewall, as the security team requires.
- Route 53 Resolver inbound and outbound endpoints for hybrid DNS.
- The VPN terminates on the Transit Gateway. Direct Connect gets its own future ADR.

## Cost, CAF readiness and rollout

- **Cost** (`aws-cost-sustainability-and-finops`). Organizations tag policies require `cost-center`, `application`, `environment`, `owner` and `data-classification`. AFT customizations create a budget for every vended account. Cost anomaly detection runs in the management account, and showback goes to each clinic group monthly.
- **CAF readiness** (`aws-well-architected-and-frameworks`):
  - Governance: an exception register and its approvers.
  - Platform: AFT pipelines.
  - Security: delegated tooling.
  - Operations: on-call for the hub.
  - People: AFT and Control Tower skills for a team of three. This is the largest gap, with a training workstream owned by the platform lead.
  - Business: chargeback agreement with finance.
- **Rollout** (`aws-iac-deployment-and-lifecycle`):
  - Phase 1: management account, Control Tower, Security OU.
  - Phase 2: Infrastructure OU and network hub.
  - Phase 3: SCPs on Policy-Staging, then NonProd, then Prod, each after a test-account soak.
  - Phase 4: invite and enroll `legacy-prod`.
  - Phase 5: vend the clinical application accounts.

## Evidence

`aws-docs-mcp-and-evidence`, using the AWS Knowledge MCP Server:

| Claim | Source | Label |
|---|---|---|
| Control Tower governs us-east-1 and us-west-2 | Control Tower user guide, governed Regions, retrieved 2026-10-18 | observed |
| An existing AWS Config recorder must be resolved before the account is enrolled in Control Tower | Control Tower enrollment prerequisites, retrieved 2026-10-18 | observed (re-check at implementation; prerequisites are version-sensitive) |
| AFT recommends a dedicated AFT management account | AFT documentation, retrieved 2026-10-18 | observed |
| A new organization's default account quota allows about 35 accounts | Not checked; there is no organization yet | not-verified |
| Every service planned for protected health information is HIPAA-eligible under the user's BAA | Not checked by the architect; needs the compliance owner | not-verified |

## Completion report

Pack: aws-cloud-architect. Date: 2026-10-18.

Outcome: the landing-zone design and handoff are designed. Nothing is enabled, created or attached, and two account-level facts are not verified.

### scope_and_inputs

Organization-wide foundations for Harbor Health Network in us-east-1 and us-west-2. Inputs were the brief, an IAM credential report, a Config export, a VPC export, a network plan and a log-retention policy excerpt (observed). Authority was read-only design, with handoff files written to `handoff/landing-zone/`.

### business_outcomes_and_requirements

- Onboard three clinical applications into isolated accounts.
- Retire long-lived credentials.
- Keep seven years of tamper-resistant logs.
- Support HIPAA scope.
- Grow to about 35 accounts.
- Give each clinic group cost visibility.

### source_facts_and_evidence

- Estate facts come from the user's exports: observed.
- Control Tower and AFT documentation via the AWS Knowledge MCP Server, 2026-10-18: observed.
- BAA status: inferred from the user's statement.
- Account quota and HIPAA eligibility of the service list: not-verified.

### framework_alignment

- CAF: all six perspectives are mapped to workstreams. People is the largest gap.
- Well-Architected: Security (identity, detective controls) and Operational Excellence (hub on-call) are designed.
- Reliability of the hub depends on redundant VPN tunnels and a future Direct Connect ADR.

### proposed_architecture

- The eight-OU model above, with a new management account.
- AFT vending.
- Identity Center with SCIM.
- Preventive, detective and corrective guardrail sets.
- An Object Lock log archive.
- A Transit Gateway hub with separate route domains and centralized inspection.

All designed. The TOPOLOGY ids cover the OUs and accounts.

### assumptions_and_tradeoffs

- ADR-001: AFT over console Account Factory.
- ADR-002: centralized inspection, which adds inspection data-processing cost in exchange for one policy point.
- ADR-003: `legacy-prod` stays as an exception rather than being rebuilt before onboarding.
- Assumption: the BAA covers the planned services (owner: compliance officer).

### implementation_and_operating_implications

- Five rollout phases, with Terraform through AFT for account baselines.
- SCPs are proven on Policy-Staging first.
- The Config recorder conflict in the legacy account must be resolved before enrollment.
- Access-key retirement has a 30-day watch.
- Owners: platform lead (organization and AFT), security lead (guardrails and logs), network lead (hub).

### security_resilience_cost_and_sustainability

- Security (designed): federation, no new IAM users, break-glass with alerting, an immutable log archive.
- Resilience (designed): the guardrails and hub span both Regions. Recovery of the management account and AFT pipeline is documented in CONSTRAINTS and not tested.
- Cost (designed): tag policies, per-account budgets, anomaly detection. Network Firewall and Transit Gateway processing costs are unpriced (not-verified).
- Sustainability: Sandbox budgets and expiry reduce idle accounts.

### output_files

| File | Purpose | Check run | Label |
|---|---|---|---|
| `handoff/landing-zone/REQ.md` | Requirements, ownership, open questions | Reviewed against the template sections | designed |
| `handoff/landing-zone/TOPOLOGY.json` | OUs, accounts, hub network | Parsed as JSON | structurally-validated |
| `handoff/landing-zone/CONSTRAINTS.json` | SCP catalogue, tags, Regions, retention, exceptions | Parsed as JSON | structurally-validated |
| `handoff/landing-zone/ADR.md` | ADR-001 to ADR-003 | Alternatives and revisit triggers present | designed |

### live_or_external_checks

- AWS Knowledge MCP documentation lookups: executed (observed).
- Organization quota, Control Tower setup, SCP behavior in a test account, and HIPAA eligibility: not executed (not-verified).

### unresolved_risks

- The account quota may need raising before vending (owner: platform lead).
- HIPAA eligibility of the service list is unconfirmed (owner: compliance officer).
- 74 access keys stay active until phase 2 (owner: security lead).
- The legacy account's CIDRs fall outside the IPAM plan (owner: network lead).

### next_safe_action

The compliance officer confirms BAA coverage of the service list, and the platform lead approves phase 1. Creating the management account and enabling Control Tower needs explicit authorization naming the account email, Regions and the person approving.
