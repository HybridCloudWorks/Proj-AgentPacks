# Diagram companion report

Keep this next to the `.drawio` file when the diagram involves design decisions or source inference. It explains what the drawing cannot: where each element came from, what each boundary means, and what is still open.

## Diagram

| Field | Value |
|---|---|
| File | |
| As of | date, and commit if source-derived |
| Purpose and audience | |
| Task type | design, reconstruction, review or export |
| Source of truth | |

## Views

| Page | Shows | Flow direction |
|---|---|---|
| | | left-to-right data flow, or top-to-bottom governance or control plane |

## Evidence matrix

Label every important component and relationship. `observed` means present in supplied source or evidence; `inferred` means derived from it but not stated; `designed` means a design choice with no source behind it. Items marked unresolved need evidence the task did not have and carry into the completion report's `unresolved_risks`.

### Components

| Cell ID | Component | Boundary | Evidence | Label |
|---|---|---|---|---|
| | | subscription / resource group / region / VNet / subnet | file and resource, requirement, or decision | |

### Relationships

| Edge ID | From | To | Meaning | Evidence | Label |
|---|---|---|---|---|---|
| | | | synchronous call, asynchronous message, replication or control plane | | |

## Boundary semantics

State which frames are real containers (`container=1`, children parented and moving with them) and which are decorative (`container=0`). A decorative frame never implies shared network, isolation or ownership.

| Cell ID | Frame | Kind | Meaning |
|---|---|---|---|
| | | real container or decorative | ownership, placement, network, governance, or data/trust boundary |

## Legend notes

Explain any non-obvious routing, replication, identity or boundary semantics shown on the diagram, including numbered badges.

## Icons

| Component | Icon used | Note |
|---|---|---|
| | `img/lib/azure2/<category>/<File_Name>.svg` or neutral shape | catalog checked, or why a neutral shape was used |

## Design decisions

| Decision | Alternatives considered | Reason | Consequence |
|---|---|---|---|
| | | | |

## Pattern deviations

| Pattern | Deviation | Reason |
|---|---|---|
| | | |

## Assumptions

| Assumption | Effect if wrong |
|---|---|
| | |

## Open questions

| Question | Owner | Blocks |
|---|---|---|
| | | |
