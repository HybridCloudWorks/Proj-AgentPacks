You are completing an existing agent pack that is missing required artifacts. Work only inside the current directory. You cannot ask questions; make reasonable assumptions and record them in `out/$pack_dir/docs/DESIGN_DECISIONS.md` under a heading "Gap fill $date".

## Workspace

- `standard/agent-pack-prompt.md`: the master prompt. Sections 2, 4 and 8 define what these artifacts must be.
- `standard/client-locations.md`: verified vendor facts, including what APM generates from prompts. Do not browse the web.
- `exemplar/`: a complete pack. STRUCTURAL REFERENCE ONLY: reuse its formats for prompts, examples and templates, never its role content or wording.
- `tooling/`: the shared validator and skill-coverage generator.
- `out/$pack_dir/`: the pack to complete. Its agents, skills and instructions are the source of truth for the role.

## Missing artifacts to author

$missing

## Rules

1. Read the pack's agents, skills and contract instruction first. Every artifact you write must serve workflows those skills already define, and must use their exact names. Do not invent capabilities the skills do not cover.
2. Prompts go in `.apm/prompts/<task>.prompt.md` with frontmatter `description` (required) and `agent: <primary agent name>`. Write one per primary workflow, typically 5 to 10. Each states inputs, the workflow (naming the skills it applies), the expected output, and that it follows the pack's contract instruction. Prompts are installed content: they may reference only installed content.
3. Examples go in `examples/<workflow>.md`: worked, realistic walkthroughs of the pack's main workflows, each ending with a completion report in the contract's format. Include one that shows a blocked or unverified outcome. Typically 4 to 7.
4. Templates go in `templates/`: the reusable documents the skills tell the agent to produce, such as handoff, completion report, and the role's own plans or records. Typically 3 to 6.
5. You may update only these existing files: `docs/PROMPT_INVENTORY.md` (create it if missing), `docs/SKILL_INVENTORY.md`, `README.md`, `tests/capability-coverage.yml` and `tests/trigger-cases.yml` (to reference the new prompts by file name), and `docs/DESIGN_DECISIONS.md`.
6. Do not change anything under `.apm/agents/`, `.apm/skills/` or `.apm/instructions/`, nor `apm.yml` or `compatibility/tool-permissions.yml`. The engine fails the run if you do.
7. Run `python tooling/skill_coverage.py out/$pack_dir` if you touched skills (you should not have), then `python tooling/validate_pack.py out/$pack_dir --install-check --no-report`, and fix every failure in the files you own. Repeat until it reports PASS.
8. End with one short paragraph: what you added, the validator's final line, assumptions, and gaps.
