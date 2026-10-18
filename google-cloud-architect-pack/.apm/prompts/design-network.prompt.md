---
description: "Design Google Cloud VPC, hybrid connectivity and load balancing"
agent: google-cloud-architect
---

# Design a Google Cloud network

## Inputs

Environments and workloads to connect, on-premises and other-cloud ranges, bandwidth, latency and availability needs, internet exposure, residency constraints and any existing VPCs or IP plans. Ask for existing ranges before allocating new ones.

## Workflow

Apply gcp-network-design. Choose the VPC topology, private access pattern, hybrid connectivity, DNS model and load balancer type from the requirements; build an IP plan and check it for overlaps and GKE or Cloud Run capacity with the skill's IP plan checker; specify firewall and egress controls with gcp-security-controls. Diagnose an existing path only with read-only evidence unless creating a Connectivity Test has been approved.

## Expected output

Topology diagram, IP plan with check results, connectivity and DNS design, load balancing and edge security choices, firewall and egress model, decision records for Day-0 choices and a validation plan. Apply the `google-cloud-architect-contract` instruction.
