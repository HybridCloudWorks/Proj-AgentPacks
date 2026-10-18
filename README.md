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

All packs are at agent-pack-prompt v2.3 and pass the shared validator, including an APM install into a scratch project for copilot, claude, codex, kiro, gemini and agent-skills (2026-10-18). Canonical agents declare no `tools`; intents live in each pack's `compatibility/tool-permissions.yml`.

| Pack | Version | Agents | Skills | Notes |
|---|---|---|---|---|
| ansible-expert-engineer-pack | 1.1.0 | 1 | 10 |  |
| apple-code-reviewer-pack | 1.1.0 | 1 | 6 |  |
| aws-cloud-architect-pack | 1.1.0 | 1 | 17 |  |
| aws-expert-designer-pack | 1.1.0 | 1 | 8 |  |
| azure-cloud-architect-pack | 1.1.0 | 1 | 18 | A leaked copy of the AWS agent was removed during conversion. |
| azure-expert-designer-pack | 1.1.0 | 1 | 8 |  |
| cloud-documentation-archivist-pack | 1.1.0 | 1 | 18 |  |
| cloud-prepress-reviewer-pack | 1.1.0 | 1 | 15 | A leaked copy of the AWS agent was removed during conversion. |
| codex-agentic-orchestrator-pack | 1.1.0 | 1 | 6 | Codex-only seed; to be rebuilt as the multi-vendor Code Workflow orchestrator. |
| github-expert-engineer-pack | 1.1.0 | 1 | 18 |  |
| hypervelocity-engineer-pack | 1.1.0 | 1 | 9 |  |
| infrastructure-pr-reviewer-pack | 1.1.0 | 1 | 8 |  |
| microsoft-certified-trainer-pack | 1.1.0 | 5 | 18 |  |
| python-distinguished-engineer-pack | 2.1.0 | 5 | 18 |  |
| terraform-expert-engineer-pack | 1.1.0 | 1 | 9 |  |
| typescript-distinguished-engineer-pack | 1.1.0 | 4 | 20 | Primary set explicitly; three specialists hidden from the picker. |

Not yet packs: the Google Cloud, CloudFlare, FinOps, Notion, Cloud Cybersecurity and Docker folders in the source material are third-party skill collections without an agent or manifest. They need a role pack generated with the master prompt, with the collection as reference material.

## Working on packs

Edit in a normal git clone, not in a synced folder. Shared tooling lives in `tooling/` at the repository root; packs carry only their own helper scripts.

```bash
python tooling/validate_pack.py <pack> --install-check   # writes <pack>/VALIDATION_REPORT.md
python tooling/build_pack.py <pack>                      # writes <pack>/dist/ and the catalog
python tooling/restructure_pack.py <v1 folder or zip> <new folder> --prompt <master prompt>
```

`restructure_pack.py` converts a prompt-v1 pack to the current layout deterministically and then prints the content checks a person must resolve by hand. `dist/` is ignored by git.
