---
name: workload-optimization
description: Find, prioritize and safely realize usage savings across idle and orphaned resources, rightsizing, storage lifecycle, network and data transfer, Kubernetes requests and autoscaling, serverless and spot patterns, scheduling and cost-aware architecture, with carbon as a fourth trade-off. Use when looking for waste or savings opportunities, reviewing an architecture or change for cost, planning cleanup or rightsizing, or tracking realized savings and carbon impact.
---

# Workload Optimization

## Purpose and activation

Reduce what is consumed without breaking what the business depends on, and prove the saving afterwards. This covers Workload Optimization, Architecting for Cloud and Cloud Sustainability in the Optimize Usage and Cost domain.

Activate for waste hunts, rightsizing, "why is this so expensive", architecture or pull request cost review, cleanup campaigns, non-production scheduling, Kubernetes efficiency, serverless or spot questions, savings tracking and carbon questions.

## Scope and exclusions

In scope: candidate discovery from billing and utilization data; classification and prioritization; rightsizing compute, databases and containers; idle and orphaned resources; storage classes, lifecycle and snapshots; data transfer and network topology; Kubernetes requests, limits, autoscaling and node efficiency; serverless sizing; spot and preemptible suitability; schedules; architecture cost review at different scales; realized-savings tracking; carbon per unit of work.

Out of scope: the rate paid (rate-optimization), allocation of the result (cost-allocation-and-chargeback). Executing any change to resources is Level 2 and belongs to the workload owner.

## Required inputs

- Billing data at ResourceId level for at least 30 days, regular charges only.
- Utilization metrics from the provider's monitoring for the same resources and a window that includes business peaks (month-end, campaigns, batch runs).
- Ownership: tags or the allocation mapping, and the owner's contact route.
- Constraints: service-level objectives, disaster recovery and compliance retention rules, change windows, data residency.
- For architecture review: the design or the diff, expected load at 1x, 10x and 100x, availability targets.

## Dependencies and tools

Billing queries (focus-billing-data-analysis), provider monitoring and inventory exports supplied by the user or read through tools already configured, Kubernetes cost data the cluster already exposes, and provider carbon tools (AWS Customer Carbon Footprint Tool, Google Cloud Carbon Footprint, the Microsoft Emissions Impact Dashboard). `waste-pattern-catalog.md` in this skill folder describes recurring patterns, their two detection signals and their safe fixes. Nothing is installed by this skill.

## Workflow

1. Build the candidate list from billing (EffectiveCost by ResourceId and ServiceCategory) joined to utilization. Require two independent signals before calling anything idle, for example CPU and network for compute, or traffic and healthy targets for a load balancer.
2. Exempt and label resources that are idle by design: disaster recovery standby, failover targets still referenced in DNS, scheduled scanners, legal holds, subnets that route management traffic through a gateway.
3. Classify each candidate as obvious, likely or possible, and prioritize by monthly cost times confidence divided by effort and risk.
4. Apply the pattern rules.
   - Compute and databases: size from a window of at least 30 days that covers peaks, using high percentiles (around p95 for CPU, p99 for memory) plus headroom; move one size step at a time; consider newer or ARM-based families where the software supports them; if the instance is covered by a commitment, plan the exchange or modification first.
   - Storage: put lifecycle rules on new data before migrating old data; account for retrieval fees, minimum storage durations and minimum billable object sizes before choosing archive tiers; expire old versions; give snapshots a lifecycle and hold orphaned ones for an agreed period before deletion.
   - Network: look for data transfer charges spread across storage, database replication, load balancing and gateway processing; use flow logs to find source and destination pairs; consider private endpoints, same-zone routing, caching and connection reuse; keep one gateway per zone where availability requires it.
   - Kubernetes: right-size requests to observed usage with headroom before tuning consolidation; keep memory limits; require disruption budgets for workloads with objectives; track requested against provisioned capacity per node; diversify instance types for spot node pools.
   - Serverless: tune memory by measurement, because CPU scales with it; prefer ARM where supported; include downstream calls in the cost; compare containers for steady, high-volume functions.
   - Spot and preemptible: only for interruption-tolerant work that drains within the notice period, spread across instance types and zones, with fallback capacity; never as the only home of a stateful primary.
   - Schedules: stop non-production outside working hours with an owner opt-out.
   - Architecture review: cost at 1x, 10x and 100x load, the managed-service premium, the floor that multi-region adds, and the cost curve of each extra level of availability.
5. Write each recommendation with the owner, the monthly impact range, confidence, the cost, speed, quality and carbon trade-off (state it when it is genuinely negligible), how to reverse it and the approval level.
6. Plan execution for the owner: acknowledgement for likely and possible candidates, a notice tag with a scheduled date, a snapshot or backup before deletion, staged rollout, rollback steps and a change window. Executing it is Level 2.
7. Measure realized savings: cost per day for the changed resources over a baseline window before the change and a stable window after it, normalized for days, reported separately from estimates. Only realized savings count toward targets.
8. Report carbon with the providers' own data, per unit of work as well as in total, location-based and market-based where both exist. Region choice is often the largest lever when latency and data residency allow; rightsizing and idle cleanup reduce cost and carbon together. Never claim reductions from purchases of renewable energy certificates the organization did not make.

Maturity guide: at Crawl, a quarterly hunt on the obvious tier with manual owner notification. At Walk, lifecycle policies, tag-driven notice periods and rightsizing at scale with owner sign-off. At Run, continuous detection, automated handling of the obvious tier under an approved policy, and cost checks in design and pull request review.

## Output

- An optimization inventory: resource, pattern, signals, classification, monthly cost, impact range, owner, trade-off, reversibility, approval level.
- Execution plans per change with rollback.
- A realized-savings tracker with baseline and post-change cost per day.
- An architecture cost review with scale scenarios and alternatives.
- Carbon figures per unit where data exists.

## Validation

- Every candidate cites two signals and the windows used.
- Estimated impact is a range derived from EffectiveCost for the resource.
- Realized savings use day-normalized windows before and after, with the resources changed listed.
- Exemptions are recorded with the reason.
- An estimate that has not been measured is labelled estimated.

## Failure handling and escalation

- Owner unknown: tag-and-notify plan only; no deletion proposal until an owner acknowledges or the organization's notice period passes under an approved policy.
- Metrics missing or too short: classify as possible and request a longer window.
- Commitment or license coupling: route to rate-optimization before resizing.
- Objective at risk: present the trade-off and let the owner decide; do not push below a safe margin.
- Rollback impossible (for example deleting data): require a backup and an explicit approval that names the data.

## Permissions and guardrails

Read and recommend. Stopping, deleting, resizing, rescheduling, retagging and applying infrastructure changes are Level 2, owned by the workload owner. Never delete without a recoverable copy unless the owner explicitly approves losing the data. Installed without the rest of the pack, treat every change to resources as requiring explicit human approval.

## Workflow connection

Within the full pack, the `find-optimization-opportunities.prompt.md` recipe starts this workflow, `estimate-workload-cost.prompt.md` uses its architecture review, and finops-evidence-reviewer checks savings claims. The `finops-professional-practitioner-contract` instruction supplies the approval, handoff and completion rules. Installed alone, the skill is complete on its own.
