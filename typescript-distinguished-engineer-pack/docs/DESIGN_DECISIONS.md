# Design Decisions

## Thin routing agent, focused Skills

The primary agent owns investigation, planning, implementation, integration, validation, and the final evidence report. Conditional expertise is split into 20 Skills so a task loads only what it needs. This follows the supplied Python engineer reference's useful consolidation pattern without copying Python-specific tooling.

## Specialist reviewers are advisory

Security, testing, and evaluation agents have narrow scopes and return evidence contracts. They do not silently approve, merge, deploy, publish, or change unrelated code.

## Evidence is a product feature

The pack uses explicit completion statuses, handoff and report templates, report validation, repository inventory, and pre/post hooks. Static pack validation is intentionally separate from proving a target repository's runtime or production behavior.

## Vendor-native targets with one source

`.apm` is the canonical source. The builder generates host-specific agent locations, Skill locations, instructions, prompts, and Codex TOML while preserving content parity. Targets are reproducible and archives use a fixed ZIP timestamp.

## Repository-neutral cloud and AI coverage

Azure, AWS, and Google Cloud appear as integration boundaries, not hard-coded environments. MCP and agentic guidance emphasizes schemas, least privilege, bounded execution, provenance, approval, and auditability rather than a particular provider implementation.

## Gap fill 2026-10-18

The pack had no `examples/`, the only failing check in `validate_pack.py`. Prompts and templates already existed and were left unchanged. The fill added `examples/` and `docs/PROMPT_INVENTORY.md`, and updated `README.md` and this file. It made no changes under `.apm/`, nor to `apm.yml`, `compatibility/` or `tests/`.

Decisions and assumptions:

- **One example per prompt workflow.** There are seven examples for nine prompts. Two pairs share one example because the second prompt consumes the first's output:
  - `design-change` and `implement-feature` share `design-and-implement-feature.md`.
  - `design-agentic-system` and `evaluate-agent` share `design-and-evaluate-agentic-system.md`.
- **Outcomes cover every status.** Across the seven examples, all five completion statuses appear:
  - `COMPLETE_VERIFIED`: feature, web flow.
  - `CHANGES_REQUIRED`: pull request review.
  - `IMPLEMENTATION_PREPARED_NOT_VERIFIED`: MCP server, failure diagnosis.
  - `BLOCKED_ON_HUMAN_DECISION`: agentic system.
  - `NOT_VERIFIED`: release readiness.

  The two `COMPLETE_VERIFIED` examples state an explicit local scope and list what lies outside it, to show the status is earned by evidence and not by narrative.
- **Report format.** Every example ends with a completion report in the shape of `templates/completion-report-template.md`. The pull request and release examples put their review verdict in the Recommendation field, as the contract instruction allows. Handoffs use the contract's handoff and response fields.
- **All examples are synthetic.** Repository names, paths, commit ids, counts, prices and command output are invented and illustrative. Each example opens with a notice that it is not evidence from a real run. Fixture identities use reserved names such as `@example.test`.
- **Technology choices are illustration, not recommendation.** Libraries and tools named in the examples (pnpm, Vitest, Fastify, zod, React with Vite, Playwright, OpenTelemetry, the MCP TypeScript SDK) are plausible stack choices for illustration. The skills still require inspecting the target repository's actual stack.
- **MCP approval.** The MCP example enforces human confirmation through MCP elicitation and fails closed when the client does not declare that capability. It makes no claim about which hosts render elicitation; that is listed as unverified.
- **Prompt-to-skill mapping is inferred.** `docs/PROMPT_INVENTORY.md` maps each prompt to skills derived from the prompt text and the skill descriptions, because the prompts do not name skills.
- **README.** The Supporting material list now matches the current layout: `.apm/instructions/`, `.apm/prompts/`, pack-only `tooling/` helpers, and the new `examples/`.

Known gaps left open, because they are outside what a gap fill may change:

- The nine prompts carry only `description`. They have no `agent: typescript-distinguished-engineer`, and they do not name their skills or the contract instruction, both of which the authoring standard expects.
- The README's Downloads and Install sections still describe an older flow: a `--write-report` flag, `quick_validate.py`, a vendor package list without Kiro, and a `.github/skills/README.md` note.
- There is no `docs/SKILL_INVENTORY.md`.

## Shared Python and TypeScript primitives (1.3.0, 2026-10-18)

- The Python and TypeScript Distinguished Engineer packs had shipped different files under the same names: the agent-evaluation-engineer agent, the skills agent-evaluation, agentic-workflow-design, playwright-validation and secure-agent-engineering, the agentic-security instruction, and the evaluate-agent and validate-web-flow prompts. Installed together into the user profile, whichever pack went last silently replaced the other's. In the instruction's case that also dropped the security rules for one language, because each version matched only its own file types.
- Each of these is now one shared copy, byte-identical in both packs and kept in sync from the repository's canonical copy; CI fails if a copy drifts.
- Unlike cloud providers, the two languages differ in concepts: runtime typing (neither enforces types at runtime, for different reasons), concurrency and cancellation (asyncio tasks against one always-running event loop with abort signals), package installation (source builds against npm lifecycle scripts), and test tooling (pytest against Vitest, Jest and Playwright Test). Each shared skill therefore decides the language from the code under change, carries a table of where the languages differ for that work, and keeps one reference per language. It translates concepts and never carries one language's code or idioms into the other.
- Because both languages are in every copy, either pack alone can handle code in either language; the other pack's deeper language skills are simply absent.
- The shared agent states no status names, because the two contracts define different ones; it follows the contract of the pack whose primary delegated the work. Its tool intent is the narrower of the two former sets: edit, read and shell, without web.
- The shared instruction applies to `.py`, `.ts`, `.tsx`, `.mts`, `.cts`, `.js`, `.jsx`, `.mjs` and `.cjs` files plus agent Markdown and MCP JSON files. The TypeScript version had also matched every Markdown, JSON and YAML file, which was broader than its rules need.
- The shared prompts carry no `agent` key, because one prompt cannot name both primary agents; Copilot then runs them with the active agent. Language-specific prompts with the same name in both packs (build-mcp-server, design-change, implement-feature, review-pull-request) still collide and await a naming decision.

## Prompt names qualified (1.4.0, 2026-10-18)

Several packs shipped prompts under the same name with different content, so installing two of them into the user profile silently replaced one pack's slash command with the other's. This pack's prompts now carry the language or provider inside the name; the qualifier is never a prefix. Slash commands change accordingly.

| Old name | New name |
|---|---|
| `build-mcp-server` | `build-typescript-mcp-server` |
| `design-change` | `design-typescript-change` |
| `implement-feature` | `implement-typescript-feature` |
| `review-pull-request` | `review-typescript-pull-request` |
