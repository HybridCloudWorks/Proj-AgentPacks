"""Validate completion evidence shape without executing claimed commands."""
from __future__ import annotations
from typing import Any

REQUIRED = ["outcome","acceptance_criteria","files_changed","decisions","public_contract_impact","dependency_impact","data_migration_impact","checks","security_review","observability_impact","operational_impact","performance_impact","cost_impact","compatibility","unverified","remaining_risks","rollback","followups"]
STATUSES = {"COMPLETE_VERIFIED", "IMPLEMENTATION_PREPARED_NOT_VERIFIED", "ANALYSIS_ONLY", "CHANGES_REQUIRED", "BLOCKED_ON_HUMAN_DECISION"}


def validate_completion(value: Any) -> list[str]:
    if not isinstance(value, dict):
        return ["report must be an object"]
    errors = ["missing field: " + key for key in REQUIRED if key not in value]
    status = value.get("status")
    if status not in STATUSES:
        errors.append("invalid status")
    criteria = value.get("acceptance_criteria")
    checks = value.get("checks")
    if not isinstance(criteria, list):
        errors.append("acceptance_criteria must be a list")
        criteria = []
    for criterion in criteria:
        if not isinstance(criterion, dict) or criterion.get("status") not in {"passed", "failed", "unverified"} or not criterion.get("id") or not criterion.get("evidence"):
            errors.append("invalid criterion")
    if not isinstance(checks, list):
        errors.append("checks must be a list")
        checks = []
    for check in checks:
        if not isinstance(check, dict) or not all(key in check for key in ("command", "exit_code", "status", "evidence")):
            errors.append("invalid check")
        elif check["status"] not in {"passed", "failed", "unverified"}:
            errors.append("invalid check status")
        elif check["status"] == "passed" and (type(check["exit_code"]) is not int or check["exit_code"] != 0 or not check["evidence"] or not check["command"]):
            errors.append("passing check lacks successful evidence")
    if not isinstance(value.get("unverified"), list):
        errors.append("unverified must be a list")
    if status == "COMPLETE_VERIFIED":
        if not criteria or any(not isinstance(c, dict) or c.get("status") != "passed" for c in criteria):
            errors.append("complete claim requires all criteria passed")
        if not checks or any(not isinstance(c, dict) or c.get("status") != "passed" for c in checks):
            errors.append("complete claim requires passing checks")
        if value.get("unverified"):
            errors.append("complete claim has unverified items")
    return errors
