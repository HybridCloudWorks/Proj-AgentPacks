# Prompt inventory

| Prompt | Skills | Expected output |
|---|---|---|
| analyze-cloud-spend.prompt.md | focus-billing-data-analysis | Audience narrative, top movers, labelled figures, data-health summary, reconciliation result |
| reconcile-billing-data.prompt.md | focus-billing-data-analysis | Data-health report, invoice reconciliation table, explained divergences, FOCUS parallel-run plan when migrating |
| investigate-cost-anomaly.prompt.md | cost-anomaly-management | Anomaly report with drivers, classification, owner, exposure range, draft owner message |
| design-allocation-model.prompt.md | cost-allocation-and-chargeback | Methodology, taxonomy and enforcement drafts, coverage report, showback draft, chargeback entry criteria |
| build-cost-forecast.prompt.md | forecasting-and-unit-economics | Forecast with drivers, scenarios, intervals and backtest error; budget proposal |
| estimate-workload-cost.prompt.md | forecasting-and-unit-economics, workload-optimization | P10 to P90 estimate by service category, alternatives with trade-offs, sensitive assumptions |
| find-optimization-opportunities.prompt.md | workload-optimization | Optimization inventory, execution plans with rollback, realized-savings tracking plan |
| plan-commitment-strategy.prompt.md | rate-optimization | Commitment recommendation, portfolio health, approvals required |
| assess-finops-maturity.prompt.md | finops-maturity-assessment | Scorecard, gaps, quick wins, 90-day plan, 12-month roadmap |
| draft-finops-policy.prompt.md | finops-practice-governance | Policy, cadence, onboarding gate, tool evaluation, enablement plan or integration charter |
| review-savings-claim.prompt.md | focus-billing-data-analysis plus the matching skill, via finops-evidence-reviewer | Located findings, recomputed figures, corrected claim |

All prompts set `agent: finops-professional-practitioner` and an `argument-hint`. APM installs them as Copilot prompt files, Claude Code commands (the `agent` key is dropped) and Gemini CLI commands. Codex and Kiro receive no prompts; their users invoke the primary agent directly and the skills activate from their descriptions.
