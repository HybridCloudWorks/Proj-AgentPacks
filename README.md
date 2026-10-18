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

Status is the shared validator's result. Fourteen packs converted from the earlier prompt never had worked examples, templates or prompts; they keep their agents and skills but do not meet the standard until those are authored.

| Pack | Version | Agents | Skills | Status | Notes |
|---|---|---|---|---|---|
| ansible-expert-engineer-pack | 1.1.0 | 1 | 10 | Incomplete: no examples, templates, prompts |  |
| apple-code-reviewer-pack | 1.1.0 | 1 | 6 | Incomplete: no examples, templates, prompts |  |
| aws-cloud-architect-pack | 1.1.0 | 1 | 17 | Incomplete: no examples, templates, prompts |  |
| aws-expert-designer-pack | 1.1.0 | 1 | 8 | Incomplete: no examples, templates, prompts |  |
| azure-cloud-architect-pack | 1.1.0 | 1 | 18 | Incomplete: no examples, templates, prompts | Leaked copy of the AWS agent removed. |
| azure-expert-designer-pack | 1.1.0 | 1 | 8 | Incomplete: no examples, templates, prompts |  |
| cloud-documentation-archivist-pack | 1.1.0 | 1 | 18 | Incomplete: no examples, prompts |  |
| cloud-prepress-reviewer-pack | 1.1.0 | 1 | 15 | Incomplete: no examples, templates, prompts | Leaked copy of the AWS agent removed. |
| codex-agentic-orchestrator-pack | 1.1.0 | 1 | 6 | Incomplete: no examples, templates, prompts | Codex-only seed; to be rebuilt as the multi-vendor orchestrator. |
| github-expert-engineer-pack | 1.1.0 | 1 | 18 | Incomplete: no examples, templates, prompts |  |
| hypervelocity-engineer-pack | 1.1.0 | 1 | 9 | Incomplete: no examples, templates, prompts |  |
| infrastructure-pr-reviewer-pack | 1.1.0 | 1 | 8 | Incomplete: no examples, templates, prompts |  |
| microsoft-certified-trainer-pack | 1.1.0 | 5 | 18 | PASS |  |
| python-distinguished-engineer-pack | 2.1.0 | 5 | 18 | PASS |  |
| terraform-expert-engineer-pack | 1.1.0 | 1 | 9 | Incomplete: no examples, templates, prompts |  |
| typescript-distinguished-engineer-pack | 1.1.0 | 4 | 20 | Incomplete: no examples | Primary set explicitly; review verdicts defined. |

Not yet packs: the Google Cloud, CloudFlare, FinOps, Notion, Cloud Cybersecurity and Docker folders in the source material are third-party skill collections. Notion is under review as a generated pack (pull request #1); CloudFlare is being generated.

## Automation (GitHub Actions)

This repository is public, so GitHub-hosted runners are free. Model usage is not: generation draws on a Claude subscription.

| Workflow | Runs when | What it does |
|---|---|---|
| `validate` | Every push and pull request; weekly; manually | Tooling tests, an install-collision report, and `validate_pack.py --install-check` for each pack. Push and pull request cover changed packs on Linux with the pinned APM (`tooling/apm-version.txt`). The weekly run covers every pack on Linux, Windows and macOS with the newest APM. |
| `release` | A tag `<pack-name>-v<version>` is pushed | Checks the tag matches `apm.yml`, validates, builds, and attaches the archives and `SHA256SUMS.txt` to a GitHub release. |
| `watch apm` | Weekly | Opens an issue when an APM release is newer than the pinned version. |
| `generate pack` | Manually, by the repository owner | Generates a pack from a public reference repository with Claude Code, runs the engine's checks, and opens a pull request. Needs the secret `CLAUDE_CODE_OAUTH_TOKEN` from `claude setup-token`. |

Generated packs always arrive as pull requests on a `pack/<name>` branch; merging one is the approval. Locally, `python tooling/generate_pack.py publish staging/<name>` does the same.

To release a pack: `git tag python-distinguished-engineer-v2.1.0 && git push origin python-distinguished-engineer-v2.1.0`.

## Working on packs

Edit in a normal git clone, not in a synced folder. Shared tooling lives in `tooling/` at the repository root; packs carry only their own helper scripts.

```bash
python tooling/validate_pack.py <pack> --install-check   # writes <pack>/VALIDATION_REPORT.md
python tooling/build_pack.py <pack>                      # writes <pack>/dist/ and the catalog
python tooling/restructure_pack.py <v1 folder or zip> <new folder> --prompt <master prompt>
```

`restructure_pack.py` converts a prompt-v1 pack to the current layout deterministically and then prints the content checks a person must resolve by hand. `dist/` is ignored by git.
