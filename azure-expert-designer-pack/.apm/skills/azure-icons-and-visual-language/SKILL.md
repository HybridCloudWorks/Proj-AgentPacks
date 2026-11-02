---
name: azure-icons-and-visual-language
description: Apply Microsoft's Azure architecture icons from draw.io's current Azure library (azure2), product labels, boundary styles, typography, and visual conventions without distorting service meaning or implying false isolation.
---

# Azure Icons and Visual Language

Use this Skill whenever an Azure product, resource boundary, governance scope, or Azure visual style is shown.

The shared skills decide which icon library is current and how boundaries nest: `drawio-core-generation` (its provider reference and workflow steps 3 and 4) and `diagram-validation-and-evidence` (its icon catalog, its checker and `references/provider-checks.md`). This Skill sets house style on top of them: typography, sizes, layout and legend. Where the two disagree, the shared skills win.

## Icons

- Use only current icons from draw.io's Azure library. "Azure" is the library's name in draw.io's More Shapes panel and `azure2` is its ID; the icons are Microsoft's Azure architecture icons. The current paths are the ones `diagram-validation-and-evidence` lists as current in `scripts/icon_catalog.json`, and its `scripts/check_drawio.py --strict` reports any other Azure path as an error.
- Copy each icon's style from the draw.io palette unchanged: the style that `python scripts/check_drawio.py --find "<product>"` prints from the `diagram-validation-and-evidence` Skill's folder, `image;aspect=fixed;html=1;align=center;fontSize=12;image=img/lib/azure2/<category>/<File_Name>.svg;`. The palette's `points=[...]` are connection points only: they do not change how the icon draws, `--find` and the catalog leave them out, and adding them is optional. The library style wins over this Skill. Append only this Skill's typography and label placement after it, for example `fontFamily=Helvetica;`. Never drop `image;` or `aspect=fixed`, and never add `whiteSpace=wrap` to an icon style: it wraps the product label to the icon's width, one or two words per line.
- Size service icons at 48 px on the longest side, with the other side taken from the palette's aspect ratio (SQL Database is 36 by 48, Storage Accounts 48 by 38.4). Size a scope icon in a frame's corner at 24 px on the longest side.
- Put the product name near the icon, even when the icon is familiar.
- Do not crop, flip, rotate, distort, recolour, or change the shape of an icon.
- Do not use a Microsoft product icon to represent a custom application, team, or generic component. Use a neutral shape for those concepts.
- If the library has no current icon for the service, or the service name is uncertain, use Microsoft's current icon download or a neutral labelled shape and record the choice; do not guess a nearby product. Where the shared provider reference names the file to use for a service, follow it.
- A private DNS zone uses the DNS Zones icon (`networking/DNS_Zones.svg`) labelled "Private DNS zone", because Microsoft's icon set has no separate private DNS zone icon.

## Boundaries

Keep these concepts distinct:

- subscription/resource group: ownership and management scope;
- region/zone: placement and failure-domain scope;
- VNet/subnet: network address and routing scope;
- governance/management group/policy: control scope, not packet flow;
- data boundary/trust boundary: information or authorization scope, not necessarily Azure resource containment.

Nest them by `drawio-core-generation` workflow step 4, and check them against the scope rules in `diagram-validation-and-evidence`'s `references/provider-checks.md`. For Azure that means:

- region > VNet > subnet. A VNet lives in one region, so draw one VNet per region frame and join VNets with a labelled peering edge.
- Subnets span every zone of their region. Never put a subnet inside a zone frame. Label a zone-redundant resource with its zones instead of drawing zone frames.
- PaaS reached through a private endpoint stays outside the VNet; only the private endpoint's network interface sits in the subnet.
- App Service with regional VNet integration stays outside the VNet, with an outbound edge into its delegated subnet.
- When ownership and network disagree, for example a private endpoint or gateway in a different resource group from its VNet, parent the resource to the network boundary it is deployed into, and show its resource group in its label or in a decorative `container=0` frame.

Draw each scope as a plain labelled container and put its scope icon in the frame's top-left corner, labelled with the frame's name: `general/Management_Groups.svg`, `general/Subscriptions.svg`, `general/Resource_Groups.svg`, `networking/Virtual_Networks.svg` and `networking/Subnet.svg`. Use real Draw.io containers only when child movement and containment are intended. Decorative region frames must not imply that resources share a VNet or that traffic is isolated.

Read [references/azure-visual-rules.md](references/azure-visual-rules.md) for the consolidated style and icon rules.
