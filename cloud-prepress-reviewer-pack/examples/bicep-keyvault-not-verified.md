# Worked example: Bicep Key Vault change with no preview evidence

Prompt: `.apm/prompts/review-deployment-preview.prompt.md`. Outcome: `NOT_VERIFIED`. This example shows an unverified outcome: the change may be correct, but the evidence the gate needs could not be obtained.

Skills applied: cloud-prepress-orchestration, change-scope-and-impact, iac-policy-and-identity-review, deployment-preview-and-environment-review, azure-evidence-and-mcp-review, tests-build-and-dependency-review, role-authority-and-handoff-review, review-report-and-pr-gate.

The repository, vault, identities and resource groups are fictional.

## Request

> We're moving `kv-app-prod` from access policies to Azure RBAC. The PR is `feature/kv-rbac`. Review it before the prod deployment review.

## 1. Fix scope and boundary (cloud-prepress-orchestration)

- Target: `app-infra`, head `feature/kv-rbac` at `b27e0f4`, base `main`.
- Environment: `prod`; resource group `rg-app-prod`; deployment scope is resource group, through `az deployment group create` in the release pipeline.
- Evidence supplied: none beyond the diff. No what-if has been captured.

A permission-model change on a production vault depends on live state the repository does not show. The reviewer asks before doing anything live:

> To verify this I need either a what-if for `main.bicep` against `rg-app-prod`, or a read-only list of the access policies on `kv-app-prod`. May I run `az deployment group what-if` and `az keyvault show --query properties.accessPolicies` with your current credentials, at that resource group only?

> No. Prod access goes through the release team. I can't authorize that.

The reviewer records the refusal as the authorization boundary and runs nothing against Azure.

## 2. Scope (change-scope-and-impact)

```text
$ git diff --name-status main...feature/kv-rbac
M       modules/keyvault.bicep
M       main.bicep
M       main.parameters.prod.json
```

The diff to `modules/keyvault.bicep`:

```bicep
-    enableRbacAuthorization: false
-    accessPolicies: [
-      {
-        tenantId: tenant().tenantId
-        objectId: webAppPrincipalId
-        permissions: { secrets: [ 'get', 'list' ] }
-      }
-    ]
+    enableRbacAuthorization: true
```

```bicep
+resource secretsUser 'Microsoft.Authorization/roleAssignments@2022-04-01' = {
+  name: guid(kv.id, webAppPrincipalId, keyVaultSecretsUserRoleId)
+  scope: kv
+  properties: {
+    roleDefinitionId: subscriptionResourceId('Microsoft.Authorization/roleDefinitions', keyVaultSecretsUserRoleId)
+    principalId: webAppPrincipalId
+    principalType: 'ServicePrincipal'
+  }
+}
```

Within the template the change is self-consistent: the web app's access policy becomes an RBAC role at vault scope. The open question is who else reads the vault. `TOPOLOGY.md`, which is unchanged but inspected for this reason, says the nightly reporting job reads `report-signing-key` from `kv-app-prod`. This template has never granted that job anything, so its access must come from somewhere the repository does not show.

## 3. IaC and identity (iac-policy-and-identity-review)

What the reviewer can confirm from the files:

- The role assignment name is a deterministic `guid()` of vault, principal and role, so redeployment is idempotent.
- The scope is the vault, not the resource group.
- `principalType` is set, which avoids failures caused by replication delay for a newly created identity.
- `keyVaultSecretsUserRoleId` matches the built-in Key Vault Secrets User role in the Microsoft Learn built-in roles reference.
- `enablePurgeProtection` and `publicNetworkAccess: 'Disabled'` are unchanged.

What it cannot confirm:

- **Other principals.** Microsoft Learn's Key Vault guidance on migrating from vault access policies to Azure RBAC states that once a vault uses the RBAC permission model, its access policies are no longer evaluated. Any principal that holds only an access policy loses access at deployment. Whether such principals exist is live state.
- **The deployment identity.** The repository `README.md` documents `id-deploy-app-prod` as Contributor on `rg-app-prod`. Contributor cannot create role assignments. If that description is current, the deployment fails on the new role assignment. The live role set is not visible.

Both are plausible and high-impact, and neither is provable here. Each is recorded as a validation hypothesis with the exact evidence that would settle it.

## 4. Build and preview

```text
$ az bicep build --file main.bicep --stdout >/dev/null
$ echo $?
0
```

That proves the template compiles; it says nothing about the effect on the live vault. The what-if is `not-verified`.

## 5. Why `NOT_VERIFIED` and not another outcome

- Not `CHANGES_REQUIRED`: no defect is confirmed. The template may be complete if the reporting job already holds an RBAC role, or was migrated earlier.
- Not `BLOCKED_ON_HUMAN_DECISION`: no decision is pending. What is missing is evidence, which the release team can produce with access it already holds.
- Not `READY_FOR_DEPLOYMENT_REVIEW`: a production permission-model switch without a preview or a read of current access is exactly what the gate exists to stop.

## Completion report

### Scope and inputs

| Item | Value |
|---|---|
| Repository and refs | `app-infra`, base `main`, head `feature/kv-rbac` at `b27e0f4` |
| Change intent | Move `kv-app-prod` from vault access policies to the Azure RBAC permission model |
| Change class | identity, infrastructure |
| Target environment | `prod`, resource group `rg-app-prod`, resource-group deployment scope |
| Requirements and design | `TOPOLOGY.md`; no ADR covers the permission model |
| Owner | Change: application platform team. Vault: application platform team. Release: release team. |
| Authorization boundary | Read-only review of the repository. Live read-only queries requested and declined by the user. No what-if, deployment, RBAC or policy change. |
| Report location | `../reviews/app-infra/kv-rbac/REVIEW.md` |

### Changed paths and methods

| Path | Change class | Review method |
|---|---|---|
| `modules/keyvault.bicep` | identity, infrastructure | Read in full; checked permission model, role assignment name, scope and principal type |
| `main.bicep` | infrastructure | Read diff; traced the module parameters |
| `main.parameters.prod.json` | infrastructure | Read diff; confirmed it passes identities and holds no secret values |

Paths inspected outside the diff, and why:

- `TOPOLOGY.md`: to find other readers of the vault.
- `README.md`: the documented role of the deployment identity.

### Evidence ledger

| Evidence | Label | Source, command or capture | Bound to |
|---|---|---|---|
| Permission model switched; web app access policy replaced by a vault-scope role | observed | `git diff main...feature/kv-rbac -- modules/keyvault.bicep` | `b27e0f4` |
| Template compiles | structurally-validated | `az bicep build --file main.bicep`, exit 0 | `b27e0f4` |
| Access policies stop being evaluated under the RBAC model | observed | Microsoft Learn, Key Vault guidance on migrating from access policies to Azure RBAC, retrieved during the review | documentation, not the live vault |
| Reporting job reads the vault | designed | `TOPOLOGY.md` | not bound |
| Deployment identity is Contributor on the resource group | designed | `README.md` | not bound |
| Current access policies on the vault | not-verified | Live read declined | not bound |
| Effect of the deployment on the vault | not-verified | What-if declined | not bound |

### Findings

#### Principals that rely on access policies lose access at deployment

| id | severity | status | file | line |
|---|---|---|---|---|
| F1 | High | validation-hypothesis | `modules/keyvault.bicep` | 18 |

- **scenario:** The deployment switches `kv-app-prod` to the RBAC permission model. Any principal granted access by an access policy outside this template, such as the nightly reporting job described in `TOPOLOGY.md`, stops being authorized when the deployment completes.
- **impact:** The reporting job, and any other such reader, fails to read its secrets in production until someone grants a role.
- **recommendation:** List the vault's current access policies, map each principal to the narrowest Key Vault data-plane role at vault scope, and add those role assignments to this template before the switch.
- **verification:** A read-only list of access policies on `kv-app-prod`, taken by the vault owner, shows every principal covered by a role assignment in the template; the what-if shows those role assignments being created.

#### Deployment identity may lack permission to create the role assignment

| id | severity | status | file | line |
|---|---|---|---|---|
| F2 | High | validation-hypothesis | `modules/keyvault.bicep` | 34 |

- **scenario:** `README.md` documents `id-deploy-app-prod` as Contributor on `rg-app-prod`. Contributor cannot write role assignments, so the deployment would fail at the new role assignment resource with an authorization error.
- **impact:** The role assignment's `scope: kv` makes it depend on the vault, so the vault update runs first. If the role assignment then fails, the vault is already on the RBAC model and the web app has no role: production loses secret access.
- **recommendation:** The resource owner confirms the identity's roles at vault scope. If it holds only Contributor, the access owner decides on a constrained role-assignment permission for the identity, or the role assignments are created in a separate, approved step.
- **verification:** The release team's read of the identity's role assignments at the vault scope, or a what-if and validation run with the deployment identity that reports no authorization error.

### Skipped checks and limits

| Check | Why skipped or limited | Effect on the recommendation |
|---|---|---|
| What-if against `rg-app-prod` | Authorization declined | The deployment effect is unknown; the gate cannot pass |
| Read of current access policies | Authorization declined | The access-policy hypothesis can be neither confirmed nor cleared |
| Read of deployment identity roles | Authorization declined | The role-assignment permission hypothesis can be neither confirmed nor cleared |
| Pre-review and post-review helpers | Not installed on the review machine | Report checked by reading against the contract |

### Architecture and ADR status

`TOPOLOGY.md` lists the vault and its readers. No accepted ADR covers the vault's permission model, so none is contradicted. Recording this decision in an ADR is optional and does not affect the gate.

### Security, IaC, policy and identity status

- Identity: the web app moves from an access policy to Key Vault Secrets User at vault scope. That is least privilege for the web app, with a deterministic name and `principalType` set.
- Other principals: unknown (the access-policy hypothesis).
- Deployment identity permission: unknown (the role-assignment permission hypothesis).
- Purge protection and disabled public network access are unchanged.
- No policy files changed. Live policy state is not verified.

Secret handling: the parameter file carries principal IDs and no secret values. Nothing was redacted, and no secret value appears in this report.

### Tests, build and preview status

| Check | Command or source | Result | Label |
|---|---|---|---|
| Compile | `az bicep build --file main.bicep` | exit 0 | structurally-validated |
| What-if | `az deployment group what-if` at `rg-app-prod` | not run; authorization declined | not-verified |

Preview change counts: no preview.

### Operations, rollback, cost and inputs

- Observability: the vault's diagnostic settings are unchanged. A failed secret read appears in its audit logs with a 403.
- Rollback boundary: redeploying with `enableRbacAuthorization: false` restores evaluation of access policies, provided they still exist. If this deployment also clears access policies, the rollback needs them re-created, and that is the point of no return. Label: designed.
- Cost: no change.
- New required inputs: none.

### Unresolved risks and human blockers

| Item | Type | Owner | Needed to clear |
|---|---|---|---|
| Current access policies on `kv-app-prod` | open risk | application platform team (vault owner) | Read-only list shared with the reviewer |
| Deployment identity roles at vault scope | open risk | release team | Read-only list, or validation output |
| What-if at `rg-app-prod` | open risk | release team | Captured what-if at `b27e0f4` with the deployment identity |

### Recommendation

NOT_VERIFIED

The change compiles, and the web app's own access is correct. But the effect on other principals and on the deployment identity depends on live state the review was not authorized to read. This is not a finding against the author and not a deployment approval.

### Engineer handoff

- Next actor: the release team, then the vault owner.
- Actions, in order: capture a what-if for `main.bicep` at `rg-app-prod` with the deployment identity at `b27e0f4`; list the vault's current access policies; list the deployment identity's roles at the vault scope; return all three to the reviewer.
- Evidence the next actor receives: this report and the exact commands in the skipped-checks table.
- Re-review trigger: the three items above arrive, or the branch changes.
- Not done by this review: no what-if, no live read, no deployment, no role change.
