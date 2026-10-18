# Worked example: a flat total that hid new spend

All figures are synthetic.

**Request.** "Total spend is flat this month but our commitment purchase should have cut it. Why didn't it?" Recipe: `investigate-cost-anomaly.prompt.md`. Skill: cost-anomaly-management.

**Delegation.** The export holds 90 days of hourly rows across 40 sub accounts. The primary delegates the segment queries to finops-data-analyst with: the question, the period (last 90 days), EffectiveCost with `ChargeClass IS NULL`, segmentation ServiceCategory by SubAccountId by RegionId, and the prohibition on any change to resources or monitors.

**Analyst return.** Query text, row counts and these aggregates:

| Segment | Expected per day | Observed per day | Direction |
|---|---|---|---|
| Compute, sa-platform, existing region | 9,400 | 6,200 | drop |
| Compute, sa-research, region not used before | 0 | 3,150 | spike |
| Total | 9,400 | 9,350 | flat |

The drop is the commitment discount applying (PricingCategory changed from Standard to Committed on the same resources). The spike started eleven days ago on large memory-optimized instances in a region the organization has never used.

**Triage.** Usage, not rate, drives the spike: PricingQuantity rose from zero. No deployment record mentions the region. The pattern (new region, large instances, no change record) is consistent with either an unsanctioned experiment or compromised credentials. The primary tells the user immediately, recommends notifying the security team, and advises keeping the resources and logs intact for them.

**Exposure.** About 3,150 per day if nothing changes: roughly 94,500 over a 30-day month or 97,650 over a 31-day month, with about 34,650 already incurred over the eleven days.

**Output.** An anomaly report listing both events separately, the drivers, the classification "suspicious, needs owner confirmation", the sub account owner from the allocation mapping, and a draft message for that owner. Recommended actions: confirm ownership today; if unsanctioned, security leads containment. Stopping the instances is Level 2 and belongs to the owner or security.

**Follow-up.** A detector change is proposed: segment-level detection on ServiceCategory by SubAccountId by RegionId, plus a rule for any new region above 50 per day. A backtest over the 90 days shows it would have alerted on day one of the spike and fired four other times, three of which owners confirmed as real.

**Completion.** Status BLOCKED_ON_APPROVAL for containment (owner and security decisions), with the analysis checks passed. The message was drafted, not sent.
