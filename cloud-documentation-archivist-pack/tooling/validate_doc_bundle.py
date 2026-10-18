#!/usr/bin/env python3
"""Validate a directory of documentation files without publishing them."""
from __future__ import annotations
import argparse
import json
import subprocess
import sys
from pathlib import Path

def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("root")
    args = parser.parse_args()
    root = Path(args.root)
    paths = [str(p) for p in sorted(root.rglob("*.md")) if ".git" not in p.parts]
    result = subprocess.run([sys.executable, str(Path(__file__).with_name("validate_documentation.py")), "--allow-template", *paths], capture_output=True, text=True, check=False)
    payload = {"root": str(root.resolve()), "files": len(paths), "result": "PASS" if result.returncode == 0 else "FAIL", "external_write": False}
    print(json.dumps(payload, indent=2))
    if result.returncode:
        print(result.stdout, end="")
        print(result.stderr, end="", file=sys.stderr)
    return result.returncode

if __name__ == "__main__":
    raise SystemExit(main())
