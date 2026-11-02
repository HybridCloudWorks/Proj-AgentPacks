# Draw.io Desktop Export Options

Checked on 2026-11-01 against the `--help` output of draw.io Desktop 32.6.1 (Microsoft Store build on Windows). Run the executable with `--help` to confirm the options of the installed version.

| Option | Meaning |
|---|---|
| `-x`, `--export` | Export the input files or folders. Besides draw.io files, `.vsdx`, `.csv` and Mermaid `.mmd` or `.mermaid` inputs are accepted. |
| `-r`, `--recursive` | With a folder input, also convert the files in its sub-folders. |
| `-f`, `--format` | `pdf` (default), `png`, `jpg`, `svg`, `xml` or `html`. Ignored when the output file name has an extension. |
| `-o`, `--output` | Output file or folder. Without it, the input name is used with the format's extension. |
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
| `-q`, `--quality` | JPEG quality, default 90. |
| `--theme` | `dark`, `light` or `auto` (default) for SVG, PNG, JPEG and PDF. `auto` keeps SVG adaptive to the viewer and renders other formats light. `--svg-theme` is the deprecated SVG-only form. |
| `-e`, `--embed-diagram` | Embed a copy of the diagram in PNG, SVG or PDF output. |
| `--embed-svg-images` | Embed images in SVG output. |
| `--embed-svg-fonts` | `true` (default) or `false`: embed fonts in SVG output. |
| `--embed-svg-metadata` | Add each cell's shape and connector properties to SVG output as `data-meta-*` attributes. |
| `-l`, `--layers` | Comma-separated layer indexes to export. |
| `-u`, `--uncompressed` | Uncompressed XML output, for XML and SVG. |
| `--mermaid-image` | `true` opens Mermaid input as a static image instead of an editable diagram; default `false`. |
| `--timeout` | Fail a file that takes longer than this many seconds, then continue with the next; default 0, no limit. |
| `--layout`, `--normalize` | Run a layout, or repair the model (move edges to their terminals' common ancestor, add missing edge geometry, grow clipping containers), before export. Avoid both for review exports. |

The help also lists HTML viewer options (`--html-*`), `--svg-links-target`, `-z`, `--zoom` for the interface, and the update switches `--disable-update` and `--no-silent-update`.

Examples, with `drawio` standing for the detected executable:

```text
drawio -x -k -f png --width 2000 -o review/diagram.png diagram.drawio
drawio -x -k -f svg --embed-svg-images -o exports/diagram.svg diagram.drawio
drawio -x -k -f pdf -a --crop -o exports/diagram.pdf diagram.drawio
```

Without `--embed-svg-images`, an SVG export points each Azure icon at a file inside the local draw.io installation; this was seen with draw.io 32.4.1 on Windows. Such an SVG shows broken images on any other machine.

Use a draft PNG without `-e` for visual review, so the image under review is exactly what a reader sees. Add `-e` only to a final export that must reopen as an editable diagram.
