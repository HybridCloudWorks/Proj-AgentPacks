# FinOps completion report

Use the field names in `tests/report-contract.yml`. A machine-readable copy can be saved as `.finops/completion.json` in the workspace, where the optional agentStop hook checks it.

| Field | What to write |
|---|---|
| status | One of VERIFIED_COMPLETE, PREPARED_NOT_VERIFIED, ANALYSIS_ONLY, CHANGES_REQUIRED, BLOCKED_ON_APPROVAL, BLOCKED_ON_DATA |
| outcome | One or two sentences on what was delivered |
| audience | Finance, Engineering, Leadership, Procurement, Product, or a named team |
| scope | Billing accounts, providers, period, and what was excluded |
| data_sources | Each source with schema or FOCUS version, period and extract date |
| cost_basis | `column` (a FOCUS cost column, or a native column plus `focus_equivalent`) and `filters` (ChargeCategory, ChargeClass, PricingCategory) |
| acceptance_criteria | Each with `id`, `status` (passed, failed, unverified) and `evidence` |
| findings | What the data shows, observation kept apart from cause |
| recommendations | Each with action, owner, monthly_impact_range `[low, high]`, savings_type (estimated or realized), confidence, tradeoff, reversibility, approval_level (0, 1, 2) |
| checks | Each with name, method, observed, status and evidence |
| assumptions | Every assumption that could change a figure |
| data_quality | Coverage, corrections, freshness, missing scopes |
| approvals | Approvals held, with exact scope; approvals still needed |
| financial_impact | Total impact range and how it was derived |
| tradeoffs | Cost against speed, quality and carbon |
| unverified | Anything not checked |
| risks | What could make the result wrong or harmful |
| rollback | How each recommended change is reversed |
| followups | Owner and date for each next step |

VERIFIED_COMPLETE needs every criterion passed, at least one executed check, every check passed and nothing unverified. A realized saving needs a passed measurement check. Without data to verify figures, write exactly: "Analysis is prepared, but the figures are not verified against billing data."
