# Infrastructure PR Review Protocol

## Contents

1. Review posture
2. Coverage ledger
3. Technology and execution inventory
4. Cross-tool dependency tracing
5. Existing-environment reasoning
6. Evidence hierarchy
7. Finding threshold
8. False-positive controls
9. Completion test

## 1. Review posture

Assume a change can be syntactically valid, formatted, tested, and still be operationally wrong. Review the transition from the current managed environment to the proposed environment, not only the final source text.

Use six simultaneous views:

- **Text view:** What changed on each added or deleted line?
- **Graph view:** Which inputs, modules, roles, scripts, resources, tasks, outputs, and workflows depend on it?
- **Target view:** Which tenant, account, subscription, project, region, resource group, cluster, namespace, inventory, host, workspace, or state key receives the change?
- **Ownership view:** Which tool owns each object or setting before and after the change?
- **Execution view:** In what order do templates, scripts, tasks, jobs, and deployment commands run?
- **Operations view:** How do failure, retry, cancellation, concurrency, rollback, and re-run behave?

Do not force one tool's concepts onto another. Terraform state addresses, Bicep deployment scopes, Ansible host patterns, PowerShell exit-code handling, and pipeline conditions are different mechanisms that must be reviewed on their own terms.

## 2. Coverage ledger

Create one ledger entry for every added or deleted line. Group adjacent lines only when they implement one inseparable expression, object, task, or command.

Track these fields internally:

| Field | Required question |
|---|---|
| Location | Which file and old or new line is under review? |
| Semantic change | What behavior changed, including deleted behavior? |
| Technology | Which parser, runtime, deployment engine, or controller interprets it? |
| Upstream inputs | Which parameters, variables, outputs, environment values, secrets, inventories, or generated artifacts determine it? |
| Downstream effects | Which resources, hosts, files, commands, jobs, or consumers are affected? |
| Target | Which environment and identity execute the change? |
| Ownership | Which tool owns the object or setting before and after the change? |
| Lifecycle effect | Create, update, replace, delete, adopt, detach, move, restart, or no-op? |
| Failure modes | What happens for null, empty, malformed, duplicate, partial, retry, cancellation, and concurrency cases? |
| Evidence | Which test, plan, what-if, compiled output, linter, schema, policy result, log, or repository rule proves the conclusion? |
| Disposition | Verified, finding, evidence gap, or not applicable? |

A line is not covered merely because a file parsed, a linter passed, or a neighboring block was reviewed.

### Deleted lines

Treat every deletion as a behavior change. Determine which validation, dependency, permission, cleanup, output, lifecycle control, error check, approval, or operational guarantee disappeared. Confirm whether another line replaces it.

### Renames and moves

Determine whether a rename changes only source organization or also changes a resource identity, deployment name, state address, task include path, module source, role path, artifact name, environment key, or consumer contract.

### Generated files

Identify generated artifacts such as lock files, compiled ARM JSON, rendered manifests, dependency files, inventories, plans, or generated documentation.

- Verify that the source change explains the generated diff.
- Detect hand edits that will be overwritten.
- Check unexpected dependency additions, removals, downgrades, major upgrades, or broad churn.
- Confirm the pipeline consumes the same generated artifact that was reviewed.

### File mode and binary changes

Review executable-bit changes for scripts and hooks. For binary artifacts, verify provenance, reproducibility, expected consumers, and whether the repository should contain them.

## 3. Technology and execution inventory

Before reviewing details, inventory the changed stack and entry points.

Examples:

- Terraform/OpenTofu root modules, child modules, providers, backends, workspaces, and plans.
- Bicep entry files, modules, parameter files, target scopes, deployment names, and compiled templates.
- PowerShell modules, scripts, advanced functions, native commands, and calling pipelines.
- Ansible playbooks, roles, collections, inventories, group variables, handlers, and vault usage.
- GitHub Actions, Azure Pipelines, Jenkinsfiles, GitLab CI, reusable workflows, templates, and environments.
- Kubernetes manifests, Helm charts, values files, Kustomize overlays, and controllers.
- Bash or Python orchestration scripts and the tools they invoke.

Write the execution sequence. Example:

1. GitHub Actions selects an environment from the branch.
2. Bicep deploys a resource group and emits host data.
3. PowerShell transforms the output into an Ansible inventory.
4. Ansible configures the hosts.
5. A smoke test validates the service.

Review the sequence as one system. A valid individual file can still break the handoff.

## 4. Cross-tool dependency tracing

Trace each changed symbol and value in both directions.

### Upstream tracing

Identify values that determine the changed behavior:

- Defaults, parameter files, tfvars, Bicep parameter files, PowerShell parameters, Ansible vars, values files, and environment variables.
- Pipeline matrices, conditions, branch or path filters, secrets, service connections, OIDC claims, runner labels, and reusable workflow inputs.
- Outputs from prior tools, JSON serialization, command substitution, temporary files, artifacts, and generated inventories.
- Identity, region, subscription, project, cluster, namespace, inventory, workspace, and state selection.
- Version constraints, lock files, module sources, registries, collections, roles, actions, images, and charts.

### Downstream tracing

Identify consumers and side effects:

- Resource declarations, modules, deployments, tasks, handlers, cmdlets, native commands, API calls, and controllers.
- Outputs, artifacts, remote-state consumers, application settings, host configuration, policies, smoke tests, and runbooks.
- Cleanup or rollback jobs, post-deployment verification, monitoring, and alerting.

Text search is useful but incomplete. Values may flow through outputs, generated files, JSON, templates, environment variables, pipeline artifacts, and dynamic expressions.

### Type and representation boundaries

Check every boundary where one tool passes data to another:

- String versus number, boolean, null, array, object, secure value, or unknown value.
- JSON depth, escaping, newline handling, encoding, path separators, quoting, globbing, and shell expansion.
- Secret masking and whether values are exposed in command lines, logs, artifacts, or outputs.
- Case sensitivity, naming normalization, resource-ID formats, and URI construction.
- Empty collections, singleton collections, duplicate keys, and ordering assumptions.

### Ownership boundaries

For every managed object, determine:

- Which tool creates it?
- Which tool updates it?
- Which tool deletes it?
- Which tool detects or ignores drift?
- Whether two tools can overwrite each other.
- Whether ownership intentionally transfers and how that transition is performed.

Overlapping ownership is a finding when it can cause perpetual drift, lost changes, unsafe deletion, or nondeterministic results.

## 5. Existing-environment reasoning

Evaluate both a clean deployment and an update against representative existing infrastructure or configuration.

Ask:

- Does the object identity remain stable?
- Does a rename imply replacement, recreation, detachment, or ownership loss?
- Do loops or iteration keys remain stable?
- Will a changed immutable property force replacement?
- Can old and new objects coexist during migration?
- Could ordering, quota, uniqueness, IP allocation, singleton constraints, or locks prevent safe replacement?
- Does a deployment mode, purge option, or absent-property behavior remove existing settings?
- Does a configuration-management task converge or oscillate on repeated runs?
- Does an imperative script correctly distinguish already-present, absent, and partially configured states?
- Does the pipeline target the same environment and identity after retry or rerun?
- Does cancellation leave a lock, temporary credential, partial artifact, or half-completed configuration?

Require environment-specific evidence when the answer depends on current state, provider or API behavior, target inventory, or deployment history.

## 6. Evidence hierarchy

Prefer evidence in this order, adjusted for the technology:

1. Repository code, tests, policies, and configuration that directly establish behavior.
2. Saved plan, what-if output, compiled template, check-mode/diff output, rendered manifest, or test result for the exact revision, target, and inputs.
3. Installed tool schema, module metadata, command help, or controller behavior.
4. Current official product documentation.
5. Reproducible experiment in a disposable environment.
6. Maintainer issue or release note when official documentation is incomplete.
7. Reasoned inference clearly labeled as inference.

Do not use memory alone for version-specific, provider-specific, module-specific, or service-specific behavior.

### Evidence integrity

Verify that evidence corresponds to:

- The reviewed commit.
- The intended target environment.
- The same parameters, variables, inventory, secrets source, and identity.
- The artifact ultimately applied or deployed.
- Representative existing state rather than an empty environment only.

A plan or what-if generated for a different target is not valid evidence.

## 7. Finding threshold

Raise a finding only when all are true:

1. The issue is introduced or exposed by the PR.
2. A specific execution path, input, target, or environment triggers it.
3. The impact is material to correctness, security, state, reliability, availability, recoverability, operability, or cost.
4. The claim is supported by evidence or by a clearly stated uncertainty that itself prevents safe approval.
5. A useful remediation direction exists.

Use an evidence gap rather than a defect when the implementation may be correct but high-risk behavior cannot be verified from available artifacts.

## 8. False-positive controls

Do not report:

- A tool preference without a demonstrated defect.
- A generic recommendation that is unrelated to the changed behavior.
- Formatting already enforced by automation.
- A hypothetical input that the repository contract provably excludes.
- A missing test without naming the exact behavior and failure the test must detect.
- A missing comment or documentation unless operators or consumers would otherwise act incorrectly.
- A provider, cloud, module, cmdlet, or collection behavior that has not been verified.
- Duplicate symptoms caused by one root issue.
- A pre-existing defect not made materially worse or reachable by the PR.

Before commenting, try to disprove the finding by checking callers, defaults, validations, conditions, policies, tests, and current documentation.

## 9. Completion test

Do not finish until all are true:

- Every changed line and deletion has a disposition.
- Every changed technology has an identified entry point and target.
- Every cross-tool handoff has compatible types, encoding, quoting, secrecy, and ownership.
- Existing-environment behavior has been considered.
- Destructive and security-sensitive paths have explicit evidence.
- Failure, retry, cancellation, concurrency, rollback, and rerun behavior have been reviewed.
- Findings meet the threshold and are not duplicated.
- Evidence gaps are clearly separated from confirmed defects.
