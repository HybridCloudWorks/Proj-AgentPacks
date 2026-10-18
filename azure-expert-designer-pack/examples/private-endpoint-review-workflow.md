# Worked example: reviewing a private endpoint diagram

Prompt: `review-azure-diagram.prompt.md`. Skills: `diagram-validation-and-evidence`, `drawio-core-generation`, `drawio-xml-authoring`, `azure-architecture-design`, `azure-architecture-patterns`, `azure-icons-and-visual-language`, `drawio-layout-and-composition`, `drawio-render-export-and-review`.

Fictional scenario. Names, paths and tool output are illustrative.

## Request

> Review whether `docs/architecture/payments-api.drawio` correctly shows the private endpoint, subnet, DNS and storage account. The Bicep is in `infra/main.bicep`. Don't change the diagram.

## 1. Scope

| Field | Value |
|---|---|
| Diagram | `docs/architecture/payments-api.drawio`, SHA-256 `9b1e…c40a` |
| Reference source | `infra/main.bicep` and `infra/modules/storage.bicep` at the working-tree commit |
| Focus | private connectivity: endpoint, subnet, DNS and the storage account |
| Mode | read-only |

## 2. What the source declares

| Bicep resource | Fact | Label |
|---|---|---|
| `Microsoft.Storage/storageAccounts` `stpayments` | `publicNetworkAccess: 'Disabled'` | `observed` |
| `Microsoft.Network/privateEndpoints` `pe-stpayments-blob` | in `snet-private-endpoints`; `groupIds: ['blob']` | `observed` |
| `Microsoft.Network/privateDnsZones` `privatelink.blob.core.windows.net` | linked to `vnet-payments`; a DNS zone group on the endpoint | `observed` |
| `Microsoft.Web/sites` `func-payments` | VNet integration into `snet-integration` | `observed` |
| `Microsoft.KeyVault/vaults` `kv-payments` | `publicNetworkAccess: 'Enabled'`; no private endpoint | `observed` |

## 3. Checks

**Structural.** The agent parsed the file and checked root cells, IDs, parents, edges, compression and image paths, using the `drawio-core-generation` output contract and the `drawio-xml-authoring` checklist. The file has 41 cells and unique IDs, and every reference resolves. One legacy stencil was found (F5).

**Semantic.** The agent compared the diagram with the Bicep facts above, using `azure-architecture-design` for boundaries and `azure-architecture-patterns` for the private endpoint pattern.

**Visual.** `drawio-render-export-and-review` detected Draw.io Desktop 24.7.17. The agent exported a PNG to `%TEMP%\payments-api-review.png`, outside the repository, and inspected it at 100% and at slide width.

## 4. Findings

| ID | Severity | Page and cell | Category | Finding | Evidence | Recommended fix |
|---|---|---|---|---|---|---|
| F1 | High | Page-1, `edge_internet_storage` | semantic | An edge from "Internet users" to the storage account is labeled "private endpoint". This draws a private endpoint as an inbound internet route. | Bicep disables public access, and the endpoint serves clients inside `vnet-payments`. `observed` | Remove the internet edge. Draw `func-payments` → endpoint NIC (private IP) → storage (Private Link). |
| F2 | High | Page-1, `storage_account` (parent `snet_pe`) | boundary | The storage account is parented under the private-endpoint subnet, which implies the PaaS resource lives in the subnet. | Only `pe-stpayments-blob` is in `snet-private-endpoints`. `observed` | Parent the storage account to the resource group, outside the VNet. Add an endpoint NIC cell in the subnet. |
| F3 | High | Page-1, `zone_secure` | boundary | A decorative dashed frame labeled "Private network" encloses both Storage and Key Vault, implying both are reachable only privately. | Key Vault has public access enabled and no private endpoint. `observed` | Remove the frame, or reduce it to Storage only. Label Key Vault "public endpoint enabled". |
| F4 | Medium | Page-1 | semantic | Private DNS is not shown, so a reader cannot tell how the storage name resolves to the private IP. | The zone, its VNet link and the zone group are declared. `observed` | Add a DNS zone tile with a control-plane "VNet link" edge to `vnet-payments`, and a legend note. |
| F5 | Low | Page-1, `storage_account` | icon | The storage account uses the legacy `shape=mxgraph.azure.storage_blob` stencil and the label "Storage". | Style attribute. `observed` | Use `img/lib/azure2/storage/Storage_Accounts.svg` at 48 px with the label "Storage account (blob)". |
| F6 | Low | Page-1, `edge_func_kv` | layout | The edge enters Key Vault from the right and crosses the storage label. The label "Private endpoint" is clipped at 100%. | Rendered PNG. `visually-validated` | Route orthogonally with a waypoint below the storage tile, and widen the label area. |

F1 to F3 would mislead a security reviewer, so they block using this diagram in a design review.

## 5. Close-out

The agent recomputed the SHA-256 at the end: unchanged. No file in the repository was written. The fixes are listed for the user to approve. A follow-up edit would write a corrected copy, or overwrite the file once approved.

## Completion report

Pack: azure-expert-designer.

### scope_and_inputs

- Task type and outcome: read-only review. Six findings; three block design-review use. `observed`
- Inputs: `docs/architecture/payments-api.drawio`, `infra/main.bicep` and `infra/modules/storage.bicep`. `observed`
- Approvals: none to edit. The review stayed read-only. `observed`

### source_facts

- Storage public access is disabled; the blob private endpoint is in `snet-private-endpoints`; a private DNS zone is linked with a zone group. `observed`
- Key Vault public access is enabled and it has no private endpoint. `observed`
- The diagram parents the storage account under the private-endpoint subnet and draws an internet edge labeled "private endpoint". `observed`

### assumptions_and_design_decisions

- The Bicep in the working tree is the intended state the diagram should reflect. `inferred`

### output_files

- None in the repository. `docs/architecture/payments-api.drawio` is unchanged (hash matched).
- `%TEMP%\payments-api-review.png`: review render outside the repository.

### structural_checks

- XML parses; 41 cells; unique IDs; all references resolve; uncompressed. `structurally-validated`
- One legacy `mxgraph.azure` stencil found (F5). `structurally-validated`

### visual_checks

- Rendered with Draw.io Desktop 24.7.17 and inspected at 100% and slide width. Clipping and crossing recorded as F6. `visually-validated`

### live_or_external_checks

- The deployed storage account, Key Vault and DNS configuration were not queried. Bicep shows intent, not deployed state. `not-verified`

### unresolved_risks

- Until F1 to F3 are fixed, the diagram overstates network isolation for Key Vault and misstates how storage is reached.
- Deployed settings may differ from the Bicep.

### next_safe_action

- The user approves the F1 to F6 fixes, and says whether to overwrite the file or write a corrected copy alongside it.
