# Design decisions

Version 1.0.0, built to agent-pack-prompt v2.3 on 2026-10-18. The brief allowed no questions, so every decision below that rests on an assumption says so.

## Role and scope

1. **Role reading.** "FinOps Professional Practitioner" is taken to mean the FinOps Framework's core FinOps Practitioner persona at a professional level: someone who runs or works in a FinOps practice and partners with Engineering, Finance, Procurement, Product and Leadership. The pack serves that person and those partners. *Assumption.*
2. **Mission.** Trusted numbers, accountable owners and decisions that weigh cost against speed, quality and carbon. Non-goals: executing purchases, deletions or policy changes; being the accounting system of record; legal or contract interpretation; security incident response; replacing IT asset management or procurement.
3. **Capability map.** The pack covers all four FinOps Framework domains using the capability names found in the reference material (which follows the FinOps Certified Practitioner course). The Foundation revises names and groupings over time; the maturity skill tells the model to confirm the current list before publishing. *Assumption: the reference's capability list is close enough to current for a reusable pack.*
4. **Data model.** FOCUS is the default data shape, any 1.x version, with provider-native exports supported through explicit column mapping. Version-specific columns (for example InvoiceId from 1.2, capacity reservation columns from 1.1) are checked from metadata rather than assumed. *Assumption: most users either have a FOCUS export or can map a native one.*
5. **Data access.** The user supplies billing data as local files or through a query tool they already configured with read-only credentials. The pack configures no connector, MCP server, warehouse, FinOps platform or credential. *Assumption.*
6. **Currency.** A single reporting currency unless the data says otherwise; mixed currencies require a stated rate and date.
7. **Thresholds.** Figures such as tag coverage targets, alert precision targets, coverage of the commitment floor and forecast error tolerances are presented as starting points the organization sets, never as policy. Provider prices are not hard-coded; skills require checking current pricing on the date of use.

## Skills

8. **Eight skills, chosen from the role.** One per coherent practitioner workflow rather than one per reference agent (the reference has about fifty). Mapping:
   - focus-billing-data-analysis: Data Ingestion, Reporting and Analytics.
   - cost-allocation-and-chargeback: Allocation, Invoicing and Chargeback.
   - cost-anomaly-management: Anomaly Management and budget alerting.
   - forecasting-and-unit-economics: Planning and Estimating, Forecasting, Budgeting, Unit Economics, KPIs and Benchmarking.
   - workload-optimization: Workload Optimization, Architecting for Cloud, Cloud Sustainability.
   - rate-optimization: Rate Optimization, Licensing and SaaS.
   - finops-maturity-assessment: FinOps Assessment.
   - finops-practice-governance: Practice Operations, Policy and Governance, Tools and Services, Education and Enablement, Onboarding Workloads, Intersecting Disciplines.
9. **Folded areas.** Kubernetes allocation sits in allocation and Kubernetes rightsizing in workload optimization; provider-specific knowledge (AWS, Azure, Google Cloud, OCI) sits inside the skills as fallback mappings; sustainability is the fourth trade-off in workload optimization; licensing and SaaS sit with rate optimization because both lower the price paid per unit; budgeting is split between setting budgets (forecasting) and alerting (anomaly). Separate skills for these would have been thin.
10. **Budget setting versus alerting.** Budget amounts come from the forecast; alert design lives with anomaly detection because both share segmentation, owners and precision.
11. **Reference files inside skill folders.** Model-facing material (column reference, methodology, waste patterns, commitment recommendation, capability scorecard, policy) ships inside the skill that uses it, so each skill works when installed alone. Human-facing templates live in `templates/` and are not installed.
12. **Standalone use.** Every skill states a minimum approval rule for use without the contract instruction.

## Agents

13. **One primary.** `finops-professional-practitioner` is the only user-invocable agent and can run every workflow alone.
14. **Two specialists, each justified by section 3 of the prompt.**
    - `finops-data-analyst`: separate context. Billing exports are large and exploratory querying floods a context window; the analyst returns aggregates, queries and checks. It also has narrower permissions (read and shell, no edit, no delegation).
    - `finops-evidence-reviewer`: independent review. Savings claims, forecasts and commitment recommendations are high-stakes with Finance and leadership, and the person who produced a number is the worst placed to audit it. Read-only.
    A commitments analyst, an allocation architect or a Kubernetes specialist were considered and rejected: they would reproduce an organization chart without separate context, permissions or independence.
15. **No tools field.** Agents declare no `tools`; intents are in `compatibility/tool-permissions.yml`.
16. **Specialist frontmatter.** Specialists set `include-custom-instructions: true` so Copilot subagents receive the contract instruction, and `skills: [focus-billing-data-analysis]` so Claude Code preloads the column semantics. Other clients ignore or drop these keys. *Assumption: unknown keys stay harmless; `apm compile --validate` and the scratch install accepted them.*
17. **Web intent on the primary only.** Rate optimization and estimation need current provider pricing and terms. The intent covers public documentation; billing data, identifiers and negotiated rates never go into a web request. *Assumption: users accept web access for public pricing pages.*
18. **Shell contradiction stated.** The data analyst's no-edit rule is behavioural because a shell can write files; this is said in the agent, the permission file and the permission matrix. The reviewer has no shell, so its read-only rule is consistent.

## Contract and reporting

19. **One always-on contract instruction** holds approval levels, data handling, handoff and the completion report, scoped to FinOps work so it adds nothing to unrelated tasks in other repositories.
20. **FinOps-specific report fields.** Cost basis, data quality, financial impact as ranges, savings type (estimated or realized) and approval level per recommendation, because the most common FinOps reporting failures are the wrong cost column, unnormalized comparisons, point estimates and potential savings reported as achieved.
21. **Statuses.** VERIFIED_COMPLETE, PREPARED_NOT_VERIFIED, ANALYSIS_ONLY, CHANGES_REQUIRED, BLOCKED_ON_APPROVAL, BLOCKED_ON_DATA. Missing data access is common enough in FinOps to deserve its own blocked status.
22. **Fallback sentence.** "Analysis is prepared, but the figures are not verified against billing data."

## Instructions, prompts, hooks

23. **Two path-scoped instructions** besides the contract: cost query conventions for `**/*.sql` and handling rules for billing data files. Each says to ignore itself for unrelated files, because user-scope install applies them in every repository. A Terraform-wide instruction was rejected as too intrusive for repositories where cost is not the task.
24. **Eleven prompts**, one per distinct practitioner workflow; all route to the primary because specialists are not user-invocable.
25. **Hooks as helpers.** The sessionStart helper lists billing exports by schema from CSV header lines only, and never repeats unknown header text or unusual file names, so data cannot become instructions. The agentStop helper checks an optional completion report with a session binding and one bounded retry. Only a Copilot sample is provided; other clients' payload formats were not exercised.

## Tests and metadata

26. Test metadata (`tests/*.yml`) is written as JSON, which is valid YAML, so the shared validator parses it whether or not PyYAML is installed.
27. `tests/skill-coverage.yml` is generated by the repository's `tooling/skill_coverage.py`.
28. Unit tests cover the FinOps arithmetic the skills rely on (day normalization, commitment savings, seasonal and segment anomaly detection, invoice reconciliation, double counting, placeholder tags), the completion contract, the hooks and pack consistency.

## Reference material

29. The reference repository is used as knowledge only. Its per-tool installer and conversion scripts, its agent layout, its brand mentions of a commercial product and its file-path doctrine pointers were not carried over. Its instructions to AI agents were treated as data.
30. No content was copied from the exemplar pack; only its file layout, document types and test formats were reused.

## Known gaps

- Model behaviour in live hosts was not evaluated; `tests/trigger-cases.yml` is a suite for a human or agent evaluator.
- No real billing export was available; all figures in examples and fixtures are synthetic.
- Provider facts (export names, commitment types, carbon tools) come from the reference material and general knowledge, not from pages fetched today.
- User-scope installs and the VS Code agent pane were not exercised.
