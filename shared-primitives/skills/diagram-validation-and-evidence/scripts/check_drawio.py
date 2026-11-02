#!/usr/bin/env python3
"""Check a .drawio file's structure and its AWS, Azure and Google Cloud icons, or look an icon up. Standard library only.

Structure: mxfile, diagram and mxGraphModel layout, compressed pages, root cells 0 and 1, unique IDs, parent,
source and target references, parent loops, vertex and edge geometry, hidden cells, and active content in labels.

Icons: each AWS, Azure and Google Cloud shape is looked up in icon_catalog.json (next to this script), which records
every palette entry draw.io's own libraries offer at one draw.io release, with its form and full style. Status is:
  current       in the provider's current draw.io library, in the form used (AWS: service icon, resource or group)
  superseded    an Azure file draw.io still offers that icon_preferences.json marks as an older design of a product
                Microsoft now draws differently; the message names the file to use
  legacy        an older icon set (AWS17, AWS18, AWS 3D, legacy Azure, Cloud & Enterprise, pre-2025 Google Cloud)
  retired       draw.io's "AWS (retired)" palette: a service AWS has retired
  wrong-form    an AWS name the library offers only in another form: a service name used as a bare stencil draws
                its symbol without the category square, and a resource or group name inside resourceIcon draws a
                symbol on a square AWS never published
  unknown       not in the catalog: usually a misspelled name. draw.io draws an unknown AWS or Google Cloud name
                as a plain coloured square with no symbol, and an unknown Azure path as a broken image
  unattributed  an embedded or linked image whose provider cannot be told from the style

icon_preferences.json (next to this script, maintained by hand, unlike the generated catalog) records which file to
use where draw.io offers one Azure product under several paths, or where Microsoft publishes the icon outside the
Azure set, with the reason, the render evidence, the sources and the date each choice was verified.

Colours (AWS and Google Cloud stencils): the palette's fillColor, strokeColor and gradientColor are part of the icon.
  - no fillColor, or fillColor=none (or any of the three set to none) where the palette sets a colour: error. The
    parts that take the colour draw in draw.io's default white or not at all, so the icon draws incompletely.
  - a colour that differs from the palette, a colour where the palette sets none (a filled AWS boundary, for
    example), or a missing strokeColor (drawn in the default black): warning, or error with --strict. AWS, Microsoft
    and Google all forbid recolouring their icons and boundaries.

Usage: python check_drawio.py <file.drawio> [--json] [--strict] [--catalog PATH] [--preferences PATH]
       python check_drawio.py --find "<product>" [--all] [--json] [--catalog PATH] [--preferences PATH]
  --strict  report legacy, retired and superseded icons, and recoloured icons, as errors instead of warnings
  --find    print the palette entries whose title, name or palette match every word, with the full style to copy;
            a product's preferred file is listed first and marked, and its superseded paths last, marked
  --all     with --find, include legacy and retired entries
Exit status: 0 no errors (or --find matched), 1 errors found (or --find matched nothing), 2 the file, the catalog or
the preferences could not be read or parsed. A compressed page that inflates to more than 10 MB is reported as an
error and not decoded.
"""
from __future__ import annotations

import argparse
import base64
import json
import re
import sys
# Only parse_xml below parses, and it refuses DOCTYPE and ENTITY declarations first.
import xml.etree.ElementTree as ET  # nosec B405
import zlib
from pathlib import Path
from urllib.parse import unquote

HERE = Path(__file__).resolve().parent
PREFERENCES = HERE / "icon_preferences.json"
# An event-handler attribute starts after whitespace, a slash or a closing quote: HTML parsers read <svg/onload=...>
# and <img src="x"onerror=...> as attributes too.
ACTIVE_CONTENT = re.compile(r"(?i)<\s*script|javascript:|<[^>]*[\s/\"']on[a-z]+\s*=")
DECLARATIONS = re.compile(r"(?i)<!DOCTYPE|<!ENTITY")
# A compressed page is inflated only up to this size, so a small hostile file cannot exhaust memory.
MAX_PAGE_BYTES = 10 * 1024 * 1024
ENTRY_FIELDS = ["name", "form", "status", "title", "palette", "w", "h"]
COLOUR_KEYS = ("fillColor", "strokeColor", "gradientColor")
# (form, key) pairs whose palette value is none and whose colour, when set anyway, does not draw. Evidence (draw.io
# Desktop 32.6.1, 2026-11-01): a strokeColor on an AWS resource stencil changes nothing visible.
INVISIBLE_WHEN_NONE = {("resource", "strokeColor")}
PROVIDER = {"aws4": "AWS", "azure2": "Azure", "gcp3": "Google Cloud"}
LIBRARY = {("aws4", "current"): "AWS current (aws4)", ("aws4", "retired"): "AWS (retired) (aws4r)",
           ("aws4", "legacy"): "AWS18 (aws4b)", ("azure2", "current"): "Azure (azure2)",
           ("azure2", "legacy"): "Azure (azure2)"}
PREFERENCE_FIELDS = ("product", "preferred", "reason", "evidence", "sources", "verified")
ROLE_ORDER = {"preferred": 0, "same-icon": 1, "superseded": 2}


class PageTooLarge(ValueError):
    """A compressed page inflates to more than MAX_PAGE_BYTES."""


def parse_xml(text: str) -> ET.Element:
    """Parse XML that may come from anyone. Entity-expansion attacks need a DOCTYPE or ENTITY declaration, which is
    refused here, and ElementTree never fetches external resources, so the standard library parser is safe."""
    if DECLARATIONS.search(text):
        raise ValueError("the content declares a DOCTYPE or ENTITY; refusing to parse it")
    # Safe: declarations were refused above.
    return ET.fromstring(text)  # noqa: S314  # nosec B314


def parse_style(style: str) -> dict[str, str]:
    out: dict[str, str] = {}
    for part in (style or "").split(";"):
        if not part:
            continue
        key, sep, value = part.partition("=")
        out[key.strip()] = value.strip() if sep else ""
    return out


def _drop(prefix: str, text: str) -> str:
    return text[len(prefix):] if text.startswith(prefix) else text


def index_preferences(data: dict) -> dict[str, dict]:
    """Validate icon_preferences.json and index it by Azure path. Each path maps to its role ("preferred",
    "same-icon": another path that draws the same icon, or "superseded": an older design), the rule it belongs to,
    and for a superseded path what it draws. Raises ValueError when the file is malformed."""
    if not isinstance(data, dict) or not isinstance(data.get("azure2", []), list):
        raise ValueError("icon preferences must be an object whose 'azure2' is a list of rules")
    out: dict[str, dict] = {}

    def claim(path: object, role: str, rule: dict, draws: str = "") -> None:
        if not isinstance(path, str) or not path.endswith(".svg") or path.startswith(("/", "img/")):
            raise ValueError(f"icon preference for {rule.get('product')!r}: {path!r} is not a path under img/lib/azure2/")
        if path in out:
            raise ValueError(f"icon preference path {path} is listed more than once")
        out[path] = {"role": role, "rule": rule, "draws": draws}

    for rule in data.get("azure2", []):
        missing = [f for f in PREFERENCE_FIELDS if not (isinstance(rule, dict) and rule.get(f))]
        if missing:
            raise ValueError(f"icon preference {rule.get('product') if isinstance(rule, dict) else rule!r} "
                             f"lacks {', '.join(missing)}")
        if not isinstance(rule["sources"], list) or not all(str(s).startswith("https://") for s in rule["sources"]):
            raise ValueError(f"icon preference for {rule['product']!r}: sources must be a list of https URLs")
        if not re.fullmatch(r"\d{4}-\d{2}-\d{2}", str(rule["verified"])):
            raise ValueError(f"icon preference for {rule['product']!r}: verified must be a date (YYYY-MM-DD)")
        superseded, same = rule.get("superseded", {}), rule.get("same_icon", [])
        if not isinstance(superseded, dict) or not isinstance(same, list):
            raise ValueError(f"icon preference for {rule['product']!r}: superseded must map paths to what they draw, "
                             "and same_icon must be a list of paths")
        claim(rule["preferred"], "preferred", rule)
        for path in same:
            claim(path, "same-icon", rule)
        for path, draws in superseded.items():
            if not draws:
                raise ValueError(f"icon preference for {rule['product']!r}: say what {path} draws")
            claim(path, "superseded", rule, str(draws))
    return out


_DEFAULT_PREFERENCES: list[dict] = []


def default_preferences() -> dict:
    """icon_preferences.json next to this script, read once; empty when the file is absent."""
    if not _DEFAULT_PREFERENCES:
        _DEFAULT_PREFERENCES.append(json.loads(PREFERENCES.read_text(encoding="utf-8")) if PREFERENCES.is_file() else {})
    return _DEFAULT_PREFERENCES[0]


class Index:
    """The catalog's palette entries, indexed by library, form and name, with the hand-maintained icon preferences
    (icon_preferences.json next to this script unless others are given)."""

    def __init__(self, catalog: dict, preferences: dict | None = None) -> None:
        self.catalog = catalog
        self.preferences = index_preferences(default_preferences() if preferences is None else preferences)
        self.version = catalog.get("drawio_version", "?")
        self.entries: dict[str, list[dict]] = {}
        self.by_key: dict[tuple[str, str, str], list[dict]] = {}
        self.by_name: dict[tuple[str, str], list[dict]] = {}
        prefixes, palettes = catalog.get("prefixes", []), catalog.get("palettes", [])
        for library in PROVIDER:
            rows = []
            for row in catalog.get(library, {}).get("entries", []):
                entry = dict(zip(ENTRY_FIELDS, row))
                entry["library"] = library
                entry["palette"] = palettes[row[4]] if isinstance(row[4], int) and row[4] < len(palettes) else row[4]
                entry["style"] = (prefixes[row[7]] if row[7] >= 0 else "") + row[8]
                entry["keys"] = parse_style(entry["style"])
                rows.append(entry)
            if not rows:  # an older catalog with name lists only: no forms, styles or colour checks
                kinds = {"aws4": [("current", "any", "current"), ("retired", "any", "retired"), ("legacy", "any", "legacy")],
                         "azure2": [("current", "image", "current")],
                         "gcp3": [("core", "core", "current"), ("categories", "category", "current")]}[library]
                for kind, form, status in kinds:
                    rows += [{"name": n, "form": form, "status": status, "title": n, "palette": "", "w": 0, "h": 0,
                              "style": "", "keys": {}, "library": library} for n in catalog.get(library, {}).get(kind, [])]
            self.entries[library] = rows
            for entry in rows:
                self.by_key.setdefault((library, entry["form"], entry["name"]), []).append(entry)
                self.by_name.setdefault((library, entry["name"]), []).append(entry)
        azure = catalog.get("azure2", {})
        self.azure_legacy = set(azure.get("legacy", []))
        self.azure_case = dict(azure.get("case_mismatch", {}))

    def preference_of(self, entry: dict) -> dict | None:
        """The icon preference that names this palette entry's file, if any."""
        return self.preferences.get(entry["name"]) if entry.get("library") == "azure2" else None


_INDEXES: dict[int, Index] = {}


def index_of(catalog) -> Index:
    if isinstance(catalog, Index):
        return catalog
    key = id(catalog)
    if key not in _INDEXES or _INDEXES[key].catalog is not catalog:
        _INDEXES[key] = Index(catalog)
    return _INDEXES[key]


def _best(entries: list[dict]) -> tuple[str, list[dict]]:
    for status in ("current", "retired", "legacy"):
        chosen = [e for e in entries if e["status"] == status]
        if chosen:
            return status, chosen
    return "unknown", []


def lookup(style: dict[str, str], catalog) -> dict | None:
    """Classify a provider icon style: provider, library, status, name, form, the matching palette entries and an
    optional message. None for any other shape."""
    index = index_of(catalog)
    shape, image = style.get("shape", ""), style.get("image", "")
    found = {"entries": [], "message": "", "form": ""}
    if shape.startswith("mxgraph.aws4."):
        base = shape[len("mxgraph.aws4."):]
        if base == "productIcon" or "prIcon" in style:
            name = _drop("mxgraph.aws4.", style.get("prIcon", base))
            return {**found, "provider": "AWS", "library": "AWS18 (aws4b)", "status": "legacy", "name": name, "form": "product"}
        if base == "resourceIcon":
            form, name = "service", _drop("mxgraph.aws4.", style.get("resIcon", ""))
        elif base in ("group", "groupCenter"):
            form, name = "group", _drop("mxgraph.aws4.", style.get("grIcon", ""))
            if not name:
                return {**found, "provider": "AWS", "library": "AWS current (aws4)", "status": "current", "name": base, "form": form}
        else:
            form, name = "resource", base
        status, entries = _best(index.by_key.get(("aws4", form, name), []) + index.by_key.get(("aws4", "any", name), []))
        others = [e for e in index.by_name.get(("aws4", name), []) if e["form"] not in (form, "any")]
        current_forms = sorted({e["form"] for e in others if e["status"] == "current"})
        usage = {"service": f"shape=mxgraph.aws4.resourceIcon;resIcon=mxgraph.aws4.{name}",
                 "resource": f"shape=mxgraph.aws4.{name}", "group": f"shape=mxgraph.aws4.group;grIcon=mxgraph.aws4.{name}",
                 "product": "an AWS18 productIcon"}
        forms = current_forms or sorted({e["form"] for e in others})
        advice = (f"use {' or '.join(usage.get(f, f) for f in forms)} with the palette's colours "
                  f"(check_drawio.py --find \"{name}\")")
        if status == "unknown" and forms:
            found["message"] = (f"AWS icon '{name}' is offered only as a {' or '.join(forms)} icon, not as a {form}; {advice}")
            status = "wrong-form"
        elif status in ("legacy", "retired") and current_forms:
            found["hint"] = f"; the current library offers '{name}' as a {' or '.join(current_forms)} icon: {advice}"
        library = LIBRARY.get(("aws4", status), "AWS current (aws4)")
        return {**found, "provider": "AWS", "library": library, "status": status, "name": name, "form": form, "entries": entries}
    if shape.startswith("mxgraph.aws3d."):
        return {**found, "provider": "AWS", "library": "AWS 3D (aws3d)", "status": "legacy", "name": shape[len("mxgraph.aws3d."):]}
    if shape.startswith(("mxgraph.aws3.", "mxgraph.aws2.", "mxgraph.aws.")):
        return {**found, "provider": "AWS", "library": "AWS17 or older (aws3)", "status": "legacy", "name": shape.split(".", 2)[-1]}
    if image.startswith("img/lib/azure2/"):
        path = image[len("img/lib/azure2/"):]
        status, entries = _best(index.by_name.get(("azure2", path), []))
        if status == "unknown" and path in index.azure_case:
            found["message"] = (f"Azure path '{path}' is the spelling draw.io's palette inserts, but the file is "
                                f"'{index.azure_case[path]}'; this spelling draws a broken image in draw.io Desktop and "
                                f"on app.diagrams.net. Use image=img/lib/azure2/{index.azure_case[path]}")
        elif status == "unknown" and path in index.azure_legacy:
            status = "legacy"
        preference = index.preferences.get(path)
        if status == "current" and preference and preference["role"] == "superseded":
            rule = preference["rule"]
            status = "superseded"
            label = f", labelled \"{rule['label']}\"" if rule.get("label") else ""
            found["superseded"] = (f"it draws {preference['draws']}, not Microsoft's current icon for {rule['product']}. "
                                   f"Use image=img/lib/azure2/{rule['preferred']}{label} (icon_preferences.json, "
                                   f"verified {rule['verified']})")
        return {**found, "provider": "Azure", "library": "Azure (azure2)", "status": status, "name": path, "form": "image",
                "entries": entries}
    if shape.startswith("mxgraph.azure.") or shape.startswith("mxgraph.mscae.") or image.startswith("img/lib/mscae/"):
        library = "legacy Azure (azure)" if shape.startswith("mxgraph.azure.") else "Cloud & Enterprise (mscae)"
        return {**found, "provider": "Azure", "library": library, "status": "legacy",
                "name": (shape or image).split(".", 2)[-1] if shape else image}
    if shape.startswith("mxgraph.gcp3."):
        name = shape[len("mxgraph.gcp3."):]
        status, entries = _best(index.by_name.get(("gcp3", name), []))
        kind = {"core": " core product", "category": " category"}.get(entries[0]["form"] if entries else "", "")
        return {**found, "provider": "Google Cloud", "library": f"Google Cloud Platform 2026 (gcp3){kind}", "status": status,
                "name": name, "form": entries[0]["form"] if entries else "", "entries": entries}
    if shape.startswith(("mxgraph.gcp2.", "mxgraph.gcp.")):
        return {**found, "provider": "Google Cloud", "library": "pre-2025 Google Cloud (gcp2)", "status": "legacy",
                "name": shape.split(".", 2)[-1]}
    if image.startswith("data:image/"):
        return {**found, "provider": "unattributed", "library": "embedded image", "status": "unattributed", "name": ""}
    if image.startswith(("http://", "https://")):
        return {**found, "provider": "unattributed", "library": "linked image (needs network to render)",
                "status": "unattributed", "name": image[:80]}
    return None


def classify(style: dict[str, str], catalog) -> tuple[str, str, str, str] | None:
    """Return (provider, library, status, name) for a provider icon style, or None for any other shape."""
    found = lookup(style, catalog)
    return None if found is None else (found["provider"], found["library"], found["status"], found["name"])


def _variant_findings(style: dict[str, str], entry: dict) -> list[tuple[str, str]]:
    """(kind, message) for each colour key where the style differs from one palette entry."""
    out = []
    for key in COLOUR_KEYS:
        palette = entry["keys"].get(key)
        value = style.get(key)
        lowered = value.lower() if value is not None else None
        if palette is None or palette.lower() == "none":
            if lowered in (None, "none"):
                continue
            if key == "gradientColor":
                out.append(("recoloured", f"gradientColor={value} adds a gradient the palette does not have"))
            elif palette is not None and (entry.get("form"), key) not in INVISIBLE_WHEN_NONE:
                # The palette's none is a value too: a fill on an AWS boundary whose palette leaves it unfilled draws.
                out.append(("recoloured", f"{key}={value} differs from draw.io's palette ({key}=none): it adds a "
                                          "colour the palette leaves out; providers forbid recolouring their icons "
                                          "and boundaries"))
            continue
        if lowered == palette.lower():
            continue
        if lowered == "none" or (lowered is None and key == "fillColor"):
            what = f"{key}=none" if lowered == "none" else f"no {key}"
            out.append(("incomplete", f"has {what} where draw.io's palette sets {key}={palette}, so the parts that take "
                                      "it do not draw: the icon draws incompletely"))
        elif lowered is None:
            out.append(("recoloured", f"has no {key}, so draw.io draws it in its default colour instead of the "
                                      f"palette's {key}={palette}"))
        else:
            out.append(("recoloured", f"{key}={value} differs from draw.io's palette ({key}={palette}); providers "
                                      "forbid recolouring their icons"))
    return out


def colour_findings(style: dict[str, str], entries: list[dict]) -> list[tuple[str, str]]:
    """(kind, message) for each colour key that differs from the palette: kind 'incomplete' or 'recoloured'.

    draw.io can offer one name several times with different colours (an AWS public and private subnet are both
    group_security_group), so a style passes when it matches every colour of any one palette entry. Otherwise it is
    reported against the closest entry, named by its palette title.

    Evidence (draw.io Desktop 32.6.1, 2026-11-01): an AWS service icon without fillColor draws white on white, and
    without strokeColor draws a black symbol; an AWS resource without fillColor draws nothing visible; an AWS group
    without strokeColor draws a black frame and icon; an AWS group with a fillColor where the palette sets none draws
    a filled boundary; a Google Cloud icon without fillColor loses the parts that take it. A resource stencil's
    strokeColor has no visible effect, and the palette sets it to none (INVISIBLE_WHEN_NONE)."""
    variants = [e for e in entries if e.get("style")]
    if not variants:
        return []
    scored = [(sum(kind == "incomplete" for kind, _ in found), len(found), entry["title"], found)
              for entry in variants for found in [_variant_findings(style, entry)]]
    best = min(scored, key=lambda item: item[:3])
    if not best[3]:
        return []
    titles = {entry["title"] for entry in variants}
    suffix = f" (compared with the palette entry '{best[2]}')" if len(titles) > 1 else ""
    return [(kind, message + suffix) for kind, message in best[3]]


def label_text(value: str) -> str:
    return re.sub(r"<[^>]+>", " ", value or "").replace("&nbsp;", " ").strip()


def inflate(data: bytes, limit: int = MAX_PAGE_BYTES) -> bytes:
    """Inflate a raw deflate stream (draw.io's compressed page), refusing more than `limit` bytes of output."""
    inflater = zlib.decompressobj(-15)
    out = inflater.decompress(data, limit + 1)
    if len(out) > limit:
        raise PageTooLarge(f"page is compressed and inflates to more than {limit / 1048576:g} MB; it was not decoded "
                           "or checked (a diagram page that large is corrupt or hostile)")
    if not inflater.eof:
        raise zlib.error("incomplete or truncated deflate stream")
    return out


def decode_page(diagram: ET.Element) -> tuple[ET.Element | None, bool, str]:
    """(model, compressed, problem): the page's mxGraphModel, decoding a compressed page, or None and why not."""
    model = diagram.find("mxGraphModel")
    if model is not None:
        return model, False, ""
    text = (diagram.text or "").strip()
    if not text:
        return None, False, "page content could not be read"
    try:
        raw = inflate(base64.b64decode(text)).decode("utf-8")
    except PageTooLarge as exc:
        return None, True, str(exc)
    except (ValueError, zlib.error, UnicodeDecodeError):
        return None, True, "page content could not be read"
    try:
        return parse_xml(unquote(raw)), True, ""
    except ET.ParseError:
        return None, True, "page content could not be read"


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


def check_page(name: str, model: ET.Element, catalog, strict: bool, report: dict) -> None:
    def add(kind: str, cell_id: str | None, message: str) -> None:
        report[kind].append({"page": name, "cell": cell_id, "message": message})

    index = index_of(catalog)
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
        style = parse_style(cell["style"])
        found = lookup(style, index) if cell["vertex"] else None
        if not found:
            continue
        provider, library, status, icon = found["provider"], found["library"], found["status"], found["name"]
        report["icons"].append({"page": name, "cell": cid, "label": label_text(cell["value"])[:60], "provider": provider,
                                "library": library, "status": status, "name": icon, "form": found["form"]})
        if found["message"]:
            add("errors", cid, found["message"])
        elif status == "unknown":
            add("errors", cid, f"{provider} icon '{icon}' is not in the draw.io {index.version} catalog; draw.io draws it "
                               "without its symbol")
        elif status in ("legacy", "retired"):
            add("errors" if strict else "warnings", cid, f"{provider} icon '{icon}' is {status} ({library}){found.get('hint', '')}")
        elif status == "superseded":
            add("errors" if strict else "warnings", cid, f"{provider} icon '{icon}' is superseded: {found['superseded']}")
        if provider in ("AWS", "Google Cloud") and found["entries"] and status != "legacy":
            for kind, message in colour_findings(style, found["entries"]):
                severity = "errors" if kind == "incomplete" or strict else "warnings"
                add(severity, cid, f"{provider} icon '{icon}' {message}")
        if provider != "unattributed" and not label_text(cell["value"]):
            add("warnings", cid, f"{provider} icon has no label; confirm a nearby text names the product")


def check(path: Path, catalog, strict: bool = False) -> dict:
    index = index_of(catalog)
    report: dict = {"file": str(path), "catalog": {"drawio_version": index.version, "built": index.catalog.get("built")},
                    "pages": [], "errors": [], "warnings": [], "icons": [], "counts": {"vertices": 0, "edges": 0}}
    root = parse_xml(path.read_text(encoding="utf-8"))
    if root.tag == "mxGraphModel":
        report["warnings"].append({"page": "(bare model)", "cell": None, "message": "bare mxGraphModel; wrap it in mxfile and diagram"})
        pages = [("(bare model)", root, False)]
    elif root.tag == "mxfile":
        pages = []
        for number, diagram in enumerate(root.findall("diagram"), 1):
            name = diagram.get("name") or f"Page-{number}"
            model, compressed, problem = decode_page(diagram)
            if compressed:
                report["errors"].append({"page": name, "cell": None,
                                         "message": "page is compressed; save it uncompressed so it can be reviewed and diffed"})
            if model is None:
                report["errors"].append({"page": name, "cell": None, "message": problem or "page content could not be read"})
                continue
            pages.append((name, model, compressed))
        if not pages and not report["errors"]:
            report["errors"].append({"page": None, "cell": None, "message": "mxfile has no diagram pages"})
    else:
        raise ValueError(f"root element is <{root.tag}>, not <mxfile>")
    for name, model, _ in pages:
        report["pages"].append(name)
        check_page(name, model, index, strict, report)
    summary: dict[str, dict[str, int]] = {}
    for icon in report["icons"]:
        summary.setdefault(icon["provider"], {}).setdefault(icon["status"], 0)
        summary[icon["provider"]][icon["status"]] += 1
    report["icon_summary"] = summary
    report["result"] = "FAIL" if report["errors"] else "PASS"
    return report


def find(catalog, query: str, include_old: bool = False) -> tuple[list[dict], int]:
    """Palette entries whose title, name, palette or provider contain every word of the query, best match first,
    and the number of legacy or retired matches left out.

    The icon preferences shape the list: a preferred file also matches its product name and label, a match on a
    superseded or same-icon path brings in the preferred file, a preferred file ranks at least as high as the best
    match among its product's paths, with its same-icon copies right after it, and superseded paths come last."""
    index = index_of(catalog)
    words = query.lower().split()
    wanted = " ".join(words)
    matches = []
    for library, entries in index.entries.items():
        for entry in entries:
            if not entry.get("style"):
                continue
            preference = index.preference_of(entry)
            extra = [preference["rule"]["product"], preference["rule"].get("label", "")] \
                if preference and preference["role"] == "preferred" else []
            haystack = " ".join([entry["title"], entry["name"].replace("_", " "), entry["name"], entry["palette"],
                                 PROVIDER[library], "gcp" if library == "gcp3" else ""] + extra).lower()
            if all(word in haystack for word in words):
                matches.append(entry)
    hidden = 0 if include_old else sum(1 for e in matches if e["status"] != "current")
    if not include_old:
        matches = [e for e in matches if e["status"] == "current"]
    present = {e["name"] for e in matches if e["library"] == "azure2"}
    for entry in list(matches):
        preference = index.preference_of(entry)
        target = preference["rule"]["preferred"] if preference and preference["role"] != "preferred" else ""
        if target and target not in present:
            offered = [e for e in index.by_name.get(("azure2", target), []) if e.get("style") and e["status"] == "current"]
            if offered:
                matches.append(offered[0])
                present.add(target)
    rank = {"current": 0, "retired": 1, "legacy": 2}

    def key(entry: dict) -> tuple:
        preference = index.preference_of(entry)
        names = [entry["title"].lower()]
        if preference and preference["role"] == "preferred":
            names += [preference["rule"]["product"].lower(), preference["rule"].get("label", "").lower()]
        closeness = min((name != wanted, not name.startswith(wanted)) for name in [n for n in names if n] or [""])
        return closeness + (rank.get(entry["status"], 3), len(entry["title"]), entry["title"])

    def group(position: int, entry: dict) -> tuple:
        """Paths of one preferred product sort together; any other entry is its own group, in catalog order."""
        preference = index.preference_of(entry)
        return ("azure2", preference["rule"]["preferred"]) if preference else ("", position)

    groups: dict[tuple, tuple] = {}
    for position, entry in enumerate(matches):
        best = groups.get(group(position, entry))
        groups[group(position, entry)] = min(best, key(entry)) if best else key(entry)

    def order(item: tuple) -> tuple:
        position, entry = item
        preference = index.preference_of(entry)
        role = ROLE_ORDER[preference["role"]] if preference else 0
        return (role == ROLE_ORDER["superseded"], groups[group(position, entry)], group(position, entry), role, key(entry))

    return [entry for _, entry in sorted(enumerate(matches), key=order)], hidden


def preference_note(index: Index, entry: dict) -> dict | None:
    """What the icon preferences say about a palette entry, for --find output; None when they say nothing."""
    preference = index.preference_of(entry)
    if not preference:
        return None
    rule = preference["rule"]
    note = {"role": preference["role"], "product": rule["product"], "use": f"img/lib/azure2/{rule['preferred']}",
            "reason": rule["reason"], "verified": rule["verified"]}
    if rule.get("label"):
        note["label"] = rule["label"]
    if preference["draws"]:
        note["draws"] = preference["draws"]
    return note


def render_find(index: Index, query: str, matches: list[dict], hidden: int, limit: int = 20) -> str:
    lines = [f"{len(matches)} palette entries match '{query}' in the draw.io {index.version} catalog"
             + (f" ({hidden} legacy or retired hidden; add --all)" if hidden else "")]
    renamed = {v: k for k, v in index.azure_case.items()}
    for entry in matches[:limit]:
        w, h = entry["w"], entry["h"]
        note = preference_note(index, entry)
        status = "superseded" if note and note["role"] == "superseded" else entry["status"]
        lines.append(f"- {PROVIDER[entry['library']]} {status} {entry['form']}: {entry['title']} "
                     f"[{entry['palette']}] default size {w:g}x{h:g}")
        lines.append(f"  {entry['style']}")
        if entry["name"] in renamed:
            lines.append(f"  note: draw.io's palette inserts '{renamed[entry['name']]}', which draws a broken image; "
                         "this style uses the file's own spelling")
        if note and note["role"] == "preferred":
            label = f"; label it \"{note['label']}\"" if note.get("label") else ""
            lines.append(f"  preferred: the file to use for {note['product']}{label} (icon_preferences.json)")
        elif note and note["role"] == "same-icon":
            lines.append(f"  same icon as {note['use']}, the preferred path for {note['product']}; use that path")
        elif note:
            lines.append(f"  superseded: draws {note['draws']}; use {note['use']} for {note['product']}")
    if len(matches) > limit:
        lines.append(f"... {len(matches) - limit} more; refine the words")
    return "\n".join(lines)


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
    parser.add_argument("file", nargs="?")
    parser.add_argument("--json", action="store_true")
    parser.add_argument("--strict", action="store_true")
    parser.add_argument("--find", metavar="PRODUCT")
    parser.add_argument("--all", action="store_true")
    parser.add_argument("--catalog", default=str(HERE / "icon_catalog.json"))
    parser.add_argument("--preferences", default=str(PREFERENCES))
    args = parser.parse_args()
    if not args.file and not args.find:
        parser.error("give a .drawio file to check, or --find \"<product>\"")
    try:
        catalog = json.loads(Path(args.catalog).read_text(encoding="utf-8"))
    except (OSError, json.JSONDecodeError) as exc:
        print(f"cannot read the icon catalog {args.catalog}: {exc}", file=sys.stderr)
        return 2
    try:
        index = Index(catalog, json.loads(Path(args.preferences).read_text(encoding="utf-8")))
    except (OSError, ValueError) as exc:  # json.JSONDecodeError is a ValueError
        print(f"cannot read the icon preferences {args.preferences}: {exc}", file=sys.stderr)
        return 2
    if args.find:
        matches, hidden = find(index, args.find, args.all)
        if args.json:
            rows = []
            for entry in matches:
                row = {k: entry[k] for k in ENTRY_FIELDS + ["library", "style"]}
                note = preference_note(index, entry)
                if note:
                    row["preference"] = note
                rows.append(row)
            print(json.dumps(rows, indent=1))
        else:
            print(render_find(index, args.find, matches, hidden))
        return 0 if matches else 1
    try:
        report = check(Path(args.file), index, args.strict)
    except (OSError, UnicodeDecodeError, ET.ParseError, ValueError) as exc:
        print(f"cannot check {args.file}: {exc}", file=sys.stderr)
        return 2
    print(json.dumps(report, indent=2) if args.json else render_text(report))
    return 1 if report["errors"] else 0


if __name__ == "__main__":
    sys.exit(main())
