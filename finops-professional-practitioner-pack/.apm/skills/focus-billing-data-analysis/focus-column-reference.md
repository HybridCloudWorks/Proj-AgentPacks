# FOCUS column reference and query shapes

A working summary for analysts. The FOCUS specification at focus.finops.org is authoritative; check the dataset's FOCUS version before relying on a column, because columns are added and occasionally deprecated between versions.

## Cost columns

| Column | Meaning | Use for | Caution |
|---|---|---|---|
| BilledCost | What the invoice charges for the row, after discounts, without amortizing prepayments | Invoices, cash budgets, reconciliation | A prepaid commitment appears as one large Purchase row |
| EffectiveCost | Cost after discounts with prepaid amounts spread over the usage they cover | Trends, run rate, allocation, chargeback, unit cost | Period totals do not equal the invoice; the prepaid Purchase row carries zero |
| ListCost | Public list price times pricing quantity | Baseline for all rate savings | List minus Effective includes negotiated discounts the customer gets anyway |
| ContractedCost | Negotiated rate times pricing quantity, before commitment discounts | Baseline for commitment savings | Purchase rows also carry it; filter ChargeCategory before summing |

Commitment savings on covered usage are ContractedCost minus EffectiveCost. Worked example: list rate 1.00, negotiated rate 0.95, effective rate 0.70 gives commitment savings of 0.25 per unit and negotiated savings of 0.05; reporting 0.30 as commitment savings overstates it.

## Quantities

- PricingQuantity is what the provider charges for after block and tier rules. Use it for cost per unit of price.
- ConsumedQuantity is what was actually used. Use it for utilization.
- Dividing cost by the wrong quantity misstates unit prices, often by a large factor when block pricing applies.

## Classification columns

| Column | Values | Practice |
|---|---|---|
| ChargeCategory | Usage, Purchase, Tax, Credit, Adjustment | Decide which categories belong in each sum |
| ChargeClass | empty (regular) or Correction | Trends use `ChargeClass IS NULL`; analyze corrections separately |
| ChargeFrequency | One-Time, Recurring, Usage-Based | Keep one-time charges out of run rate |
| PricingCategory | Standard, Dynamic, Committed, Other | Dynamic covers spot and similar; Committed is usage priced by a commitment discount |
| CommitmentDiscountStatus | Used, Unused | Unused is waste only once its time window has closed |
| CommitmentDiscountCategory | Spend, Usage | Quantity analysis only makes sense for usage-based commitments |
| ServiceCategory, ServiceSubcategory | Normalized lists | Use for cross-provider grouping; ServiceName is provider-specific |

Capacity reservations (columns from FOCUS 1.1) guarantee availability, not a discount. They have no Purchase rows, and their Used and Unused status is a separate signal from commitment discounts.

## Parties and identifiers

- The provider makes the service available, the publisher produced it and the invoice issuer bills for it. They differ for marketplace, reseller and managed-service purchases: group by publisher for total spend with a software vendor, by invoice issuer for reconciliation. Later FOCUS versions rename some of these columns; check the version.
- Identifiers (BillingAccountId, SubAccountId, ResourceId) are stable; names can change. Join on identifiers.
- Tags is a JSON object whose values are strings, numbers, booleans or null. Providers resolve tag inheritance before the data is published.

## Format rules

- Timestamps are UTC ISO 8601. Periods are inclusive at the start and exclusive at the end.
- Currency codes are ISO 4217.
- Nulls are real nulls, not empty strings or placeholder text.
- Store cost columns with generous precision (for example precision 30, scale 15) so many small amounts aggregate correctly.

## Query shapes

These use generic SQL. JSON extraction differs by engine: DuckDB `json_extract_string(Tags, '$.team')`, BigQuery `JSON_VALUE(Tags, '$.team')`, Snowflake `PARSE_JSON(Tags):team::string`, Athena or Trino `json_extract_scalar(Tags, '$.team')`.

Cost per day by month, to remove the month-length swing:

```sql
-- EffectiveCost, regular charges only, last six full months
SELECT date_trunc('month', ChargePeriodStart) AS month,
       SUM(EffectiveCost) AS effective_cost,
       COUNT(DISTINCT CAST(ChargePeriodStart AS DATE)) AS days,
       SUM(EffectiveCost) / COUNT(DISTINCT CAST(ChargePeriodStart AS DATE)) AS cost_per_day
FROM focus
WHERE ChargePeriodStart >= :start AND ChargePeriodStart < :end
  AND ChargeClass IS NULL
GROUP BY 1
ORDER BY 1;
```

Invoice reconciliation:

```sql
-- BilledCost per invoice; compare with the invoice document to the cent
SELECT InvoiceId, BillingCurrency, SUM(BilledCost) AS billed_cost
FROM focus
WHERE BillingPeriodStart = :billing_period_start
GROUP BY 1, 2
ORDER BY 1;
```

Top movers between two equal windows:

```sql
-- EffectiveCost, regular charges, two seven-day windows
SELECT ServiceCategory, SubAccountId,
       SUM(CASE WHEN ChargePeriodStart >= :current_start THEN EffectiveCost ELSE 0 END) AS current_cost,
       SUM(CASE WHEN ChargePeriodStart <  :current_start THEN EffectiveCost ELSE 0 END) AS previous_cost
FROM focus
WHERE ChargePeriodStart >= :previous_start AND ChargePeriodStart < :current_end
  AND ChargeClass IS NULL
GROUP BY 1, 2
ORDER BY current_cost - previous_cost DESC
LIMIT 10;
```

Allocation coverage for a required tag:

```sql
-- Share of usage EffectiveCost with a usable team tag
SELECT SUM(CASE WHEN json_extract_string(Tags, '$.team') IS NULL
                  OR lower(json_extract_string(Tags, '$.team')) IN ('', 'unknown', 'none', 'tbd')
                THEN EffectiveCost ELSE 0 END) / NULLIF(SUM(EffectiveCost), 0) AS untagged_share
FROM focus
WHERE ChargePeriodStart >= :start AND ChargePeriodStart < :end
  AND ChargeCategory = 'Usage' AND ChargeClass IS NULL;
```

Commitment utilization by commitment:

```sql
-- EffectiveCost of used and unused commitment, closed windows only
SELECT CommitmentDiscountId, CommitmentDiscountCategory,
       SUM(CASE WHEN CommitmentDiscountStatus = 'Used' THEN EffectiveCost ELSE 0 END) AS used_cost,
       SUM(CASE WHEN CommitmentDiscountStatus = 'Unused' THEN EffectiveCost ELSE 0 END) AS unused_cost
FROM focus
WHERE CommitmentDiscountId IS NOT NULL
  AND ChargePeriodEnd <= :closed_through
  AND ChargeClass IS NULL
GROUP BY 1, 2
ORDER BY unused_cost DESC;
```

Corrections summary, kept apart from trends:

```sql
SELECT BillingPeriodStart, ServiceCategory, SUM(BilledCost) AS correction_amount
FROM focus
WHERE ChargeClass = 'Correction'
  AND BillingPeriodStart >= :start
GROUP BY 1, 2
ORDER BY 1, 3;
```
