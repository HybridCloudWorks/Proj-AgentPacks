# Terraform and OpenTofu Review Adapter

Apply this adapter only to Terraform or OpenTofu configuration, tests, state-migration declarations, provider locks, and workflows that run those tools. Verify version-specific behavior against the installed CLI and current official documentation.

## 1. Root modules and execution context

Identify:

- Root modules and reusable child modules.
- CLI and language version constraints.
- Provider sources, versions, aliases, and inherited versus explicit mappings.
- Backend type, state key, workspace or environment model, and locking mechanism.
- Variable sources and precedence: defaults, tfvars, environment variables, CLI flags, pipeline inputs, and generated files.
- Plan and apply entry points, wrapper tools, and policy or test stages.

Do not review a child module as if it controls the backend or deployment identity unless its callers do so.

## 2. State identity and ownership

Scrutinize:

- Resource and module renames.
- `count` to `for_each`, `for_each` to `count`, key changes, collection reordering, and conditional creation changes.
- `moved`, `import`, and `removed` blocks or equivalent state operations.
- Backend, workspace, state key, account, subscription, project, region, or provider-alias changes.
- Transfer of an object between root modules, states, workspaces, providers, or tools.

Verify that existing addresses map to the intended remote objects. A clean plan against empty state does not prove an upgrade is safe.

Raise a finding when a changed address can recreate, orphan, duplicate, or destroy an existing object without an explicit migration path.

## 3. Plan semantics and lifecycle

Require a plan against representative existing state for changes involving:

- Immutable or replacement-sensitive arguments.
- Data-bearing or shared resources.
- Provider or module upgrades.
- Lifecycle rules.
- Address or backend changes.
- Computed values that determine identity, count, keys, or scope.

Review create, update, replace, delete, import, move, and no-op actions explicitly.

Scrutinize:

- `create_before_destroy` where uniqueness, quota, IP, port, or singleton constraints prevent coexistence.
- `prevent_destroy` that hides the need for a migration or creates an unmaintainable dead end.
- `ignore_changes` that suppresses security, identity, networking, encryption, or ownership drift.
- `replace_triggered_by` that expands replacement blast radius.
- `-target`, `-replace`, `-refresh=false`, `-lock=false`, direct state commands, or forced unlock operations.
- Saved plans that are generated with different variables, credentials, state, or revision than the apply job.

## 4. Expressions, collections, and unknown values

For changed expressions, test mentally or with unit tests:

- Null, unknown, empty, zero, false, duplicate, and reordered values.
- `try`, `can`, `coalesce`, conditional expressions, optional attributes, and defaults.
- Collection conversions that lose ordering, uniqueness, or key stability.
- `flatten`, `merge`, `zipmap`, comprehensions, and dynamic blocks.
- Unknown values used as iteration keys, counts, provider settings, or resource identity.
- Sensitive values transformed into nonsensitive outputs or logs.

Do not infer behavior from variable names; trace the actual expression graph.

## 5. Module contracts

Verify:

- Inputs have correct types, validation, nullable behavior, and safe defaults.
- Required providers and aliases are declared and passed correctly.
- Outputs preserve types, sensitivity, and compatibility for all consumers.
- Module source and version changes are intentional and reproducible.
- A change in a reusable module does not break callers that are outside the visible diff.
- Deprecated inputs or outputs have a migration path.
- Local path modules used in CI resolve to the intended source.

Search all callers and consumers before declaring an interface safe.

## 6. Providers and dependencies

Verify:

- Terraform/OpenTofu, provider, and module versions are intentionally constrained.
- `.terraform.lock.hcl` changes match the declared dependency change.
- Provider source addresses and aliases are correct.
- Major upgrades include release-note, schema, plan, and migration evidence.
- Mutable branches or unpinned module references are not used for production-critical code.
- Provider default tags, features, locations, or identities do not silently change unrelated resources.

Do not report lock-file hash volume alone. Report unexpected providers, versions, source changes, downgrades, removals, or unexplained churn.

## 7. Data sources and external dependencies

Verify:

- Data-source queries are scoped narrowly and return a unique intended result.
- External data or local-exec scripts are deterministic, safe, and fail correctly.
- Runtime API lookups do not make plans unstable or environment-dependent without controls.
- Cross-state reads use the intended state and do not expose sensitive outputs broadly.
- Provider-computed values are not assumed known before apply.

## 8. Security and sensitive data

Verify:

- No credentials or secrets in source, tfvars, state artifacts, plan artifacts, outputs, logs, or command lines.
- Sensitive variables and outputs are marked where appropriate, while recognizing that sensitivity markings do not remove values from state.
- IAM, role assignments, policies, security groups, firewall rules, public endpoints, and encryption changes follow least privilege.
- State storage has access control, encryption, versioning or recovery, and locking appropriate to its risk.
- CI uses short-lived identity where supported and scopes permissions to plan or apply needs.

## 9. CI/CD integrity

Verify:

- Pull-request jobs do not apply to privileged environments.
- Plan and apply use the same code revision, variables, provider locks, state, workspace, identity, and target.
- The approved saved plan is the artifact applied, or a freshly generated plan is protected by equivalent approval controls.
- State locking and pipeline concurrency prevent overlapping applies.
- Environment approvals and branch protections cannot be bypassed by condition or path changes.
- Backend initialization cannot select a default or wrong state silently.
- Plan artifacts are protected because they can contain sensitive values.

## 10. Validation evidence

Use, when safe and available:

```text
terraform fmt -check -diff -recursive
terraform init -backend=false
terraform validate
terraform test
terraform plan
```

Use the equivalent OpenTofu commands for OpenTofu repositories.

Cautions:

- `validate` establishes syntax and internal consistency, not remote-service correctness or existing-state behavior.
- `test` can execute plan or apply operations and may create real infrastructure.
- `plan` can read remote systems and state and must use the correct target and credentials.

Never treat a clean formatter, validator, or linter result as proof of lifecycle correctness.
