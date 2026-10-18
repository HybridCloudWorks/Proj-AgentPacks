# Prompt inventory

| Prompt | Skills | Expected output |
|---|---|---|
| design-cloudflare-architecture.prompt.md | solution-architecture, plus storage, AI or edge as needed | Architecture brief with sourced limits, decisions and open questions; analysis status. |
| build-workers-application.prompt.md | workers-development, storage-and-state | Diff, checker result, tests, release notes; prepared, not applied. |
| build-agent-or-mcp-server.prompt.md | agents-and-ai, workers-development, storage-and-state | Agent or MCP contract, code, evaluation cases, cost notes. |
| secure-zone-and-apis.prompt.md | application-security, iac-and-api-automation (guard) | Posture summary, findings, proposed rules, observe-then-enforce plan, rollback exports. |
| deploy-zero-trust-access.prompt.md | zero-trust, observability-and-troubleshooting | Dependency-ordered change set, pilot staging, validation cases, rollback. |
| plan-cloudflare-migration.prompt.md | migration-planning, product skills; delegates to the migration analyst | Assessment, accounting table and checker summary, wave plan, owner decisions. |
| review-cloudflare-change.prompt.md | workers-development, iac-and-api-automation, product skills; delegates to the security reviewer | Located findings, checks run, review limits; read-only. |
| troubleshoot-cloudflare-issue.prompt.md | observability-and-troubleshooting, edge, security, zero-trust, workers | Diagnostic report with evidence, cause or ranked hypotheses, next test. |
| release-cloudflare-change.prompt.md | change-control, iac-and-api-automation | Change plan, snapshots, executed steps, verification per step, rollback status. |

All prompts set `agent: cloudflare-subject-matter-expert` and an `argument-hint`. APM installs them as Copilot prompt files, Claude commands (the `agent` key is dropped) and Gemini commands. Codex and Kiro receive no prompts; their users invoke the primary agent directly, and the skills carry the same workflows.
