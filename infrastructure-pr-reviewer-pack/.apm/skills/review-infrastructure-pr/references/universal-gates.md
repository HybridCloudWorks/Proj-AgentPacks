# Universal Infrastructure and Automation Review Gates

Apply only the gates relevant to the change, but do not omit a gate merely because the file uses a different tool or language.

## 1. Intent and target correctness

Verify:

- The declared intent matches the actual create, update, replace, delete, configure, or deploy behavior.
- Target selection is explicit and cannot silently fall back to a default tenant, account, subscription, project, region, resource group, cluster, namespace, host, inventory, workspace, state key, or environment.
- Credentials and identities correspond to the target and use the expected trust boundary.
- Branch, tag, path, matrix, user input, and environment-derived target selection are validated and fail closed.
- Production cannot be reached through a pull-request job, untrusted fork, ambiguous condition, missing environment, or typo.
- Names, IDs, scopes, and references point to the intended existing objects.

High-risk signals include implicit CLI context, inherited environment values, global defaults, substring matching for environment names, and targets derived directly from branch names.

## 2. Idempotency, convergence, and determinism

Verify:

- Re-running with unchanged inputs produces no unintended change.
- Partial execution followed by retry converges to the intended state.
- Imperative scripts detect current state rather than blindly creating or appending.
- Configuration-management tasks use idempotent modules or define accurate `changed` and failure behavior.
- Generated names, GUIDs, timestamps, random values, ordering, and serialization are stable where identity matters.
- API responses, unordered maps, filesystem enumeration, and command output do not create nondeterministic plans or artifacts.
- A failure after an external side effect does not cause duplication on retry.

## 3. Ownership, state, and drift

Verify:

- Exactly one authoritative tool owns each object or setting unless shared ownership is explicitly safe.
- State, deployment history, inventory, or controller ownership remains associated with the correct target.
- Renames, moves, imports, adoptions, detachments, and tool-to-tool migrations preserve identity and do not orphan or recreate resources accidentally.
- Ignore or drift-suppression rules are narrow and do not hide security or configuration regression.
- Out-of-band changes are detected, reconciled, or intentionally preserved.
- Generated state, plans, caches, inventories, and temporary ownership files are not committed when they contain secrets or environment-specific data.

## 4. Lifecycle and destructive impact

Verify:

- Create, update, replace, delete, purge, detach, and deconfigure behavior is understood for existing targets.
- Immutable-property changes and replacement triggers are identified.
- Data-bearing and shared resources have retention, backup, restore, and migration plans.
- Delete or purge modes cannot remove objects omitted unintentionally from a template, inventory, or configuration.
- Create-before-destroy or rolling replacement can coexist within naming, quota, IP, port, singleton, or capacity constraints.
- Destroy-before-create does not create unacceptable downtime or loss.
- Cleanup steps do not run after a failed prerequisite in a way that removes healthy resources.
- Rollback is feasible after schema, identity, state, secret, or data migration.

## 5. Inputs, types, and validation

Verify:

- Required inputs fail early with actionable errors.
- Defaults are safe for every environment, especially production.
- Null, empty string, empty collection, zero, false, missing key, duplicate key, and malformed values behave intentionally.
- Enumerations, ranges, resource IDs, CIDRs, host patterns, paths, and names are validated.
- Secure inputs remain secure through outputs, logs, files, artifacts, and subprocess arguments.
- Type conversion across YAML, JSON, HCL, Bicep, PowerShell, shell, and pipeline expressions preserves meaning.
- Quoting and escaping protect whitespace, metacharacters, wildcard characters, newlines, and user-controlled input.
- Boolean-like strings such as `"false"` are not treated as truthy accidentally.

## 6. Dependencies and ordering

Verify:

- Explicit and implicit dependencies reflect actual runtime requirements.
- Parallel execution is safe.
- Outputs are consumed only after they are available and validated.
- Scripts do not rely on eventual consistency without bounded retry and a clear timeout.
- Handlers, post-deployment jobs, health checks, and cleanup steps run under the correct success or failure conditions.
- Cross-stack references do not create circular dependencies or hidden deployment order.
- Dependency removal does not leave stale consumers or orphaned permissions.

## 7. Security and secrets

Verify:

- Least privilege for identities, roles, service connections, runners, hosts, modules, tasks, and deployment commands.
- No hardcoded credentials, tokens, private keys, connection strings, certificates, vault passwords, or sensitive defaults.
- Secrets are not exposed through command-line arguments, process listings, logs, debug traces, outputs, diffs, artifacts, caches, or generated files.
- Public network exposure, firewall rules, ingress, anonymous access, wildcard origins, and broad CIDRs are intentional and minimized.
- Encryption at rest and in transit is preserved.
- TLS verification, signature verification, and host-key checking are not disabled without a narrowly justified control.
- Downloads and executable dependencies have trusted sources and integrity verification.
- User-controlled values cannot become shell, PowerShell, template, expression, path, or workflow-command injection.
- Sensitive logs and Ansible diffs use appropriate suppression without hiding all operational evidence.

## 8. Error handling and exit status

Verify:

- Failures propagate to the caller and pipeline.
- Native command exit codes are checked in scripting languages that do not automatically throw.
- Non-terminating errors are converted to terminating failures when correctness depends on them.
- `continue-on-error`, ignored errors, forced success, rescue blocks, and fallback paths do not conceal failed deployment or configuration.
- Retries are bounded, selective, and do not repeat non-idempotent actions blindly.
- Timeouts exist for remote operations, readiness waits, locks, and polling loops.
- Cleanup runs at the correct time and preserves diagnostic evidence.
- Error messages identify the failed target and operation without leaking secrets.

## 9. Concurrency and locking

Verify:

- Concurrent runs against the same target are prevented or safe.
- State, deployment, package, or configuration locks are enabled and have recovery procedures.
- Pipeline concurrency groups distinguish environments correctly.
- Matrix jobs cannot collide on shared names, files, workspaces, caches, or targets.
- A rerun or delayed job cannot apply stale artifacts after a newer deployment.
- Cancellation does not leave locks, leases, half-written files, or temporary credentials.
- Leader-only, `run_once`, delegated, or singleton tasks execute on the intended host and only once.

## 10. Version and supply-chain integrity

Verify:

- Tool, provider, module, collection, role, action, image, chart, extension, and runtime versions are intentionally constrained.
- Production dependencies do not use mutable branches, floating tags, `latest`, or unverified download URLs where reproducibility matters.
- Lock-file or dependency-file changes match the declared upgrade.
- Major or breaking upgrades include migration and compatibility evidence.
- Checksums, signatures, immutable digests, or trusted registries protect executable artifacts where supported.
- Generated output is reproducible from reviewed source.
- Dependency update automation cannot bypass review, policy, or environment gates.

## 11. Reliability, availability, and recovery

Verify:

- Rollout strategy preserves required capacity and redundancy.
- Health probes, readiness checks, service restarts, handler timing, and dependency readiness are correct.
- Single-zone, single-instance, or singleton changes are deliberate.
- Retry behavior handles eventual consistency without masking permanent errors.
- Backups are not merely configured but restorable within requirements.
- Rollback procedures account for irreversible data or schema changes.
- Monitoring, alerts, logs, and ownership exist for newly introduced failure modes.
- Maintenance windows, drain behavior, serial execution, and failure thresholds match the blast radius.

## 12. Cost, quota, and capacity

Verify:

- New resources, replicas, SKUs, retention, logging, egress, public IPs, licenses, and hosted runners have understood cost impact.
- Loops and matrices cannot create an unintended multiplicative number of resources or jobs.
- Quotas and regional capacity support replacement and scale-out.
- Autoscaling boundaries, minimums, maximums, and defaults are safe.
- Orphaned resources, snapshots, disks, addresses, identities, secrets, or artifacts are cleaned up intentionally.

## 13. Observability and operability

Verify:

- Operators can identify what version, commit, target, and identity performed the change.
- Logs are useful but do not expose secrets.
- Deployment outputs and pipeline summaries identify replacements, deletions, skipped targets, and partial failures.
- Alerts and dashboards cover new critical dependencies.
- Runbooks, ownership, support boundaries, and rollback commands remain accurate.
- Manual recovery steps are documented when automation cannot safely handle them.

## 14. Validation and test evidence

Select evidence appropriate to the tool and risk:

- Parser, formatter, linter, schema validation, and compilation.
- Unit tests for transformations, parameter validation, and script logic.
- Mocked failures for API, native command, timeout, and partial-result paths.
- Plan, what-if, rendered output, or check-mode evidence for exact inputs and targets.
- Policy, security, dependency, secret, and configuration scans.
- Idempotence test: a second safe run reports no unintended change.
- Upgrade test against representative existing state.
- Rollback or recovery rehearsal for high-risk production changes.

A green pipeline is insufficient when required checks were skipped, ran on the wrong files, used different inputs, or produced an artifact different from the one deployed.
