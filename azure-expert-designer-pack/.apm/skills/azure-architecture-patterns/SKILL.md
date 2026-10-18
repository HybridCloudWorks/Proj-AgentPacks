---
name: azure-architecture-patterns
description: Model common Azure architecture patterns such as private networking, AKS, serverless, analytics, CI/CD, landing zones, hybrid connectivity, and multi-region designs without misleading flows.
---

# Azure Architecture Patterns

Use this Skill when a diagram needs a recognizable Azure architecture pattern or a review of whether a pattern is represented honestly.

## Pattern checks

- Serverless web: show entry, compute, identity/secrets, data, observability, and private connectivity only where configured.
- VNet and private endpoint: distinguish subnet placement, private endpoint NIC, private DNS resolution, and the target PaaS resource. A private endpoint is not the same thing as a service endpoint or an inbound route.
- AKS: separate control plane, node pools, ingress, workload identity, network policy, service-to-service flow, and managed dependencies. Do not draw every Kubernetes object as an Azure resource.
- Data and analytics: show ingestion, processing, storage, serving, governance, and sensitivity boundaries; distinguish batch, streaming, and replication.
- CI/CD: show source, build, artifact, deployment identity, environment gates, and target subscriptions/resource groups; do not imply that a pipeline is a runtime dependency.
- Landing zone and governance: show management groups, policy, role assignments, subscriptions, and network topology as separate layers.
- Hybrid and multi-region: label routing, latency, failover authority, replication direction, and active/active versus active/passive. Do not imply that a global edge service automatically replicates or moves database traffic.

Use the supplied basic and advanced templates as pattern references, then adapt to actual source evidence and record deviations.
