#!/usr/bin/env python3
"""Check that every source rule in a migration to Cloudflare has exactly one valid disposition.

Reads a source rule list and mapping rows from JSON or CSV files; makes no network calls and
prints a JSON summary. Messages name source IDs only, never rule contents.

Source: a JSON list of objects with "id" (or {"rules": [...]}), or CSV with an id or source_id column.
Mapping: a JSON list (or {"rows": [...]}) or CSV with source_id, disposition, target, reason,
security_impact, owner and optional owner_decision columns.

Usage: python3 rule_accounting.py --source source.json --mapping mapping.csv
Exit 0 when no errors (check ready_to_enable separately), 1 when errors are found, 2 when input is unreadable.
"""
from __future__ import annotations

import argparse
import csv
import io
import json
import sys
from collections import defaultdict
from pathlib import Path
from typing import Any

MAX_BYTES = 20 * 1024 * 1024
DISPOSITIONS = ("migrated", "partial", "not_migrated", "needs_identity", "needs_posture", "manual_review")
MULTI_ROW_OK = {"migrated", "partial"}
ALWAYS_PENDING = {"needs_identity", "needs_posture", "manual_review"}
REQUIRED = {
    "migrated": ("target",),
    "partial": ("target", "reason", "security_impact"),
    "not_migrated": ("reason", "security_impact", "owner"),
    "needs_identity": ("reason",),
    "needs_posture": ("reason",),
    "manual_review": ("reason",),
}
MAX_LISTED = 50


def _text(value: Any) -> str:
    return value.strip() if isinstance(value, str) else ("" if value is None else str(value).strip())


def _label(value: str) -> str:
    return value if len(value) <= 128 else value[:125] + "..."


def read_records(path: Path, list_key: str) -> list[dict[str, Any]]:
    if path.is_symlink() or not path.is_file() or path.stat().st_size > MAX_BYTES:
        raise ValueError(f"{path.name}: missing, a symlink, or larger than the checker reads")
    text = path.read_text(encoding="utf-8-sig")
    if path.suffix.lower() == ".csv":
        reader = csv.DictReader(io.StringIO(text))
        return [{(k or "").strip().lower(): v for k, v in row.items()} for row in reader]
    data = json.loads(text)
    if isinstance(data, dict):
        data = data.get(list_key)
    if not isinstance(data, list) or not all(isinstance(r, dict) for r in data):
        raise ValueError(f"{path.name}: expected a list of objects")
    return data


def check(source: list[dict[str, Any]], mapping: list[dict[str, Any]]) -> dict[str, Any]:
    errors: list[str] = []
    source_ids: list[str] = []
    for index, rule in enumerate(source, start=1):
        rule_id = _text(rule.get("id", rule.get("source_id")))
        if not rule_id:
            errors.append(f"source rule #{index} has no id")
            continue
        source_ids.append(rule_id)
    seen: set[str] = set()
    for rule_id in source_ids:
        if rule_id in seen:
            errors.append(f"source id {_label(rule_id)} appears more than once in the source")
        seen.add(rule_id)

    rows_by_id: dict[str, list[dict[str, Any]]] = defaultdict(list)
    for index, row in enumerate(mapping, start=1):
        rule_id = _text(row.get("source_id"))
        disposition = _text(row.get("disposition")).lower()
        if not rule_id:
            errors.append(f"mapping row #{index} has no source_id")
            continue
        if rule_id not in seen:
            errors.append(f"mapping row #{index} refers to unknown source id {_label(rule_id)}")
            continue
        if disposition not in DISPOSITIONS:
            errors.append(f"source id {_label(rule_id)}: invalid disposition")
            continue
        missing = [field for field in REQUIRED[disposition] if not _text(row.get(field)) or (field == "target" and _text(row.get(field)).lower() == "none")]
        if missing:
            errors.append(f"source id {_label(rule_id)}: {disposition} row lacks {', '.join(missing)}")
        rows_by_id[rule_id].append({"disposition": disposition, "owner_decision": _text(row.get("owner_decision")).lower()})

    counts = {d: 0 for d in DISPOSITIONS}
    pending: list[str] = []
    for rule_id in dict.fromkeys(source_ids):
        rows = rows_by_id.get(rule_id, [])
        if not rows:
            errors.append(f"source id {_label(rule_id)} is not accounted for")
            continue
        dispositions = {r["disposition"] for r in rows}
        if len(rows) > 1 and not dispositions <= MULTI_ROW_OK:
            errors.append(f"source id {_label(rule_id)} has conflicting dispositions: {', '.join(sorted(dispositions))}")
            continue
        effective = "partial" if "partial" in dispositions else rows[0]["disposition"]
        counts[effective] += 1
        accepted = all(r["owner_decision"] == "accepted" for r in rows if r["disposition"] == "partial")
        if effective in ALWAYS_PENDING or (effective == "partial" and not accepted):
            pending.append(_label(rule_id))

    return {
        "tool": "rule_accounting",
        "version": 1,
        "source_rules": len(source_ids),
        "mapping_rows": len(mapping),
        "counts": counts,
        "error_count": len(errors),
        "errors": errors[:MAX_LISTED],
        "pending_count": len(pending),
        "pending": pending[:MAX_LISTED],
        "ready_to_enable": not errors and not pending,
    }


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    parser.add_argument("--source", required=True, type=Path)
    parser.add_argument("--mapping", required=True, type=Path)
    args = parser.parse_args()
    try:
        result = check(read_records(args.source, "rules"), read_records(args.mapping, "rows"))
    except (OSError, ValueError, csv.Error) as exc:
        message = str(exc) if isinstance(exc, ValueError) and not isinstance(exc, json.JSONDecodeError) else type(exc).__name__
        print(json.dumps({"tool": "rule_accounting", "error": message}))
        return 2
    print(json.dumps(result, indent=2))
    return 1 if result["error_count"] else 0


if __name__ == "__main__":
    sys.exit(main())
