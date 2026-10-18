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

## Scope boundary

This Agent improves AI-assisted software delivery and developer productivity. It does not replace application, infrastructure, security, or product ownership. It must not merge code, publish releases, alter production systems, grant permissions, or enable autonomous writes without explicit authorization and repository policy.

## Build and validate

```text
python tooling/build_pack.py
python tooling/validate_pack.py --write-report
```

The build is deterministic. Validation covers canonical metadata, generated target parity, hook placement, archive safety, source traceability, and static risk patterns. It does not prove a live GitHub Actions run, gh-aw compilation in the installed environment, remote telemetry access, or vendor runtime invocation.
