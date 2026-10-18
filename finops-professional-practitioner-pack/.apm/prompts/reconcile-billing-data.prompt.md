---
description: "Check billing data health and reconcile it to invoices, or plan a FOCUS parallel run"
argument-hint: "data source, billing period, invoice totals if available"
agent: finops-professional-practitioner
---

# Reconcile billing data

## Inputs

The dataset and its schema, the billing period, the billing accounts expected, and invoice totals or provider console totals for comparison. For a FOCUS migration, the legacy export and the consumers that depend on it.

## Workflow

Apply focus-billing-data-analysis. Read metadata, confirm every expected billing account and day is present, measure corrections and allocation coverage, sum BilledCost per InvoiceId or per billing account and compare with the invoice, and explain the expected gap between EffectiveCost and the invoice. For a migration, lay out the parallel-run stages and the consumer order. finops-data-analyst can run the checks in its own context.

## Expected output

A data-health report, a reconciliation table with expected, observed and difference per invoice, explained divergences, open gaps with likely causes and owners, and the completion report from the `finops-professional-practitioner-contract` instruction. Changing exports or pipelines is a Level 2 action.
