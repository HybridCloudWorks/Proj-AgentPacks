# Design Decisions

## Hypervelocity is an operating model

The Agent is broader than a workflow author but remains grounded in the supplied gh-aw domain. It helps choose the right automation mechanism and guardrail level; it does not become a generic software architect or deployment operator.

## Thin Agent and progressive Skills

The two supplied Agent files are duplicates. One canonical Agent owns routing and boundaries. Procedures remain in nine Skills so the runtime loads only the relevant guidance.

## Gap closures

- `workflow-lifecycle-and-release` adds compile, validate, run, lock-file, upgrade, and source/compiled parity controls.
- `agent-governance-and-guardrails` adds permission, safe-output, MCP, network, secret, and approval decision rules.
- `agent-delegation-and-composition` adds agent selection, subagent boundaries, context handoff, deterministic-tool choice, and failure containment.
- `workflow-observability-and-evaluation` adds run summaries, telemetry, cost/quality measurement, experiments, and regression evidence.
- `agent-usage-reporting` gives the supplied hook one owner and preserves its non-blocking, opt-in behavior.

## Source versus additions

Source-derived gh-aw routing, token efficiency, Copilot review handling, and the usage hook are retained. Gap closures are pack additions supported by current gh-aw guidance and clearly labeled as additions in this document.

## Gap fill 2026-10-18

The pack was missing its prompts, examples and templates. This fill added them without changing agents, Skills, instructions, `apm.yml` or tool permissions.

### Added

- Ten prompts in `.apm/prompts/`: design-agent-mechanism, author-gh-aw-workflow, diagnose-gh-aw-run, upgrade-gh-aw-workflow, optimize-workflow-cost, compress-agent-prompt, resolve-review-feedback, review-agent-guardrails, evaluate-workflow-reliability, report-agent-usage.
- Seven examples in `examples/`, one of which (`blocked-auto-merge-request.md`) ends blocked, while `author-gh-aw-workflow.md` and `report-agent-usage.md` end partly unverified.
- Six templates in `templates/`: completion report, delegation handoff, guardrail decision record, review feedback ledger, optimization plan with evaluation record, workflow release gate.
- `docs/PROMPT_INVENTORY.md`; prompt sections in `README.md`; `prompt_map` in `tests/capability-coverage.yml`; `workflow_prompt` on every case in `tests/trigger-cases.yml`, plus five cases so every prompt is referenced.

### Decisions and assumptions

1. **Workflows come from the Skills.** Each prompt is a workflow that the agent's routing list and the Skills already define. Create and update share one prompt because `agentic-workflows` makes that distinction itself and both paths apply the same guardrail and compile steps. Upgrade gets its own prompt because the router and `workflow-lifecycle-and-release` treat it as a separate route with its own lock-diff review.
2. **Prompt names avoid upstream gh-aw names.** The router loads upstream procedures called create, update, debug and upgrade agentic workflow. Pack prompts use different names so the two never share a file name once installed.
3. **Prompts carry only `description` and `agent`.** This matches the master prompt and the structural exemplar. Claude drops `agent` with a warning, as recorded in `client-locations.md`.
4. **Prompts describe outputs inline.** Templates are not installed, so prompts name the fields to return rather than pointing at a template file. Examples and README may refer to templates because they are not installed.
5. **No status vocabulary was invented.** The contract instruction defines seven section names and no status codes. Examples and the template start the report with a plain-language "Outcome" sentence instead. A status code would also have to be added to `tests/report-contract.yml`, which this fill may not change.
6. **gh-aw syntax in examples is illustrative.** Commands come only from the Skills (`gh aw compile`, `validate`, `run`, `logs`, `audit`, `fix`) plus standard `gh` and `gh api` calls. Frontmatter field names (`on`, `permissions`, `engine`, `tools`, `safe-outputs`, `network`, `timeout-minutes`) come from general gh-aw knowledge. They were not re-verified, because this fill could not browse, and the first example says to check them against the installed extension.
7. **Example data is fictional.** `example-org/inventory-service`, handles, run IDs, commits and every token and timing figure are illustrative and labeled as such.
8. **`trigger-cases.yml` uses a new key.** Each case already used `prompt` for the user's words, so the prompt file goes under `workflow_prompt` to avoid changing the meaning of an existing key.
9. **The usage example works without the hook.** The `agent-usage-reporting` Skill allows reporting from the transcript directly, which is what the example and its prompt do.
10. **The README validate command was corrected.** It used a `--write-report` flag that the shared validator does not have, and it omitted the pack folder argument.
11. **No skill inventory was created.** The fill rules allow updating `docs/SKILL_INVENTORY.md` but not creating it, and it did not exist. The Skill-to-prompt mapping lives in `docs/PROMPT_INVENTORY.md` instead.

### Gaps found but not fixed

These sit in files this fill may not change.

- `agent-usage-reporting` and `tests/hook-contract.yml` describe `.apm/hooks/agent-report.ps1`, which is not in the pack. The shared validator also rejects any `.apm/hooks/` folder. The hook needs to move to `hooks/` as a helper script and the Skill text needs updating.
- `compatibility/compatibility-matrix.yml` lists a Claude hook path and omits Kiro. `DESCRIPTION.md` says adapters are generated for four clients and that the Claude target includes the hook.
- `AGENT-PACK-README.md` (the artifact catalog required by the master prompt, section 2) is absent.
- `VALIDATION_REPORT.md` was not regenerated, because the fill runs the validator with `--no-report`.
- Where each APM target places prompt files was not observed. A scratch install outside the validator was not permitted in this session.
