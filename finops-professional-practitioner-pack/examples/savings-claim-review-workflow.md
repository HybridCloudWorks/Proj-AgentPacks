# Worked example: reviewing a savings claim before the board deck

All figures are synthetic.

**Request.** "Check this slide before it goes to the board: 'Our optimization program cut cloud costs 10 percent in February and our commitments save 30 percent.'" Recipe: `review-savings-claim.prompt.md`.

**Delegation.** The primary sends finops-evidence-reviewer the slide, the January and February totals by cost column, the commitment aggregates (ListCost, ContractedCost, EffectiveCost on committed usage) and the list of changes made in February. No raw rows.

**Reviewer findings.**

| Severity | Location | Evidence | Impact | Correction | Blocking |
|---|---|---|---|---|---|
| Blocker | Slide claim 1 | January 310,000 over 31 days, February 280,000 over 28 days: cost per day 10,000 in both months | The 10 percent drop is the shorter month, not the program | Report cost per day; the program's measured effect is in the resources changed, not the total | Yes |
| High | Slide claim 2 | List 1.00, contracted 0.95, effective 0.70 per unit on committed usage | 30 percent mixes the negotiated discount with commitment savings | Commitment savings are 0.25 per unit, an effective savings rate of 26 percent against contracted rates | Yes |
| Medium | Footnote | Savings figures are labelled "achieved" | Two initiatives have not yet been measured after the change | Label them estimated until measured | No |
| Note | Chart | Purchase rows appear in the trend line | Readers may see a spike in the purchase month | Show the one-time purchase separately | No |

Status from the reviewer: CHANGES_REQUIRED. It names one check to close a gap: cost per day for the resources the program changed, before and after.

**Closing the gap.** The primary asks finops-data-analyst to run that check. Result: the changed resources fell from 1,900 to 1,050 per day, a realized saving of about 25,500 per month.

**Corrected claim.** "The optimization program has realized about 25,500 per month in measured savings; two further initiatives are estimated at 8,000 to 11,000 per month. Commitments lower covered compute by 26 percent against our negotiated rates."

**Completion.** VERIFIED_COMPLETE for the corrected claim: both checks executed and passed, every finding resolved. Sending the deck is the user's action.
