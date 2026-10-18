#!/usr/bin/env python3
"""Detect common GitHub and git mutations before a command is executed."""
from __future__ import annotations

import argparse
import re
import sys

PATTERNS = [
    r"\bgh\s+pr\s+(merge|close|reopen|review)", r"\bgh\s+workflow\s+(run|enable|disable)",
    r"\bgh\s+secret\s+(set|delete)", r"\bgh\s+variable\s+(set|delete)",
    r"\bgh\s+repo\s+(delete|archive|rename|edit)", r"\bgh\s+release\s+(create|delete|edit)",
    r"\bgh\s+api\b.*--method\s+(POST|PATCH|PUT|DELETE)", r"\bgit\s+push\b", r"\bgit\s+remote\s+set-url\b",
]

def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("command")
    parser.add_argument("--allow-mutation", action="store_true")
    args = parser.parse_args()
    hits = [pattern for pattern in PATTERNS if re.search(pattern, args.command, re.I)]
    result = {"mutation_detected": bool(hits), "allowed": bool(hits) and args.allow_mutation, "patterns": hits}
    print(result)
    if hits and not args.allow_mutation:
        print("BLOCKED: explicit human authorization is required before executing this command.", file=sys.stderr)
        return 2
    return 0

if __name__ == "__main__":
    raise SystemExit(main())
