# Worked example: architecture drift that needs a decision

Prompt: `.apm/prompts/check-architecture-alignment.prompt.md`, with `.apm/prompts/verify-handoff-readiness.prompt.md` for ownership. Outcome: `BLOCKED_ON_HUMAN_DECISION`.

Skills applied: change-scope-and-impact, architecture-and-adr-consistency, iac-policy-and-identity-review, security-secrets-and-supply-chain-review, documentation-inputs-and-repository-contracts, role-authority-and-handoff-review, review-report-and-pr-gate.

The repository, ADRs, people and resources are fictional.

## Request

> `feature/claims-reporting` adds the reporting backend product asked for. Check it against our topology and ADRs before the PR. Product already approved it.

## 1. Gather the design artifacts

The reviewer works only from the artifacts the repository holds, not from an ideal design:

- `docs/architecture/TOPOLOGY.md`: one Azure SQL database serves the claims portal, and reporting reads use its readable secondary.
- `docs/architecture/CONSTRAINTS.md`: region `eastus2` only, enforced by an allowed-locations `deny` assignment at the management group. Claims data is classified Confidential, and a new store of Confidential data needs data owner approval.
- ADR-0003, Accepted: PaaS data services are reachable only through private networking, with public network access disabled.
- ADR-0006, Accepted, decider "lead architect, claims platform": reporting reads come from the transactional database's readable secondary; there is no second data store.

"Product already approved it" is recorded as a claim. No accepted or proposed ADR in the repository supersedes ADR-0006.

## 2. What the change alters (change-scope-and-impact)

```text
$ git diff --name-status main...feature/claims-reporting
M       infra/main.bicep
A       infra/modules/reporting/postgres.bicep
M       infra/main.parameters.prod.json
A       src/reporting/repository.py
A       src/reporting/sync_job.py
M       requirements.txt
```

The diff adds a new service, an Azure Database for PostgreSQL flexible server. It adds a new data flow: `sync_job.py` copies claim rows from Azure SQL into PostgreSQL every hour. It adds a new region, because `postgres.bicep` hard-codes `location: 'westus3'`. And it adds a new network exposure:

```bicep
22    network: {
23      publicNetworkAccess: 'Enabled'
24    }
...
29  resource allowAzure 'Microsoft.DBforPostgreSQL/flexibleServers/firewallRules@2022-12-01' = {
30    parent: server
31    name: 'AllowAllAzureServices'
32    properties: { startIpAddress: '0.0.0.0', endIpAddress: '0.0.0.0' }
33  }
```

## 3. Compare with the design (architecture-and-adr-consistency)

| Change | Design artifact | Result |
|---|---|---|
| Second data store for reporting | ADR-0006 | Contradiction. The ADR is not superseded, so this needs a new or superseding ADR. |
| Public network access with the `0.0.0.0` rule | ADR-0003 | Contradiction, proven in the file |
| `westus3` | `CONSTRAINTS.md` | Contradiction with the documented region constraint |
| Copying Confidential data to a new store | `CONSTRAINTS.md` | Needs data owner approval; none recorded |

The `0.0.0.0` start and end rule permits connections from any Azure-hosted client, in any tenant, not only this subscription. That is also a security finding in its own right (security-secrets-and-supply-chain-review).

## 4. Ownership and contracts (role-authority-and-handoff-review, documentation-inputs-and-repository-contracts)

- `CODEOWNERS` has no entry for `infra/modules/reporting/`, and the server has no `owner` tag, so no owner exists for the new store.
- The administrator credential arrives as an `@secure()` parameter, fed in `main.parameters.prod.json` by a Key Vault reference to the secret `reporting-admin`. That is a reference, not a value, which is correct. `CHECKLIST.md`, however, does not list the new secret, and no runbook covers backup or restore of the new store.

## 5. Choosing the outcome

The confirmed findings are real, and the implementer could start fixing them. But whether the PostgreSQL server should exist at all is the open question, and only the ADR-0006 decider can answer it. If the decision is "use the readable secondary as ADR-0006 says", the module, the sync job and three of the findings disappear. Fixing first risks work that gets deleted. The reviewer therefore recommends `BLOCKED_ON_HUMAN_DECISION`, lists the findings so they are not lost, and routes detailed design back to the architect.

## Completion report

### Scope and inputs

| Item | Value |
|---|---|
| Repository and refs | `claims-portal`, base `main`, head `feature/claims-reporting` at `5d90a3e` |
| Change intent | Add a reporting backend fed hourly from the claims database |
| Change class | mixed: infrastructure, data, networking, application |
| Target environment | `prod`, per `infra/main.parameters.prod.json` |
| Requirements and design | `TOPOLOGY.md`, `CONSTRAINTS.md`, ADR-0003, ADR-0006 |
| Owner | Change: claims feature team. New store: none recorded. ADR-0006 decider: lead architect, claims platform. |
| Authorization boundary | Read-only review of the repository. No live read-only queries requested. No deployment, RBAC, policy or secret change. |
| Report location | `../reviews/claims-portal/claims-reporting/REVIEW.md` |

### Changed paths and methods

| Path | Change class | Review method |
|---|---|---|
| `infra/modules/reporting/postgres.bicep` (added) | infrastructure, networking | Read in full; compared network, region and tags with ADR-0003 and `CONSTRAINTS.md` |
| `infra/main.bicep`, `infra/main.parameters.prod.json` | infrastructure | Read diff; traced the module call and the secret reference |
| `src/reporting/sync_job.py`, `src/reporting/repository.py` (added) | application, data | Read in full; identified the new data flow |
| `requirements.txt` | dependency | Checked the new PostgreSQL driver pin |

Paths inspected outside the diff, and why:

- `docs/architecture/TOPOLOGY.md`, `docs/architecture/CONSTRAINTS.md`, `docs/adr/0003-*.md`, `docs/adr/0006-*.md`: the design the change is measured against.
- `CODEOWNERS`, `CHECKLIST.md`: ownership and required-input contracts.

### Evidence ledger

| Evidence | Label | Source, command or capture | Bound to |
|---|---|---|---|
| New PostgreSQL server, public access, `0.0.0.0` rule, `westus3` | observed | `infra/modules/reporting/postgres.bicep` | `5d90a3e` |
| Hourly copy of claim rows into the new store | observed | `src/reporting/sync_job.py` | `5d90a3e` |
| ADR-0003 and ADR-0006 are Accepted and not superseded | observed | `docs/adr/` | `5d90a3e` |
| Allowed-locations `deny` assignment at the management group | designed | `CONSTRAINTS.md` | not bound |
| Product approval of the new store | not-verified | Stated by the requester; no record | not bound |
| Live policy assignments | not-verified | No live read requested | not bound |

### Findings

#### Second data store implemented without an accepted ADR

| id | severity | status | file | line |
|---|---|---|---|---|
| F1 | High | human-blocker | `infra/main.bicep` | 57 |

- **scenario:** The module call adds a PostgreSQL server and an hourly copy of claim data, contradicting Accepted ADR-0006 (reporting from the readable secondary, no second store). No superseding ADR exists.
- **impact:** The topology, cost, security boundary and data classification change without the decision owner's acceptance. Every other finding depends on whether the store stays.
- **recommendation:** The ADR-0006 decider either accepts a superseding ADR that covers the store, its network model, region, owner and data classification, or rejects it, in which case the module and sync job are removed.
- **verification:** A superseding ADR with status Accepted is linked in the pull request, or the module and the sync job are absent from the diff.

#### Reporting database is publicly reachable from any Azure-hosted client

| id | severity | status | file | line |
|---|---|---|---|---|
| F2 | High | confirmed | `infra/modules/reporting/postgres.bicep` | 23 |

- **scenario:** `publicNetworkAccess` is `Enabled`, and the `AllowAllAzureServices` rule at lines 29 to 33 sets start and end to `0.0.0.0`, which admits connections from any Azure-hosted client in any tenant.
- **impact:** Confidential claim data sits behind a single administrator credential on a reachable endpoint, contradicting ADR-0003.
- **recommendation:** If the store survives the decision, use private networking as ADR-0003 requires, either private access in a delegated subnet or a private endpoint, set `publicNetworkAccess` to `Disabled`, and remove the firewall rule.
- **verification:** The template shows public access disabled and no firewall rules; a what-if at the target scope shows no public endpoint configuration.

#### Server is placed in a region the constraints do not allow

| id | severity | status | file | line |
|---|---|---|---|---|
| F3 | Medium | confirmed | `infra/modules/reporting/postgres.bicep` | 12 |

- **scenario:** `location` is hard-coded to `westus3`. `CONSTRAINTS.md` allows `eastus2` only and documents a `deny` assignment for other regions.
- **impact:** If the assignment is in place as documented, the deployment is denied. If it is not, Confidential data leaves the approved region.
- **recommendation:** Take `location` from a parameter that defaults to `resourceGroup().location`.
- **verification:** The template has no literal region, and the prod parameter file resolves to `eastus2`.

#### New secret input and recovery notes are missing from the repository contracts

| id | severity | status | file | line |
|---|---|---|---|---|
| F4 | Medium | confirmed | `CHECKLIST.md` | 22 |

- **scenario:** The deployment needs the Key Vault secret `reporting-admin` to exist before it runs. `CHECKLIST.md` does not list it, and no runbook covers backup or restore of the new server.
- **impact:** The first deployment fails on the missing secret reference, and nobody knows how to recover the store after an incident.
- **recommendation:** If the store survives the decision, add the secret by name and reference to `CHECKLIST.md`, and add a runbook covering backup retention, point-in-time restore and the resync procedure.
- **verification:** `CHECKLIST.md` lists the secret reference, and the runbook exists and names an owner.

### Skipped checks and limits

| Check | Why skipped or limited | Effect on the recommendation |
|---|---|---|
| What-if and build of `infra/` | Deferred until the decision; the module may be removed | Deployment evidence not gathered |
| Code review of `src/reporting/` beyond the data flow | Deferred until the decision | Defects in the sync job not assessed |
| Live policy assignments | No live read requested | The region-denial impact is conditional |
| Pre-review and post-review helpers | Not installed on the review machine | Report checked by reading against the contract |

### Architecture and ADR status

- ADR-0006: contradicted by the second data store; needs a superseding ADR or removal (the human-blocker finding).
- ADR-0003: contradicted by public network access (the High network finding).
- `CONSTRAINTS.md`: contradicted by the region; the data-classification approval is missing.
- Detailed design of a reporting store, if accepted, is routed to the claims platform architect.

### Security, IaC, policy and identity status

- Public network exposure of a Confidential data store (the High network finding).
- The administrator credential is a Key Vault reference through an `@secure()` parameter, which is correct handling.
- No RBAC or policy files changed. The region constraint relies on a documented `deny` assignment whose live state is not verified.
- New dependency: a PostgreSQL driver pinned to an exact version.

Secret handling: the parameter file and the module carry a secret reference, not a value. Nothing was redacted, and no secret value appears in this report.

### Tests, build and preview status

| Check | Command or source | Result | Label |
|---|---|---|---|
| Unit tests | not run; deferred | not run | not-verified |
| Bicep build | not run; deferred | not run | not-verified |
| What-if | none captured | not run | not-verified |

Preview change counts: no preview.

### Operations, rollback, cost and inputs

- Observability and ownership: no diagnostic settings, owner tag or `CODEOWNERS` entry for the new store.
- Rollback boundary: once the first sync copies claim data, removing the server no longer undoes the exposure. Copied data must be treated as having existed in the new store. Label: designed.
- Cost: no estimate supplied for the new server; required before deployment review.
- New required inputs: Key Vault secret reference `reporting-admin` (name only).

### Unresolved risks and human blockers

| Item | Type | Owner | Needed to clear |
|---|---|---|---|
| Superseding ADR or rejection of the second store | human blocker | lead architect, claims platform | Recorded decision |
| Approval to copy Confidential claim data to a new store | human blocker | claims data owner | Recorded approval, or rejection |
| Owner of the new store | human blocker | claims platform lead | `CODEOWNERS` entry and `owner` tag |
| Product approval cited by the requester | open risk | requester | Link to the record |

### Recommendation

BLOCKED_ON_HUMAN_DECISION

The change contradicts two accepted ADRs and a documented constraint. Whether the new store should exist is a decision for the ADR-0006 decider and the data owner, and it determines whether the confirmed findings are fixed or deleted.

### Engineer handoff

- Next actor: the lead architect, claims platform, with the claims data owner.
- Actions, in order: decide on the second data store and record it as a superseding ADR or a rejection; record the data owner's decision; name an owner. Then the change author either removes the module and sync job, or fixes the network exposure, the region and the missing contracts.
- Evidence the next actor receives: this report; its architecture and ADR status section is the design comparison.
- Re-review trigger: an ADR decision is recorded, or the branch changes.
- Not done by this review: no code review of the sync job beyond its data flow, no build, no what-if, no deployment.
