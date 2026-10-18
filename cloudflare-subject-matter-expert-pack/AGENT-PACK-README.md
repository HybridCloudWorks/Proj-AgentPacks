# cloudflare-subject-matter-expert 1.0.0: artifact catalog

Every file in this pack, with its purpose and location. Contents are in the files themselves.

| ARTIFACT NAME | PURPOSE | LOCATION |
|---|---|---|
| cloudflare-migration-analyst.agent.md | Canonical agent: Offline migration analyst that parses source-platform exports such as Zscaler, Palo Alto, legacy VPN, another CDN or WAF, or a DNS provider, maps every source object to a Cloudflare target or an explicit not-migrated row, and returns a rule accounting table with gaps and decisions. | .apm/agents/cloudflare-migration-analyst.agent.md |
| cloudflare-security-reviewer.agent.md | Canonical agent: Independent read-only reviewer of Cloudflare security posture and changes, covering WAF, rate limiting, bot and DDoS settings, API Shield, Access and Gateway policy, Tunnel exposure, API token scope, secrets handling and Worker code; returns located findings. | .apm/agents/cloudflare-security-reviewer.agent.md |
| cloudflare-subject-matter-expert.agent.md | Canonical agent: Cloudflare subject matter expert who designs, builds, secures, migrates, troubleshoots and releases work on Workers, storage, AI, zone delivery and security, Zero Trust and Cloudflare infrastructure as code, with retrieval-first evidence and guarded account changes. | .apm/agents/cloudflare-subject-matter-expert.agent.md |
| cloudflare-ci-deploy.instructions.md | Canonical instruction: Rules for CI workflows that build, test or deploy to Cloudflare: token handling, environment gates, preview versus production, and verification steps. | .apm/instructions/cloudflare-ci-deploy.instructions.md |
| cloudflare-iac.instructions.md | Canonical instruction: Rules for Terraform and Pulumi code that configures Cloudflare: provider pinning, resource naming, state imports, ruleset ownership, drift and token scope. | .apm/instructions/cloudflare-iac.instructions.md |
| cloudflare-subject-matter-expert-contract.instructions.md | Canonical instruction: Approval levels, specialist handoff rules and the completion report format for the Cloudflare Subject Matter Expert pack. Always on; applies whenever work concerns Cloudflare or this pack's agents, skills and prompts. | .apm/instructions/cloudflare-subject-matter-expert-contract.instructions.md |
| cloudflare-workers-config.instructions.md | Canonical instruction: Rules for Wrangler configuration and local Worker secrets files: compatibility settings, bindings, environments, observability and secret handling. | .apm/instructions/cloudflare-workers-config.instructions.md |
| build-agent-or-mcp-server.prompt.md | Canonical prompt: Build an AI agent, retrieval feature or remote MCP server on Cloudflare | .apm/prompts/build-agent-or-mcp-server.prompt.md |
| build-workers-application.prompt.md | Canonical prompt: Build or change a Cloudflare Workers application with its bindings, storage and tests | .apm/prompts/build-workers-application.prompt.md |
| deploy-zero-trust-access.prompt.md | Canonical prompt: Design, stage or troubleshoot Cloudflare One access, Gateway filtering, device client or Tunnel | .apm/prompts/deploy-zero-trust-access.prompt.md |
| design-cloudflare-architecture.prompt.md | Canonical prompt: Design a Cloudflare architecture or choose Cloudflare products for a workload | .apm/prompts/design-cloudflare-architecture.prompt.md |
| plan-cloudflare-migration.prompt.md | Canonical prompt: Assess and plan a migration onto Cloudflare with rule-by-rule accounting | .apm/prompts/plan-cloudflare-migration.prompt.md |
| release-cloudflare-change.prompt.md | Canonical prompt: Apply, verify or roll back an approved change on a live Cloudflare account | .apm/prompts/release-cloudflare-change.prompt.md |
| review-cloudflare-change.prompt.md | Canonical prompt: Review a Cloudflare-related change: Worker code, Wrangler config, Terraform or Pulumi, rules or policies | .apm/prompts/review-cloudflare-change.prompt.md |
| secure-zone-and-apis.prompt.md | Canonical prompt: Harden a Cloudflare zone and its APIs, tune a false positive, or respond to an attack | .apm/prompts/secure-zone-and-apis.prompt.md |
| troubleshoot-cloudflare-issue.prompt.md | Canonical prompt: Diagnose a Cloudflare error, block, cache surprise, slowdown or connectivity failure | .apm/prompts/troubleshoot-cloudflare-issue.prompt.md |
| SKILL.md | Canonical skill: Build AI features and agents on Cloudflare with Workers AI, AI Gateway, Vectorize and AI Search retrieval, Browser Rendering, the Agents SDK and remote MCP servers built with McpAgent and OAuth, including tool authorization, human approval and cost controls. Use when adding inference, retrieval, chat or scheduled agents, tool-using agents, approval steps, or an MCP server hosted on Cloudflare. | .apm/skills/cloudflare-agents-and-ai/SKILL.md |
| SKILL.md | Canonical skill: Protect Cloudflare zones and APIs with WAF custom and managed rules, rate limiting, bot management, DDoS overrides, API Shield, Turnstile and security event analysis, including expression writing, false-positive tuning, log-first rollout and attack response. Use when hardening a zone, writing or reviewing security rules, tuning a false positive, responding to an attack, or adding bot or API protection. | .apm/skills/cloudflare-application-security/SKILL.md |
| change-plan-template.md | Canonical skill | .apm/skills/cloudflare-change-control/change-plan-template.md |
| SKILL.md | Canonical skill: Plan, apply, verify and roll back changes to live Cloudflare accounts, covering Worker deploys and gradual rollouts, secrets, DNS and TLS switches, rule and policy enablement, Zero Trust rollouts, D1 and Durable Object migrations, Terraform applies and cache purges, with pre-change snapshots and post-change evidence. Use when a task will write to a Cloudflare account or affect production traffic, or when a release, rollback or emergency change is requested. | .apm/skills/cloudflare-change-control/SKILL.md |
| SKILL.md | Canonical skill: Configure and tune zone traffic on Cloudflare: DNS records and proxy status, DNSSEC, SSL/TLS modes and certificates, origin protection, caching and cache rules, redirect, transform, origin and configuration rules, load balancing, Argo and Smart Placement, Images, and Core Web Vitals audits. Use when onboarding a zone, changing DNS or TLS, raising cache hit ratio, fixing redirects or headers, or improving page and origin performance. | .apm/skills/cloudflare-edge-delivery-and-performance/SKILL.md |
| ruleset_guard.py | Canonical skill | .apm/skills/cloudflare-iac-and-api-automation/scripts/ruleset_guard.py |
| SKILL.md | Canonical skill: Author, review and operate Cloudflare automation with the Terraform provider, Pulumi, the REST API and SDKs, Wrangler in CI and Cloudflare MCP tools, covering API token scope, state import and drift, provider upgrades, pagination, rate limits and safe ruleset updates. Use when writing or reviewing Cloudflare Terraform or Pulumi code, scripting the Cloudflare API, building a deploy pipeline, or reconciling dashboard drift. | .apm/skills/cloudflare-iac-and-api-automation/SKILL.md |
| rule-accounting-template.md | Canonical skill | .apm/skills/cloudflare-migration-planning/rule-accounting-template.md |
| rule_accounting.py | Canonical skill | .apm/skills/cloudflare-migration-planning/scripts/rule_accounting.py |
| SKILL.md | Canonical skill: Plan migrations onto Cloudflare from another DNS provider, CDN or WAF, object storage or serverless platform, legacy VPN, or a SASE stack such as Zscaler or Palo Alto, with structured inventories, rule-by-rule accounting, parity gaps, dependency-ordered staging, cutover and rollback. Use when assessing, mapping or sequencing a move to Cloudflare, or checking that every source rule is accounted for. | .apm/skills/cloudflare-migration-planning/SKILL.md |
| SKILL.md | Canonical skill: Diagnose Cloudflare incidents and instrument Workers using Ray IDs, Cloudflare error codes, response headers, Workers Logs and traces, wrangler tail, Tail Workers, Logpush, the GraphQL Analytics API, Analytics Engine, Security Events, Gateway and Access logs and Tunnel diagnostics. Use when a site, API or Worker returns errors, behaves differently through Cloudflare, is slow, is blocked unexpectedly, or needs logging, metrics and alerts. | .apm/skills/cloudflare-observability-and-troubleshooting/SKILL.md |
| decision-record-template.md | Canonical skill | .apm/skills/cloudflare-solution-architecture/decision-record-template.md |
| SKILL.md | Canonical skill: Choose Cloudflare products and design solution architectures across compute, storage, AI, networking, delivery, security and Zero Trust, recording limits, plan entitlements, cost drivers, alternatives and open decisions. Use when someone asks which Cloudflare product fits, how to architect a workload on Cloudflare, or whether a design will hold within platform limits. | .apm/skills/cloudflare-solution-architecture/SKILL.md |
| SKILL.md | Canonical skill: Design and implement data and state on Cloudflare with KV, D1, R2, Durable Objects, Queues, Workflows, Hyperdrive, Vectorize and Secrets Store, covering consistency, concurrency, schema migrations, idempotency, backups and limits. Use when choosing or changing a Cloudflare data store, writing Durable Objects, queue consumers or Workflows, or planning a schema or data migration on Cloudflare. | .apm/skills/cloudflare-storage-and-state/SKILL.md |
| wrangler_check.py | Canonical skill | .apm/skills/cloudflare-workers-development/scripts/wrangler_check.py |
| SKILL.md | Canonical skill: Build, review and test Cloudflare Workers code and Wrangler configuration, including bindings, static assets, service bindings, Hyperdrive, cron and queue handlers, Containers and Sandbox, local development with Miniflare and tests with the Workers Vitest pool. Use when writing or reviewing Worker code, editing Wrangler configuration, or diagnosing Worker build and runtime errors in a repository. | .apm/skills/cloudflare-workers-development/SKILL.md |
| SKILL.md | Canonical skill: Design, configure, troubleshoot and review Cloudflare One deployments: Access applications and policies, identity providers and SCIM, service tokens, Gateway DNS, network and HTTP policies, TLS inspection, DLP and CASB, device client enrollment, device profiles and split tunnels, Cloudflare Tunnel and private networks. Use when replacing a VPN, protecting internal or SaaS applications, filtering user traffic, or diagnosing an Access, Gateway, device client or Tunnel problem. | .apm/skills/cloudflare-zero-trust/SKILL.md |
| apm.yml | APM manifest: name, version, targets. | apm.yml |
| capability-map.yml | Vendor compatibility metadata | compatibility/capability-map.yml |
| compatibility-matrix.yml | Vendor compatibility metadata | compatibility/compatibility-matrix.yml |
| optional-skills.yml | Vendor compatibility metadata | compatibility/optional-skills.yml |
| tool-permissions.yml | Vendor compatibility metadata | compatibility/tool-permissions.yml |
| vendor-sources.yml | Vendor compatibility metadata | compatibility/vendor-sources.yml |
| DESCRIPTION.md | What the pack is for and who uses it. | DESCRIPTION.md |
| AGENT_INVENTORY.md | Pack contract or inventory | docs/AGENT_INVENTORY.md |
| APPROVAL_MATRIX.md | Pack contract or inventory | docs/APPROVAL_MATRIX.md |
| DESIGN_DECISIONS.md | Pack contract or inventory | docs/DESIGN_DECISIONS.md |
| HANDOFF_CONTRACT.md | Pack contract or inventory | docs/HANDOFF_CONTRACT.md |
| INTEGRATION_CONTRACT.md | Pack contract or inventory | docs/INTEGRATION_CONTRACT.md |
| MAINTENANCE.md | Pack contract or inventory | docs/MAINTENANCE.md |
| PROMPT_INVENTORY.md | Pack contract or inventory | docs/PROMPT_INVENTORY.md |
| SKILL_INVENTORY.md | Pack contract or inventory | docs/SKILL_INVENTORY.md |
| SOURCE_TRACEABILITY.md | Pack contract or inventory | docs/SOURCE_TRACEABILITY.md |
| TOOL_PERMISSION_MATRIX.md | Pack contract or inventory | docs/TOOL_PERMISSION_MATRIX.md |
| final-completion-report.md | Worked example | examples/final-completion-report.md |
| gradual-worker-release-workflow.md | Worked example | examples/gradual-worker-release-workflow.md |
| origin-522-troubleshooting-workflow.md | Worked example | examples/origin-522-troubleshooting-workflow.md |
| remote-mcp-server-workflow.md | Worked example | examples/remote-mcp-server-workflow.md |
| copilot-instructions.md | Optional repository-level file | examples/repository/copilot-instructions.md |
| vpn-replacement-migration-workflow.md | Worked example | examples/vpn-replacement-migration-workflow.md |
| waf-false-positive-tuning-workflow.md | Worked example | examples/waf-false-positive-tuning-workflow.md |
| workers-d1-queue-feature-workflow.md | Worked example | examples/workers-d1-queue-feature-workflow.md |
| post-cloudflare-work.ps1 | Hook helper script | hooks/post-cloudflare-work.ps1 |
| post-cloudflare-work.sh | Hook helper script | hooks/post-cloudflare-work.sh |
| pre-cloudflare-work.ps1 | Hook helper script | hooks/pre-cloudflare-work.ps1 |
| pre-cloudflare-work.sh | Hook helper script | hooks/pre-cloudflare-work.sh |
| README.md | Hook helper script | hooks/README.md |
| cloudflare-sme.copilot-hooks.sample.json | Reviewed hook sample, not installed | hooks/samples/cloudflare-sme.copilot-hooks.sample.json |
| LICENSE | License terms. | LICENSE |
| PORTABLE_AGENT_SKILL_PACK_AUTHORING_PROMPT.md | The master prompt this pack was built to. | PORTABLE_AGENT_SKILL_PACK_AUTHORING_PROMPT.md |
| README.md | How to install and use the pack. | README.md |
| completion-report.md | Reusable template | templates/completion-report.md |
| handoff.md | Reusable template | templates/handoff.md |
| wrangler.baseline.jsonc | Reusable template | templates/wrangler.baseline.jsonc |
| capability-coverage.yml | Local test or recorded evidence | tests/capability-coverage.yml |
| applied-not-verified-completion.json | Local test or recorded evidence | tests/fixtures/applied-not-verified-completion.json |
| invalid-completion.json | Local test or recorded evidence | tests/fixtures/invalid-completion.json |
| migration-mapping.csv | Local test or recorded evidence | tests/fixtures/migration-mapping.csv |
| migration-source.json | Local test or recorded evidence | tests/fixtures/migration-source.json |
| ruleset-current.json | Local test or recorded evidence | tests/fixtures/ruleset-current.json |
| ruleset-proposed-drops-rule.json | Local test or recorded evidence | tests/fixtures/ruleset-proposed-drops-rule.json |
| valid-completion.json | Local test or recorded evidence | tests/fixtures/valid-completion.json |
| report-contract.yml | Local test or recorded evidence | tests/report-contract.yml |
| skill-coverage.yml | Local test or recorded evidence | tests/skill-coverage.yml |
| test_cloudflare_pack.py | Local test or recorded evidence | tests/test_cloudflare_pack.py |
| trigger-cases.yml | Local test or recorded evidence | tests/trigger-cases.yml |
| completion_contract.py | Pack-specific helper code | tooling/completion_contract.py |
| hook_runner.py | Pack-specific helper code | tooling/hook_runner.py |
| VALIDATION_REPORT.md | Executed checks and what remains unverified. | VALIDATION_REPORT.md |

## Build outputs (dist/, not committed)

- copilot-cloudflare-subject-matter-expert.zip: 33 files generated by `apm install --target copilot`
- claude-cloudflare-subject-matter-expert.zip: 33 files generated by `apm install --target claude`
- codex-cloudflare-subject-matter-expert.zip: 20 files generated by `apm install --target codex`
- kiro-cloudflare-subject-matter-expert.zip: 24 files generated by `apm install --target kiro`
- gemini-cloudflare-subject-matter-expert.zip: 26 files generated by `apm install --target gemini`
- agent-skills-cloudflare-subject-matter-expert.zip: 17 files generated by `apm install --target agent-skills`
- cloudflare-subject-matter-expert-canonical.zip, cloudflare-subject-matter-expert-prompt.zip, cloudflare-subject-matter-expert-validation.zip, cloudflare-subject-matter-expert-skills.zip, cloudflare-subject-matter-expert-full-pack.zip, SHA256SUMS.txt
