# Worked example: normalizing and reflowing an exported landing-zone diagram

Prompts: `repair-azure-drawio-xml.prompt.md`, then `reflow-diagram-layout.prompt.md`. Skills: `drawio-xml-authoring`, `azure-icons-and-visual-language`, `drawio-core-generation`, `drawio-layout-and-composition`, `diagram-validation-and-evidence`, `drawio-render-export-and-review`.

Fictional scenario. Names, paths and tool output are illustrative.

## Request

> Our landing-zone diagram, `docs/architecture/landing-zone.drawio`, fails validation, and it is unreadable on the wiki. Fix it and make it readable.

## 1. Approval first

The request would change an existing diagram, so the agent asked before editing:

> Should I overwrite `landing-zone.drawio`, or write a repaired copy next to it?

The user answered: "Write a new file; we'll swap it in after review." The output path became `docs/architecture/landing-zone.normalized.drawio`. The original was not modified. Its SHA-256 was recorded before and after.

## 2. Structural defects found

Following the `drawio-xml-authoring` XML checklist reference:

| Defect | Count | Detail |
|---|---|---|
| Compressed payload | 1 | `<diagram>` held a deflated, base64-encoded string with no inline `mxGraphModel` |
| Duplicate IDs | 3 | Copy-pasted cells reused the IDs `5`, `6` and `12` |
| Edge with a missing target | 2 | The target cells had been deleted |
| Legacy `mxgraph.azure` stencils | 9 | |
| False containment | 1 | The hub VNet was parented under a "Policy: allowed locations" note, which had `container=1` |
| Unreadable font size | 14 cells | 8 pt labels, shrunk to fit one page |

## 3. Repair

**Payload.** The agent decoded the payload (base64, then raw inflate, then URL-decode) into an inline `mxGraphModel` in the new file.

**IDs.** It assigned stable semantic IDs where needed, such as `mg_platform`, `sub_connectivity`, `vnet_hub` and `vpngw_hub`, and kept the 31 existing IDs that were already unique. The companion change log records the old-to-new ID map.

**Icons.** `azure-icons-and-visual-language` mapped the legacy stencils:

- Seven had an exact Azure2 equivalent and were replaced with `img/lib/azure2/...` image paths.
- `mxgraph.azure.enterprise`, labeled "Ops tooling", is a custom internal tool. Using a product icon for it would be wrong, so it became a neutral labeled shape.
- `mxgraph.azure.mobile_services`, labeled "Partner API", has an uncertain service mapping. It became a neutral labeled shape, and the limitation was recorded.

**Broken edges.**

- The edge labeled "VPN" from "On-premises" ended at the position of the hub VNet's VPN gateway cell. It was reconnected to `vpngw_hub` and labeled `inferred`.
- An unlabeled edge with no target had no nearby candidate. Guessing a target would invent a flow, so it was left out of the repaired copy and listed as an unresolved risk.

**Containment.** The hub VNet was re-parented from the policy note to `sub_connectivity`, and the note was set to `container=0`. This changes what the diagram claims, so it is recorded as a semantic correction, not a cosmetic fix.

No service or flow was added. After `drawio-core-generation` confirmed the output contract, the repaired copy passed the structural checks.

## 4. Reflow

`drawio-layout-and-composition`, with the wiki page at 1100 px wide as the consumption size:

- Sixteen primary elements on one page could not stay readable at that width, so the agent split them into two pages instead of shrinking the text:
  - "Governance": the management group hierarchy, top to bottom, with policy assignments as their own layer.
  - "Connectivity": the hub and spokes, left to right, with on-premises on the left.
- Spacing of 220 px horizontal and 160 px vertical on the governance page (13 or more elements), and 180 px and 120 px on the connectivity page. There is 30 px of padding inside every real boundary, and coordinates are aligned to 10 px.
- Labels at 11 pt minimum. Icons are a consistent 48 px. Numbered badges 1 to 9 with a right-side legend on the connectivity page.
- Peering and VPN edges routed orthogonally with waypoints around the spoke containers. The policy-assignment edges use the dotted control-plane style.

Cell IDs were unchanged by the reflow, so the diff shows geometry, style and the new page only.

## 5. Render review

Draw.io Desktop 24.7.17 exported both pages to `%TEMP%\landing-zone-review\` at the wiki width. The first render showed the "Identity" subscription label colliding with a badge. The agent moved the badge 20 px right. The second render was clean on both pages.

## Completion report

Pack: azure-expert-designer.

### scope_and_inputs

- Task type and outcome: repair and reflow. A normalized two-page copy was written; the original was left unchanged. `observed`
- Inputs: `docs/architecture/landing-zone.drawio` (compressed) and the user's report of a validation failure and poor wiki readability. `observed`
- Approval: write a new file; the original must not be overwritten. `observed`

### source_facts

- The original has a compressed payload, three duplicate IDs, two edges with missing targets, nine legacy stencils and a hub VNet parented under a policy note. `observed`

### assumptions_and_design_decisions

- The "VPN" edge's intended target is the hub VPN gateway, based on its label and end geometry. `inferred`
- The unlabeled, targetless edge was left out instead of being guessed. `designed`
- The hub VNet was moved into the connectivity subscription. This is a semantic correction. `designed`
- "Ops tooling" and "Partner API" are neutral shapes; no product icon was guessed. `designed`
- The diagram was split into "Governance" and "Connectivity" pages, instead of being shrunk. `designed`

### output_files

- `docs/architecture/landing-zone.normalized.drawio`: new, uncompressed, two pages.
- `docs/architecture/landing-zone.normalized.md`: change log with the defects, fixes, ID map and semantic corrections.
- `docs/architecture/landing-zone.drawio`: unchanged; the hash matched before and after.
- `%TEMP%\landing-zone-review\`: review renders outside the repository.

### structural_checks

- XML parses; root cells on both pages; unique IDs; all parents, sources and targets resolve; uncompressed; no legacy `mxgraph.azure` shapes; Helvetica throughout. `structurally-validated`

### visual_checks

- Both pages rendered with Draw.io Desktop 24.7.17 and inspected at 1100 px. One collision was fixed; the second render was clean. `visually-validated`

### live_or_external_checks

- Management group, subscription and policy names were not compared with the live tenant. `not-verified`

### unresolved_risks

- The dropped unlabeled edge may have represented a real flow. The diagram owner should confirm it.
- The "Partner API" service is unidentified.
- The wiki still embeds the original file until it is swapped.

### next_safe_action

- The diagram owner reviews `landing-zone.normalized.drawio` and its change log, confirms the dropped edge, and then approves replacing the original.
