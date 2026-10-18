---
name: azure-workload-and-service-selection
description: Selects Azure compute, containers, serverless, integration, AI, and platform services from workload requirements, operational fit, limits, and Well-Architected trade-offs.
---

# Azure Workload and Service Selection

Map workload characteristics to a small set of viable Azure services: ownership, runtime, state, scaling, latency, deployment, tenancy, compliance, regional availability, support, quotas, and cost. Compare App Service, Functions, Container Apps, AKS, VMs/VMSS, Batch, and managed PaaS deliberately.

For application platforms, cover ingress, identity, configuration, secrets, background work, integration, messaging, cache, database, storage, backup, observability, and deployment slots/revisions. For AI/data workloads, include model/data boundary, private access, quotas, responsible-AI constraints, and operator ownership.

Do not select a named service solely because it is familiar or appears in a reference architecture. Cite current official guidance for version-sensitive limits, availability, SKU behavior, and deprecation risk.
