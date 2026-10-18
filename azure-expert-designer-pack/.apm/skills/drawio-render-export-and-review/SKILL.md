---
name: drawio-render-export-and-review
description: Export Draw.io diagrams through the installed desktop CLI and perform a renderer-based review of labels, icons, edges, boundaries, and output legibility.
---

# Draw.io Render, Export, and Review

Use this Skill for PNG, SVG, PDF, or JPG export, renderer-based inspection, visual regression, or troubleshooting an output that does not look correct.

## Detect before use

Detect the Draw.io Desktop executable and print its version. On Windows, common locations include `C:\Program Files\draw.io\draw.io.exe` and the user installation directory. Do not assume the executable is on PATH. If it is unavailable, report that rendering was not run and continue with static checks only.

## Export workflow

Keep the `.drawio` source as the authoritative editable artifact. Export to the requested format with an explicit output path, page selection, scale, background, and crop behavior. Never overwrite the source merely to obtain an export. Keep generated exports separate from source unless the repository contract says otherwise.

## Visual review

Inspect the rendered result for clipped text, unreadable labels, icon distortion, poor contrast, hidden edges, overlaps, crossed flows, false containment, excessive whitespace, and page cropping. Review at the intended consumption size. A successful CLI exit code proves export execution, not diagram quality.

Use the upstream Draw.io self-check or image review loop when available, but preserve the distinction between automated heuristics and human/vision inspection.
