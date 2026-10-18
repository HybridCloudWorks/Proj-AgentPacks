# Skill inventory

| Skill | FinOps Framework coverage | Activation | Reference file in the skill folder | Workflow prompt |
|---|---|---|---|---|
| focus-billing-data-analysis | Data Ingestion; Reporting and Analytics | Numbers from billing exports, spend narratives, invoice reconciliation, FOCUS adoption, cross-provider comparison | focus-column-reference.md | analyze-cloud-spend.prompt.md, reconcile-billing-data.prompt.md |
| cost-allocation-and-chargeback | Allocation; Invoicing and Chargeback | Costs need owners, tag coverage low or drifting, showback or chargeback designed or disputed | allocation-methodology-template.md | design-allocation-model.prompt.md |
| cost-anomaly-management | Anomaly Management; budget alerting | Unexpected spend change, fired or noisy alerts, detector design, spend in unexpected places | none | investigate-cost-anomaly.prompt.md |
| forecasting-and-unit-economics | Planning and Estimating; Forecasting; Budgeting; Unit Economics; KPIs and Benchmarking | Forecasts, budgets, variance, workload or migration estimates, unit cost, KPIs | none | build-cost-forecast.prompt.md, estimate-workload-cost.prompt.md |
| workload-optimization | Workload Optimization; Architecting for Cloud; Cloud Sustainability | Waste hunts, rightsizing, architecture cost review, realized savings, carbon | waste-pattern-catalog.md | find-optimization-opportunities.prompt.md |
| rate-optimization | Rate Optimization; Licensing and SaaS | Commitments, renewals, private pricing, licenses, SaaS seats, marketplace | commitment-recommendation-template.md | plan-commitment-strategy.prompt.md |
| finops-maturity-assessment | FinOps Assessment | Practice maturity, next priorities, investment case | capability-scorecard.md | assess-finops-maturity.prompt.md |
| finops-practice-governance | Practice Operations; Policy and Governance; Tools and Services; Education and Enablement; Onboarding Workloads; Intersecting Disciplines | Cadences, policies, onboarding gates, tooling, enablement, adjacent disciplines | policy-template.md | draft-finops-policy.prompt.md |

Every SKILL.md has the same ten sections, matching section 4 of the master prompt: purpose and activation; scope and exclusions; required inputs; dependencies and tools; workflow; output; validation; failure handling and escalation; permissions and guardrails; workflow connection. A unit test checks that all ten are present in every skill.

Each skill is useful installed alone: it names its own inputs and tools, carries its reference file, and states a minimum approval rule for use without the contract instruction. With the full pack, the contract instruction supplies the approval levels, handoff rules and report format.

The skills describe what the model should do; they are not a guarantee that it will. Behavioural evaluation is described in EVALUATION_PLAN.md.
