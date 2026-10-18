---
name: cloudflare-application-security
description: "Protect Cloudflare zones and APIs with WAF custom and managed rules, rate limiting, bot management, DDoS overrides, API Shield, Turnstile and security event analysis, including expression writing, false-positive tuning, log-first rollout and attack response. Use when hardening a zone, writing or reviewing security rules, tuning a false positive, responding to an attack, or adding bot or API protection."
---

# Cloudflare Application Security

## Purpose and activation

Configure layered protection for websites and APIs on Cloudflare that blocks real attacks without breaking legitimate traffic, and that can be explained rule by rule. Activate for zone hardening, security reviews, rule and expression authoring, false-positive investigations, active attacks, bot or credential-stuffing problems, API protection and Turnstile integration.

## Scope and exclusions

In scope: the Ruleset Engine model (phases, entry-point rulesets, actions, skip and exceptions), WAF custom rules, managed rulesets and overrides, rate limiting rules, leaked-credential detection, Bot Fight Mode, Super Bot Fight Mode and Bot Management, DDoS managed ruleset overrides, Under Attack mode, API Shield (endpoint management, schema validation, JWT validation, mutual TLS), Turnstile, client-side security, Security Events and Security Analytics.

Not in scope: workforce access control (cloudflare-zero-trust), TLS and origin configuration (cloudflare-edge-delivery-and-performance, though origin lockdown is checked here), applying changes (cloudflare-change-control), and penetration testing.

## Required inputs

- Zone, plan and add-ons (security features differ sharply by plan), the applications and APIs behind it, authentication model, known clients (mobile apps, partners, monitoring, search engines).
- Current rulesets per phase, exported as JSON, and recent Security Events for the paths in question.
- For incidents: timeline, affected hostnames and paths, sample Ray IDs, and business tolerance for challenging users.

## Dependencies and tools

- Current documentation for the Ruleset Engine phases and traffic sequence, the Rules language field reference, managed ruleset contents, rate limiting characteristics, Bot Management fields, API Shield and Turnstile. Retrieve the phase order before explaining precedence; do not state it from memory, because summaries disagree.
- Security Events and Security Analytics (read-only), the GraphQL Analytics API for larger investigations, and ruleset exports.
- `ruleset_guard.py` in the cloudflare-iac-and-api-automation skill, when installed, to check that a proposed ruleset update does not silently drop rules.

## Workflow

1. Inventory: list every entry-point ruleset by phase with its rules, actions, expressions and ownership (dashboard, Terraform, API). Note plan-gated features in use.
2. Check origin exposure first: a proxied hostname whose origin accepts direct traffic makes every rule optional for an attacker.
3. Map threats to controls: injection and known CVEs to managed rulesets; brute force and scraping to rate limiting and bot controls; automated abuse of forms to Turnstile; API abuse to schema validation, JWT validation, mutual TLS and rate limits keyed on identity; volumetric attacks to DDoS overrides.
4. Write rules with the expression rules below. Give every rule a description with purpose, owner, ticket and, for temporary rules, an expiry date.
5. Roll out in observe mode: log action where available, or a managed challenge on a narrow scope, or disabled rules on a staging zone; review a representative window of events; add narrow exceptions; then enforce.
6. Hand application to cloudflare-change-control, including the exported current rulesets for rollback.
7. Re-check Security Events after enforcement for blocked legitimate traffic and for bypasses.

## Ruleset and expression rules

- Rules run by phase; within a phase, terminating actions stop evaluation at the first match. A skip rule only skips what its parameters name: the rest of the current ruleset, specific phases, or specific products. Put skip rules before the rules they bypass and scope them by path and rule ID, never by hostname alone.
- Managed rulesets are deployed with an execute rule in their phase and tuned with overrides (ruleset, category or rule level), not by editing the managed rules.
- Replacing an entry-point ruleset through the API overwrites its entire rule list. Change single rules through the rule-level endpoints or merge with the current list and verify with a guard.
- Field names change between versions of the Rules language (for example, location fields); confirm every field in the current reference. Quote strings, prefer `starts_with`, `eq` and `in` over regular expressions, normalize case with `lower()`, and use lists for IP sets and other reusable values.
- Never deploy an expression of `true` with block, or a broad skip, as a shortcut.
- Rate limiting: count on the request that matters (login, checkout, API method), choose characteristics that identify a client (IP plus a session cookie, header or token when users share NAT or carrier IPs), and set period and mitigation timeout from observed traffic.
- Challenges cannot be solved by native apps, API clients or webhooks. Protect machine traffic with tokens, mutual TLS, schema validation and rate limits instead of challenges.
- Bot scores of 0 mean the score was not computed. Allow verified bots deliberately and confirm them through the verified-bot field, not the user agent.
- DDoS managed protection is always on; overrides adjust sensitivity and action. Under Attack mode challenges every visitor, breaks API clients, and must be scoped and time-limited.
- Turnstile: validate every token server-side with siteverify, require `success`, the expected action and an allowed hostname, treat tokens as single-use, fail closed on network errors, keep the secret in the server's secret store, and use Cloudflare's documented test keys locally.
- API Shield: start schema validation and JWT validation in log mode; mutual TLS requires a client certificate rollout plan.

## Incident response

1. Confirm the attack from Security Analytics or the GraphQL Analytics API: paths, methods, sources (ASN, country, JA3 or JA4 where available), rates and what currently mitigates them.
2. Apply the smallest effective mitigation: a targeted custom rule or rate limit, then broader measures only if needed. Record each emergency rule with an expiry.
3. Watch for collateral blocking and adjust. After the event, convert emergency rules into reviewed permanent controls or remove them.

## Expected output

A posture summary per phase, located findings for reviews (severity, location, evidence, impact, recommended change, blocking), the proposed rules as JSON or Terraform with descriptions, the observe-mode plan with review window and enforcement criteria, and the rollback export.

## Validation

- Each new rule is shown matching sample malicious requests and not matching sample legitimate requests from Security Events or test traffic the user authorized.
- Proposed full-list ruleset updates pass the guard with no unexpected removals.
- Every plan-dependent recommendation names the plan or add-on it needs.

## Failure handling and escalation

- Plan does not include a feature: recommend the available alternative and flag the upgrade as an owner decision.
- False positives during enforcement: switch the specific rule to log or add a narrow exception, never disable the whole managed ruleset.
- An attack exceeds what rules can mitigate: escalate to the account owner and Cloudflare support with Ray IDs and timeline.
- Evidence contains personal data: summarize and redact before sharing.

## Permissions and guardrails

Read-only analysis and local drafting. Creating, changing, enabling or deleting rules, overrides, lists, Turnstile widgets, API Shield settings or Under Attack mode needs explicit approval for the exact zone and rule. Do not send attack traffic, scanners or load tests at any property without written authorization for that property and window. Never put Turnstile secrets or API tokens in code, chat or logs.

## Workflow connection

Within the complete pack, the optional `secure-zone-and-apis.prompt.md` and `review-cloudflare-change.prompt.md` recipes connect this skill to the primary `cloudflare-subject-matter-expert` workflow, and the `cloudflare-security-reviewer` specialist uses it for independent reviews. This skill is self-contained when installed alone. With the full pack installed, the `cloudflare-subject-matter-expert-contract` instruction supplies the approval, handoff and completion rules.
