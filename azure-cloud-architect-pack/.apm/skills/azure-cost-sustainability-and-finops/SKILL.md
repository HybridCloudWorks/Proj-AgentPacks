---
name: azure-cost-sustainability-and-finops
description: Embeds Azure cost, unit economics, budgets, tagging, reservations, savings, egress, quota, sustainability, and FinOps controls into architecture decisions.
---

# Azure Cost, Sustainability, and FinOps

Cost an architecture with stated assumptions: region, SKU/tier, quantity, utilization, storage growth, requests, data transfer, logs, backups, licenses, support, and commitments. Use Azure Pricing, Cost Management, Advisor, budgets, exports, tags, reservations, savings plans, and chargeback/showback when current evidence is available.

Model the cost of shared services, NAT/firewalls, Private Link, cross-zone/region transfer, observability, replicas, DR capacity, idle environments, and egress. Tie every cost center to an owner and workload; do not claim an estimate is a quote.

Include sustainability trade-offs such as utilization, region choice, lifecycle, autoscaling, right-sizing, and retention. Governance should prevent unbounded spend without blocking justified exceptions.
