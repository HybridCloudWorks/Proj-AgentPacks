# Worked example: CI and supply-chain security gate

Prompt: `.apm/prompts/review-security-and-supply-chain.prompt.md`. Outcome: `CHANGES_REQUIRED`.

Skills applied: cloud-prepress-orchestration, change-scope-and-impact, security-secrets-and-supply-chain-review, iac-policy-and-identity-review, role-authority-and-handoff-review, tests-build-and-dependency-review, review-report-and-pr-gate.

The repository, organization, action, identities and values are fictional.

## Request

> `feature/pr-previews` deploys a preview Container App for every PR, including PRs from forks. Run the security gate on it.

## 1. Scope and trust model

- Target: `web-frontend`, a public repository that accepts pull requests from forks. Head `feature/pr-previews` at `e4a19c2`, base `main`.
- Trust model, from `SECURITY.md`: fork contributors are untrusted. Third-party actions are pinned to a full commit SHA, while GitHub-owned actions may use major-version tags. Deployment identities are used only from jobs bound to a protected environment.
- Authorization: read-only. No workflow runs, no Azure access, no secret testing.

```text
$ git diff --name-status main...feature/pr-previews
A       .github/workflows/deploy-preview.yml
A       scripts/deploy-preview.sh
A       infra/identity.bicep
A       infra/preview.parameters.json
M       package.json
M       package-lock.json
```

change-scope-and-impact lists the trust-boundary changes: a new trigger that runs with the base repository's privileges, a new federated identity, a new role assignment, and a new third-party action.

## 2. The workflow (security-secrets-and-supply-chain-review)

```yaml
 1  name: deploy-preview
 2  on:
 3    pull_request_target:
 4      types: [opened, synchronize]
 5  permissions:
 6    id-token: write
 7    contents: read
 8    pull-requests: write
 9  jobs:
10    preview:
11      runs-on: ubuntu-latest
12      steps:
13        - uses: actions/checkout@v4
14          with:
15            ref: ${{ github.event.pull_request.head.sha }}
16        - uses: actions/setup-node@v4
17          with:
18            node-version: 20
19        - run: npm ci && npm run build
20        - uses: azure/login@v2
21          with:
22            client-id: ${{ vars.PREVIEW_CLIENT_ID }}
23            tenant-id: ${{ vars.AZURE_TENANT_ID }}
24            subscription-id: ${{ vars.PREVIEW_SUBSCRIPTION_ID }}
25        - id: deploy
26          run: ./scripts/deploy-preview.sh "${{ github.event.pull_request.number }}"
27        - uses: example-labs/preview-comment@v2
28          with:
29            url: ${{ steps.deploy.outputs.url }}
```

The reviewer traces the exploit path rather than pattern-matching the trigger name:

1. `pull_request_target` runs in the base repository's context, so the job gets `id-token: write` even for a fork pull request.
2. Line 15 checks out the fork's head commit.
3. Line 19 runs `npm ci`, which executes the fork's install scripts, and `npm run build`, which runs the fork's build script. Line 26 runs the fork's own `scripts/deploy-preview.sh` after Azure login.
4. With `id-token: write`, any step can request an OIDC token. Fork code can therefore act as the preview identity, either directly or through the logged-in CLI session.
5. The CI run on same-repository pull request #212 logged a successful Azure login, so the federated credential matches this event.

The path is complete and needs no assumption: it is a confirmed Critical.

The interpolation on line 26 inserts the pull request number, an integer, so it is not an injection vector. If it inserted the title or the branch name, it would be.

## 3. Identity and secrets (iac-policy-and-identity-review)

`infra/identity.bicep` creates a user-assigned identity, a federated credential bound to the pull-request subject, and this role assignment:

```bicep
27  properties: {
28    roleDefinitionId: subscriptionResourceId('Microsoft.Authorization/roleDefinitions', contributorRoleId)
29    principalId: previewIdentity.properties.principalId
30    principalType: 'ServicePrincipal'
31  }
```

The scope is `rg-web-preview`. The preview deployment updates one Container App, so Contributor on the whole resource group is broader than the operation needs.

`infra/preview.parameters.json` line 9 holds a literal in the shape of a registry credential:

```json
"registryPassword": { "value": "[REDACTED_POSSIBLE_SECRET]" }
```

The reviewer redacts the value, does not copy it into notes, and does not try it against the registry. This is static secret-pattern evidence, not a confirmed compromise. But the branch has been pushed to a public repository, so the value is readable by anyone and stays in history after deletion. That evidence supports a rotation recommendation, and the decision belongs to the registry credential owner.

## 4. Pinning and dependencies (tests-build-and-dependency-review)

`example-labs/preview-comment@v2` is a third-party action on a mutable tag, running in a job that holds the deployment identity. `SECURITY.md` requires a SHA. `package-lock.json` changes only by a patch bump of `@azure/identity`, resolved from the public registry with an integrity hash, so there is no finding.

## 5. Role drift (role-authority-and-handoff-review)

Before this change, deployment identities were used only from environment-bound jobs. The new job has no `environment:`, so it deploys with no reviewer gate. That is the role drift `SECURITY.md` forbids. It is covered by the Critical finding's recommendation rather than reported twice.

## Completion report

### Scope and inputs

| Item | Value |
|---|---|
| Repository and refs | `web-frontend` (public, accepts fork pull requests), base `main`, head `feature/pr-previews` at `e4a19c2` |
| Change intent | Deploy a preview Container App for every pull request, including forks |
| Change class | CI/CD, identity, infrastructure |
| Target environment | Preview, resource group `rg-web-preview` |
| Requirements and design | `SECURITY.md` trust model and pinning rules |
| Owner | Change: web team. Preview identity and registry: platform team. |
| Authorization boundary | Read-only review. No workflow runs, no Azure access, no secret testing, no pull request comments. |
| Report location | `../reviews/web-frontend/pr-previews/REVIEW.md` |

### Changed paths and methods

| Path | Change class | Review method |
|---|---|---|
| `.github/workflows/deploy-preview.yml` (added) | CI/CD | Read in full; traced the fork-to-identity path |
| `scripts/deploy-preview.sh` (added) | CI/CD | Read; confirmed it runs from the fork checkout |
| `infra/identity.bicep` (added) | identity | Read; checked principal, role and scope |
| `infra/preview.parameters.json` (added) | infrastructure | Read; one value redacted |
| `package.json`, `package-lock.json` | dependency | Checked the version change, source and integrity |

Paths inspected outside the diff, and why:

- `SECURITY.md`: the repository's trust model and pinning rule.

### Evidence ledger

| Evidence | Label | Source, command or capture | Bound to |
|---|---|---|---|
| Privileged trigger checks out and runs fork code | observed | `.github/workflows/deploy-preview.yml` | `e4a19c2` |
| Federated credential accepted for pull request events | observed | CI run log for pull request #212, successful Azure login | `e4a19c2` |
| Contributor at resource group scope | observed | `infra/identity.bicep` | `e4a19c2` |
| Literal credential-shaped value | observed | `infra/preview.parameters.json`, value redacted | `e4a19c2` |
| Whether the value is a live credential | not-verified | Not tested, by rule | not bound |
| Live role assignments and federated credentials | not-verified | No Azure access | not bound |

### Findings

#### Fork pull requests run arbitrary code with the deployment identity

| id | severity | status | file | line |
|---|---|---|---|---|
| F1 | Critical | confirmed | `.github/workflows/deploy-preview.yml` | 15 |

- **scenario:** A fork contributor opens a pull request whose `package.json` install script, build script or `scripts/deploy-preview.sh` requests an OIDC token or uses the logged-in session. `pull_request_target` grants `id-token: write`, and line 15 checks out the fork's code, which lines 19 and 26 execute.
- **impact:** Any external contributor can act with Contributor on `rg-web-preview`: deploying arbitrary images, reading app configuration, or deleting resources. No environment gate stands in the way.
- **recommendation:** Build fork code under `pull_request` with no secrets and no `id-token`, and upload only the build output. Deploy from a separate workflow, triggered by `workflow_run`, that never checks out or runs pull request code, treats the downloaded build output as untrusted data, uses a job bound to a `preview` environment with required reviewers, and binds the federated credential to the subject `repo:example-org/web-frontend:environment:preview`.
- **verification:** No workflow combines `pull_request_target` or `workflow_run` with a checkout of pull request code. The federated credential subject names the environment. A fork pull request's run shows no Azure login without an environment approval.

#### Credential-shaped literal committed to a public repository

| id | severity | status | file | line |
|---|---|---|---|---|
| F2 | High | confirmed | `infra/preview.parameters.json` | 9 |

- **scenario:** The `registryPassword` parameter holds a literal value, shown here as `[REDACTED_POSSIBLE_SECRET]`. The branch is public, so the value is readable now and remains in history after deletion.
- **impact:** If the value is a live registry credential, anyone can push or pull images in the preview registry.
- **recommendation:** Remove the parameter. Pull images with the Container App's managed identity and the AcrPull role instead of a registry credential. The registry credential owner decides on rotation; the public exposure supports rotating.
- **verification:** No credential parameter remains in `infra/`. The Container App's registry configuration names the managed identity. The credential owner records the rotation decision.

#### Third-party action on a mutable tag in a privileged job

| id | severity | status | file | line |
|---|---|---|---|---|
| F3 | Medium | confirmed | `.github/workflows/deploy-preview.yml` | 27 |

- **scenario:** `example-labs/preview-comment@v2` resolves to whatever commit the tag points at when the job runs. The job holds `id-token: write` and `pull-requests: write`.
- **impact:** A compromised or retagged action receives the job's identity and token permissions. This breaks the `SECURITY.md` pinning rule.
- **recommendation:** Pin to a full commit SHA, with the version in a comment. Move the comment step to a job without `id-token`.
- **verification:** The `uses:` line carries a 40-character SHA, and the job that runs it has no `id-token` permission.

#### Preview identity holds Contributor on the whole resource group

| id | severity | status | file | line |
|---|---|---|---|---|
| F4 | Medium | confirmed | `infra/identity.bicep` | 28 |

- **scenario:** The preview deployment updates one Container App, but the role assignment grants Contributor at `rg-web-preview`.
- **impact:** Any misuse of the identity reaches every resource in the group, not just the preview app.
- **recommendation:** Scope the assignment to the preview Container App resource.
- **verification:** The role assignment's `scope` is the Container App, and a preview deployment still succeeds.

### Skipped checks and limits

| Check | Why skipped or limited | Effect on the recommendation |
|---|---|---|
| Testing the redacted value | Prohibited: secrets are never validated externally | Compromise unconfirmed; rotation left to the owner |
| Live federated credential and role assignment read | No Azure access authorized | Bicep source reviewed, live state not verified |
| Workflow execution | Read-only review | Exploit path traced statically and confirmed by the logged login on pull request #212 |
| Pre-review and post-review helpers | Not installed on the review machine | Report checked by reading against the contract |

### Architecture and ADR status

No ADR covers preview environments. The `SECURITY.md` trust model is the governing contract, and the change contradicts it on environment gating and pinning.

### Security, IaC, policy and identity status

- Trust boundary: fork code crosses into the base repository's privileged context (the Critical finding).
- Identity: federated credential bound to the pull-request subject rather than an environment; Contributor broader than needed (the Medium scope finding).
- Supply chain: one third-party action unpinned. The lock file change is a patch bump with integrity hashes.
- Policy: no policy files changed.

Secret handling: one possible secret found in `infra/preview.parameters.json` and redacted as `[REDACTED_POSSIBLE_SECRET]`. It was not copied, echoed or tested. No secret value appears in this report.

### Tests, build and preview status

| Check | Command or source | Result | Label |
|---|---|---|---|
| Workflow lint | none defined in the repository | not run | not-verified |
| Bicep build | not run; findings change the template | not run | not-verified |
| Dependency integrity | `package-lock.json` read | integrity hashes present | observed |

Preview change counts: no preview.

### Operations, rollback, cost and inputs

- Observability: preview deployments carry no environment record, so there is no audit trail of who approved what.
- Rollback boundary: disabling the workflow stops new exposure, but it does not undo use of the identity or exposure of the credential. Label: designed.
- Cost: an unbounded number of fork-triggered previews is also a cost risk. Previews need a cleanup on pull request close.
- New required inputs: repository variables `PREVIEW_CLIENT_ID`, `AZURE_TENANT_ID` and `PREVIEW_SUBSCRIPTION_ID`, which are identifiers, not secrets.

### Unresolved risks and human blockers

| Item | Type | Owner | Needed to clear |
|---|---|---|---|
| Rotation of the exposed registry credential | human blocker | platform team, registry credential owner | Recorded rotation decision |
| Whether fork pull requests get previews at all | open risk | web team maintainers | Decision recorded in `SECURITY.md` |

The rotation decision runs in parallel with the fixes and does not block the implementer.

### Recommendation

CHANGES_REQUIRED

A confirmed Critical path lets any fork contributor act as the deployment identity, and a credential-shaped value sits in a public branch. The change must not merge in this form.

### Engineer handoff

- Next actor: the change author, with the platform team for the credential.
- Actions, in order: split build and deploy as the Critical finding describes and bind the identity to a protected environment; remove the credential parameter in favor of managed identity pulls; pin the comment action; narrow the role scope. In parallel, the credential owner decides on rotation.
- Evidence the next actor receives: this report.
- Re-review trigger: any new commit to `.github/workflows/`, `infra/` or `scripts/` on the branch.
- Not done by this review: no workflow run, no Azure access, no secret validation, no pull request comment.
