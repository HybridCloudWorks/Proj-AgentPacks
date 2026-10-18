# Design Decisions

1. Use a thin `github-expert-engineer` router and 18 focused Skills to limit prompt duplication.
2. Treat GitHub content and AI-generated code as untrusted data and preserve human approval boundaries.
3. Keep query helpers read-only, bounded, schema-first, and explicit about owner/repository and pagination.
4. Make mutation guards and hooks available, but never hide authorization behind a script flag.
5. Generate four vendor targets from one canonical source and validate exact Skill parity.
6. Use uppercase `VALIDATION_REPORT.md` as the only validation-report filename.
7. Record official documentation URLs while separating static pack proof from live GitHub state.

## Gap fill 2026-10-18

The pack shipped with empty `examples/`, `templates/` and `.apm/prompts/`. This fill added ten prompts, seven examples and six templates, plus `docs/PROMPT_INVENTORY.md`. No agent, Skill, instruction, `apm.yml` or tool-permission file was changed, so `tests/skill-coverage.yml` was not regenerated.

### Assumptions

1. **Workflows come from the pack itself.** The ten primary workflows are taken from the agent's routing list, the 18 Skills, the five positive cases in `tests/capability-coverage.yml` and the four trigger cases. Governance assessment and governance change planning share one prompt (`review-repository-governance.prompt.md`), because the same three Skills (administration, repository lifecycle, rulesets) define both and the change path ends in an owner decision either way.
2. **No specialists, so handoffs go to people.** The pack has a single agent. `templates/handoff.md` addresses human owners (organization owner, repository admin, security owner, cloud identity owner, release manager), not subagents.
3. **Recommendation meanings.** The contract lists the five values without defining them. The examples and the completion-report template use them this way: READY_FOR_REVIEW for a finished local deliverable that changed nothing live; READY_FOR_MERGE_REVIEW for a PR with no confirmed finding and every gate evidenced on the head SHA, handed to a human for the merge decision; CHANGES_REQUIRED when a confirmed finding blocks; BLOCKED_ON_HUMAN_DECISION when the next step needs an owner's authority or decision; NOT_VERIFIED when evidence the decision depends on could not be obtained.
4. **Severity scale.** The contract names a severity field but no scale. Critical, High, Medium and Low are assumed.
5. **Finding ID prefixes.** `GH-`, `ACT-`, `SEC-` and `FIND-`, because `tooling/validate_github_review.py` detects duplicates only among those prefixes.
6. **Hooks and helpers in prompts.** Prompts are installed content, and `hooks/`, `tools/` and `tooling/` are not installed. The prompts therefore refer to the pre-review inventory and the post-review report check by function ("when the installer has made them available") and never by path. Examples and templates are pack docs, so they use the real paths.
7. **Example data.** Every organization, repository, SHA, run ID, digest and issue number is fictional (`example-org`). Action pin SHAs are shown as `<sha …>` placeholders rather than invented values that could pass for real ones. GitHub API fields, endpoints and `gh` flags are written as GitHub documents them.
8. **Test metadata.** Existing entries in `tests/capability-coverage.yml` and `tests/trigger-cases.yml` were kept unchanged. The fill added a `prompts` map to the first and a `prompt` key, plus one case per new workflow, to the second. The shared validator checks that every referenced prompt file exists.
9. **No new skill inventory.** `docs/SKILL_INVENTORY.md` does not exist, and the fill rules permit creating only `docs/PROMPT_INVENTORY.md`. The Skill-to-prompt map therefore lives in the prompt inventory.
10. **README corrections.** While adding the workflow, example and template sections, two stale statements in `README.md` were corrected: the mutation guard is `tooling/query_guard.py`, not `tools/query_guard.py`, and validation and build run from the shared repository-root tooling, not from scripts inside the pack.

### Interactions found with the pack's own report checker

`tooling/validate_github_review.py` counts every occurrence of a recommendation value and of a finding ID anywhere in the report. Two consequences shaped the examples and the completion-report template:

- The audit Skill's evidence label is spelled the same as the recommendation value NOT_VERIFIED. A report that recommends anything else and also uses the uppercase label fails the "exactly one recommendation" rule. Reports therefore put unobserved items under Skipped checks with lowercase "not verified" wording. The evidence ledger, a separate document, keeps the uppercase label.
- A cross-reference such as "see GH-1" counts as a second ID and fails the duplicate check. Reports write each ID once, in its finding heading, and refer to other findings by title.

All seven examples were checked against the checker's rules (one recommendation value, all five sections, unique IDs, no secret-like strings) by reproducing its regular expressions. The checker itself was not executed in this session.

### Gaps not fixed (outside the files this fill may change)

- `github-review-automation-and-hooks` tells the model to use `tools/query_guard.py`, but the script is at `tooling/query_guard.py`. Because the Skill is installed content and could not be edited, it still names the wrong path.
- `compatibility/compatibility-matrix.yml` and the README download list cover four vendors and omit Kiro, although `apm.yml` targets Kiro. The matrix also lists a Gemini agent path, but APM generates no Gemini agents.
- `tests/` contains no `test_*.py`, so the validator skips pack unit tests. The prompts, examples and templates are checked structurally only. How the agent behaves when it runs these prompts has not been evaluated.
- What APM generates from prompts for Gemini CLI and Kiro is not recorded in the verified vendor facts.
