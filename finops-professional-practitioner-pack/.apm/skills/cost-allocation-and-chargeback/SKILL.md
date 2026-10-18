---
name: cost-allocation-and-chargeback
description: Design and run cloud cost allocation, covering the account hierarchy, tag and label taxonomy, enforcement at creation, shared-cost and Kubernetes allocation, unallocated spend, and the progression from showback to chargeback with reconciliation and disputes. Use when costs must be attributed to teams, products, environments or customers, tag coverage is low or drifting, or a showback or chargeback model is being designed, rolled out, audited or disputed.
---

# Cost Allocation and Chargeback

## Purpose and activation

Give every unit of spend an accountable owner through an allocation model that teams can audit and Finance can reconcile. This covers the Allocation capability (Understand Usage and Cost) and Invoicing and Chargeback (Manage the FinOps Practice).

Activate when someone asks who owns a cost, why a report says "unallocated", how to tag, how to split a shared platform, how to bill teams, or why a team rejects its charges.

## Scope and exclusions

In scope: account, subscription and project hierarchy; tag and label taxonomy and value rules; policy-as-code that enforces tags at creation (drafts); coverage measurement and remediation campaigns; shared-cost pools and allocation keys; Kubernetes cluster cost allocation; external allocation mappings; showback reports; chargeback policy, cadence, true-ups and disputes; reconciliation of allocated totals to the invoice.

Out of scope: running the general ledger or posting journal entries (Finance does, from an approved file); unit cost per business output (forecasting-and-unit-economics); applying policies or retagging resources, which is Level 2.

## Required inputs

- The organizational structure the allocation must express (business units, cost centers, teams, products, environments, customers) and who maintains it.
- The current hierarchy (billing accounts, sub accounts, management groups, folders) and any existing taxonomy.
- Billing data with Tags for at least one full month, and the coverage it shows.
- Shared services and platforms (networking, observability, security tooling, CI/CD, support plans, shared clusters) and any usage metrics available for them.
- Finance's requirements: chart of accounts, close calendar, materiality threshold, whether charges will reach profit and loss.

## Dependencies and tools

Read tools for billing data and infrastructure code; a shell for queries when available. Provider policy services (AWS Organizations tag policies and service control policies, Azure Policy, Google Cloud organization policies and label rules in infrastructure code), admission controllers for Kubernetes and CI checks are drafted here, not applied. Kubernetes allocation data comes from what the cluster already exposes (OpenCost or a commercial equivalent, or the provider's split cost allocation). `allocation-methodology-template.md` in this skill folder is the one-page methodology structure.

## Workflow

1. Build on the hierarchy first. Account, subscription and project boundaries are the most durable allocation signal; map them to owners before relying on tags.
2. Define a short taxonomy: a handful of mandatory keys (typically owner or team, cost center, environment, application or product) with allowed values and exact spelling. Placeholder values such as `unknown` count as untagged.
3. Measure coverage as the share of usage EffectiveCost, excluding corrections, carrying valid values for each mandatory key. Trend it weekly by billing account and service category. Use creation events to find owners of untagged resources.
4. Enforce at creation, not afterwards. Prefer deny over warn for mandatory keys, with an exception path that has an owner and an expiry date. Use inheritance from account or project where the provider supports it. Apply the same rules to non-production, which often carries a large share of spend.
5. Where reorganizations are frequent, keep the mapping from stable identifiers (BillingAccountId, SubAccountId, project or resource group) to the organization in an external table that can change without retagging.
6. Allocate shared costs pool by pool. For each pool, name the owner, the key (a measured usage driver such as requests, CPU hours or bytes is more defensible than a fixed ratio, and an even split is least defensible) and the review date. Socialize keys with the receiving teams before publishing. Look for network cost spread across storage, database and load-balancing lines, not only the networking category.
7. Allocate Kubernetes clusters from node cost to workloads using both requests and actual usage, show idle and system capacity as an explicit line rather than hiding it inside teams, and map namespaces and labels to the same taxonomy as the rest of the estate.
8. Allocate EffectiveCost so prepaid commitments land on the workloads that consumed them. Make the result complete and exclusive: team totals plus an explicit unallocated line equal the total. Reconcile the underlying BilledCost to the invoice for Finance.
9. Move through the maturity steps deliberately: visibility, then showback, then soft chargeback (charges affect budgets), then hard chargeback (charges reach profit and loss). Before any chargeback, require several months of consistent showback, a methodology signed off by Finance and engineering leaders, a dispute process, small and visible unallocated spend, and a parallel run in which showback and chargeback agree. Charge monthly with periodic true-ups.
10. Treat disputes as data-quality input. Publish each dispute and its resolution. If teams reject charges broadly, pause chargeback, return to showback, fix the cause and restart on a published timeline.

Maturity guide: at Crawl, hierarchy-based showback and a coverage report. At Walk, enforced taxonomy, documented shared-cost keys and soft chargeback. At Run, external allocation mappings, usage-driven keys for shared platforms and chargeback that Finance books without rework.

## Output

- A one-page allocation methodology built from `allocation-methodology-template.md`.
- The taxonomy with allowed values and the enforcement plan (policy-as-code drafts, not applied).
- A coverage report with the query used, by billing account and service category.
- A showback report draft per team, environment and product, with the unallocated line visible.
- For chargeback: entry criteria status, cadence, true-up rule, dispute process and a rollout plan with dates.

## Validation

- Allocated totals plus unallocated equal the total EffectiveCost for the period.
- The coverage query reruns and yields the same figure.
- Every shared pool has an owner, a key and a data source for that key.
- BilledCost reconciles to the invoice for the same scope.
- Sign-off by Finance and engineering leadership is recorded as passed only when it actually happened; until then it is unverified.
- Policy drafts were evaluated against existing resources in a non-production scope, or are reported as untested.

## Failure handling and escalation

- No owner can be identified: report the resource and spend as unallocated; never assign an owner by guess.
- Coverage below the organization's threshold: lead with remediation; team-level showback on that data carries a visible caveat.
- A key cannot be measured: use a documented proxy, label it as such and schedule a review.
- A team disputes a charge: record it, recompute with the team's evidence, and escalate unresolved disputes to the methodology owners rather than overriding them.
- Pressure to start chargeback before the entry criteria are met: present the risk and the criteria; the decision belongs to the sponsor.

## Permissions and guardrails

Read and draft only. Applying tag or organization policies, retagging resources, changing allocation rules in a shared tool, publishing showback or chargeback to teams and sending figures to Finance systems are Level 2. Allocation reports name teams and their spend; share them only with the agreed audience. Installed without the rest of the pack, treat every change to shared systems and every distribution of figures as requiring explicit human approval.

## Workflow connection

Within the full pack, the `design-allocation-model.prompt.md` recipe starts this workflow, focus-billing-data-analysis supplies coverage and reconciliation queries, and finops-evidence-reviewer checks the model before publication. The `finops-professional-practitioner-contract` instruction supplies the approval, handoff and completion rules. Installed alone, the skill is complete on its own.
