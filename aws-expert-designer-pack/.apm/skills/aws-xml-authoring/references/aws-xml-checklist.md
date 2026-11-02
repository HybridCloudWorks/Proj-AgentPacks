# AWS XML Checklist

Before returning a `.drawio` file, check:

1. The XML parses with a standard parser that refuses DOCTYPE and ENTITY declarations, as `check_drawio.py` does. Draw.io XML has no namespaces.
2. `mxfile`, `diagram`, `mxGraphModel`, `root`, cells `0` and `1` exist on every page.
3. IDs are unique within each page and stable; all parent references resolve.
4. All edges have existing source and target cells.
5. `check_drawio.py --strict` from `diagram-validation-and-evidence` exits 0: every AWS icon name is in the catalog's current list, with no legacy, retired or unknown names. Record the catalog's draw.io version. Unknown services are neutral labelled shapes, not guessed icons.
6. Every AWS icon and group carries its full library style: the category `fillColor`, the `strokeColor`, `verticalLabelPosition=bottom;verticalAlign=top` for icons, and the library group keys for boundaries. Only typography differs from the library.
7. No compressed diagram payload is used when reviewable diffs are required.
8. Labels are escaped and no untrusted input is interpreted as XML markup.
9. Account, Region, VPC, Availability Zone and subnet are real containers nested in that order, and each subnet sits in exactly one Availability Zone. No cell is parented to a `container=0` cell, and decorative frames and category tiles create no containment.
10. Geometry fits the page and does not place labels or icons outside their intended cells.
11. The render through `drawio-render-export-and-review` is reviewed when Draw.io Desktop is available, and validation is completed after it. The structural checks above do not count as a visual check.
