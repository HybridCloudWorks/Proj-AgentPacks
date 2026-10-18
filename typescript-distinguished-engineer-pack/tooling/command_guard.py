#!/usr/bin/env python3
"""Conservative command guard; it rejects common external or destructive mutations."""
from __future__ import annotations

import argparse
import re

PATTERNS = [
    r"\bgit\s+(push|merge|reset\s+--hard|clean\s+-f|branch\s+-D)\b",
    r"\b(gh\s+(pr\s+(merge|approve|close)|release\s+create|workflow\s+run))\b",
    r"\b(terraform|tofu)\s+apply\b",
    r"\b(az|aws|gcloud)\s+.*\b(deploy|apply|delete|create|update|set)\b",
    r"\b(npm|pnpm|yarn)\s+publish\b",
    r"\b(kubectl|helm)\s+.*\b(apply|delete|upgrade)\b",
    r"\b(curl|Invoke-WebRequest|iwr)\b.*\b(-d|--data|PUT|POST|DELETE)\b",
]

def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("command")
    args = parser.parse_args()
    hits = [pattern for pattern in PATTERNS if re.search(pattern, args.command, flags=re.IGNORECASE)]
    if hits:
        print("blocked by default command guard; approval is required")
        for hit in hits:
            print(f"matched: {hit}")
        return 3
    print("command is not in the default blocked set; still follow repository and host approval policy")
    return 0

if __name__ == "__main__":
    raise SystemExit(main())
