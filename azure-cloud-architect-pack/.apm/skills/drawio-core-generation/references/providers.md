# Provider Icon Libraries and Scope Rules

Facts below were verified on 2026-11-01 against draw.io 32.6.9 source, renders made with draw.io Desktop 32.6.1, and each provider's official icon page and download. The `diagram-validation-and-evidence` Skill carries a checker whose catalog records every palette entry these libraries offer, with its full style; prefer it over this summary when the two disagree, and recheck both when a provider publishes a new icon set.

In the draw.io editor the libraries are under More Shapes, in the Networking group. Each library has an ID, shown in brackets below, that also appears in shape searches and style names.

## Finding the exact style

Run the checker from the `diagram-validation-and-evidence` Skill's folder:

```text
python scripts/check_drawio.py --find "<product name>"
```

It lists the matching palette entries of the current libraries (add `--all` for legacy and retired ones) with the provider, form, palette title, palette, default size and the full style draw.io inserts. Copy the whole style. Do not read `icon_catalog.json` itself: it is about 300 KB, and the checker reads it for you.

The style is part of the icon. AWS and Google Cloud icons are stencils whose colours come from the style:

| Style | Without it (draw.io Desktop 32.6.1) |
|---|---|
| AWS service icon `fillColor` (category colour) | white symbol on white: the icon disappears |
| AWS service icon `strokeColor=#ffffff` | the symbol draws black |
| AWS resource icon `fillColor` | nothing visible |
| AWS group `strokeColor` | black frame and black corner icon |
| Google Cloud core `fillColor=#4285f4` | the blue parts are missing, for example Cloud Run's blue chevron |
| Google Cloud category `fillColor=#9aa0a6` | the grey parts are missing |

AWS, Microsoft and Google all forbid recolouring their icons. So the provider's library style wins for provider icons and provider boundary shapes; a pack's style skill sets typography, sizes, layout and the legend only, and never replaces a library colour.

## AWS

Official set: AWS Architecture Icons. AWS releases packages quarterly, at the end of January, April and July, with no fourth-quarter release. The newest package seen was dated 31 July 2026. AWS warns that third-party libraries may contain legacy icon sets.

Current draw.io library: "AWS <current year>" [aws4]. Each name exists in one form, and the forms are not interchangeable:

- Service icons: `shape=mxgraph.aws4.resourceIcon;resIcon=mxgraph.aws4.<service>` with the category colour as `fillColor` (for example `#ED7100` for Compute) and `strokeColor=#ffffff`. Default size 78 by 78.
- Resource icons: `shape=mxgraph.aws4.<resource>` with the category colour as `fillColor` and `strokeColor=none`, for example `mxgraph.aws4.instance2`.
- Groups: `shape=mxgraph.aws4.group;grIcon=mxgraph.aws4.<group>`, or `groupCenter` for Auto Scaling groups. The library's own styles are `group_aws_cloud_alt` (AWS Cloud), `group_account`, `group_region` (dashed, stroke `#00A4A6`), `group_vpc2` (stroke `#8C4FFF`), and `group_security_group` for subnets: public subnet stroke `#7AA116` on fill `#F2F6E8`, private subnet stroke `#00A4A6` on fill `#E6F6F7`. An Availability Zone is a dashed rectangle with no icon, stroke `#147EBA`.
- Every group style carries `container=1`, so a shape dropped on it becomes its child. A frame that only decorates (a legend box, a highlight) sets `container=0` explicitly.
- A service name used as a bare stencil (`shape=mxgraph.aws4.ec2`) draws the symbol without its category square, and a resource or group name inside `resourceIcon` draws a symbol on a square AWS never published. Neither is an AWS icon; the checker reports both as wrong-form.
- Recent services are present, for example Amazon Bedrock AgentCore.

Legacy draw.io libraries, avoid for new work:

- "AWS18" [aws4b]: `shape=mxgraph.aws4.productIcon;prIcon=mxgraph.aws4.<name>`, and some service and resource forms of names the current library offers differently. It shares the `mxgraph.aws4` namespace with the current library, so the namespace alone does not prove an icon is current.
- "AWS17" [aws3]: `mxgraph.aws3.*`.
- "AWS (retired)" [aws4r]: current-style names for services AWS has retired, for example Amazon Honeycode and AWS RoboMaker.
- "AWS 3D" [aws3d]: an isometric set, not AWS's official icons.

Scope: an account belongs to an organization. A VPC lives in one Region and spans that Region's Availability Zones. "Each subnet must reside entirely within one Availability Zone and cannot span zones" (Amazon VPC User Guide).

## Azure

Official set: Azure architecture icons, downloaded as `Azure_Public_Service_Icons_V24.zip`. Microsoft Foundry was added in November 2024. The newest update, July 2026, added Azure DocumentDB, Azure Resiliency, AI Gateway and Azure DDoS custom policies, and new or updated Microsoft Foundry icons such as Foundry Models, Foundry Projects and Foundry Agent Service. Microsoft's rules: include the product name close to the icon, use the icons as they appear in Azure, and don't crop, flip, rotate, distort or change their shape, or use Microsoft product icons for your own product or service.

Current draw.io library: "Azure" [azure2]. Icons are images, not stencils, so colour keys do not change them:

- Style: `image;aspect=fixed;html=1;align=center;fontSize=12;image=img/lib/azure2/<category>/<File_Name>.svg`.
- Categories: ai_machine_learning, analytics, app_services, azure_ecosystem, azure_stack, azure_vmware_solution, blockchain, compute, containers, cxp, databases, devops, general, hybrid_multicloud, identity, integration, internet_of_things, intune, iot, management_governance, menu, migrate, mixed_reality, mobile, monitor, networking, other, power_platform, preview, security, storage, web.
- draw.io 32.6.9 includes the July 2026 additions, for example `databases/Azure_DocumentDB.svg`, `other/Resiliency.svg`, `integration/AI_Gateway.svg`, `networking/DDoS_Custom_Policy.svg` and `ai_machine_learning/Foundry_Agent_Service.svg`. Microsoft Foundry itself is `ai_machine_learning/AI_Foundry.svg`.
- Scope icons: `general/Management_Groups.svg`, `general/Subscriptions.svg`, `general/Resource_Groups.svg`, `networking/Virtual_Networks.svg`, `networking/Subnet.svg`. The library has no boundary shapes, so draw a scope as a plain labelled container and place its icon in the frame's corner.

Which file to use, decided by rendering each candidate with draw.io Desktop 32.6.1 next to Microsoft's official file:

| Product | Use | Do not use | Evidence |
|---|---|---|---|
| Microsoft Entra ID | `other/Entra_Identity.svg`, labelled "Microsoft Entra ID" | `identity/Azure_Active_Directory.svg`, the pre-rename Azure Active Directory pyramid | Microsoft publishes the Entra ID icon in its separate Microsoft Entra architecture icons set (October 2023), not in Azure V24, which has only Entra sub-service icons in `identity/`. `other/Entra_Identity.svg` draws identically to "Microsoft Entra ID color icon.svg" from that set. |
| Private endpoint | `other/Private_Endpoints.svg` | `networking/Private_Endpoint.svg`, an older design | V24's only private endpoint icon is `other/...-Private-Endpoints.svg`; the `other/` file draws identically to it. |
| Private DNS zone | `networking/DNS_Zones.svg`, labelled "Private DNS zone" | | V24 has a DNS Zones icon and no separate private DNS zone icon; the draw.io file draws identically to it. |
| App Service | `app_services/App_Services.svg` | | The copies in `compute/` and `containers/` draw identically, as Microsoft ships the same file in five V24 folders; draw.io's own Mobile and Web palettes reuse the `app_services/` file. |
| Log Analytics workspace | `analytics/Log_Analytics_Workspaces.svg` | | The `management_governance/` copy draws identically; draw.io's Monitor palette reuses the `analytics/` file. |
| Local network gateway | `networking/Local_Network_Gateways.svg` | | The `other/` copy draws identically, as in V24. |

Four palette entries are spelled with different letter case from the file, and the palette spelling draws a broken image in draw.io Desktop and on app.diagrams.net. Use the file's spelling, which `--find` prints: `management_governance/Solutions.svg`, `networking/IP_Address_manager.svg`, `other/Arc_Data_services.svg`, `other/Database_Instance_For_SAP.svg`.

Legacy draw.io shapes, avoid for new work: the old Azure library `mxgraph.azure.*`, and Cloud & Enterprise `mxgraph.mscae.*` or `img/lib/mscae/`. A few `img/lib/azure2` files are no longer offered in the palette; the checker reports them as legacy.

Scope: a tenant (Microsoft Entra ID) holds management groups, subscriptions and resource groups, which are management and ownership scopes, not networks. "A virtual network is limited to a single region", and "virtual networks and subnets span all availability zones in a region" (Azure Virtual Network documentation). A zonal resource sits in a zone while its subnet does not. A PaaS service behind a private endpoint is not in the subnet: only the endpoint's network interface is. A PaaS service with regional virtual network integration also stays outside the VNet and sends traffic out through its delegated subnet.

## Google Cloud

Official set: Google's icon page says that "in early 2025, we updated our product iconography", and offers three downloads: product category icons (`category-icons.zip`), core product icons (`core-products-icons.zip`) and legacy console icons (`google-cloud-legacy-icons.zip`), with a product icon guide (PDF) explaining the change. The downloads, checked on 2026-11-01, hold:

- Exactly 19 four-colour core product icons: AI Hypercomputer, AlloyDB, Anthos, Apigee, BigQuery, Cloud Run, Cloud SQL, Spanner, Cloud Storage, Compute Engine, Google Distributed Cloud, GKE, Hyperdisk, Looker, Mandiant, Google Security Operations, Security Command Center, Google Threat Intelligence and Vertex AI.
- 26 two-colour category icons, one per product category. Every product without a core icon uses its category's icon, so the label is the only thing that tells two products apart.
- No Gemini icon in either set.

Vertex AI: Google's product documentation now titles it "Gemini Enterprise Agent Platform". Label the icon with that name (optionally "(Vertex AI)"); the official file is still named `VertexAI` and the draw.io shape is `mxgraph.gcp3.vertexai`.

Gemini has no official icon. Draw it as a labelled neutral shape and record the choice. Never borrow the Vertex AI icon or a category icon for it.

Current draw.io library: "Google Cloud Platform 2026" [gcp3], added in draw.io 30.0.4 (May 2026). Style: `shape=mxgraph.gcp3.<name>`, with `fillColor=#4285f4` for core products and `fillColor=#9aa0a6` for categories; without it the icon draws incompletely.

- Core product names, one for one with Google's core download: aihypercomputer, alloydb, anthos, apigee, bigquery, cloudrun, cloudspanner, cloudsql, cloud_storage, computeengine, distributedcloud, gke, hyperdisk, looker, mandiant, secops, securitycommandcenter, threatintelligence, vertexai.
- Category names, one for one with Google's category download: agents (AI Applications & Agents), aimachinelearning, businessintelligence, collaboration, compute, containers, dataanalytics, databases, developer_tools, devops, hybridmulticloud, integrationservices, managementtools, mapsgeospatial, marketplace, mediaservices, migration, mixedreality, networking, observability, operations, securityidentity, serverlesscomputing, storage, web3, webmobile.
- The library has no boundary shapes. Draw organization, folder, project, network, region and zone as plain labelled containers.

Category for common products, as listed in Google's product icon guide; confirm a product's category there when it matters:

| Category | Products |
|---|---|
| Data Analytics | Pub/Sub, Dataflow, Dataproc, Cloud Composer, Dataplex, Datastream |
| Databases | Firestore, Bigtable, Memorystore, Datastore, Database Migration Service |
| Serverless Computing | Cloud Functions, App Engine |
| Networking | Virtual Private Cloud, Cloud Load Balancing, Cloud CDN, Cloud DNS, Cloud NAT, Cloud VPN, Cloud Interconnect, Cloud Armor, Private Service Connect |
| Security Identity | Identity and Access Management, Secret Manager, Key Management Service, Identity-Aware Proxy, Certificate Manager |
| DevOps | Artifact Registry, Cloud Build, Cloud Deploy |
| Observability | Cloud Logging, Cloud Monitoring, Trace, Error Reporting |
| Integration Services | Eventarc, Workflows, API Gateway, Application Integration |
| Developer Tools | Cloud Scheduler, Cloud Tasks, Cloud Shell, Cloud Workstations |
| Storage | Filestore, Persistent Disk, Google Cloud NetApp Volumes |

Legacy, avoid for new work: Google's legacy console icons download, and in draw.io "Google Cloud Platform" [gcp2], the pre-2025 icons and product cards in `mxgraph.gcp2.*`, which the editor also opens for the old ID "gcp"; "GCP Icons" [gcpicons], the legacy console icons embedded as SVG data; and the oldest `mxgraph.gcp.*` shapes. The gcp2 zone colours are plain rounded rectangles and can still serve as neutral frames.

Scope: an organization holds folders and projects; a project is the ownership, billing and IAM boundary. "VPC networks, including their associated routes and firewall rules, are global resources. Subnets are regional resources" (VPC documentation). Zonal resources such as Compute Engine VMs and zonal GKE clusters sit in one zone. With Shared VPC a host project owns the network and service projects attach to it: draw each service project's resources in that project's frame, connected to the host project's network. A managed service reached by private IP, such as Cloud SQL through private services access or Private Service Connect, runs in a Google-managed network, not in the customer's subnet.

## Sources

- draw.io source, palettes and Azure images: https://github.com/jgraph/drawio (src/main/webapp/js/diagramly/sidebar and img/lib/azure2), tag v32.6.9
- AWS Architecture Icons: https://aws.amazon.com/architecture/icons/
- Azure icons: https://learn.microsoft.com/azure/architecture/icons/
- Microsoft Entra architecture icons: https://learn.microsoft.com/entra/architecture/architecture-icons
- Google Cloud icons: https://cloud.google.com/icons and the product icon guide linked there
- Gemini Enterprise Agent Platform documentation: https://docs.cloud.google.com/vertex-ai/docs
- Network scope: https://docs.aws.amazon.com/vpc/latest/userguide/configure-subnets.html, https://learn.microsoft.com/azure/virtual-network/virtual-networks-faq, https://cloud.google.com/vpc/docs/vpc
