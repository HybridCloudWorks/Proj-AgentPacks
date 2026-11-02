# Export and render record

Evidence for an export and for renderer-based review. A successful exit code proves only that the export ran. Legibility is established by inspecting the output at the size people will see it.

## Renderer

- Locations checked. On Windows: the installer path `C:\Program Files\draw.io\draw.io.exe`; the per-user `%LOCALAPPDATA%\Programs\draw.io\draw.io.exe`; PATH; and the Microsoft Store build, `app\draw.io.exe` inside the InstallLocation that `Get-AppxPackage *draw.io*` reports, or inside `C:\Program Files\WindowsApps\<package>`, where `<package>` is the name that `reg query "HKCU\Software\Classes\Local Settings\Software\Microsoft\Windows\CurrentVersion\AppModel\Repository\Packages" | findstr draw.io` prints:
- Executable found and the version `--version` printed:
- If no renderer was available: write "Rendering was not run", list only the static checks, and produce no export.

## Source

- `.drawio` path:
- Structural checks passed before export (`check_drawio.py --strict`, exit code): yes / no, with reference to the completion report
- Source left unchanged by the export: yes / no (if no, give the approval that covered the change)

## Exports

| Output path | Format | Page | Scale | Background | Border / crop | Command | Exit code |
|---|---|---|---|---|---|---|---|
|  | png / svg / pdf / jpg |  |  | transparent / white |  |  |  |

Every command uses `-x -k`, so an existing export is never overwritten, and SVG exports add `--embed-svg-images`. Review exports never use `--layout` or `--normalize`, which change the diagram before it is drawn. Keep exports apart from the source unless the repository's own conventions say otherwise.

## Visual review

- Reviewed at (intended consumption size):
- Inspection method: human / vision model / automated heuristic. Record each one separately.

| Check | Result | Notes |
|---|---|---|
| Every provider icon and group drew its symbol (no plain coloured squares or broken images) |  |  |
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

## Validation after the render

- `diagram-validation-and-evidence` completed after the final render, with its visual checks based on it: yes / no

## Limits

- Font substitution, viewer differences, pages or formats not reviewed:
