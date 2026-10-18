"""Validate the shape of a FinOps completion report without trusting its claims."""
from __future__ import annotations

from typing import Any

REQUIRED = ["outcome", "audience", "scope", "data_sources", "cost_basis", "acceptance_criteria", "findings",
            "recommendations", "checks", "assumptions", "data_quality", "approvals", "financial_impact", "tradeoffs",
            "unverified", "risks", "rollback", "followups"]
STATUSES = {"VERIFIED_COMPLETE", "PREPARED_NOT_VERIFIED", "ANALYSIS_ONLY", "CHANGES_REQUIRED", "BLOCKED_ON_APPROVAL",
            "BLOCKED_ON_DATA"}
OUTCOMES = {"passed", "failed", "unverified"}
COST_COLUMNS = {"BilledCost", "EffectiveCost", "ListCost", "ContractedCost"}
CHECK_FIELDS = ("name", "method", "observed", "status", "evidence")
RECOMMENDATION_FIELDS = ("action", "owner", "monthly_impact_range", "savings_type", "confidence", "tradeoff",
                         "reversibility", "approval_level")
SAVINGS_TYPES = {"estimated", "realized"}


def _number(value: Any) -> bool:
    return isinstance(value, (int, float)) and not isinstance(value, bool)


def _cost_basis_errors(basis: Any) -> list[str]:
    if not isinstance(basis, dict):
        return ["cost_basis must be an object"]
    column = basis.get("column")
    if column == "not applicable":
        return []
    if column not in COST_COLUMNS and basis.get("focus_equivalent") not in COST_COLUMNS:
        return ["cost_basis must name a FOCUS cost column or the FOCUS equivalent of a native column"]
    if not basis.get("filters"):
        return ["cost_basis must state the filters applied"]
    return []


def _recommendation_errors(item: Any, has_passed_check: bool) -> list[str]:
    if not isinstance(item, dict) or any(key not in item for key in RECOMMENDATION_FIELDS):
        return ["recommendation missing required fields"]
    errors = []
    impact = item["monthly_impact_range"]
    if not (isinstance(impact, list) and len(impact) == 2 and all(_number(v) for v in impact) and impact[0] <= impact[1]):
        errors.append("monthly_impact_range must be [low, high] with low <= high")
    if item["savings_type"] not in SAVINGS_TYPES:
        errors.append("savings_type must be estimated or realized")
    elif item["savings_type"] == "realized" and not has_passed_check:
        errors.append("realized savings need a passed measurement check")
    if item["approval_level"] not in (0, 1, 2) or isinstance(item["approval_level"], bool):
        errors.append("approval_level must be 0, 1 or 2")
    if not item["owner"]:
        errors.append("recommendation needs an owner")
    return errors


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
        if not isinstance(criterion, dict) or criterion.get("status") not in OUTCOMES or not criterion.get("id") or not criterion.get("evidence"):
            errors.append("invalid criterion")

    checks = value.get("checks")
    if not isinstance(checks, list):
        errors.append("checks must be a list")
        checks = []
    passed = 0
    for check in checks:
        if not isinstance(check, dict) or any(key not in check for key in CHECK_FIELDS):
            errors.append("invalid check")
        elif check["status"] not in OUTCOMES:
            errors.append("invalid check status")
        elif check["status"] == "passed":
            if not (check["method"] and check["observed"] not in (None, "") and check["evidence"]):
                errors.append("passing check lacks method, observed result or evidence")
            else:
                passed += 1

    if "cost_basis" in value:
        errors += _cost_basis_errors(value["cost_basis"])
    recommendations = value.get("recommendations")
    if not isinstance(recommendations, list):
        errors.append("recommendations must be a list")
        recommendations = []
    for item in recommendations:
        errors += _recommendation_errors(item, passed > 0)
    if isinstance(value.get("cost_basis"), dict) and value["cost_basis"].get("column") == "not applicable" and recommendations:
        errors.append("recommendations with financial impact need a cost basis")

    if not isinstance(value.get("unverified"), list):
        errors.append("unverified must be a list")
    if status == "VERIFIED_COMPLETE":
        if not criteria or any(not isinstance(c, dict) or c.get("status") != "passed" for c in criteria):
            errors.append("verified claim requires every criterion passed")
        if not checks or passed != len(checks):
            errors.append("verified claim requires executed, passing checks")
        if value.get("unverified"):
            errors.append("verified claim has unverified items")
    return errors
