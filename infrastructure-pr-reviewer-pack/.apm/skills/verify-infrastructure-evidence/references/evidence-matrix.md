# Infrastructure Review Evidence Matrix

## Evidence Integrity

For every artifact, verify:

- Exact reviewed commit or immutable source digest.
- Intended environment, tenant/account/subscription/project, region, resource group, cluster, namespace, inventory, workspace, and state key.
- Same variables, parameters, secrets source, identity, dependency lock, tool version, and generated modules used by deployment.
- Artifact provenance, access controls, retention, and whether deployment consumes that artifact without silent rebuild or re-resolution.

## Technology Matrix

| Technology | Safe local evidence | Higher-risk or target-specific evidence | Key limitation |
|---|---|---|---|
| Terraform/OpenTofu | `fmt -check`, initialized `validate`, parser/static checks | Existing-state plan, migration rehearsal, policy, apply provenance | Empty-state or wrong-target plans do not prove upgrade safety |
| Bicep/ARM | Lint, compile to ARM JSON | Exact-scope what-if, policy evaluation, deployment provenance | Compilation does not establish target or deletion behavior |
| PowerShell | Parser, PSScriptAnalyzer, isolated unit tests | Pester with controlled mocks, platform matrix, safe disposable integration | Parsing does not prove native exit propagation or idempotency |
| Ansible | Offline lint and syntax when dependencies exist | Limited safe-target check/diff, disposable integration, second-run idempotence | Check mode support varies and may still change targets |
| CI/CD and scripts | Schema/lint, ShellCheck, unit tests, template expansion | Permission review, OIDC claims, protected environment evidence, artifact digest chain | Do not execute untrusted workflow code with privileged context |
| Kubernetes/Helm/Kustomize | YAML/schema, Helm lint/render, Kustomize build | Policy/admission, server-side dry-run, GitOps diff against representative cluster | Client render does not prove CRD/admission or upgrade behavior |

## Risk Escalation

Require stronger evidence for production, shared, data-bearing, identity, network, public exposure, destructive, state or ownership transfer, provider/API upgrade, pipeline permission, deployment-mode, or cross-tool migration changes.

## Result Semantics

- **Pass:** The exact check completed successfully; state only what that check establishes.
- **Fail:** The check produced a reproducible defect or invalid artifact; preserve the relevant evidence.
- **Skip:** A tool, dependency, target, permission, or safe precondition was unavailable.
- **Evidence gap:** The risk cannot be cleared without a specific target-linked artifact.
- **Not applicable:** The check does not apply to the changed stack or path.
