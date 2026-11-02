---
name: drawio-render-export-and-review
description: "Export Draw.io diagrams through the installed Draw.io Desktop command line and review the rendered output for AWS, Azure, Google Cloud, or mixed diagrams: icons that failed to draw, labels, edges, boundaries and legibility. Use when exporting a diagram to PNG, SVG, PDF or JPG, inspecting a render, or troubleshooting an output that does not look right."
---

# Draw.io Render, Export, and Review

## Purpose and activation

Turn the editable diagram into the requested exports without changing it, and review what a reader will actually see. Activate for PNG, SVG, PDF, or JPG export, renderer-based inspection, visual regression, or an output that does not look right, for one provider or several in one diagram.

## Scope and exclusions

In scope: detecting Draw.io Desktop, exporting with explicit options, and reviewing the render, including each provider's icon failure modes. Out of scope: editing the diagram (drawio-core-generation) and structural or semantic validation (diagram-validation-and-evidence), although this skill's visual findings feed that report.

## Inputs

The `.drawio` source, the requested formats, pages, scale or width, background and theme, the output paths, and the size at which the result will be consumed.

## Dependencies and tools

- Draw.io Desktop's command line. Do not assume it is on PATH; common locations:
  - Windows: `C:\Program Files\draw.io\draw.io.exe` for the installer. The Microsoft Store version is `C:\Program Files\WindowsApps\<package folder>\app\draw.io.exe` and accepts the same options. `Get-AppxPackage *draw.io*` reports the folder as InstallLocation. When PowerShell or that cmdlet is unavailable or denied, this read-only query prints the package folder name, such as `draw.io.draw.ioDiagrams_32.6.1.0_x64__1zh33159kp73c`, as the last part of a key: `reg query "HKCU\Software\Classes\Local Settings\Software\Microsoft\Windows\CurrentVersion\AppModel\Repository\Packages" | findstr draw.io`. The WindowsApps folder itself cannot be listed, but the full path to the executable works.
  - macOS: `/Applications/draw.io.app/Contents/MacOS/draw.io`, or `drawio` from Homebrew.
  - Linux: `drawio` from the deb, rpm or snap package, or an AppImage.
- [references/export-cli.md](references/export-cli.md): the export options, checked against `--help` of draw.io Desktop 32.6.1.
- An image viewer or vision-capable review for the rendered output.

## Workflow

1. Detect the executable and print its version with `--version`.
2. Export with an explicit output path, page, scale or width, border, background, and size mode.
   - Pass `-k` so an existing export is never overwritten by accident.
   - Do not pass `--layout` or `--normalize` for a review export. Both change the diagram before export and can hide the defects the review must find.
   - For SVG, pass `--embed-svg-images`. Azure icons are images rather than stencils, and without the option the SVG points them at files inside the local draw.io installation.
   - Use a draft PNG without `-e` for review, and add `-e` only to a final export that must reopen as an editable diagram.
   - On Windows, draw.io Desktop can print `Gpu Cache Creation failed` on stderr. It is harmless when the exit code is 0 and the export exists.
3. Review the render at the intended consumption size for clipped text, unreadable labels, icon distortion, poor contrast, hidden edges, overlaps, crossed flows, false containment, excessive whitespace, and page cropping. Then check:
   - AWS and Google Cloud icons are stencils. A wrong name draws a plain coloured square with no symbol, so check that every icon shows its symbol.
   - A partially drawn icon means a missing library colour: an AWS service icon without `fillColor` vanishes and without `strokeColor` shows a black symbol, and a Google Cloud icon without `fillColor` loses parts, such as Cloud Run's blue chevron.
   - Azure icons are images. A wrong path, including the palette's wrong letter case for a few files, draws a broken-image placeholder.
   - Google Cloud category icons look the same for many products, so each must carry a readable product label.
   - Labels: `whiteSpace=wrap` on an icon style wraps the label to the icon's width, one word per line; a long label without it runs into its neighbours. Give long labels room or a deliberate line break.
   - Edge labels sit at the midpoint of the edge's path, so on a bent edge they can land on a frame border or another edge. Move the label along the edge or onto a straight segment.
   - Where a crossing cannot be avoided, the crossing edge should use `jumpStyle=arc` so the reader sees the two flows do not join.
   - In a mixed diagram, icons from different libraries should look the same size, and every cross-provider edge label should be legible.
4. Use the upstream draw.io self-check or image review loop when it is installed, but keep automated heuristics separate from human or vision inspection.

## Output

The exports at the requested paths, the draw.io version and the exact command used for each, and the visual findings with the location of each problem.

## Validation

Each export exists, is not empty, and was opened or viewed before any visual claim. Every provider icon visibly drew. A successful exit code proves only that the export ran, not that the diagram is right.

## Failure handling and escalation

- No executable: report that rendering was not run and continue with static checks only. Installing draw.io needs the user's approval.
- The command line crashes or hangs, for example in a sandbox: retry once with `--timeout`, then report the failure and deliver the `.drawio` source without exports.
- An export shows a defect: report it with its location and hand the fix to drawio-core-generation. Never patch the export image.

## Permissions and guardrails

Never overwrite or modify the `.drawio` source to obtain an export, and keep exports separate from source unless the repository says otherwise. Write only to the requested output paths. Do not install or update software without approval.

## Connection to the pack

This skill ships unchanged in the AWS, Azure and Google Cloud architect packs and the AWS and Azure designer packs, so whichever pack is installed last leaves the same skill in place. It sits between drawio-core-generation and diagram-validation-and-evidence in every diagram workflow. Installed on its own, it still works and the guardrails above still apply. Installed with a pack, it follows that pack's always-on contract instruction for approval levels, handoffs and the completion report.
