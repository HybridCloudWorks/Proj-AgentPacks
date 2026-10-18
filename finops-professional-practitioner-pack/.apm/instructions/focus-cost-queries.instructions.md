---
description: "Conventions for SQL that reads cloud billing data: name the cost column, bound the scan, exclude corrections from trends, avoid double counting commitment purchases, and prefer normalized FOCUS columns."
applyTo: "**/*.sql"
---

# Cost query conventions

Apply these when a SQL file reads billing or cost data (FOCUS tables, AWS CUR, Azure cost exports, GCP billing export). Ignore them for unrelated SQL.

- Start each cost query with a comment that states the question, the cost column (BilledCost for invoices and cash, EffectiveCost for trends, allocation and unit cost, ListCost or ContractedCost only for savings baselines), the period and the filters.
- Bound every scan with a ChargePeriodStart range or the table's partition column. Use an inclusive start and exclusive end in UTC. Run new queries on one day or with a LIMIT before widening.
- Trend and allocation queries filter `ChargeClass IS NULL` and analyze corrections separately.
- Never sum ListCost, ContractedCost or BilledCost across Purchase and Usage rows without deciding which ChargeCategory belongs in the answer; commitment purchases appear in both.
- Filter on normalized columns (ServiceCategory, ChargeCategory, ChargeFrequency, PricingCategory, CommitmentDiscountStatus), not substring matches on descriptions or service names.
- Read Tags with the engine's JSON functions, never `LIKE` on the raw column. Join on identifiers (BillingAccountId, SubAccountId, ResourceId); display names.
- Monthly comparisons divide by days in the period or compare equal-length windows.
- Keep provider-native column names out of shared views when a FOCUS column exists; where only a native column exists, comment its FOCUS equivalent.
- Do not hard-code negotiated rates, account identifiers or customer names in committed SQL; parameterize them.
