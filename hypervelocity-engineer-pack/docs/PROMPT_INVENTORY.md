# Prompt inventory

One prompt per primary workflow, all under `.apm/prompts/` and all bound to the `hypervelocity-engineer` agent. Each prompt names its inputs, the Skills it applies, its expected output, and the `hypervelocity-engineer-contract` instruction for the completion report.

| Prompt | Skills applied | Expected output | Worked example |
|---|---|---|---|
| design-agent-mechanism.prompt.md | agent-delegation-and-composition, agentic-workflows, agent-governance-and-guardrails, workflow-observability-and-evaluation | Mechanism table with rejected alternatives, delegate contracts, guardrail decision record, approval gates, evaluation criteria. Design only. | examples/design-agent-mechanism.md |
| author-gh-aw-workflow.prompt.md | agentic-workflows, agent-governance-and-guardrails, workflow-lifecycle-and-release | Source diff, lock-diff summary, permission, safe-output, network, MCP and secret table, compile and validate results, live-run status, release-gate gaps. | examples/author-gh-aw-workflow.md |
| diagnose-gh-aw-run.prompt.md | agentic-workflows, workflow-observability-and-evaluation, workflow-lifecycle-and-release, agent-governance-and-guardrails, optimize-agentic-workflow | Timeline, confirmed root cause with ruled-out hypotheses, evidence table, proposed or applied fix, what stays unverified. | examples/diagnose-gh-aw-run.md |
| upgrade-gh-aw-workflow.prompt.md | agentic-workflows, workflow-lifecycle-and-release, agent-governance-and-guardrails | Fixes proposed and applied per workflow, extension versions, permission and capability delta, validation, rollback. | none |
| optimize-workflow-cost.prompt.md | optimize-agentic-workflow, prompt-token-efficiency, workflow-observability-and-evaluation, workflow-lifecycle-and-release | Baseline, cost-driver table, approved plan, before and after comparison labeled observed or projected, quality-equivalence evidence. | examples/optimize-workflow-cost.md |
| compress-agent-prompt.prompt.md | prompt-token-efficiency, workflow-lifecycle-and-release, optimize-agentic-workflow | Compressed prompt, preserved constraints, removed duplication, remaining ambiguity, length labeled measured or estimated. | none (step 3 of the optimize example) |
| resolve-review-feedback.prompt.md | copilot-review-feedback, workflow-lifecycle-and-release | Feedback ledger, changes, validation, replies, unresolved and out-of-scope items. | examples/resolve-review-feedback.md |
| review-agent-guardrails.prompt.md | agent-governance-and-guardrails, workflow-lifecycle-and-release, agent-delegation-and-composition | Located findings by severity, decision record, release-gate status, approvals and owners, least-privilege proposal. | examples/blocked-auto-merge-request.md |
| evaluate-workflow-reliability.prompt.md | workflow-observability-and-evaluation, agent-governance-and-guardrails | Case table with results, labeled metrics, uncertainty, and an operate, fix or revert recommendation for the owner. | none (sections 4 and 5 of the optimize example) |
| report-agent-usage.prompt.md | agent-usage-reporting | Source, window and counting rules, count table, metrics the source does not expose. | examples/report-agent-usage.md |

## Skill to prompt

Every Skill is reached by at least one prompt.

| Skill | Primary prompt | Also applied by |
|---|---|---|
| agentic-workflows | author-gh-aw-workflow.prompt.md | design-agent-mechanism, diagnose-gh-aw-run, upgrade-gh-aw-workflow |
| optimize-agentic-workflow | optimize-workflow-cost.prompt.md | diagnose-gh-aw-run, compress-agent-prompt |
| prompt-token-efficiency | compress-agent-prompt.prompt.md | optimize-workflow-cost |
| copilot-review-feedback | resolve-review-feedback.prompt.md | none |
| agent-usage-reporting | report-agent-usage.prompt.md | none |
| workflow-lifecycle-and-release | author-gh-aw-workflow.prompt.md | diagnose-gh-aw-run, upgrade-gh-aw-workflow, optimize-workflow-cost, compress-agent-prompt, resolve-review-feedback, review-agent-guardrails |
| agent-governance-and-guardrails | review-agent-guardrails.prompt.md | design-agent-mechanism, author-gh-aw-workflow, diagnose-gh-aw-run, upgrade-gh-aw-workflow, evaluate-workflow-reliability |
| agent-delegation-and-composition | design-agent-mechanism.prompt.md | review-agent-guardrails |
| workflow-observability-and-evaluation | evaluate-workflow-reliability.prompt.md | design-agent-mechanism, diagnose-gh-aw-run, optimize-workflow-cost |

## Installation behaviour

Prompts carry only `description` and `agent` frontmatter. Per the APM facts verified on 2026-10-18 (APM 0.33.0), commands ship as prompts, prompt keys that Claude commands do not support (such as `agent`) are dropped with a warning, and a user-scope `apm install -g` delivers prompts to Copilot but not to Codex. Where each target places prompt files was not observed during the gap fill; the validator's `apm install` check confirms that installation succeeds, not where prompts land. Users of a client that receives no prompts invoke the `hypervelocity-engineer` agent directly with the same request.

Prompt names avoid the upstream gh-aw procedure names that the `agentic-workflows` router loads (create, update, debug and upgrade agentic workflow), so no installed prompt shares a file name with an upstream procedure.
