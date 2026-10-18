---
name: gcp-cost-sustainability
description: "Estimate, attribute and optimize Google Cloud cost and carbon - cost drivers per architecture, labels and billing export, budgets and alerts, rightsizing and autoscaling, pricing models such as committed use discounts and Spot VMs, storage lifecycle, network egress, low-carbon regions and Carbon Footprint data. Use when estimating the cost of a design, reviewing spend, planning savings or adding sustainability goals to a Google Cloud workload."
---

# Google Cloud Cost and Sustainability

## Purpose and activation

Tie spend and emissions to business value: know what a design will cost and why, who owns each cost, and which changes save money or carbon without breaking reliability or performance. Activate for design-time estimates, cost reviews, savings plans, FinOps governance, commitment decisions, or sustainability requirements.

## Scope and exclusions

In scope: cost modelling, attribution, governance, optimization levers and their risks, commitment analysis, carbon-aware region and scheduling choices, measurement. Out of scope: purchasing commitments or reservations, changing budgets, deleting resources and negotiating contracts; the agent recommends and the human acts.

## Inputs

Architecture or scope (billing account, folders, projects), billing export or cost reports the user can share, utilization data, workload criticality and its reliability requirements, existing commitments and reservations, growth forecasts, the savings or carbon goal, and residency limits on region choice.

## Dependencies and tools

[Well-Architected cost optimization pillar](https://docs.cloud.google.com/architecture/framework/cost-optimization/printable.md.txt), [sustainability pillar](https://docs.cloud.google.com/architecture/framework/sustainability/printable.md.txt), the Google Cloud Pricing Calculator and each product's pricing page, Cloud Billing reports, billing export to BigQuery, Recommender and Active Assist, FinOps hub, Carbon Footprint and its BigQuery export, and the region picker's carbon data. This skill does not hard-code prices; always read current pricing.

## Workflow

1. Model the design's cost drivers before numbers: compute (per request, per vCPU-second, per node or per pod request), storage (class, location type, operations), databases (edition, HA, replicas, storage, backups), network (internet egress, inter-region and inter-zone traffic, load balancer data processing, Interconnect), logging and monitoring ingestion, AI tokens or provisioned throughput, and licences. Mark which drivers scale with traffic and which are fixed.
2. Estimate with the Pricing Calculator or pricing pages for the chosen regions and editions, state every assumption (traffic, data volume, hours, growth), and give a range with a confidence level instead of a single precise figure.
3. Attribution and governance: require labels (environment, application, owner, cost centre) through IaC and policy, enable billing export to BigQuery (standard, detailed and pricing tables), set budgets with alert thresholds for each project or folder, route budget notifications to owners, and use GKE cost allocation for namespace-level visibility.
4. Optimization levers, each with its risk:
   - Rightsizing from Recommender and utilization data; for GKE, VPA recommendations applied with headroom.
   - Autoscaling and scale to zero (Cloud Run, GKE Autopilot, managed instance groups); schedule non-production shutdowns.
   - Pricing models: resource-based or spend-based committed use discounts for steady baselines, sized from at least a few months of usage and aligned with machine families you will keep; Spot VMs for fault-tolerant batch, CI and stateless replicas with disruption handling (not for single-replica or stateful critical services, and not as the first choice for accelerator inference where startup latency is severe).
   - Storage: Object Lifecycle Management to colder classes, Autoclass, deleting dark data after owners confirm, BigQuery partitioning, clustering, long-term storage pricing and on-demand versus capacity pricing.
   - Network: keep chatty components in the same region and zone where reliability allows, cache at the edge with Cloud CDN, avoid unnecessary cross-region replication, and review NAT and load balancer processing charges.
   - Telemetry: exclusion filters and sampling for high-volume logs, retention matched to need, and metric cardinality limits.
   - Managed and serverless services for new workloads unless a technical constraint rules them out.
5. Sustainability: prefer regions with high carbon-free energy where latency, residency and cost allow; run flexible batch work in lower-carbon regions or periods; scale idle capacity to zero; choose current machine generations and specialized accelerators for better work per watt; prefer cold or on-demand DR environments; measure with Carbon Footprint and join its export with billing data to find hotspots.
6. Rank recommendations by savings, effort and risk, and say which reliability or performance requirement each one touches.
7. Define the measurement plan: the baseline, the metric (cost per transaction, per user or per environment), and the review cadence.

## Output

Cost model with drivers, assumptions and range; attribution and budget design; ranked optimization list (lever, scope, estimated saving with basis, risk, owner, effort); commitment analysis; sustainability recommendations with carbon data sources; measurement plan.

## Validation

Every estimate cites its pricing source and date and lists assumptions; every recommendation names the requirement it could affect; commitment proposals show the usage window they are based on; billing export queries were dry-run and approved before running, and their bytes processed are reported.

## Failure handling and escalation

No billing data available: deliver a design-time estimate and a data request instead of guessed savings. A saving that would breach an SLO or residency requirement: present it as rejected with the reason. Commitment or reservation purchase requested: prepare the analysis and return it for a human purchase decision.

## Permissions and guardrails

Reading billing reports a user shares is Level 0; querying billing export tables is billable and needs approval with a byte budget (dry-run first); changing budgets, labels on live resources, machine types or schedules, purchasing commitments and deleting resources or data are Level 2. Without the pack's contract installed, treat every cost-affecting change as needing explicit approval.

## Connection to the pack

The optional `optimize-cost.prompt.md` recipe runs this skill; gcp-solution-architecture, gcp-migration-planning and gcp-well-architected-review use it for the cost and sustainability pillars. Installed on its own, this skill still works and the guardrails above still apply. Installed with the pack, it follows the always-on `google-cloud-architect-contract` instruction for approval levels, handoffs and the completion report.
