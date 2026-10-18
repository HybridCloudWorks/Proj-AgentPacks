#!/usr/bin/env python3
"""Read-only bounded discussion query wrapper."""
from __future__ import annotations
import argparse
import json
import subprocess

def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--repo")
    parser.add_argument("--limit", type=int, default=30)
    args = parser.parse_args()
    if not 1 <= args.limit <= 100:
        parser.error("limit must be 1..100")
    command = ["gh", "discussion", "list", "--limit", str(args.limit), "--json", "number,title,author,createdAt,updatedAt,category,labels,answer,url"]
    if args.repo:
        command += ["--repo", args.repo]
    result = subprocess.run(command, capture_output=True, text=True, check=False)
    if result.returncode:
        print(result.stderr, end="")
        return result.returncode
    data = json.loads(result.stdout)
    print(json.dumps({"items": data, "item_count": len(data)}, indent=2))
    return 0

if __name__ == "__main__":
    raise SystemExit(main())
