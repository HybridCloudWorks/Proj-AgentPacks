---
description: "Apply, verify or roll back an approved change on a live Cloudflare account"
agent: cloudflare-subject-matter-expert
argument-hint: "[change, target account or zone, environment]"
---

# Release a Cloudflare change

## Inputs

The reviewed change (diff, plan file, guard output or settings), the exact account, zone, Worker and environment, the configured credential, the approval for this action and target, and the rollback triggers.

## Workflow

Apply cloudflare-change-control: confirm the credential reaches the approved target, snapshot current state, fill in the change plan, request any missing approval, execute one staged step at a time, verify each step in the changed environment, and roll back on any trigger. Use cloudflare-iac-and-api-automation for plan files and ruleset guards.

## Expected output

The change plan, snapshots, commands with results, verification evidence per step, rollback status, and a completion report under the `cloudflare-subject-matter-expert-contract` instruction: COMPLETE_VERIFIED only with verification in the changed environment, otherwise APPLIED_NOT_VERIFIED or CHANGE_PREPARED_NOT_APPLIED.
