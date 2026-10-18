---
description: "Design a new Notion database or change an existing schema safely"
agent: notion-subject-matter-expert
---

# Design or change a Notion database

## Inputs

What one row represents, the questions the database must answer, who maintains which fields, and the target location. For a change, the existing database link.

## Workflow

Apply notion-database-design. Search for an existing database first. Fetch schemas and identify data sources and dependents. For changes, classify each with the risk matrix, list what breaks, and get approval for Level 2 changes with the undo step (duplicate or export) taken first. Verify by re-fetching the schema and sampling entries.

## Expected output

A schema table, relation map, view list, templates and automations with their notifications, and for changes a risk-classified plan; then the verified result with URLs. Report with the `notion-subject-matter-expert-contract` completion format, including schema impact.
