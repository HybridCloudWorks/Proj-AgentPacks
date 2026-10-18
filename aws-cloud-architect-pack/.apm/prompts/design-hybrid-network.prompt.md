---
description: "Design or choose AWS network, hybrid and edge connectivity: VPC layout, Transit Gateway, peering, PrivateLink, Direct Connect, VPN, DNS and egress"
agent: aws-cloud-architect
---

# Design hybrid and edge connectivity

## Inputs

- Sites, accounts and VPCs to connect, with their CIDR ranges and owners.
- Bandwidth, latency, encryption and availability requirements for each path.
- Inspection, segmentation and egress policy, and any traffic that must stay private.
- DNS model: on-premises resolvers, private hosted zones, split-horizon needs.
- Traffic volumes by path, so transfer and processing costs can be modelled.
- Current routing evidence: route tables, attachments, propagation settings, existing VPN or Direct Connect.

## Workflow

1. `aws-architecture-foundations`: scope the connectivity problem and the failure the user is trying to avoid.
2. `aws-networking-hybrid-and-edge`: CIDR ownership and non-overlap, AZ placement, subnet intent, route propagation, inspection points, DNS resolution, ingress and egress. Compare the plausible options (peering, Transit Gateway, PrivateLink; Direct Connect, Site-to-Site VPN, or both) and say why each rejected one was rejected.
3. `aws-security-identity-and-compliance`: security groups, NACLs, encryption in transit, endpoint policies and inspection coverage.
4. `aws-resilience-dr-and-migration`: failure domains of each link, location and attachment, and the failover behavior when one fails.
5. `aws-cost-sustainability-and-finops`: NAT, cross-AZ, cross-Region, hybrid, endpoint and attachment cost-bearing paths.
6. `aws-docs-mcp-and-evidence`: verify quotas, regional support and pricing before sizing.
7. `aws-architecture-handoff-and-adr`: TOPOLOGY with routes and attachments, CONSTRAINTS with CIDR and egress rules, and an ADR for the connectivity choice.

## Expected output

- A connectivity design with route tables per segment, DNS resolution paths, inspection points and egress design.
- An option comparison covering security, resilience, operations and cost.
- Failure behavior per link, including asymmetric-routing risks, and a list of cost-bearing paths.
- The handoff artifacts and a completion report in the contract's format.

## Guardrails

Validate route tables and return paths, not just attachments. Do not change routes, attachments, VPN or Direct Connect configuration, security groups or DNS without explicit, scoped authorization and a rollback plan. Follow the `aws-cloud-architect-contract` instruction.
