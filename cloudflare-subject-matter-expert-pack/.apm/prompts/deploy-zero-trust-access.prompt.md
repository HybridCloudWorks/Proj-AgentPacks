---
description: "Design, stage or troubleshoot Cloudflare One access, Gateway filtering, device client or Tunnel"
agent: cloudflare-subject-matter-expert
argument-hint: "[applications, users or problem]"
---

# Deploy Zero Trust access

## Inputs

Users, groups and identity provider with SCIM status, applications and their types, networks and private DNS, devices and MDM, pilot group and rollback owner.

## Workflow

Apply cloudflare-zero-trust: inventory existing Cloudflare One objects, choose application types and on-ramps, write the change set in dependency order, and stage policies disabled or for a pilot group. Use cloudflare-observability-and-troubleshooting for log-driven diagnosis. Ask `cloudflare-security-reviewer` to review Access and Gateway policies before broad enablement. Apply through cloudflare-change-control with explicit approval per stage.

## Expected output

Design or change set with prerequisites, validation cases and results, rollback, open decisions and a completion report under the `cloudflare-subject-matter-expert-contract` instruction.
