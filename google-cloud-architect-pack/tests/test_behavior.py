"""Tests for the pack's helper scripts and report contract. Everything runs offline: no client session, network or cloud API."""
from __future__ import annotations

import copy
import json
import re
import subprocess
import sys
import tempfile
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
SKILLS = ROOT / ".apm" / "skills"
sys.path[:0] = [str(ROOT / "tooling")] + [str(SKILLS / name / "scripts") for name in
                                          ("gcp-estate-discovery", "gcp-network-design", "gcp-reliability-dr", "gcp-iac-validation")]
from availability import dr_check, error_budget_minutes, parallel, parse_parallel, serial
from command_guard import classify, command_from_payload
from completion_contract import CHECK_FIELDS, FALLBACK, REQUIRED, STATUSES, validate_completion
from ip_plan import check_plan, pod_block_size
from plan_summary import summarize

GUARD = SKILLS / "gcp-estate-discovery" / "scripts" / "command_guard.py"


def level(command: str | list[str]) -> int | None:
    return classify(command)["level"]


class CommandGuardTests(unittest.TestCase):
    def test_read_only_commands_are_level_one(self):
        for command in ("gcloud compute instances list --project=p --format=json(name)",
                        "gcloud asset search-all-iam-policies --scope=organizations/1 --query=policy:roles/owner",
                        "gcloud compute interconnects attachments list --project=p",
                        "gcloud scc settings describe --organization=1",
                        "gcloud logging read \"severity>=ERROR\" --project=p --limit=20",
                        "bq --location US ls",
                        "bq query --use_legacy_sql=false --dry_run 'SELECT 1'",
                        "kubectl -n prod get pods",
                        "kubectl apply -f deploy.yaml --dry-run=server",
                        "terraform -chdir=infra plan -input=false -out=tfplan",
                        "gsutil ls gs://bucket"):
            with self.subTest(command=command):
                self.assertEqual(1, level(command))

    def test_help_is_level_zero(self):
        self.assertEqual(0, level("gcloud help compute instances create"))

    def test_mutations_need_approval(self):
        for command in ("gcloud projects add-iam-policy-binding p --member=user:a@example.com --role=roles/owner",
                        "gcloud services enable compute.googleapis.com --project=p",
                        "gcloud projects delete my-list",
                        "gcloud network-management connectivity-tests create t --project=p",
                        "gcloud org-policies set-policy policy.yaml",
                        "gcloud kms keys versions destroy 1 --key=k --keyring=r --location=global --project=p",
                        "bq query 'SELECT * FROM big.table'",
                        "bq rm -f dataset.table",
                        "kubectl apply -f deploy.yaml",
                        "kubectl apply -f deploy.yaml --dry-run=none",
                        "kubectl get secret db -o yaml",
                        "terraform apply tfplan",
                        "terraform state pull",
                        "terraform test",
                        "gsutil iam ch allUsers:objectViewer gs://bucket"):
            with self.subTest(command=command):
                self.assertEqual(2, level(command))

    def test_secret_and_token_exposure_needs_approval(self):
        self.assertEqual(2, level("gcloud secrets versions access latest --secret=db --project=p"))
        self.assertEqual(2, level("gcloud auth print-access-token"))
        self.assertEqual(2, level("gcloud auth login"))

    def test_iam_change_is_labelled(self):
        result = classify("gcloud projects add-iam-policy-binding p --member=x --role=y")
        self.assertIn("gcloud: IAM change", result["reasons"])

    def test_preview_flag_downgrades_to_level_one(self):
        self.assertEqual(1, level("gcloud run deploy svc --image=i --region=r --project=p --dry-run"))

    def test_missing_project_is_warned(self):
        self.assertTrue(classify("gcloud compute instances list")["warnings"])
        self.assertFalse(classify("gcloud compute instances list --project=p")["warnings"])

    def test_compound_and_multiline_commands_take_the_highest_level(self):
        self.assertEqual(2, level("gcloud compute instances list --project=p && gcloud projects delete p"))
        self.assertEqual(2, level("gcloud compute instances list --project=p\ngcloud projects delete p"))
        self.assertEqual(1, level("gcloud compute instances list \\\n  --project=p"))
        self.assertIn("compound command", " ".join(classify("gcloud config list | cat")["reasons"]))

    def test_unclassifiable_input_needs_approval(self):
        self.assertEqual(2, level("gcloud projects delete $(cat id.txt)"))
        self.assertEqual(2, level("gcloud compute instances list --filter=\"unbalanced"))
        self.assertEqual(2, level("gcloud compute frobnicate --project=p"))
        self.assertEqual(2, level("sudo gcloud compute instances list --project=p"))

    def test_redirect_is_local_write(self):
        self.assertEqual(1, level("terraform show -json tfplan > tfplan.json"))

    def test_windows_paths_and_argv_lists(self):
        result = classify("C:\\tools\\google\\gcloud.cmd compute instances list --project=p")
        self.assertEqual((1, ["gcloud"]), (result["level"], result["tools"]))
        self.assertEqual(2, level(["gcloud", "projects", "delete", "p"]))

    def test_non_cloud_commands_are_out_of_scope(self):
        result = classify("ls -la")
        self.assertIsNone(result["level"])
        self.assertEqual("allow", result["verdict"])

    def test_payload_shapes(self):
        self.assertEqual("gcloud a", command_from_payload({"tool_input": {"command": "gcloud a"}}))
        self.assertEqual("gcloud b", command_from_payload({"toolArgs": json.dumps({"command": "gcloud b"})}))
        self.assertEqual("gcloud c", command_from_payload({"command": "gcloud c"}))
        self.assertIsNone(command_from_payload({"toolArgs": "not json"}))
        self.assertIsNone(command_from_payload([]))

    def test_hook_mode_blocks_without_echoing_the_command(self):
        payload = json.dumps({"tool_input": {"command": "gcloud projects delete synthetic-private-name-42"}})
        proc = subprocess.run([sys.executable, "-I", "-B", str(GUARD), "hook"], input=payload, text=True, capture_output=True, timeout=20)
        self.assertEqual(2, proc.returncode)
        self.assertEqual("ask", json.loads(proc.stdout)["decision"])
        self.assertNotIn("synthetic-private-name-42", proc.stdout + proc.stderr)

    def test_hook_mode_rejects_invalid_input_without_echo(self):
        proc = subprocess.run([sys.executable, "-I", "-B", str(GUARD), "hook"], input="private-sample-7f3a{", text=True, capture_output=True, timeout=20)
        self.assertEqual(3, proc.returncode)
        self.assertNotIn("private-sample-7f3a", proc.stdout + proc.stderr)

    def test_hook_mode_allows_read_only(self):
        payload = json.dumps({"toolArgs": json.dumps({"command": "gcloud run services list --project=p --region=r"})})
        proc = subprocess.run([sys.executable, "-I", "-B", str(GUARD), "hook"], input=payload, text=True, capture_output=True, timeout=20)
        self.assertEqual(0, proc.returncode)
        self.assertEqual("allow", json.loads(proc.stdout)["decision"])


class IpPlanTests(unittest.TestCase):
    def setUp(self):
        self.example = json.loads((ROOT / "templates" / "ip-plan.example.json").read_text(encoding="utf-8"))

    def test_pod_block_sizes_match_gke_allocation(self):
        self.assertEqual({8: 16, 16: 32, 32: 64, 48: 128, 64: 128, 65: 256, 110: 256},
                         {n: pod_block_size(n) for n in (8, 16, 32, 48, 64, 65, 110)})

    def test_example_plan_is_clean(self):
        result = check_plan(self.example)
        self.assertEqual([], result["errors"])
        prod = next(s for s in result["subnets"] if s["name"] == "prod-app-europe-west1")
        self.assertEqual("/25", prod["pod_block"])
        self.assertEqual(1024, prod["node_capacity_from_pod_range"])
        self.assertTrue(any("RFC 6598" in n for n in result["notes"]))

    def test_overlap_is_an_error_unless_explicitly_allowed(self):
        plan = copy.deepcopy(self.example)
        plan["subnets"][1]["cidr"] = "10.16.0.0/22"
        errors = check_plan(plan)["errors"]
        self.assertTrue(any(e.startswith("overlap:") for e in errors))
        plan["allow_overlap"] = [["prod-app-europe-west1", "prod-serverless-europe-west1"]]
        result = check_plan(plan)
        self.assertFalse(any(e.startswith("overlap:") for e in result["errors"]))
        self.assertTrue(any(w.startswith("overlap:") for w in result["warnings"]))

    def test_on_premises_overlap_is_caught(self):
        plan = copy.deepcopy(self.example)
        plan["subnets"][0]["cidr"] = "10.8.0.0/20"
        self.assertTrue(any("on-premises" in e for e in check_plan(plan)["errors"]))

    def test_pod_range_too_small_for_nodes(self):
        plan = copy.deepcopy(self.example)
        plan["subnets"][0]["gke"]["max_nodes"] = 2000
        self.assertTrue(any("Pod range" in e for e in check_plan(plan)["errors"]))

    def test_primary_range_exhaustion_from_serverless(self):
        plan = copy.deepcopy(self.example)
        plan["subnets"][1]["serverless"]["max_instances"] = 600
        self.assertTrue(any("primary range" in e for e in check_plan(plan)["errors"]))

    def test_invalid_inputs(self):
        self.assertTrue(check_plan(None)["errors"])
        plan = copy.deepcopy(self.example)
        plan["subnets"][0]["cidr"] = "10.16.0.1/20"
        self.assertTrue(any("invalid CIDR" in e for e in check_plan(plan)["errors"]))
        plan = copy.deepcopy(self.example)
        plan["subnets"][0]["gke"]["pods_range"] = "missing"
        self.assertTrue(any("pods_range" in e for e in check_plan(plan)["errors"]))

    def test_public_range_is_warned(self):
        plan = {"subnets": [{"name": "odd", "cidr": "203.0.113.0/24"}]}
        self.assertTrue(check_plan(plan)["warnings"])


class AvailabilityTests(unittest.TestCase):
    def test_error_budget(self):
        self.assertAlmostEqual(43.2, error_budget_minutes(99.9, 30), places=6)

    def test_composition(self):
        self.assertAlmostEqual(99.940005, serial([99.95, 99.99]), places=5)
        self.assertAlmostEqual(99.9975, parallel(99.5, 2), places=6)
        self.assertAlmostEqual(parallel(99.5, 2), parse_parallel("99.5x2"), places=9)

    def test_invalid_values(self):
        for call in (lambda: error_budget_minutes(101, 30), lambda: parallel(99, 0), lambda: parse_parallel("99.5")):
            with self.assertRaises(ValueError):
                call()

    def test_dr_check(self):
        ok = dr_check(rpo_minutes=15, rto_minutes=60, restore_minutes=40, backup_interval_minutes=5)
        self.assertTrue(ok["meets_rpo"] and ok["meets_rto"])
        gap = dr_check(rpo_minutes=15, rto_minutes=60, restore_minutes=50, backup_interval_minutes=60,
                       replication_lag_minutes=1, detection_minutes=15)
        self.assertTrue(gap["meets_rpo"])
        self.assertFalse(gap["meets_rto"])
        self.assertEqual(-5, gap["rto_margin_minutes"])
        with self.assertRaises(ValueError):
            dr_check(rpo_minutes=1, rto_minutes=1, restore_minutes=1)

    def test_cli_exit_codes(self):
        script = SKILLS / "gcp-reliability-dr" / "scripts" / "availability.py"
        ok = subprocess.run([sys.executable, "-I", "-B", str(script), "dr-check", "--rpo-minutes", "15", "--rto-minutes", "60",
                             "--restore-minutes", "40", "--backup-interval-minutes", "5"], capture_output=True, text=True, timeout=20)
        gap = subprocess.run([sys.executable, "-I", "-B", str(script), "dr-check", "--rpo-minutes", "1", "--rto-minutes", "60",
                              "--restore-minutes", "40", "--backup-interval-minutes", "5"], capture_output=True, text=True, timeout=20)
        self.assertEqual((0, 1), (ok.returncode, gap.returncode))


class PlanSummaryTests(unittest.TestCase):
    PLAN = {"resource_changes": [
        {"address": "google_sql_database_instance.main", "type": "google_sql_database_instance", "mode": "managed",
         "change": {"actions": ["delete"], "after": None}},
        {"address": "google_container_node_pool.gpu", "type": "google_container_node_pool", "mode": "managed",
         "change": {"actions": ["delete", "create"], "after": {"name": "gpu"}}},
        {"address": "google_project_iam_policy.all", "type": "google_project_iam_policy", "mode": "managed",
         "change": {"actions": ["create"], "after": {"policy_data": "{}"}}},
        {"address": "google_storage_bucket_iam_member.public", "type": "google_storage_bucket_iam_member", "mode": "managed",
         "change": {"actions": ["create"], "after": {"member": "allUsers", "role": "roles/storage.objectViewer"}}},
        {"address": "google_compute_firewall.open", "type": "google_compute_firewall", "mode": "managed",
         "change": {"actions": ["create"], "after": {"direction": "INGRESS", "source_ranges": ["0.0.0.0/0"], "allow": [{"protocol": "tcp"}]}}},
        {"address": "google_project_service.compute", "type": "google_project_service", "mode": "managed",
         "change": {"actions": ["delete"], "after": None}},
        {"address": "google_sql_database_instance.replica", "type": "google_sql_database_instance", "mode": "managed",
         "change": {"actions": ["update"], "after": {"deletion_protection": False}}},
        {"address": "google_compute_network.vpc", "type": "google_compute_network", "mode": "managed",
         "change": {"actions": ["no-op"], "after": {}}},
        {"address": "data.google_project.p", "type": "google_project", "mode": "data", "change": {"actions": ["read"]}},
    ]}

    def test_risky_changes_are_ranked(self):
        result = summarize(self.PLAN)
        self.assertEqual({"delete": 2, "replace": 1, "create": 3, "update": 1, "no-op": 1}, result["counts"])
        by_address: dict[str, str] = {}
        for finding in result["findings"]:  # sorted most severe first; keep the first severity per address
            by_address.setdefault(finding["address"], finding["severity"])
        self.assertEqual("Critical", by_address["google_sql_database_instance.main"])
        self.assertEqual("Critical", by_address["google_container_node_pool.gpu"])
        self.assertEqual("High", by_address["google_project_iam_policy.all"])
        self.assertEqual("Critical", by_address["google_storage_bucket_iam_member.public"])
        self.assertEqual("High", by_address["google_compute_firewall.open"])
        self.assertEqual("High", by_address["google_project_service.compute"])
        self.assertEqual("High", by_address["google_sql_database_instance.replica"])
        self.assertNotIn("google_compute_network.vpc", by_address)
        self.assertEqual("Critical", result["findings"][0]["severity"])

    def test_deny_rule_open_to_internet_is_not_flagged(self):
        plan = {"resource_changes": [{"address": "google_compute_firewall.deny", "type": "google_compute_firewall", "mode": "managed",
                                      "change": {"actions": ["create"], "after": {"source_ranges": ["0.0.0.0/0"], "deny": [{"protocol": "all"}]}}}]}
        self.assertEqual([], summarize(plan)["findings"])

    def test_cli_exit_codes(self):
        script = SKILLS / "gcp-iac-validation" / "scripts" / "plan_summary.py"
        with tempfile.TemporaryDirectory() as folder:
            risky, clean, bad = Path(folder, "risky.json"), Path(folder, "clean.json"), Path(folder, "bad.json")
            risky.write_text(json.dumps(self.PLAN), encoding="utf-8")
            clean.write_text(json.dumps({"resource_changes": []}), encoding="utf-8")
            bad.write_text("[]", encoding="utf-8")
            codes = [subprocess.run([sys.executable, "-I", "-B", str(script), str(p)], capture_output=True, timeout=20).returncode
                     for p in (risky, clean, bad)]
        self.assertEqual([1, 0, 2], codes)


class CompletionTests(unittest.TestCase):
    def setUp(self):
        self.valid = json.loads((ROOT / "tests" / "fixtures" / "valid-completion.json").read_text(encoding="utf-8"))

    def test_valid_fixture_conforms(self):
        self.assertEqual([], validate_completion(self.valid))

    def test_non_objects_and_partial_reports_fail(self):
        for value in ("text", 42, {}, {"status": "ANALYSIS_ONLY", "outcome": "partial"}):
            with self.subTest(value=value):
                self.assertNotEqual([], validate_completion(value))

    def test_complete_claim_with_unverified_items_and_proposed_decision_fails(self):
        problems = validate_completion(json.loads((ROOT / "tests" / "fixtures" / "invalid-completion.json").read_text(encoding="utf-8")))
        self.assertIn("COMPLETE_VERIFIED cannot have unverified items", problems)
        self.assertIn("COMPLETE_VERIFIED cannot have a decision still Proposed", problems)
        self.assertIn("COMPLETE_VERIFIED needs at least one check and every check passed", problems)

    def test_cloud_change_needs_recorded_approval(self):
        problems = validate_completion(json.loads((ROOT / "tests" / "fixtures" / "invalid-cloud-change.json").read_text(encoding="utf-8")))
        self.assertIn("cloud change without target, action and approval", problems)

    def test_passed_check_needs_integer_zero_exit_and_target(self):
        for field, value in (("exit_code", False), ("exit_code", 1), ("target", "")):
            report = copy.deepcopy(self.valid)
            report["checks"][0][field] = value
            with self.subTest(field=field, value=value):
                self.assertIn("a passed check needs exit code 0, a command, a target and evidence", validate_completion(report))

    def test_ready_for_review_cannot_hide_a_failed_check(self):
        report = copy.deepcopy(self.valid)
        report["checks"][0].update(status="failed", exit_code=1)
        self.assertIn("DESIGN_READY_FOR_REVIEW cannot have a failed criterion or check", validate_completion(report))

    def test_prepared_not_verified_states_the_fallback(self):
        report = copy.deepcopy(self.valid)
        report["status"] = "PREPARED_NOT_VERIFIED"
        self.assertTrue(validate_completion(report))
        report["outcome"] += " " + FALLBACK
        self.assertEqual([], validate_completion(report))

    def test_validator_matches_report_contract(self):
        contract = json.loads((ROOT / "tests" / "report-contract.yml").read_text(encoding="utf-8"))
        self.assertEqual(contract["required_fields"], REQUIRED)
        self.assertEqual(set(contract["statuses"]), STATUSES)
        self.assertEqual(contract["fallback"], FALLBACK)
        self.assertEqual(tuple(contract["check_fields"]), CHECK_FIELDS)
        instruction = (ROOT / ".apm" / "instructions" / "google-cloud-architect-contract.instructions.md").read_text(encoding="utf-8")
        self.assertIn(FALLBACK, instruction)
        for status in contract["statuses"]:
            self.assertIn(status, instruction)

    def test_cli(self):
        script = ROOT / "tooling" / "completion_contract.py"
        fixtures = ROOT / "tests" / "fixtures"
        codes = [subprocess.run([sys.executable, "-I", "-B", str(script), "--report", str(fixtures / name)], capture_output=True, timeout=20).returncode
                 for name in ("valid-completion.json", "invalid-completion.json", "missing.json")]
        self.assertEqual([0, 1, 2], codes)


class PackContentTests(unittest.TestCase):
    SECTIONS = ["Purpose and activation", "Scope and exclusions", "Inputs", "Dependencies and tools", "Workflow",
                "Output", "Validation", "Failure handling and escalation", "Permissions and guardrails", "Connection to the pack"]

    def skills(self) -> list[Path]:
        return sorted(p for p in SKILLS.iterdir() if p.is_dir())

    def test_every_skill_is_operational(self):
        for skill in self.skills():
            text = (skill / "SKILL.md").read_text(encoding="utf-8")
            with self.subTest(skill=skill.name):
                self.assertRegex(text, rf"(?m)^name: {re.escape(skill.name)}$")
                self.assertRegex(text, r"(?m)^description: \".*Use when [^.]+\.\"$")
                for section in self.SECTIONS:
                    self.assertIn(f"## {section}", text)

    def test_files_named_in_skills_exist_in_the_same_folder(self):
        for skill in self.skills():
            text = (skill / "SKILL.md").read_text(encoding="utf-8")
            for ref in set(re.findall(r"`((?:scripts/)?[\w.-]+\.(?:py|md))`", text)):
                if ref.endswith(".prompt.md") or ref == "SKILL.md":
                    continue
                with self.subTest(skill=skill.name, ref=ref):
                    self.assertTrue((skill / ref).is_file(), f"{skill.name} names {ref}")

    def test_tests_name_every_skill_and_existing_prompts(self):
        names = {p.name for p in self.skills()}
        prompts = {p.name for p in (ROOT / ".apm" / "prompts").glob("*.prompt.md")}
        coverage = json.loads((ROOT / "tests" / "capability-coverage.yml").read_text(encoding="utf-8"))
        triggers = json.loads((ROOT / "tests" / "trigger-cases.yml").read_text(encoding="utf-8"))
        self.assertEqual(sorted(names), sorted(r["skill"] for r in coverage["requirements"]))
        self.assertEqual(names, {s for case in triggers["cases"] for s in case["skills"]})
        for item in coverage["requirements"] + triggers["cases"]:
            self.assertIn(item["prompt"], prompts)

    def test_agents_declare_no_tools_and_one_primary(self):
        agents = sorted((ROOT / ".apm" / "agents").glob("*.agent.md"))
        primaries = 0
        for path in agents:
            front = path.read_text(encoding="utf-8").split("---")[1]
            self.assertNotRegex(front, r"(?m)^tools:")
            primaries += "user-invocable: true" in front
        self.assertEqual(1, primaries)
        permissions = (ROOT / "compatibility" / "tool-permissions.yml").read_text(encoding="utf-8")
        for path in agents:
            self.assertIn(f"  {path.name[:-len('.agent.md')]}:", permissions)

    def test_installed_content_references_only_installed_content(self):
        # Pack folders that are never installed; URL paths such as cloud.google.com/docs/ are allowed.
        pattern = re.compile(r"(?<![/\w.])(docs|tests|templates|tooling|hooks|shared)/")
        for path in (ROOT / ".apm").rglob("*.md"):
            with self.subTest(path=path.relative_to(ROOT).as_posix()):
                self.assertIsNone(pattern.search(path.read_text(encoding="utf-8")))


if __name__ == "__main__":
    unittest.main()
