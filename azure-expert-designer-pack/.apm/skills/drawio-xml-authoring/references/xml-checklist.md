# XML Checklist

Before returning a `.drawio` file, check:

1. XML parses with a namespace-aware parser.
2. `mxfile`, `diagram`, `mxGraphModel`, `root`, cells `0` and `1` exist.
3. IDs are unique and stable; all parent references resolve.
4. All edges have existing source and target cells.
5. All image paths match the Azure2 catalog or are explicitly labeled as neutral/custom.
6. No compressed diagram payload is used when reviewable diffs are required.
7. Labels are escaped and no untrusted input is interpreted as XML markup.
8. Real containers have correct parentage; decorative frames do not create false containment.
9. Geometry fits the page and does not place labels or icons outside their intended cells.
10. A renderer-based check is run separately when available.
