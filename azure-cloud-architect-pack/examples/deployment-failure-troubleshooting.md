# Worked example: failed private endpoint deployment

Synthetic scenario. Names, IDs and messages are illustrative, and the error text is abbreviated. Prompt: `troubleshoot-azure-issue.prompt.md`.

## Request

"The invoicing data deployment failed in the prod pipeline last night. Fix it."

Supplied: the failed GitHub Actions log, the Bicep source for `data.bicep` in contoso/invoicing, and authority for read-only queries. The user signed in to Azure CLI with an account that holds Reader on `sub-invoicing-prod` and allowed the agent to run `az` read commands in that subscription. Nothing else was authorized. The service has not gone live; its production gate has not been passed.

The log's error, abbreviated:

```text
ERROR: {"code": "DeploymentFailed", "details": [{"code": "RequestDisallowedByPolicy",
"message": "Resource 'privatelink.database.windows.net' was disallowed by policy. ...
Policy assignment: 'Deny-Private-DNS-Zones' ...
scope: '/providers/Microsoft.Management/managementGroups/mg-landingzones'"}]}
```

## 1. Locate the boundary

From `azure-operations-observability-and-troubleshooting`: the deployment was accepted and started, so bootstrap, authentication and template validation passed. The failure came back from a resource request during the deployment, with a policy error code. The boundary is **deployment: policy effect on a resource write**.

## 2. Evidence

Read-only commands the agent ran within the authorized subscription:

```text
> az deployment group show -g rg-invoicing-data-prod-weu -n data-20261017.2 --query properties.provisioningState -o tsv
Failed

> az deployment operation group list -g rg-invoicing-data-prod-weu -n data-20261017.2 \
    --query "[].{resource:properties.targetResource.resourceName, type:properties.targetResource.resourceType, state:properties.provisioningState}" -o table
Resource                          Type                                 State
--------------------------------  -----------------------------------  ---------
pe-sql-invoicing-prod             Microsoft.Network/privateEndpoints   Succeeded
privatelink.database.windows.net  Microsoft.Network/privateDnsZones    Failed

> az policy assignment list --disable-scope-strict-match --query "[?name=='Deny-Private-DNS-Zones'].{scope:scope, enforcement:enforcementMode}" -o table
Scope                                                               Enforcement
------------------------------------------------------------------  -------------
/providers/Microsoft.Management/managementGroups/mg-landingzones   Default
```

## 3. Hypotheses

| ID | Hypothesis | Status | Evidence |
|---|---|---|---|
| H1 | A landing-zone policy denies private DNS zones in application subscriptions because the platform owns them centrally | Confirmed | The error names the assignment; deployment operations show the zone failed; the assignment is inherited and enforced [observed] |
| H2 | The pipeline identity lacks permissions | Rejected | The error code is `RequestDisallowedByPolicy`, not `AuthorizationFailed`, and the same identity created the private endpoint [observed] |
| H3 | A platform DeployIfNotExists policy will register the endpoint's A record in the central zone | Open | The ALZ pattern pairs this deny with a registration policy, but whether Contoso assigned one, and for which zones, is not visible with Reader on one subscription [inferred] |

## 4. Partial change and impact

The private endpoint `pe-sql-invoicing-prod` exists with no DNS zone group, so no private A record exists for the SQL server. A client in the spoke would resolve the public endpoint, which is disabled, and fail to connect. There is no customer impact, because the service is not live. Nothing needs deleting: an incremental redeployment reuses the endpoint with the same name.

## 5. Proposed fix

Not applied. The agent was authorized only to read.

1. Remove the `Microsoft.Network/privateDnsZones` resource and its VNet link from `data.bicep`, and keep the private endpoint.
2. Ask the platform team which registration pattern applies (H3):
   - (a) Their DeployIfNotExists policy creates the record. Nothing more in Bicep; a remediation task may be needed for the endpoint that already exists, and the platform team runs it.
   - (b) Workloads add a `privateDnsZoneGroups` child that references the central zone by resource ID. The pipeline identity then needs `Microsoft.Network/privateDnsZones/join/action` on that zone, granted by the platform team.
3. Redeploy through the pipeline once the change is merged.

Verification for the operator, from a host inside the spoke:

```text
nslookup sql-invoicing-prod-weu.database.windows.net
# expected: resolves through the privatelink name to an address in snet-pe (10.43.2.0/26)
az network private-endpoint dns-zone-group list -g rg-invoicing-data-prod-weu --endpoint-name pe-sql-invoicing-prod -o table
# expected for pattern (b): one zone group pointing at the central zone; for (a): the record exists in the central zone
```

## 6. Prevention

- Add `C-NET-04` to the invoicing `CONSTRAINTS.json`: private DNS zones are platform-owned, and workloads never declare them.
- Add a PR check in landing-zone workload repositories that fails when a template declares `Microsoft.Network/privateDnsZones`.
- Link the deployment-failure alert to a runbook entry for `RequestDisallowedByPolicy` that starts with "read the assignment name and scope in the error".

## Completion report

- Pack: azure-cloud-architect
- Workflow: `troubleshoot-azure-issue.prompt.md`
- Outcome: cause confirmed; fix proposed but not applied; the DNS registration path (H3) is unconfirmed, so private name resolution after the fix is not-verified.

### scope_and_inputs

Failed deployment `data-20261017.2` to `rg-invoicing-data-prod-weu`. Inputs: pipeline log and `data.bicep`. Authority: read-only `az` queries in `sub-invoicing-prod` under the user's Reader session. No changes authorized.

### business_outcomes_and_requirements

Restore a working deployment path for the invoicing data tier before its production gate; data services reachable only privately (AC-SEC-01).

### source_facts_and_evidence

Error text, deployment state, deployment operations and the inherited policy assignment [observed]. The platform's registration policy (H3) [inferred]. The join permission that pattern (b) needs was not retrieved from documentation in this session [not-verified].

### framework_alignment

Security: the central DNS model held, as intended. Operational Excellence: the workload template contradicted a platform constraint that was never written into the workload's `CONSTRAINTS.json`; prevention closes that gap. Reliability, Cost and Performance: no effect.

### proposed_architecture

No change to the architecture. The workload stops declaring private DNS zones and uses the platform's registration pattern (a) or (b) [designed].

### assumptions_and_tradeoffs

Assumed the deny assignment is intended and must not be exempted; an exemption would split DNS authority and was rejected. Pattern (a) keeps workloads simpler; pattern (b) makes the dependency explicit in code but needs a cross-subscription permission.

### implementation_and_operating_implications

Workload team: edit `data.bicep` and redeploy through the pipeline. Platform team: confirm the pattern, run any remediation task, or grant the join permission. Operator: run the verification commands after redeployment.

### security_resilience_cost_and_sustainability

No public exposure was created; the leftover endpoint is harmless and gets reused. No resilience, cost or sustainability effect.

### output_files

| File | Purpose | Status and label |
|---|---|---|
| Proposed `data.bicep` change | Remove the private DNS zone and its link | described, not written [designed] |
| CONSTRAINTS.json (invoicing handoff) | Add C-NET-04 | proposed [designed] |
| REQ.md, TOPOLOGY.json, ADR.md | Unchanged | not applicable |

### live_or_external_checks

| Check | Command | Scope | Result | Label |
|---|---|---|---|---|
| Deployment state | `az deployment group show` | rg-invoicing-data-prod-weu | Failed | live-verified |
| Failed operation | `az deployment operation group list` | same | zone failed, endpoint succeeded | live-verified |
| Policy assignment | `az policy assignment list --disable-scope-strict-match` | sub-invoicing-prod | Deny-Private-DNS-Zones, enforced | live-verified |
| Platform registration policy | not run: needs management-group read | mg-landingzones | none | not-verified |
| Name resolution from the spoke | not run: no host access | snet-pe | none | not-verified |

### unresolved_risks

If the platform has no registration policy and pattern (b) is not granted, the redeployment succeeds but private name resolution still fails.

### next_safe_action

Send the platform team the H3 question with the evidence above. Once they answer, the workload team removes the zone from `data.bicep` and redeploys through the pipeline, and the operator runs the verification commands.
