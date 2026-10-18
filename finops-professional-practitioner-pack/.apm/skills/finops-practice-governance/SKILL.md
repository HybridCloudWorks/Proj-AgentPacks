---
name: finops-practice-governance
description: Run the FinOps practice through operating cadences and decision logs, one-page policies with exception registers, workload onboarding gates, FinOps tool selection, education and enablement, and coordination with finance, procurement, ITAM, ITSM, ITFM, security and sustainability. Use when setting up or running FinOps reviews, writing or reviewing a FinOps policy, onboarding or migrating workloads, choosing FinOps tooling, building an enablement program, or aligning FinOps with adjacent disciplines.
---

# FinOps Practice Governance

## Purpose and activation

Make FinOps a habit of the organization rather than a report from one team: regular decisions with owners, short policies that are enforced, new workloads that arrive cost-transparent, tools chosen for real gaps and people who know how to act on cost data. This covers FinOps Practice Operations, Policy and Governance, FinOps Tools and Services, FinOps Education and Enablement, Onboarding Workloads and Intersecting Disciplines.

Activate for review cadences and agendas, policy drafting or review, exception handling, migration and onboarding checklists, tool evaluations, training and champions programs, and questions about who owns what between FinOps and adjacent teams.

## Scope and exclusions

In scope: the operating model and principles; cadence design and meeting outputs; decision logs; policy library and exception register; onboarding gates and post-go-live reviews; mergers and acquisitions integration plans; tool portfolio and evaluation criteria; enablement curricula, champions and communications; integration charters with adjacent disciplines.

Out of scope: approving spend or policies (owners and sponsors do); procurement of tools; human resources matters; detailed allocation, forecasting or optimization methods (their own skills).

## Required inputs

- The current operating model: who does FinOps centrally and in teams, the sponsor, existing meetings and reports.
- Existing policies, exception lists and how they are enforced.
- For onboarding: the workload, its owner, target environment, go-live date and the source environment if migrating.
- For tooling: the capability gaps (often from finops-maturity-assessment), current tools with cost and renewal dates, data and security requirements.
- For enablement: the personas to reach, their tools and channels, and the vocabulary already in use.
- For adjacent disciplines: who runs ITAM, ITSM, ITFM or technology business management, security, sustainability and procurement, and what each already reports.

## Dependencies and tools

Read tools for existing documents; the other skills of this pack for the content each policy or gate refers to. `policy-template.md` in this skill folder holds the one-page policy and exception register structure. Nothing is installed by this skill.

## Workflow

### Operating model

Work from the FinOps principles, paraphrased: teams collaborate; business value drives technology decisions; everyone owns their technology usage; FinOps data is accessible, timely and accurate; FinOps is enabled centrally; and the variable cost model is used to advantage. A small central team enables, and the teams that build and run workloads own their cost.

### Cadences

1. Weekly tactical: anomalies, open actions, blockers.
2. Monthly business review: variance against budget and forecast, realized savings, decisions needed, KPI trends.
3. Quarterly strategic: commitment plan, maturity progress, roadmap, policy review.
4. Every meeting ends with decisions (proceed, reject or defer for named analysis), owners and dates, recorded in a searchable decision log. Application teams make the final call on their workloads; FinOps advises with evidence.

### Policies

1. One page each: purpose, scope, rule, enforcement point (preventive at creation, detective after the fact), exception process, owner and review date.
2. A typical library: tagging and allocation, commitment purchase authority and thresholds, budget and spend approval, anomaly response times, non-production schedules, billing data access, marketplace purchases, tool procurement.
3. Prefer preventive enforcement for high-cost rules, with a legitimate exception path; otherwise people route around the policy.
4. Keep an exception register with owner, reason and expiry date, and review it quarterly. Track attempted violations as an early signal of where policy and work collide.
5. Share enforcement infrastructure with security policy rather than building a parallel stack.

### Onboarding workloads

Before production, a workload has an owner, an account or project placement and tags that allocate it, an estimate and a forecast, a budget with an alert owner, a reviewed architecture cost and, for migrations, an exit date for the source environment so the overlap period closes. Defer commitments until usage has been stable for 60 to 90 days. Review actuals against the estimate at 30 and 90 days. Mergers and acquisitions take months of integration work: billing structure, taxonomy, commitments, tools and contracts.

### Tools and services

Start from capability gaps, not from products. Native provider tools usually cover Crawl needs. Require ingestion and export of FOCUS data so tools can be reconciled with each other. Avoid two broad platforms that overlap. Compare the tool's cost with the savings and time it enables. Build only where the organization has the data engineering to sustain it. Review the portfolio yearly. This skill does not recommend vendors by name; it produces criteria and a comparison of the options the user names.

### Education and enablement

Teach each persona what it needs: engineers cost per request and the cost of architecture choices, Finance the difference between cash and amortized views, Product cost in the business case, leaders unit cost and trends. Teach the shared vocabulary of cost columns once. Grow a champions network inside teams, add a FinOps module to engineering onboarding, put guidance where work happens (runbooks, design templates, pipeline documentation) and publish wins. Measure the program as a funnel from awareness to action to result.

### Intersecting disciplines

Agree one dataset and many views. Respect ownership: IT asset management owns license compliance, service management owns change management, IT financial management owns the IT budget and cost model, security owns incident response, sustainability owns carbon reporting, procurement owns contracts. Define shared KPIs once. Send cost anomalies that look like misuse to security. Feed the FinOps forecast into the IT budget rather than running a parallel one.

### Data in the path

Shape every output for the place its audience already works: a ticket for engineering, a tab in the finance close workbook, a panel in the team's dashboard, a section in the business review deck. Prepare drafts; publishing or sending them is Level 2.

## Output

- A cadence calendar with owners, inputs and agendas, and a decision log format.
- Policies from `policy-template.md` and an exception register.
- An onboarding checklist and a post-go-live review plan.
- A tool evaluation: capability gaps, criteria, options compared, total cost, recommendation and risks.
- An enablement plan by persona with measures.
- An integration charter per adjacent discipline: shared, owned, handed off, escalation path.

## Validation

- Every policy has an owner, an enforcement point, an exception path and a review date.
- Every cadence produces decisions with owners and dates.
- Onboarding gates are testable yes or no checks.
- Tool comparisons use the same criteria for every option and cite their sources and dates.
- Approval by the sponsor or owners is recorded as passed only when it was given.

## Failure handling and escalation

- No sponsor: state that governance without sponsorship tends to stall and propose the smallest cadence that earns one.
- Policy conflicts with security or procurement rules: escalate to both owners; do not choose for them.
- Teams bypass a policy: look at the exception path before tightening enforcement.
- Tool request without a gap: record it and test it against the capability gaps first.

## Permissions and guardrails

Draft and advise. Publishing policies, changing enforcement in shared accounts, scheduling meetings, sending communications, starting tool procurement and sharing billing data with a vendor for evaluation are Level 2. Installed without the rest of the pack, treat every publication, change to shared systems and external communication as requiring explicit human approval.

## Workflow connection

Within the full pack, the `draft-finops-policy.prompt.md` recipe starts this workflow, finops-maturity-assessment supplies the gaps that drive priorities, and the other skills supply the content each policy and gate refers to. The `finops-professional-practitioner-contract` instruction supplies the approval, handoff and completion rules. Installed alone, the skill is complete on its own.
