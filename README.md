# Agent Packs

Official, source-controlled agent packs for Code Workflow and Code Conductor. Each top-level folder is one pack built to the master prompt kept in Code Workflow at `docs/agent-pack-prompt.md`.

## Standard

A pack is an APM package. Its canonical source is `apm.yml` plus the `.apm/` folder: `agents/*.agent.md`, `skills/<name>/SKILL.md`, `instructions/*.instructions.md`, `prompts/*.prompt.md`. Everything a client reads is generated from that source, by APM or by the Code Workflow installer. Packs carry no hand-built vendor folders and no committed archives.

Install one pack into a project with APM:

```bash
apm install hybridcloudworks/Proj-AgentPacks/python-distinguished-engineer-pack#python-distinguished-engineer-v2.3.0
```

Code Workflow installs packs into the user profile so they work in every repository; see that project's docs.

## Packs

Status is the shared validator's result with an APM install check for every target, run on 2026-10-18. Every pack meets the standard.

| Pack | Version | Agents | Skills | Status | Notes |
|---|---|---|---|---|---|
| ansible-expert-engineer-pack | 1.2.0 | 1 | 10 | PASS | Examples, templates and prompts gap-filled. |
| apple-code-reviewer-pack | 1.2.0 | 1 | 6 | PASS | Examples, templates and prompts gap-filled. |
| aws-cloud-architect-pack | 1.4.0 | 1 | 17 | PASS | Examples, templates and prompts gap-filled. Ships the shared draw.io skills (AWS, Azure and Google Cloud diagrams). |
| aws-expert-designer-pack | 1.4.0 | 1 | 8 | PASS | Examples, templates and prompts gap-filled. Ships the shared draw.io skills (AWS, Azure and Google Cloud diagrams). |
| azure-cloud-architect-pack | 1.4.0 | 1 | 18 | PASS | Leaked copy of the AWS agent removed. Examples, templates and prompts gap-filled. Ships the shared draw.io skills (AWS, Azure and Google Cloud diagrams). |
| azure-expert-designer-pack | 1.4.0 | 1 | 8 | PASS | Examples, templates and prompts gap-filled. Ships the shared draw.io skills (AWS, Azure and Google Cloud diagrams). |
| cloud-documentation-archivist-pack | 1.2.0 | 1 | 18 | PASS | Examples, templates and prompts gap-filled. |
| cloud-prepress-reviewer-pack | 1.2.0 | 1 | 15 | PASS | Leaked copy of the AWS agent removed. Examples, templates and prompts gap-filled. |
| cloudflare-subject-matter-expert-pack | 1.0.0 | 3 | 11 | PASS | Generated from the CloudFlare skill collection. |
| docker-senior-engineer-pack | 1.0.0 | 3 | 6 | PASS | Generated from the Docker skill collection. |
| finops-professional-practitioner-pack | 1.0.0 | 3 | 8 | PASS | Generated from the FinOps skill collection. |
| github-expert-engineer-pack | 1.2.0 | 1 | 18 | PASS | Examples, templates and prompts gap-filled. |
| google-cloud-architect-pack | 1.2.0 | 3 | 20 | PASS | Generated from the Google Cloud skill collection. Ships the shared draw.io skills (AWS, Azure and Google Cloud diagrams). |
| hypervelocity-engineer-pack | 1.2.0 | 1 | 9 | PASS | Examples, templates and prompts gap-filled. |
| infrastructure-pr-reviewer-pack | 1.2.0 | 1 | 8 | PASS | Examples, templates and prompts gap-filled. |
| microsoft-certified-trainer-pack | 1.1.0 | 5 | 18 | PASS | |
| notion-subject-matter-expert-pack | 1.0.0 | 2 | 7 | PASS | Generated from the Notion skill collection. |
| python-distinguished-engineer-pack | 2.3.0 | 5 | 18 | PASS | Shares its agent-evaluation agent, four skills, agentic-security instruction and two prompts with the TypeScript pack. |
| terraform-expert-engineer-pack | 1.2.0 | 1 | 9 | PASS | Examples, templates and prompts gap-filled. |
| typescript-distinguished-engineer-pack | 1.4.0 | 4 | 20 | PASS | Primary set explicitly; review verdicts defined. Examples, templates and prompts gap-filled. Shares its agent-evaluation agent, four skills, agentic-security instruction and two prompts with the Python pack. |

Orchestrators are not packs: each client's main coordinating agent is generated per desktop from the tools found there and the agents and skills selected, so it lives in `orchestrators/` until the orchestrator standard is defined. The Codex orchestrator seed, formerly `codex-agentic-orchestrator-pack`, is kept there unchanged as reference.

Five packs were generated from third-party skill collections: Notion, CloudFlare, Docker, Google Cloud and FinOps. The Cloud Cybersecurity collection is skipped for now.

## Automation (GitHub Actions)

This repository is public, so GitHub-hosted runners are free. Model usage is not: generation draws on a Claude subscription.

| Workflow | Runs when | What it does |
|---|---|---|
| `validate` | Every push and pull request; weekly; manually | Tooling tests, a check that shared primitives are identical in every pack, an install-collision report, and `validate_pack.py --install-check` for each pack. Push and pull request cover changed packs on Linux with the pinned APM (`tooling/apm-version.txt`). The weekly run covers every pack on Linux, Windows and macOS with the newest APM. |
| `release` | A tag `<pack-name>-v<version>` is pushed | Checks the tag matches `apm.yml`, validates, builds, and attaches the archives and `SHA256SUMS.txt` to a GitHub release. |
| `watch apm` | Weekly | Opens an issue when an APM release is newer than the pinned version. |
| `watch diagram sources` | Weekly; on changes to its inputs | Rebuilds the shared diagram skills' icon catalog from the newest draw.io release and confirms each provider's current icon release on its official page (`shared-primitives/diagram-facts.json`). Opens one issue when either changed. |
| `generate pack` | Manually, by the repository owner | Generates a pack from a public reference repository with Claude Code, runs the engine's checks, and opens a pull request. Needs the secret `CLAUDE_CODE_OAUTH_TOKEN` from `claude setup-token`. |

Generated packs always arrive as pull requests on a `pack/<name>` branch; merging one is the approval. Locally, `python tooling/generate_pack.py publish staging/<name>` does the same.

To release a pack: `git tag python-distinguished-engineer-v2.3.0 && git push origin python-distinguished-engineer-v2.3.0`.

## Working on packs

Edit in a normal git clone, not in a synced folder. Shared tooling lives in `tooling/` at the repository root; packs carry only their own helper scripts.

Shared primitives (skills, agents, instructions and prompts) ship with identical content in several packs, so installing any of those packs leaves the same file in place. Their one canonical copy lives in `shared-primitives/`, laid out like a pack's `.apm/` folder, with `consumers.json` naming the packs that ship each one: the draw.io skills for the AWS, Azure and Google Cloud packs, and the agent, skills, instruction and prompts that the Python and TypeScript packs share. Edit a primitive there and run `python tooling/sync_shared.py`; the `validate` workflow fails when a pack's copy drifts. `python tooling/check_collisions.py` reports agent, skill, instruction and prompt names that two packs ship with different content.

```bash
python tooling/validate_pack.py <pack> --install-check   # writes <pack>/VALIDATION_REPORT.md
python tooling/build_pack.py <pack>                      # writes <pack>/dist/ and the catalog
python tooling/restructure_pack.py <v1 folder or zip> <new folder> --prompt <master prompt>
```

`restructure_pack.py` converts a prompt-v1 pack to the current layout deterministically and then prints the content checks a person must resolve by hand. `dist/` is ignored by git.

## Where to install from

The catalog is installed from **`hybridcloudworks/Proj-AgentPacks`**, a mirror of this repository's `main` and release tags that the `publish` workflow pushes on every merge and tag. This repository is where packs are written and reviewed; that one is the address in every install line:

```bash
apm install hybridcloudworks/Proj-AgentPacks                                  # the whole catalog, each pack at its release tag (root apm.yml)
apm install -g hybridcloudworks/Proj-AgentPacks                               # the same, into the user profile for every client
apm install hybridcloudworks/Proj-AgentPacks/<pack>#<pack-name>-vX.Y.Z        # one pack
```

`apm.yml` at the root lists every pack at its current release tag; `python tooling/root_manifest.py` regenerates it and CI checks it is current.

### Publishing authentication (one-time, repository owner)

The `publish` workflow authenticates as a **GitHub App**, never a personal token: each run mints a one-hour installation token scoped to `hybridcloudworks/Proj-AgentPacks` alone ([`actions/create-github-app-token`](https://github.com/actions/create-github-app-token), pinned by commit).

1. Under the owner's account: **Settings → Developer settings → GitHub Apps → New GitHub App**. Name `AgentPacks Publisher`; homepage this repository's URL; **Webhook: Active off**; *Repository permissions → Contents: Read and write*, nothing else; *Where can this app be installed: Any account* (the app is owned by the person but installed on the organization). Create it and note the **App ID** (a number).
2. On the app's page: **Generate a private key** (a `.pem` download). Then **Install App → HybridCloudWorks → Only select repositories → AgentPacks**; do not install it on the personal account.
3. In `saulpatinojr/Proj-Agent_Packs` → Settings → Secrets and variables → Actions: **variable** `AGENTPACKS_PUBLISH_APP_ID` = the App ID (a number); **secret** (not a variable) `AGENTPACKS_PUBLISH_APP_PRIVATE_KEY` = the full contents of the `.pem` file. From PowerShell, with the key in Downloads: `gh variable set AGENTPACKS_PUBLISH_APP_ID -R saulpatinojr/Proj-Agent_Packs -b <id>` and `gh secret set AGENTPACKS_PUBLISH_APP_PRIVATE_KEY -R saulpatinojr/Proj-Agent_Packs -b (Get-Content -Raw <path to the .pem>)`, then check `gh secret list` before deleting the local `.pem`.
4. Actions → `publish` → **Run workflow** once; it mirrors `main` and every tag. From then on it runs on each merge to `main` and each release tag.

The app has no access to this repository or to anything else in the organization, and the private key never leaves the repository secret.
