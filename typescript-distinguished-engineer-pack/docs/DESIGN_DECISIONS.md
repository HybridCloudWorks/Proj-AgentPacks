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
