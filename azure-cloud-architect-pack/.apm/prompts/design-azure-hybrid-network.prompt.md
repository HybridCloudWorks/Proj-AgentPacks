---
description: "Design Azure hybrid and edge networking: hub-spoke or Virtual WAN, ExpressRoute or VPN, Private Link, DNS, ingress and egress"
agent: azure-cloud-architect
---

# Design Azure hybrid and edge networking

## Inputs

Address plans or IPAM records, on-premises sites with bandwidth and latency needs, existing circuits and gateways, the current DNS design, inspection and egress requirements, PaaS services that need private access, intended public exposure, regions, and who operates each network component. Mark overlapping or unallocated address space as a finding, not an assumption.

## Workflow

1. Apply `azure-architecture-foundations` to fix the subscriptions, regions and network boundaries in scope and who owns them.
2. Apply `azure-networking-hybrid-and-edge`: define address ownership and non-overlap, routing domains, trust zones, DNS resolution, ingress, egress, inspection and failure domains before choosing topology. Choose hub-spoke or Virtual WAN from scale, routing, connectivity and operating requirements. Evaluate ExpressRoute, site-to-site and point-to-site VPN, firewall or NVA, Front Door, Application Gateway, Load Balancer, NAT Gateway, DDoS, NSG and ASG, UDR, route propagation and forced tunnelling. Distinguish service endpoints from private endpoints and centralized private DNS. Check transitive routing and asymmetric paths.
3. Apply `azure-security-identity-and-compliance` for trust zones, inspection points and public exposure.
4. Apply `azure-resilience-dr-and-migration` for connectivity failure domains, such as a backup path when a circuit fails.
5. Apply `azure-cost-sustainability-and-finops` to model firewall, NAT, Private Link, gateway, circuit and cross-zone or cross-region transfer cost.
6. Apply `azure-docs-mcp-and-evidence` to quotas, supported regions, SKU limits and routing behaviour that the design relies on.
7. Apply `azure-architecture-handoff-and-adr` to record the topology decision and its alternatives.

Do not change routes, peerings, gateways, DNS zones or firewall rules. Design them and name the approval each change needs.

## Expected output

- An address and routing plan, a DNS resolution path for private endpoints and on-premises names, and the ingress and egress paths, each labelled with evidence.
- A connectivity ADR with alternatives and its revisit trigger.
- `REQ.md`, `TOPOLOGY.json`, `CONSTRAINTS.json` and `ADR.md`, and a completion report.

Follow the `azure-cloud-architect-contract` instruction: report every contract section, label evidence, and state what was not verified. Existing authorization applies only within its stated scope.
