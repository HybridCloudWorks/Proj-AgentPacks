#!/usr/bin/env python3
"""Validate a redacted GitHub review report contract."""
from __future__ import annotations

import argparse
import re
import sys
from pathlib import Path

RECOMMENDATIONS = {"READY_FOR_REVIEW", "READY_FOR_MERGE_REVIEW", "CHANGES_REQUIRED", "BLOCKED_ON_HUMAN_DECISION", "NOT_VERIFIED"}
SECTIONS = ("Scope", "Evidence", "Findings", "Skipped checks", "Recommendation")

def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("report")
    args = parser.parse_args()
    text = Path(args.report).read_text(encoding="utf-8")
    errors = [f"missing section: {section}" for section in SECTIONS if not re.search(rf"^#+\s+{re.escape(section)}\s*$", text, re.I | re.M)]
    if len(re.findall(r"\b(?:READY_FOR_REVIEW|READY_FOR_MERGE_REVIEW|CHANGES_REQUIRED|BLOCKED_ON_HUMAN_DECISION|NOT_VERIFIED)\b", text)) != 1:
        errors.append("report must contain exactly one recommendation")
    if re.search(r"(?i)(ghp_[A-Za-z0-9]{20,}|github_pat_[A-Za-z0-9_]{20,}|-----BEGIN (?:RSA|OPENSSH|EC) PRIVATE KEY-----|api[_ -]?key\s*[:=]\s*[A-Za-z0-9+/]{16,})", text):
        errors.append("secret-like value detected")
    ids = re.findall(r"\b(?:GH|FIND|SEC|ACT)-\d+\b", text)
    if len(ids) != len(set(ids)):
        errors.append("duplicate finding IDs")
    if errors:
        print("FAIL")
        for error in errors:
            print(f"- {error}")
        return 1
    print("PASS")
    return 0

if __name__ == "__main__":
    raise SystemExit(main())
