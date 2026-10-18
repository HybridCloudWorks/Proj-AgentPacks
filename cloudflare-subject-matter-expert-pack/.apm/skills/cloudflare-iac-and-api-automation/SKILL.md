---
name: cloudflare-iac-and-api-automation
description: "Author, review and operate Cloudflare automation with the Terraform provider, Pulumi, the REST API and SDKs, Wrangler in CI and Cloudflare MCP tools, covering API token scope, state import and drift, provider upgrades, pagination, rate limits and safe ruleset updates. Use when writing or reviewing Cloudflare Terraform or Pulumi code, scripting the Cloudflare API, building a deploy pipeline, or reconciling dashboard drift."
---

# Cloudflare IaC and API Automation

## Purpose and activation

Make Cloudflare configuration reproducible and reviewable as code, and make scripts against the Cloudflare API safe to rerun. Activate for Terraform or Pulumi code that uses the Cloudflare provider, scripts or services that call the Cloudflare API or SDKs, CI pipelines that run Wrangler or IaC, token design, provider upgrades, imports and drift.

## Scope and exclusions

In scope: provider pinning and upgrades, resource modeling, state layout, imports and generated configuration, `moved` blocks and state moves, drift handling, plan review, API token design, REST and SDK usage (pagination, rate limits, retries, idempotency), ruleset updates through the API, GraphQL Analytics API queries, Wrangler in CI, and use of Cloudflare MCP tools the user has connected.

Not in scope: deciding what the configuration should be (use the product skills), and running apply, import, destroy or write API calls (cloudflare-change-control).

## Required inputs

- The repository with its provider lock file and versions, backend and state layout, module structure, and CI workflows.
- Which tool owns each Cloudflare object today (Terraform, Pulumi, Wrangler, dashboard, another script).
- Target accounts and zones per environment, and the token or tokens the automation uses (permission groups and resources, never the secret).

## Dependencies and tools

- Provider documentation for the exact pinned version, the Cloudflare API reference, and the SDK documentation for the language in use.
- Terraform or Pulumi CLI for local `fmt`, `validate` and `plan` or `preview`; plans read live state with the configured credentials and must be run only where the user has configured them.
- `scripts/ruleset_guard.py` in this skill folder: a Python 3 checker that compares a current ruleset export with a proposed full rule list and reports added, removed, modified and reordered rules and catch-all rules. It reads local JSON only.

## Workflow

1. Map ownership: list objects by owner. One owner per object; anything managed in two places will flap.
2. Pin and read: confirm the provider version and read resource documentation for that version. Across major versions resources were renamed and attributes reshaped; plan renames as state moves or `moved` blocks, never destroy and create for DNS, Access, tunnels or rulesets.
3. Bring existing objects under management with imports (import blocks or `terraform import`) or generated configuration; never let a plan create a duplicate of an existing record, setting or application.
4. Model safely: separate state per account and environment; variables for account and zone IDs; sensitive variables for secrets supplied from the environment; no secrets in outputs; `lifecycle` ignore rules only for documented provider drift, each with a comment.
5. Review the plan: list every delete, replace and in-place change to DNS records, rulesets, Access applications and policies, tunnels, Workers and zone settings, with the user-visible effect. A plan that replaces a ruleset or tunnel is a blocking finding until explained.
6. For API scripts, apply the API rules below and make every write idempotent (look up before create, use stable names or refs).
7. For ruleset changes through the API, export the current ruleset, build the full proposed list, and run `python3 scripts/ruleset_guard.py --current current.json --proposed proposed.json` (`python` on Windows). Do not proceed while it reports unexpected removals or catch-all rules.
8. Hand apply, import and write calls to cloudflare-change-control with the reviewed plan file or guard output.

## API and token rules

- Use scoped API tokens, not the Global API Key. Grant only the permission groups and accounts or zones the job needs; add IP filtering and expiry where the environment allows; use separate tokens per pipeline and environment. Diagnose 401 (token invalid or missing) separately from 403 (token lacks permission for that resource).
- Read tokens from the environment or a secret manager. Never log request headers, and never pass tokens as command-line arguments.
- Page through list endpoints until done; default page sizes silently truncate results.
- Respect rate limits: bound concurrency, honor `Retry-After`, back off with jitter, and stop on repeated 429 responses rather than hammering.
- Replacing an entry-point ruleset overwrites all its rules; prefer the rule-level create, update and delete endpoints for single-rule changes.
- Inside a Worker, use bindings instead of calling the API for the same account.
- The GraphQL Analytics API is cost-limited; request only the fields, filters and time ranges needed, and discover datasets through the schema for the account's plan.
- Cloudflare's remote MCP servers (documentation, bindings, builds, observability, API) are usable only if the user has connected them; call them by their fully qualified tool names, use read tools freely within scope, and treat write tools exactly like write API calls.

## CI rules

- Store the token and account ID as CI secrets, minimal workflow permissions, no secrets for untrusted fork pull requests.
- Run format, validate, type checks, tests, `wrangler types --check` and plan or dry-run before any deploy step; save the plan as an artifact and apply exactly that plan.
- Gate production with a protected environment or approval, and follow every deploy with a verification step.

## Expected output

Code or review findings (severity, location, evidence, impact, recommended change, blocking), the ownership map, import and state-move steps, a plan summary listing destructive and security-relevant changes, guard output for ruleset changes, and the token permission list the automation needs.

## Validation

- `terraform fmt -check`, `terraform validate` (or Pulumi equivalents) and the plan run cleanly, and the plan shows no unexplained deletes or replacements.
- Imports produce an empty plan for the imported objects before any change is layered on.
- Ruleset updates pass the guard; API scripts were tested against fixtures or a non-production account the user named.

## Failure handling and escalation

- Drift between code and account: report each drifted object and ask which side is authoritative before reconciling.
- A provider upgrade needs many state moves: stage it as its own change with a full plan review.
- Token lacks a permission: name the exact permission group and resource needed; do not suggest a broader token than that.
- Rate limited or partial failure mid-script: stop, report what was written, and resume idempotently.

## Permissions and guardrails

Local authoring, `fmt`, `validate`, `plan` or `preview`, and the guard are allowed. `apply`, `import`, `destroy`, state edits, Pulumi `up`, API writes, token creation and CI runs that deploy are consequential and need explicit approval for the exact account, zone and objects. Never commit state files, plans containing secrets, or tokens.

## Workflow connection

Within the complete pack, the optional `review-cloudflare-change.prompt.md` and `release-cloudflare-change.prompt.md` recipes connect this skill to the primary `cloudflare-subject-matter-expert` workflow, and cloudflare-application-security uses the ruleset guard. This skill is self-contained when installed alone. With the full pack installed, the `cloudflare-subject-matter-expert-contract` instruction supplies the approval, handoff and completion rules.
