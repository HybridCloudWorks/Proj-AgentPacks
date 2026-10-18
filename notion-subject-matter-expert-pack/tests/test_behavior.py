"""Offline tests for the pack's helper scripts and cross-file contracts; no Notion, network or host session."""
from __future__ import annotations

import copy
import json
import re
import subprocess
import sys
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
FIXTURES = ROOT / "tests" / "fixtures"
sys.path.insert(0, str(ROOT / "tooling"))
from completion_contract import load_contract, validate_completion  # noqa: E402
from notion_draft_check import hook, scan_text  # noqa: E402

# Built at runtime so that no credential-shaped string is stored in the repository.
SYNTHETIC_TOKEN = "ntn_" + "A1b2C3d4" * 6


def checks(result: dict, key: str = "errors") -> set[str]:
    return {f["check"] for f in result[key]}


def frontmatter(path: Path) -> dict[str, str]:
    match = re.match(r"\A---\r?\n(.*?)\r?\n---\r?\n", path.read_text(encoding="utf-8"), re.DOTALL)
    fields = {}
    for line in (match.group(1).splitlines() if match else []):
        key, _, value = line.partition(":")
        fields[key.strip()] = value.strip().strip("\"'")
    return fields


class CompletionContractTests(unittest.TestCase):
    def setUp(self):
        self.valid = json.loads((FIXTURES / "valid-completion.json").read_text(encoding="utf-8"))

    def test_valid_fixture_passes(self):
        self.assertEqual([], validate_completion(self.valid))

    def test_missing_and_malformed_reports_fail(self):
        for value in (None, [], {}, {"status": "COMPLETE_VERIFIED"}):
            with self.subTest(value=value):
                self.assertTrue(validate_completion(value))

    def test_unconfirmed_write_cannot_be_complete(self):
        value = json.loads((FIXTURES / "invalid-completion.json").read_text(encoding="utf-8"))
        errors = validate_completion(value)
        self.assertIn("complete claim requires all criteria passed", errors)
        self.assertIn("complete claim requires a URL for every workspace change", errors)
        self.assertIn("complete claim requires a passing fetch check for workspace changes", errors)
        self.assertIn("complete claim has unverified items", errors)

    def test_failed_or_boolean_exit_code_is_not_a_passing_command(self):
        for exit_code in (1, False, "0", None):
            value = copy.deepcopy(self.valid)
            value["checks"][1]["exit_code"] = exit_code
            with self.subTest(exit_code=exit_code):
                self.assertIn("passing command check lacks a zero exit code", validate_completion(value))

    def test_unknown_change_action_and_check_method_fail(self):
        value = copy.deepcopy(self.valid)
        value["notion_changes"][0]["action"] = "published"
        value["checks"][0]["method"] = "guess"
        errors = validate_completion(value)
        self.assertIn("invalid notion change action", errors)
        self.assertIn("invalid check method", errors)

    def test_prepared_report_may_carry_unverified_items(self):
        value = copy.deepcopy(self.valid)
        value["status"] = "PREPARED_NOT_VERIFIED"
        value["notion_changes"][0]["url"] = ""
        value["checks"] = [{"check": "Re-fetch", "method": "fetch", "status": "unverified", "evidence": "No connector."}]
        value["unverified"] = ["Page not written: no Notion tool in the session."]
        self.assertEqual([], validate_completion(value))

    def test_analysis_only_cannot_list_workspace_changes(self):
        value = copy.deepcopy(self.valid)
        value["status"] = "ANALYSIS_ONLY"
        self.assertIn("analysis-only report lists workspace changes", validate_completion(value))


class DraftCheckTests(unittest.TestCase):
    def test_clean_research_draft_passes(self):
        text = (FIXTURES / "research-draft-clean.md").read_text(encoding="utf-8")
        self.assertEqual([], scan_text(text, "internal", "research")["errors"])
        self.assertEqual([], scan_text(text, "external", "research")["errors"])

    def test_research_without_sources_or_citations_fails(self):
        result = scan_text("# Findings\n\nRevenue grew.\n", "internal", "research")
        self.assertEqual({"missing-section:sources", "research-without-citations"}, checks(result))

    def test_external_agenda_leaks_are_found(self):
        text = (FIXTURES / "external-agenda-leak.md").read_text(encoding="utf-8")
        found = checks(scan_text(text, "external", "agenda"))
        self.assertEqual({"unfilled-placeholder", "internal-marker-in-external-draft", "mention-page-without-url"}, found)
        lines = sorted(f["line"] for f in scan_text(text, "external", "agenda")["errors"] if f["check"] == "internal-marker-in-external-draft")
        self.assertEqual(2, len(lines), "both the internal-only note and the pre-read reference must be flagged")

    def test_internal_audience_allows_internal_markers(self):
        text = "# INTERNAL - renewal pre-read\n\nInternal only. Do not forward.\n"
        self.assertEqual([], scan_text(text, "internal", "preread")["errors"])
        self.assertIn("preread-for-external-audience", checks(scan_text(text, "external", "preread")))
        self.assertIn("preread-not-marked-internal", checks(scan_text("# Renewal notes\n\nBackground.\n", "internal", "preread")))

    def test_mention_urls_must_be_real_links(self):
        for mention in ('<mention-page url="...">X</mention-page>', "<mention-database>Tasks</mention-database>", '<mention-user url=""/>'):
            with self.subTest(mention=mention):
                self.assertTrue(any(c.endswith("-without-url") for c in checks(scan_text(mention))))

    def test_person_mentions_in_external_drafts_warn(self):
        result = scan_text('<mention-user url="https://www.notion.so/synthetic-user">A</mention-user>', "external")
        self.assertEqual({"person-mention-in-external-draft"}, checks(result, "warnings"))

    def test_decision_record_needs_its_sections(self):
        text = "# Decision: adopt fortnightly releases\n\n## Context\n\n## Options considered\n"
        self.assertEqual({"missing-section:consequences"}, checks(scan_text(text, "internal", "decision")))

    def test_secret_is_reported_without_echoing_it(self):
        result = scan_text(f"Token for the sync job: {SYNTHETIC_TOKEN}\n")
        self.assertEqual({"secret:notion-token"}, checks(result))
        self.assertNotIn(SYNTHETIC_TOKEN, json.dumps(result))

    def test_code_blocks_still_scanned_for_secrets(self):
        text = f"```\nNOTION_TOKEN={SYNTHETIC_TOKEN}\n{{{{ template }}}}\n```\n"
        self.assertEqual({"secret:notion-token"}, checks(scan_text(text)))


class HookTests(unittest.TestCase):
    def payload(self, content: str) -> bytes:
        return json.dumps({"tool_name": "mcp__notion__notion-create-pages",
                           "tool_input": {"pages": [{"properties": {"title": "Sync notes"}, "content": content}]}}).encode()

    def test_clean_write_is_allowed(self):
        self.assertEqual((0, ""), hook(self.payload("Nightly sync now retries on 429.")))

    def test_credential_blocks_without_echo(self):
        code, message = hook(self.payload(f"Use {SYNTHETIC_TOKEN} for the job"))
        self.assertEqual(2, code)
        self.assertIn("notion-token", message)
        self.assertNotIn(SYNTHETIC_TOKEN, message)

    def test_json_encoded_tool_arguments_are_scanned(self):
        raw = json.dumps({"toolName": "notion-update-page", "toolArgs": json.dumps({"content": SYNTHETIC_TOKEN})}).encode()
        self.assertEqual(2, hook(raw)[0])

    def test_invalid_and_oversized_input_are_bounded(self):
        self.assertEqual(1, hook(b"not json")[0])
        self.assertEqual(1, hook(b"[1, 2]")[0])
        self.assertEqual(2, hook(b" " * 2_000_001)[0])

    def test_command_line_hook_does_not_echo_stdin(self):
        script = ROOT / "tooling" / "notion_draft_check.py"
        for stdin, expected in ((self.payload(SYNTHETIC_TOKEN), 2), (b"garbage " + SYNTHETIC_TOKEN.encode(), 1)):
            with self.subTest(expected=expected):
                result = subprocess.run([sys.executable, "-I", "-B", str(script), "--hook"], input=stdin,
                                        capture_output=True, timeout=30)
                self.assertEqual(expected, result.returncode)
                self.assertNotIn(SYNTHETIC_TOKEN.encode(), result.stdout + result.stderr)


class PackConsistencyTests(unittest.TestCase):
    def setUp(self):
        self.agents = {p.name[: -len(".agent.md")] for p in (ROOT / ".apm" / "agents").glob("*.agent.md")}
        self.skills = {p.name for p in (ROOT / ".apm" / "skills").iterdir() if p.is_dir()}

    def test_prompts_name_existing_agents_and_skills(self):
        for path in (ROOT / ".apm" / "prompts").glob("*.prompt.md"):
            with self.subTest(prompt=path.name):
                self.assertIn(frontmatter(path).get("agent"), self.agents)
                named = set(re.findall(r"\bnotion-[a-z-]+", path.read_text(encoding="utf-8")))
                self.assertTrue(named & self.skills, "each prompt applies at least one skill")
                self.assertFalse(named - self.skills - self.agents - {"notion-subject-matter-expert-contract"})

    def test_primary_routes_to_every_skill(self):
        text = (ROOT / ".apm" / "agents" / "notion-subject-matter-expert.agent.md").read_text(encoding="utf-8")
        self.assertEqual(self.skills, set(re.findall(r"\bnotion-[a-z-]+", text)) & self.skills)

    def test_skill_reference_files_exist_in_their_folder(self):
        for skill in self.skills:
            folder = ROOT / ".apm" / "skills" / skill
            text = (folder / "SKILL.md").read_text(encoding="utf-8")
            self.assertEqual(skill, frontmatter(folder / "SKILL.md").get("name"))
            for name in set(re.findall(r"\b[\w-]+\.md\b", text)) - {"SKILL.md"}:
                with self.subTest(skill=skill, file=name):
                    self.assertTrue((folder / name).is_file())

    def test_contract_and_validator_share_one_report_contract(self):
        contract_text = (ROOT / ".apm" / "instructions" / "notion-subject-matter-expert-contract.instructions.md").read_text(encoding="utf-8")
        rc = load_contract()
        self.assertIn(rc["fallback"], contract_text)
        for status in rc["statuses"]:
            self.assertIn(status, contract_text)
        for agent in self.agents:
            self.assertIn(agent, contract_text)


if __name__ == "__main__":
    unittest.main()
