# Diagram review findings

Use for a read-only review of an existing diagram, and for a source-to-diagram audit. The reviewed file is not modified; fixes are proposed, not applied.

## Review scope

| Field | Value |
|---|---|
| Diagram file | |
| Content hash before review | |
| Content hash after review | must match; state it |
| Reference sources | requirements, infrastructure paths and commit, or pattern |
| Review focus | |
| Renderer | Draw.io Desktop path and version (installer, per-user or Microsoft Store build), or not found in any of those locations |

## Findings

Severity: **High** misrepresents security, network, identity, data or failure behavior; **Medium** omits or weakens something a reviewer needs to judge the design; **Low** affects readability, labels or style only.

| ID | Severity | Page and cell ID | Category | Finding | Evidence and label | Impact on a reader | Recommended fix |
|---|---|---|---|---|---|---|---|
| F1 | | | semantic, boundary, icon, layout or structural | | | | |

## Source-to-diagram audit

Fill this section for an audit; leave it out of a plain review.

| Item | Classification | Diagram location | Source location | Label |
|---|---|---|---|---|
| | matched, in source only, on diagram only, wrong boundary, or relationship differs | | | observed or inferred |

## Checks

| Check | Run | Result |
|---|---|---|
| `check_drawio.py --strict` (diagram-validation-and-evidence): XML parse, root cells, IDs per page, parents, edges, compression | yes or no | result, error and warning counts |
| Azure icons against the catalog | yes or no | catalog draw.io version; current, legacy and unknown counts |
| Boundary scope rules (provider-checks.md) and edge labels | yes or no | |
| Semantic comparison against reference sources | yes or no | |
| Rendered visual inspection, including that every Azure icon drew | yes or no | |
| Live Azure comparison | yes or no | |

## Proposed follow-up

The edits that would resolve the findings, grouped so the user can approve them separately.
