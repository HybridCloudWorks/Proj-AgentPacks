# finops-professional-practitioner 1.0.0: artifact catalog

Every file in this pack, with its purpose and location. Contents are in the files themselves.

| ARTIFACT NAME | PURPOSE | LOCATION |
|---|---|---|
| finops-data-analyst.agent.md | Canonical agent: Run scoped, read-only queries and data-health checks over assigned billing data (FOCUS or provider-native) and return aggregated results with the exact queries, filters, row counts and caveats. | .apm/agents/finops-data-analyst.agent.md |
| finops-evidence-reviewer.agent.md | Canonical agent: Independently review cost figures, savings claims, forecasts, allocations and commitment recommendations against the evidence supplied, and return located findings without editing or querying. | .apm/agents/finops-evidence-reviewer.agent.md |
| finops-professional-practitioner.agent.md | Canonical agent: FinOps practitioner for cloud and SaaS cost visibility, allocation, anomalies, forecasting, unit economics, usage and rate optimization, and practice governance, grounded in FOCUS billing data and evidence-labelled reporting. | .apm/agents/finops-professional-practitioner.agent.md |
| billing-data-files.instructions.md | Canonical instruction: Handling rules for billing export files in a workspace: inspect schema and metadata before rows, read samples before full files, aggregate instead of echoing rows, and keep exports out of commits and external services. | .apm/instructions/billing-data-files.instructions.md |
| finops-professional-practitioner-contract.instructions.md | Canonical instruction: Approval levels, specialist handoff rules and the completion report format for FinOps work done with the FinOps Professional Practitioner pack. Always on; the pack's agents, skills and prompts rely on it. | .apm/instructions/finops-professional-practitioner-contract.instructions.md |
| focus-cost-queries.instructions.md | Canonical instruction: Conventions for SQL that reads cloud billing data: name the cost column, bound the scan, exclude corrections from trends, avoid double counting commitment purchases, and prefer normalized FOCUS columns. | .apm/instructions/focus-cost-queries.instructions.md |
| analyze-cloud-spend.prompt.md | Canonical prompt: Analyze cloud spend for a period and write an audience-ready narrative with top movers and labelled figures | .apm/prompts/analyze-cloud-spend.prompt.md |
| assess-finops-maturity.prompt.md | Canonical prompt: Assess FinOps practice maturity per capability and produce a scorecard, 90-day plan and roadmap | .apm/prompts/assess-finops-maturity.prompt.md |
| build-cost-forecast.prompt.md | Canonical prompt: Build or refresh a driver-based cloud cost forecast or budget with scenarios and a backtest | .apm/prompts/build-cost-forecast.prompt.md |
| design-allocation-model.prompt.md | Canonical prompt: Design or repair a cost allocation, showback or chargeback model | .apm/prompts/design-allocation-model.prompt.md |
| draft-finops-policy.prompt.md | Canonical prompt: Draft or review a FinOps policy, cadence, onboarding gate, tool evaluation or enablement plan | .apm/prompts/draft-finops-policy.prompt.md |
| estimate-workload-cost.prompt.md | Canonical prompt: Estimate the cost of a proposed workload, architecture alternative or migration before it is built | .apm/prompts/estimate-workload-cost.prompt.md |
| find-optimization-opportunities.prompt.md | Canonical prompt: Find, classify and prioritize usage optimization opportunities and plan their safe execution | .apm/prompts/find-optimization-opportunities.prompt.md |
| investigate-cost-anomaly.prompt.md | Canonical prompt: Triage an unexpected spend change or a fired alert, find the drivers and route it to an owner | .apm/prompts/investigate-cost-anomaly.prompt.md |
| plan-commitment-strategy.prompt.md | Canonical prompt: Review a commitment discount portfolio and recommend the next tranche, renewal or exchange | .apm/prompts/plan-commitment-strategy.prompt.md |
| reconcile-billing-data.prompt.md | Canonical prompt: Check billing data health and reconcile it to invoices, or plan a FOCUS parallel run | .apm/prompts/reconcile-billing-data.prompt.md |
| review-savings-claim.prompt.md | Canonical prompt: Independently review a savings claim, forecast, allocation or commitment recommendation before it reaches Finance or leadership | .apm/prompts/review-savings-claim.prompt.md |
| allocation-methodology-template.md | Canonical skill | .apm/skills/cost-allocation-and-chargeback/allocation-methodology-template.md |
| SKILL.md | Canonical skill: Design and run cloud cost allocation, covering the account hierarchy, tag and label taxonomy, enforcement at creation, shared-cost and Kubernetes allocation, unallocated spend, and the progression from showback to chargeback with reconciliation and disputes. Use when costs must be attributed to teams, products, environments or customers, tag coverage is low or drifting, or a showback or chargeback model is being designed, rolled out, audited or disputed. | .apm/skills/cost-allocation-and-chargeback/SKILL.md |
| SKILL.md | Canonical skill: Detect, triage and explain unexpected cloud spend changes and tune budget alerts with segment-level, seasonality-aware detection, masked-anomaly checks, root-cause tracing to line items, owner routing and alert precision tracking. Use when spend moved unexpectedly, an anomaly or budget alert fired or is too noisy, anomaly detection or budget alerting is being set up or tuned, or new spend appears in an unexpected service, account or region. | .apm/skills/cost-anomaly-management/SKILL.md |
| capability-scorecard.md | Canonical skill | .apm/skills/finops-maturity-assessment/capability-scorecard.md |
| SKILL.md | Canonical skill: Assess FinOps practice maturity capability by capability with evidence, weigh gaps by business impact and produce a scorecard, a 90-day plan and a 12-month roadmap. Use when an organization asks where its FinOps practice stands, wants a maturity scorecard against the FinOps Framework, is choosing its next FinOps priorities, or needs to justify investment in the practice. | .apm/skills/finops-maturity-assessment/SKILL.md |
| policy-template.md | Canonical skill | .apm/skills/finops-practice-governance/policy-template.md |
| SKILL.md | Canonical skill: Run the FinOps practice through operating cadences and decision logs, one-page policies with exception registers, workload onboarding gates, FinOps tool selection, education and enablement, and coordination with finance, procurement, ITAM, ITSM, ITFM, security and sustainability. Use when setting up or running FinOps reviews, writing or reviewing a FinOps policy, onboarding or migrating workloads, choosing FinOps tooling, building an enablement program, or aligning FinOps with adjacent disciplines. | .apm/skills/finops-practice-governance/SKILL.md |
| focus-column-reference.md | Canonical skill | .apm/skills/focus-billing-data-analysis/focus-column-reference.md |
| SKILL.md | Canonical skill: Analyze and report cloud and SaaS billing data in FOCUS or provider-native form by choosing the right cost column, applying the right filters, checking data health, reconciling to invoices, normalizing trends and writing audience-ready spend narratives. Use when a question needs numbers from billing exports, a spend report or top-movers narrative is due, totals must be reconciled to an invoice, a FOCUS adoption or conformance check is planned, or spend must be compared across providers. | .apm/skills/focus-billing-data-analysis/SKILL.md |
| SKILL.md | Canonical skill: Quantify the business value of cloud spend with driver-based forecasts that carry ranges and backtests, budgets, pre-deployment workload and migration estimates, unit economics and a small set of KPIs and benchmarks. Use when someone needs a forecast, budget, variance explanation, cost estimate for a proposed workload or migration, cost per unit of business output, or KPIs and benchmarks for teams or the organization. | .apm/skills/forecasting-and-unit-economics/SKILL.md |
| commitment-recommendation-template.md | Canonical skill | .apm/skills/rate-optimization/commitment-recommendation-template.md |
| SKILL.md | Canonical skill: Lower the rate paid for cloud and software through commitment discount portfolios (reservations, savings plans, committed use discounts), coverage and utilization management, laddered purchases and expirations, private pricing negotiation preparation, licensing and bring-your-own-license choices, SaaS entitlements and marketplace spend. Use when evaluating, buying, renewing, exchanging or reviewing commitments, preparing for a pricing agreement negotiation, or reducing license, SaaS or marketplace cost. | .apm/skills/rate-optimization/SKILL.md |
| SKILL.md | Canonical skill: Find, prioritize and safely realize usage savings across idle and orphaned resources, rightsizing, storage lifecycle, network and data transfer, Kubernetes requests and autoscaling, serverless and spot patterns, scheduling and cost-aware architecture, with carbon as a fourth trade-off. Use when looking for waste or savings opportunities, reviewing an architecture or change for cost, planning cleanup or rightsizing, or tracking realized savings and carbon impact. | .apm/skills/workload-optimization/SKILL.md |
| waste-pattern-catalog.md | Canonical skill | .apm/skills/workload-optimization/waste-pattern-catalog.md |
| apm.yml | APM manifest: name, version, targets. | apm.yml |
| capability-map.yml | Vendor compatibility metadata | compatibility/capability-map.yml |
| compatibility-matrix.yml | Vendor compatibility metadata | compatibility/compatibility-matrix.yml |
| optional-skills.yml | Vendor compatibility metadata | compatibility/optional-skills.yml |
| tool-permissions.yml | Vendor compatibility metadata | compatibility/tool-permissions.yml |
| vendor-sources.yml | Vendor compatibility metadata | compatibility/vendor-sources.yml |
| DESCRIPTION.md | What the pack is for and who uses it. | DESCRIPTION.md |
| AGENT_INVENTORY.md | Pack contract or inventory | docs/AGENT_INVENTORY.md |
| APPROVAL_MATRIX.md | Pack contract or inventory | docs/APPROVAL_MATRIX.md |
| DESIGN_DECISIONS.md | Pack contract or inventory | docs/DESIGN_DECISIONS.md |
| EVALUATION_PLAN.md | Pack contract or inventory | docs/EVALUATION_PLAN.md |
| HANDOFF_CONTRACT.md | Pack contract or inventory | docs/HANDOFF_CONTRACT.md |
| INTEGRATION_CONTRACT.md | Pack contract or inventory | docs/INTEGRATION_CONTRACT.md |
| MAINTENANCE.md | Pack contract or inventory | docs/MAINTENANCE.md |
| PROMPT_INVENTORY.md | Pack contract or inventory | docs/PROMPT_INVENTORY.md |
| SECURITY_AND_DATA_HANDLING.md | Pack contract or inventory | docs/SECURITY_AND_DATA_HANDLING.md |
| SKILL_INVENTORY.md | Pack contract or inventory | docs/SKILL_INVENTORY.md |
| SOURCE_TRACEABILITY.md | Pack contract or inventory | docs/SOURCE_TRACEABILITY.md |
| TOOL_PERMISSION_MATRIX.md | Pack contract or inventory | docs/TOOL_PERMISSION_MATRIX.md |
| commitment-portfolio-workflow.md | Worked example | examples/commitment-portfolio-workflow.md |
| final-completion-report.md | Worked example | examples/final-completion-report.md |
| idle-resource-cleanup-workflow.md | Worked example | examples/idle-resource-cleanup-workflow.md |
| masked-anomaly-investigation-workflow.md | Worked example | examples/masked-anomaly-investigation-workflow.md |
| maturity-assessment-workflow.md | Worked example | examples/maturity-assessment-workflow.md |
| monthly-spend-narrative-workflow.md | Worked example | examples/monthly-spend-narrative-workflow.md |
| copilot-instructions.md | Optional repository-level file | examples/repository/copilot-instructions.md |
| savings-claim-review-workflow.md | Worked example | examples/savings-claim-review-workflow.md |
| showback-to-chargeback-workflow.md | Worked example | examples/showback-to-chargeback-workflow.md |
| post-finops-completion.ps1 | Hook helper script | hooks/post-finops-completion.ps1 |
| post-finops-completion.sh | Hook helper script | hooks/post-finops-completion.sh |
| pre-finops-session.ps1 | Hook helper script | hooks/pre-finops-session.ps1 |
| pre-finops-session.sh | Hook helper script | hooks/pre-finops-session.sh |
| README.md | Hook helper script | hooks/README.md |
| finops.copilot-hooks.sample.json | Reviewed hook sample, not installed | hooks/samples/finops.copilot-hooks.sample.json |
| LICENSE | License terms. | LICENSE |
| PORTABLE_AGENT_SKILL_PACK_AUTHORING_PROMPT.md | The master prompt this pack was built to. | PORTABLE_AGENT_SKILL_PACK_AUTHORING_PROMPT.md |
| README.md | How to install and use the pack. | README.md |
| completion-report.md | Reusable template | templates/completion-report.md |
| handoff.md | Reusable template | templates/handoff.md |
| monthly-finops-review.md | Reusable template | templates/monthly-finops-review.md |
| realized-savings-tracker.csv | Reusable template | templates/realized-savings-tracker.csv |
| capability-coverage.yml | Local test or recorded evidence | tests/capability-coverage.yml |
| focus-sample.csv | Local test or recorded evidence | tests/fixtures/focus-sample.csv |
| invalid-completion.json | Local test or recorded evidence | tests/fixtures/invalid-completion.json |
| valid-completion.json | Local test or recorded evidence | tests/fixtures/valid-completion.json |
| report-contract.yml | Local test or recorded evidence | tests/report-contract.yml |
| skill-coverage.yml | Local test or recorded evidence | tests/skill-coverage.yml |
| test_behavior.py | Local test or recorded evidence | tests/test_behavior.py |
| trigger-cases.yml | Local test or recorded evidence | tests/trigger-cases.yml |
| completion_contract.py | Pack-specific helper code | tooling/completion_contract.py |
| finops_math.py | Pack-specific helper code | tooling/finops_math.py |
| hook_runner.py | Pack-specific helper code | tooling/hook_runner.py |
| requirements.txt | Pack-specific helper code | tooling/requirements.txt |
| VALIDATION_REPORT.md | Executed checks and what remains unverified. | VALIDATION_REPORT.md |

## Build outputs (dist/, not committed)

- copilot-finops-professional-practitioner.zip: 31 files generated by `apm install --target copilot`
- claude-finops-professional-practitioner.zip: 31 files generated by `apm install --target claude`
- codex-finops-professional-practitioner.zip: 17 files generated by `apm install --target codex`
- kiro-finops-professional-practitioner.zip: 20 files generated by `apm install --target kiro`
- gemini-finops-professional-practitioner.zip: 25 files generated by `apm install --target gemini`
- agent-skills-finops-professional-practitioner.zip: 14 files generated by `apm install --target agent-skills`
- finops-professional-practitioner-canonical.zip, finops-professional-practitioner-prompt.zip, finops-professional-practitioner-validation.zip, finops-professional-practitioner-skills.zip, finops-professional-practitioner-full-pack.zip, SHA256SUMS.txt
