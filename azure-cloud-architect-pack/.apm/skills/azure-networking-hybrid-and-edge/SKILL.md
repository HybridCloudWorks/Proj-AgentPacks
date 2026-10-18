---
name: azure-networking-hybrid-and-edge
description: Designs Azure VNets, hub-spoke or Virtual WAN, routing, NSGs, Azure Firewall, Private Link, DNS, ExpressRoute, VPN, edge, ingress, and hybrid connectivity.
---

# Azure Networking, Hybrid, and Edge

Define address ownership, non-overlap, routing domains, trust zones, DNS resolution, egress, ingress, inspection, failure domains, and operational ownership before drawing a network. Choose hub-spoke or Virtual WAN from scale, routing, connectivity, and operating requirements rather than habit.

Evaluate ExpressRoute, site-to-site VPN, point-to-site, SD-WAN, Azure Firewall/NVA, Front Door, Application Gateway/WAF, Load Balancer, NAT Gateway, DDoS, NSG/ASG, UDR, route propagation, and forced tunneling. Make public exposure explicit.

For PaaS, distinguish service endpoints from Private Link/private endpoints and centralized private DNS. Place private endpoints with the resource lifecycle unless governance requires otherwise. Validate quotas, supported regions, transitive routing, asymmetric paths, and DNS behavior against current docs.
