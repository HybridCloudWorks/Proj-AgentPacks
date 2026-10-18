#!/usr/bin/env python3
"""Validate the minimum evidence contract for an engineering completion report."""
from __future__ import annotations

import argparse
import re
from pathlib import Path

REQUIRED = ["acceptance", "files", "checks", "security", "unverified", "risk"]
STATUSES = {"COMPLETE_VERIFIED", "IMPLEMENTATION_PREPARED_NOT_VERIFIED", "CHANGES_REQUIRED", "BLOCKED_ON_HUMAN_DECISION", "NOT_VERIFIED"}

def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("report", type=Path)
    args = parser.parse_args()
    text = args.report.read_text(encoding="utf-8")
    lower = text.lower()
    missing = [item for item in REQUIRED if item not in lower]
    statuses = {match for match in STATUSES if match in text}
    secret_like = bool(re.search(r"(?i)(api[_-]?key|secret|password|token)\s*[:=]\s*['\"]?[^<>{}\s]+", text))
    if missing:
        print("missing report concepts: " + ", ".join(missing))
        return 2
    if not statuses:
        print("no supported completion status found")
        return 2
    if secret_like:
        print("possible secret-like value found; inspect and redact")
        return 2
    print(f"valid engineering report; statuses={','.join(sorted(statuses))}")
    return 0

if __name__ == "__main__":
    raise SystemExit(main())
