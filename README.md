# Agent Packs

Official, source-controlled agent packs for Code Workflow and Code Conductor. Each top-level folder is one pack built to the master prompt kept in Code Workflow at `docs/agent-pack-prompt.md`.

## Standard

A pack is an APM package. Its canonical source is `apm.yml` plus the `.apm/` folder: `agents/*.agent.md`, `skills/<name>/SKILL.md`, `instructions/*.instructions.md`, `prompts/*.prompt.md`. Everything a client reads is generated from that source, by APM or by the Code Workflow installer. Packs carry no hand-built vendor folders and no committed archives.

Install one pack into a project with APM:

```bash
apm install saulpatinojr/Proj-Agent_Packs/python-distinguished-engineer-pack
```

Code Workflow installs packs into the user profile so they work in every repository; see that project's docs.

## Packs

| Pack | Version | Standard | Notes |
|---|---|---|---|
| python-distinguished-engineer-pack | 2.1.0 | prompt v2 | Restructured 2026-10-18. APM validation and six-target install verified. |
| microsoft-certified-trainer-pack | 1.0.0 | prompt v1 | Not yet restructured. |
| codex-agentic-orchestrator-pack | 1.0.0 | prompt v1 | Codex-only seed for the Code Workflow orchestrator. Not yet restructured. |

## Working on packs

Edit in a normal git clone, not in a synced folder. Run `python tooling/validate_pack.py` inside a pack before committing, and `python tooling/build_pack.py` to produce archives under `dist/` when releasing. `dist/` is ignored by git.
