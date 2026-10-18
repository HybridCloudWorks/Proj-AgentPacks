---
name: cloudflare-change-control
description: "Plan, apply, verify and roll back changes to live Cloudflare accounts, covering Worker deploys and gradual rollouts, secrets, DNS and TLS switches, rule and policy enablement, Zero Trust rollouts, D1 and Durable Object migrations, Terraform applies and cache purges, with pre-change snapshots and post-change evidence. Use when a task will write to a Cloudflare account or affect production traffic, or when a release, rollback or emergency change is requested."
---

# Cloudflare Change Control

## Purpose and activation

Make every write to a Cloudflare account deliberate, staged, verified and reversible. Activate whenever the next step changes an account: deploying or rolling back Workers, setting secrets, editing DNS, TLS, cache or rules, enabling security or Zero Trust policies, running remote migrations or backfills, purging cache, applying Terraform or Pulumi, or creating tokens.

## Scope and exclusions

In scope: pre-change identity and target confirmation, snapshots, blast-radius analysis, approval requests, staged rollout per product, execution of the approved step, post-change verification, rollback, emergency changes and the change record.

Not in scope: deciding what the change should be (product skills) and authoring IaC (cloudflare-iac-and-api-automation). This skill never grants approval; it only executes what was approved.

## Required inputs

- The reviewed change: diff, plan file, guard output or exact settings, and the acceptance criteria.
- The exact target: account, zone, Worker, environment and resource identifiers, and the credential the user has configured for it.
- The approval: who approved which action on which target, in this run, and any window or communication requirement.
- Rollback criteria: the signals and thresholds that trigger rollback, and who decides.

## Dependencies and tools

- The project's Wrangler, Terraform or Pulumi, `cloudflared`, the Cloudflare API or a connected Cloudflare tool, whichever the change uses, run with credentials the user already configured.
- Read-only verification probes (`curl -sI`, `dig`, log queries) against the changed hostnames.
- `change-plan-template.md` in this skill folder.

## Workflow

1. Confirm identity and target. Check which account the credential reaches (`wrangler whoami`, the token verify endpoint, or the provider's configured account) and that it matches the approved target. Stop on any mismatch.
2. Snapshot current state: `wrangler deployments list` and `wrangler versions list`, exported rulesets, DNS record export, settings values, Access and Gateway policy exports, a D1 export or recovery point, or the Terraform plan file. Store snapshots in the workspace, never in chat.
3. Fill in `change-plan-template.md`: steps, blast radius, verification per step, rollback per step, and the approval it relies on.
4. Request any missing approval with the exact action, target, environment, parameters, effect, blast radius, risk, cost, verification and rollback. Reuse an existing grant only for the same action and target.
5. Execute one step at a time with the staged pattern for the product below.
6. Verify after each step against the changed environment and compare with the snapshot. Watch error rates, latency and security events for the agreed window.
7. Roll back on any trigger, then verify the rollback the same way.
8. Record the change: what ran, when, results, deviations and follow-ups.

## Staged patterns by product

Workers
- Upload a version without routing traffic (`wrangler versions upload`), test it on its preview URL, then shift traffic gradually with `wrangler versions deploy` and the documented percentage options, then complete. `wrangler rollback` returns code to a previous version; it does not undo storage migrations, data changes or Durable Object migrations.
- Check current Wrangler behavior for secrets: in recent versions `wrangler secret put` creates and deploys a new version immediately; when staging, use the version-scoped secret commands documented for the installed Wrangler.
- Durable Object migrations apply with the deploy and are not reverted by rollback; a deleted class loses its data. Gradual deployments have documented constraints for Durable Objects and are not available for Workers for Platforms user Workers.

DNS and TLS
- Lower TTLs ahead of record changes; change one record or hostname at a time; verify on authoritative nameservers and on public resolvers; keep old values for rollback. Toggling proxy status changes which IP is exposed and which features apply.
- Before tightening SSL/TLS to Full (strict), verify the origin certificate for every proxied hostname with a direct check; an invalid certificate produces 526 errors for all visitors.
- Enable HSTS only after HTTPS works on every covered hostname, starting with a short max-age.

Rules and security
- Deploy new WAF, rate limiting, bot and API Shield rules in log mode or with a narrow scope, review events, then enforce. Replace rulesets only with a guard-checked full list. Emergency rules carry an expiry.

Zero Trust
- New Access and Gateway policies start disabled or scoped to a pilot group. Enable TLS inspection for pilot devices first. Change device profiles for a pilot group before the default profile. Keep an administrator path that does not depend on the policy being changed.

Data
- Take a D1 export or note the recovery point before remote migrations; run them against staging first; keep migrations forward-compatible with the running code. Backfills are idempotent and resumable, and run in batches.

Cache
- Purge by URL, prefix, hostname or tag; purge everything only with approval and an origin capacity check.

Infrastructure as code
- Apply exactly the reviewed plan file. If the plan is stale or the state changed, re-plan and re-review.

## Emergency changes

During an active incident, the smallest reversible mitigation (a scoped rule, a rollback, a disabled policy) may go first under the incident owner's approval. Record it immediately with an expiry, and bring it through the normal plan and review afterwards.

## Expected output

The change plan, the snapshot locations, the approval used, each executed command or API call with its result, verification evidence per step with environment labels, rollback status, and a completion report. Status is COMPLETE_VERIFIED only when the changed environment was verified; APPLIED_NOT_VERIFIED when the change ran but verification is incomplete; CHANGE_PREPARED_NOT_APPLIED when nothing was applied.

## Validation

- The account and target checked in step 1 match the approval.
- Each step has a recorded result and a verification probe from the changed environment.
- The rollback path was confirmed available before the step ran.

## Failure handling and escalation

- Command fails partway: stop, capture the error, determine what was applied, and either complete or roll back by plan; never retry blindly.
- Verification fails or a trigger fires: roll back, verify the rollback, and report.
- Credential reaches a different account than approved, or lacks a permission: stop and report; never switch credentials or widen a token without approval.
- No rollback exists for a step: say so before execution and get explicit acceptance of that risk.

## Permissions and guardrails

This skill performs Level 2 actions only under explicit, current approval for the exact account, zone, resource, environment and operation, and only with credentials the user configured. It never creates or widens tokens without approval, never prints or passes secrets as arguments, never combines unapproved changes into an approved run, and never treats a successful command as proof of a working change.

## Workflow connection

Within the complete pack, the optional `release-cloudflare-change.prompt.md` recipe connects this skill to the primary `cloudflare-subject-matter-expert` workflow; every product skill hands its live changes here. This skill is self-contained when installed alone. With the full pack installed, the `cloudflare-subject-matter-expert-contract` instruction supplies the approval levels, handoff and completion rules.
