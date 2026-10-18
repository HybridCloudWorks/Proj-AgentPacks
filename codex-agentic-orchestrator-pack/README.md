# Codex Agentic Orchestrator Pack

This pack provides an OpenAI Codex-native orchestration layer for the user's domain Agent packs. It is designed to be dropped into a repository without requiring every domain agent to be installed.

## Primary downloads

- `dist/codex-agentic-orchestrator-pack.zip` - complete pack
- `dist/codex-agentic-orchestrator-canonical.zip` - canonical Agent and Skills
- `dist/codex-agentic-orchestrator-prompt.zip` - reusable authoring prompt
- `dist/codex-agentic-orchestrator-skills.zip` - individual Skill bundle
- `dist/codex-agentic-orchestrator-validation.zip` - uppercase validation report

The Codex target is `dist/openai-codex/openai-codex.zip`. Individual Skill archives are under `dist/skills/<skill-name>/skill.zip`.

## Install

Vendor files are generated from `.apm/` by `apm install` or the Code Workflow installer; nothing is copied by hand.

The target contains the orchestrator custom agent, Skills, registry, schemas, hook scripts, and workflow tooling. Domain agents are separate packs and may be installed in any combination.

## Operating contract

1. Discover the installed Codex custom agents.
2. Select one, a named subset, or all registry capabilities.
3. Create a workflow state directory before delegation.
4. Ask Codex to delegate required work through its native subagent mechanism.
5. Require each subagent to write a structured handoff and artifact list.
6. Validate dependencies, handoffs, evidence, and completion status.
7. Never silently replace a missing required agent with the parent agent.

Codex's own concurrency and permission settings remain authoritative. The pack provides deterministic outcomes, not an impossible promise of network, authentication, model, quota, or permission availability.

## Build and validate

```text
python tooling/build_pack.py
python tooling/validate_pack.py --write-report
python tooling/workflow.py discover
python tooling/workflow.py init --mode selected --agents terraform-expert-engineer,cloud-documentation-archivist --objective "Review the change"
python tooling/workflow.py init --mode all --objective "Review the complete installed agent set"
python tooling/workflow.py validate --workflow <workflow-id>
```

In `all` mode, installed registry agents are required and missing registry entries are recorded as optional skips. Add `--require-all` only when every registry role must be installed.
