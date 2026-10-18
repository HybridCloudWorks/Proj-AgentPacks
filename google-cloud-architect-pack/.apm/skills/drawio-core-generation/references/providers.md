# Provider Icon Libraries and Scope Rules

Facts below were verified on 2026-10-18 against draw.io 32.5.5 source and each provider's official icon page. The `diagram-validation-and-evidence` Skill carries a checker whose catalog lists every icon name these libraries offer; prefer it over this summary when the two disagree, and recheck both when a provider publishes a new icon set.

In the draw.io editor the libraries are under More Shapes, in the Networking group. Each library has an ID, shown in brackets below, that also appears in shape searches and style names.

## AWS

Official set: AWS Architecture Icons. AWS releases packages quarterly, at the end of January, April and July, with no fourth-quarter release. The newest package seen was dated 31 July 2026. AWS warns that third-party libraries may contain legacy icon sets.

Current draw.io library: "AWS <current year>" [aws4].

- Service icons: `shape=mxgraph.aws4.resourceIcon;resIcon=mxgraph.aws4.<service>` with the category colour as `fillColor`, for example `#ED7100` for Compute. The library's default size is 78 by 78.
- Resource icons: `shape=mxgraph.aws4.<resource>`, for example `mxgraph.aws4.instance2`.
- Groups: `shape=mxgraph.aws4.group;grIcon=mxgraph.aws4.<group>`. The library's own styles are `group_aws_cloud_alt` (AWS Cloud), `group_account`, `group_region` (dashed, stroke `#00A4A6`), `group_vpc2` (stroke `#8C4FFF`), and `group_security_group` for subnets: public subnet stroke `#7AA116` on fill `#F2F6E8`, private subnet stroke `#00A4A6` on fill `#E6F6F7`. An Availability Zone is a dashed rectangle with no icon, stroke `#147EBA`. Take these styles from the library rather than retyping them.
- Recent services are present, for example Amazon Bedrock AgentCore.

Legacy draw.io libraries, avoid for new work:

- "AWS18" [aws4b]: `shape=mxgraph.aws4.productIcon;prIcon=mxgraph.aws4.<name>`. It shares the `mxgraph.aws4` namespace with the current library, so the namespace alone does not prove an icon is current.
- "AWS17" [aws3]: `mxgraph.aws3.*`.
- "AWS (retired)" [aws4r]: current-style names for services AWS has retired, for example Amazon Honeycode and AWS RoboMaker.
- "AWS 3D" [aws3d]: an isometric set, not AWS's official icons.

Scope: an account belongs to an organization. A VPC lives in one Region and spans that Region's Availability Zones. "Each subnet must reside entirely within one Availability Zone and cannot span zones" (Amazon VPC User Guide).

## Azure

Official set: Azure architecture icons, downloaded as `Azure_Public_Service_Icons_V24.zip`. The newest update was July 2026, which added Azure DocumentDB, Azure Resiliency, AI Gateway and new Microsoft Foundry icons. Microsoft's rules: include the product name close to the icon, use the icons as they appear in Azure, and don't crop, flip, rotate, distort or change their shape, or use Microsoft product icons for your own product or service.

Current draw.io library: "Azure" [azure2]. Icons are images, not stencils:

- Style: `image;aspect=fixed;html=1;align=center;fontSize=12;image=img/lib/azure2/<category>/<File_Name>.svg`.
- Categories: ai_machine_learning, analytics, app_services, azure_ecosystem, azure_stack, azure_vmware_solution, blockchain, compute, containers, cxp, databases, devops, general, hybrid_multicloud, identity, integration, intune, iot, management_governance, menu, migrate, mixed_reality, mobile, monitor, networking, other, power_platform, preview, security, storage, web.
- draw.io 32.5.5 includes the July 2026 additions, for example `databases/Azure_DocumentDB.svg` and `ai_machine_learning/AI_Foundry.svg`.
- Scope icons: `general/Management_Groups.svg`, `general/Subscriptions.svg`, `general/Resource_Groups.svg`, `networking/Virtual_Networks.svg`, `networking/Subnet.svg`. The library has no boundary shapes, so draw a scope as a plain labelled container and place its icon in the frame's corner.

Legacy draw.io shapes, avoid for new work: the old Azure library `mxgraph.azure.*`, and Cloud & Enterprise `mxgraph.mscae.*` or `img/lib/mscae/`. A few `img/lib/azure2` files are no longer offered in the palette; the checker reports them as legacy.

Scope: a tenant (Microsoft Entra ID) holds management groups, subscriptions and resource groups, which are management and ownership scopes, not networks. "A virtual network is limited to a single region", and "virtual networks and subnets span all availability zones in a region" (Azure Virtual Network documentation). A zonal resource sits in a zone while its subnet does not.

## Google Cloud

Official set: in early 2025 Google replaced more than 250 product icons with about 40. Google's product icon guide, updated May 2026, defines two kinds:

- Unique four-colour icons for core products: AI Hypercomputer, AlloyDB, Anthos, Apigee, BigQuery, Cloud Run, Cloud SQL, Cloud Storage, Compute Engine, Gemini, GKE, Google Distributed Cloud, Mandiant, Security Command Center, Google Security Operations, Google Threat Intelligence, Spanner, Looker, Hyperdisk.
- Two-colour category icons for every other product. Each product belongs to exactly one category, so the label is the only thing that tells two products apart.

Google states that the legacy console icons "should not be used as of 2026."

Current draw.io library: "Google Cloud Platform 2026" [gcp3], added in draw.io 30.0.4 (May 2026). Style: `shape=mxgraph.gcp3.<name>`.

- Core product names: aihypercomputer, alloydb, anthos, apigee, bigquery, cloudrun, cloudspanner, cloudsql, cloud_storage, computeengine, distributedcloud, gke, hyperdisk, looker, mandiant, secops, securitycommandcenter, threatintelligence, vertexai.
- Category names: agents (AI Applications & Agents), aimachinelearning, businessintelligence, collaboration, compute, containers, dataanalytics, databases, developer_tools, devops, hybridmulticloud, integrationservices, managementtools, mapsgeospatial, marketplace, mediaservices, migration, mixedreality, networking, observability, operations, securityidentity, serverlesscomputing, storage, web3, webmobile.
- The two lists differ. draw.io ships a Vertex AI icon that Google's list does not name as a core product, and no Gemini icon although Google lists Gemini as core. For Gemini, use the official core product download or a labelled neutral shape, and record the choice.
- The library has no boundary shapes. Draw organization, folder, project, network, region and zone as plain labelled containers.

Category for common products, from Google's guide:

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

Legacy draw.io libraries, avoid for new work: "Google Cloud Platform" [gcp2], the pre-2025 icons and product cards in `mxgraph.gcp2.*`, which the editor also opens for the old ID "gcp"; "GCP Icons" [gcpicons], the legacy console icons embedded as SVG data; and the oldest `mxgraph.gcp.*` shapes. The gcp2 zone colours are plain rounded rectangles and can still serve as neutral frames.

Scope: an organization holds folders and projects; a project is the ownership, billing and IAM boundary. "VPC networks, including their associated routes and firewall rules, are global resources. Subnets are regional resources" (VPC documentation). Zonal resources such as Compute Engine VMs and zonal GKE clusters sit in one zone. With Shared VPC a host project owns the network and service projects attach to it: draw each service project's resources in that project's frame, connected to the host project's network.

## Sources

- draw.io source, palettes and Azure images: https://github.com/jgraph/drawio (src/main/webapp/js/diagramly/sidebar and img/lib/azure2)
- AWS Architecture Icons: https://aws.amazon.com/architecture/icons/
- Azure icons: https://learn.microsoft.com/azure/architecture/icons/
- Google Cloud icons: https://cloud.google.com/icons and the product icon guide linked there
- Network scope: https://docs.aws.amazon.com/vpc/latest/userguide/configure-subnets.html, https://learn.microsoft.com/azure/virtual-network/virtual-networks-faq, https://cloud.google.com/vpc/docs/vpc
