---
description: "Export a Draw.io diagram to PNG, SVG, PDF or JPG and review the rendered output"
agent: aws-expert-designer
---

# Export and review a Draw.io diagram

## Inputs

The `.drawio` source; the formats, pages, scale, background, border or crop; and the output directory. Exports go to an explicit path, kept separate from the source unless the repository's own conventions say otherwise.

## Workflow

1. Apply the `diagram-validation-and-evidence` structural checks to the source first, against the `drawio-core-generation` output contract. An export of a broken file is not a deliverable, and the `.drawio` source stays the authoritative editable artifact.
2. Apply `drawio-render-export-and-review`. Detect the Draw.io Desktop executable and record its version; on Windows, check `C:\Program Files\draw.io\draw.io.exe` and the user installation directory, and do not assume the executable is on PATH. Export with an explicit output path, page selection, scale, background and crop. Never overwrite the source to obtain an export.
3. Open each output at its intended consumption size. Inspect it for clipped text, unreadable labels, icon distortion, poor contrast, hidden edges, overlaps, crossed flows, false containment, excessive whitespace and page cropping. Keep automated heuristics separate from human or vision inspection.
4. If the review finds a layout defect, apply `aws-layout-and-composition` and `aws-xml-authoring`, but only with approval to change the source. Then export again.

If Draw.io Desktop is unavailable, say that rendering was not run, produce no export, and report static checks only.

## Expected output

The export files at the requested paths; a render record with the executable path and version, the commands, exit codes, outputs, sizes reviewed and defects found; and a completion report. A successful exit code proves that the export ran, not that the diagram is legible. Do not publish exports externally without approval.

Follow the `aws-expert-designer-contract` instruction: report every section it lists, label evidence with its labels, and never describe an unexecuted check as passed.
