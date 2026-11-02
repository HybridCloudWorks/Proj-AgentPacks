# XML Checklist

Before returning a `.drawio` file, check:

1. The XML parses with a standard parser that refuses DOCTYPE and ENTITY declarations, as `check_drawio.py` does. Draw.io XML has no namespaces.
2. `mxfile`, `diagram`, `mxGraphModel`, `root`, and cells `0` and `1` exist on every page.
3. IDs are unique within each page and stable; all parent references resolve.
4. All edges have existing source and target cells, and every edge carries a label.
5. Every Azure icon is a current `img/lib/azure2/` path in the `diagram-validation-and-evidence` catalog, in the palette's full style as `check_drawio.py --find "<product>"` prints it (`image;aspect=fixed;...`; the palette's `points` are optional), and no `mxgraph.azure.*`, `mxgraph.mscae.*` or `img/lib/mscae/` shape remains unless the user asked to match a legacy diagram. Other components are explicitly labelled neutral or custom shapes.
6. No compressed diagram payload is used when reviewable diffs are required.
7. Labels are escaped and no untrusted input is interpreted as XML markup.
8. Real containers have correct parentage, no cell is parented to a `container=0` frame, and decorative frames do not create false containment.
9. Geometry fits the page and does not place labels or icons outside their intended cells.
10. `diagram-validation-and-evidence`'s `scripts/check_drawio.py --strict` reports no errors. It covers items 1 to 3, the edge references in item 4, the Azure paths in item 5, item 6, and script or event-handler markup in labels. Edge labels, the Azure icon style and size, and items 7 to 9 still need reading or a render: Azure icons are images, so the checker looks up their path, not their style.
11. A renderer-based check is run separately when available, and the checker runs again after the last edit.
