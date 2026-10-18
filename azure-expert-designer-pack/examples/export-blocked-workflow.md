# Worked example: SVG export blocked because there is no renderer

Prompt: `export-and-review-render.prompt.md`. Skills: `drawio-render-export-and-review`, `diagram-validation-and-evidence`, `drawio-core-generation`.

Fictional scenario. Names, paths and tool output are illustrative. The outcome is **blocked**.

## Request

> Export `docs/architecture/landing-zone.drawio` to SVG for Thursday's design review, check that the labels and icons are legible, replace `docs/architecture/landing-zone.svg`, and push it to the design repository.

## 1. Detect the renderer

`drawio-render-export-and-review` says to detect the executable before use, and not to assume PATH:

```text
PS> Get-Command draw.io, drawio -ErrorAction SilentlyContinue
(no output)
PS> Test-Path "C:\Program Files\draw.io\draw.io.exe"
False
PS> Test-Path "$env:LOCALAPPDATA\Programs\draw.io\draw.io.exe"
False
```

Draw.io Desktop is not installed in either the machine-wide or the per-user location, so no version can be printed. The export is blocked.

The agent did not use a browser-based converter or another tool to produce an SVG. The visual check must inspect the output of the renderer the deliverable depends on, and the skill says that without it, rendering is reported as not run and the work continues with static checks only.

## 2. Structural checks continue

`diagram-validation-and-evidence` structural checks ran on the source:

- The XML parses. Cells `0` and `1` are present, and 87 cells have unique IDs.
- Every parent, source and target resolves. The file is uncompressed and every image path is under `img/lib/azure2/`.
- Two cells, `note_policy_exemptions` and `label_er_circuit`, use `fontSize=8`. That is a static heuristic: they *may* be unreadable on a slide. It is not a visual result, so it is reported as a risk, not a finding.

## 3. Requests that were not carried out

| Requested | Done | Reason |
|---|---|---|
| Export to SVG | No | No renderer available |
| Check labels and icons are legible | No | A legibility check requires a render. Static checks are not visual validation. |
| Replace `docs/architecture/landing-zone.svg` | No | There is no new export. Even with one, replacing an existing export needs the user's confirmation. |
| Push to the design repository | No | Publishing outside the working copy needs explicit authorization. The agent asked for it and did not assume it. |

`docs/architecture/landing-zone.drawio` and the existing `landing-zone.svg` were not touched. Following `drawio-core-generation`, the `.drawio` source stays the authoritative artifact.

## 4. What the agent asked

> Draw.io Desktop isn't installed here, so I can't export or check legibility. Can you install it or tell me where it is? Once the export exists: should it replace `docs/architecture/landing-zone.svg`, and do you authorize pushing it to the design repository? If so, which repository and branch?

## Completion report

Pack: azure-expert-designer.

### scope_and_inputs

- Task type and outcome: export. **Blocked**: no Draw.io Desktop executable was found. `observed`
- Request: SVG export of `docs/architecture/landing-zone.drawio` with a legibility check, replacement of the existing SVG, and a push to the design repository. `observed`
- Approvals: none for replacing the existing SVG or for publishing. Both were asked for. `observed`

### source_facts

- Draw.io Desktop is not on PATH and not at `C:\Program Files\draw.io\draw.io.exe` or `%LOCALAPPDATA%\Programs\draw.io\draw.io.exe`. `observed`
- The source diagram has 87 cells and two cells at `fontSize=8`. `observed`

### assumptions_and_design_decisions

- The per-user installation directory is `%LOCALAPPDATA%\Programs\draw.io`. `inferred`
- No substitute renderer was used, because the review must inspect the deliverable's real renderer output. `designed`

### output_files

- None. `docs/architecture/landing-zone.drawio` and `docs/architecture/landing-zone.svg` were not modified.

### structural_checks

- XML parses; root cells present; unique IDs; all references resolve; uncompressed; Azure2 image paths only. `structurally-validated`

### visual_checks

- No export was produced, and labels and icons were not inspected. `not-verified`

### live_or_external_checks

- Nothing was pushed to the design repository. `not-verified`

### unresolved_risks

- Two 8 pt labels may be unreadable at slide size.
- Thursday's design review has no fresh SVG yet. The existing `landing-zone.svg` may not match the current source.

### next_safe_action

- The user installs Draw.io Desktop or gives its path. Then re-run the export, and confirm whether to replace the existing SVG and whether to authorize the push, naming the repository and branch.
