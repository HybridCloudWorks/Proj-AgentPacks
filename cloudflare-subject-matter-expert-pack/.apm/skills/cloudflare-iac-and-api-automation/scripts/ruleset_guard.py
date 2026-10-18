#!/usr/bin/env python3
"""Compare a current Cloudflare ruleset export with a proposed full rule list before replacing it.

Replacing an entry-point ruleset overwrites every rule in it, so a proposed list that forgets a
rule deletes that rule. This guard reports added, removed, modified and reordered rules, phase
mismatches and catch-all rules. It reads local JSON only and makes no network calls.

Accepted input shapes: an API envelope {"result": {...}}, a ruleset object {"phase": ..., "rules": [...]},
or a plain list of rules.

Usage: python3 ruleset_guard.py --current current.json --proposed proposed.json [--allow-removal]
Exit 0 when safe to apply, 1 when not safe, 2 when input is unreadable.
"""
from __future__ import annotations

import argparse
import json
import sys
from pathlib import Path
from typing import Any

MAX_BYTES = 10 * 1024 * 1024
COMPARED_FIELDS = ("action", "expression", "enabled", "action_parameters", "ratelimit", "logging")
CATCH_ALL_ERROR = {"block", "skip"}
CATCH_ALL_WARN = {"challenge", "js_challenge", "managed_challenge"}


def load_ruleset(path: Path) -> tuple[str | None, list[dict[str, Any]]]:
    if path.is_symlink() or not path.is_file() or path.stat().st_size > MAX_BYTES:
        raise ValueError(f"{path.name}: missing, a symlink, or larger than the guard reads")
    data = json.loads(path.read_text(encoding="utf-8-sig"))
    if isinstance(data, dict) and isinstance(data.get("result"), dict):
        data = data["result"]
    if isinstance(data, list):
        phase, rules = None, data
    elif isinstance(data, dict):
        phase, rules = data.get("phase"), data.get("rules", [])
    else:
        raise ValueError(f"{path.name}: not a ruleset")
    if not isinstance(rules, list) or not all(isinstance(r, dict) for r in rules):
        raise ValueError(f"{path.name}: rules must be a list of objects")
    return (str(phase) if phase else None), rules


def label(rule: dict[str, Any], index: int) -> str:
    for key in ("ref", "id", "description"):
        value = rule.get(key)
        if isinstance(value, str) and value.strip():
            text = value.strip()
            return text if len(text) <= 80 else text[:77] + "..."
    return f"#{index + 1}"


def _canonical(value: Any) -> str:
    return json.dumps(value, sort_keys=True, separators=(",", ":"))


def _enabled(rule: dict[str, Any]) -> bool:
    return rule.get("enabled", True) is not False


def compare(current: list[dict[str, Any]], proposed: list[dict[str, Any]], current_phase: str | None = None,
            proposed_phase: str | None = None, allow_removal: bool = False) -> dict[str, Any]:
    findings: list[dict[str, str]] = []
    if current_phase and proposed_phase and current_phase != proposed_phase:
        findings.append({"level": "error", "code": "phase-mismatch", "message": f"current phase {current_phase} differs from proposed phase {proposed_phase}"})

    indexes: dict[str, dict[str, int]] = {"id": {}, "ref": {}, "description": {}}
    duplicate_descriptions: set[str] = set()
    for i, rule in enumerate(current):
        for key in indexes:
            value = rule.get(key)
            if isinstance(value, str) and value.strip():
                if key == "description" and value in indexes[key]:
                    duplicate_descriptions.add(value)
                indexes[key].setdefault(value, i)
    for value in duplicate_descriptions:
        indexes["description"].pop(value, None)

    matched: dict[int, int] = {}
    added: list[str] = []
    modified: list[dict[str, Any]] = []
    for j, rule in enumerate(proposed):
        if not rule.get("action") or not isinstance(rule.get("expression"), str) or not rule["expression"].strip():
            findings.append({"level": "error", "code": "incomplete-rule", "message": f"proposed rule {label(rule, j)} lacks an action or expression"})
        expression = rule.get("expression", "").strip().lower() if isinstance(rule.get("expression"), str) else ""
        action = str(rule.get("action", "")).lower()
        if _enabled(rule) and expression == "true" and action in CATCH_ALL_ERROR:
            findings.append({"level": "error", "code": "catch-all", "message": f"proposed rule {label(rule, j)} applies {action} to all traffic"})
        elif _enabled(rule) and expression == "true" and action in CATCH_ALL_WARN:
            findings.append({"level": "warn", "code": "catch-all-challenge", "message": f"proposed rule {label(rule, j)} challenges all traffic, including API clients"})
        match = next((indexes[key][rule[key]] for key in ("id", "ref", "description")
                      if isinstance(rule.get(key), str) and rule[key] in indexes[key] and indexes[key][rule[key]] not in matched), None)
        if match is None:
            added.append(label(rule, j))
            continue
        matched[match] = j
        changed = [f for f in COMPARED_FIELDS if _canonical(current[match].get(f)) != _canonical(rule.get(f))
                   and not (f == "enabled" and _enabled(current[match]) == _enabled(rule))]
        if changed:
            modified.append({"rule": label(rule, j), "fields": changed})

    removed = [label(rule, i) for i, rule in enumerate(current) if i not in matched]
    order = [matched[i] for i in sorted(matched)]
    reordered = order != sorted(order)
    if removed and not allow_removal:
        findings.append({"level": "error", "code": "rules-removed", "message": f"{len(removed)} current rules are missing from the proposed list and would be deleted"})
    if reordered:
        findings.append({"level": "warn", "code": "reordered", "message": "matched rules change relative order; first-match evaluation may change"})
    return {
        "tool": "ruleset_guard", "version": 1, "phase": proposed_phase or current_phase,
        "current_rules": len(current), "proposed_rules": len(proposed),
        "added": added, "removed": removed, "modified": modified, "reordered": reordered,
        "findings": findings, "safe_to_apply": not any(f["level"] == "error" for f in findings),
    }


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    parser.add_argument("--current", required=True, type=Path)
    parser.add_argument("--proposed", required=True, type=Path)
    parser.add_argument("--allow-removal", action="store_true", help="removals are intended")
    args = parser.parse_args()
    try:
        current_phase, current = load_ruleset(args.current)
        proposed_phase, proposed = load_ruleset(args.proposed)
    except (OSError, ValueError) as exc:
        message = type(exc).__name__ if isinstance(exc, json.JSONDecodeError) or not isinstance(exc, ValueError) else str(exc)
        print(json.dumps({"tool": "ruleset_guard", "error": message}))
        return 2
    result = compare(current, proposed, current_phase, proposed_phase, args.allow_removal)
    print(json.dumps(result, indent=2))
    return 0 if result["safe_to_apply"] else 1


if __name__ == "__main__":
    sys.exit(main())
