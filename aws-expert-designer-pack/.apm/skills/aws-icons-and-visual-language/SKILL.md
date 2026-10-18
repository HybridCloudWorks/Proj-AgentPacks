---
name: aws-icons-and-visual-language
description: Apply current AWS4 service and resource icons, labels, category containers, boundary styles, typography, and AWS architecture diagram conventions.
---

# AWS Icons and Visual Language

Use this Skill whenever an AWS product, resource, account boundary, network scope, or AWS visual style is shown.

## Icons

- Prefer the current AWS4 icon/resource library exposed by the installed Draw.io distribution or the current AWS-approved icon package.
- Use the `mxgraph.aws4.*` namespace and valid `resIcon` names; do not invent names or silently use legacy AWS shapes.
- Keep service icons at 48x48 inside a 120x120 colored category container. Put the AWS product name and an optional italic role label near the icon.
- Do not distort, rotate, crop, or use an AWS product icon to represent a custom application, team, or generic component. Use a neutral/general icon for those concepts and label it.
- For mixed architectures, use AWS icons only for AWS services and general icons for non-AWS systems. Record any approximate mapping.

## Visual language

Use Helvetica, a professional title and subtitle, clear category tinting, explicit flow direction, and a teal numbered step badge plus right-hand legend for complex diagrams or seven or more primary services. Keep auxiliary services such as IAM, CloudWatch, CloudTrail, and X-Ray visually distinct and do not force them into the primary business flow unless they are part of the requested architecture.

Read [references/aws-visual-rules.md](references/aws-visual-rules.md) when selecting boundary styles, dark-mode behavior, or complex-diagram conventions.
