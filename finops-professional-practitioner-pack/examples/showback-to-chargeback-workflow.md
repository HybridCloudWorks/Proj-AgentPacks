# Worked example: chargeback requested before showback was trusted

All figures are synthetic.

**Request.** "The CFO wants chargeback to every product team from next quarter. Build it." Recipe: `design-allocation-model.prompt.md`. Skill: cost-allocation-and-chargeback.

**Baseline.** Allocation coverage is 74 percent of usage EffectiveCost. There is no showback today. Shared platform costs (networking, observability, a shared Kubernetes cluster) are 22 percent of spend and unallocated.

**Assessment against the entry criteria.**

| Criterion | Status |
|---|---|
| Several months of consistent showback | Not met: none yet |
| Methodology signed off by Finance and engineering leaders | Not met |
| Dispute process | Not met |
| Small, visible unallocated spend | Not met: 26 percent untagged plus 22 percent shared |
| Parallel run where showback and chargeback agree | Not started |

**Recommendation.** Start showback now and present the chargeback timeline as a sequence of gates rather than a date: tagging remediation and a deny-at-creation policy for three mandatory keys (60 to 90 days), showback published monthly, shared-cost keys agreed with the receiving teams (requests for the ingress layer, CPU hours for the shared cluster, log volume for observability), then soft chargeback against budgets once two consecutive months reconcile without disputes, and hard chargeback after at least two quarters of soft chargeback.

**Methodology draft.** Built from the skill's methodology template: hierarchy mapping of 40 sub accounts to 12 product teams, the taxonomy with allowed values, five shared pools with keys and owners, the unallocated line shown in every report, monthly cadence with quarterly true-ups and a five-day dispute window.

**Review.** finops-evidence-reviewer checks the draft showback: team totals plus unallocated equal total EffectiveCost (passed), and flags a High finding that the observability pool used an even split in one table. The primary corrects it to the log-volume key.

**Completion.** Status PREPARED_NOT_VERIFIED: the methodology and showback draft are ready, the coverage query and sum check passed, and the sign-offs are unverified until they happen. Applying the tag policy and publishing showback are Level 2. The risk of an early chargeback (teams rejecting charges and the program losing credibility) is stated for the sponsor, who decides.
