"""Validate the shape of a Notion completion report against tests/report-contract.yml.

The validator checks structure and internal consistency only. It never contacts Notion and never
treats a report's claims as proof; a reviewer still has to look at the cited pages and commands.

Usage: python tooling/completion_contract.py REPORT.json
Exit 0 when the report is valid, 1 when it is not, 2 when the file cannot be read.
"""
from __future__ import annotations

import json
import sys
from pathlib import Path
from typing import Any

CONTRACT_PATH = Path(__file__).resolve().parent.parent / "tests" / "report-contract.yml"
MAX_BYTES = 1_000_000


def load_contract(path: Path = CONTRACT_PATH) -> dict[str, Any]:
    # report-contract.yml is written as JSON, which is also valid YAML.
    return json.loads(path.read_text(encoding="utf-8"))


def _list(value: Any, name: str, errors: list[str]) -> list[Any]:
    if isinstance(value, list):
        return value
    errors.append(f"{name} must be a list")
    return []


def validate_completion(value: Any, contract: dict[str, Any] | None = None) -> list[str]:
    c = contract or load_contract()
    if not isinstance(value, dict):
        return ["report must be an object"]
    errors = ["missing field: " + key for key in c["required_fields"] if key not in value]
    status = value.get("status")
    if status not in c["statuses"]:
        errors.append("invalid status")

    criteria = _list(value.get("acceptance_criteria"), "acceptance_criteria", errors)
    for criterion in criteria:
        if (not isinstance(criterion, dict) or criterion.get("status") not in c["criterion_statuses"]
                or not criterion.get("id") or not criterion.get("evidence")):
            errors.append("invalid criterion")

    checks = _list(value.get("checks"), "checks", errors)
    for check in checks:
        if not isinstance(check, dict) or any(key not in check for key in c["check_fields"]):
            errors.append("invalid check")
        elif check["method"] not in c["check_methods"]:
            errors.append("invalid check method")
        elif check["status"] not in c["criterion_statuses"]:
            errors.append("invalid check status")
        elif check["status"] == "passed":
            if not check["evidence"] or not check["check"]:
                errors.append("passing check lacks evidence")
            # bool is a subclass of int, so compare the exact type.
            if check["method"] == "command" and (type(check.get("exit_code")) is not int or check["exit_code"] != 0):
                errors.append("passing command check lacks a zero exit code")

    changes = _list(value.get("notion_changes"), "notion_changes", errors)
    for change in changes:
        if not isinstance(change, dict) or any(key not in change for key in c["change_fields"]):
            errors.append("invalid notion change")
        elif change["action"] not in c["change_actions"]:
            errors.append("invalid notion change action")

    unverified = _list(value.get("unverified"), "unverified", errors)

    if status == "ANALYSIS_ONLY" and changes:
        errors.append("analysis-only report lists workspace changes")
    if status == "COMPLETE_VERIFIED":
        if not criteria or any(not isinstance(x, dict) or x.get("status") != "passed" for x in criteria):
            errors.append("complete claim requires all criteria passed")
        if not checks or any(not isinstance(x, dict) or x.get("status") != "passed" for x in checks):
            errors.append("complete claim requires passing checks")
        if unverified:
            errors.append("complete claim has unverified items")
        if changes:
            if any(not isinstance(x, dict) or not str(x.get("url", "")).startswith("https://") for x in changes):
                errors.append("complete claim requires a URL for every workspace change")
            if not any(isinstance(x, dict) and x.get("method") == "fetch" and x.get("status") == "passed" for x in checks):
                errors.append("complete claim requires a passing fetch check for workspace changes")
    return errors


def main(argv: list[str]) -> int:
    if len(argv) != 2:
        print("usage: completion_contract.py REPORT.json", file=sys.stderr)
        return 2
    path = Path(argv[1])
    try:
        if path.stat().st_size > MAX_BYTES:
            raise ValueError("report too large")
        report = json.loads(path.read_text(encoding="utf-8"))
    except (OSError, ValueError):
        print(json.dumps({"valid": False, "errors": ["report unreadable, too large or not JSON"]}))
        return 2
    errors = validate_completion(report)
    print(json.dumps({"valid": not errors, "errors": errors}))
    return int(bool(errors))


if __name__ == "__main__":
    raise SystemExit(main(sys.argv))
