"""Tests for the shared pack tooling. Run: python -m unittest discover -s tooling/tests -v"""
from __future__ import annotations

import base64
import contextlib
import html
import http.client
import importlib.util
import io
import json
import shutil
import socket
import subprocess
import sys
import tempfile
import time
import unittest
import urllib.error
import zlib
from html.parser import HTMLParser
from pathlib import Path
from unittest import mock
from urllib.parse import quote

REPO = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(REPO / "tooling"))

import build_icon_catalog  # noqa: E402
import check_collisions  # noqa: E402
import ci_plan  # noqa: E402
import generate_pack  # noqa: E402
import restructure_pack  # noqa: E402
import skill_coverage  # noqa: E402
import sync_shared  # noqa: E402
import validate_pack  # noqa: E402

EXEMPLAR = REPO / "python-distinguished-engineer-pack"
CHECKER = REPO / "shared-primitives" / "skills" / "diagram-validation-and-evidence" / "scripts" / "check_drawio.py"
_spec = importlib.util.spec_from_file_location("check_drawio", CHECKER)
check_drawio = importlib.util.module_from_spec(_spec)
_spec.loader.exec_module(check_drawio)
CATALOG = json.loads((CHECKER.parent / "icon_catalog.json").read_text(encoding="utf-8"))


def drawio_page(cells: str, name: str = "P") -> str:
    return (f'<mxfile><diagram name="{name}"><mxGraphModel><root><mxCell id="0"/><mxCell id="1" parent="0"/>{cells}'
            '</root></mxGraphModel></diagram></mxfile>')


def drawio_vertex(cell_id: str, style: str, value: str = "x") -> str:
    return (f'<mxCell id="{cell_id}" value="{value}" style="{style}" vertex="1" parent="1">'
            '<mxGeometry width="50" height="50" as="geometry"/></mxCell>')


def failed_checks(root: Path) -> list[str]:
    rep, _ = validate_pack.validate(root, install_check=False, write_report=False)
    return [check for _, check, status, _ in rep.rows if status == "FAIL"]


class ValidatorTests(unittest.TestCase):
    def setUp(self) -> None:
        self.tmp = Path(tempfile.mkdtemp(prefix="tooling-test-"))
        self.pack = self.tmp / EXEMPLAR.name
        shutil.copytree(EXEMPLAR, self.pack, ignore=shutil.ignore_patterns("dist", "__pycache__", "*.pyc"))

    def tearDown(self) -> None:
        shutil.rmtree(self.tmp, ignore_errors=True)

    def test_exemplar_passes(self) -> None:
        self.assertEqual(failed_checks(self.pack), [])

    def test_tools_field_on_an_agent_fails(self) -> None:
        agent = next((self.pack / ".apm" / "agents").glob("*.agent.md"))
        agent.write_text(agent.read_text(encoding="utf-8").replace("---\n", "---\ntools: [read]\n", 1), encoding="utf-8")
        self.assertTrue(any("no tools field" in c for c in failed_checks(self.pack)))

    def test_installed_content_pointing_at_docs_fails(self) -> None:
        skill = next((self.pack / ".apm" / "skills").glob("*/SKILL.md"))
        skill.write_text(skill.read_text(encoding="utf-8") + "\nSee docs/HANDOFF_CONTRACT.md.\n", encoding="utf-8")
        self.assertTrue(any("references only installed things" in c for c in failed_checks(self.pack)))

    def test_undefined_status_name_fails(self) -> None:
        skill = next((self.pack / ".apm" / "skills").glob("*/SKILL.md"))
        skill.write_text(skill.read_text(encoding="utf-8") + "\nEnd with READY_TO_SHIP.\n", encoding="utf-8")
        self.assertTrue(any("status names" in c for c in failed_checks(self.pack)))

    def test_stale_skill_coverage_fails(self) -> None:
        (self.pack / ".apm" / "skills" / "extra-skill").mkdir()
        (self.pack / ".apm" / "skills" / "extra-skill" / "SKILL.md").write_text(
            "---\nname: extra-skill\ndescription: Use when testing.\n---\n# Extra\n", encoding="utf-8")
        self.assertTrue(any("skill-coverage.yml lists exactly the shipped skills" in c for c in failed_checks(self.pack)))

    def test_empty_required_folder_fails(self) -> None:
        for f in (self.pack / "examples").iterdir():
            f.unlink() if f.is_file() else shutil.rmtree(f)
        self.assertTrue(any("required artifact examples" in c for c in failed_checks(self.pack)))

    def test_old_layout_folder_fails(self) -> None:
        (self.pack / "targets" / "claude-code").mkdir(parents=True)
        self.assertTrue(any("no stale folder targets/" in c for c in failed_checks(self.pack)))


class SkillCoverageTests(unittest.TestCase):
    def test_committed_coverage_is_current(self) -> None:
        expected = skill_coverage.render(skill_coverage.build(EXEMPLAR))
        self.assertEqual((EXEMPLAR / "tests" / "skill-coverage.yml").read_text(encoding="utf-8"), expected)


class RestructureTests(unittest.TestCase):
    def test_v1_pack_is_converted(self) -> None:
        tmp = Path(tempfile.mkdtemp(prefix="restructure-test-"))
        try:
            src = tmp / "demo-role-pack"
            files = {
                "apm.yml": "name: demo-role\nversion: 1.0.0\ndescription: Demo role.\nlicense: MIT\ncanonical:\n  agent: x\nvendor_targets:\n  - claude-code\n",
                ".apm/agents/demo-role.agent.md": "---\nname: demo-role\ndescription: Demo primary.\ntools: [read, edit, execute]\nuser-invocable: true\n---\n# Demo\n",
                ".apm/skills/demo-skill/SKILL.md": "---\nname: demo-skill\ndescription: Use when demonstrating.\n---\n# Demo skill\n",
                "instructions/demo.instructions.md": "---\napplyTo: \"**\"\n---\n# Demo instructions\nAlways be concise and accurate in this demo.\n",
                "prompts/run-demo.prompt.md": "# Run the demo\nDo it.\n",
                "targets/claude-code/.claude/agents/demo-role.md": "old target\n",
                "docs/APPROVAL_MATRIX.md": "# Approval matrix\n\nLevel 0 read. Level 1 edit. Level 2 consequential.\n",
                "tests/report-contract.yml": "statuses:\n  - COMPLETE_VERIFIED\n  - NOT_VERIFIED\n",
                "README.md": "# Demo\n\nA demonstration pack used by the tooling tests to check conversion end to end.\n",
            }
            for rel, text in files.items():
                (src / rel).parent.mkdir(parents=True, exist_ok=True)
                (src / rel).write_text(text, encoding="utf-8")
            dest = tmp / "out" / "demo-role-pack"
            restructure_pack.restructure(src, dest, EXEMPLAR / "PORTABLE_AGENT_SKILL_PACK_AUTHORING_PROMPT.md",
                                         "https://example.invalid/repo", "tester")
            agent = (dest / ".apm" / "agents" / "demo-role.agent.md").read_text(encoding="utf-8")
            self.assertNotIn("tools:", agent)
            perms = (dest / "compatibility" / "tool-permissions.yml").read_text(encoding="utf-8")
            self.assertIn("intent: [edit, read, shell]", perms)
            self.assertTrue((dest / ".apm" / "instructions" / "demo.instructions.md").is_file())
            self.assertIn("description:", (dest / ".apm" / "instructions" / "demo.instructions.md").read_text(encoding="utf-8"))
            self.assertIn("description:", (dest / ".apm" / "prompts" / "run-demo.prompt.md").read_text(encoding="utf-8"))
            self.assertTrue((dest / ".apm" / "instructions" / "demo-role-contract.instructions.md").is_file())
            self.assertFalse((dest / "targets").exists())
            manifest = (dest / "apm.yml").read_text(encoding="utf-8")
            self.assertIn("version: 1.1.0", manifest)
            self.assertNotIn("canonical:", manifest)
            self.assertIn("  - kiro", manifest)
            self.assertTrue((dest / "tests" / "skill-coverage.yml").is_file())
            self.assertTrue((src / "targets").exists(), "the source pack must be left untouched")
        finally:
            shutil.rmtree(tmp, ignore_errors=True)


class RepoToolsTests(unittest.TestCase):
    def test_collision_report_shape(self) -> None:
        found = check_collisions.collisions(REPO)
        self.assertEqual(set(found), {"agents", "skills", "instructions", "prompts"})
        for names in found.values():
            self.assertTrue(all(len(packs) > 1 for packs in names.values()))

    def test_scheduled_plan_covers_every_pack_on_three_systems(self) -> None:
        result = ci_plan.plan("schedule", "")
        self.assertEqual(result["packs"], ci_plan.all_packs())
        self.assertEqual(len(result["os"]), 3)
        self.assertEqual(result["apm"], "latest")

    def test_publish_mirrors_the_release_tags_themselves(self):
        import yaml

        steps = yaml.safe_load((REPO / ".github" / "workflows" / "publish.yml").read_text(encoding="utf-8"))
        steps = steps["jobs"]["mirror"]["steps"]

        def index(test):
            return next((i for i, step in enumerate(steps) if test(step)), None)

        checkout = index(lambda step: str(step.get("uses", "")).startswith("actions/checkout@"))
        fetch = index(lambda step: "git fetch --force --tags origin" in str(step.get("run", "")))
        push = index(lambda step: "git push dist --tags" in str(step.get("run", "")))
        self.assertNotIn(None, (checkout, fetch, push), "checkout, the tag fetch and the mirror push must all be steps")
        self.assertLess(checkout, fetch)
        self.assertLess(fetch, push, "restore the annotated tags before mirroring them")
        self.assertNotIn("if", steps[fetch], "the tag fetch must always run")

    def test_checkout_is_pinned_at_a_version_that_keeps_annotated_tags(self):
        for workflow in sorted((REPO / ".github" / "workflows").glob("*.yml")):
            for line in workflow.read_text(encoding="utf-8").splitlines():
                if "actions/checkout@" not in line:
                    continue
                ref, _, comment = line.split("actions/checkout@", 1)[1].partition("#")
                self.assertRegex(ref.strip(), r"^[0-9a-f]{40}$", f"{workflow.name}: pin checkout by commit SHA")
                version = tuple(int(part) for part in comment.strip().lstrip("v").split("."))
                self.assertGreaterEqual(version, (6, 0, 2), f"{workflow.name}: checkout before 6.0.2 makes tags lightweight")

    def test_exemplar_identity_terms(self) -> None:
        hard, skills = generate_pack.identity_terms(EXEMPLAR)
        self.assertIn("python-distinguished-engineer", hard)
        self.assertTrue(skills)

    def test_milestones_on_an_empty_workspace(self) -> None:
        tmp = Path(tempfile.mkdtemp(prefix="milestones-test-"))
        try:
            (tmp / "out" / "demo-pack").mkdir(parents=True)
            (tmp / "workspace.json").write_text(json.dumps({"name": "demo", "created": "2026-01-01T00:00:00"}), encoding="utf-8")
            items = generate_pack.milestones(tmp)
            self.assertEqual(len(items), 20)
            self.assertEqual(sum(ok for _, ok in items), 0)
        finally:
            shutil.rmtree(tmp, ignore_errors=True)

    def test_identical_copies_are_shared_not_collisions(self):
        tmp = Path(tempfile.mkdtemp(prefix="collisions-test-"))
        try:
            for pack, skills in (("a-pack", {"common": "same", "other": "one"}), ("b-pack", {"common": "same"}),
                                 ("c-pack", {"other": "two"})):
                (tmp / pack).mkdir()
                (tmp / pack / "apm.yml").write_text("name: x\nversion: 1.0.0\n", encoding="utf-8")
                for name, text in skills.items():
                    (tmp / pack / ".apm" / "skills" / name).mkdir(parents=True)
                    (tmp / pack / ".apm" / "skills" / name / "SKILL.md").write_text(text, encoding="utf-8")
            for pack, text in (("a-pack", "same prompt"), ("c-pack", "other prompt")):
                (tmp / pack / ".apm" / "prompts").mkdir(parents=True)
                (tmp / pack / ".apm" / "prompts" / "go.prompt.md").write_text(text, encoding="utf-8")
            self.assertEqual(check_collisions.collisions(tmp)["skills"], {"other": ["a-pack", "c-pack"]})
            self.assertEqual(check_collisions.shared(tmp)["skills"], {"common": ["a-pack", "b-pack"]})
            self.assertEqual(check_collisions.collisions(tmp)["prompts"], {"go": ["a-pack", "c-pack"]})
        finally:
            shutil.rmtree(tmp, ignore_errors=True)


class CheckDrawioTests(unittest.TestCase):
    def run_check(self, xml: str, strict: bool = False) -> dict:
        tmp = Path(tempfile.mkdtemp(prefix="drawio-test-"))
        try:
            path = tmp / "diagram.drawio"
            path.write_text(xml, encoding="utf-8")
            return check_drawio.check(path, CATALOG, strict)
        finally:
            shutil.rmtree(tmp, ignore_errors=True)

    @staticmethod
    def statuses(report: dict) -> dict[str, str]:
        return {icon["cell"]: icon["status"] for icon in report["icons"]}

    @staticmethod
    def palette(query: str, name: str) -> str:
        """The full palette style the catalog records for one icon, found the way an agent would find it."""
        matches, _ = check_drawio.find(CATALOG, query)
        return next(e["style"] for e in matches if e["name"] == name)

    def messages(self, style: str, strict: bool = False) -> tuple[list[str], list[str]]:
        report = self.run_check(drawio_page(drawio_vertex("v", style, "Label")), strict)
        return [e["message"] for e in report["errors"]], [w["message"] for w in report["warnings"]]

    def test_current_icons_of_all_three_providers_pass(self):
        report = self.run_check(drawio_page(
            drawio_vertex("aws", self.palette("lambda", "lambda"))
            + drawio_vertex("aws-resource", self.palette("instance", "instance2"))
            + drawio_vertex("azure", self.palette("documentdb", "databases/Azure_DocumentDB.svg"))
            + drawio_vertex("gcp-core", self.palette("cloud run", "cloudrun"))
            + drawio_vertex("gcp-category", self.palette("data analytics", "dataanalytics"))), strict=True)
        self.assertEqual(report["result"], "PASS", report["errors"])
        self.assertEqual(report["warnings"], [])
        self.assertEqual(set(self.statuses(report).values()), {"current"})
        self.assertEqual(set(report["icon_summary"]), {"AWS", "Azure", "Google Cloud"})

    def test_missing_fill_colour_draws_incompletely_and_is_an_error(self):
        cases = {"aws service": "shape=mxgraph.aws4.resourceIcon;resIcon=mxgraph.aws4.lambda;strokeColor=#ffffff;",
                 "aws resource": "shape=mxgraph.aws4.instance2;strokeColor=none;",
                 "gcp core": "shape=mxgraph.gcp3.cloudrun;",
                 "gcp category": "shape=mxgraph.gcp3.networking;",
                 "fill none": "shape=mxgraph.aws4.resourceIcon;resIcon=mxgraph.aws4.lambda;fillColor=none;strokeColor=#ffffff;"}
        for case, style in cases.items():
            errors, _ = self.messages(style)
            self.assertTrue(any("draws incompletely" in m for m in errors), f"{case}: {errors}")

    def test_recoloured_icon_warns_and_fails_when_strict(self):
        for style in ("shape=mxgraph.gcp3.cloudrun;fillColor=#EA4335;",
                      self.palette("lambda", "lambda").replace("fillColor=#ED7100", "fillColor=#232F3E"),
                      self.palette("lambda", "lambda").replace("strokeColor=#ffffff;", ""),
                      self.palette("vpc", "group_vpc2").replace("strokeColor=#8C4FFF", "strokeColor=#ED7100"),
                      self.palette("instance", "instance2").replace("gradientColor=none", "gradientColor=#FFFFFF")):
            errors, warnings = self.messages(style)
            self.assertEqual(errors, [], style)
            self.assertEqual(len(warnings), 1, (style, warnings))
            self.assertTrue(any(word in warnings[0] for word in ("differs", "default colour", "adds a gradient")), warnings)
            strict_errors, _ = self.messages(style, strict=True)
            self.assertEqual(len(strict_errors), 1, style)

    def test_colour_differences_that_do_not_draw_are_accepted(self):
        quiet = (self.palette("lambda", "lambda").replace("#ED7100", "#ed7100"),
                 self.palette("instance", "instance2").replace("strokeColor=none;", ""),
                 self.palette("instance", "instance2").replace("strokeColor=none", "strokeColor=#000000"),
                 self.palette("vpc", "group_vpc2").replace("fillColor=none;", ""))
        for style in quiet:
            self.assertEqual(self.messages(style, strict=True), ([], []), style)

    def test_any_palette_variant_of_a_name_is_accepted_but_not_a_mix_of_variants(self):
        subnets = [e for e in check_drawio.find(CATALOG, "subnet")[0] if e["name"] == "group_security_group"]
        self.assertEqual(sorted(e["title"] for e in subnets), ["Private subnet", "Public subnet"])
        for entry in subnets:
            self.assertEqual(self.messages(entry["style"], strict=True), ([], []), entry["title"])
        public = next(e["style"] for e in subnets if e["title"] == "Public subnet")
        mixed = public.replace("fillColor=#F2F6E8", "fillColor=#E6F6F7")
        errors, warnings = self.messages(mixed)
        self.assertEqual(errors, [])
        self.assertEqual(len(warnings), 1, warnings)
        self.assertIn("differs from draw.io's palette", warnings[0])
        self.assertRegex(warnings[0], r"compared with the palette entry '(Public|Private) subnet'")
        self.assertEqual(len(self.messages(mixed, strict=True)[0]), 1)
        lambda_functions = [e for e in check_drawio.find(CATALOG, "lambda function")[0] if e["name"] == "lambda_function"]
        self.assertGreater(len({e["keys"]["fillColor"] for e in lambda_functions}), 1)
        for entry in lambda_functions:
            self.assertEqual(self.messages(entry["style"], strict=True), ([], []), entry["palette"])

    def test_aws_name_in_a_form_the_palette_does_not_offer_is_an_error(self):
        cases = {"shape=mxgraph.aws4.ec2;fillColor=#ED7100;": "only as a service",
                 "shape=mxgraph.aws4.resourceIcon;resIcon=mxgraph.aws4.instance2;fillColor=#ED7100;strokeColor=#ffffff;": "only as a resource",
                 "shape=mxgraph.aws4.group_vpc2;fillColor=#8C4FFF;": "only as a group"}
        for style, expected in cases.items():
            report = self.run_check(drawio_page(drawio_vertex("v", style)))
            self.assertEqual(self.statuses(report), {"v": "wrong-form"})
            self.assertTrue(any(expected in e["message"] for e in report["errors"]), report["errors"])

    def test_legacy_aws18_form_points_to_the_current_form(self):
        report = self.run_check(drawio_page(drawio_vertex(
            "v", "shape=mxgraph.aws4.resourceIcon;resIcon=mxgraph.aws4.bucket;fillColor=#7AA116;strokeColor=#ffffff;")))
        self.assertEqual(self.statuses(report), {"v": "legacy"})
        self.assertEqual(len(report["warnings"]), 1, report["warnings"])
        self.assertIn("shape=mxgraph.aws4.bucket", report["warnings"][0]["message"])

    def test_azure_palette_spelling_with_wrong_letter_case_is_an_error(self):
        broken = self.run_check(drawio_page(drawio_vertex("v", "image;image=img/lib/azure2/management_governance/solutions.svg;")))
        self.assertEqual(self.statuses(broken), {"v": "unknown"})
        self.assertIn("management_governance/Solutions.svg", broken["errors"][0]["message"])
        fixed = self.run_check(drawio_page(drawio_vertex("v", "image;image=img/lib/azure2/management_governance/Solutions.svg;")), True)
        self.assertEqual((fixed["result"], self.statuses(fixed)), ("PASS", {"v": "current"}))

    def test_azure_icons_offered_by_full_path_are_current(self):
        for path in ("internet_of_things/Logic_Apps.svg", "internet_of_things/Time_Series_Insights_Access_Policies.svg",
                     "iot/Azure_Stack_HCI_Sizer.svg", "iot/Stack_HCI_Premium.svg"):
            report = self.run_check(drawio_page(drawio_vertex("v", f"image;image=img/lib/azure2/{path};")), strict=True)
            self.assertEqual((report["result"], self.statuses(report)), ("PASS", {"v": "current"}), path)

    def test_find_returns_the_palette_style_best_match_first(self):
        matches, _ = check_drawio.find(CATALOG, "Vertex AI")
        self.assertEqual(matches[0]["name"], "vertexai")
        self.assertIn("fillColor=#4285f4", matches[0]["style"])
        current, hidden = check_drawio.find(CATALOG, "honeycode")
        self.assertEqual((current, hidden > 0), ([], True))
        everything, _ = check_drawio.find(CATALOG, "honeycode", include_old=True)
        self.assertTrue(everything and all(e["status"] == "retired" for e in everything))
        self.assertEqual(check_drawio.find(CATALOG, "gemini"), ([], 0))
        solutions, _ = check_drawio.find(CATALOG, "solutions")
        self.assertIn("img/lib/azure2/management_governance/Solutions.svg", solutions[0]["style"])

    def test_find_command_line_exit_codes(self):
        found = subprocess.run([sys.executable, str(CHECKER), "--find", "ec2"], capture_output=True, text=True, check=False)
        self.assertEqual(found.returncode, 0, found.stderr)
        self.assertIn("resIcon=mxgraph.aws4.ec2;", found.stdout)
        missing = subprocess.run([sys.executable, str(CHECKER), "--find", "no such product"],
                                 capture_output=True, text=True, check=False)
        self.assertEqual(missing.returncode, 1)

    def test_older_name_list_catalog_still_classifies(self):
        old = {"drawio_version": "32.5.5", "aws4": {"current": ["lambda"], "retired": [], "legacy": []},
               "azure2": {"current": ["databases/SQL_Database.svg"], "legacy": ["databases/Old.svg"]},
               "gcp3": {"core": ["cloudrun"], "categories": ["networking"]}}
        cells = (drawio_vertex("a", "shape=mxgraph.aws4.resourceIcon;resIcon=mxgraph.aws4.lambda;")
                 + drawio_vertex("z", "image;image=img/lib/azure2/databases/Old.svg;")
                 + drawio_vertex("g", "shape=mxgraph.gcp3.networking;"))
        tmp = Path(tempfile.mkdtemp(prefix="drawio-test-"))
        try:
            (tmp / "d.drawio").write_text(drawio_page(cells), encoding="utf-8")
            report = check_drawio.check(tmp / "d.drawio", old)
        finally:
            shutil.rmtree(tmp, ignore_errors=True)
        self.assertEqual(self.statuses(report), {"a": "current", "z": "legacy", "g": "current"})

    def test_misspelled_names_are_errors(self):
        report = self.run_check(drawio_page(
            drawio_vertex("aws", "shape=mxgraph.aws4.resourceIcon;resIcon=mxgraph.aws4.lamda;")
            + drawio_vertex("azure", "image;image=img/lib/azure2/app_services/App_Service.svg;")
            + drawio_vertex("gcp", "shape=mxgraph.gcp3.cloud_run;")))
        self.assertEqual(set(self.statuses(report).values()), {"unknown"})
        self.assertEqual(len(report["errors"]), 3)

    def test_legacy_and_retired_icons_warn_and_fail_when_strict(self):
        cells = (drawio_vertex("aws18", "shape=mxgraph.aws4.productIcon;prIcon=mxgraph.aws4.ec2;")
                 + drawio_vertex("retired", "shape=mxgraph.aws4.resourceIcon;resIcon=mxgraph.aws4.honeycode;"
                                            "fillColor=#DD344C;strokeColor=#ffffff;")
                 + drawio_vertex("old-azure", "shape=mxgraph.azure.sql_database;")
                 + drawio_vertex("gcp2", "shape=mxgraph.gcp2.hexIcon;"))
        report = self.run_check(drawio_page(cells))
        self.assertEqual(self.statuses(report), {"aws18": "legacy", "retired": "retired", "old-azure": "legacy", "gcp2": "legacy"})
        self.assertEqual(report["result"], "PASS")
        self.assertEqual(self.run_check(drawio_page(cells), strict=True)["result"], "FAIL")

    def test_broken_references_and_duplicate_ids_are_errors(self):
        cells = (drawio_vertex("a", "rounded=1;") + drawio_vertex("a", "rounded=1;")
                 + '<mxCell id="e" edge="1" parent="1" source="a" target="missing"><mxGeometry relative="1" as="geometry"/></mxCell>'
                 + '<mxCell id="o" value="x" vertex="1" parent="nowhere"><mxGeometry width="5" height="5" as="geometry"/></mxCell>')
        messages = " | ".join(e["message"] for e in self.run_check(drawio_page(cells))["errors"])
        for expected in ("duplicate id", "edge target 'missing' does not exist", "parent 'nowhere' does not exist"):
            self.assertIn(expected, messages)

    def test_ids_are_unique_per_page_not_per_file(self):
        one = drawio_page(drawio_vertex("v", "rounded=1;"), "One")
        two = drawio_page(drawio_vertex("v", "rounded=1;"), "Two")
        xml = one[: -len("</mxfile>")] + two[len("<mxfile>"):]
        self.assertEqual(self.run_check(xml)["errors"], [])

    def test_user_object_wrapper_is_read(self):
        cell = ('<UserObject id="u" label="Cloud SQL"><mxCell style="shape=mxgraph.gcp3.cloudsql;fillColor=#4285f4;" vertex="1" parent="1">'
                '<mxGeometry width="50" height="50" as="geometry"/></mxCell></UserObject>')
        report = self.run_check(drawio_page(cell))
        self.assertEqual(report["result"], "PASS")
        self.assertEqual(report["icons"][0]["label"], "Cloud SQL")

    def test_compressed_page_is_decoded_and_reported(self):
        model = ('<mxGraphModel><root><mxCell id="0"/><mxCell id="1" parent="0"/>'
                 + drawio_vertex("g", "shape=mxgraph.gcp3.bigquery;") + '</root></mxGraphModel>')
        deflate = zlib.compressobj(9, zlib.DEFLATED, -15)
        data = deflate.compress(quote(model).encode()) + deflate.flush()
        report = self.run_check(f'<mxfile><diagram name="Z">{base64.b64encode(data).decode()}</diagram></mxfile>')
        self.assertTrue(any("compressed" in e["message"] for e in report["errors"]))
        self.assertEqual(self.statuses(report), {"g": "current"})

    def test_doctype_is_refused(self):
        with self.assertRaises(ValueError):
            self.run_check('<!DOCTYPE x [<!ENTITY a "b">]>' + drawio_page(""))

    def test_doctype_inside_a_compressed_page_is_refused(self):
        model = '<!DOCTYPE m [<!ENTITY a "b">]><mxGraphModel><root><mxCell id="0"/></root></mxGraphModel>'
        deflate = zlib.compressobj(9, zlib.DEFLATED, -15)
        data = deflate.compress(quote(model).encode()) + deflate.flush()
        with self.assertRaises(ValueError):
            self.run_check(f'<mxfile><diagram name="Z">{base64.b64encode(data).decode()}</diagram></mxfile>')

    def test_event_handler_in_label_is_an_error(self):
        report = self.run_check(drawio_page(drawio_vertex("v", "rounded=1;html=1;", "&lt;img src=x onerror=alert(1)&gt;")))
        self.assertTrue(any("event-handler" in e["message"] for e in report["errors"]))

    def test_event_handler_after_a_slash_or_a_quote_is_an_error(self):
        """HTML parsers read <svg/onload=...> and <img src="x"onerror=...> as event-handler attributes too."""
        for label in ("&lt;svg/onload=alert(1)&gt;", "&lt;img src=&quot;x&quot;onerror=alert(1)&gt;",
                      "&lt;img src='x'onerror=alert(1)&gt;"):
            report = self.run_check(drawio_page(drawio_vertex("v", "rounded=1;html=1;", label)))
            self.assertTrue(any("event-handler" in e["message"] for e in report["errors"]), label)
        benign = "&lt;a href=&quot;https://example.com/docs&quot;&gt;docs&lt;/a&gt; on time, onclick=1 as text"
        self.assertEqual(self.run_check(drawio_page(drawio_vertex("v", "rounded=1;html=1;", benign)))["errors"], [])

    def label_report(self, label_html: str, strict: bool = False) -> dict:
        """Check a one-vertex page whose label is this HTML, escaped into the XML attribute the way draw.io saves it."""
        return self.run_check(drawio_page(drawio_vertex("v", "rounded=1;html=1;", html.escape(label_html))), strict)

    # Labels that would run code if rendered as HTML, each with a phrase the reason must contain.
    ACTIVE_LABELS = {
        "<script>alert(1)</script>": "<script>",
        "<ScRiPt>alert(1)</sCrIpT>": "<script>",
        "<IMG SRC=x OnErRoR=alert(1)>": "event-handler attribute (onerror)",
        "<div><img src=x onerror  =  alert(1)></div>": "event-handler",
        '<a href="javascript:alert(1)">x</a>': "javascript: URL in href",
        '<a href="JaVaScRiPt:alert(1)">x</a>': "javascript: URL in href",
        '<a href=" \tjava\nscript:alert(1)">x</a>': "javascript: URL in href",
        '<a href="&#106;avascript:alert(1)">x</a>': "javascript: URL in href",
        '<a href="&#x6A;&#x61;vascript&colon;alert(1)">x</a>': "javascript: URL in href",
        '<a href="java&Tab;script:alert(1)">x</a>': "javascript: URL in href",
        '<a href="&#0000106;avascript:alert(1)">x</a>': "javascript: URL in href",
        '<iframe src="javascript:alert(1)"></iframe>': "javascript: URL in src",
        '<form action="javascript:alert(1)">f</form>': "javascript: URL in action",
        '<button formaction="javascript:alert(1)">b</button>': "javascript: URL in formaction",
        '<svg><a xlink:href="javascript:alert(1)"><text>x</text></a></svg>': "javascript: URL in xlink:href",
        '<object data="javascript:alert(1)"></object>': "javascript: URL in data",
        '<svg><a><animate attributeName="href" values="0;javascript:alert(1)"/><text>x</text></a></svg>': "values",
        '<svg><a><set attributeName="href" to="javascript:alert(1)"/><text>x</text></a></svg>': "to",
        '<iframe srcdoc="&lt;script&gt;alert(1)&lt;/script&gt;"></iframe>': "<script> element inside srcdoc",
        # Browsers end these comments, declarations and raw-text elements where older html.parser releases do not.
        "<!--><img src=x onerror=alert(1)>-->": "onerror",
        "<!-- --!><img src=x onerror=alert(1)>-->": "onerror",
        "<![CDATA[><img src=x onerror=alert(1)>]]>": "onerror",
        "<?x><img src=x onerror=alert(1)>": "onerror",
        "<style></style x><img src=x onerror=alert(1)>": "onerror",
        "<![CDATA[" * 6 + "x<b>]]>": "nested more than",
        # A browser ends a raw-text element at its end tag even inside what html.parser reads as an attribute value or a
        # comment (mutation XSS); noscript is raw text when scripting is on, as in the draw.io editor.
        '<noscript><p title="</noscript><img src=x onerror=alert(1)>"></noscript>': "after </noscript>",
        '<xmp><p title="</xmp><img src=x onerror=alert(1)>"></xmp>': "after </xmp>",
        '<iframe><p title="</iframe><img src=x onerror=alert(1)>"></iframe>': "after </iframe>",
        '<noembed><p title="</noembed><img src=x onerror=alert(1)>"></noembed>': "after </noembed>",
        '<noframes><p title="</noframes><img src=x onerror=alert(1)>"></noframes>': "after </noframes>",
        '<textarea><p title="</textarea><img src=x onerror=alert(1)>"></textarea>': "after </textarea>",
        '<title><p title="</title><img src=x onerror=alert(1)>"></title>': "after </title>",
        '<style><p title="</style><img src=x onerror=alert(1)>"></style>': "after </style>",
        "<noscript><!-- </noscript><img src=x onerror=alert(1)> --></noscript>": "onerror",
        'x\r\n<xmp>\r\n<p title="</xmp\n><img src=x onerror=alert(1)>"></xmp>': "after </xmp>",
        # Inside SVG or MathML these elements hold markup, not text.
        "<svg><style><img src=x onerror=alert(1)></style></svg>": "onerror",
        "<math><mtext><table><mglyph><style><img src=x onerror=alert(1)>": "onerror",
        "<title>" * 50: "nested more than",
    }
    # Labels that run nothing; each must pass --strict.
    INERT_LABELS = ['<a href="https://example.test/onboarding=1">Onboarding</a>',
                    '<a href="https://learn.example.com/path/onboarding=true">Onboarding guide</a>',
                    "<a href=https://example.test/onboarding=1>unquoted</a>", "<img src=x/onerror=alert(1)>",
                    '<font color="#FF0000">onboarding=1</font>', "<span style=\"font-family:'Open Sans'\">x</span>",
                    "<b>Front end</b>: JavaScript: React SPA", '<span title="javascript: the language">x</span>',
                    "Use &lt;script&gt; tags as text", "a < b and c > d", "< script>is text, not a tag",
                    "https://example.test/?a=1&online=1", "<div>App Service<br>P1v3</div>",
                    # Raw-text elements that end where html.parser also ends them, one after another, nested, or
                    # holding escaped markup as text.
                    "<div>a</div>\n<title>t</title>\n<b>x</b>",
                    "<noscript><style>.a{color:red}</style><b>x</b></noscript>",
                    "<textarea>&lt;script&gt;alert(1)&lt;/script&gt;</textarea>",
                    "".join(f"<xmp>{i}</xmp><title>t{i}</title>" for i in range(40))]

    def test_active_content_is_decided_from_the_label_html(self):
        """A <script> element, an on* attribute or a javascript: URL in a URL attribute, however it is spelled."""
        for label, reason in self.ACTIVE_LABELS.items():
            found = check_drawio.active_content(label)
            self.assertIn(reason, found, label)
            report = self.label_report(label)
            self.assertEqual(report["result"], "FAIL", label)
            self.assertIn(f"label contains active content: {found}", [e["message"] for e in report["errors"]], label)
        for label in self.INERT_LABELS:
            self.assertEqual(check_drawio.active_content(label), "", label)
            self.assertEqual(self.label_report(label, strict=True)["errors"], [], label)

    def test_active_content_does_not_depend_on_html_parser_raw_text_handling(self):
        """Pre-PR round 3 N3: Python 3.9's html.parser reads only script and style as raw text, later releases add
        xmp, iframe, noembed, noframes, textarea, title and plaintext, and a scripting browser adds noscript. The
        scanner never enters html.parser's raw-text mode and applies the browser's rule itself, so the verdicts are the
        same whichever lists html.parser has."""
        labels = list(self.ACTIVE_LABELS) + self.INERT_LABELS
        verdicts = [check_drawio.active_content(label) for label in labels]
        lists = {"3.9": (("script", "style"), ()),
                 "browser": (("script", "style", "xmp", "iframe", "noembed", "noframes", "noscript", "plaintext"),
                             ("textarea", "title"))}
        for name, (raw_text, escapable) in lists.items():
            with mock.patch.object(HTMLParser, "CDATA_CONTENT_ELEMENTS", raw_text), \
                    mock.patch.object(HTMLParser, "RCDATA_CONTENT_ELEMENTS", escapable, create=True):
                self.assertEqual([check_drawio.active_content(label) for label in labels], verdicts, name)
        label = "<xmp><textarea><title><style><noscript><plaintext><b>"
        scanner = check_drawio._ActiveContentScanner(label, 0, [len(label)])
        scanner.feed(label)
        self.assertIsNone(scanner.cdata_elem, "html.parser entered its raw-text mode")
        self.assertEqual([tag for _, tag, _ in scanner.raw_text],
                         ["xmp", "textarea", "title", "style", "noscript", "plaintext"])
        # Unterminated or deeply nested raw-text elements are reported, not read without bound.
        self.assertIn(check_drawio.active_content("<title>" * 2000),
                      (check_drawio.TOO_DEEP, check_drawio.TOO_MUCH))

    def test_active_content_work_grows_linearly_with_label_length(self):
        """Pre-PR round 4 N4: finish() searched from every raw-text start tag to the end of the label, so a 1 MB label of
        repeated <textarea> took 75 s, its end-tag search scanning 250,000 times the label's length. The test counts work, not
        time: the characters the raw-text end-tag patterns scan and the characters html.parser is fed must each stay
        within a small multiple of the label's length. The wall-clock limit is only a backstop."""
        scanned, parsed = [0], [0]

        class CountingPattern:
            """Delegates to a compiled pattern and counts the characters each search or finditer pass scans."""

            def __init__(self, pattern) -> None:
                self.pattern = pattern

            def search(self, text, pos=0, *args):
                match = self.pattern.search(text, pos, *args)
                scanned[0] += (match.end() if match else len(text)) - pos
                return match

            def finditer(self, text, pos=0, *args):
                scanned[0] += len(text) - pos
                return self.pattern.finditer(text, pos, *args)

        feed = check_drawio._ActiveContentScanner.feed

        def counting_feed(scanner, data):
            parsed[0] += len(data)
            return feed(scanner, data)

        counting = {tag: CountingPattern(pattern) for tag, pattern in check_drawio.RAW_TEXT_END.items()}
        shapes = {"<textarea>": 1_000_000, "<title>": 200_000, '<noscript><p title="</noscript>': 200_000,
                  '<iframe srcdoc="&lt;b&gt;">': 200_000}
        started = time.monotonic()
        for unit, size in shapes.items():
            label = (unit * (size // len(unit) + 1))[:size]
            scanned[0] = parsed[0] = 0
            with mock.patch.object(check_drawio, "RAW_TEXT_END", counting), \
                    mock.patch.object(check_drawio._ActiveContentScanner, "feed", counting_feed):
                found = check_drawio.active_content(label)
            self.assertTrue(found, unit)
            self.assertLessEqual(scanned[0], 10 * size, f"{unit}: end-tag search scanned {scanned[0] / size:.0f}x the label")
            self.assertLessEqual(parsed[0], check_drawio.REREAD_FACTOR * size + check_drawio.REREAD_SLACK, unit)
        self.assertLess(time.monotonic() - started, 120, "backstop: the hostile labels took minutes, not seconds")

    def test_link_whose_url_contains_on_passes_the_command_line_check(self):
        """Pre-PR round 2 N2: <a href=".../onboarding=true"> failed every diagram that carried it."""
        tmp = Path(tempfile.mkdtemp(prefix="drawio-test-"))
        try:
            labels = {"href.drawio": '<a href="https://learn.example.com/path/onboarding=true">Onboarding guide</a>',
                      "svg.drawio": "<svg/onload=alert(1)>", "entity.drawio": '<a href="&#106;avascript:alert(1)">x</a>'}
            codes = {}
            for name, label in labels.items():
                (tmp / name).write_text(drawio_page(drawio_vertex("v", "rounded=1;html=1;", html.escape(label))),
                                        encoding="utf-8")
                codes[name] = subprocess.run([sys.executable, str(CHECKER), str(tmp / name), "--strict"],
                                             capture_output=True, text=True, check=False).returncode
            self.assertEqual(codes, {"href.drawio": 0, "svg.drawio": 1, "entity.drawio": 1})
        finally:
            shutil.rmtree(tmp, ignore_errors=True)

    def test_compressed_page_is_inflated_only_up_to_the_size_cap(self):
        deflate = zlib.compressobj(9, zlib.DEFLATED, -15)
        small = deflate.compress(b"x" * 1000) + deflate.flush()
        self.assertEqual(len(check_drawio.inflate(small, limit=1000)), 1000)
        with self.assertRaises(check_drawio.PageTooLarge):
            check_drawio.inflate(small, limit=999)
        with self.assertRaises(zlib.error):
            check_drawio.inflate(small[:-4])
        model = ('<mxGraphModel><root><mxCell id="0"/><mxCell id="1" parent="0"/>'
                 + drawio_vertex("v", "rounded=1;", "a" * (check_drawio.MAX_PAGE_BYTES + 1)) + '</root></mxGraphModel>')
        deflate = zlib.compressobj(9, zlib.DEFLATED, -15)
        bomb = deflate.compress(quote(model).encode()) + deflate.flush()
        self.assertLess(len(bomb), 100_000, "the probe should be a small file that inflates past the cap")
        report = self.run_check(f'<mxfile><diagram name="Z">{base64.b64encode(bomb).decode()}</diagram></mxfile>')
        self.assertEqual(report["result"], "FAIL")
        self.assertTrue(any("inflates to more than 10 MB" in e["message"] for e in report["errors"]), report["errors"])
        self.assertEqual(report["icons"], [])

    def test_fill_on_a_boundary_the_palette_leaves_unfilled_is_recolouring(self):
        """A VPC group with fillColor=#FFC0CB draws a pink boundary (draw.io Desktop 32.6.1, review probe p17)."""
        vpc = self.palette("vpc", "group_vpc2")
        self.assertIn("fillColor=none", vpc)
        errors, warnings = self.messages(vpc.replace("fillColor=none", "fillColor=#FFC0CB"))
        self.assertEqual(errors, [])
        self.assertEqual(len(warnings), 1, warnings)
        self.assertIn("fillColor=#FFC0CB differs from draw.io's palette (fillColor=none)", warnings[0])
        strict_errors, _ = self.messages(vpc.replace("fillColor=none", "fillColor=#FFC0CB"), strict=True)
        self.assertEqual(len(strict_errors), 1, strict_errors)
        # Colours the probes showed draw nothing stay accepted: a resource stencil's stroke, and a stroke on a
        # Google Cloud icon, whose palette sets none.
        for quiet in (self.palette("instance", "instance2").replace("strokeColor=none", "strokeColor=#FFC0CB"),
                      self.palette("cloud run", "cloudrun").rstrip(";") + ";strokeColor=#000000;"):
            self.assertEqual(self.messages(quiet, strict=True), ([], []), quiet)

    def test_superseded_azure_files_warn_and_fail_when_strict(self):
        cases = {"identity/Azure_Active_Directory.svg": ("active directory", "other/Entra_Identity.svg",
                                                         'labelled "Microsoft Entra ID"'),
                 "networking/Private_Endpoint.svg": ("private endpoint", "other/Private_Endpoints.svg", "older")}
        for path, (query, preferred, detail) in cases.items():
            style = self.palette(query, path)
            report = self.run_check(drawio_page(drawio_vertex("v", style, "Label")))
            self.assertEqual(self.statuses(report), {"v": "superseded"}, path)
            self.assertEqual(report["errors"], [], path)
            self.assertEqual(len(report["warnings"]), 1, report["warnings"])
            for expected in (f"image=img/lib/azure2/{preferred}", detail, "icon_preferences.json"):
                self.assertIn(expected, report["warnings"][0]["message"])
            strict = self.run_check(drawio_page(drawio_vertex("v", style, "Label")), strict=True)
            self.assertEqual(strict["result"], "FAIL", path)
            self.assertIn(f"image=img/lib/azure2/{preferred}", strict["errors"][0]["message"])

    def test_preferred_and_same_icon_azure_files_pass_strict(self):
        for query, path in (("entra identity", "other/Entra_Identity.svg"), ("private endpoint", "other/Private_Endpoints.svg"),
                            ("private dns zone", "networking/DNS_Zones.svg"), ("app service", "compute/App_Services.svg"),
                            ("log analytics", "management_governance/Log_Analytics_Workspaces.svg")):
            report = self.run_check(drawio_page(drawio_vertex("v", self.palette(query, path), "Label")), strict=True)
            self.assertEqual((report["result"], report["warnings"], self.statuses(report)), ("PASS", [], {"v": "current"}), path)

    def test_find_lists_the_preferred_file_first_and_marks_the_others(self):
        def names(query: str) -> list[str]:
            return [e["name"] for e in check_drawio.find(CATALOG, query)[0]]

        self.assertEqual(names("private endpoint"), ["other/Private_Endpoints.svg", "networking/Private_Endpoint.svg"])
        # The superseded pyramid matches "active directory"; the preferred Entra ID file is brought in first, and the
        # pyramid ranks last, after every other match.
        directory = names("active directory")
        self.assertGreater(len(directory), 2)
        self.assertEqual((directory[0], directory[-1]), ("other/Entra_Identity.svg", "identity/Azure_Active_Directory.svg"))
        for query in ("private endpoint", "active directory", "entra", "identity", "networking"):
            ranked = check_drawio.find(CATALOG, query, include_old=True)[0]
            roles = [(check_drawio.index_of(CATALOG).preference_of(e) or {}).get("role") == "superseded" for e in ranked]
            self.assertEqual(roles, sorted(roles), f"{query}: a superseded path ranks above another match")
        self.assertEqual(names("Microsoft Entra ID")[0], "other/Entra_Identity.svg")
        self.assertEqual(names("private dns zone"), ["networking/DNS_Zones.svg"])
        app = names("app service")
        preferred = [i for i, n in enumerate(app) if n == "app_services/App_Services.svg"]
        copies = [i for i, n in enumerate(app) if n in ("compute/App_Services.svg", "containers/App_Services.svg")]
        self.assertEqual(preferred[0], 0)
        self.assertLess(max(preferred), min(copies))
        index = check_drawio.index_of(CATALOG)
        matches, hidden = check_drawio.find(CATALOG, "private endpoint")
        text = check_drawio.render_find(index, "private endpoint", matches, hidden)
        self.assertIn("preferred: the file to use for Private endpoint", text)
        self.assertIn("- Azure superseded image: Private Endpoint", text)
        self.assertIn("superseded: draws an older private endpoint design; use img/lib/azure2/other/Private_Endpoints.svg", text)
        found = subprocess.run([sys.executable, str(CHECKER), "--find", "active directory", "--json"],
                               capture_output=True, text=True, check=False)
        self.assertEqual(found.returncode, 0, found.stderr)
        rows = json.loads(found.stdout)
        self.assertEqual((rows[0]["name"], rows[0]["preference"]["role"]), ("other/Entra_Identity.svg", "preferred"))
        self.assertEqual((rows[-1]["name"], rows[-1]["preference"]["role"], rows[-1]["preference"]["use"]),
                         ("identity/Azure_Active_Directory.svg", "superseded", "img/lib/azure2/other/Entra_Identity.svg"))

    def test_a_label_for_one_use_of_a_file_is_given_with_its_condition(self):
        """Pre-PR round 2 N1: DNS Zones draws public and private zones, so "Private DNS zone" applies only to a private
        one, whatever the search; Microsoft Entra ID's label applies to every use of its file."""
        index = check_drawio.index_of(CATALOG)

        def found(query: str) -> tuple[list[str], str]:
            matches, hidden = check_drawio.find(CATALOG, query)
            return [e["name"] for e in matches], check_drawio.render_find(index, query, matches, hidden)

        conditional = 'label it "Private DNS zone" only when the zone is private (icon_preferences.json)'
        for query in ("dns zone", "public dns zone", "private dns zone", "dns"):
            names, text = found(query)
            self.assertEqual(names[0], "networking/DNS_Zones.svg", query)
            self.assertIn("preferred: the file to use for DNS zone (public or private)", text, query)
            self.assertIn(conditional, text, query)
            self.assertNotIn('label it "Private DNS zone" (icon_preferences.json)', text, query)
        self.assertIn('label it "Microsoft Entra ID" (icon_preferences.json)', found("entra identity")[1])
        rows = subprocess.run([sys.executable, str(CHECKER), "--find", "dns zone", "--json"],
                              capture_output=True, text=True, check=False)
        self.assertEqual(rows.returncode, 0, rows.stderr)
        preference = json.loads(rows.stdout)[0]["preference"]
        self.assertEqual((preference["label"], preference["label_when"]), ("Private DNS zone", "the zone is private"))
        # A superseded path of such a rule names the condition too.
        rule = {"product": "P", "preferred": "other/Private_Endpoints.svg", "label": "L", "label_when": "it is private",
                "superseded": {"networking/Private_Endpoint.svg": "an older design"}, "reason": "r", "evidence": "e",
                "sources": ["https://example.com/"], "verified": "2026-11-01"}
        custom = check_drawio.Index(CATALOG, {"azure2": [rule]})
        tmp = Path(tempfile.mkdtemp(prefix="drawio-test-"))
        try:
            path = tmp / "diagram.drawio"
            path.write_text(drawio_page(drawio_vertex("v", self.palette("private endpoint", "networking/Private_Endpoint.svg"))),
                            encoding="utf-8")
            warnings = [w["message"] for w in check_drawio.check(path, custom)["warnings"]]
        finally:
            shutil.rmtree(tmp, ignore_errors=True)
        self.assertTrue(any('other/Private_Endpoints.svg, labelled "L" only when it is private' in w for w in warnings),
                        warnings)

    def test_preferences_file_is_well_formed_and_names_current_catalog_paths(self):
        preferences = json.loads(check_drawio.PREFERENCES.read_text(encoding="utf-8"))
        indexed = check_drawio.index_preferences(preferences)
        self.assertEqual(indexed["identity/Azure_Active_Directory.svg"]["role"], "superseded")
        self.assertEqual(indexed["networking/Private_Endpoint.svg"]["rule"]["preferred"], "other/Private_Endpoints.svg")
        self.assertEqual(build_icon_catalog.stale_preferences(CATALOG, preferences), [])
        self.assertEqual(sorted(build_icon_catalog.preference_paths(preferences)), sorted(indexed))

    def test_malformed_preferences_are_refused(self):
        good = {"product": "P", "preferred": "networking/DNS_Zones.svg", "reason": "r", "evidence": "e",
                "sources": ["https://example.com/"], "verified": "2026-11-01"}
        broken = [{"azure2": [{"product": "P", "preferred": "networking/DNS_Zones.svg"}]},
                  {"azure2": [good, dict(good, product="Q")]},
                  {"azure2": [dict(good, superseded={"networking/Private_Endpoint.svg": ""})]},
                  {"azure2": [dict(good, sources=["http://example.com/"])]},
                  {"azure2": [dict(good, verified="last week")]},
                  {"azure2": [dict(good, preferred="img/lib/azure2/networking/DNS_Zones.svg")]},
                  {"azure2": [dict(good, label_when="the zone is private")]},
                  {"azure2": [dict(good, label="Private DNS zone", label_when=" ")]},
                  {"azure2": [dict(good, label=3)]},
                  {"azure2": {"not": "a list"}}]
        self.assertEqual(set(check_drawio.Index(CATALOG, {"azure2": [good]}).preferences), {"networking/DNS_Zones.svg"})
        for preferences in broken:
            with self.assertRaises(ValueError, msg=preferences):
                check_drawio.Index(CATALOG, preferences)
        missing = subprocess.run([sys.executable, str(CHECKER), "--find", "dns", "--preferences", str(REPO / "no-such.json")],
                                 capture_output=True, text=True, check=False)
        self.assertEqual(missing.returncode, 2)
        self.assertIn("cannot read the icon preferences", missing.stderr)


AWS4_JS = """
(function()
{
    // Adds AWS shapes; a comment's apostrophe (don't) must not open a string
    Sidebar.prototype.addAWS4Palette = function()
    {
        var gn = 'mxgraph.aws4';
        var s = 1;
        var w2 = s * 78;
        this.addAWS4ComputePalette(s, w2, gn, this);
    };
    Sidebar.prototype.addAWS4ComputePalette = function(s, w2, gn, sb)
    {
        var n = 'sketch=0;fillColor=#ED7100;strokeColor=none;aspect=fixed;' + mxConstants.STYLE_SHAPE + "=mxgraph.aws4.";
        var n2 = 'sketch=0;fillColor=#ED7100;strokeColor=#ffffff;aspect=fixed;' + mxConstants.STYLE_SHAPE + "=mxgraph.aws4.";
        this.addPaletteFunctions('aws4Compute', 'AWS / Compute', false,
        [
            this.createVertexTemplateEntry(n2 + 'resourceIcon;resIcon=' + gn + '.ec2;',
                w2, w2, '', 'EC2', null, null, 'tags'),
            this.createVertexTemplateEntry(n + 'instance2;points=[[0,0,0],[1,1,0]];',
                s * 48, s * 48, '', 'Instance', null, null, 'tags'),
            this.createVertexTemplateEntry('fillColor=none;strokeColor=#147EBA;dashed=1;',
                s * 130, s * 130, 'Availability Zone', 'Availability Zone', null, null, 'tags')
        ]);
    };
    Sidebar.prototype.addAWS4GroupsPalette = function()
    {
        var n4 = 'container=1;' + mxConstants.STYLE_SHAPE + "=mxgraph.aws4.";
        this.addPaletteFunctions('aws4Groups', 'AWS / Groups', false,
        [
            this.createVertexTemplateEntry(n4 + 'group;grIcon=mxgraph.aws4.group_vpc2;strokeColor=#8C4FFF;fillColor=none;',
                130, 130, 'VPC', 'VPC', null, null, 'tags')
        ]);
    };
    Sidebar.prototype.addAWS4RetiredPalette = function()
    {
        var gn = 'mxgraph.aws4';
        var svc = function(color)
        {
            return 'sketch=0;fillColor=' + color + ';strokeColor=#ffffff;' + mxConstants.STYLE_SHAPE + '=mxgraph.aws4.resourceIcon;resIcon=' + gn + '.';
        };
        this.addPaletteFunctions('aws4r', 'AWS (retired)', false,
        [
            this.createVertexTemplateEntry(svc('#DD344C') + 'honeycode;', 78, 78, '', 'Honeycode (retired)', null, null, 'x')
        ]);
    };
})();
"""
AWS4B_JS = """
Sidebar.prototype.addAWS4bPalette = function()
{
    var n = 'sketch=0;fillColor=#232F3E;' + mxConstants.STYLE_SHAPE + "=mxgraph.aws4.";
    var gn = 'mxgraph.aws4';
    this.addAWS4bComputePalette(n, gn);
};
Sidebar.prototype.addAWS4bComputePalette = function(n, gn)
{
    this.addPaletteFunctions('aws4bCompute', 'AWS18 / Compute', false,
    [
        this.createVertexTemplateEntry(n + 'productIcon;prIcon=' + gn + '.ec2;', 80, 100, 'Amazon EC2', null, null, null, 'x'),
        this.createVertexTemplateEntry(n + 'productIcon;prIcon=' + gn + '.cloudwatch;', 80, 100, 'CloudWatch', null, null, null, 'x')
    ]);
};
"""
AZURE2_JS = """
Sidebar.prototype.addAzure2Palette = function()
{
    var s = 'image;aspect=fixed;html=1;image=img/lib/azure2/';
    var r = 400;
    this.addAzure2DatabasesPalette('mxgraph.azure2', r, this, s + 'databases/');
    this.addAzure2ManagementPalette('mxgraph.azure2', r, this, s + 'management_governance/');
};
Sidebar.prototype.addAzure2DatabasesPalette = function(gn, r, sb, s)
{
    var fns = [
        this.createVertexTemplateEntry(s + 'SQL_Database.svg;points=[[0.5,0,0]];', r * 0.12, r * 0.16, '', 'SQL Database', null, null, 'x'),
        this.createVertexTemplateEntry('image;aspect=fixed;html=1;image=img/lib/azure2/iot/Stack_HCI_Premium.svg;',
            r * 0.17, r * 0.17, '', 'Stack HCI Premium', null, null, 'x')
    ];
    this.addPalette('azure2Databases', 'Azure / Databases', false, function(content) { for (var i = 0; i < fns.length; i++) {} });
};
Sidebar.prototype.addAzure2ManagementPalette = function(gn, r, sb, s)
{
    var fns = [
        this.createVertexTemplateEntry(s + 'solutions.svg;', r * 0.16, r * 0.16, '', 'Solutions', null, null, 'x')
    ];
};
"""
GCP3_JS = """
Sidebar.prototype.addGCP3CategoriesPalette = function()
{
    var s = 0.5;
    var n = 'sketch=0;html=1;aspect=fixed;shape=mxgraph.gcp3.';
    var fns = [
        this.createVertexTemplateEntry(n + 'compute;fillColor=#9aa0a6', s * 72.82, s * 100.0, 'Compute', null, null, null, 'x'),
        this.createVertexTemplateEntry(n + 'agents;fillColor=#9aa0a6', s * 100.0, s * 99.23, 'AI Applications\\n& Agents', null, null, null, 'x')
    ];
    this.addPalette('gcp3Categories', 'GCP Categories', false, null);
};
Sidebar.prototype.addGCP3CoreProductsPalette = function()
{
    var s = 0.5;
    var n = 'sketch=0;html=1;aspect=fixed;shape=mxgraph.gcp3.';
    var fns = [
        this.createVertexTemplateEntry(n + 'cloudrun;fillColor=#4285f4', s * 100.0, s * 99.49, 'Cloud Run', null, null, null, 'x')
    ];
};
"""


class IconCatalogTests(unittest.TestCase):
    def test_evaluator_handles_the_sidebar_expression_subset(self):
        env = {"gn": "mxgraph.aws4", "s": 0.5}
        evaluate = build_icon_catalog.evaluate
        self.assertEqual(evaluate("'a;' + mxConstants.STYLE_SHAPE + \"=\" + gn + '.ec2;'", env), "a;shape=mxgraph.aws4.ec2;")
        self.assertEqual(evaluate("s * 99.49", env), 49.745)
        self.assertEqual(evaluate("'w=' + s * 100 + ';'", env), "w=50;")
        self.assertEqual(evaluate("'Line\\nTwo'", env), "Line\nTwo")
        self.assertEqual(evaluate("-(2 - 5) / 3", env), 1.0)
        with self.assertRaises(build_icon_catalog.Unresolved):
            evaluate("unknownName + 'x'", env)
        with self.assertRaises(build_icon_catalog.Unresolved):
            evaluate("this.getTagsForStencil(gn).join(' ')", env)

    def test_comments_with_quotes_do_not_break_the_scan(self):
        stripped = build_icon_catalog.strip_comments("var a = 'x//y'; // don't\n/* it's */ var b = \"q\";")
        self.assertEqual(stripped, "var a = 'x//y'; \n var b = \"q\";")

    def test_aws_parser_records_form_status_title_size_and_style(self):
        entries = build_icon_catalog.parse_aws(AWS4_JS, AWS4B_JS)
        by = {(e["form"], e["name"], e["status"]): e for e in entries}
        ec2 = by[("service", "ec2", "current")]
        self.assertEqual((ec2["title"], ec2["palette"], ec2["w"], ec2["h"]), ("EC2", "AWS / Compute", 78.0, 78.0))
        self.assertIn("fillColor=#ED7100;strokeColor=#ffffff;", ec2["style"])
        self.assertTrue(ec2["style"].endswith("shape=mxgraph.aws4.resourceIcon;resIcon=mxgraph.aws4.ec2;"))
        instance = by[("resource", "instance2", "current")]
        self.assertNotIn("points=", instance["style"], "connection points are dropped")
        self.assertEqual(instance["w"], 48.0)
        self.assertIn(("plain", "", "current"), by)
        self.assertEqual(by[("group", "group_vpc2", "current")]["palette"], "AWS / Groups")
        self.assertIn("fillColor=#DD344C", by[("service", "honeycode", "retired")]["style"])
        self.assertIn(("product", "cloudwatch", "legacy"), by)

    def test_unevaluable_entry_stops_the_build(self):
        broken = AWS4_JS.replace("w2, w2, '', 'EC2'", "w2, w2, '', 'EC2' + notDefined")
        with self.assertRaises(build_icon_catalog.SourceError):
            build_icon_catalog.parse_aws(broken, AWS4B_JS)

    def test_fetch_retries_network_errors_but_not_client_errors(self):
        class Response:
            def __enter__(self):
                return self

            def __exit__(self, *exc):
                return False

            def read(self):
                return b"ok"

        def http_error(code: int) -> urllib.error.HTTPError:
            error = urllib.error.HTTPError("https://api.github.com/x", code, "status", hdrs=None, fp=None)
            self.addCleanup(error.close)
            return error

        url = "https://api.github.com/repos/jgraph/drawio/releases/latest"
        for failures in ([urllib.error.URLError("name resolution failed"), socket.timeout("read timed out")],
                         [http.client.IncompleteRead(b""), http_error(503)], [http_error(429)]):
            calls = []

            def urlopen(request, timeout, failures=failures, calls=calls):
                calls.append(request.full_url)
                if len(calls) <= len(failures):
                    raise failures[len(calls) - 1]
                return Response()

            with mock.patch.object(build_icon_catalog.urllib.request, "urlopen", urlopen), \
                    mock.patch.object(build_icon_catalog.time, "sleep"):
                self.assertEqual(build_icon_catalog.get(url), b"ok")
            self.assertEqual(len(calls), len(failures) + 1, failures)
        for error in (http_error(404), urllib.error.URLError("down")):
            calls = []

            def failing(request, timeout, error=error, calls=calls):
                calls.append(request.full_url)
                raise error

            with mock.patch.object(build_icon_catalog.urllib.request, "urlopen", failing), \
                    mock.patch.object(build_icon_catalog.time, "sleep"), \
                    self.assertRaises(build_icon_catalog.SourceError):
                build_icon_catalog.get(url)
            self.assertEqual(len(calls), 1 if isinstance(error, urllib.error.HTTPError) else build_icon_catalog.ATTEMPTS)

    def run_main(self, *argv: str, build=None, preferences: Path | None = None) -> tuple[int, str, str]:
        out, err = io.StringIO(), io.StringIO()
        with mock.patch.object(sys, "argv", ["build_icon_catalog.py", *argv]), \
                mock.patch.object(build_icon_catalog, "build", build), \
                mock.patch.object(build_icon_catalog, "PREFERENCES", preferences or build_icon_catalog.PREFERENCES), \
                contextlib.redirect_stdout(out), contextlib.redirect_stderr(err):
            code = build_icon_catalog.main()
        return code, out.getvalue(), err.getvalue()

    def test_exit_status_tells_a_failed_fetch_from_a_change(self):
        """Exit 2 is a failed run and must never open the weekly issue; only a real difference exits 1."""
        tmp = Path(tempfile.mkdtemp(prefix="catalog-test-"))
        try:
            markdown = tmp / "catalog.md"

            def unreachable(tag):
                raise build_icon_catalog.SourceError(f"could not read the {tag} release")

            def crashed(tag):
                raise RecursionError("evaluator recursed")

            for build in (unreachable, crashed):
                code, _, err = self.run_main("--check", "--tag", "v0.0.0", "--markdown", str(markdown), build=build)
                self.assertEqual(code, 2, err)
                self.assertIn("cannot build the catalog", err)
                self.assertFalse(markdown.exists(), "a failed run must not write the issue body")
            committed = json.loads(build_icon_catalog.CATALOG.read_text(encoding="utf-8"))
            code, out, _ = self.run_main("--check", "--markdown", str(markdown), build=lambda tag: committed)
            self.assertEqual((code, markdown.exists()), (0, False), out)
            changed = json.loads(json.dumps(committed))
            rows = changed["gcp3"]["entries"]
            del rows[next(i for i, row in enumerate(rows) if row[1] == "core")]
            code, out, _ = self.run_main("--check", "--markdown", str(markdown), build=lambda tag: changed)
            self.assertEqual(code, 1, out)
            self.assertIn("gcp3 core: +0 -1", markdown.read_text(encoding="utf-8"))
            markdown.unlink()
            stale = tmp / "icon_preferences.json"
            stale.write_text(json.dumps({"azure2": [{"preferred": "networking/Gone.svg"}]}), encoding="utf-8")
            code, out, _ = self.run_main("--check", "--markdown", str(markdown), build=lambda tag: committed, preferences=stale)
            self.assertEqual(code, 1, out)
            self.assertIn("networking/Gone.svg", markdown.read_text(encoding="utf-8"))
        finally:
            shutil.rmtree(tmp, ignore_errors=True)

    def test_watch_opens_the_issue_only_for_a_real_change(self):
        workflow = (REPO / ".github" / "workflows" / "watch-diagram-sources.yml").read_text(encoding="utf-8")
        self.assertNotIn("steps.catalog.outcome", workflow, "a failed fetch must not count as a catalog change")
        issue_step = workflow.split("- name: open or update the issue", 1)[1].split("- name:", 1)[0]
        self.assertIn("steps.catalog.outputs.exit == '1'", issue_step)
        self.assertIn("steps.catalog.outputs.exit != '0' && steps.catalog.outputs.exit != '1'", workflow)

    def test_azure_parser_reads_full_paths_and_records_case_mismatches(self):
        files = ["databases/SQL_Database.svg", "databases/Old_Thing.svg", "databases/readme.txt",
                 "iot/Stack_HCI_Premium.svg", "management_governance/Solutions.svg"]
        entries, legacy, case = build_icon_catalog.parse_azure(AZURE2_JS, files)
        names = sorted(e["name"] for e in entries)
        self.assertEqual(names, ["databases/SQL_Database.svg", "iot/Stack_HCI_Premium.svg", "management_governance/Solutions.svg"])
        self.assertEqual(legacy, ["databases/Old_Thing.svg"])
        self.assertEqual(case, {"management_governance/solutions.svg": "management_governance/Solutions.svg"})
        solutions = next(e for e in entries if e["name"].endswith("Solutions.svg"))
        self.assertIn("image=img/lib/azure2/management_governance/Solutions.svg;", solutions["style"])
        sql = next(e for e in entries if e["name"] == "databases/SQL_Database.svg")
        self.assertEqual((sql["title"], sql["palette"], sql["w"], sql["h"]), ("SQL Database", "Azure / Databases", 48.0, 64.0))

    def test_gcp3_parser_splits_core_and_categories(self):
        entries = build_icon_catalog.parse_gcp3(GCP3_JS)
        self.assertEqual(sorted((e["form"], e["name"]) for e in entries),
                         [("category", "agents"), ("category", "compute"), ("core", "cloudrun")])
        agents = next(e for e in entries if e["name"] == "agents")
        self.assertEqual(agents["title"], "AI Applications & Agents")
        self.assertTrue(agents["style"].endswith("fillColor=#9aa0a6"))

    def test_catalog_round_trip_lists_and_differences(self):
        tag_source = {"Sidebar-AWS4.js": AWS4_JS, "Sidebar-AWS4b.js": AWS4B_JS, "Sidebar-Azure2.js": AZURE2_JS,
                      "Sidebar-GCP3.js": GCP3_JS}
        images = ["databases/SQL_Database.svg", "iot/Stack_HCI_Premium.svg", "management_governance/Solutions.svg"]
        catalog = build_icon_catalog.assemble("v1.0.0", tag_source, images, built="2026-01-01")
        reread = json.loads(build_icon_catalog.dump(catalog))
        self.assertEqual(reread, catalog)
        found = build_icon_catalog.lists(reread)
        self.assertEqual(found[("aws4", "current")], {"ec2", "instance2", "group_vpc2"})
        self.assertEqual(found[("aws4", "retired")], {"honeycode"})
        self.assertEqual(found[("aws4", "legacy")], {"cloudwatch"})
        self.assertEqual([e["style"] for e in build_icon_catalog.unpack_entries(reread, "aws4")],
                         [e["style"] for e in build_icon_catalog.parse_aws(AWS4_JS, AWS4B_JS)])
        self.assertEqual(build_icon_catalog.differences(reread, catalog), [])
        recoloured = build_icon_catalog.assemble("v1.0.1", {**tag_source, "Sidebar-AWS4.js": AWS4_JS.replace("#ED7100", "#FF9900")},
                                                 images, built="2026-01-02")
        self.assertTrue(any("palette styles changed" in line for line in build_icon_catalog.differences(catalog, recoloured)))
        older = {"aws4": {"current": ["ec2"]}}
        self.assertTrue(any("older name-list layout" in line for line in build_icon_catalog.differences(older, catalog)))

    def test_committed_catalog_is_complete(self):
        self.assertEqual(CATALOG.get("schema"), build_icon_catalog.SCHEMA)
        self.assertTrue(CATALOG.get("drawio_version"))
        found = build_icon_catalog.lists(CATALOG)
        for library, kind in build_icon_catalog.LISTS:
            if (library, kind) != ("azure2", "legacy"):
                self.assertTrue(found[(library, kind)], f"{library} {kind} is empty")
        self.assertEqual(len(found[("gcp3", "core")]), 19)
        self.assertIn("vertexai", found[("gcp3", "core")])
        for library in ("aws4", "azure2", "gcp3"):
            for entry in build_icon_catalog.unpack_entries(CATALOG, library):
                self.assertTrue(entry["style"] and entry["palette"] and entry["w"] and entry["h"], entry)
        for palette_path, file_path in CATALOG["azure2"]["case_mismatch"].items():
            self.assertNotIn(palette_path, found[("azure2", "current")])
            self.assertIn(file_path, found[("azure2", "current")])


def tracked_drawio_files() -> list[Path]:
    """Every .drawio file git tracks in this repository, or every one on disk when git is unavailable."""
    try:
        out = subprocess.run(["git", "ls-files", "-z", "--", "*.drawio"], cwd=REPO, capture_output=True, check=True)
        return sorted(REPO / p for p in out.stdout.decode("utf-8").split("\0") if p)
    except (OSError, subprocess.CalledProcessError):
        return sorted(p for p in REPO.rglob("*.drawio") if ".git" not in p.parts)


class CommittedDiagramTests(unittest.TestCase):
    def test_every_committed_diagram_passes_the_strict_checker(self):
        """Templates, fixtures and examples teach by example, so each must pass check_drawio.py --strict."""
        files = tracked_drawio_files()
        self.assertTrue(files, "no .drawio files found")
        failures = []
        for path in files:
            report = check_drawio.check(path, CATALOG, strict=True)
            failures += [f"{path.relative_to(REPO).as_posix()} [{e['page']}] {e['cell']}: {e['message']}" for e in report["errors"]]
        self.assertEqual(failures, [], "\n" + "\n".join(failures))

    def test_committed_diagrams_exercise_every_provider_library(self):
        """At least one committed diagram per provider, so the strict guard above sees real AWS, Azure and Google
        Cloud icons in files, not only in unit-test styles."""
        providers = set()
        for path in tracked_drawio_files():
            providers |= {icon["provider"] for icon in check_drawio.check(path, CATALOG, strict=True)["icons"]}
        self.assertLessEqual({"AWS", "Azure", "Google Cloud"}, providers)


class SharedPrimitiveTests(unittest.TestCase):
    def test_every_shared_copy_is_identical(self):
        self.assertEqual(sync_shared.drift(REPO), [])

    def test_shared_language_primitives_name_both_languages(self):
        shared = REPO / "shared-primitives"
        for name in ("agent-evaluation", "agentic-workflow-design", "playwright-validation", "secure-agent-engineering"):
            skill = shared / "skills" / name
            text = (skill / "SKILL.md").read_text(encoding="utf-8")
            self.assertIn("Where Python and TypeScript differ", text, name)
            for language in ("python", "typescript"):
                self.assertTrue((skill / "references" / f"{language}.md").is_file(), f"{name} lacks references/{language}.md")
                self.assertIn(f"references/{language}.md", text, f"{name} does not point to references/{language}.md")

    def test_sync_copies_every_kind_and_drift_is_reported(self):
        tmp = Path(tempfile.mkdtemp(prefix="shared-test-"))
        try:
            shared = tmp / "shared-primitives"
            (shared / "skills" / "demo").mkdir(parents=True)
            (shared / "skills" / "demo" / "SKILL.md").write_text(
                "---\nname: demo\ndescription: Use when demonstrating.\n---\n# Demo\n", encoding="utf-8")
            (shared / "agents").mkdir()
            (shared / "agents" / "helper.agent.md").write_text("---\nname: helper\ndescription: Demo.\n---\n# Helper\n", encoding="utf-8")
            (shared / "prompts").mkdir()
            (shared / "prompts" / "run-demo.prompt.md").write_text("---\ndescription: Run the demo\n---\n# Run\n", encoding="utf-8")
            (shared / "consumers.json").write_text(json.dumps({
                "skills": {"demo": ["a-pack", "b-pack"]}, "agents": {"helper": ["a-pack", "b-pack"]},
                "prompts": {"run-demo": ["a-pack", "b-pack"]}}), encoding="utf-8")
            for pack in ("a-pack", "b-pack", "c-pack"):
                (tmp / pack / ".apm" / "skills").mkdir(parents=True)
                (tmp / pack / "tests").mkdir()
                (tmp / pack / "apm.yml").write_text("name: x\nversion: 1.0.0\n", encoding="utf-8")
            self.assertEqual(sync_shared.sync(tmp), ["a-pack", "b-pack"])
            self.assertEqual(sync_shared.drift(tmp), [])
            self.assertTrue((tmp / "a-pack" / "tests" / "skill-coverage.yml").is_file())
            self.assertTrue((tmp / "b-pack" / ".apm" / "agents" / "helper.agent.md").is_file())
            self.assertTrue((tmp / "b-pack" / ".apm" / "prompts" / "run-demo.prompt.md").is_file())
            (tmp / "b-pack" / ".apm" / "skills" / "demo" / "SKILL.md").write_text("changed\n", encoding="utf-8")
            (tmp / "a-pack" / ".apm" / "agents" / "helper.agent.md").write_text("edited in the pack\n", encoding="utf-8")
            shutil.copytree(tmp / "a-pack" / ".apm" / "skills" / "demo", tmp / "c-pack" / ".apm" / "skills" / "demo")
            problems = " | ".join(sync_shared.drift(tmp))
            self.assertIn("b-pack/.apm/skills/demo differs", problems)
            self.assertIn("a-pack/.apm/agents/helper.agent.md differs", problems)
            self.assertIn("c-pack ships skill demo but is not listed", problems)
        finally:
            shutil.rmtree(tmp, ignore_errors=True)


if __name__ == "__main__":
    unittest.main()
