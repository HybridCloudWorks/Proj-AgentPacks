"""Validate the shape of a Docker completion report without executing any claimed command.

The constants mirror tests/report-contract.yml; a unit test keeps them in step.
"""
from __future__ import annotations

from typing import Any

REQUIRED = ["outcome", "acceptance_criteria", "files_changed", "decisions", "image_impact", "runtime_contract_impact",
            "security_review", "supply_chain_impact", "platform_compatibility", "operational_impact", "checks",
            "unverified", "remaining_risks", "rollback", "followups"]
STATUSES = {"COMPLETE_VERIFIED", "IMPLEMENTATION_PREPARED_NOT_VERIFIED", "ANALYSIS_ONLY", "CHANGES_REQUIRED",
            "BLOCKED_ON_HUMAN_DECISION"}
CRITERION_STATUSES = {"passed", "failed", "unverified"}
CRITERION_FIELDS = ("id", "status", "evidence", "evidence_level")
CHECK_FIELDS = ("command", "exit_code", "status", "environment", "evidence")
EVIDENCE_LEVELS = {"static", "local_build", "local_runtime", "scan", "live"}
FALLBACK = "Container change is prepared, but completion is not verified."


def validate_completion(value: Any) -> list[str]:
    if not isinstance(value, dict):
        return ["report must be an object"]
    errors = ["missing field: " + key for key in REQUIRED if key not in value]
    status = value.get("status")
    if status not in STATUSES:
        errors.append("invalid status")
    criteria = value.get("acceptance_criteria")
    if not isinstance(criteria, list):
        errors.append("acceptance_criteria must be a list")
        criteria = []
    for criterion in criteria:
        if not isinstance(criterion, dict) or not all(criterion.get(k) for k in CRITERION_FIELDS):
            errors.append("criterion needs id, status, evidence and evidence_level")
        elif criterion["status"] not in CRITERION_STATUSES:
            errors.append("invalid criterion status")
        elif criterion["evidence_level"] not in EVIDENCE_LEVELS:
            errors.append("invalid evidence level")
    checks = value.get("checks")
    if not isinstance(checks, list):
        errors.append("checks must be a list")
        checks = []
    for check in checks:
        if not isinstance(check, dict) or not all(key in check for key in CHECK_FIELDS):
            errors.append("check needs command, exit_code, status, environment and evidence")
        elif check["status"] not in CRITERION_STATUSES:
            errors.append("invalid check status")
        elif check["status"] == "passed" and (type(check["exit_code"]) is not int or check["exit_code"] != 0
                                              or not check["command"] or not check["evidence"] or not check["environment"]):
            errors.append("passing check lacks a zero exit code, command, environment or evidence")
    if not isinstance(value.get("unverified"), list):
        errors.append("unverified must be a list")
    if status == "COMPLETE_VERIFIED":
        if not criteria or any(not isinstance(c, dict) or c.get("status") != "passed" for c in criteria):
            errors.append("complete claim requires every criterion passed")
        if not checks or any(not isinstance(c, dict) or c.get("status") != "passed" for c in checks):
            errors.append("complete claim requires passing checks")
        if value.get("unverified"):
            errors.append("complete claim has unverified items")
    return errors
