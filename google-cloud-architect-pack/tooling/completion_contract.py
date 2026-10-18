"""Check a Google Cloud Architect completion report against the pack's report contract.

The checker reads the report only. It never runs or trusts the commands the report lists.
Usage: python tooling/completion_contract.py --report completion.json
Exit 0 when the report conforms, 1 when it does not, 2 when it cannot be read.
"""
from __future__ import annotations

import argparse
import json
import sys
from pathlib import Path
from typing import Any

REQUIRED = ["outcome", "acceptance_criteria", "deliverables", "decisions", "assumptions", "security_posture",
            "reliability_posture", "cost_estimate", "sustainability_impact", "operational_impact", "performance_impact",
            "compliance_and_residency", "cloud_changes", "checks", "unverified", "remaining_risks", "rollback", "followups"]
STATUSES = {"COMPLETE_VERIFIED", "DESIGN_READY_FOR_REVIEW", "PREPARED_NOT_VERIFIED", "ANALYSIS_ONLY",
            "CHANGES_REQUIRED", "BLOCKED_ON_HUMAN_DECISION"}
RESULT_STATUSES = {"passed", "failed", "unverified"}
DECISION_STATUSES = {"Proposed", "Accepted", "Superseded", "Rejected"}
CHECK_FIELDS = ("command", "target", "exit_code", "status", "evidence")
CHANGE_FIELDS = ("target", "action", "approval")
FALLBACK = "The design is prepared, but completion is not verified."
MAX_BYTES = 262144


def _items(report: dict[str, Any], key: str, problems: list[str]) -> list[dict[str, Any]]:
    """Return the dict entries of a list field, recording a problem for a non-list or a non-object entry."""
    value = report.get(key)
    if not isinstance(value, list):
        problems.append(f"{key} is not a list")
        return []
    if not all(isinstance(entry, dict) for entry in value):
        problems.append(f"{key} has an entry that is not an object")
    return [entry for entry in value if isinstance(entry, dict)]


def _check_problems(check: dict[str, Any]) -> list[str]:
    if any(field not in check for field in CHECK_FIELDS):
        return ["check needs command, target, exit_code, status and evidence"]
    if check["status"] not in RESULT_STATUSES:
        return ["check status is not passed, failed or unverified"]
    succeeded = type(check["exit_code"]) is int and check["exit_code"] == 0
    if check["status"] == "passed" and not (succeeded and check["command"] and check["target"] and check["evidence"]):
        return ["a passed check needs exit code 0, a command, a target and evidence"]
    return []


def _status_problems(status: str, criteria: list[dict[str, Any]], checks: list[dict[str, Any]],
                     decisions: list[dict[str, Any]], unverified: object, outcome: str) -> list[str]:
    problems: list[str] = []

    def passed(entries: list[dict[str, Any]]) -> bool:
        return bool(entries) and all(e.get("status") == "passed" for e in entries)

    def failed(entries: list[dict[str, Any]]) -> bool:
        return any(e.get("status") == "failed" for e in entries)

    if status == "COMPLETE_VERIFIED":
        if not passed(criteria):
            problems.append("COMPLETE_VERIFIED needs every criterion passed")
        if not passed(checks):
            problems.append("COMPLETE_VERIFIED needs at least one check and every check passed")
        if unverified:
            problems.append("COMPLETE_VERIFIED cannot have unverified items")
        if any(d.get("status") == "Proposed" for d in decisions):
            problems.append("COMPLETE_VERIFIED cannot have a decision still Proposed")
    elif status == "DESIGN_READY_FOR_REVIEW":
        if not criteria:
            problems.append("DESIGN_READY_FOR_REVIEW needs acceptance criteria")
        if failed(criteria) or failed(checks):
            problems.append("DESIGN_READY_FOR_REVIEW cannot have a failed criterion or check")
    elif status == "PREPARED_NOT_VERIFIED" and FALLBACK not in outcome:
        problems.append("PREPARED_NOT_VERIFIED outcome must contain the fallback sentence")
    return problems


def validate_completion(report: Any) -> list[str]:
    """Return the list of contract problems; an empty list means the report conforms."""
    if not isinstance(report, dict):
        return ["the report is not a JSON object"]
    problems = [f"field missing: {key}" for key in REQUIRED if key not in report]
    status = report.get("status")
    if status not in STATUSES:
        problems.append("status is not one of the contract statuses")

    criteria = _items(report, "acceptance_criteria", problems)
    for criterion in criteria:
        if not criterion.get("id") or criterion.get("status") not in RESULT_STATUSES or not criterion.get("evidence"):
            problems.append("criterion needs an id, a status of passed, failed or unverified, and evidence")
    checks = _items(report, "checks", problems)
    for check in checks:
        problems.extend(_check_problems(check))
    decisions = _items(report, "decisions", problems)
    for decision in decisions:
        if not decision.get("id") or decision.get("status") not in DECISION_STATUSES:
            problems.append("decision needs an id and a status of Proposed, Accepted, Superseded or Rejected")
    for change in _items(report, "cloud_changes", problems):
        if not all(change.get(field) for field in CHANGE_FIELDS):
            problems.append("cloud change without target, action and approval")
    unverified = report.get("unverified")
    if not isinstance(unverified, list):
        problems.append("unverified is not a list")

    problems.extend(_status_problems(str(status), criteria, checks, decisions, unverified, str(report.get("outcome", ""))))
    return problems


def main(argv: list[str]) -> int:
    parser = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    parser.add_argument("--report", type=Path, required=True)
    args = parser.parse_args(argv)
    try:
        if args.report.stat().st_size > MAX_BYTES:
            raise ValueError("report too large")
        problems = validate_completion(json.loads(args.report.read_text(encoding="utf-8")))
    except (OSError, ValueError):
        print(json.dumps({"conforms": False, "problems": ["report could not be read, is too large or is not JSON"]}))
        return 2
    print(json.dumps({"conforms": not problems, "problems": problems}))
    return 1 if problems else 0


if __name__ == "__main__":
    raise SystemExit(main(sys.argv[1:]))
