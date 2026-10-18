# Hypervelocity Engineer Pack

Portable Agent/Skill package for engineers operating in an AI-accelerated development model. It treats agents, prompts, workflows, tools, safe outputs, review loops, and telemetry as engineering assets that need scope, tests, cost awareness, and human governance.

The source material is specifically centered on GitHub Agentic Workflows (`gh aw` / `gh-aw`). The pack preserves that specialization while adding reusable guidance for agent selection, workflow lifecycle, guardrails, measurement, and developer productivity.

## Deliverables

- `DESCRIPTION.md` - architecture and capability summary.
- `hypervelocity-engineer-pack.zip` - complete source and generated vendor files.
- `hypervelocity-engineer-canonical.zip` - APM-friendly canonical source.
- `hypervelocity-engineer-prompt.zip` - reusable authoring prompt.
- `hypervelocity-engineer-skills.zip` - bundle containing one `skill.zip` per Skill.
- `hypervelocity-engineer-validation.zip` - generated `VALIDATION_REPORT.md`.
- `dist/` - four target packages and individual Skill archives.

## Skill set

1. `agentic-workflows`
2. `optimize-agentic-workflow`
3. `prompt-token-efficiency`
4. `copilot-review-feedback`
5. `agent-usage-reporting`
6. `workflow-lifecycle-and-release`
7. `agent-governance-and-guardrails`
8. `agent-delegation-and-composition`
9. `workflow-observability-and-evaluation`

The five additions close meaningful gaps in the supplied material: persistent usage reporting, compile/run/upgrade lifecycle safety, agent/tool governance, bounded delegation, and measurable quality/observability loops.

## Workflows (prompts)

Ten prompts under `.apm/prompts/`, one per primary workflow, each bound to the `hypervelocity-engineer` agent and to the `hypervelocity-engineer-contract` instruction. `docs/PROMPT_INVENTORY.md` maps each prompt to its Skills and expected output.

| Prompt | Workflow |
|---|---|
| `design-agent-mechanism.prompt.md` | Choose agent, subagent, script, MCP tool, CI or human per step; design before building |
| `author-gh-aw-workflow.prompt.md` | Create or update a gh-aw workflow with least privilege and safe outputs; compile and review the lock |
| `diagnose-gh-aw-run.prompt.md` | Debug or audit a run from `gh aw logs` and `gh aw audit` evidence |
| `upgrade-gh-aw-workflow.prompt.md` | Apply gh-aw upgrades or deprecation fixes without widening permissions |
| `optimize-workflow-cost.prompt.md` | Measure and cut tokens, AI credits, denials or timeouts with equivalent quality |
| `compress-agent-prompt.prompt.md` | Rewrite a prompt or agent profile for fewer tokens and less ambiguity |
| `resolve-review-feedback.prompt.md` | Ledger, address, reply to and resolve trusted pull request feedback |
| `review-agent-guardrails.prompt.md` | Review permissions, safe outputs, secrets, network and approval gates |
| `evaluate-workflow-reliability.prompt.md` | Decide with evidence whether a workflow or change is fit to operate |
| `report-agent-usage.prompt.md` | Report observed agent, skill and tool activity |

## Examples and templates

These are for people reading the pack. They are not installed, and installed content never refers to them.

- `examples/`: worked walkthroughs, each ending with a completion report in the contract's seven sections. `author-gh-aw-workflow.md`, `diagnose-gh-aw-run.md`, `optimize-workflow-cost.md`, `resolve-review-feedback.md`, `design-agent-mechanism.md`, `report-agent-usage.md`, and `blocked-auto-merge-request.md`, which shows a request the agent must stop at.
- `templates/`: the documents the Skills tell the agent to produce. `completion-report.md`, `delegation-handoff.md`, `guardrail-decision-record.md`, `review-feedback-ledger.md`, `optimization-plan.md`, `workflow-release-gate.md`.

## Scope boundary

This Agent improves AI-assisted software delivery and developer productivity. It does not replace application, infrastructure, security, or product ownership. It must not merge code, publish releases, alter production systems, grant permissions, or enable autonomous writes without explicit authorization and repository policy.

## Build and validate

```text
python tooling/build_pack.py
python tooling/skill_coverage.py <pack-folder> --check
python tooling/validate_pack.py <pack-folder> --install-check
```

Run these from the pack repository root; the tooling is shared there and is not copied into the pack. The validator writes `VALIDATION_REPORT.md` unless `--no-report` is passed.

The build is deterministic. Validation covers canonical metadata, generated target parity, hook placement, archive safety, source traceability, and static risk patterns. It does not prove a live GitHub Actions run, gh-aw compilation in the installed environment, remote telemetry access, or vendor runtime invocation.
