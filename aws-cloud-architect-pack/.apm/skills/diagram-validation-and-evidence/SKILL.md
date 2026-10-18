---
name: diagram-validation-and-evidence
description: Validate Draw.io structure and AWS diagram evidence, then report static, rendered, live, and unresolved results without overstating what was proven.
---

# Diagram Validation and Evidence

Use this Skill for final review, regression checking, source-to-diagram audits, or any claim that a diagram is correct.

## Structural checks

Parse the XML and verify the root structure, unique IDs, parent/source/target references, valid geometry, uncompressed content, safe labels, AWS4 icon namespaces, expected font and container styles, and absence of orphaned or hidden cells. Check that the output and any report exist at the requested paths.

## Semantic checks

Compare the diagram against source files or requirements. For each important component and relationship, record evidence as observed, inferred, designed, or unresolved. Check that accounts, Regions, Availability Zones, VPCs, subnets, endpoints, DNS, IAM, ingress/egress, replication, governance, and data flows are not represented more strongly than the evidence supports.

## Visual checks

Only mark a visual check passed after opening or rendering the actual output. Inspect spacing, clipping, icon scale, labels, contrast, edge routing, arrow direction, boundary semantics, legend completeness, and page cropping. Static XML validation must never be reported as visual validation.

## Report contract

Report scope and inputs, source facts, assumptions and design decisions, output files, structural checks, visual checks, live/external checks, unresolved risks, and the next safe action. Use explicit evidence labels and say when Draw.io Desktop, AWS CLI, repository source, or live APIs were unavailable.
