---
name: azure-icons-and-visual-language
description: Apply official Azure2 icons, labels, boundary styles, typography, and visual conventions without distorting service meaning or implying false isolation.
---

# Azure Icons and Visual Language

Use this Skill whenever an Azure product, resource boundary, governance scope, or Azure visual style is shown.

## Icons

- Prefer the official Azure2 icon path from the supplied catalog: `img/lib/azure2/<category>/<File_Name>.svg`.
- Keep the icon undistorted, unrotated, uncropped, and at a consistent visual size. Put the product name near the icon, even when the icon is familiar.
- Do not use a Microsoft product icon to represent a custom application, team, or generic component. Use a neutral shape for those concepts.
- If an exact service icon is unavailable or the service name is uncertain, use a neutral labeled shape and record the limitation; do not guess a nearby product.

## Boundaries

Keep these concepts distinct:

- subscription/resource group: ownership and management scope;
- region/zone: placement and failure-domain scope;
- VNet/subnet: network address and routing scope;
- governance/management group/policy: control scope, not packet flow;
- data boundary/trust boundary: information or authorization scope, not necessarily Azure resource containment.

Use real Draw.io containers only when child movement and containment are intended. Decorative region frames must not imply that resources share a VNet or that traffic is isolated.

Read [references/azure-visual-rules.md](references/azure-visual-rules.md) for the consolidated style and icon rules.
