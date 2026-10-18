#!/usr/bin/env python3
"""Run static safety and reference checks on an uncompressed Draw.io file."""
from __future__ import annotations

import argparse
import re
import sys
import xml.etree.ElementTree as ET
from pathlib import Path


def local(tag: str) -> str:
    return tag.rsplit("}", 1)[-1]


def validate(path: Path) -> list[str]:
    errors: list[str] = []
    try:
        root = ET.fromstring(path.read_text(encoding="utf-8"))
    except (OSError, ET.ParseError) as exc:
        return [f"XML parse failure: {exc}"]
    if local(root.tag) != "mxfile":
        errors.append("root element is not mxfile")
    diagrams = [e for e in root.iter() if local(e.tag) == "diagram"]
    if not diagrams:
        errors.append("missing diagram element")
    cells = [e for e in root.iter() if local(e.tag) == "mxCell"]
    by_id: dict[str, object] = {}
    for cell in cells:
        ident = cell.attrib.get("id")
        if not ident:
            errors.append("mxCell without id")
        elif ident in by_id:
            errors.append(f"duplicate cell id: {ident}")
        else:
            by_id[ident] = cell
    for required in ("0", "1"):
        if required not in by_id:
            errors.append(f"missing root cell {required}")
    for cell in cells:
        ident = cell.attrib.get("id", "<unknown>")
        parent = cell.attrib.get("parent")
        if ident not in ("0",) and parent and parent not in by_id:
            errors.append(f"{ident}: missing parent {parent}")
        if cell.attrib.get("edge") == "1":
            for attr in ("source", "target"):
                ref = cell.attrib.get(attr)
                if not ref or ref not in by_id:
                    errors.append(f"{ident}: missing {attr} reference {ref}")
        style = cell.attrib.get("style", "")
        if "image=" in style:
            match = re.search(r"(?:^|;)image=([^;]+)", style)
            if match and not match.group(1).startswith(("img/lib/aws4/", "img/lib/general/")):
                errors.append(f"{ident}: unsupported image path {match.group(1)}")
        if "mxgraph.aws." in style:
            errors.append(f"{ident}: legacy AWS shape syntax")
        if "mxgraph.aws4." in style and not ("shape=mxgraph.aws4." in style or "resIcon=mxgraph.aws4." in style):
            errors.append(f"{ident}: unsupported AWS4 style syntax")
    payload = path.read_text(encoding="utf-8")
    if "compressed=\"true\"" in payload or "<diagram" in payload and "<mxGraphModel" not in payload:
        errors.append("diagram appears compressed or lacks inline mxGraphModel")
    return errors


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("path", type=Path)
    args = parser.parse_args()
    errors = validate(args.path)
    if errors:
        for error in errors:
            print(f"FAIL: {error}")
        return 1
    print(f"PASS: {args.path}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
