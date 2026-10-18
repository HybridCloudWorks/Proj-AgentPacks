#!/usr/bin/env python3
"""Check a .drawio file's structure and classify its AWS, Azure and Google Cloud icons. Standard library only.

Structure: mxfile, diagram and mxGraphModel layout, compressed pages, root cells 0 and 1, unique IDs, parent,
source and target references, parent loops, vertex and edge geometry, hidden cells, and active content in labels.

Icons: each AWS, Azure and Google Cloud shape is looked up in icon_catalog.json (next to this script), which lists
what draw.io's own libraries offer at one draw.io release. Status is one of:
  current       in the provider's current draw.io library
  legacy        an older icon set (AWS17, AWS18, AWS 3D, legacy Azure, Cloud & Enterprise, pre-2025 Google Cloud)
  retired       draw.io's "AWS (retired)" palette: a service AWS has retired
  unknown       not in the catalog: usually a misspelled name. draw.io draws an unknown AWS or Google Cloud
                name as a plain coloured square with no symbol, and an unknown Azure path as a broken image
  unattributed  an embedded or linked image whose provider cannot be told from the style

Usage: python check_drawio.py <file.drawio> [--json] [--strict] [--catalog PATH]
  --strict  report legacy and retired icons as errors instead of warnings
Exit status: 0 no errors, 1 errors found, 2 the file could not be read or parsed.
"""
from __future__ import annotations

import argparse
import base64
import json
import re
import sys
import xml.etree.ElementTree as ET
import zlib
from pathlib import Path
from urllib.parse import unquote

HERE = Path(__file__).resolve().parent
ACTIVE_CONTENT = re.compile(r"(?i)<\s*script|javascript:|<[^>]*\son[a-z]+\s*=")
AWS_CUSTOM = {"resourceIcon", "productIcon", "group", "groupCenter"}


def parse_style(style: str) -> dict[str, str]:
    out: dict[str, str] = {}
    for part in (style or "").split(";"):
        if not part:
            continue
        key, sep, value = part.partition("=")
        out[key.strip()] = value.strip() if sep else ""
    return out


def classify(style: dict[str, str], catalog: dict) -> tuple[str, str, str, str] | None:
    """Return (provider, library, status, name) for a provider icon style, or None for any other shape."""
    shape, image = style.get("shape", ""), style.get("image", "")
    aws_lists = catalog.get("aws4", {})

    def aws(name: str) -> tuple[str, str, str, str]:
        if name in aws_lists.get("current", []):
            return "AWS", "AWS current (aws4)", "current", name
        if name in aws_lists.get("retired", []):
            return "AWS", "AWS (retired) (aws4r)", "retired", name
        if name in aws_lists.get("legacy", []):
            return "AWS", "AWS18 (aws4b)", "legacy", name
        return "AWS", "AWS current (aws4)", "unknown", name

    if shape.startswith("mxgraph.aws4."):
        base = shape[len("mxgraph.aws4."):]
        if base == "productIcon" or "prIcon" in style:
            return "AWS", "AWS18 (aws4b)", "legacy", style.get("prIcon", base).removeprefix("mxgraph.aws4.")
        if base == "resourceIcon":
            return aws(style.get("resIcon", "").removeprefix("mxgraph.aws4."))
        if base in ("group", "groupCenter"):
            name = style.get("grIcon", "").removeprefix("mxgraph.aws4.")
            return aws(name) if name else ("AWS", "AWS current (aws4)", "current", base)
        return aws(base)
    if shape.startswith("mxgraph.aws3d."):
        return "AWS", "AWS 3D (aws3d)", "legacy", shape[len("mxgraph.aws3d."):]
    if shape.startswith(("mxgraph.aws3.", "mxgraph.aws2.", "mxgraph.aws.")):
        return "AWS", "AWS17 or older (aws3)", "legacy", shape.split(".", 2)[-1]
    if image.startswith("img/lib/azure2/"):
        path = image[len("img/lib/azure2/"):]
        azure = catalog.get("azure2", {})
        status = "current" if path in azure.get("current", []) else "legacy" if path in azure.get("legacy", []) else "unknown"
        return "Azure", "Azure (azure2)", status, path
    if shape.startswith("mxgraph.azure.") or shape.startswith("mxgraph.mscae.") or image.startswith("img/lib/mscae/"):
        library = "legacy Azure (azure)" if shape.startswith("mxgraph.azure.") else "Cloud & Enterprise (mscae)"
        return "Azure", library, "legacy", (shape or image).split(".", 2)[-1] if shape else image
    if shape.startswith("mxgraph.gcp3."):
        name, gcp = shape[len("mxgraph.gcp3."):], catalog.get("gcp3", {})
        if name in gcp.get("core", []):
            return "Google Cloud", "Google Cloud Platform 2026 (gcp3) core product", "current", name
        if name in gcp.get("categories", []):
            return "Google Cloud", "Google Cloud Platform 2026 (gcp3) category", "current", name
        return "Google Cloud", "Google Cloud Platform 2026 (gcp3)", "unknown", name
    if shape.startswith(("mxgraph.gcp2.", "mxgraph.gcp.")):
        return "Google Cloud", "pre-2025 Google Cloud (gcp2)", "legacy", shape.split(".", 2)[-1]
    if image.startswith("data:image/"):
        return "unattributed", "embedded image", "unattributed", ""
    if image.startswith(("http://", "https://")):
        return "unattributed", "linked image (needs network to render)", "unattributed", image[:80]
    return None


def label_text(value: str) -> str:
    return re.sub(r"<[^>]+>", " ", value or "").replace("&nbsp;", " ").strip()


def decode_page(diagram: ET.Element) -> tuple[ET.Element | None, bool]:
    model = diagram.find("mxGraphModel")
    if model is not None:
        return model, False
    text = (diagram.text or "").strip()
    if not text:
        return None, False
    try:
        raw = zlib.decompress(base64.b64decode(text), -15).decode("utf-8")
        return ET.fromstring(unquote(raw)), True
    except (ValueError, zlib.error, ET.ParseError, UnicodeDecodeError):
        return None, True


def cells_of(model: ET.Element) -> list[dict]:
    """Flatten mxCell elements, including those wrapped in UserObject or object, into plain records."""
    root = model.find("root")
    out = []
    for element in list(root) if root is not None else []:
        if element.tag == "mxCell":
            cell, wrapper = element, None
        elif element.tag in ("UserObject", "object"):
            cell, wrapper = element.find("mxCell"), element
            if cell is None:
                continue
        else:
            continue
        attrs = dict(cell.attrib)
        if wrapper is not None:
            attrs["id"] = wrapper.get("id")
            attrs["value"] = wrapper.get("label", "")
        geometry = cell.find("mxGeometry")
        out.append({"id": attrs.get("id"), "parent": attrs.get("parent"), "value": attrs.get("value", ""),
                    "style": attrs.get("style", ""), "vertex": attrs.get("vertex") == "1", "edge": attrs.get("edge") == "1",
                    "source": attrs.get("source"), "target": attrs.get("target"), "visible": attrs.get("visible", "1"),
                    "geometry": None if geometry is None else dict(geometry.attrib)})
    return out


def check_page(name: str, model: ET.Element, catalog: dict, strict: bool, report: dict) -> None:
    def add(kind: str, cell_id: str | None, message: str) -> None:
        report[kind].append({"page": name, "cell": cell_id, "message": message})

    if model.tag != "mxGraphModel" or model.find("root") is None:
        add("errors", None, "page has no mxGraphModel with a root element")
        return
    cells = cells_of(model)
    ids: dict[str, dict] = {}
    for cell in cells:
        if not cell["id"]:
            add("errors", None, "cell without an id")
        elif cell["id"] in ids:
            add("errors", cell["id"], "duplicate id")
        else:
            ids[cell["id"]] = cell
    if "0" not in ids:
        add("errors", "0", "root cell 0 is missing")
    if "1" not in ids:
        add("errors", "1", "default layer cell 1 is missing")
    elif ids["1"]["parent"] != "0":
        add("errors", "1", "cell 1 must have parent 0")
    for cell in cells:
        cid = cell["id"]
        if cid and cid != "0":
            if not cell["parent"]:
                add("errors", cid, "no parent")
            elif cell["parent"] not in ids:
                add("errors", cid, f"parent '{cell['parent']}' does not exist")
        seen, cursor = set(), cell
        while cursor and cursor["parent"] and cursor["parent"] in ids:
            if cursor["id"] in seen:
                add("errors", cid, "parent chain loops")
                break
            seen.add(cursor["id"])
            cursor = ids[cursor["parent"]]
        if cell["visible"] == "0":
            add("warnings", cid, "hidden cell (visible=0)")
        if ACTIVE_CONTENT.search(cell["value"] or ""):
            add("errors", cid, "label contains script, javascript: or an event-handler attribute")
        if cell["edge"]:
            report["counts"]["edges"] += 1
            for end in ("source", "target"):
                if cell[end] and cell[end] not in ids:
                    add("errors", cid, f"edge {end} '{cell[end]}' does not exist")
                elif not cell[end]:
                    add("warnings", cid, f"edge has no {end}: it is not attached to a shape")
            if cell["geometry"] is None:
                add("errors", cid, "edge has no mxGeometry (draw.io needs <mxGeometry relative=\"1\" as=\"geometry\"/>)")
        elif cell["vertex"]:
            report["counts"]["vertices"] += 1
            geometry = cell["geometry"]
            if geometry is None:
                add("errors", cid, "vertex has no mxGeometry")
            else:
                try:
                    if float(geometry.get("width", "0")) <= 0 or float(geometry.get("height", "0")) <= 0:
                        add("warnings", cid, "vertex has zero width or height")
                except ValueError:
                    add("errors", cid, "vertex geometry is not numeric")
        found = classify(parse_style(cell["style"]), catalog) if cell["vertex"] else None
        if found:
            provider, library, status, icon = found
            report["icons"].append({"page": name, "cell": cid, "label": label_text(cell["value"])[:60],
                                    "provider": provider, "library": library, "status": status, "name": icon})
            if status == "unknown":
                add("errors", cid, f"{provider} icon '{icon}' is not in the draw.io {catalog.get('drawio_version', '?')} "
                                   "catalog; draw.io draws it without its symbol")
            elif status in ("legacy", "retired"):
                add("errors" if strict else "warnings", cid, f"{provider} icon '{icon}' is {status} ({library})")
            if provider != "unattributed" and not label_text(cell["value"]):
                add("warnings", cid, f"{provider} icon has no label; confirm a nearby text names the product")


def check(path: Path, catalog: dict, strict: bool = False) -> dict:
    report: dict = {"file": str(path), "catalog": {"drawio_version": catalog.get("drawio_version"), "built": catalog.get("built")},
                    "pages": [], "errors": [], "warnings": [], "icons": [], "counts": {"vertices": 0, "edges": 0}}
    text = path.read_text(encoding="utf-8")
    if re.search(r"<!DOCTYPE|<!ENTITY", text, re.I):
        raise ValueError("the file declares a DOCTYPE or ENTITY; refusing to parse it")
    root = ET.fromstring(text)
    if root.tag == "mxGraphModel":
        report["warnings"].append({"page": "(bare model)", "cell": None, "message": "bare mxGraphModel; wrap it in mxfile and diagram"})
        pages = [("(bare model)", root, False)]
    elif root.tag == "mxfile":
        pages = []
        for index, diagram in enumerate(root.findall("diagram"), 1):
            name = diagram.get("name") or f"Page-{index}"
            model, compressed = decode_page(diagram)
            if compressed:
                report["errors"].append({"page": name, "cell": None,
                                         "message": "page is compressed; save it uncompressed so it can be reviewed and diffed"})
            if model is None:
                report["errors"].append({"page": name, "cell": None, "message": "page content could not be read"})
                continue
            pages.append((name, model, compressed))
        if not pages and not report["errors"]:
            report["errors"].append({"page": None, "cell": None, "message": "mxfile has no diagram pages"})
    else:
        raise ValueError(f"root element is <{root.tag}>, not <mxfile>")
    for name, model, _ in pages:
        report["pages"].append(name)
        check_page(name, model, catalog, strict, report)
    summary: dict[str, dict[str, int]] = {}
    for icon in report["icons"]:
        summary.setdefault(icon["provider"], {}).setdefault(icon["status"], 0)
        summary[icon["provider"]][icon["status"]] += 1
    report["icon_summary"] = summary
    report["result"] = "FAIL" if report["errors"] else "PASS"
    return report


def render_text(report: dict) -> str:
    lines = [f"file: {report['file']}", f"pages: {len(report['pages'])} ({', '.join(report['pages'])})",
             f"cells: {report['counts']['vertices']} vertices, {report['counts']['edges']} edges",
             f"catalog: draw.io {report['catalog']['drawio_version']}, built {report['catalog']['built']}"]
    for provider, statuses in sorted(report["icon_summary"].items()):
        lines.append(f"icons {provider}: " + ", ".join(f"{k} {v}" for k, v in sorted(statuses.items())))
    for kind in ("errors", "warnings"):
        lines.append(f"{kind}: {len(report[kind])}")
        lines += [f"  [{item['page']}] {item['cell'] or '-'}: {item['message']}" for item in report[kind]]
    lines.append(f"result: {report['result']}")
    return "\n".join(lines)


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    parser.add_argument("file")
    parser.add_argument("--json", action="store_true")
    parser.add_argument("--strict", action="store_true")
    parser.add_argument("--catalog", default=str(HERE / "icon_catalog.json"))
    args = parser.parse_args()
    try:
        catalog = json.loads(Path(args.catalog).read_text(encoding="utf-8"))
    except (OSError, json.JSONDecodeError) as exc:
        print(f"cannot read the icon catalog {args.catalog}: {exc}", file=sys.stderr)
        return 2
    try:
        report = check(Path(args.file), catalog, args.strict)
    except (OSError, UnicodeDecodeError, ET.ParseError, ValueError) as exc:
        print(f"cannot check {args.file}: {exc}", file=sys.stderr)
        return 2
    print(json.dumps(report, indent=2) if args.json else render_text(report))
    return 1 if report["errors"] else 0


if __name__ == "__main__":
    sys.exit(main())
