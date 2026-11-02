"""Guards for the draw.io files and diagram guidance this pack ships. Offline: standard library only,
no draw.io, network or AWS access.

Every .drawio file in the pack (templates and test fixtures) must pass the shared checker in strict mode,
draw AWS boundaries with draw.io's own "AWS / Groups" styles nested account > Region > VPC > Availability
Zone > subnet, keep each icon's full palette style, and never parent a cell to anything but a real
boundary container. These are the defects the 2026-11-01 review found (AWS-01, AWS-02, AWS-03, AWS-06,
AWS-13). The pre-PR review of the same day added two more: every edge carries a label (F6: one of two twin
egress edges had none), and an AWS icon sits inside a Region frame unless it is an external actor or a global
service (an Amazon S3 bucket drawn outside the Region reads as global). The same file ships in the AWS Expert
Designer and AWS Cloud Architect packs.
"""
from __future__ import annotations

import re
import subprocess
import sys
import unittest
import xml.etree.ElementTree as ET
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
SKILLS = ROOT / ".apm" / "skills"
CHECKER = SKILLS / "diagram-validation-and-evidence" / "scripts" / "check_drawio.py"
SHARED = {"drawio-core-generation", "diagram-validation-and-evidence", "drawio-render-export-and-review"}
DRAWIO = sorted(p for p in ROOT.rglob("*.drawio") if "dist" not in p.relative_to(ROOT).parts)
REMOVED_VALIDATOR = "validate_drawio" + "_xml"

# draw.io "AWS / Groups" palette, Sidebar-AWS4.js at draw.io 32.6.9: the colour keys of each boundary.
GROUPS = {
    "group_aws_cloud_alt": {"strokeColor": "#232F3E", "fillColor": "none", "fontColor": "#232F3E", "dashed": "0"},
    "group_account": {"strokeColor": "#CD2264", "fillColor": "none", "fontColor": "#CD2264", "dashed": "0"},
    "group_region": {"strokeColor": "#00A4A6", "fillColor": "none", "fontColor": "#147EBA", "dashed": "1"},
    "group_vpc2": {"strokeColor": "#8C4FFF", "fillColor": "none", "fontColor": "#AAB7B8", "dashed": "0"},
}
SUBNETS = {  # group_security_group;grStroke=0
    "private": {"strokeColor": "#00A4A6", "fillColor": "#E6F6F7", "fontColor": "#147EBA", "dashed": "0"},
    "public": {"strokeColor": "#7AA116", "fillColor": "#F2F6E8", "fontColor": "#248814", "dashed": "0"},
}
AZ = {"strokeColor": "#147EBA", "fillColor": "none", "fontColor": "#147EBA", "dashed": "1"}
# Which boundary may hold which: account > Region > VPC > Availability Zone > subnet.
ALLOWED_PARENT = {"region": {"account", "cloud", "layer"}, "vpc": {"region"}, "az": {"vpc"}, "subnet": {"az"}}
BOUNDARY_LABEL = re.compile(r"^(AWS account|AWS Region|VPC|Availability Zone|Public subnet|Private subnet)\b")
# AWS icons a pack file may draw outside every Region: external actors and global services. Add a name here only
# when a pack file draws such an icon (for example cloudfront or route_53); a Regional resource never belongs here.
OUTSIDE_REGION = {"users"}


def style_of(cell: ET.Element) -> dict[str, str]:
    out: dict[str, str] = {}
    for part in (cell.get("style") or "").split(";"):
        if part:
            key, _, value = part.partition("=")
            out[key] = value
    return out


def kind(cell: ET.Element) -> str | None:
    """Classify a cell as a library boundary, or None when it is not one."""
    s = style_of(cell)
    icon = s.get("grIcon", "").removeprefix("mxgraph.aws4.")
    if s.get("shape") == "mxgraph.aws4.group":
        return {"group_account": "account", "group_aws_cloud_alt": "cloud", "group_region": "region",
                "group_vpc2": "vpc", "group_security_group": "subnet"}.get(icon, "other-group")
    if all(s.get(k) == v for k, v in AZ.items()) and "shape" not in s:
        return "az"
    return None


def pages(path: Path):
    root = ET.parse(path).getroot()
    for diagram in root.iter("diagram"):
        model = diagram.find("mxGraphModel")
        if model is not None:
            yield diagram.get("name"), {c.get("id"): c for c in model.iter("mxCell")}


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

    def test_boundaries_use_library_group_styles(self):
        for path in DRAWIO:
            for page, cells in pages(path):
                for cid, cell in cells.items():
                    s, label = style_of(cell), re.sub(r"<[^>]+>", " ", cell.get("value") or "")
                    with self.subTest(file=path.name, page=page, cell=cid):
                        if BOUNDARY_LABEL.match(label):
                            self.assertIsNotNone(kind(cell), f"{label!r} is drawn without draw.io's AWS group style")
                        if s.get("shape") != "mxgraph.aws4.group":
                            continue
                        icon = s.get("grIcon", "").removeprefix("mxgraph.aws4.")
                        if icon in GROUPS:
                            expected = [GROUPS[icon]]
                        elif icon == "group_security_group":
                            self.assertEqual("0", s.get("grStroke"), "library subnet styles set grStroke=0")
                            expected = list(SUBNETS.values())
                        else:
                            continue
                        colours = {k: s.get(k) for k in expected[0]}
                        self.assertIn(colours, expected, f"{icon} colours differ from the library")
                        self.assertEqual("1", s.get("container"), "library group styles are containers")

    def test_nesting_and_parents(self):
        for path in DRAWIO:
            for page, cells in pages(path):
                kinds = {cid: kind(cell) for cid, cell in cells.items()}
                for cid, cell in cells.items():
                    parent = cell.get("parent")
                    if parent is None or parent not in cells:
                        continue
                    parent_cell = cells[parent]
                    parent_is_layer = parent_cell.get("vertex") != "1"
                    with self.subTest(file=path.name, page=page, cell=cid):
                        if not parent_is_layer:
                            self.assertEqual("1", style_of(parent_cell).get("container"),
                                             f"{cid} is parented to {parent}, which is not a container")
                            self.assertIn(kinds[parent], {"account", "cloud", "region", "vpc", "az", "subnet"},
                                          f"{cid} is parented to {parent}, which is not an AWS boundary (category tile?)")
                        rule = ALLOWED_PARENT.get(kinds[cid] or "")
                        if rule:
                            self.assertIn("layer" if parent_is_layer else kinds[parent], rule,
                                          f"{kinds[cid]} {cid} must sit in one of {sorted(rule)}")

    def test_aws_icons_keep_palette_style(self):
        for path in DRAWIO:
            for page, cells in pages(path):
                for cid, cell in cells.items():
                    s = style_of(cell)
                    shape = s.get("shape", "")
                    if not shape.startswith("mxgraph.aws4.") or shape == "mxgraph.aws4.group":
                        continue
                    with self.subTest(file=path.name, page=page, cell=cid):
                        self.assertNotIn(s.get("fillColor"), (None, "", "none"), "palette fillColor missing")
                        self.assertIn("strokeColor", s)
                        self.assertEqual("bottom", s.get("verticalLabelPosition"))
                        self.assertEqual("top", s.get("verticalAlign"))
                        self.assertEqual("fixed", s.get("aspect"))
                        if shape == "mxgraph.aws4.resourceIcon":
                            self.assertEqual("#ffffff", s.get("strokeColor"))

    def test_every_edge_is_labelled(self):
        """The legend reads cost-bearing paths from edge labels, and twin edges must say the same thing."""
        for path in DRAWIO:
            for page, cells in pages(path):
                for cid, cell in cells.items():
                    if cell.get("edge") != "1":
                        continue
                    with self.subTest(file=path.name, page=page, cell=cid):
                        label = re.sub(r"<[^>]+>", " ", cell.get("value") or "").strip()
                        self.assertTrue(label, f"edge {cid} has no label")

    def test_aws_icons_sit_in_a_region(self):
        """A Regional resource, such as an Amazon S3 bucket, is drawn inside its Region frame; at page level or
        inside only the account it reads as global."""
        for path in DRAWIO:
            for page, cells in pages(path):
                kinds = {cid: kind(cell) for cid, cell in cells.items()}
                for cid, cell in cells.items():
                    s = style_of(cell)
                    shape = s.get("shape", "")
                    if (cell.get("vertex") != "1" or not shape.startswith("mxgraph.aws4.")
                            or shape in ("mxgraph.aws4.group", "mxgraph.aws4.groupCenter")):
                        continue
                    name = (s.get("resIcon", "") if shape == "mxgraph.aws4.resourceIcon" else shape)
                    name = name.removeprefix("mxgraph.aws4.")
                    if name in OUTSIDE_REGION:
                        continue
                    ancestors, cursor = [], cell.get("parent")
                    while cursor in cells and cursor not in ancestors:
                        ancestors.append(cursor)
                        cursor = cells[cursor].get("parent")
                    with self.subTest(file=path.name, page=page, cell=cid):
                        self.assertIn("region", [kinds[a] for a in ancestors],
                                      f"AWS icon '{name}' ({cid}) is not inside a Region frame")

    def test_removed_validator_is_not_referenced(self):
        self.assertFalse((ROOT / "tooling" / f"{REMOVED_VALIDATOR}.py").exists())
        for path in ROOT.rglob("*"):
            rel = path.relative_to(ROOT)
            if not path.is_file() or "dist" in rel.parts or path.suffix not in (".md", ".yml", ".yaml", ".py", ".json", ".drawio"):
                continue
            with self.subTest(file=rel.as_posix()):
                self.assertFalse(REMOVED_VALIDATOR in path.read_text(encoding="utf-8", errors="replace"),
                                 f"{rel.as_posix()} still mentions the removed pack-local validator")

    def test_pack_skills_route_to_shared_checker(self):
        own = [p for p in SKILLS.glob("*/SKILL.md") if p.parent.name not in SHARED]
        diagram_skills = [p for p in own if "drawio" in p.read_text(encoding="utf-8").lower()
                          or "draw.io" in p.read_text(encoding="utf-8").lower()]
        self.assertTrue(diagram_skills)
        for path in diagram_skills:
            text = path.read_text(encoding="utf-8")
            with self.subTest(skill=path.parent.name):
                self.assertFalse("aws-architecture-diagram`" in text, "routes to an unshipped, unvetted skill")
                self.assertIsNone(re.search(r"(?i)inside a 120x120 colou?red category container", text),
                                  "parents icons to category containers")
                for shared in ("drawio-core-generation", "diagram-validation-and-evidence"):
                    self.assertIn(shared, text, f"does not route to {shared}")

    def test_visual_rules_state_library_values(self):
        rules = SKILLS / "aws-icons-and-visual-language" / "references" / "aws-visual-rules.md"
        if not rules.is_file():
            self.skipTest("this pack ships no AWS visual rules")
        text = rules.read_text(encoding="utf-8")
        for value in ("group_region", "group_vpc2", "group_security_group;grStroke=0", "group_account",
                      "#7AA116", "#F2F6E8", "#E6F6F7", "#AAB7B8", "#CD2264", "container=0"):
            with self.subTest(value=value):
                self.assertIn(value, text)
        self.assertNotRegex(text, r"(?i)text colou?r matches the stroke")
        self.assertNotRegex(text, r"(?i)Region groups use `container=0`")


if __name__ == "__main__":
    unittest.main()
