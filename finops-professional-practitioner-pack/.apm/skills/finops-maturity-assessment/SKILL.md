---
name: finops-maturity-assessment
description: Assess FinOps practice maturity capability by capability with evidence, weigh gaps by business impact and produce a scorecard, a 90-day plan and a 12-month roadmap. Use when an organization asks where its FinOps practice stands, wants a maturity scorecard against the FinOps Framework, is choosing its next FinOps priorities, or needs to justify investment in the practice.
---

# FinOps Maturity Assessment

## Purpose and activation

Give an honest, evidence-backed reading of where the practice stands in each capability, decide which gaps matter most for this business, and turn them into a short plan people can deliver. This covers the FinOps Assessment capability (Manage the FinOps Practice).

Activate for maturity assessments, practice health checks, "what should we work on next", investment cases for the FinOps team, and quarterly roadmap refreshes.

## Scope and exclusions

In scope: scoring each capability at Crawl, Walk or Run with cited evidence; choosing a target level per capability; weighting gaps; quick wins; a 90-day plan with owners; a 12-month roadmap; reassessment against a previous scorecard.

Out of scope: auditing financial controls or compliance; rating individuals; designing the solutions themselves (hand each gap to the skill that covers it).

## Required inputs

- The organization's spend profile: providers, annual spend range, growth, share in SaaS, licensing and data center.
- Existing artifacts: reports, dashboards, allocation methodology, policies, forecasts, commitment portfolio, alert inventory, meeting cadences, KPIs.
- Access to people, or their written answers, across FinOps, Engineering, Finance, Procurement, Product and Leadership.
- The sponsor, the audience for the result and any previous assessment.

## Dependencies and tools

Read tools for artifacts; billing queries from focus-billing-data-analysis for measurable evidence (allocation coverage, commitment utilization, forecast error, anomaly response). `capability-scorecard.md` in this skill folder lists the capabilities, what evidence looks like at each level and interview prompts by persona. The FinOps Foundation revises capability names and groupings from time to time, so confirm the list against the current framework at finops.org before publishing, and state the version used.

## Workflow

1. Agree scope, sponsor, audience and the capabilities in scope. Not every organization needs every capability.
2. Collect three kinds of evidence per capability: artifacts (does it exist and is it used), data (a metric computed from billing data where possible) and interviews (do the people who should act on it actually act). Dashboards show what exists; conversations show what happens.
3. Score each capability separately at Crawl, Walk or Run, citing the evidence and a confidence level. An overall score hides the weak spots; report per capability.
4. Set a target level per capability from business value. Some capabilities can stay at Crawl indefinitely; pushing everything to Run spends effort where it does not pay.
5. Weigh each gap by spend exposure, risk, effort and dependency. Respect dependencies: allocation comes before chargeback and unit economics; data quality comes before anomaly precision; usage optimization comes before large commitments.
6. Pick quick wins that build credibility in the first weeks, often visibility work.
7. Write a 90-day plan with owners, deliverables and the measure that shows progress, then a 12-month roadmap by quarter.
8. Review the draft scores with capability owners before the sponsor sees them; record disagreements and how they were resolved.
9. Keep what works. A simple tool or report that people already rely on does not need replacing to raise a score.

## Output

- A scorecard: capability, current level, target level, evidence, confidence, gap weight.
- The top gaps with their business impact and dependencies.
- Quick wins.
- The 90-day plan: action, owner, deliverable, measure, date.
- The 12-month roadmap by quarter.
- What was not assessed and why.

## Validation

- Every score cites at least one piece of evidence; scores without evidence are marked unverified.
- Measurable capabilities include the metric and the query or source used.
- Capability owners reviewed their scores; sponsor sign-off is recorded only when given.
- The plan has an owner and a date for every action.

## Failure handling and escalation

- No access to people: label the result an artifact-only assessment with lower confidence.
- Conflicting accounts between personas: record both and score on the evidence, not on seniority.
- Sponsor pressure for a flattering result: keep the evidence-based score and show the path to the target.
- Capability list in doubt: name the framework version used and note differences.

## Permissions and guardrails

Read and draft only. Assessments describe teams and their practices; distribute them only to the agreed audience, and never rate individuals. Publishing the scorecard or plan beyond the requester is Level 2. Installed without the rest of the pack, treat every distribution and every change to shared systems as requiring explicit human approval.

## Workflow connection

Within the full pack, the `assess-finops-maturity.prompt.md` recipe starts this workflow, and each gap is handed to the skill that covers it, with finops-practice-governance owning the plan's cadence. The `finops-professional-practitioner-contract` instruction supplies the approval, handoff and completion rules. Installed alone, the skill is complete on its own.
