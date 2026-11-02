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

1. Apply `drawio-render-export-and-review`. Detect the Draw.io Desktop executable from that skill's list of locations and print its version with `--version`. Do not assume it is on PATH. On Windows check the installer location `C:\Program Files\draw.io\draw.io.exe`, the per-user installation directory, and the Microsoft Store build: `app\draw.io.exe` inside the InstallLocation that `Get-AppxPackage *draw.io*` reports. When PowerShell is unavailable, `reg query "HKCU\Software\Classes\Local Settings\Software\Microsoft\Windows\CurrentVersion\AppModel\Repository\Packages" | findstr draw.io` names the package folder, and the executable is `C:\Program Files\WindowsApps\<package folder>\app\draw.io.exe`.
2. If the executable is not found in any of those places, the export is blocked. Do not substitute another renderer for the review. Report that rendering was not run and continue with structural checks only.
3. Run `diagram-validation-and-evidence` structural checks on the source before exporting.
4. Export with an explicit output path, page selection, scale, background and crop behavior, and pass `-k` so no existing file is overwritten. For SVG, pass `--embed-svg-images`: Azure icons are images, and without it the SVG points them at files inside the local draw.io installation, so they show as broken images on every other machine. Never pass `--layout` or `--normalize` for a review export; both change the diagram before it is drawn. Keep the `.drawio` source authoritative, as `drawio-core-generation` requires: never overwrite it to obtain an export, and keep exports separate from source unless the repository's own conventions say otherwise.
5. Ask before replacing an existing export file, and before publishing or pushing anything outside the working copy.
6. Inspect the rendered output at the intended size for clipped text, unreadable labels, icon distortion, poor contrast, hidden edges, overlaps, crossed flows, false containment, edge labels on frame borders, excess whitespace and page cropping. Confirm that every Azure icon drew and none shows a broken-image placeholder; for an SVG, also confirm it carries no path into the local draw.io installation. A successful exit code proves only that the export ran.
7. Close with `diagram-validation-and-evidence`, so its report records the visual checks from this render beside the structural ones.
8. Report visual defects. Fixing them in the source is a separate edit that needs approval.

## Expected output

- The exported files at the agreed paths, with the renderer path and version and the exact command used for each.
- Visual findings at the consumption size, and which pages were reviewed.
- A completion report that follows the `azure-expert-designer-contract` instruction, with visual checks marked `not-verified` whenever rendering did not run.
