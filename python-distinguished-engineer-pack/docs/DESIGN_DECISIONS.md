# Design decisions

1. Recreate Python Distinguished Engineer from its user specification and later primary/specialist clarification. The existing trainer pack is an independent artifact; none of its curriculum or persona content is imported.
2. Keep the established canonical .apm source, uppercase DESCRIPTION/VALIDATION_REPORT, authoring prompt, compatibility/docs/tests/tooling/hooks, instructions/prompts/examples/templates, vendor targets and archive families. Copilot retains the exact five-agent/eighteen-Skill/five-instruction/ten-prompt/six-example map.
3. One user-facing primary owns all workflows. Specialists remain optional and in the same agents directory. Copilot uses user-invocable false for specialists and agent delegation on primary; other hosts use documented role/config capabilities without a false universal picker promise.
4. Security gets read/search only, since shell access would defeat a genuine read-only boundary. Performance gets bounded measurement without edit. Tests/eval workers have narrowly assigned edits, with host policy enforcing actual execution permissions.
5. No generic browser/test/mcp tool aliases. External tools and SDKs require independently verified identity/scope; none is preinstalled. Codex approval/sandbox inheritance is documented accurately.
6. Hooks inspect metadata and completion evidence deterministically; they do not auto-run arbitrary repository scripts or approve actions. Missing post-session evidence requests one correction then returns a bounded failure status to avoid loops.
7. Build from an explicit manifest into deterministic archives, omitting cache/legacy files. Generate an ordered full-content artifact catalog and verify archive bytes, paths, parity and embedded report freshness.
8. APM-friendly means preserved source layout and manifest; no undocumented APM schema/version compatibility claim. Live client invocation, cloud behavior and provider evaluation require separate evidence.

## 2026-10-18: restructured to agent-pack-prompt v2

- `apm.yml` limited to APM-defined fields; `targets` declared (copilot, claude, codex, kiro, gemini, agent-skills).
- Instructions and prompts moved under `.apm/` so APM generates `.github/instructions`, `.claude/rules`, `.kiro/steering`, Claude commands, Copilot prompts and Gemini commands from one source.
- Hand-built `targets/` removed; vendor packages are produced by `tooling/build_pack.py` through `apm install` into a scratch project.
- `tools` removed from agents in favour of `compatibility/tool-permissions.yml` (see TOOL_PERMISSION_MATRIX.md).
- Native hook JSON moved to `hooks/samples/`; see hooks/README.md.
- Repository-level `copilot-instructions.md` moved to `examples/repository/` as an optional extra for GitHub Copilot code review.
- Archives are build outputs under `dist/`, not committed. The artifact catalog lists files instead of embedding them.
