---
name: gcp-network-design
description: "Design Google Cloud networks - VPC topology and Shared VPC, IP planning for VMs, GKE and Cloud Run, private access to Google and producer services, hybrid and cross-cloud connectivity, DNS, load balancing and edge security, egress control, and read-only path diagnosis. Use when planning or reviewing VPCs, subnets, connectivity, load balancers, firewall models or a network path problem on Google Cloud."
---

# Google Cloud Network Design

## Purpose and activation

Produce a network that is private by default, has room to grow, and whose Day-0 choices (ranges, topology, cluster networking) are made on purpose. Activate for new environments, VPC or subnet planning, hybrid or multicloud connectivity, internet-facing frontends, private service access, GKE or serverless networking, egress control, or a connectivity problem.

## Scope and exclusions

In scope: topology, IP plan, private access, hybrid connectivity, DNS, load balancer and edge choice, firewall and egress model, network telemetry and read-only diagnosis. Perimeters and identity-based controls are covered with gcp-security-controls; cluster-internal policy with gcp-gke-platform. Creating or changing network resources is out of scope for the agent unless authorized at Level 2.

## Inputs

Environments and workloads, existing VPCs and ranges, on-premises and other-cloud ranges, bandwidth and latency needs, availability target for connectivity, internet exposure and residency constraints, expected node, pod and serverless instance counts, and the teams who own the network.

## Dependencies and tools

[VPC design best practices](https://docs.cloud.google.com/architecture/best-practices-vpc-design.md.txt), [landing zone network decision](https://docs.cloud.google.com/architecture/landing-zones/decide-network-design.md.txt), [hub-and-spoke](https://docs.cloud.google.com/architecture/deploy-hub-spoke-vpc-network-topology.md.txt), [hybrid and multicloud secure networking patterns](https://docs.cloud.google.com/architecture/hybrid-multicloud-secure-networking-patterns.md.txt), [load balancer selection](https://docs.cloud.google.com/load-balancing/docs/choosing-load-balancer.md.txt), [private access options](https://docs.cloud.google.com/vpc/docs/private-access-options.md.txt). `scripts/ip_plan.py` in this skill folder checks an IP plan offline (Python 3.10 or later, standard library only).

## Workflow

1. Topology. Default to a Shared VPC per environment (host project in the common folder, workloads as service projects) so network administration stays central and workload teams keep their projects. Use hub-and-spoke (Network Connectivity Center or VPC Network Peering) when spokes need isolation, a shared services hub or centralized network appliances. Remember peering is not transitive and has per-network limits. Use separate VPCs only for hard isolation boundaries.
2. IP plan. Allocate non-overlapping ranges across all environments, on-premises and other clouds that may ever connect. Size primary subnets per region with growth room; each primary IPv4 range loses four addresses to the platform. For GKE, plan the Pod and Service secondary ranges: each node takes a Pod range sized to twice its maximum Pods rounded up to a power of two (48 Pods per node uses a /25, 110 uses a /24), so the Pod range caps the node count. For Cloud Run Direct VPC egress, budget roughly two addresses per instance. When RFC 1918 space is short, use RFC 6598 (`100.64.0.0/10`) or Class E (`240.0.0.0/4`) ranges where every component supports them, and plan dual-stack. Write the plan as JSON and run `python scripts/ip_plan.py plan.json`; fix every error before recording the plan as a decision.
3. Private access. Enable Private Google Access on subnets with private workloads; for perimeter or restricted designs, map `*.googleapis.com` in a private Cloud DNS zone to `restricted.googleapis.com` (`199.36.153.4/30`) or `private.googleapis.com` (`199.36.153.8/30`). Use Private Service Connect endpoints for Google APIs and for producer services (Cloud SQL, AlloyDB, partner and your own published services) to avoid peering and range coordination; use private services access only where the producer requires it. Serverless workloads reach the VPC through Direct VPC egress, which scales to zero, in preference to Serverless VPC Access connectors.
4. Hybrid and cross-cloud. Choose Dedicated or Partner Interconnect for bandwidth and predictable latency, HA VPN for lower bandwidth or as backup, Cross-Cloud Interconnect to other clouds; follow the documented redundant topology for the availability you need (connections in two metros and Cloud Routers in two regions for the highest tier). Use Cloud Router with BGP, plan custom route advertisements and MTU, and decide whether Network Connectivity Center provides transit.
5. DNS. Private zones per environment, forwarding zones and inbound server policies for on-premises resolution, DNS peering from service projects to the host, and zones for Private Service Connect endpoints.
6. Edge and load balancing. Pick the load balancer from client location, protocol, proxy or passthrough, and where TLS may terminate (a regional external Application Load Balancer keeps termination in-region for residency). For internet frontends, per backend workload type:
   - Static objects: cache all static content with long TTLs, compression, negative caching and serve-while-stale.
   - Cacheable read-only APIs: honour origin cache headers, include query strings in the cache key, apply Cloud Armor preconfigured OWASP rules and per-client rate limiting.
   - Transactional endpoints (login, checkout, account changes): bypass the cache, apply strict rate limits, OWASP rules and bot management.
   - Server-rendered pages: honour origin headers and bypass the cache when session cookies are present.
   Derive rate-limit thresholds from measured traffic; use Google-managed certificates through Certificate Manager; restrict backend ingress so traffic cannot bypass the load balancer.
7. Firewall and egress. Use hierarchical and global network firewall policies with secure tags or service accounts as targets, a default-deny posture with explicit allows, logging on rules that matter, and Cloud NGFW features (FQDN, geolocation, threat intelligence, intrusion prevention) where required. Private workloads reach the internet only through Cloud NAT, with port allocation sized for connection rates, or through Secure Web Proxy where egress must be filtered by destination.
8. Telemetry. Plan VPC Flow Logs (sampling and metadata settings, and their cost), firewall rules logging, Cloud NAT logs and Network Intelligence Center.
9. Diagnosis of an existing path, read-only first: describe routes, firewall policies and instance state; query firewall and NAT logs (prefer a BigQuery linked dataset for aggregation, dry-run the query first because queries bill); read metrics. Present the direct answer as soon as one source is conclusive, including "no traffic", instead of chasing discrepancies between sources. A Connectivity Test creates a resource in the project: propose it as a Level 2 step, and when approved, delete it afterwards and show the deletion output. A `REACHABLE` result is static analysis; also confirm that the endpoints are running.

## Output

Topology diagram, IP plan with `scripts/ip_plan.py` results, private access and DNS design, hybrid connectivity design with its redundancy tier, load balancer and edge configuration per backend, firewall and egress model, telemetry plan, decision records for Day-0 choices and a validation plan.

## Validation

`scripts/ip_plan.py` reports no errors and its capacity summary covers the expected node, Pod and instance counts. Every flow in the diagram has an explicit firewall allow and a route. No backend is reachable around its load balancer. Read-only checks on a named project: `gcloud compute networks subnets list --project=PROJECT_ID --format="json(name,region,ipCidrRange,secondaryIpRanges)"`, `gcloud compute firewall-rules list --project=PROJECT_ID`, `gcloud compute routers get-status ROUTER --region=REGION --project=PROJECT_ID`.

## Failure handling and escalation

Overlapping ranges with an existing network: stop and present renumbering or translation options (Hybrid NAT, Private Service Connect) instead of silently accepting the overlap. Unknown on-premises ranges: block the IP plan as BLOCKED_ON_HUMAN_DECISION. A diagnosis needs a resource-creating test or a billable query that has not been approved: return the exact command and wait.

## Permissions and guardrails

Creating or modifying networks, subnets, routes, firewall rules or policies, NAT, VPN, Interconnect attachments, DNS zones, load balancers or Connectivity Tests is Level 2. Never open `0.0.0.0/0` ingress, remove a deny rule or disable logging to make a test pass. Without the pack's contract installed, treat every network change as needing explicit approval.

## Connection to the pack

The optional `design-network.prompt.md` recipe runs this skill; gcp-landing-zone, gcp-gke-platform and gcp-serverless-apps depend on its IP plan and private access model, and gcp-security-reviewer uses it to trace exposure. Installed on its own, this skill still works and the guardrails above still apply. Installed with the pack, it follows the always-on `google-cloud-architect-contract` instruction for approval levels, handoffs and the completion report.
