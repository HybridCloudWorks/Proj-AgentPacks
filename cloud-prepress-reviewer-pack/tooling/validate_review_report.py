#!/usr/bin/env python3
"""Validate the Cloud Pre-Press Reviewer report contract without changing it."""
from __future__ import annotations

import argparse
import re
from pathlib import Path

RECOMMENDATIONS = {"READY_FOR_PR", "READY_FOR_DEPLOYMENT_REVIEW", "CHANGES_REQUIRED", "BLOCKED_ON_HUMAN_DECISION", "NOT_VERIFIED"}
REQUIRED = ("Scope", "Evidence", "Findings", "Recommendation", "Engineer Handoff")


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("report", type=Path)
    args = parser.parse_args()
    errors: list[str] = []
    try:
        text = args.report.read_text(encoding="utf-8")
    except OSError as exc:
        print(f"FAIL: {exc}")
        return 1
    for heading in REQUIRED:
        if not re.search(rf"^#+\s+{re.escape(heading)}\b", text, re.I | re.M):
            errors.append(f"missing required section: {heading}")
    recommendations = [value for value in RECOMMENDATIONS if value in text]
    if len(recommendations) != 1:
        errors.append(f"expected exactly one recommendation, found: {recommendations}")
    if re.search(r"(?i)(password|api[_ -]?key|client[_ -]?secret|private[_ -]?key|connectionstring)\s*[:=]\s*[^<\[\n]{8,}", text):
        errors.append("possible unredacted secret-like value")
    finding_ids = re.findall(r"\bF\d+\b", text)
    if len(finding_ids) != len(set(finding_ids)):
        errors.append("duplicate finding ID")
    if errors:
        for error in errors:
            print(f"FAIL: {error}")
        return 1
    print(f"PASS: {args.report}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
