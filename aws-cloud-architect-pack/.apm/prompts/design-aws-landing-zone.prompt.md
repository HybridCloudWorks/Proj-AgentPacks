---
description: "Design a multi-account AWS landing zone: Organizations, Control Tower, OUs, guardrails, identity, logging, network hub and account vending"
agent: aws-cloud-architect
---

# Design a multi-account landing zone

## Inputs

- Organization structure, business units, environments, and the expected account count and growth.
- Current state: existing accounts, whether AWS Organizations or Control Tower is already in use, IAM users and access keys, existing logging and AWS Config setup.
- Compliance frameworks, log retention requirements, data classification, and allowed Regions or partition.
- Identity provider and federation model, plus who owns platform, security, network and billing.
- On-premises CIDR ranges, hybrid connectivity, inspection requirements and DNS model.
- Cost-allocation model: cost centers, showback or chargeback, budget owners.

## Workflow

1. `aws-architecture-foundations`: establish scope, risk model and current-state evidence with read-only discovery.
2. `aws-caf-landing-zones-and-governance`: account model, OU hierarchy, account vending, delegated administration, break-glass access, and exceptions with owner and expiry.
3. `aws-security-identity-and-compliance`: IAM Identity Center federation, permission sets, cross-account roles, centralized CloudTrail, Config, GuardDuty, Security Hub and Macie, and KMS ownership. Keep preventive, detective and corrective controls distinct; an SCP limits permissions and never grants them.
4. `aws-networking-hybrid-and-edge`: IPAM and CIDR strategy, network hub account, Transit Gateway sharing, inspection, egress and hybrid DNS.
5. `aws-cost-sustainability-and-finops`: mandatory tags, budgets, anomaly detection and showback ownership.
6. `aws-well-architected-and-frameworks`: frame readiness through the six CAF perspectives with workstreams, owners and measurable outcomes.
7. `aws-docs-mcp-and-evidence`: verify Control Tower governed Regions, enrollment prerequisites for existing accounts, and organization quotas, or mark them not-verified.
8. `aws-iac-deployment-and-lifecycle`: phase the rollout, testing guardrails on a staging OU before NonProd and Prod.
9. `aws-architecture-handoff-and-adr`: REQ, TOPOLOGY (OUs, accounts, network hub), CONSTRAINTS (SCPs, tags, Regions, retention) and ADRs for the account model and vending approach.

## Expected output

- OU and account map with the purpose, owner and isolation reason for each account.
- Guardrail catalogue split into preventive, detective and corrective controls, with break-glass and exception handling.
- Identity, logging, security-tooling, network-hub and account-vending designs, and a phased rollout plan.
- The four handoff artifacts and a completion report in the contract's format.

## Guardrails

Do not enable Control Tower, create or move accounts, attach SCPs, or change Identity Center, IAM or the organization unless the user gives explicit, scoped authorization for that exact change. Define break-glass access before any preventive guardrail is enforced. A landing-zone design is not a compliance attestation. Follow the `aws-cloud-architect-contract` instruction.
