# Governance, maintenance and versioning

Pack version 2.1.0 follows agent-pack-prompt v2.2. The canonical `.apm/` source is authoritative; vendor files are generated at install time by APM or by the Code Workflow installer and are never edited by hand. Change source first, update capability, trigger and report tests, run the repository's shared `tooling/validate_pack.py <pack> --install-check`, then `tooling/build_pack.py <pack>` for release archives.

Use semantic versioning: major for incompatible instruction/tool/contract changes; minor for compatible capabilities; patch for corrections. Track exact commit/tag plus prompt/tool/model/SDK versions in consumers. Do not pin an unrequested model in generated profiles. Review official vendor schemas when upgrading clients and verify discovery with installed CLI/IDE; surface support can differ.

Owners approve significant architecture/security/data/permission/release decisions. Reassess Skills from observed failures and realistic tasks; do not accumulate universal rules from isolated examples. Remove duplicate domain prose, maintain provenance dates and retire outdated guidance with migration notes.

## Known limits and unresolved operational inputs

Target repository/tool versions, framework, acceptance thresholds, production identities, data classifications, paid evaluation budgets and deployment authority must be discovered for each task. Live discovery in Claude Code, Codex, Copilot, Kiro and Gemini CLI, browser sessions, SDK protocol initialization, cloud integration and paid model quality are not established by local tests. Subagent metadata cannot guarantee independence or access isolation across every client. APM 0.33.0 validation and a project-scope install for all six targets were executed on 2026-10-18; user-scope installs were not.

## Genuine not-applicable artifacts

No live tenant credential/MCP registration/deployment manifest is generated: the reusable pack has no concrete environment. The integration contract retains that artifact purpose and explains task-time inputs. All canonical categories remain present.
