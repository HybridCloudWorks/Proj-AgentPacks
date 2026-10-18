---
description: "Export a Draw.io diagram to PNG, SVG, PDF or JPG and review the rendered output"
agent: azure-expert-designer
---

# Export and review a rendered diagram

## Inputs

- The source `.drawio` file.
- Format, pages, scale, background, border or crop, and the output path.
- The intended consumption size, such as a slide, wiki page or print.

## Workflow

1. Apply `drawio-render-export-and-review`. Detect the Draw.io Desktop executable and print its version. Do not assume it is on PATH; on Windows also check `C:\Program Files\draw.io\draw.io.exe` and the user installation directory.
2. If the executable is not found, the export is blocked. Do not substitute another renderer for the review. Report that rendering was not run and continue with structural checks only.
3. Run `diagram-validation-and-evidence` structural checks on the source before exporting.
4. Export with an explicit output path, page selection, scale, background and crop behavior. Keep the `.drawio` source authoritative, as `drawio-core-generation` requires: never overwrite it to obtain an export, and keep exports separate from source unless the repository's own conventions say otherwise.
5. Ask before replacing an existing export file, and before publishing or pushing anything outside the working copy.
6. Inspect the rendered output at the intended size for clipped text, unreadable labels, icon distortion, poor contrast, hidden edges, overlaps, crossed flows, false containment, excess whitespace and page cropping. A successful exit code proves only that the export ran.
7. Report visual defects. Fixing them in the source is a separate edit that needs approval.

## Expected output

- The exported files at the agreed paths, with the renderer path and version.
- Visual findings at the consumption size, and which pages were reviewed.
- A completion report that follows the `azure-expert-designer-contract` instruction, with visual checks marked `not-verified` whenever rendering did not run.
