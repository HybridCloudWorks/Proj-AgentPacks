# Design decisions

Version 1.0.0, 2026-10-18. The brief did not allow questions, so every assumption below was made by the author and is recorded here for review.

## Assumptions about the role

1. "CloudFlare" in the role name means Cloudflare, Inc.'s platform; content uses the vendor's spelling, "Cloudflare". The pack name stays as given.
2. The subject matter expert is hands-on: it writes code and configuration and can operate accounts under approval, not only advise. Users are developers, platform and network engineers, security teams, SREs and architects.
3. Scope covers four areas: the developer platform (Workers, storage, AI, Agents SDK), application services (DNS, TLS, caching, rules, performance, WAF, bots, DDoS, API Shield, Turnstile), Cloudflare One (Access, Gateway, device client, Tunnel, DLP, CASB), and automation and operations (Terraform, Pulumi, API, CI, observability, releases), plus migrations onto Cloudflare.
4. Out of scope: contract and pricing negotiation, Cloudflare's internal support processes, registrar transfers as a business process, deep Magic Transit and Network Interconnect engineering (covered only at architecture level), Email Security, and penetration testing.
5. No account, plan, zone, credential, identity provider or MCP server is assumed. Plan tier is always a task-time input because many security and Zero Trust features are plan-gated.

## Structure

6. Eleven skills, grouped by the job a user is doing rather than by product. The reference has thirteen skills and more than sixty product references; mirroring that would create many thin skills. Two cross-cutting skills (change control, observability and troubleshooting) exist because release and diagnosis discipline is shared by every product.
7. One primary agent plus two specialists, each justified in AGENT_INVENTORY.md: a read-only security reviewer (independent review, narrower permissions) and an offline migration analyst (context isolation for large exports, no network). No other specialist met the master prompt's test.
8. Nine prompts, one per primary workflow. Counts were chosen for this role, not inherited.
9. Four instruction files. Only the contract is always on (`applyTo: "**"`), and it states that it applies only to Cloudflare work, because a user-scope install puts it in every repository. The other three are path-scoped to Wrangler configuration and secrets files, Terraform and Pulumi files, and CI workflows, and each says to ignore itself when the file is not about Cloudflare.
10. Three skills bundle stdlib-only Python checkers in their own `scripts/` folder so they work when installed alone. The hook runner imports the Wrangler checker from the pack's own skill folder instead of keeping a second copy.

## Evidence and safety

11. Retrieval first: skills carry procedures and stable behavior but no limits or prices. Agents retrieve and cite current documentation with dates, or mark numbers unverified.
12. Every write to a Cloudflare account is Level 2, including secrets, cache purges, remote D1 commands and Terraform imports. Read-only account inspection is Level 0 only when the user put the account in scope with credentials already configured; log queries stay inside the incident window.
13. Completion statuses add CHANGE_PREPARED_NOT_APPLIED and APPLIED_NOT_VERIFIED to the usual set, because the most common false claim on this platform is "deployed, so done". A complete claim with account changes needs a passing check in the changed environment; every check carries an environment label.
14. Credentials are never requested in chat, printed or passed as arguments; the completion validator rejects reports that look like they contain one.
15. Gradual and observe-first rollouts are the default: Worker versions before promotion, WAF log mode before block, Zero Trust pilots before broad policies, targeted purges before purge-everything.

## Vendor mechanics

16. Agents declare no `tools`; intents live in `compatibility/tool-permissions.yml`. The Gemini mapping omits a web tool because the vendor facts list none.
17. Specialists set `include-custom-instructions: true` so GitHub Copilot subagents read the installed contract; the field is documented for Copilot and ignored or dropped elsewhere.
18. The Claude-only `skills` preload field is not used: APM copies frontmatter verbatim to Copilot, where the field is undocumented, and the agents route to skills by name instead.
19. No MCP servers are declared in `apm.yml`, because connecting remote servers is a consequential action the user should choose.
20. Hooks ship as helper scripts and one reviewed Copilot sample, not native hook definitions, because APM copies hook commands verbatim without deploying their scripts. The session-start hook passes only fixed finding codes and counts to the model, never names or values from repository files.
21. Test metadata files use JSON syntax inside `.yml` files so the shared validator can read them with or without PyYAML.
22. Python helpers target 3.11 or later (TOML parsing uses `tomllib`); they were executed with the Python on the authoring machine through the shared validator.

## Knowledge gaps filled without the reference

23. DNS (proxy status, CNAME flattening, DNSSEC during nameserver moves, CAA), SSL/TLS modes and edge certificate coverage, cache rules and cache status values, Origin, Redirect and Transform Rules, Cloudflare error codes, and DNS, CDN, storage and serverless migration notes were written from general Cloudflare knowledge, because the reference does not cover them and web access was not available. They are phrased as stable behavior with instructions to confirm against current documentation, and they are the first content to re-verify (see MAINTENANCE.md).

## Delivery rules from the brief

24. No `AGENT-PACK-README.md`, `VALIDATION_REPORT.md`, `dist/`, archives, or per-pack copies of the shared validator and builder are created in the pack; the repository's engine produces them.
