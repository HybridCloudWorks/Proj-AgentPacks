# Capability scorecard

Capabilities are grouped by the four FinOps Framework domains. Names follow the framework as it stood in the reference material used to build this pack; confirm them against the current framework before publishing.

## Level definitions, paraphrased

- Crawl: little reporting or tooling, basic measures, basic processes, the capability is understood but not followed by all major teams, work targets the easy wins.
- Walk: the capability is understood and followed across the organization, hard edge cases are known and some are deferred, automation or process covers most needs, goals are moderate to high.
- Run: every team follows it, hard edge cases are being handled, goals are high, and automation is the default approach.

## Evidence by capability

| Domain | Capability | Crawl looks like | Walk looks like | Run looks like | Measurable signal |
|---|---|---|---|---|---|
| Understand usage and cost | Data ingestion | One provider export, loaded by hand | Multi-provider conformed dataset with freshness checks | Conformance and reconciliation tests gate every load | Days from period end to reconciled data |
| | Allocation | Hierarchy-based ownership, tag policy on paper | Enforced taxonomy, documented shared-cost keys | Usage-driven shared keys, external mapping survives reorganizations | Share of spend allocated |
| | Reporting and analytics | Monthly report from the console | Persona-specific reports in the tools people use | Self-service views on one conformed dataset | Report consumers acting on findings |
| | Anomaly management | Provider default alerts | Segment-level detection with owners | Context-rich routing with precision and response targets | Alert precision, time to resolve |
| Quantify business value | Planning and estimating | Calculator estimates for big projects | Estimates in design review with ranges | Estimates in pipelines for infrastructure changes | Estimate error at 90 days |
| | Forecasting | Linear extrapolation | Backtested driver model | Reforecast triggered by driver change | Forecast error |
| | Budgeting | Annual budget per business unit | Budgets per accountable scope with trajectory alerts | Budgets tied to driver forecasts | Variance explained |
| | KPIs and benchmarking | Spend totals | A short KPI set with definitions | KPIs with targets reviewed in business reviews | KPIs with owners |
| | Unit economics | None or ad hoc | One agreed unit with a trend | Unit cost in launch dashboards and margin views | Products with unit cost |
| Optimize usage and cost | Architecting for cloud | Cost raised after launch | Cost section in design records | Cost checks in design and pull request review | Designs with cost estimates |
| | Workload optimization | Occasional cleanups | Lifecycle policies, owner-approved rightsizing | Continuous detection, automated obvious tier | Realized savings per quarter |
| | Rate optimization | One flexible commitment | Layered portfolio, tranche purchases | Centralized purchasing with utilization targets | Effective savings rate, utilization |
| | Licensing and SaaS | Renewals at list | Seat reviews before renewal | Entitlement data joined to usage continuously | Seat utilization |
| | Cloud sustainability | Provider carbon report read occasionally | Carbon per unit for main workloads | Carbon at design decision points | Carbon per unit trend |
| Manage the FinOps practice | Practice operations | Monthly meeting | Weekly, monthly and quarterly cadences with decision logs | Cadences measured by decisions made | Decisions with owners |
| | Policy and governance | Tagging policy only | Policy library with exception register | Preventive policy for high-cost rules, exceptions expire | Expired exceptions |
| | FinOps assessment | Self-assessment | Periodic evidence-based assessment | Plan refreshed each cycle | Plan actions completed |
| | Tools and services | Native tools | Gap-driven tool choices | Portfolio reviewed against capability needs | Tool cost against savings |
| | Education and enablement | Occasional sessions | Persona curricula and champions | FinOps in onboarding and daily workflows | Teams with a trained champion |
| | Invoicing and chargeback | Invoices paid centrally | Showback trusted by teams | Chargeback booked without rework | Disputes per cycle |
| | Onboarding workloads | Ad hoc | Intake gate before production | Gate automated in delivery pipelines | Workloads passing the gate |
| | Intersecting disciplines | Parallel analyses | Shared dataset with ITAM and security | Joint KPIs across disciplines | Duplicate reports retired |

## Interview prompts by persona

- Engineering: When did you last see your team's cloud cost? What would you do with it? What stops you acting?
- Finance: Which cloud figures do you trust? How long does month-end reconciliation take? Where do forecasts miss?
- Procurement: Who decides commitment and contract purchases? How are renewals tracked?
- Product: Do you know the cost of serving a customer or a feature? Would it change a decision?
- Leadership: What decision about cloud spend is hardest today? What would good look like in a year?
- FinOps team: Which reports are used and which are ignored? Where do disputes come from?
