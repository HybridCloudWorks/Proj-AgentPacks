---
description: "Assess and plan a migration onto Cloudflare with rule-by-rule accounting"
agent: cloudflare-subject-matter-expert
argument-hint: "[source platform and scope]"
---

# Plan a migration to Cloudflare

## Inputs

The source platform and scope, structured exports with hit counts, target account and plan, identity readiness, cutover window and rollback owner.

## Workflow

Apply cloudflare-migration-planning. For large exports, delegate the rule-by-rule mapping to `cloudflare-migration-analyst` with the export file paths, the assigned output folder, and the Cloudflare documentation excerpts it needs; it works offline. Run the rule accounting checker on the result. Use the product skills to design the target objects. Nothing is created or switched without per-wave approval through cloudflare-change-control.

## Expected output

Assessment, accounting table and checker summary, prerequisites in order, wave plan with pilot, validation and rollback, owner decisions, and a completion report under the `cloudflare-subject-matter-expert-contract` instruction.
