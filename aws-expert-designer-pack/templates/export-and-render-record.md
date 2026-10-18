# Export and render record

Evidence for an export and for renderer-based review. A successful exit code proves only that the export ran. Legibility is established by inspecting the output at the size people will see it.

## Renderer

- Locations checked (on Windows: `C:\Program Files\draw.io\draw.io.exe`, the user installation directory, PATH):
- Executable found and the version it printed:
- If no renderer was available: write "Rendering was not run", list only the static checks, and produce no export.

## Source

- `.drawio` path:
- Structural checks passed before export: yes / no, with reference to the completion report
- Source left unchanged by the export: yes / no (if no, give the approval that covered the change)

## Exports

| Output path | Format | Page | Scale | Background | Border / crop | Command | Exit code |
|---|---|---|---|---|---|---|---|
|  | png / svg / pdf / jpg |  |  | transparent / white |  |  |  |

Keep exports apart from the source unless the repository's own conventions say otherwise.

## Visual review

- Reviewed at (intended consumption size):
- Inspection method: human / vision model / automated heuristic. Record each one separately.

| Check | Result | Notes |
|---|---|---|
| Clipped text |  |  |
| Labels readable at consumption size |  |  |
| Icon distortion or inconsistent scale |  |  |
| Contrast, including dark mode if required |  |  |
| Hidden edges |  |  |
| Overlaps |  |  |
| Crossed flows |  |  |
| False containment |  |  |
| Excessive whitespace |  |  |
| Page cropping |  |  |
| Legend complete |  |  |

## Defects and fixes

| Defect | Fix | Re-exported | Re-inspected |
|---|---|---|---|
|  |  |  |  |

## Limits

- Font substitution, viewer differences, pages or formats not reviewed:
