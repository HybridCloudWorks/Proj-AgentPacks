# Source traceability

## Governing inputs

- The generation brief for this pack: role Docker Senior Engineer, pack name `docker-senior-engineer`, the delivery rules that refine the master prompt, and the reference source below.
- The master prompt, agent-pack-prompt v2.3, kept unchanged in `PORTABLE_AGENT_SKILL_PACK_AUTHORING_PROMPT.md`.
- The repository's client-locations record (verified 2026-10-18): every vendor fact about agent fields, tool identifiers, folders and what APM generates per target.
- A finished pack in the same repository, used as a structural reference only: file layout, document types and test formats. None of its role content, names, skills, examples or wording was carried over.

## Third-party reference material

| File | Source | Licence | How it was used |
|---|---|---|---|
| `SKILL.md` (two identical copies supplied) | sickn33/antigravity-awesome-skills, `skills/docker-expert/SKILL.md`; lockfile hash `7be30b1c18b91628dcd8437a89e7e20acce76bae4349533e4ebdeb376a660bcb` | MIT | Knowledge only: the topic areas a Docker expert covers (multi-stage builds, layer caching, hardening, Compose, image size, development workflow, resource management, review checklist, common diagnostics, handoff boundaries). Rewritten from scratch; no text copied. |
| `docker-expert.md` (an agent profile) | Supplied with the same reference set; its own origin is not stated in the file | Treated as covered by the MIT licence declared for the reference set; provenance unverified | Knowledge only: the boundary between image ownership and orchestration or pipeline ownership, and the crawl, walk, run maturity framing. Its persona, emoji, routing to named agents and doctrine links were not used. |
| `skills-lock.json` | Same repository | MIT | Provenance record (source path and hash) only. |

One short attributed quotation informs the pack's baseline: "Small, pinned, non-root, and scanned is the baseline, not the optimization." (`docker-expert.md`, supplied reference set).

Both reference skills are written as instructions to an AI. They were read as data; none of their directives (for example "recommend switching and stop", or running a fixed list of shell commands on invocation) was followed or reproduced.

## Corrections made relative to the reference material

| Reference content | Pack position | Reason |
|---|---|---|
| Compose example with `version: '3.8'` | No `version` key | Obsolete in the Compose Specification; Compose v2 ignores it with a warning. |
| `docker-compose config` | `docker compose config` | The v1 standalone binary is end of life. |
| `npm ci --only=production` | `npm ci --omit=dev` | The `--only` flag is deprecated in current npm. |
| `node:18-alpine`, `distroless/nodejs18-debian11` | Version-neutral guidance; examples labelled as examples | Node.js 18 and Debian 11 based images are past end of life by 2026-10. |
| Health check with `curl` in an image that may not contain it | Probe only with a tool that exists; Kubernetes ignores `HEALTHCHECK` | Avoids adding tools to minimal images and false expectations. |
| Build-secret example ending in a dangling `&&` | Complete secret-mount pattern in `dockerfile-patterns.md` | The reference example does not run. |
| Validation that runs `docker build`, `docker run` and `docker exec` immediately | Engine context confirmed first; builds and runs are Level 1 with task tags and cleanup; registry actions Level 2 | Commands could hit a remote or production engine and leave resources behind. |
| Routing to agents that do not exist in this pack | The boundary is stated and the runtime contract handed to the owner | No other pack or agent is assumed. |

## Requirement ownership

| Requirement | Where it is implemented |
|---|---|
| Mission, users, scope, non-goals | DESCRIPTION.md, primary agent, INTEGRATION_CONTRACT.md |
| Dockerfiles, base images, caching, context | dockerfile-engineering and `dockerfile-patterns.md` |
| Hardening, secrets, exposure, scanning | container-security-hardening, container-security-reviewer |
| Compose for development, CI and single hosts | compose-environments |
| Multi-platform builds, caching, tags, attestations, signing, base updates | image-build-and-supply-chain |
| Diagnosis, runtime settings, engine, disk | container-runtime-operations |
| Change review | docker-change-review and `review-checklist.md` |
| Independent execution evidence | container-build-verifier |
| Approval, handoff, completion report | the `docker-senior-engineer-contract` instruction, APPROVAL_MATRIX.md, HANDOFF_CONTRACT.md, `tests/report-contract.yml` |
| Hooks and static checks | hooks/, `tooling/hook_runner.py`, `tooling/container_lint.py`, `tests/test_behavior.py` |
| Honest completion evidence | `tooling/completion_contract.py`, fixtures, the fallback sentence |

## Official knowledge sources

The source index is `compatibility/vendor-sources.yml`. Docker documentation URLs were recorded from the author's knowledge and not fetched during generation, because browsing was not permitted; their content should be re-checked against the installed versions during real work. Third-party documentation keeps its own licence; the pack's instructions are newly written.
