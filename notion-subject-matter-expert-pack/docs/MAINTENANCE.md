# Governance, maintenance and versioning

Pack version 1.0.0 follows agent-pack-prompt v2.3. The canonical `.apm/` source is authoritative; vendor files are generated at install time by APM or by the Code Workflow installer and are never edited by hand.

## Making a change

1. Change the source under `.apm/` first.
2. Update `tests/capability-coverage.yml` and `tests/trigger-cases.yml` so they still name every skill, and `tests/report-contract.yml` if the report format changes; keep the contract instruction in step with it.
3. Regenerate `tests/skill-coverage.yml` with the repository's shared `tooling/skill_coverage.py <pack>` whenever a skill is added, removed or its description changes.
4. Run `python -m unittest discover -s tests`, then the shared `tooling/validate_pack.py <pack> --install-check`, then the shared builder for release archives.

Use semantic versioning: major for incompatible changes to the contract, approval levels, report fields or agent names; minor for new capabilities; patch for corrections.

## Keeping Notion facts current

Notion changes features, labels, plan limits and API versions. Review the skills' reference files against Notion's help center and API changelog at least twice a year and whenever Notion announces a new API version. Pay particular attention to data sources, permission levels, automation options, view types, Trash and history retention, and rate or size limits. Update `compatibility/vendor-sources.yml` with the verification date.

## Ownership

The pack owner approves changes to approval levels, the reviewer's scope and the report contract. Reassess skills from observed failures in real use rather than adding rules for isolated cases.

## Known limits

- No live Notion workspace was used. Connector behaviour, tool names and what each server exposes are task-time facts.
- The reviewer's read-only boundary is behavioural in APM-generated agents, which inherit all host tools.
- Gemini CLI receives no agents from APM, so reviews there are performed by the primary and are not independent.
- The draft check matches common credential shapes and simple markers; it cannot recognize every secret or every piece of internal content.

## Not established

- Agents appearing and running in the VS Code agent pane, or in any client's picker.
- A user-profile install behaving identically on Windows and macOS.
- Live Kiro, Gemini CLI, Claude Code, Codex and Copilot behaviour with a real Notion MCP server.
- Model behaviour when the agents are invoked; the unit tests cover the helper scripts and cross-file contracts only.
- Hook behaviour: the hook ships as a helper and a sample; no native hook was installed or exercised.

## Artifacts deliberately absent

- No MCP server registration, integration token, OAuth client or webhook endpoint: the reusable pack has no concrete workspace. The integration contract describes them as task-time inputs.
- No repository-level Copilot instructions example: the path-scoped integration-code instruction already generates into the repository's instruction folder on a project install.
- No artifact catalog, validation report or archives in the source: the shared tooling produces them as build outputs.
