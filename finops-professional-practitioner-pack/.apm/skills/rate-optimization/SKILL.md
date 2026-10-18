---
name: rate-optimization
description: Lower the rate paid for cloud and software through commitment discount portfolios (reservations, savings plans, committed use discounts), coverage and utilization management, laddered purchases and expirations, private pricing negotiation preparation, licensing and bring-your-own-license choices, SaaS entitlements and marketplace spend. Use when evaluating, buying, renewing, exchanging or reviewing commitments, preparing for a pricing agreement negotiation, or reducing license, SaaS or marketplace cost.
---

# Rate Optimization

## Purpose and activation

Pay less per unit for what the organization will use anyway, without trading away more flexibility than the savings are worth. This covers Rate Optimization and Licensing and SaaS in the Optimize Usage and Cost domain.

Activate for commitment recommendations and renewals, utilization or coverage reviews, unused-commitment waste, expiration planning, private pricing or enterprise agreement preparation, bring-your-own-license decisions, SaaS renewals and marketplace purchases.

## Scope and exclusions

In scope: baseline analysis for commitments; existing portfolio review; option modelling across type, term, payment and scope; purchase recommendations in tranches; utilization and coverage monitoring; expiration calendars; private pricing analysis and negotiation preparation; license-included against bring-your-own-license models; hybrid-use benefits; SaaS seat utilization; marketplace channel analysis; dynamic pricing (spot) as a rate lever.

Out of scope: buying, exchanging or selling commitments, signing agreements or speaking to vendors (all Level 2, done by the authorized owner); legal interpretation of contract clauses (route to Legal); license compliance determinations (owned by IT asset management); whether a workload tolerates interruption (workload-optimization).

## Required inputs

- 60 to 90 days of usage eligible for commitments, by provider, service, family, region and scope, with PricingCategory.
- The existing portfolio: CommitmentDiscountId, type, category (spend or usage), term, payment option, scope, start and end dates, utilization.
- Planned changes: migrations, decommissions, rightsizing in flight, architecture changes, growth plans with their owners.
- Finance constraints: cash-flow preference, cost of capital, approval thresholds, the fiscal calendar.
- For private pricing: 12 to 24 months of spend, the growth plan, the current agreement and alternatives.
- For licensing and SaaS: entitlements, active usage over 30, 60 and 90 days, renewal dates, and the IT asset management contact.

## Dependencies and tools

Billing queries from focus-billing-data-analysis (commitment utilization and coverage shapes), forecasts from forecasting-and-unit-economics, provider documentation for current commitment types and terms read on the date of the recommendation, and provider recommendation tools as one input among several. `commitment-recommendation-template.md` in this skill folder structures a recommendation. Nothing is installed or purchased by this skill.

## Workflow

### Commitment portfolio

1. Optimize usage first. Commit to the workload after rightsizing and cleanup, not before; otherwise the commitment locks in waste.
2. Find the steady floor: the lowest sustained hourly or daily eligible usage over the window, by the scope a commitment would apply to. Separate PricingCategory Dynamic usage, which already runs at a reduced rate.
3. Review what exists before buying: utilization by commitment for closed windows, coverage, unused amount, and expirations in the next 90 days. Prefer exchange or modification of under-used commitments over new purchases.
4. Model options: coverage levels below the floor, terms, payment options and flexibility (spend-based or compute-flexible against resource-specific). For each, compute commitment savings as ContractedCost minus EffectiveCost on covered usage, the effective savings rate, the break-even utilization and the downside if eligible usage falls by a fifth or by two fifths.
5. Layer from flexible to specific: broad spend-based or compute-flexible commitments for the base, resource-specific ones only for genuinely stable usage. Do not stack two commitments on the same usage. Capacity reservations buy availability, not a discount; decide them separately.
6. Recommend tranches spread over time rather than one large purchase, with the exact specification (provider, type, scope, term, payment option, hourly or total commitment, region or family), the savings range, the downside and the approvals required.
7. Monitor weekly: utilization, coverage and expirations. Act before expiry with renewal, exchange or deliberate lapse.

### Private pricing preparation

Establish the baseline from trailing spend, build the growth case with named engineering and product owners, and model low, expected and stretch commitment levels with the shortfall exposure of each. Committing beyond trailing actual spend needs a funded plan for the difference. List the non-price terms that carry value (ramp schedule, marketplace drawdown eligibility, credits, support and training) and the alternatives available. Flag shortfall, true-up and carry-forward clauses for legal review. The analysis prepares the negotiator; it does not negotiate.

### Licensing, SaaS and marketplace

- Compare license-included and bring-your-own-license costs over the term, including hybrid-use benefits such as Azure Hybrid Benefit, and check eligibility before buying reservations for the same workloads.
- Involve IT asset management for any license decision; they own compliance risk.
- Before each SaaS renewal, compare entitled seats with active users over 30, 60 and 90 days and propose the right tier and count.
- For marketplace purchases, use the publisher to see total spend with a vendor across channels and the invoice issuer for reconciliation; confirm whether a purchase draws down a cloud commitment before assuming it does.

Maturity guide: at Crawl, one flexible commitment covering a conservative share of the steady base, reviewed quarterly. At Walk, a layered portfolio, tranche purchases, utilization tracking and a renewal calendar. At Run, commitment savings and utilization tracked as KPIs, centralized purchasing and exchange triggers.

## Output

- A commitment recommendation from `commitment-recommendation-template.md`: baseline evidence, current portfolio, options table, recommended tranche, savings math with the columns used, sensitivity and downside, risks, approvals and monitoring plan.
- A portfolio health report: utilization, coverage, unused cost for closed windows, expirations.
- A private pricing brief: baseline, scenarios, shortfall exposure, non-price terms, alternatives, clauses for legal review.
- A license and SaaS review: model comparison, seat utilization, renewal recommendations, marketplace channel view.

## Validation

- Savings are computed from ContractedCost and EffectiveCost, not ListCost, and shown as a range.
- Unused commitment is counted only for windows that have closed.
- The recommended coverage leaves explicit headroom below the steady floor.
- The downside scenario is shown next to the expected one.
- Current provider terms were checked on a stated date; otherwise the recommendation says they are unconfirmed.

## Failure handling and escalation

- Usage too short or unstable: recommend waiting and reforecasting, or a smaller flexible tranche, and say why.
- Pending migration or architecture change: hold resource-specific commitments until the target state is stable.
- Provider recommendation disagrees with the analysis: show both and explain the difference in assumptions.
- Contract language unclear: route to Legal; do not interpret it.
- License compliance question: route to IT asset management.

## Permissions and guardrails

Analysis and drafts only. Purchasing, exchanging, selling or letting commitments lapse, accepting any pricing term, and contacting vendors are Level 2 and usually require Finance or procurement approval as well. Many commitments cannot be cancelled; say so in every purchase recommendation. Negotiated rates are confidential. Installed without the rest of the pack, treat every purchase, contract action and vendor communication as requiring explicit human approval.

## Workflow connection

Within the full pack, the `plan-commitment-strategy.prompt.md` recipe starts this workflow and finops-evidence-reviewer checks the savings math before a purchase decision. The `finops-professional-practitioner-contract` instruction supplies the approval, handoff and completion rules. Installed alone, the skill is complete on its own.
