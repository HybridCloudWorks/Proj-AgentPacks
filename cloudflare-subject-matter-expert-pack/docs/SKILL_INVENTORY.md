# Skill inventory

| Skill | Activation | Bundled files | Workflow prompt |
|---|---|---|---|
| cloudflare-solution-architecture | Product selection, workload design, fit against limits and plans. | `decision-record-template.md` | design-cloudflare-architecture.prompt.md |
| cloudflare-workers-development | Worker code and Wrangler configuration written, reviewed or failing. | `scripts/wrangler_check.py` | build-workers-application.prompt.md |
| cloudflare-storage-and-state | Choosing or changing KV, D1, R2, Durable Objects, Queues, Workflows, Hyperdrive, Vectorize; schema or data migrations. | none | build-workers-application.prompt.md |
| cloudflare-agents-and-ai | Inference, retrieval, Agents SDK, approval steps, remote MCP servers. | none | build-agent-or-mcp-server.prompt.md |
| cloudflare-edge-delivery-and-performance | Zone onboarding, DNS, TLS, caching, rules, load balancing, performance audits. | none | troubleshoot-cloudflare-issue.prompt.md |
| cloudflare-application-security | Zone hardening, rules and expressions, false positives, attacks, bot and API protection, Turnstile. | none (uses the ruleset guard when its skill is installed) | secure-zone-and-apis.prompt.md |
| cloudflare-zero-trust | VPN replacement, internal and SaaS app access, Gateway filtering, device client and Tunnel problems. | none | deploy-zero-trust-access.prompt.md |
| cloudflare-migration-planning | Assessing, mapping and sequencing moves onto Cloudflare; checking every source rule is accounted for. | `scripts/rule_accounting.py`, `rule-accounting-template.md` | plan-cloudflare-migration.prompt.md |
| cloudflare-iac-and-api-automation | Terraform, Pulumi, API scripts, CI pipelines, drift and provider upgrades. | `scripts/ruleset_guard.py` | review-cloudflare-change.prompt.md |
| cloudflare-change-control | Any write to a Cloudflare account; releases, rollbacks, emergency changes. | `change-plan-template.md` | release-cloudflare-change.prompt.md |
| cloudflare-observability-and-troubleshooting | Errors, unexpected blocks, slowness, connectivity failures; logging and alerting. | none | troubleshoot-cloudflare-issue.prompt.md |

Each SKILL.md has the ten operational sections the master prompt requires: purpose and activation, scope and exclusions, required inputs, dependencies and tools, workflow, expected output, validation, failure handling and escalation, permissions and guardrails, and workflow connection. `tests/test_cloudflare_pack.py` checks that every skill has them and that every bundled file a skill names exists.

Every skill is useful installed alone: it states its own approval rule for account writes and names the contract instruction only as the fuller source when the whole pack is installed. The bundled Python checkers use only the standard library (Python 3.11 or later for TOML parsing), read local files, make no network calls and never print secret values.

Why eleven: the role spans four Cloudflare areas (developer platform, application services, Zero Trust, automation and operations) and the reference material covers more than sixty products. Grouping by the job a user is doing, rather than by product, keeps each skill strong and avoids sixty thin ones; the two cross-cutting skills (change control, observability) exist because every product shares the same release and diagnosis discipline.
