"""Tests for the shared pack tooling. Run: python -m unittest discover -s tooling/tests -v"""
from __future__ import annotations

import json
import shutil
import sys
import tempfile
import unittest
from pathlib import Path

REPO = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(REPO / "tooling"))

import check_collisions  # noqa: E402
import ci_plan  # noqa: E402
import generate_pack  # noqa: E402
import restructure_pack  # noqa: E402
import skill_coverage  # noqa: E402
import validate_pack  # noqa: E402

EXEMPLAR = REPO / "python-distinguished-engineer-pack"


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
        self.assertEqual(set(found), {"agents", "skills"})
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


if __name__ == "__main__":
    unittest.main()
