"""Guards for the draw.io files and diagram guidance this pack ships. Offline: standard library only, no draw.io,
network or Azure access.

Every .drawio file in the pack (the skeleton, where the pack ships one, and the test fixture) must pass the pack's own
copy of the shared checker in strict mode, and keep the Azure rules that the checker does not decide:

- each Azure icon starts with the palette style that `check_drawio.py --find` prints for its path, keeps
  `aspect=fixed` and the palette's aspect ratio, appends only the palette's optional `points`, typography and label
  placement (never `whiteSpace=wrap`), and is 48 px on its longest side, or 24 px for a scope icon;
- no cell is parented to a decorative `container=0` frame, or to any other vertex that is not a real container;
- no subnet sits inside a zone frame, by parent or by position: an Azure subnet spans every zone of its region;
- each scope icon (management group, subscription, resource group, VNet, subnet) is labelled with its scope;
- every edge carries a label;
- nothing mentions the pack's former Draw.io helper, removed in 1.5.0.

The 2026-11-01 review (F9) found these rules checked only by an unshipped script. The 1.4.0 fixture, embedded below,
passes the strict checker but breaks three of them, so the negative tests show that each guard can fail. The same
file ships in the Azure Expert Designer and Azure Cloud Architect packs; a check whose files a pack does not ship is
skipped.
"""
from __future__ import annotations

import functools
import json
import re
import subprocess
import sys
import unittest
import xml.etree.ElementTree as ET
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
SKILLS = ROOT / ".apm" / "skills"
CHECKER = SKILLS / "diagram-validation-and-evidence" / "scripts" / "check_drawio.py"
DRAWIO = sorted(p for p in ROOT.rglob("*.drawio") if "dist" not in p.relative_to(ROOT).parts)
REMOVED_VALIDATOR = "validate_drawio" + "_xml"
AZURE = "img/lib/azure2/"
PALETTE_PREFIX = "image;aspect=fixed;html=1;align=center;fontSize=12;image=" + AZURE
# What a pack may append after the palette style: the palette's connection points, typography and label placement.
APPENDABLE = {"points", "fontFamily", "fontSize", "fontStyle", "fontColor", "align", "verticalAlign", "labelPosition",
              "verticalLabelPosition", "spacing", "spacingLeft", "spacingRight", "spacingTop", "spacingBottom",
              "labelBackgroundColor"}
SERVICE_PX, SCOPE_PX = 48.0, 24.0
# Scope icons sit in a frame's top-left corner, labelled with the frame's name; the label must name the scope.
SCOPE_ICONS = {
    "general/Management_Groups.svg": re.compile(r"(?i)management group"),
    "general/Subscriptions.svg": re.compile(r"(?i)subscription"),
    "general/Resource_Groups.svg": re.compile(r"(?i)resource group"),
    "networking/Virtual_Networks.svg": re.compile(r"(?i)\bvnet\b|virtual network"),
    "networking/Subnet.svg": re.compile(r"(?i)subnet"),
}
ZONE_FRAME_LABEL = re.compile(r"(?i)^(availability\s+)?zones?(\s|:|$)")
SUBNET_FRAME_LABEL = re.compile(r"(?i)^subnet\b")
# Guidance whose icon-style wording must match what the shared tools print (review finding F4).
GUIDANCE = [SKILLS / "azure-icons-and-visual-language" / "SKILL.md",
            SKILLS / "azure-icons-and-visual-language" / "references" / "azure-visual-rules.md",
            SKILLS / "drawio-xml-authoring" / "SKILL.md",
            SKILLS / "drawio-xml-authoring" / "references" / "xml-checklist.md",
            ROOT / "README.md"]
POINTS_REQUIRED = re.compile(r"(?i)\b(plus|followed by)\b[^.\n]{0,30}`points")

# tests/fixtures/minimal.drawio as shipped in 1.4.0 (`git show <1.4.0>:azure-expert-designer-pack/tests/fixtures/
# minimal.drawio`): a generic image style, 120 px icons, and the icons and edge parented to a container=0 frame.
FIXTURE_1_4_0 = (
    '<mxfile host="app.diagrams.net" version="24.7.17"><diagram id="azure-minimal" name="Page-1">'
    '<mxGraphModel><root><mxCell id="0" /><mxCell id="1" parent="0" />'
    '<mxCell id="region" value="Azure Region" style="rounded=1;whiteSpace=wrap;html=1;container=0;fontFamily=Helvetica;'
    'fillColor=#F5F5F5;strokeColor=#9E9E9E;" vertex="1" parent="1">'
    '<mxGeometry x="40" y="40" width="420" height="220" as="geometry" /></mxCell>'
    '<mxCell id="app_service" value="Azure App Service" style="shape=image;aspect=fixed;html=1;'
    'image=img/lib/azure2/app_services/App_Services.svg;fontFamily=Helvetica;" vertex="1" parent="region">'
    '<mxGeometry x="80" y="90" width="120" height="120" as="geometry" /></mxCell>'
    '<mxCell id="storage" value="Azure Storage" style="shape=image;aspect=fixed;html=1;'
    'image=img/lib/azure2/storage/Storage_Accounts.svg;fontFamily=Helvetica;" vertex="1" parent="region">'
    '<mxGeometry x="280" y="90" width="120" height="120" as="geometry" /></mxCell>'
    '<mxCell id="edge_app_storage" value="HTTPS" style="edgeStyle=orthogonalEdgeStyle;rounded=0;orthogonalLoop=1;'
    'jettySize=auto;html=1;fontFamily=Helvetica;endArrow=block;" edge="1" parent="region" source="app_service" '
    'target="storage"><mxGeometry relative="1" as="geometry" /></mxCell>'
    '</root></mxGraphModel></diagram></mxfile>')


def style_of(text: str | None) -> dict[str, str]:
    out: dict[str, str] = {}
    for part in (text or "").split(";"):
        if part:
            key, _, value = part.partition("=")
            out[key.strip()] = value.strip()
    return out


def label(value: str | None) -> str:
    return re.sub(r"<[^>]+>", " ", value or "").replace("&nbsp;", " ").strip()


def pages(text: str):
    """(page name, {id: cell}) for each uncompressed page. Compressed pages are left to the strict checker."""
    if re.search(r"(?i)<!DOCTYPE|<!ENTITY", text):
        raise ValueError("refusing a DOCTYPE or ENTITY declaration")
    root = ET.fromstring(text)
    for number, diagram in enumerate(root.iter("diagram"), 1):
        model = diagram.find("mxGraphModel")
        if model is None or model.find("root") is None:
            continue
        cells: dict[str, dict] = {}
        for element in model.find("root"):
            if element.tag == "mxCell":
                cell, ident, value = element, element.get("id"), element.get("value", "")
            elif element.tag in ("UserObject", "object") and element.find("mxCell") is not None:
                cell, ident, value = element.find("mxCell"), element.get("id"), element.get("label", "")
            else:
                continue
            geometry = cell.find("mxGeometry")
            cells[ident] = {"id": ident, "parent": cell.get("parent"), "value": value, "raw": cell.get("style") or "",
                            "style": style_of(cell.get("style")), "vertex": cell.get("vertex") == "1",
                            "edge": cell.get("edge") == "1", "geometry": {} if geometry is None else dict(geometry.attrib)}
        yield diagram.get("name") or f"Page-{number}", cells


def number(geometry: dict, key: str) -> float:
    try:
        return float(geometry.get(key) or 0)
    except ValueError:
        return 0.0


def azure_path(cell: dict) -> str | None:
    image = cell["style"].get("image", "")
    return image[len(AZURE):] if cell["vertex"] and image.startswith(AZURE) else None


def is_text(cell: dict) -> bool:
    return "text" in cell["style"] or cell["style"].get("shape") == "text"


def parent_vertex(cells: dict, cell: dict) -> dict | None:
    parent = cells.get(cell["parent"] or "")
    return parent if parent is not None and parent["vertex"] else None


def ancestors(cells: dict, cell: dict):
    seen = {cell["id"]}
    parent = parent_vertex(cells, cell)
    while parent is not None and parent["id"] not in seen:
        seen.add(parent["id"])
        yield parent
        parent = parent_vertex(cells, parent)


def box(cells: dict, cell: dict) -> tuple[float, float, float, float]:
    """Absolute (left, top, right, bottom): a child's geometry is relative to its parent vertex."""
    g = cell["geometry"]
    x, y = number(g, "x"), number(g, "y")
    for parent in ancestors(cells, cell):
        x, y = x + number(parent["geometry"], "x"), y + number(parent["geometry"], "y")
    return x, y, x + number(g, "width"), y + number(g, "height")


@functools.lru_cache(maxsize=None)
def palette(path: str) -> tuple[dict, ...]:
    """The current palette entries for an Azure path, as `check_drawio.py --find <path> --json` prints them."""
    proc = subprocess.run([sys.executable, "-B", str(CHECKER), "--find", path, "--json"], capture_output=True, text=True)
    if proc.returncode not in (0, 1):
        raise RuntimeError(proc.stdout + proc.stderr)
    return tuple(e for e in json.loads(proc.stdout or "[]")
                 if e.get("library") == "azure2" and e.get("name") == path and e.get("status") == "current")


def icon_problems(cells: dict) -> list[str]:
    out = []
    for cid, cell in cells.items():
        path = azure_path(cell)
        if path is None:
            continue
        entries = palette(path)
        if not entries:
            out.append(f"{cid}: {path} is not a current palette entry (check_drawio.py --find)")
            continue
        raw = cell["raw"] if cell["raw"].endswith(";") else cell["raw"] + ";"
        matched = next((e for e in entries if raw.startswith(e["style"])), None)
        if matched is None:
            out.append(f"{cid}: style does not start with the palette style {entries[0]['style']!r}")
        else:
            extra = sorted(set(style_of(raw[len(matched['style']):])) - APPENDABLE)
            if extra:
                out.append(f"{cid}: appends {', '.join(extra)}; append only points, typography and label placement")
        if cell["style"].get("aspect") != "fixed":
            out.append(f"{cid}: aspect=fixed is missing or overridden")
        if cell["style"].get("whiteSpace") == "wrap":
            out.append(f"{cid}: whiteSpace=wrap wraps the product label to the icon's width")
        w, h = number(cell["geometry"], "width"), number(cell["geometry"], "height")
        longest = max(w, h)
        if abs(longest - SERVICE_PX) > 0.05 and not (path in SCOPE_ICONS and abs(longest - SCOPE_PX) <= 0.05):
            size = "48 px, or 24 px for a scope icon" if path in SCOPE_ICONS else "48 px"
            out.append(f"{cid}: {w:g}x{h:g}; the longest side must be {size}")
        if h and not any(e["h"] and abs((w / h) / (e["w"] / e["h"]) - 1) <= 0.01 for e in entries):
            out.append(f"{cid}: {w:g}x{h:g} distorts the palette's aspect ratio {entries[0]['w']:g}x{entries[0]['h']:g}")
    return out


def parent_problems(cells: dict) -> list[str]:
    out = []
    for cid, cell in cells.items():
        parent = parent_vertex(cells, cell)
        if parent is None:
            continue
        container = parent["style"].get("container")
        if container == "0":
            out.append(f"{cid}: parented to decorative frame {parent['id']} (container=0)")
        elif container != "1":
            out.append(f"{cid}: parented to {parent['id']}, which is not a real container (container=1)")
    return out


def subnets(cells: dict) -> set[str]:
    found = set()
    for cid, cell in cells.items():
        if azure_path(cell) == "networking/Subnet.svg":
            found.add(cid)
            parent = parent_vertex(cells, cell)
            if parent is not None and parent["style"].get("container") == "1":
                found.add(parent["id"])
        elif cell["vertex"] and not is_text(cell) and azure_path(cell) is None and SUBNET_FRAME_LABEL.match(label(cell["value"])):
            found.add(cid)
    return found


def zone_problems(cells: dict) -> list[str]:
    zones = [c for c in cells.values() if c["vertex"] and not is_text(c) and azure_path(c) is None
             and ZONE_FRAME_LABEL.match(label(c["value"]))]
    out = []
    for sid in sorted(subnets(cells)):
        subnet = cells[sid]
        left, top, right, bottom = box(cells, subnet)
        for zone in zones:
            z_left, z_top, z_right, z_bottom = box(cells, zone)
            if any(a["id"] == zone["id"] for a in ancestors(cells, subnet)):
                out.append(f"{sid}: subnet is a child of zone frame {zone['id']}")
            elif z_left <= left and z_top <= top and right <= z_right and bottom <= z_bottom:
                out.append(f"{sid}: subnet is drawn inside zone frame {zone['id']}")
    return out


def scope_label_problems(cells: dict) -> list[str]:
    out = []
    for cid, cell in cells.items():
        path = azure_path(cell)
        if path in SCOPE_ICONS and not SCOPE_ICONS[path].search(label(cell["value"])):
            out.append(f"{cid}: scope icon {path} is not labelled with its scope (label {label(cell['value'])!r})")
    return out


def edge_label_problems(cells: dict) -> list[str]:
    out = []
    for cid, cell in cells.items():
        if not cell["edge"] or label(cell["value"]):
            continue
        if not any(c["parent"] == cid and label(c["value"]) for c in cells.values()):
            out.append(f"{cid}: edge has no label")
    return out


def all_problems(text: str) -> dict[str, list[str]]:
    found: dict[str, list[str]] = {}
    for _, cells in pages(text):
        for name, rule in (("icons", icon_problems), ("parents", parent_problems), ("zones", zone_problems),
                           ("scope labels", scope_label_problems), ("edge labels", edge_label_problems)):
            found.setdefault(name, []).extend(rule(cells))
    return found


def page_with(cells_xml: str) -> str:
    return ('<mxfile><diagram name="P"><mxGraphModel><root><mxCell id="0" /><mxCell id="1" parent="0" />'
            + cells_xml + "</root></mxGraphModel></diagram></mxfile>")


def vertex(cid: str, style: str, parent: str = "1", value: str = "x", x: float = 0, y: float = 0,
           w: float = 48, h: float = 48) -> str:
    return (f'<mxCell id="{cid}" value="{value}" style="{style}" vertex="1" parent="{parent}">'
            f'<mxGeometry x="{x}" y="{y}" width="{w}" height="{h}" as="geometry" /></mxCell>')


FRAME = "rounded=0;html=1;container=1;"
SUBNET_ICON = PALETTE_PREFIX + "networking/Subnet.svg;fontFamily=Helvetica;"


class DrawioAssetTests(unittest.TestCase):
    def test_pack_ships_drawio_files(self):
        self.assertTrue(DRAWIO, "expected at least the test fixture")

    def test_strict_checker_passes(self):
        self.assertTrue(CHECKER.is_file(), CHECKER)
        for path in DRAWIO:
            with self.subTest(file=path.name):
                proc = subprocess.run([sys.executable, "-B", str(CHECKER), "--strict", str(path)],
                                      capture_output=True, text=True)
                self.assertEqual(0, proc.returncode, proc.stdout + proc.stderr)

    def test_azure_invariants(self):
        for path in DRAWIO:
            for rule, problems in all_problems(path.read_text(encoding="utf-8")).items():
                with self.subTest(file=path.relative_to(ROOT).as_posix(), rule=rule):
                    self.assertEqual([], problems)

    def test_files_use_azure_icons(self):
        icons = [azure_path(c) for path in DRAWIO for _, cells in pages(path.read_text(encoding="utf-8"))
                 for c in cells.values() if azure_path(c)]
        self.assertTrue(icons, "the icon guards need at least one Azure icon to check")

    def test_removed_validator_is_not_referenced(self):
        self.assertFalse((ROOT / "tooling" / f"{REMOVED_VALIDATOR}.py").exists())
        for path in ROOT.rglob("*"):
            rel = path.relative_to(ROOT)
            if not path.is_file() or "dist" in rel.parts or path.suffix not in (".md", ".yml", ".yaml", ".py", ".json", ".drawio"):
                continue
            with self.subTest(file=rel.as_posix()):
                self.assertNotIn(REMOVED_VALIDATOR, path.read_text(encoding="utf-8", errors="replace"),
                                 f"{rel.as_posix()} still mentions the removed pack-local validator")

    def test_icon_guidance_matches_the_shared_tools(self):
        present = [p for p in GUIDANCE if p.is_file()]
        if not any(PALETTE_PREFIX in p.read_text(encoding="utf-8") for p in present):
            self.skipTest("this pack ships no Azure icon-style guidance")
        for path in present:
            text = path.read_text(encoding="utf-8")
            with self.subTest(file=path.relative_to(ROOT).as_posix()):
                required = POINTS_REQUIRED.search(text)
                self.assertIsNone(required, required and f"{required.group(0)!r}: requires the palette's points, "
                                                         "which --find and the catalog leave out")
                self.assertFalse("namespace-aware" in text,
                                 "says 'namespace-aware'; draw.io XML has no namespaces and the checker uses a plain parser")
                if PALETTE_PREFIX in text:
                    self.assertIn("--find", text, "quotes the palette style without pointing to check_drawio.py --find")


class GuardsCanFail(unittest.TestCase):
    """Each guard fails on a known defect, so a pass on the shipped files means something."""

    def test_1_4_0_fixture_fails(self):
        found = all_problems(FIXTURE_1_4_0)
        self.assertTrue(any("does not start with the palette style" in p for p in found["icons"]), found)
        self.assertTrue(any("120x120" in p for p in found["icons"]), found)
        # both icons and the edge between them are children of the decorative region frame
        self.assertEqual(3, sum("container=0" in p for p in found["parents"]), found)

    def test_subnet_inside_zone_frame_fails(self):
        by_position = page_with(
            vertex("zone1", "rounded=0;html=1;container=0;dashed=1;", value="Zone 1", w=400, h=400)
            + vertex("vnet", FRAME, value="", x=20, y=20, w=300, h=300)
            + vertex("snet", FRAME, parent="vnet", value="", x=20, y=40, w=200, h=200)
            + vertex("snet_icon", SUBNET_ICON, parent="snet", value="Subnet: app", x=12, y=10, w=24, h=14.37))
        self.assertEqual(2, len(all_problems(by_position)["zones"]))
        by_parent = page_with(
            vertex("zone1", FRAME, value="Availability zone 1", w=400, h=400)
            + vertex("snet", FRAME, parent="zone1", value="Subnet: app", x=20, y=40, w=200, h=200))
        self.assertTrue(any("child of zone frame" in p for p in all_problems(by_parent)["zones"]))
        across = page_with(
            vertex("zone1", "rounded=0;html=1;container=0;", value="Zone 1", w=200, h=400)
            + vertex("snet", FRAME, value="Subnet: app", x=20, y=40, w=400, h=200))
        self.assertEqual([], all_problems(across)["zones"], "a subnet drawn across zones is correct")

    def test_unlabelled_scope_icon_and_edge_fail(self):
        found = all_problems(page_with(
            vertex("rg", FRAME, value="", w=300, h=300)
            + vertex("rg_icon", PALETTE_PREFIX + "general/Resource_Groups.svg;", parent="rg", value="",
                     w=24, h=22.59)
            + vertex("a", "rounded=1;", x=400) + vertex("b", "rounded=1;", x=600)
            + '<mxCell id="e" value="" style="edgeStyle=orthogonalEdgeStyle;" edge="1" parent="1" source="a" '
              'target="b"><mxGeometry relative="1" as="geometry" /></mxCell>'))
        self.assertEqual(1, len(found["scope labels"]), found)
        self.assertEqual(["e: edge has no label"], found["edge labels"])

    def test_wrapped_or_distorted_icon_fails(self):
        found = all_problems(page_with(
            vertex("wrapped", PALETTE_PREFIX + "app_services/App_Services.svg;whiteSpace=wrap;", value="App Service")
            + vertex("squashed", PALETTE_PREFIX + "storage/Storage_Accounts.svg;", value="Storage", w=48, h=48)
            + vertex("small", PALETTE_PREFIX + "app_services/App_Services.svg;", value="App Service", w=24, h=24)))
        icons = " | ".join(found["icons"])
        self.assertIn("wrapped: appends whiteSpace", icons)
        self.assertIn("wrapped: whiteSpace=wrap", icons)
        self.assertIn("squashed: 48x48 distorts", icons)
        self.assertIn("small: 24x24; the longest side must be 48 px", icons)

    def test_child_of_non_container_fails(self):
        found = all_problems(page_with(vertex("box", "rounded=0;html=1;", w=300, h=300)
                                       + vertex("child", "rounded=1;", parent="box")))
        self.assertEqual(["child: parented to box, which is not a real container (container=1)"], found["parents"])


if __name__ == "__main__":
    unittest.main()
