# Provider Checks

The checker in `scripts/check_drawio.py` applies the icon rules below automatically. The scope rules need judgement, so apply them by reading the diagram. The `drawio-core-generation` Skill's provider reference gives the background for each rule.

## Icon status by style

| Provider | Current | Legacy or retired |
|---|---|---|
| AWS | `shape=mxgraph.aws4.resourceIcon;resIcon=mxgraph.aws4.<name>`, `shape=mxgraph.aws4.<name>`, `shape=mxgraph.aws4.group;grIcon=...`, with the name in the catalog's current list | `productIcon` or `prIcon` (AWS18), `mxgraph.aws3.*` (AWS17), `mxgraph.aws3d.*` (AWS 3D), names in the catalog's retired list (AWS (retired)) |
| Azure | `image=img/lib/azure2/<category>/<File>.svg` with the path in the catalog's current list | `mxgraph.azure.*` (old Azure), `mxgraph.mscae.*` or `img/lib/mscae/` (Cloud & Enterprise), azure2 files the palette no longer offers |
| Google Cloud | `shape=mxgraph.gcp3.<name>` with the name in the catalog's core or category list | `mxgraph.gcp2.*` (pre-2025 icons and product cards), `mxgraph.gcp.*` (oldest), GCP Icons (legacy console icons embedded as SVG data, reported as unattributed) |

A name that matches a namespace but is missing from the catalog is unknown and almost always a typo. The AWS current and AWS18 libraries share the `mxgraph.aws4` namespace, so judge AWS icons by style and name, not namespace.

## What the checker cannot decide

- Whether the icon is the right product for the component. A valid Amazon S3 icon on a database is still wrong.
- Whether a Google Cloud category icon's label names the product, or whether a nearby text cell carries the label.
- Containment semantics, flow direction, and whether a boundary is drawn at the right scope.
- Embedded or linked images. Linked images also need network access to render.

## Scope rules

| Rule | Wrong drawing |
|---|---|
| An AWS subnet sits in exactly one Availability Zone | one subnet frame stretched across two AZ frames |
| An AWS VPC or Azure VNet lives in one region | one network frame spanning two region frames; draw one network per region, joined by a labelled peering or transit link |
| Azure and Google Cloud subnets span the zones of their region | a subnet frame inside a zone frame |
| A Google Cloud VPC network is global | a VPC network frame inside a single region frame |
| Ownership scopes are not networks | account, subscription, resource group or project frames used as if they isolate traffic |
| Governance scopes are not packet paths | flow arrows through an organization, management group, folder or policy frame |
| Private connectivity is drawn where it exists | a public path shown for a service reached through AWS PrivateLink, Azure Private Endpoint or Google Cloud Private Service Connect, or the reverse |

## Mixed-provider rules

- Each provider has its own outer frame; no provider's resources sit inside another provider's frame.
- Every cross-provider or on-premises link is an edge labelled with its transport, its direction and what crosses it.
- Identity federation is drawn as its own flow, not implied by adjacency.
- Icons from different libraries share one visual size, and the legend names the provider where icon families could be confused.
