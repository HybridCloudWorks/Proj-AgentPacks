# Knowledge and integration contract

The pack configures no integration. Everything below describes how the agents use tools the user already has, and what must be discovered for each task.

## Billing data

- **FOCUS exports** are the default. Check the FOCUS version, data generator, currency and freshness from metadata before querying.
- **AWS**: Cost and Usage Report or Data Exports (including the FOCUS export where enabled), typically queried in a lakehouse or warehouse. Unblended cost is the cash view; the amortized commitment columns give the accrual view.
- **Azure**: Cost Management exports (actual, amortized, FOCUS). Confirm the agreement type first because column shapes differ.
- **Google Cloud**: the detailed billing export in BigQuery; show cost before and after credits.
- **OCI and SaaS**: cost reports or invoice exports; check whether a FOCUS version is available.
- Access is read-only, through local files or a query tool the user configured. Scans are bounded by date or partition; material scans are Level 2.

## Operational data

Monitoring metrics (utilization, traffic, healthy targets), inventory exports, flow logs and cluster cost data are read where the user supplies them or where a configured tool exposes them. The agents do not enable logging or install collectors.

## Pricing and terms

Provider pricing pages, calculators and commitment documentation are read on the date of use and cited with that date. The primary's web intent covers public pages only; no billing data, identifiers or negotiated rates go into a request.

## Business data

Driver volumes, customer counts and revenue come from the organization's authoritative systems through the user. The agents never invent them.

## Delivery surfaces

Outputs are shaped for where each audience already works: tickets, pull request comments, finance workbooks, business review decks, team dashboards. The agents prepare drafts. Posting, sending or publishing is Level 2.

## MCP and connectors

None is installed or assumed. If the user has a billing, warehouse or ticketing connector, the agents use it only within its documented tools and the approval levels; a connector's tool description does not grant permission.
