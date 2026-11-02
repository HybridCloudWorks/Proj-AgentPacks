# AWS Visual Rules

## Where styles come from

draw.io's current AWS library ("AWS <current year>", library ID `aws4`) is the source of every AWS icon and boundary style. `drawio-core-generation` and its provider reference decide which library is current and how boundaries nest, and the `diagram-validation-and-evidence` catalog lists every current name. Copy each style from the library: the editor's shape search, or the palette entry named in the provider reference. Never retype a style from memory or from this file.

Copy the full palette style. For an icon that means the category `fillColor`, the `strokeColor`, `verticalLabelPosition=bottom;verticalAlign=top`, `aspect=fixed` and the shape keys. For a group it means the `shape=mxgraph.aws4.group;grIcon=...` keys, the colours and `container=1`. Change only the house typography (`fontFamily`, `fontSize`, `fontStyle`) and the geometry. Never recolour an icon or a boundary.

## Boundary values in the library

The table restates draw.io's "AWS / Groups" palette (`Sidebar-AWS4.js` at draw.io 32.6.9) so that a reviewer can recognise a drifted copy. It is not a substitute for copying the style.

| Boundary | Library style | Stroke | Fill | Label colour | Line |
|---|---|---|---|---|---|
| AWS Cloud | `group;grIcon=mxgraph.aws4.group_aws_cloud_alt` | `#232F3E` | none | `#232F3E` | solid |
| AWS account | `group;grIcon=mxgraph.aws4.group_account` | `#CD2264` | none | `#CD2264` | solid |
| Region | `group;grIcon=mxgraph.aws4.group_region` | `#00A4A6` | none | `#147EBA` | dashed |
| Availability Zone | plain rectangle, no icon | `#147EBA` | none | `#147EBA` | dashed |
| VPC | `group;grIcon=mxgraph.aws4.group_vpc2` | `#8C4FFF` | none | `#AAB7B8` | solid |
| Public subnet | `group;grIcon=mxgraph.aws4.group_security_group;grStroke=0` | `#7AA116` | `#F2F6E8` | `#248814` | solid |
| Private subnet | `group;grIcon=mxgraph.aws4.group_security_group;grStroke=0` | `#00A4A6` | `#E6F6F7` | `#147EBA` | solid |
| Security group | plain rectangle, no icon | `#DD3522` | none | `#DD3522` | solid |

The label colour differs from the stroke for the Region, the VPC and both subnets. `#248814` and `#147EBA` are label colours, not subnet strokes, and `#147EBA` is also the Availability Zone stroke: a private subnet stroked in `#147EBA` reads as an Availability Zone. `group_vpc`, `group_subnet` and `group_availability_zone` belong to the legacy AWS18 library; do not use them for new work.

## Containment

- Nest account > Region > VPC > Availability Zone > subnet. A VPC lives in one Region and spans that Region's Availability Zones. Each subnet sits in exactly one Availability Zone frame. A subnet in a Local Zone, a Wavelength Zone or on an Outpost sits in exactly one frame for that zone or Outpost, labelled with its type.
- Never stretch one VPC across two Region frames. Draw one VPC per Region and join them with a labelled peering, Transit Gateway or Cloud WAN edge.
- These boundaries are real draw.io containers, and every child is parented to the boundary it really sits in: a NAT gateway to its public subnet, a Regional service such as Amazon S3 to the Region, a VPC-wide resource to the VPC.
- The library's group styles already carry `container=1;collapsible=0;recursiveResize=0`. The library's Availability Zone entry is a plain rectangle without `container=1`, so add `container=1;collapsible=0;recursiveResize=0` to it before parenting subnets to it.
- A frame used decoratively, such as an auxiliary-services frame or an annotation around a group of icons, must set `container=0` explicitly and have no children. Because library group styles carry `container=1`, a group style copied for a decorative frame without that override creates false containment. Parent the icons drawn over a decorative frame to their real scope, and place them after the frame in the file so they draw on top.
- Security groups attach to network interfaces. Draw them as `container=0` outlines around the resources they apply to, never as a parent of subnets.
- An account or AWS Cloud frame is an ownership scope, not a network boundary. An Organization, OU or SCP is a governance scope, not a packet path.

## Icons and category tiles

- House icon size is 48x48 for every icon in the diagram, whatever its provider. The library's default is 78x78. Use one size throughout.
- Azure and Google Cloud components use their own provider's current library, as `drawio-core-generation` describes. Only custom applications, teams and third-party or on-premises systems get labelled neutral shapes. AWS's General Resources icons (`users`, `user`, `client`, `traditional_server`) may stand for people and generic devices.
- A category tile is optional house style: a 120x120 tile behind an icon that groups services by category. It is decorative. It has `container=0`, no children and the same parent as its icon, it comes before the icon in the file, and it is never an edge endpoint.
- Never stroke or fill a tile in a boundary colour. The Networking & Content Delivery category colour (`#8C4FFF`) is the VPC stroke and the Storage category colour (`#7AA116`) is the public-subnet stroke, so a tile in either reads as a nested boundary. Use a neutral fill such as `#F5F5F5` with `strokeColor=none`, or leave tiles out: the library icon already carries its category colour.

## House style

- `fontFamily=Helvetica` for all text. Use sketch attributes only when the user explicitly asks for sketch mode.
- Title 30 px bold, subtitle 16 px, account, Region and VPC labels 14 px bold, Availability Zone and subnet labels 12 px bold, service labels 10 px, edge labels 11 px.
- When dark-mode compatibility is required, house elements (title, legend, badges, neutral shapes) may use `light-dark()` colours and `fillStyle=auto`. Leave library icon and boundary colours as the library sets them, and do not hardcode `mxGraphModel background`.
- Place external actors below the title block, outside the account frame. Draw cross-cutting services that are not primary flow steps over a dashed decorative frame (`container=0`), parented to their real scope.

AWS's official icon page says that icon packages are released quarterly and warns that third-party libraries may contain legacy icon sets. Recheck the current package before adding a service that the installed library lacks, and record the gap rather than borrowing a nearby product's icon.
