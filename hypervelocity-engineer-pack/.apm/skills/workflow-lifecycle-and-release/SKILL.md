---
name: workflow-lifecycle-and-release
description: Create, compile, validate, run, upgrade, review, and release GitHub Agentic Workflows with source and generated artifacts kept aligned.
---

# Workflow Lifecycle and Release

Use this skill when a task creates, changes, debugs, upgrades, validates, runs, or releases a GitHub Agentic Workflow.

## Source and generated artifacts

- Treat the Markdown workflow and its YAML frontmatter as the human-maintained source.
- Treat the generated `.lock.yml` as a reviewed build artifact, not an independent source of intent.
- Run `gh aw compile` after source changes and review the generated diff.
- Use `gh aw validate` and, when available in the installed extension, strict or no-emit validation for preflight checks.
- Keep source and lock files in the same change when repository policy tracks both; otherwise document the generation contract.

## Safe lifecycle

1. Identify the workflow name, trigger, repository, data path, expected outputs, permissions, and whether a live run is authorized.
2. Inspect frontmatter, engines, tools, network access, MCP servers, safe outputs, secrets, runner choice, and permissions.
3. Compile and validate before asking for a live run.
4. Use `gh aw run` only for an authorized Agentic Workflow run. Do not confuse it with ordinary `gh workflow run`.
5. Review run logs and output artifacts with `gh aw logs`, then record evidence and missing proof.
6. For upgrades, inspect available fixes, apply changes only with authorization, recompile, validate, and review the lock diff.

## Release gate

Do not call a workflow production-ready merely because it compiles. Require source review, generated-artifact review, least-privilege permissions, safe-output review, secret and network review, representative validation, rollback or disable instructions, and an explicit owner for live execution.

Pin actions and external references where repository policy requires it. Preserve the single-file workflow model unless the repository has a documented reason to split responsibilities. Never imply that a local compile or static check proves live GitHub behavior.
