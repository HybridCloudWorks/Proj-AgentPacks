"""Tests for the shared pack tooling. Run: python -m unittest discover -s tooling/tests -v"""
from __future__ import annotations

import base64
import importlib.util
import json
import shutil
import subprocess
import sys
import tempfile
import unittest
import zlib
from pathlib import Path
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
        with self.assertRaises(SystemExit):
            build_icon_catalog.parse_aws(broken, AWS4B_JS)

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
