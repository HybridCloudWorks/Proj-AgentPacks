---
description: "Build or refresh a driver-based cloud cost forecast or budget with scenarios and a backtest"
argument-hint: "scope, horizon, drivers available, Finance calendar"
agent: finops-professional-practitioner
---

# Build a cost forecast

## Inputs

The scope and horizon, cost history split by pricing category and charge frequency, business drivers from an authoritative system, known events and the granularity Finance needs.

## Workflow

Apply forecasting-and-unit-economics. Separate committed, recurring, usage-based and one-time spend, model usage as driver times unit cost, work in cost per day, build base, upside and downside scenarios with intervals, backtest on a held-out period, and layer known events. For budgets, set them at accountable scopes with owners. Ask finops-evidence-reviewer to check the model before it reaches Finance.

## Expected output

The forecast with drivers, assumptions, scenarios, intervals and backtest error, a variance explanation if refreshing, any budget proposal with owners, and the completion report from the `finops-professional-practitioner-contract` instruction. Publishing into Finance systems is Level 2.
