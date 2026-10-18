# Worked example: March spend narrative for Finance

All figures are synthetic.

**Request.** "Write the March cloud summary for Finance. Leadership thinks costs jumped." Recipe: `analyze-cloud-spend.prompt.md`. Skill: focus-billing-data-analysis. Level 0 and Level 1 (local query files).

**Scope.** The primary reads the FOCUS export metadata: FOCUS 1.2, two billing accounts, USD, data through 31 March, extracted 3 April. Audience is Finance, so both views are needed: BilledCost for the invoice and EffectiveCost for the trend.

**Data health.** One correction row restates February storage (−1,240). Allocation coverage is 91 percent of usage EffectiveCost. A one-year prepaid commitment was bought on 2 March (BilledCost 36,000, EffectiveCost 0 on the Purchase row).

**Analysis.**

| View | February | March | Change |
|---|---|---|---|
| BilledCost (invoice) | 168,000 | 217,760 | +29.6% |
| EffectiveCost total, regular charges | 168,000 | 186,000 | +10.7% |
| EffectiveCost per day | 6,000 | 6,000 | 0.0% |

The invoice rose because of the prepaid purchase; the run rate did not change at all. March is three days longer than February, which explains the whole movement in EffectiveCost. Within that flat run rate, compute rose by 380 per day (a new analytics cluster, owner tag `team=insights`) and storage fell by about the same after a lifecycle rule took effect.

**Reconciliation.** BilledCost per InvoiceId matches both March invoices to the cent. The gap between BilledCost and regular EffectiveCost (31,760) is the prepaid purchase (36,000) less the share amortized into March (3,000, which appears in EffectiveCost on usage rows billed at zero) and the February correction (−1,240, which the invoice carries but the trend excludes).

**Narrative for Finance (draft).** "Cash spend in March was 217,760, including a 36,000 prepaid commitment that lowers compute rates for the next twelve months. Excluding that purchase and adjusting for March's three extra days, the daily run rate was unchanged at 6,000. A new analytics cluster added about 380 per day, offset by storage savings. Forecast impact: none for Q2; the commitment amortizes at about 3,000 per month."

**Review.** Because the figures go to Finance, the primary sends the aggregates and queries to finops-evidence-reviewer. The reviewer confirms the column choices and the day normalization and adds a Note: label the 36,000 as One-Time in the chart so it is not read as run rate.

**Completion.** Status VERIFIED_COMPLETE: the reconciliation and the per-day query were executed and passed, and the reviewer's note was applied. Distribution to Finance is Level 2; the primary hands the draft to the user to send.
