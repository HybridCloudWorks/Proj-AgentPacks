# Worked example: next savings plan tranche

All figures are synthetic.

**Request.** "Two savings plans expire in February. What should we buy?" Recipe: `plan-commitment-strategy.prompt.md`. Skill: rate-optimization.

**Pre-checks.** A rightsizing wave is in flight for 14 percent of eligible compute (owner approved, completes in January). The primary models the steady floor after that wave, not before.

**Evidence.** 90 days of eligible compute usage, regular charges. Hourly eligible usage at contracted rates: floor 41.0 per hour after rightsizing, median 52.0. Existing portfolio: plan A (18.0 per hour, utilization 99.1 percent over closed windows) and plan B (10.0 per hour, utilization 93.4 percent) both expire on 14 February.

**Options modelled.** Commitment savings use ContractedCost minus EffectiveCost on covered usage.

| Option | Hourly commitment | Coverage of floor | Term | Expected monthly saving | If usage falls 20% | If usage falls 40% |
|---|---|---|---|---|---|---|
| A | 28.0 | 68% | 1 year | 5,900 to 6,300 | 5,900 to 6,300 | 3,100 to 3,500 |
| B | 33.0 | 80% | 1 year | 6,900 to 7,300 | 6,500 to 6,900 | 1,800 to 2,200 |
| C | 33.0 | 80% | 3 years | 9,600 to 10,100 | 9,000 to 9,500 | 2,600 to 3,100 |

**Recommendation.** Renew at 28.0 per hour for one year on 1 February (option A) and review a second tranche of 5.0 per hour in April once the rightsizing results are measured. Reasons: it preserves headroom below the floor while a platform migration is still being planned, and the downside at a 40 percent drop stays positive. Option C saves more but locks three years against an architecture that may change; that trade-off is stated for Finance.

**Review.** finops-evidence-reviewer recomputes the savings from the supplied ContractedCost and EffectiveCost aggregates and confirms that unused commitment was counted only for closed windows. It raises a Medium finding: the provider recommendation tool suggested 39.0 per hour; the difference comes from the tool using pre-rightsizing usage. The primary adds that explanation.

**Completion.** Status BLOCKED_ON_APPROVAL. The package states the exact specification (provider, plan type, scope, term, payment option, hourly amount, start date), the savings range, the downside, that the commitment cannot be cancelled, and the approvers (FinOps lead and Finance controller above the threshold). Purchasing is Level 2 and was not done.
