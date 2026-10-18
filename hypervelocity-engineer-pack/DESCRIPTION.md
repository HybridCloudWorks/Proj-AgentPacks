# Hypervelocity Engineer Agent

## Purpose

The Hypervelocity Engineer helps software engineers use AI agents, copilots, automation, structured prompts, and agentic workflows to increase delivery throughput without losing correctness, reviewability, security, or human control.

Its primary domain is GitHub Agentic Workflows (`gh-aw`): Markdown-defined workflows compiled into GitHub Actions that run an AI engine in response to repository events or schedules. It also covers the surrounding operating model: deciding when to use an agent, composing specialists, reducing context and token waste, enforcing safe outputs, observing runs, and learning from review and usage evidence.

## Agent design

The canonical Agent contains only mission, scope, inputs, capability requirements, Skill routing, guardrails, evidence rules, and output expectations. It does not repeat workflow syntax, token-optimization procedures, review-response checklists, or hook implementation details.

## Skill architecture

```text
hypervelocity-engineer
        |
        +-- agentic-workflows
        +-- optimize-agentic-workflow
        +-- prompt-token-efficiency
        +-- copilot-review-feedback
        +-- agent-usage-reporting
        +-- workflow-lifecycle-and-release
        +-- agent-governance-and-guardrails
        +-- agent-delegation-and-composition
        +-- workflow-observability-and-evaluation
```

## Capability coverage

- Route gh-aw design, create, update, debug, and upgrade requests to the correct specialized procedure.
- Design minimal-context, token-efficient prompts and workflows.
- Decide when an agent, subagent, deterministic script, MCP tool, or ordinary automation is the right mechanism.
- Enforce least privilege, safe-output boundaries, network and secret controls, and human approval gates.
- Handle Copilot and trusted-team PR feedback completely and reply with evidence.
- Compile, validate, run, audit, and upgrade agentic workflows deliberately.
- Observe runs through summaries, reports, logs, traces, and cost/quality metrics.
- Use the optional Claude Stop hook to report actual observed Agent, Skill, and tool calls without blocking work.

## Safety and evidence

Treat workflows as code. Review source and compiled output, keep permissions minimal, and avoid direct free-form writes when structured safe outputs can provide the boundary. Separate observed facts from inference, local structure from live behavior, and equivalent output quality from lower token cost. Never claim an agent is safe merely because its prompt says it is safe.

## Portability

Skills use the shared `SKILL.md` format. Native Agent adapters are generated for GitHub Copilot, Claude Code, OpenAI Codex, and Gemini CLI. The Claude target includes the optional PowerShell usage-report hook; other targets retain the canonical guidance and document that hook as Claude-specific.
