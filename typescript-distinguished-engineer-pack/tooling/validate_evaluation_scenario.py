#!/usr/bin/env python3
"""Validate required keys in an evaluation scenario without requiring PyYAML."""
from __future__ import annotations

import argparse
from pathlib import Path

REQUIRED = ["id:", "title:", "goal:", "expected:", "budgets:", "scoring:"]

def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("scenario", type=Path)
    args = parser.parse_args()
    text = args.scenario.read_text(encoding="utf-8")
    missing = [key for key in REQUIRED if key not in text]
    if missing:
        print("missing scenario keys: " + ", ".join(missing))
        return 2
    print("evaluation scenario shape is valid")
    return 0

if __name__ == "__main__":
    raise SystemExit(main())
