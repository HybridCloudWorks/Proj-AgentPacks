---
name: agentic-workflows
description: Route GitHub Agentic Workflows design, creation, update, debugging, audit, and upgrade requests to the correct gh-aw procedure and current official reference. Use when a Markdown workflow, gh aw command, GitHub Actions agent, or gh-aw skill is in scope.
---

# Agentic Workflows Router

First classify the request: design, create, configure, update, debug, optimize, audit, test, report, or upgrade. Load only the matching repository or upstream gh-aw Skill/prompt; do not load the entire gh-aw library.

## Routing

- Design or interview -> designer/patterns guidance.
- Create a new workflow -> create-agentic-workflow guidance.
- Update an existing workflow -> update-agentic-workflow guidance.
- Debug or audit a run -> debug-agentic-workflow, logs, audit, and error-pattern guidance.
- Upgrade or fix deprecations -> upgrade-agentic-workflows or `gh aw fix` guidance.
- Safe outputs or MCP -> the matching safe-outputs or MCP guidance.
- Token or cost problem -> `optimize-agentic-workflow`.
- Telemetry or traces -> `workflow-observability-and-evaluation` and the OTEL guidance.

If a repository overlay such as `.github/aw/instructions.md` exists, load it after the matched upstream procedure and treat the repository overlay as the local policy when it conflicts. If the needed upstream files are not available, state that limitation and use the official gh-aw documentation links in `OFFICIAL_SOURCES.md` rather than inventing syntax.

## Identity check

`gh aw` is the GitHub Agentic Workflows CLI extension. It is not the Copilot CLI. Use `gh aw compile`, `gh aw validate`, `gh aw run`, `gh aw logs`, and `gh aw audit` for gh-aw lifecycle tasks. Do not trigger an agentic workflow with an ordinary `gh workflow run` command when `gh aw run` is available and appropriate.

## Boundary

This Skill dispatches. It does not duplicate the workflow schema, safe-output reference, or full debugging procedure. Return the selected procedure, required inputs, constraints, and evidence needed before implementation.
