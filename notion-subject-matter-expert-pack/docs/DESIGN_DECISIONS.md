# Design decisions

Version 1.0.0, authored 2026-10-18 to agent-pack-prompt v2.3 under the repository's generation brief. The brief did not allow questions, so every assumption is recorded here.

## Role interpretation

1. "Notion Subject Matter Expert" is read as an expert practitioner who works in the user's own workspace through a connector and advises on structure, databases, documentation, meetings, delivery tracking and integrations. It is not a Notion support agent, a Notion employee persona, or an administrator console operator.
2. The users are knowledge workers, team leads, project and product managers, workspace administrators and developers. Writing application code unrelated to Notion, deploying services, administering identity providers and making legal retention decisions are non-goals.

## Assumptions

3. Notion access comes from a Notion MCP server or an integration token the user configures. The pack configures neither. Tool names are taken from the reference collection (notion-search, notion-fetch, notion-create-pages, notion-update-page and others) and treated as examples; agents are told to use the tools the session lists.
4. Most connectors cannot read sharing settings, member lists, audit logs or automation definitions. Reviews and audits ask for that evidence rather than infer it.
5. Notion product and API facts (permission levels, view types, formula functions, data sources, error codes, rate and size limits) come from the author's knowledge, not from browsing, because the brief forbids browsing. Installed content states them as orientation and tells the model to verify plan-dependent features and versioned API limits; `compatibility/vendor-sources.yml` lists the official pages as "to verify".
6. Python 3.10 or later is available wherever the helper scripts run. The scripts use only the standard library.
7. The Claude Code hook sample assumes that exit code 2 from a PreToolUse hook blocks the call and shows stderr to the model, and that MCP tools are named `mcp__<server>__<tool>`. The second fact is in client-locations.md; the first is not, so `hooks/README.md` tells the user to confirm it before relying on the hook.
8. Setting `include-custom-instructions: true` on the reviewer follows client-locations.md guidance for Copilot subagents that must read repository instructions. The key is copied verbatim to Claude Code, which is assumed to ignore it; Kiro and Codex drop it.

## Structure

9. Seven skills, chosen from the role: four reworked from the reference workflows and three added for gaps a Notion expert is routinely asked about (workspace structure and sharing, database modeling and schema-change safety, API and MCP integration). Audits, migrations, formulas, automations, progress tracking and post-meeting capture were folded into those seven rather than shipped as thin skills.
10. Skill names differ from the reference collection's names (for example notion-knowledge-curation rather than notion-knowledge-capture) so that both can be installed side by side in `~/.claude/skills`, `~/.agents/skills` or `~/.kiro/skills` without one overwriting the other, and to signal newly authored content.
11. One specialist, `notion-governance-reviewer`, because it needs fewer permissions than the primary and gives an independent review of the actions hardest to undo in Notion. A separate API engineer, meeting, research or delivery specialist was rejected: each would share the primary's tools, context and approval rules and add only an organization-chart layer.
12. Each skill keeps its outlines and checklists in a reference file inside its own folder, because installed content may reference only installed content and a skill must work alone.
13. Two instruction files: the always-on contract, and a path-scoped instruction for Notion integration code (`**/*notion*.py` and similar, plus `**/notion/**`). The contract's first paragraph limits it to work done through this pack, because `applyTo: "**"` loads it in every repository.
14. Eight prompts, one per main workflow plus a separate audit prompt because audits are read-only and use the reviewer.
15. The pre-publication check exists twice by necessity: as prose in each skill's validation section (installed, so the model can apply it) and as `tooling/notion_draft_check.py` (not installed, for people, CI and the hook sample). The script automates the same checklist.

## Contract choices

16. Approval levels are tailored to Notion. Writes are visible to everyone who can see the parent, so Level 1 is limited to additive writes in a location the user chose. Moves are Level 2 because they change inherited permissions. Mentions, assignments, comments and automations are Level 2 because they reach other people. There is no numeric bulk threshold, which would be arbitrary policy; instead, any batch whose exact list the user has not seen is Level 2.
17. The status `PREPARED_NOT_VERIFIED` replaces an implementation-oriented status, and the fallback sentence is "The Notion work is prepared, but it is not verified in the workspace." Both cover the two common gaps: no connector or approval, and a write that was not re-fetched.
18. Checks carry a `method` of fetch, command or manual, because most Notion verification is a re-fetch rather than a command. Only command checks need an exit code. A `COMPLETE_VERIFIED` report with workspace changes must include a passing fetch check and a URL for every change.

## Changes to reference behaviour

19. The reference recommends cross-linking a meeting's agenda and pre-read. For meetings with external participants the pack links one way only (pre-read to agenda), because an internal page's title in an external agenda is itself a leak.
20. The reference creates tasks directly from a spec; the pack shows the task list first unless the user already approved it, because creating entries in a shared database can fire automations and notifications, and it leaves assignees empty unless names are given.
21. The reference refers to the model by vendor name when it means general knowledge. The pack says "general knowledge" so that the content stays vendor-neutral across five clients.
22. Directives inside the reference material were treated as data and not followed.

## Delivery

23. Per the brief, the pack contains no artifact catalog, validation report, archives or copies of the shared validator and builder. The README describes those as build outputs of the shared tooling.
24. `apm.yml` contains exactly the fields the brief lists.
25. The files under `tests/` with a `.yml` extension are written as JSON, which is valid YAML, following the exemplar; the shared validator can parse them with or without PyYAML.
26. Fixtures are synthetic. Credential-shaped test strings are built at runtime in `tests/test_behavior.py`, so no file in the pack contains one that a secret scanner would flag.
27. No repository-level Copilot instructions example is shipped. The integration-code instruction already generates into `.github/instructions` on a project install, which Copilot code review reads, so a second hand-written copy would only drift.
