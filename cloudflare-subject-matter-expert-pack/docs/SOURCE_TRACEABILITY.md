# Source traceability

## Governing inputs

- Brief for this pack: role "CloudFlare Subject Matter Expert", pack name `cloudflare-subject-matter-expert`, delivery rules that override sections 7 and 9 of the master prompt.
- Master prompt: agent-pack-prompt v2.3 (`PORTABLE_AGENT_SKILL_PACK_AUTHORING_PROMPT.md` in this pack).
- Vendor facts: the repository's `client-locations.md`, verified 2026-10-18. Every agent field, tool identifier and APM behavior in this pack comes from it; nothing vendor-related was taken from the web.
- Structural reference: the Python Distinguished Engineer pack, used for file layout, document types and test formats only. None of its role content, names, skills or examples was reused.

## Third-party reference material

- Source: https://github.com/cloudflare/skills (Cloudflare's Agent Skills collection), supplied as a local snapshot.
- License: Apache License 2.0. Copyright remains with its authors.
- Use: knowledge only. The pack's text is newly written. No file was copied, and no reference text is redistributed beyond the short attributed quote below, so no NOTICE obligations arise; this page is the attribution.
- Quote: the reference repeatedly tells agents to "Prefer retrieval over pre-training" (cloudflare/skills, for example `skills/cloudflare/SKILL.md`). The pack adopts the principle in its contract instruction and skills in its own words.
- Directives inside the reference (instructions addressed to an AI, a plugin MCP configuration, slash commands, a wizard that writes files into repositories) were treated as data and not followed.

## What informed which part of the pack

| Pack element | Reference material that informed it |
|---|---|
| cloudflare-solution-architecture | `skills/cloudflare/SKILL.md` decision trees and product index; product READMEs under `skills/cloudflare/references/`; `skills/cloudflare-email-service` (email products) |
| cloudflare-workers-development | `skills/workers-best-practices` (rules and review checklist), `skills/wrangler`, `rules/workers.mdc`, `references/workers`, `references/static-assets`, `references/hyperdrive`; `skills/sandbox-next`, `sandbox-stable` and `sandbox-migrate-to-next` (package-line gate) |
| cloudflare-storage-and-state | `skills/durable-objects` and its rules; `references/kv`, `d1`, `r2`, `queues`, `workflows`, `hyperdrive`, `vectorize`, `secrets-store` gotchas |
| cloudflare-agents-and-ai | `skills/agents-sdk` and its MCP reference; `commands/build-agent.md`, `commands/build-mcp.md`; `references/workers-ai`, `ai-gateway`, `ai-search`, `browser-rendering` |
| cloudflare-edge-delivery-and-performance | `skills/web-perf`; `references/cache-reserve`, `smart-placement`, `argo-smart-routing`, `spectrum`, `snippets`, `images`. DNS, DNSSEC, SSL/TLS modes, edge certificate coverage, cache rules and Origin, Redirect and Transform Rules are not covered by the reference and were written from general Cloudflare knowledge in retrieval-first form (see DESIGN_DECISIONS.md) |
| cloudflare-application-security | `references/waf`, `ddos`, `bot-management`, `api-shield`, `turnstile`; `skills/turnstile-spin` (server-side siteverify checks, single-use tokens, secret handling) |
| cloudflare-zero-trust | `skills/cloudflare-one`; `references/tunnel` |
| cloudflare-migration-planning | `skills/cloudflare-one-migrations` (SASE mapping traps, accounting and validation gates); `references/tunnel` (VPN replacement). DNS, CDN, storage and serverless migration notes were written from general knowledge |
| cloudflare-iac-and-api-automation | `references/terraform`, `pulumi`, `api` gotchas; README MCP server list |
| cloudflare-change-control | `skills/wrangler` (versions, rollback, secrets), `references/workers-for-platforms` (no gradual deployments), WAF and DDoS tuning guidance (log first) |
| cloudflare-observability-and-troubleshooting | `references/observability`, `analytics-engine`, `graphql-api`, `tail-workers`; `skills/cloudflare-one` logs and DEX section |
| Bundled checkers | Original code. The Wrangler checker encodes rules from `workers-best-practices` and `wrangler`; the ruleset guard encodes the "update replaces all rules" gotcha from `references/waf`; the accounting checker encodes the disposition model from `cloudflare-one-migrations` |

## Deliberate departures from the reference

1. The reference tells agents to install Wrangler when missing. The pack asks first, because installing packages changes the workspace and its supply chain.
2. The reference's Turnstile wizard writes a skill file into the user's repository. The pack never writes agent configuration into repositories.
3. The reference plugin auto-registers five remote MCP servers. The pack declares none; connecting a server is the user's choice.
4. The reference's WAF pages disagree with each other on the order of the custom, managed and rate limiting phases. The pack states no order and requires retrieving the current traffic sequence.
5. The reference embeds numeric limits and prices. The pack omits them and requires retrieval with source and date, which is the reference's own stated principle.
6. The reference suggests remote development bindings freely. The pack treats remote bindings and paid inference as approval-gated, because they touch real resources and cost money.
7. One reference page describes D1 as eventually consistent. The pack states the primary is consistent and that read replicas need the Sessions API for read-your-writes, and asks for retrieval to confirm.

## Official sources for task-time retrieval

Listed in `compatibility/vendor-sources.yml` with their use. The agent records each page it relies on, with the date, in the completion report's sources consulted.
