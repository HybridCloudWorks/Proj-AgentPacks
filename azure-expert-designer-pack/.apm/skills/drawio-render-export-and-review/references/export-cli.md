# Draw.io Desktop Export Options

Verified on 2026-10-18 against draw.io Desktop 32.5.5 (`src/main/args.js` in `jgraph/drawio-desktop`). Run the executable with `--help` to confirm the options of the installed version.

| Option | Meaning |
|---|---|
| `-x`, `--export` | Export the input files or folders. Besides draw.io files, `.vsdx`, `.csv` and Mermaid `.mmd` or `.mermaid` inputs are accepted. |
| `-f`, `--format` | `pdf` (default), `png`, `jpg`, `svg`, `xml` or `html`. Ignored when the output file name has an extension. |
| `-o`, `--output` | Output file or folder. |
| `-k`, `--check` | Do not overwrite existing files. |
| `-p`, `--page-index` | Page to export, counting from 1. Images export the first page when it is omitted. |
| `-a`, `--all-pages` | Export all pages, for PDF and HTML only. |
| `-g`, `--page-range` | Page range such as `1..3`, for PDF only. |
| `-s`, `--scale` | Scale the diagram. |
| `--width`, `--height` | Fit the image or PDF into this width or height, keeping the aspect ratio. Do not combine with `-s`. |
| `-b`, `--border` | Border width around the diagram, default 0. |
| `--size` | `diagram` (default) crops PNG, JPG or SVG output to the content; `page` exports the full page. |
| `--crop` | Crop PDF output to the diagram. |
| `-t`, `--transparent` | Transparent background for PNG and SVG. |
| `--theme` | `dark`, `light` or `auto` (default) for SVG, PNG, JPEG and PDF. `auto` keeps SVG adaptive to the viewer and renders other formats light. |
| `-e`, `--embed-diagram` | Embed a copy of the diagram in PNG, SVG or PDF output. |
| `--embed-svg-images` | Embed images in SVG output. |
| `-l`, `--layers` | Comma-separated layer indexes to export. |
| `-u`, `--uncompressed` | Uncompressed XML output, for XML and SVG. |
| `--timeout` | Fail a file that takes longer than this many seconds. |
| `--layout`, `--normalize` | Run a layout, or repair the model, before export. Avoid both for review exports. |

Examples, with `drawio` standing for the detected executable:

```text
drawio -x -k -f png --width 2000 -o review/diagram.png diagram.drawio
drawio -x -k -f svg --embed-svg-images -o exports/diagram.svg diagram.drawio
drawio -x -k -f pdf -a --crop -o exports/diagram.pdf diagram.drawio
```

Without `--embed-svg-images`, an SVG export points each Azure icon at a file inside the local draw.io installation; this was seen with draw.io 32.4.1 on Windows. Such an SVG shows broken images on any other machine.

Use a draft PNG without `-e` for visual review, so the image under review is exactly what a reader sees. Add `-e` only to a final export that must reopen as an editable diagram.
