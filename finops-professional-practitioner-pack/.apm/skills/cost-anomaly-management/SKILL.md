---
name: cost-anomaly-management
description: Detect, triage and explain unexpected cloud spend changes and tune budget alerts with segment-level, seasonality-aware detection, masked-anomaly checks, root-cause tracing to line items, owner routing and alert precision tracking. Use when spend moved unexpectedly, an anomaly or budget alert fired or is too noisy, anomaly detection or budget alerting is being set up or tuned, or new spend appears in an unexpected service, account or region.
---

# Cost Anomaly Management

## Purpose and activation

Find unexpected spend while it is still cheap to fix, explain it with evidence, and get it to the person who can act. Keep the alerting layer small enough that people trust it. This covers the Anomaly Management capability and the alerting side of Budgeting.

Activate for: "why did spend jump", "this alert fired", "our alerts are noise", "set up anomaly detection", "budget alert design", "unexpected charges in a region we do not use".

## Scope and exclusions

In scope: triage and root cause of a specific movement; detector design for segments; seasonality handling; masked anomalies, where a rise in one place and a fall elsewhere cancel out in totals; new-service and new-region signals; budget alerts based on trajectory; routing, ownership and response times; alert precision reviews; tuning or retiring alerts.

Out of scope: setting budget amounts (forecasting-and-unit-economics); fixing the underlying waste (workload-optimization); investigating a security incident, which belongs to the security team once a suspicious pattern is raised. Creating or changing monitors in a shared account is Level 2.

## Required inputs

- The movement or alert: segment, period, magnitude and where it was observed.
- Daily billing history for the segment and its neighbours, ideally 60 to 90 days, with EffectiveCost and usage quantities.
- Change context where available: deployments, commitment purchases or expirations, price changes, migrations, incidents.
- For detector design: the accountability structure (who can act on which segment), existing alerts with their firing and acknowledgement history, and the channels each team watches.

## Dependencies and tools

Billing data queries (focus-billing-data-analysis supplies the patterns); provider monitoring metrics for usage confirmation; provider-native anomaly features where the organization uses them, configured by their owners. A shell for local statistics when available. This skill installs and configures nothing.

## Workflow

### Triage a movement

1. Confirm it in the billing data, not only in a dashboard.
2. Rule out data artifacts: late or restated data, corrections (ChargeClass), one-time purchases (ChargeCategory Purchase, ChargeFrequency One-Time), credits ending, and month length.
3. Segment to accountability: ServiceCategory by SubAccountId by region by owner tag, then down to ResourceId and SKU.
4. Split the change into usage (PricingQuantity) and rate (effective unit price). A rate change with flat usage points to pricing, commitment coverage or discounts; a usage change points to workload behaviour.
5. Check for masking: compare segment-level movements with the total. A commitment purchase that lowers one workload's cost can hide a new workload's spend; report both as separate events.
6. Correlate with change events and name the most likely cause, labelled as inference until confirmed by the owner.
7. Classify: expected and intentional, waste, error or misconfiguration, or suspicious. Spend in a region or service the organization does not use, sudden large compute or egress, or new accounts can indicate compromised credentials; tell the user at once and recommend notifying security, keeping the evidence intact.
8. Quantify the daily run rate and the exposure if nothing changes, as a range.
9. Prepare a routed message for the owner with segment, magnitude, expected against observed, direction, top drivers, likely cause and the decision needed. Sending it is Level 2.

### Design or tune detection

1. Segment at the level where someone can act; payer-level alerts rarely lead to action.
2. Baseline on EffectiveCost, regular charges only, over 30 to 90 days.
3. Account for weekly and monthly seasonality, for example by comparing each day with the same weekday in earlier weeks or with a seasonal decomposition. Prefer robust statistics (median and median absolute deviation) so one earlier spike does not widen the band.
4. Alert on direction as well as size; a sudden drop can mean an outage or a broken autoscaler.
5. Add a minimum absolute change so small segments do not page anyone, and a separate rule for any new service or region above a small floor.
6. Backtest on history: how many alerts would have fired and how many mattered. Dry-run for a week before routing to people.
7. Give every alert an owner, a channel and a response time. Track precision (alerts acted on divided by alerts fired) and review it monthly with owners; tune or retire alerts that fail the target the owners agreed.

### Budget alerts

Alert on trajectory ("at the current daily run rate this scope exceeds its budget by X around date Y") rather than on a fixed percentage on a fixed day. Compute run rate from EffectiveCost excluding corrections and reconcile to BilledCost at invoice time. One alerting channel per severity tier.

Maturity guide: at Crawl, a trajectory alert per major scope and a monthly review. At Walk, segment-level detection on the largest movers with precision tracking. At Run, routing with context bundles, response-time targets and precision targets per segment.

## Output

- Anomaly report: segment, period, observed and expected, direction, size as amount and as score or percentage, drivers that account for the change, classification, owner, daily exposure range, recommended action with its approval level.
- Detector or alert proposal: segments, baseline, seasonality method, thresholds, floors, owners, channels, backtest results.
- Alert hygiene review: alerts fired, acted on, precision, alerts to retire.

## Validation

- The movement is reproduced from billing data with the query recorded.
- Drivers listed add up to the observed change within a stated tolerance.
- The baseline window and the seasonality treatment are stated.
- A detector proposal includes a backtest; untested thresholds are reported as unverified.

## Failure handling and escalation

- Under four weeks of history: use simple floor and new-service rules, and say that seasonal detection is not yet possible.
- Volatile segment: aggregate one level up or lengthen the window instead of lowering the threshold.
- Owner unknown: report the segment as unowned and route the allocation gap to cost-allocation-and-chargeback.
- Suspected compromise: escalate to the user immediately with the evidence; do not attempt containment.
- Cost still accruing fast: present the containment options to the owner with their trade-offs; acting on resources is Level 2.

## Permissions and guardrails

Read and draft only. Never stop, delete or resize resources to contain spend, and never create, mute or delete monitors or budgets in shared accounts, without explicit approval. Routing messages and notifying security are actions the user takes or approves. Installed without the rest of the pack, treat every change to resources, alerts or communications as requiring explicit human approval.

## Workflow connection

Within the full pack, the `investigate-cost-anomaly.prompt.md` recipe starts this workflow and finops-data-analyst can run the segment queries. The `finops-professional-practitioner-contract` instruction supplies the approval, handoff and completion rules. Installed alone, the skill is complete on its own.
