#!/usr/bin/env python3
"""Create a bounded local documentation inventory without publishing or network calls."""
from __future__ import annotations
import argparse
import json
from pathlib import Path

DOC_EXTENSIONS = {".md", ".mdx", ".rst", ".adoc", ".txt"}

def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--root", default=".")
    parser.add_argument("--out", default="documentation-inventory.json")
    args = parser.parse_args()
    root = Path(args.root).resolve()
    rows = []
    for path in sorted(root.rglob("*")):
        if not path.is_file() or ".git" in path.parts or path.suffix.lower() not in DOC_EXTENSIONS:
            continue
        text = path.read_text(encoding="utf-8", errors="replace")
        rows.append({"path": path.relative_to(root).as_posix(), "bytes": path.stat().st_size, "lines": text.count(chr(10)) + 1, "frontmatter": text.startswith("---" + chr(10)), "headings": sum(1 for line in text.splitlines() if line.startswith("#"))})
    data = {"root": str(root), "documents": rows, "document_count": len(rows), "network_access": False, "published": False}
    Path(args.out).write_text(json.dumps(data, indent=2) + chr(10), encoding="utf-8")
    print(json.dumps({"out": str(Path(args.out).resolve()), "document_count": len(rows), "published": False}))
    return 0

if __name__ == "__main__":
    raise SystemExit(main())
