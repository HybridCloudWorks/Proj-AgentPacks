# Worked example: maturity assessment for a mid-sized practice

All figures are synthetic.

**Request.** "Assess our FinOps maturity and tell us what to do next quarter." Recipe: `assess-finops-maturity.prompt.md`. Skill: finops-maturity-assessment.

**Evidence collected.** Artifacts (monthly report, tag policy, commitment spreadsheet, alert list), billing metrics (allocation coverage 81 percent, commitment utilization 97 percent, no forecast backtest on record) and written answers from Engineering, Finance and Procurement. Leadership was unavailable, so leadership-related scores carry lower confidence.

**Excerpt of the scorecard.**

| Capability | Current | Target | Evidence | Confidence |
|---|---|---|---|---|
| Allocation | Crawl | Walk | 81% coverage, tag policy is warn-only, no shared-cost keys | High |
| Rate optimization | Walk | Walk | Layered commitments, 97% utilization, quarterly review | High |
| Forecasting | Crawl | Walk | Linear extrapolation, no backtest, Finance reports misses | Medium |
| Unit economics | Not started | Crawl | No agreed unit | Medium |
| Anomaly management | Crawl | Walk | Provider default alerts, 40 per week, no owners | High |

Rate optimization is already at its target; pushing it to Run would cost effort without proportionate value at this spend level.

**Gaps and dependencies.** Allocation comes first because forecasting by team, anomaly routing and unit economics all depend on it.

**90-day plan (excerpt).**

| Action | Owner | Deliverable | Measure | Due |
|---|---|---|---|---|
| Deny-at-creation for three mandatory keys | Platform lead | Policy in place with exception register | Coverage above 92% | Week 6 |
| Assign owners to the 40 weekly alerts, retire the rest | FinOps lead | Alert inventory | Alerts with owners 100%, weekly fires under 10 | Week 4 |
| Backtested driver forecast for the top three products | FinOps analyst | Model and error report | Error agreed with Finance | Week 10 |

**Review.** Capability owners reviewed their rows; Engineering disputed the anomaly score, and the evidence (no owners on any alert) kept it at Crawl, with the disagreement recorded.

**Completion.** Status PREPARED_NOT_VERIFIED: the scorecard and plan are ready; sponsor sign-off is unverified. Distribution beyond the requester is Level 2.
