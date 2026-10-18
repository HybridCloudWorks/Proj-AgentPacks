# Worked example: AKS platform diagram derived from Terraform

Prompt: `derive-diagram-from-infrastructure.prompt.md`. Skills: `azure-architecture-design`, `azure-architecture-patterns`, `drawio-core-generation`, `azure-icons-and-visual-language`, `drawio-layout-and-composition`, `drawio-xml-authoring`, `diagram-validation-and-evidence`.

Fictional scenario. Names, paths and tool output are illustrative. The outcome is partly unverified: the diagram is structurally valid, but there was no renderer and no live evidence.

## Request

> Derive the production architecture diagram from `infra/terraform` in the orders repository. Label what is observed and what is inferred.

## 1. Brief and constraints

| Field | Value |
|---|---|
| Task type | reconstruction |
| Source of truth | `infra/terraform` and `k8s/orders-api` at commit `4f2c9e1` |
| Environment | production |
| Output | `docs/architecture/orders-platform.drawio` and `docs/architecture/orders-platform.md` |

`backend.tf` configures an `azurerm` remote state backend through `-backend-config`. The agent did not run `terraform init` or `terraform graph`: both would contact the backend and the provider registry, and the user had not approved credentials or network use. It used a controlled extraction from the files instead.

Only `envs/dev.tfvars` is in the repository. The production variable file lives in a configuration repository that was not supplied.

## 2. Source inventory

`azure-architecture-design` in source-derived mode inventoried the files before any drawing.

| File | Declared | Notes |
|---|---|---|
| `network.tf` | `azurerm_virtual_network.hub`, `azurerm_virtual_network.spoke`, `azurerm_subnet.aks_nodes`, `azurerm_subnet.private_endpoints`, `azurerm_virtual_network_peering.hub_to_spoke`, `azurerm_virtual_network_peering.spoke_to_hub` | Address spaces come from `var.hub_cidr` and `var.spoke_cidr`. `dns_servers` is not set on the spoke. |
| `aks.tf` | `azurerm_kubernetes_cluster.main`, `azurerm_kubernetes_cluster_node_pool.user` | `default_node_pool.vnet_subnet_id = azurerm_subnet.aks_nodes.id`; `network_policy = "azure"`; `oidc_issuer_enabled` and `workload_identity_enabled` are `true` |
| `registry.tf` | `azurerm_container_registry.main`, `azurerm_role_assignment.aks_acr_pull` | AcrPull is granted to the kubelet identity. No private endpoint; `public_network_access_enabled` is not set. |
| `data.tf` | `azurerm_key_vault.app`, `azurerm_private_endpoint.kv`, `azurerm_private_dns_zone.kv`, `azurerm_private_dns_zone_virtual_network_link.kv_hub` | The endpoint is in `azurerm_subnet.private_endpoints`. The zone is `privatelink.vaultcore.azure.net`, linked to the **hub** VNet only. |
| `identity.tf` | `azurerm_user_assigned_identity.orders_api`, `azurerm_federated_identity_credential.orders_api`, `azurerm_role_assignment.orders_api_kv` | Subject is `system:serviceaccount:orders:orders-api`; the role is Key Vault Secrets User |
| `variables.tf` | `location`, `hub_cidr`, `spoke_cidr` | No defaults |
| `k8s/orders-api/*.yaml` | Deployment, Service, ServiceAccount `orders-api`, Ingress with `ingressClassName: nginx` | The ServiceAccount carries the workload identity client ID annotation |

Unknown values preserved on the diagram:

- Region: shown as `var.location (production value not in repository)`.
- Address spaces: shown as `var.hub_cidr` and `var.spoke_cidr`.
- Ingress controller: the `nginx` class is used, but nothing in this repository deploys a controller.

## 3. Evidence matrix

| Relationship | Evidence | Label |
|---|---|---|
| AKS system node pool in `aks_nodes` subnet | `vnet_subnet_id` reference | `observed` |
| Key Vault private endpoint NIC in `private_endpoints` subnet | `azurerm_private_endpoint.kv.subnet_id` | `observed` |
| Private DNS zone linked to hub VNet | `azurerm_private_dns_zone_virtual_network_link.kv_hub` | `observed` |
| Hub and spoke peered in both directions | two peering resources | `observed` |
| orders-api pods use the user-assigned identity through workload identity | federated credential subject matches the ServiceAccount in `k8s/orders-api` | `inferred` |
| orders-api reads secrets from Key Vault | role assignment exists; the application code was not traced | `inferred` |
| Kubelet pulls images from ACR over its public endpoint | AcrPull assignment; no private endpoint; public access left at its default | `inferred` |
| User node pool placement | `azurerm_kubernetes_cluster_node_pool.user` has no `vnet_subnet_id` | unresolved |
| Pods resolve the Key Vault private endpoint | zone linked to hub only; spoke uses Azure-provided DNS | unresolved |

The existence of the DNS zone does not prove that the spoke resolves it. With no `dns_servers` on the spoke and no link to it, pods in the spoke would resolve the Key Vault name through Azure-provided DNS, unless a link or DNS forwarding exists outside this repository. The diagram shows the link exactly as declared, adds a numbered note, and lists the gap as a risk. It does not draw a resolution path that the source does not support.

## 4. Pattern and drawing

`azure-architecture-patterns` applied the AKS and VNet-with-private-endpoint checks:

- The AKS control plane is drawn outside the VNet, labeled "AKS control plane (Azure-managed)".
- Node pools are drawn inside the `aks_nodes` subnet. The user pool carries a "subnet not declared" badge.
- Workload identity is drawn as a control-plane edge from the federated credential to the user-assigned identity.
- orders-api is one workload tile. Services, Deployments and the ServiceAccount are not drawn as Azure resources.
- The NGINX ingress controller is a neutral shape labeled "NGINX ingress controller (deployment not in repository)". It is not an Azure product, so no Azure icon is used.

`drawio-core-generation` chose native XML. Per its upstream routing reference, a Terraform importer was not run, because its input would require `terraform init`. `drawio-xml-authoring` derived IDs from resource addresses, for example `azurerm_kubernetes_cluster.main` became `aks_main` and `azurerm_private_endpoint.kv` became `pe_kv`, so a later regeneration diffs cleanly.

`drawio-layout-and-composition` placed the hub on the left and the spoke on the right, with ACR and Key Vault outside both VNets. Eleven primary elements got numbered badges and a legend.

## 5. Validation

The XML was parsed and checked after the write. Draw.io Desktop was not on PATH, and was not found at `C:\Program Files\draw.io\draw.io.exe` or in the user installation directory. Rendering was not run.

## Completion report

Pack: azure-expert-designer.

### scope_and_inputs

- Task type and outcome: reconstruction. The diagram was written; visual and live checks were not run. `observed`
- Inputs: `infra/terraform` and `k8s/orders-api` at commit `4f2c9e1`. `observed`
- Approvals: none for credentials, remote state or network access. `observed`

### source_facts

- Hub-spoke VNets peered both ways; AKS system pool in `aks_nodes`; Key Vault private endpoint in `private_endpoints`. `observed`
- Private DNS zone `privatelink.vaultcore.azure.net` linked to the hub VNet only; spoke has no custom DNS servers. `observed`
- AKS has OIDC issuer and workload identity enabled; a federated credential targets `orders:orders-api`. `observed`
- ACR has no private endpoint and no explicit public access setting. `observed`

### assumptions_and_design_decisions

- orders-api uses the user-assigned identity and reads secrets from Key Vault. `inferred`
- Image pulls go over the ACR public endpoint, because the provider default leaves public access enabled. `inferred`
- Region and address spaces are shown as variable names, because the production values were not supplied. `designed`

### output_files

- `docs/architecture/orders-platform.drawio`: new, uncompressed, one page.
- `docs/architecture/orders-platform.md`: companion report with the source inventory and evidence matrix.

### structural_checks

- XML parses; root cells present; unique IDs; all parents, sources and targets resolve; uncompressed; Azure2 image paths only, plus neutral shapes. `structurally-validated`

### visual_checks

- Draw.io Desktop was not found, so no render was opened or inspected. `not-verified`

### live_or_external_checks

- Remote Terraform state, the live cluster and live Azure resources were not read. `not-verified`

### unresolved_risks

- Pods in the spoke may not resolve the Key Vault private endpoint unless DNS is configured outside this repository.
- The user node pool's subnet is not declared, so its placement is unknown.
- ACR exposure depends on the live public network access setting.
- The ingress controller's source, version and exposure are unknown.
- Production region and address spaces are unknown.

### next_safe_action

- Supply the production variable file, or approve a read-only `az network vnet show` and `az acr show` against the production subscription. Then open the diagram in Draw.io Desktop for the visual check.
