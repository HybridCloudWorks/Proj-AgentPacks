---
description: "Analyze AWS architecture economics or spend and recommend measured cost and sustainability optimizations without weakening security or resilience"
agent: aws-cloud-architect
---

# Review AWS cost and sustainability

## Inputs

- Workload, accounts and Regions in scope, the time window and the currency.
- Billing evidence: Cost Explorer exports, Cost and Usage Report queries, budgets, anomaly history, commitments in force.
- Demand profile: current, expected and peak, plus known failure or recovery scenarios.
- The architecture or topology, tagging coverage, and the security, recovery and compliance requirements that must not be traded away.

## Workflow

1. `aws-architecture-foundations`: confirm the scope and which requirements are fixed.
2. `aws-cost-sustainability-and-finops`: break spend into cost dimensions (compute, storage and requests, data transfer, NAT and endpoints, load balancing, observability, licensing, support, backup and replication). Model current, expected, peak and failure scenarios. Check tag ownership, budgets and anomaly detection. Add workload-specific sustainability actions.
3. `aws-networking-hybrid-and-edge`: expose NAT, cross-AZ, cross-Region, hybrid and internet-egress paths.
4. `aws-workload-and-service-selection`: right-sizing, managed alternatives, storage classes and lifecycle policies.
5. `aws-resilience-dr-and-migration` and `aws-security-identity-and-compliance`: record what each saving would cost in recovery, isolation or detection.
6. `aws-docs-mcp-and-evidence`: use the AWS Pricing API, a pricing MCP server or official pricing pages when available, and record the retrieval date and Region.
7. `aws-architecture-handoff-and-adr`: an ADR for every recommendation that trades cost against another pillar.

## Expected output

- A cost-driver breakdown with evidence labels.
- Ranked recommendations. Each one gives an estimated saving range, confidence, effort, risk, trade-off and owner.
- A measurement plan that shows how each saving will be confirmed, commitment guidance with its caveats, and tagging or budget gaps.
- A completion report in the contract's format.

## Guardrails

Label every estimate and never present one as a bill. Do not buy commitments, resize, stop, delete or reconfigure resources without explicit, scoped authorization. Do not recommend removing multi-AZ capacity, NAT redundancy, backups or security tooling without recording the resilience or security trade-off and its owner. Follow the `aws-cloud-architect-contract` instruction.
