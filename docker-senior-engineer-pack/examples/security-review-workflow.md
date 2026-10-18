# Worked example: independent security review of a CI helper image

Synthetic scenario for the `review-container-change` prompt, the docker-change-review and container-security-hardening skills, and the container-security-reviewer specialist. Review only: no fixes, no comments posted.

## Handoff

The primary resolves the pull request's base and head and sends the reviewer: the new `tools/ci-helper/Dockerfile`, the Compose service that runs it, the workflow that builds and pushes it, the build context, the fact that the helper will run on shared CI hosts, the organisation's base image policy, and the prohibited actions (no edits, no commands, no network). No credentials or secret values are shared.

## Findings returned

| Severity | Location | Evidence | Impact | Recommended change | Blocking |
|---|---|---|---|---|---|
| Blocker | compose service `ci-helper`, volumes | Mounts `/var/run/docker.sock` | Any code in the helper controls the CI host's engine and every job on it | Remove the mount; if engine access is essential, use a restricted API proxy after an owner decision | yes |
| High | Dockerfile line 6 | `ARG NPM_TOKEN` used by `RUN npm ci` | The token value is recorded in image history and in maximum-mode provenance | Use `RUN --mount=type=secret,id=npm_token` | yes |
| High | workflow, build step | `cache-to: type=registry,...,mode=max` to a public repository | Every intermediate stage, including the one that received the token, is published | Private cache repository with the image's access controls, and no secret in any stage | yes |
| Medium | Dockerfile final stage | No `USER`; base image runs as root | Container processes run as root on shared hosts | Numeric non-root `USER` | no |
| Low | Dockerfile line 1 | `FROM node:22` without a minor version or digest | Rebuilds drift as the tag moves | Pin version and digest; let Renovate update | no |
| Question | workflow trigger | Push step runs on `pull_request` | Unclear whether forks can trigger a push | Confirm intent; push only on trusted events | no |

The reviewer also lists the negative checks that would prove the fixes: `docker history --no-trunc` shows no token; `docker run --rm --entrypoint id` prints a non-zero UID; the Compose file renders without the socket mount.

## Reconciliation

The primary confirms the trigger question against the workflow file (forks cannot reach secrets on `pull_request`, but same-repository branches can push), adds that to the Question's answer, and reports status CHANGES_REQUIRED with the three blocking findings. No secret value appears anywhere in the review.
