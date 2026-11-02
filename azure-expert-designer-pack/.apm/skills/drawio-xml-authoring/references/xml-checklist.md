# XML Checklist

Before returning a `.drawio` file, check:

1. XML parses with a namespace-aware parser.
2. `mxfile`, `diagram`, `mxGraphModel`, `root`, and cells `0` and `1` exist on every page.
3. IDs are unique within each page and stable; all parent references resolve.
4. All edges have existing source and target cells, and every edge carries a label.
5. Every Azure icon is a current `img/lib/azure2/` path in the `diagram-validation-and-evidence` catalog, in the palette's full style (`image;aspect=fixed;...`), and no `mxgraph.azure.*`, `mxgraph.mscae.*` or `img/lib/mscae/` shape remains unless the user asked to match a legacy diagram. Other components are explicitly labelled neutral or custom shapes.
6. No compressed diagram payload is used when reviewable diffs are required.
7. Labels are escaped and no untrusted input is interpreted as XML markup.
8. Real containers have correct parentage, no cell is parented to a `container=0` frame, and decorative frames do not create false containment.
9. Geometry fits the page and does not place labels or icons outside their intended cells.
10. `diagram-validation-and-evidence`'s `scripts/check_drawio.py --strict` reports no errors. It covers items 1 to 6 and the icon catalog; items 7 to 9 still need reading or a render.
11. A renderer-based check is run separately when available, and the checker runs again after the last edit.
