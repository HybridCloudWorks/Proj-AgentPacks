# Bicep and ARM Template Review Adapter

Apply this adapter to `.bicep`, `.bicepparam`, ARM JSON templates, deployment-stack definitions, template specs, module registry references, and workflows that compile or deploy them.

## 1. Entry point, deployment scope, and identity

Identify:

- Entry-point files and module graph.
- `targetScope` and the actual CLI or pipeline deployment scope.
- Tenant, management group, subscription, resource group, and location selection.
- Deployment name and whether deployment-history behavior matters.
- Parameter sources, secure parameters, defaults, environment overlays, and generated parameter files.
- The identity performing validation, what-if, and deployment.

Verify that source-level scope and command-level scope agree. Fail closed when a subscription, resource group, location, or tenant value is absent or malformed.

## 2. Resource identity and existing resources

Review:

- Resource type, name, scope, parent, and API version.
- Loop keys, index-based names, conditions, and changes to symbolic-name references.
- `existing` declarations and whether they identify the intended object at the intended scope.
- Parent-child resource names and extension-resource scopes.
- Role-assignment or other deterministic GUID generation and its input stability.
- Transfer of ownership between Bicep, Terraform, scripts, deployment stacks, or manual management.

A symbolic-name rename alone usually does not change the deployed identity; a name, scope, type, parent, or deterministic-ID change can.

## 3. Deployment and deletion behavior

Determine the actual deployment mechanism and mode. Review whether omitted resources or properties are retained, reset, detached, or deleted under that mechanism.

Scrutinize:

- Complete, purge, delete, detach, or deployment-stack behavior.
- Resource conditions that become false for existing objects.
- Changes that remove a resource from the entry point or module graph.
- Immutable property changes and replacement requirements.
- Data-bearing resources, locks, retention, soft delete, backup, and recovery.
- Nested deployments and deployment names that can conflict or overwrite history.
- Cleanup scripts that execute outside ARM's declarative lifecycle.

Do not infer deletion behavior from the source alone; verify the exact command, API, mode, and target scope.

## 4. API versions and resource schemas

Verify:

- API versions support the used properties and are appropriate for the target cloud and regions.
- A version change does not remove defaults, rename properties, change enum values, or alter read/write behavior unexpectedly.
- Preview APIs are deliberate and accepted for the environment.
- Child and extension resources use the correct type and scope.
- Read-only, computed, or server-defaulted properties are not treated as stable inputs.

Consult the current resource-provider schema or official reference when uncertain.

## 5. Modules and registries

Verify:

- Local and registry module references resolve to the intended source.
- Registry tags or versions are immutable or sufficiently constrained for production use.
- Module inputs, outputs, types, defaults, and secure values remain compatible.
- Aliases in `bicepconfig.json` cannot redirect modules unexpectedly.
- Restore behavior and caches do not allow validation to use different module content than deployment.
- Published template specs or module artifacts have provenance and versioning.

## 6. Expressions, loops, and conditions

Review:

- Null, empty, boolean, object, array, and union-type behavior.
- `if` conditions and whether dependencies or outputs still exist when a resource is skipped.
- Loops, batch sizing, name uniqueness, index stability, and multiplicative resource creation.
- Safe dereference and null-forgiving operations.
- String interpolation, resource IDs, subscription or resource-group functions, and scope functions.
- Runtime values used to determine resource IDs, conditions, scope, names, or API versions.
- Explicit `dependsOn` entries that serialize unnecessarily or hide a missing symbolic dependency.

Bicep automatically derives many dependencies from symbolic references. Extra `dependsOn` is not automatically a defect, but missing runtime dependency or accidental serialization can be.

## 7. Parameters, outputs, and secrets

Verify:

- Required parameters have validation and safe environment-specific values.
- Secure parameters are not assigned insecure defaults, emitted as outputs, written to artifacts, or passed on command lines that are logged.
- Outputs have stable names and types for downstream PowerShell, pipelines, Terraform, Ansible, or applications.
- Output consumers handle absent conditional resources and null values.
- Parameter files do not contain committed secrets.
- `getSecret` or equivalent secret references use the intended vault and deployment identity.

## 8. Networking, identity, and policy

Scrutinize:

- Role assignments, managed identities, federated credentials, policy assignments, locks, and deny settings.
- Public network access, firewall rules, private endpoints, DNS links, routes, NSGs, ingress, and service endpoints.
- Broad role scopes, wildcard permissions, inherited access, and deterministic role-assignment identities.
- Policy effects that can deny, modify, or deploy additional resources beyond the visible template.
- Cross-subscription or cross-tenant deployment assumptions.

## 9. What-if and compiled-template evidence

Use both source and generated evidence:

- `bicep lint` for syntax and configured rules.
- `bicep build ... --stdout` for compiled ARM JSON.
- A target-scoped what-if result for the exact commit, parameters, identity, and deployment command.

Cautions:

- Compilation proves translation, not target correctness.
- What-if is evidence, not absolute proof; runtime-dependent values and unsupported provider behavior can reduce precision.
- Ensure the deployment job consumes the reviewed source or immutable compiled artifact, not a later recompile with different modules or parameters.
- Review every predicted delete, replacement-like action, ignored change, and no-change result that conflicts with intent.

## 10. CI/CD integrity

Verify:

- Validation, what-if, approval, and deployment use the same source revision and parameter set.
- The service connection or federated identity is scoped to the intended environment.
- Deployment scope is explicit in every command.
- CLI context cannot fall back to a default subscription or resource group.
- Generated templates and parameter artifacts are protected and traceable to the commit.
- Environment approvals and concurrency controls prevent overlapping or stale deployments.
- Deployment commands propagate failures and do not use permissive flags without a documented reason.
