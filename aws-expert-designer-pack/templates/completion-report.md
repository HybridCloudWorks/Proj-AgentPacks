# Completion report

Use this form at the end of every AWS Expert Designer task. The section names and evidence labels come from the always-on `aws-expert-designer-contract` instruction. Keep them verbatim so that reports from different tasks can be compared and checked.

Evidence labels:

- `observed`: read directly from a source file, requirement text or the user's answer, with its location.
- `inferred`: implied by the evidence but not stated by it.
- `designed`: chosen by the agent or the user to satisfy a requirement.
- `structurally-validated`: confirmed by an XML or reference check that was actually run.
- `visually-validated`: confirmed by opening or rendering the actual output and inspecting it.
- `live-verified`: confirmed against a live AWS account, API or current documentation under the authority stated.
- `not-verified`: not checked. Say why.

Never describe an unexecuted check as passed. State what was not verified.

---

Pack: aws-expert-designer.

Outcome: one sentence in plain words (for example, "diagram delivered", "review delivered, no files changed", or "blocked on two decisions").

## scope_and_inputs

- Task type: design from requirements, reconstruction from source, pattern model, review, repair, layout reflow, or export.
- Purpose and audience:
- Scope (accounts, Regions, environments, pages):
- Inputs read, with paths:
- Inputs requested but not available:
- Existing diagram affected, and the approval that covered the change:

## source_facts

One line for each fact the diagram depends on.

| Fact | Location | Label |
|---|---|---|
|  |  | observed |

## assumptions_and_design_decisions

| Item | Reason | Label |
|---|---|---|
|  |  | inferred / designed |

## output_files

| Path | Kind | New or changed | Approval |
|---|---|---|---|
|  | `.drawio` source / companion report / export / review record | new / changed | not needed for a new file / granted by the user for this path |

Name scratch renders too, and say they are not deliverables.

## structural_checks

| Check | Method | Result | Label |
|---|---|---|---|
| XML parses; `mxfile`, `diagram`, `mxGraphModel`, `root`, cells `0` and `1` |  |  | structurally-validated / not-verified |
| Unique stable IDs; parents resolve |  |  |  |
| Edges have existing sources and targets, attached to icons, not containers |  |  |  |
| Uncompressed payload |  |  |  |
| Icon catalog check: `check_drawio.py --strict` from `diagram-validation-and-evidence`; record the exit code, the icon counts per provider and status, and the catalog's draw.io version | command and exit code |  |  |
| Correct product for each component (the checker cannot judge this) | manual comparison with the source or model |  | observed / not-verified |
| Boundary and icon styles copied whole from draw.io's library; account > Region > VPC > Availability Zone > subnet nesting; nothing parented to a `container=0` cell |  |  |  |
| Font and container styles |  |  |  |
| Outputs exist at the requested paths |  |  |  |

A namespace check (`mxgraph.aws4`) is not an icon check: the current and legacy AWS18 libraries share that namespace.

## visual_checks

- Renderer, path and version (installer, per-user install, PATH or Microsoft Store build), or the locations checked and the reason it was unavailable:
- Output inspected and the size it was reviewed at:
- Defects found and fixed:
- Label: `visually-validated` only after the actual output was opened or rendered and inspected. Otherwise `not-verified`.

## live_or_external_checks

- AWS account, CLI, API or documentation checks, and the authority that covered them:
- Label: `live-verified` or `not-verified`.

## unresolved_risks

- What the diagram might still misrepresent, and the evidence that would settle it.

## next_safe_action

- The single next step that needs no new authority, or the exact decision the user must make: the action, the target and the effect.
