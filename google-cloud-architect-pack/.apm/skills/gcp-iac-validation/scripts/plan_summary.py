#!/usr/bin/env python3
"""Summarize a Terraform JSON plan for Google Cloud and flag risky changes. Reads a file; never runs Terraform.

Usage: terraform show -json tfplan > tfplan.json && python plan_summary.py tfplan.json
Exit 0 when no Critical or High risk is found, 1 when one is, 2 when the input cannot be read.
"""
from __future__ import annotations

import json
import sys
from pathlib import Path

STATEFUL_TYPES = {
    "google_sql_database_instance", "google_sql_database", "google_alloydb_cluster", "google_alloydb_instance",
    "google_spanner_instance", "google_spanner_database", "google_bigquery_dataset", "google_bigquery_table",
    "google_storage_bucket", "google_compute_disk", "google_compute_region_disk", "google_container_cluster",
    "google_container_node_pool", "google_bigtable_instance", "google_bigtable_table", "google_firestore_database",
    "google_filestore_instance", "google_redis_instance", "google_redis_cluster", "google_memorystore_instance",
    "google_kms_crypto_key", "google_kms_key_ring", "google_secret_manager_secret", "google_project", "google_folder",
    "google_logging_project_bucket_config", "google_pubsub_topic", "google_pubsub_subscription",
}
POLICY_TYPES = {"google_org_policy_policy", "google_organization_policy", "google_folder_organization_policy",
                "google_project_organization_policy", "google_access_context_manager_service_perimeter",
                "google_access_context_manager_access_policy"}
AUTHORITATIVE_IAM_POLICY = {"google_project_iam_policy", "google_folder_iam_policy", "google_organization_iam_policy"}
PUBLIC_MEMBERS = ("allUsers", "allAuthenticatedUsers")
BASIC_ROLES = {"roles/owner", "roles/editor", "roles/viewer"}


def classify_actions(actions: list[str]) -> str:
    if actions in (["delete", "create"], ["create", "delete"]):
        return "replace"
    if actions in (["create"], ["update"], ["delete"], ["read"], ["no-op"]):
        return actions[0]
    return "+".join(actions) or "unknown"


def _strings(value: object) -> list[str]:
    if isinstance(value, str):
        return [value]
    if isinstance(value, dict):
        return [s for v in value.values() for s in _strings(v)]
    if isinstance(value, list):
        return [s for v in value for s in _strings(v)]
    return []


def summarize(plan: object) -> dict[str, object]:
    if not isinstance(plan, dict) or not isinstance(plan.get("resource_changes", []), list):
        raise ValueError("not a Terraform JSON plan")
    counts: dict[str, int] = {}
    findings: list[dict[str, str]] = []

    def flag(severity: str, address: str, reason: str) -> None:
        findings.append({"severity": severity, "address": address, "reason": reason})

    for rc in plan.get("resource_changes", []):
        if not isinstance(rc, dict) or rc.get("mode") == "data":
            continue
        rtype = str(rc.get("type", ""))
        address = str(rc.get("address", rtype))
        change = rc.get("change") or {}
        action = classify_actions(list(change.get("actions") or []))
        counts[action] = counts.get(action, 0) + 1
        after = change.get("after") or {}
        after_strings = _strings(after)

        if action in ("delete", "replace"):
            if rtype in STATEFUL_TYPES:
                flag("Critical", address, f"{action} of a stateful or irreplaceable resource; confirm intent and a tested backup")
            elif rtype == "google_project_service":
                flag("High", address, "disables an API; dependent resources may stop working")
            else:
                flag("Medium", address, f"{action}; confirm the resource is not in use")
        if action == "no-op" or action == "read":
            continue
        if rtype == "google_service_account_key":
            flag("High", address, "creates a long-lived service account key; use federation or impersonation")
        if rtype in AUTHORITATIVE_IAM_POLICY:
            flag("High", address, "authoritative IAM policy replaces every binding, including owners and service agents")
        elif "_iam_" in rtype:
            if any(member in s for s in after_strings for member in PUBLIC_MEMBERS):
                flag("Critical", address, "grants access to allUsers or allAuthenticatedUsers")
            elif any(s in BASIC_ROLES for s in after_strings):
                flag("High", address, "grants a basic role (owner, editor or viewer)")
            elif action in ("create", "update", "replace"):
                flag("Low", address, "IAM change; confirm least privilege")
        if rtype in POLICY_TYPES:
            flag("High", address, "organization policy or perimeter change affects every resource in scope")
        if rtype == "google_compute_firewall" and isinstance(after, dict):
            sources = after.get("source_ranges") or []
            if after.get("direction", "INGRESS") == "INGRESS" and "0.0.0.0/0" in sources and not after.get("deny"):
                flag("High", address, "allows ingress from 0.0.0.0/0")
        if rtype in ("google_cloud_run_v2_service", "google_cloud_run_service") and "INGRESS_TRAFFIC_ALL" in after_strings:
            flag("Medium", address, "Cloud Run ingress allows all traffic; confirm a load balancer is not being bypassed")
        if isinstance(after, dict) and after.get("deletion_protection") is False and rtype in STATEFUL_TYPES:
            flag("High", address, "deletion_protection is false on a stateful resource")

    order = {"Critical": 0, "High": 1, "Medium": 2, "Low": 3}
    findings.sort(key=lambda f: (order.get(f["severity"], 9), f["address"]))
    return {"counts": counts, "findings": findings,
            "limits": "A plan shows intended changes only; it does not prove permissions, quotas, policy approval or runtime behaviour."}


def main(argv: list[str]) -> int:
    if len(argv) != 2:
        print(json.dumps({"error": "usage: plan_summary.py tfplan.json"}))
        return 2
    try:
        result = summarize(json.loads(Path(argv[1]).read_text(encoding="utf-8")))
    except (OSError, ValueError) as exc:
        print(json.dumps({"error": f"cannot read plan: {exc}"}))
        return 2
    print(json.dumps(result, indent=2))
    return 1 if any(f["severity"] in ("Critical", "High") for f in result["findings"]) else 0


if __name__ == "__main__":
    raise SystemExit(main(sys.argv))
