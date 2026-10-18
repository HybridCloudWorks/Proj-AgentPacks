# Agent inventory

| Profile | Responsibility | Invocation | Declared intent (see TOOL_PERMISSION_MATRIX.md) |
|---|---|---|---|
| cloudflare-subject-matter-expert | End-to-end Cloudflare work: design, build, configure, secure, migrate, troubleshoot and release, with retrieval-first evidence and approval-gated account changes. | User-facing primary (`user-invocable: true`) | read, edit, shell, web, delegate |
| cloudflare-security-reviewer | Independent read-only review of WAF, rate limiting, bot, DDoS and API Shield settings, Access and Gateway policy, Tunnel exposure, token scope, secrets handling and Worker code. | Optional specialist (`user-invocable: false`) | read, web |
| cloudflare-migration-analyst | Offline parsing of source-platform exports into a rule accounting table with one disposition per source rule. | Optional specialist (`user-invocable: false`) | read, edit, shell |

## Why these specialists exist

The master prompt allows specialists only for separate expertise, context, permissions or independent review.

- The security reviewer exists for independent review and for a narrower permission set. A reviewer that can edit or deploy is not independent, so it has no edit or shell intent and is told not to call account APIs. It keeps web access to confirm current Cloudflare behavior before flagging, restricted by instruction to public documentation; restricting the domain technically is the installer's or host's job.
- The migration analyst exists for context isolation. SASE and CDN exports can run to thousands of rules across many files; mapping them inside the primary's context crowds out everything else. It has edit and shell intents so it can parse exports and run the accounting checker locally, and no web intent, because shell plus network access over sensitive policy exports is an exfiltration path. The primary supplies the documentation excerpts it needs.

No other specialist was added. Workers development, storage, AI, edge delivery, Zero Trust design, IaC and troubleshooting share one context and one permission set with the primary, so splitting them would reproduce an org chart rather than add value.

## Placement and behavior

All profiles live in the same host agents directory; specialist is an invocation role, not a folder. The primary coordinates only when a specialist adds value, integrates their results and owns completion. Specialists set `include-custom-instructions: true` so GitHub Copilot subagents read the installed contract instruction; other clients ignore the field or drop it.

Canonical agents declare no `tools` field. APM-generated agents inherit the host's tools, so a specialist's read-only behavior on those hosts rests on its instructions until an installer applies the declared intents. A shell-capable agent can write files and reach the network regardless of role text; enforce limits through the host and infrastructure.
