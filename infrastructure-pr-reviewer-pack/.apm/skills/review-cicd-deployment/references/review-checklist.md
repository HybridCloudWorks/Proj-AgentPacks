# CI/CD Pipelines and Deployment Scripts Review Adapter

Apply this adapter to GitHub Actions, Azure Pipelines, GitLab CI, Jenkins, reusable workflows and templates, Bash, Python orchestration, Makefiles, task runners, and deployment wrappers.

## 1. Trigger and trust-boundary review

Verify:

- Which events start validation, preview, plan, deployment, cleanup, and rollback jobs.
- Pull requests from forks or untrusted contributors cannot access privileged secrets, self-hosted runners, service connections, or production environments.
- Branch, tag, path, schedule, manual input, and repository-dispatch filters are exact and fail closed.
- A change to a workflow on an untrusted branch cannot cause that same unreviewed workflow to run with privileged credentials.
- Automatic re-runs, retries, and manual dispatches preserve the intended commit and target.
- Production deployment is gated by protected environments, approvals, branch rules, and required checks.

Review platform-specific event semantics rather than inferring from the event name alone.

## 2. Identity, permissions, and credentials

Verify:

- Job- and workflow-level permissions follow least privilege.
- OIDC or workload identity claims restrict repository, branch or environment, workflow, audience, and target as appropriate.
- Service connections and cloud identities cannot deploy outside the intended scope.
- Long-lived credentials are avoided where short-lived federation is supported.
- Secrets are not available to jobs, steps, containers, or reusable workflows that do not need them.
- Credentials are not placed in command lines, artifacts, caches, outputs, environment dumps, debug logs, or process listings.
- Self-hosted runner trust, persistence, network reach, and cleanup match the sensitivity of the job.

## 3. Conditions and expression semantics

Trace every changed condition and expression:

- Boolean versus string behavior.
- Null, empty, missing, skipped, cancelled, success, failure, and always conditions.
- Operator precedence and implicit conversion.
- Branch and environment string matching.
- Step, job, stage, and dependency outputs.
- Matrix expansion, exclusions, fail-fast, and continue-on-error.
- Azure Pipelines compile-time template expressions versus runtime expressions and conditions.
- GitHub Actions contexts and whether values are attacker controlled.

A condition that looks readable can still run on skipped or failed dependencies, deploy to a default environment, or treat `"false"` as true.

## 4. Artifact and plan/deploy integrity

Verify:

- The artifact validated, scanned, previewed, or approved is the artifact deployed.
- Artifact names, paths, digests, retention, and download selectors cannot pick a stale or different run.
- Generated plans, compiled templates, packages, charts, manifests, inventories, and scripts are tied to the reviewed commit.
- Deployment does not re-resolve mutable dependencies after approval unless equivalent controls revalidate the result.
- Build and deploy jobs use compatible tool versions, lock files, parameters, and target identity.
- Artifacts containing plans, secrets, or environment data have restricted access and retention.
- Promotion across environments preserves provenance and does not rebuild silently.

## 5. Environment and target selection

Verify:

- Target environment is explicit and validated before credentials are acquired.
- CLI contexts are set and then read back or otherwise verified.
- Subscription, project, account, resource group, cluster, namespace, inventory, workspace, and state key are not inherited accidentally.
- Matrix or template parameters cannot cross-wire credentials and targets.
- Environment-specific variable groups, secret stores, parameter files, and approvals align.
- Defaults are safe and do not point to production.

## 6. Concurrency, cancellation, and stale runs

Verify:

- Concurrency groups are scoped by the real shared target.
- Cancel-in-progress behavior is safe for deployment jobs.
- A delayed older run cannot deploy after a newer run.
- State, resource, package, and configuration locks prevent collisions.
- Matrix jobs do not share unsafe workspaces, caches, temporary files, names, or ports.
- Cancellation cleanup does not delete healthy resources or release a lock while work continues remotely.
- Manual approvals expire or bind to the exact artifact and commit where supported.

## 7. Reusable workflows and templates

Verify:

- Inputs and secrets have explicit contracts and safe defaults.
- Callers cannot override protected target, identity, approval, or permission settings.
- Nested templates and reusable workflows are pinned to trusted immutable revisions where appropriate.
- Output types and names remain compatible with callers.
- Permissions do not expand unexpectedly when a reusable component is called.
- Repository or organization templates are reviewed at the resolved version, not only by name.

## 8. Dependency and supply-chain controls

Scrutinize:

- GitHub Actions pinned only to mutable tags or branches where immutable references are required.
- Azure DevOps extensions, tasks, marketplace components, containers, package feeds, and downloaded tools.
- `curl | sh`, `Invoke-Expression`, remote scripts, unsigned binaries, and missing checksums.
- Docker images using floating tags for privileged deployment jobs.
- Package installation that ignores lock files or resolves differently between validation and deployment.
- Pull-request code executed before the trust boundary is established.

## 9. Bash and POSIX shell

Review:

- Quoting of variables, command substitutions, paths, globs, and arrays.
- Exit status of pipelines, subshells, background jobs, and command substitutions.
- `set -e`, `set -u`, and `pipefail` semantics in the actual shell; do not treat them as a substitute for explicit error handling.
- Temporary-file creation, permissions, cleanup traps, and race resistance.
- Word splitting, glob expansion, newline handling, and filenames beginning with `-`.
- `eval`, constructed commands, and user-controlled input.
- Retry loops, timeouts, signals, traps, and partial side effects.
- Portability when scripts claim POSIX compatibility but use shell-specific features.

Use ShellCheck evidence where available, but verify deployment semantics manually.

## 10. Python deployment and orchestration scripts

Review:

- `subprocess` calls for argument arrays, `check=True` or explicit return-code handling, timeouts, captured output, and secret exposure.
- Exceptions that are swallowed or converted to successful exit status.
- API retries, pagination, partial results, idempotency, and timeouts.
- Temporary files, cleanup, file permissions, and encoding.
- Configuration loading, type validation, environment defaults, and target verification.
- Concurrency, async tasks, cancellation, and shared state.
- Dependency pinning and virtual-environment reproducibility.
- Logging that includes credentials, tokens, headers, request bodies, or sensitive outputs.

## 11. Deployment-command flags

Treat bypass or force flags as high-scrutiny signals:

- Auto-approve, force, replace, target, delete, purge, complete mode, no-lock, no-wait, skip-validation, insecure TLS, disabled host-key checking, continue-on-error, and equivalent options.
- Flags that suppress output needed to prove scope or destructive changes.
- Commands that deploy the current working tree rather than an immutable artifact.
- Commands that infer target from previously cached CLI context.

The presence of a flag is not automatically a defect; verify why it is necessary and what control replaces the bypassed safeguard.

## 12. Validation evidence

Use, when available:

- Workflow or pipeline schema validation.
- `actionlint`, task/template expansion, or platform preview features.
- ShellCheck for shell scripts.
- Python tests, type checks, linting, and mocked subprocess/API failure tests.
- Dry-run or preview modes that do not contact privileged targets.
- Logs showing exact commit, artifact digest, target, identity, and approval chain.

Do not execute an untrusted pipeline or deployment wrapper merely to validate syntax.
