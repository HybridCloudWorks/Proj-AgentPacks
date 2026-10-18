"""Validate the shape of a Cloudflare completion report without executing any claimed command.

The field names and statuses mirror tests/report-contract.yml and the always-on contract instruction.
A report that passes is well formed and internally consistent; it is not proof that the work happened.
"""
from __future__ import annotations

import re
from typing import Any

REQUIRED = ["outcome", "acceptance_criteria", "target_scope", "files_changed", "account_changes", "decisions",
            "sources_consulted", "limits_and_entitlements", "checks", "security_review", "secrets_handling",
            "blast_radius", "cost_impact", "observability", "rollout", "rollback", "unverified",
            "remaining_risks", "followups"]
STATUSES = {"COMPLETE_VERIFIED", "CHANGE_PREPARED_NOT_APPLIED", "APPLIED_NOT_VERIFIED", "ANALYSIS_ONLY",
            "CHANGES_REQUIRED", "BLOCKED_ON_HUMAN_DECISION"}
RESULTS = {"passed", "failed", "unverified"}
ENVIRONMENTS = {"local", "preview", "staging", "production"}
CHECK_FIELDS = ("command", "environment", "exit_code", "status", "evidence")
CREDENTIAL = re.compile(r"(?i)(bearer\s+[a-z0-9._~+/=-]{20,}|\b(api[_-]?token|api[_-]?key|secret|password|tunnel[_-]?token)\b\s*[=:]\s*[^\s,;\"']{12,})")


def _strings(value: Any) -> list[str]:
    if isinstance(value, str):
        return [value]
    if isinstance(value, dict):
        return [s for v in value.values() for s in _strings(v)]
    if isinstance(value, list):
        return [s for v in value for s in _strings(v)]
    return []


def _passed(check: Any) -> bool:
    return isinstance(check, dict) and check.get("status") == "passed"


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
        if not isinstance(criterion, dict) or criterion.get("status") not in RESULTS or not criterion.get("id") or not criterion.get("evidence"):
            errors.append("invalid criterion")

    checks = value.get("checks")
    if not isinstance(checks, list):
        errors.append("checks must be a list")
        checks = []
    for check in checks:
        if not isinstance(check, dict) or not all(key in check for key in CHECK_FIELDS):
            errors.append("invalid check")
        elif check["status"] not in RESULTS:
            errors.append("invalid check status")
        elif check["environment"] not in ENVIRONMENTS:
            errors.append("invalid check environment")
        elif check["status"] == "passed" and (type(check["exit_code"]) is not int or check["exit_code"] != 0
                                              or not check["evidence"] or not check["command"]):
            errors.append("passing check lacks successful evidence")

    for key in ("unverified", "account_changes", "files_changed"):
        if key in value and not isinstance(value.get(key), list):
            errors.append(f"{key} must be a list")
    account_changes = value.get("account_changes") if isinstance(value.get("account_changes"), list) else []
    has_rollback = bool(str(value.get("rollback") or "").strip())

    if status == "COMPLETE_VERIFIED":
        if not criteria or any(not isinstance(c, dict) or c.get("status") != "passed" for c in criteria):
            errors.append("complete claim requires all criteria passed")
        if not checks or not all(_passed(c) for c in checks):
            errors.append("complete claim requires passing checks")
        if value.get("unverified"):
            errors.append("complete claim has unverified items")
        if account_changes and not any(_passed(c) and c.get("environment") != "local" for c in checks):
            errors.append("complete claim with account changes requires a passing check in the changed environment")
    if status == "APPLIED_NOT_VERIFIED" and not account_changes:
        errors.append("applied status requires recorded account changes")
    if status == "CHANGE_PREPARED_NOT_APPLIED" and account_changes:
        errors.append("prepared status cannot list account changes")
    if account_changes and not has_rollback:
        errors.append("account changes require a rollback")
    if any(CREDENTIAL.search(text) for text in _strings(value)):
        errors.append("report appears to contain a credential")
    return errors
