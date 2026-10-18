---
name: aws-networking-hybrid-and-edge
description: Design and troubleshoot AWS VPC, routing, segmentation, Transit Gateway, Direct Connect, VPN, PrivateLink, DNS, CloudFront, and edge connectivity.
---

# AWS Networking, Hybrid, and Edge

Use this Skill for VPCs, subnets, route tables, security groups, NACLs, NAT, endpoints, TGW, VPC peering, Cloud WAN, Direct Connect, Site-to-Site VPN, Route 53, CloudFront, Global Accelerator, WAF, and hybrid connectivity.

## Design

Define CIDR ownership and non-overlap, AZ placement, public/private/data subnet intent, route propagation, inspection points, DNS resolution, egress, ingress, and failure behavior. Security groups are stateful allow rules; NACLs are stateless subnet controls. A public subnet is determined by routing, not its name.

Choose VPC peering for limited non-transitive relationships, Transit Gateway for hub-and-spoke multi-account routing, PrivateLink for one-way private service exposure, Direct Connect for predictable private connectivity, and VPN for encrypted internet paths or backup. Validate route tables and asymmetric paths, not just attachments.

## Edge and cost

Distinguish CloudFront, Route 53, Global Accelerator, ALB/NLB/GWLB, API Gateway, WAF, and Shield roles. Make NAT, cross-AZ, cross-Region, hybrid, and internet egress visible; use endpoints or service-local paths when they meet the security and cost requirements. Validate current quotas, regional support, and pricing before sizing.
