---
description: "Harden a Cloudflare zone and its APIs, tune a false positive, or respond to an attack"
agent: cloudflare-subject-matter-expert
argument-hint: "[zone, application or incident]"
---

# Secure a zone and its APIs

## Inputs

Zone, plan and add-ons, applications and API clients, current ruleset exports per phase, recent Security Events, and for incidents the timeline and sample Ray IDs.

## Workflow

Apply cloudflare-application-security: inventory rulesets and origin exposure, map threats to controls, draft rules with descriptions, and plan an observe-then-enforce rollout. Check proposed full-list ruleset updates with the ruleset guard from cloudflare-iac-and-api-automation. Delegate an independent read-only review to `cloudflare-security-reviewer` when the change is broad or production-critical. Apply changes only through cloudflare-change-control with explicit approval.

## Expected output

Posture summary, located findings with severity, proposed rules, the rollout and enforcement criteria, rollback exports, and a completion report under the `cloudflare-subject-matter-expert-contract` instruction.
