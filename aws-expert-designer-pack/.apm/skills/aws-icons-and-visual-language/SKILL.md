---
name: aws-icons-and-visual-language
description: Apply draw.io's current AWS library icons and group styles, product labels, optional decorative category tiles, typography, and AWS architecture diagram conventions.
---

# AWS Icons and Visual Language

Use this Skill whenever an AWS product, resource, account boundary, network scope, or AWS visual style is shown.

`drawio-core-generation` decides which icon library is current and how boundaries nest. Its provider reference and the `diagram-validation-and-evidence` catalog are the source for every icon and group style. This Skill adds the pack's house style on top: sizes, typography, labels, badges and the legend.

## Icons

- Copy every AWS icon and group style from draw.io's current AWS library ("AWS <current year>"), through the editor's shape search or the names in the shared provider reference. Keep the full palette style, including the category `fillColor`, the `strokeColor` and the bottom label position, and change only the house typography and size. Never retype a style from memory or recolour an icon.
- Confirm every name with `check_drawio.py --strict` from `diagram-validation-and-evidence`. Legacy names (AWS18 `productIcon`, AWS17, AWS 3D), retired names and unknown names fail. The `mxgraph.aws4` namespace alone does not prove that an icon is current.
- When a specific resource type is shown, prefer its resource icon, for example `application_load_balancer` for an Application Load Balancer rather than the Elastic Load Balancing service icon.
- Keep every icon at 48x48 and parent it directly to the boundary it really sits in. Put the AWS product name, and an optional italic role label, in the icon's label.
- Do not distort, rotate or crop an icon, and do not use an AWS product icon to represent a custom application, team or generic component.

## Other providers and non-cloud systems

Azure and Google Cloud components use their own provider's current library, as `drawio-core-generation` describes, at the same 48x48 size. Only custom applications, teams and third-party or on-premises systems get labelled neutral shapes. AWS's General Resources icons (users, client, traditional server) may stand for people and generic devices. Record any approximate mapping.

## Category tiles (optional)

A 120x120 tile behind an icon may group services by category. It is decorative only: `container=0`, no children, the same parent as its icon, placed before the icon in the file, and never an edge endpoint. Never stroke or fill a tile in a boundary colour. The Networking (`#8C4FFF`) and Storage (`#7AA116`) category colours equal the VPC and public-subnet strokes, so a tile in those colours reads as a nested boundary. Use a neutral fill without a stroke, or leave tiles out.

## Boundaries

Draw account, Region, VPC and subnets with the library's AWS group styles, and the Availability Zone with the library's dashed rectangle, nested account > Region > VPC > Availability Zone > subnet. Library group styles carry `container=1`, so a frame used decoratively must set `container=0` explicitly and have no children.

## Visual language

Use Helvetica, a professional title and subtitle, explicit flow direction, and a teal numbered step badge plus a right-hand legend for complex diagrams or seven or more primary services. Keep auxiliary services such as IAM, CloudWatch, CloudTrail, and X-Ray visually distinct, and do not force them into the primary business flow unless they are part of the requested architecture.

Read [references/aws-visual-rules.md](references/aws-visual-rules.md) when drawing or checking AWS boundaries, containment, category tiles, typography or dark-mode behavior.
