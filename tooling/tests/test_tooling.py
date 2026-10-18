"""Tests for the shared pack tooling. Run: python -m unittest discover -s tooling/tests -v"""
from __future__ import annotations

import base64
import importlib.util
import json
import shutil
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

    def test_current_icons_of_all_three_providers_pass(self):
        report = self.run_check(drawio_page(
            drawio_vertex("aws", "shape=mxgraph.aws4.resourceIcon;resIcon=mxgraph.aws4.lambda;")
            + drawio_vertex("azure", "image;image=img/lib/azure2/databases/Azure_DocumentDB.svg;")
            + drawio_vertex("gcp-core", "shape=mxgraph.gcp3.cloudrun;")
            + drawio_vertex("gcp-category", "shape=mxgraph.gcp3.dataanalytics;")))
        self.assertEqual(report["result"], "PASS")
        self.assertEqual(set(self.statuses(report).values()), {"current"})
        self.assertEqual(set(report["icon_summary"]), {"AWS", "Azure", "Google Cloud"})

    def test_misspelled_names_are_errors(self):
        report = self.run_check(drawio_page(
            drawio_vertex("aws", "shape=mxgraph.aws4.resourceIcon;resIcon=mxgraph.aws4.lamda;")
            + drawio_vertex("azure", "image;image=img/lib/azure2/app_services/App_Service.svg;")
            + drawio_vertex("gcp", "shape=mxgraph.gcp3.cloud_run;")))
        self.assertEqual(set(self.statuses(report).values()), {"unknown"})
        self.assertEqual(len(report["errors"]), 3)

    def test_legacy_and_retired_icons_warn_and_fail_when_strict(self):
        cells = (drawio_vertex("aws18", "shape=mxgraph.aws4.productIcon;prIcon=mxgraph.aws4.ec2;")
                 + drawio_vertex("retired", "shape=mxgraph.aws4.resourceIcon;resIcon=mxgraph.aws4.honeycode;")
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
        cell = ('<UserObject id="u" label="Cloud SQL"><mxCell style="shape=mxgraph.gcp3.cloudsql;" vertex="1" parent="1">'
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


class IconCatalogTests(unittest.TestCase):
    def test_aws_parser_separates_current_retired_and_legacy(self):
        aws4 = ("Sidebar.prototype.addAWS4ComputePalette = function(s, w, h, w2, gn, sb)\n{\n"
                "    var n2 = 'sketch=0;' + mxConstants.STYLE_SHAPE + \"=mxgraph.aws4.\";\n"
                "    this.createVertexTemplateEntry(n2 + 'resourceIcon;resIcon=' + gn + '.ec2;', 1, 1);\n"
                "    this.createVertexTemplateEntry(n2 + 'instance2;', 1, 1);\n};\n"
                "Sidebar.prototype.addAWS4RetiredPalette = function()\n{\n"
                "    this.createVertexTemplateEntry(svc('#8C4FFF') + 'honeycode;', 1, 1);\n};\n")
        aws4b = ("Sidebar.prototype.addAWS4bComputePalette = function()\n{\n"
                 "    this.createVertexTemplateEntry(n + 'productIcon;prIcon=' + gn + '.ec2;', 1, 1);\n"
                 "    this.createVertexTemplateEntry(n + 'productIcon;prIcon=' + gn + '.cloudwatch;', 1, 1);\n};\n")
        parsed = build_icon_catalog.parse_aws(aws4, aws4b)
        self.assertIn("ec2", parsed["current"])
        self.assertIn("instance2", parsed["current"])
        self.assertEqual(parsed["retired"], ["honeycode"])
        self.assertIn("cloudwatch", parsed["legacy"])
        self.assertNotIn("ec2", parsed["legacy"])

    def test_azure_parser_maps_palette_categories(self):
        js = ("Sidebar.prototype.addAzure2Palette = function()\n{\n"
              "    this.addAzure2DatabasesPalette(gn, r, sb, s + 'databases/');\n};\n"
              "Sidebar.prototype.addAzure2DatabasesPalette = function(gn, r, sb, s)\n{\n"
              "    this.createVertexTemplateEntry(s + 'SQL_Database.svg;', 1, 1);\n};\n")
        parsed = build_icon_catalog.parse_azure(js, ["databases/SQL_Database.svg", "databases/Old_Thing.svg", "databases/readme.txt"])
        self.assertEqual(parsed, {"current": ["databases/SQL_Database.svg"], "legacy": ["databases/Old_Thing.svg"]})

    def test_gcp3_parser_splits_core_and_categories(self):
        js = ("Sidebar.prototype.addGCP3CategoriesPalette = function()\n{\n"
              "    this.createVertexTemplateEntry(n + 'compute;fillColor=#9aa0a6', 1, 1);\n};\n"
              "Sidebar.prototype.addGCP3CoreProductsPalette = function()\n{\n"
              "    this.createVertexTemplateEntry(n + 'cloudrun;fillColor=#4285f4', 1, 1);\n};\n")
        self.assertEqual(build_icon_catalog.parse_gcp3(js), {"core": ["cloudrun"], "categories": ["compute"]})

    def test_committed_catalog_has_every_list(self):
        self.assertTrue(CATALOG.get("drawio_version"))
        for library, kind in build_icon_catalog.LISTS:
            if (library, kind) != ("azure2", "legacy"):
                self.assertTrue(CATALOG[library][kind], f"{library} {kind} is empty")


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
