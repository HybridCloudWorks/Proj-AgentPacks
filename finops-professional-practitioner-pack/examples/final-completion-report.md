# Worked completion report

Synthetic. This illustrates the report format from the pack contract; it is not a claim about any real dataset.

**Status:** PREPARED_NOT_VERIFIED

**Outcome.** A Q3 forecast for three products with base, upside and downside scenarios. The backtest could not run because the July export is incomplete.

**Audience.** Finance planning.

**Scope.** Billing accounts ba-001 and ba-002, all providers in the conformed dataset, forecast horizon July to September.

**Data sources.** FOCUS 1.2 conformed table, charge periods January to June, extracted 2 July; product volumes from the analytics warehouse, same months.

**Cost basis.** EffectiveCost; ChargeCategory Usage and Purchase amortized; ChargeClass null; PricingCategory split into Committed and Standard plus Dynamic.

| Acceptance criterion | Status | Evidence |
|---|---|---|
| History reconciles to billing data | passed | Six monthly totals match the conformed table to the cent |
| Backtest error within the level agreed with Finance | unverified | July data incomplete; backtest not run |
| Scenarios name their driver assumptions | passed | Driver table in the model |

**Findings.** Usage-based spend tracks monthly active users closely; committed spend is flat until a commitment expires in September.

**Recommendations.**

| Action | Owner | Monthly impact range | Savings type | Confidence | Trade-off | Reversibility | Approval level |
|---|---|---|---|---|---|---|---|
| Decide the September renewal by mid-August | FinOps lead | 0 to 4,000 | estimated | medium | Flexibility against rate | Decision only | 0 |

**Checks.**

| Name | Method | Observed | Status | Evidence |
|---|---|---|---|---|
| History tie-out | Sum EffectiveCost by month against the conformed table | Differences 0.00 for all six months | passed | Query saved with the model |
| Backtest | Forecast June from January to May | Not run | unverified | July export incomplete |

**Assumptions.** Active-user growth of 3 to 5 percent per month; no price changes announced.

**Data quality.** Allocation coverage 93 percent; one correction in May excluded.

**Approvals.** None needed for the forecast; publishing into the planning system is Level 2 and was not done.

**Financial impact.** Q3 forecast 1.46 million to 1.61 million, base 1.52 million.

**Tradeoffs.** Not applicable beyond the renewal decision above.

**Unverified items.** The backtest.

**Risks.** A product launch in August is not yet in the driver plan.

**Rollback.** Not applicable; no change was made.

**Followups.** Run the backtest when the July export completes (FinOps analyst, 8 July).

Analysis is prepared, but the figures are not verified against billing data.

The JSON fixtures in `tests/fixtures/` exercise the report validator only. Their illustrative values are never reused as a real completion claim.
