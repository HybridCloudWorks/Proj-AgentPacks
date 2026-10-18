---
name: forecasting-and-unit-economics
description: Quantify the business value of cloud spend with driver-based forecasts that carry ranges and backtests, budgets, pre-deployment workload and migration estimates, unit economics and a small set of KPIs and benchmarks. Use when someone needs a forecast, budget, variance explanation, cost estimate for a proposed workload or migration, cost per unit of business output, or KPIs and benchmarks for teams or the organization.
---

# Forecasting and Unit Economics

## Purpose and activation

Connect spend to the business drivers behind it so Finance can plan, engineers can see what a design will cost before building it, and leaders can tell growth from inefficiency. This covers the Quantify Business Value domain: Planning and Estimating, Forecasting, Budgeting, Unit Economics, and KPIs and Benchmarking.

Activate for forecasts and reforecasts, budget proposals, variance explanations, "what will this architecture cost", migration business cases, cost per customer or per transaction, and KPI or benchmark requests.

## Scope and exclusions

In scope: forecast models and scenarios; budget proposals at accountable scopes; variance analysis; estimates for new workloads, architecture alternatives and migrations; unit-cost definitions, models and trends; KPI dictionaries; internal and external benchmarking.

Out of scope: budget alert mechanics (cost-anomaly-management); commitment purchase decisions (rate-optimization, which consumes the forecast); revenue figures, which come from Finance or Product systems and are never invented.

## Required inputs

- Daily or monthly cost history, ideally 6 to 12 months, split by PricingCategory and ChargeFrequency.
- Business drivers and their history or plan: users, transactions, data volume, customers, sites, model calls, from an authoritative system.
- Known events: launches, migrations, decommissions, commitment purchases and expirations, price changes, contract renewals.
- For estimates: the proposed design, usage profile (steady and peak), data volumes and growth, availability and region requirements, existing commitments and negotiated rates.
- For unit economics: the candidate unit agreed with Product and Finance, its source system, and the allocation of shared costs.
- The planning calendar and the granularity Finance needs.

## Dependencies and tools

Billing queries from focus-billing-data-analysis; allocation outputs from cost-allocation-and-chargeback for shared costs; official provider pricing pages and calculators read on the date of the estimate; a shell for local modelling when available. Nothing is installed by this skill.

## Workflow

### Forecast

1. Split the history: committed spend (PricingCategory Committed) is largely known; recurring charges are predictable; usage-based spend carries the volatility; one-time charges are listed separately and kept out of the run rate.
2. Model usage-based spend as driver times unit cost wherever a driver exists. Fall back to a time-series baseline only where no driver exists, and label it.
3. Work in cost per day and multiply by days in each target month.
4. Build base, upside and downside scenarios with named driver assumptions, and show prediction intervals rather than a single line.
5. Backtest: hold out the most recent period, forecast it from earlier data and report the error (for example mean absolute percentage error). Agree the acceptable error with Finance; fix the model before shipping if it misses.
6. Layer known events on top and reforecast when a driver changes materially, not only on the calendar.
7. Explain variance as volume, rate, mix, one-time and calendar effects.

### Budget

Derive budgets from the forecast at the scope where an owner is accountable, align them with the finance calendar and the IT budget process, and record the owner. A budget is a target and a forecast is an expectation; keep both visible. Hand alerting to cost-anomaly-management.

### Estimate a workload or migration

1. Write down the reference design with named services, sizes, regions and availability topology.
2. Price each component by ServiceCategory at low, expected and high usage (for example P10, P50 and P90).
3. Price data movement explicitly: internet egress, cross-zone and cross-region transfer, NAT processing, replication, load balancer processing. It is the most commonly missed cost.
4. Include storage growth and retention, backups, observability ingestion and retention, support plans and licensing.
5. Show the managed-service premium against a self-managed option, stated in money, and let the owner decide.
6. Price at on-demand and at the effective rate the organization actually gets with existing commitments.
7. Compare one or two alternatives, with the cost, speed, quality and carbon trade-off for each.
8. For migrations, budget the overlap period when both source and target run, set an exit date for the source, and plan to compare actuals weekly from day one.
9. Name the few assumptions that move the estimate most, and what would change if each is wrong.

### Unit economics

1. Agree the unit with Product and Finance: it should rise and fall with how the business earns or delivers value. One unit per model.
2. The numerator is EffectiveCost attributable to the unit: direct costs plus shared costs allocated by documented keys. Exclude what cannot be traced, and say how much was excluded.
3. The denominator comes from the authoritative business system for the same period.
4. Report unit cost together with volume, segmented by customer tier or cohort where they differ, as a trend. Distinguish average and marginal cost when decisions depend on growth.
5. Publish the methodology next to the number, and add unit cost to launch dashboards for new features.

### KPIs and benchmarks

Choose three to seven KPIs with written definitions, data sources and normalization, preferring established definitions such as those in the FinOps Foundation KPI library (examples: allocation coverage, commitment coverage and utilization, effective savings rate, forecast accuracy, unit cost trend, time to resolve anomalies). Compare teams with their own targets and trends before comparing them with each other, avoid raw-cost leaderboards, compare internally before externally, and date and caveat every external benchmark.

Maturity guide: at Crawl, a spreadsheet driver model and calculator-based estimates with notes. At Walk, a backtested hybrid model, sensitivity tables and one agreed unit metric. At Run, reforecasts triggered by driver changes, estimates in design review and accuracy targets.

## Output

- Forecast: drivers, assumptions, scenarios, intervals, backtest error, known events, variance explanation.
- Budget proposal: scope, owner, amount, basis, review date.
- Estimate: design, P10 to P90 table by ServiceCategory, explicit data-transfer lines, on-demand and effective-rate views, alternatives, sensitivity list.
- Unit economics: unit definition, numerator and denominator sources, allocation method, trend with volume.
- KPI dictionary: definition, formula, source, normalization, owner, target.

## Validation

- The backtest was executed and its error is reported; an unexecuted backtest is unverified.
- Historical totals in the model reconcile to the billing data for the same period.
- Every output is a range or scenario set, with named assumptions.
- Unit denominators reconcile to the business system's own totals.

## Failure handling and escalation

- No history for a new workload: estimate with a wide range and schedule reforecasts at 30, 60 and 90 days.
- No driver data: use a labelled statistical baseline and request the driver feed.
- Fast growth or a structural break: do not trust a pure time series; say so and use drivers or scenarios.
- Pricing uncertain: cite the pricing page and date used, and flag terms that need confirmation.
- Unit disputed: stop modelling until Product and Finance agree; two units produce two different stories.

## Permissions and guardrails

Read and draft only. Publishing forecasts or budgets into Finance systems, or sharing figures beyond the requester, is Level 2. Never invent revenue, headcount or business volumes. Installed without the rest of the pack, treat every publication of figures and every change to shared planning systems as requiring explicit human approval.

## Workflow connection

Within the full pack, the `build-cost-forecast.prompt.md` and `estimate-workload-cost.prompt.md` recipes start this workflow, and finops-evidence-reviewer checks forecasts and estimates before they reach Finance. The `finops-professional-practitioner-contract` instruction supplies the approval, handoff and completion rules. Installed alone, the skill is complete on its own.
