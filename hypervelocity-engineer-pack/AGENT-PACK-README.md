# hypervelocity-engineer 1.2.0: artifact catalog

Every file in this pack, with its purpose and location. Contents are in the files themselves.

| ARTIFACT NAME | PURPOSE | LOCATION |
|---|---|---|
| hypervelocity-engineer.agent.md | Canonical agent: AI-accelerated engineering specialist for designing, creating, debugging, optimizing, governing, reviewing, and observing GitHub Agentic Workflows and related agent-assisted software delivery. Use when an agent, copilot, gh-aw workflow, prompt, MCP tool, safe output, review loop, or agent productivity problem is in scope. | .apm/agents/hypervelocity-engineer.agent.md |
| hypervelocity-engineer-contract.instructions.md | Canonical instruction: Approval, handoff and completion-report rules for the hypervelocity engineer pack. Always on; the agents, skills and prompts in this pack refer to it. | .apm/instructions/hypervelocity-engineer-contract.instructions.md |
| author-gh-aw-workflow.prompt.md | Canonical prompt: Create or update a GitHub Agentic Workflow with least privilege, safe outputs, and a compiled lock file reviewed before any live run | .apm/prompts/author-gh-aw-workflow.prompt.md |
| compress-agent-prompt.prompt.md | Canonical prompt: Rewrite a prompt, agent profile or workflow instruction for fewer tokens and less ambiguity without dropping constraints | .apm/prompts/compress-agent-prompt.prompt.md |
| design-agent-mechanism.prompt.md | Canonical prompt: Choose the right mechanism for an automation request and design a bounded agentic workflow before any code is written | .apm/prompts/design-agent-mechanism.prompt.md |
| diagnose-gh-aw-run.prompt.md | Canonical prompt: Debug or audit a failed or misbehaving GitHub Agentic Workflow run from its logs, audit data and compiled workflow | .apm/prompts/diagnose-gh-aw-run.prompt.md |
| evaluate-workflow-reliability.prompt.md | Canonical prompt: Evaluate whether an agentic workflow, or a change to it, is correct, safe, reliable and affordable enough to operate | .apm/prompts/evaluate-workflow-reliability.prompt.md |
| optimize-workflow-cost.prompt.md | Canonical prompt: Measure and reduce token use, AI credits, tool denials or timeouts in a GitHub Agentic Workflow while keeping output quality equivalent | .apm/prompts/optimize-workflow-cost.prompt.md |
| report-agent-usage.prompt.md | Canonical prompt: Report observed agent, skill and tool activity for a session or run without estimating what the source does not expose | .apm/prompts/report-agent-usage.prompt.md |
| resolve-review-feedback.prompt.md | Canonical prompt: Collect, triage, address, reply to and resolve trusted pull request review feedback, including Copilot reviews, before calling the work complete | .apm/prompts/resolve-review-feedback.prompt.md |
| review-agent-guardrails.prompt.md | Canonical prompt: Review an agent, GitHub Agentic Workflow, MCP configuration or automation for least privilege, safe outputs, secrets, network and approval gates | .apm/prompts/review-agent-guardrails.prompt.md |
| upgrade-gh-aw-workflow.prompt.md | Canonical prompt: Upgrade GitHub Agentic Workflows or fix deprecations, recompile, and confirm the lock diff does not widen permissions | .apm/prompts/upgrade-gh-aw-workflow.prompt.md |
| SKILL.md | Canonical skill: Select and compose agents, subagents, deterministic scripts, MCP tools, and human review so each task has a bounded owner and reliable handoff. | .apm/skills/agent-delegation-and-composition/SKILL.md |
| SKILL.md | Canonical skill: Design least-privilege permissions, safe outputs, network and MCP boundaries, secrets handling, approvals, and failure containment for agent-assisted engineering. | .apm/skills/agent-governance-and-guardrails/SKILL.md |
| SKILL.md | Canonical skill: Measure observed agent, skill, and tool activity with an optional non-blocking report hook when a repository needs lightweight usage visibility. | .apm/skills/agent-usage-reporting/SKILL.md |
| OFFICIAL_SOURCES.md | Canonical skill | .apm/skills/agentic-workflows/OFFICIAL_SOURCES.md |
| SKILL.md | Canonical skill: Route GitHub Agentic Workflows design, creation, update, debugging, audit, and upgrade requests to the correct gh-aw procedure and current official reference. Use when a Markdown workflow, gh aw command, GitHub Actions agent, or gh-aw skill is in scope. | .apm/skills/agentic-workflows/SKILL.md |
| SKILL.md | Canonical skill: Collect, filter, resolve, reply to, and close GitHub pull request review feedback from Copilot, GitHub Actions, repository collaborators, and trusted team members before declaring the work complete. | .apm/skills/copilot-review-feedback/SKILL.md |
| SKILL.md | Canonical skill: Measure and reduce token use, AI credits, tool denials, timeouts, context waste, and run frequency in GitHub Agentic Workflows while preserving safe-output behavior and equivalent result quality. | .apm/skills/optimize-agentic-workflow/SKILL.md |
| SKILL.md | Canonical skill: Rewrite prompts and agent instructions for minimal tokens, maximal clarity, low ambiguity, stable terminology, and testable output without removing safety or task-critical context. | .apm/skills/prompt-token-efficiency/SKILL.md |
| SKILL.md | Canonical skill: Create, compile, validate, run, upgrade, review, and release GitHub Agentic Workflows with source and generated artifacts kept aligned. | .apm/skills/workflow-lifecycle-and-release/SKILL.md |
| SKILL.md | Canonical skill: Observe agentic workflow runs and evaluate quality, safety, cost, latency, and reliability with reproducible evidence. | .apm/skills/workflow-observability-and-evaluation/SKILL.md |
| apm.yml | APM manifest: name, version, targets. | apm.yml |
| capability-map.yml | Vendor compatibility metadata | compatibility/capability-map.yml |
| compatibility-matrix.yml | Vendor compatibility metadata | compatibility/compatibility-matrix.yml |
| tool-permissions.yml | Vendor compatibility metadata | compatibility/tool-permissions.yml |
| vendor-sources.yml | Vendor compatibility metadata | compatibility/vendor-sources.yml |
| DESCRIPTION.md | What the pack is for and who uses it. | DESCRIPTION.md |
| DESIGN_DECISIONS.md | Pack contract or inventory | docs/DESIGN_DECISIONS.md |
| OFFICIAL_SOURCES.md | Pack contract or inventory | docs/OFFICIAL_SOURCES.md |
| PROMPT_INVENTORY.md | Pack contract or inventory | docs/PROMPT_INVENTORY.md |
| SOURCE_TRACEABILITY.md | Pack contract or inventory | docs/SOURCE_TRACEABILITY.md |
| author-gh-aw-workflow.md | Worked example | examples/author-gh-aw-workflow.md |
| blocked-auto-merge-request.md | Worked example | examples/blocked-auto-merge-request.md |
| design-agent-mechanism.md | Worked example | examples/design-agent-mechanism.md |
| diagnose-gh-aw-run.md | Worked example | examples/diagnose-gh-aw-run.md |
| optimize-workflow-cost.md | Worked example | examples/optimize-workflow-cost.md |
| report-agent-usage.md | Worked example | examples/report-agent-usage.md |
| resolve-review-feedback.md | Worked example | examples/resolve-review-feedback.md |
| README.md | Hook helper script | hooks/README.md |
| LICENSE | License terms. | LICENSE |
| PORTABLE_AGENT_SKILL_PACK_AUTHORING_PROMPT.md | The master prompt this pack was built to. | PORTABLE_AGENT_SKILL_PACK_AUTHORING_PROMPT.md |
| README.md | How to install and use the pack. | README.md |
| completion-report.md | Reusable template | templates/completion-report.md |
| delegation-handoff.md | Reusable template | templates/delegation-handoff.md |
| guardrail-decision-record.md | Reusable template | templates/guardrail-decision-record.md |
| optimization-plan.md | Reusable template | templates/optimization-plan.md |
| review-feedback-ledger.md | Reusable template | templates/review-feedback-ledger.md |
| workflow-release-gate.md | Reusable template | templates/workflow-release-gate.md |
| capability-coverage.yml | Local test or recorded evidence | tests/capability-coverage.yml |
| hook-contract.yml | Local test or recorded evidence | tests/hook-contract.yml |
| report-contract.yml | Local test or recorded evidence | tests/report-contract.yml |
| skill-coverage.yml | Local test or recorded evidence | tests/skill-coverage.yml |
| trigger-cases.yml | Local test or recorded evidence | tests/trigger-cases.yml |
| VALIDATION_REPORT.md | Executed checks and what remains unverified. | VALIDATION_REPORT.md |

## Build outputs (dist/, not committed)

- copilot-hypervelocity-engineer.zip: 22 files generated by `apm install --target copilot`
- claude-hypervelocity-engineer.zip: 22 files generated by `apm install --target claude`
- codex-hypervelocity-engineer.zip: 11 files generated by `apm install --target codex`
- kiro-hypervelocity-engineer.zip: 12 files generated by `apm install --target kiro`
- gemini-hypervelocity-engineer.zip: 20 files generated by `apm install --target gemini`
- agent-skills-hypervelocity-engineer.zip: 10 files generated by `apm install --target agent-skills`
- hypervelocity-engineer-canonical.zip, hypervelocity-engineer-prompt.zip, hypervelocity-engineer-validation.zip, hypervelocity-engineer-skills.zip, hypervelocity-engineer-full-pack.zip, SHA256SUMS.txt
