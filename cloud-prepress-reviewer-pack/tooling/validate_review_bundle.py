#!/usr/bin/env python3
"""Validate a review handoff directory and invoke the report validator."""
from __future__ import annotations

import argparse
import subprocess
import sys
from pathlib import Path


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("path", type=Path)
    args = parser.parse_args()
    required = ["REVIEW.md"]
    missing = [name for name in required if not (args.path / name).is_file()]
    if missing:
        for name in missing:
            print(f"FAIL: missing {args.path / name}")
        return 1
    validator = Path(__file__).with_name("validate_review_report.py")
    result = subprocess.run([sys.executable, str(validator), str(args.path / "REVIEW.md")])
    return result.returncode


if __name__ == "__main__":
    raise SystemExit(main())
