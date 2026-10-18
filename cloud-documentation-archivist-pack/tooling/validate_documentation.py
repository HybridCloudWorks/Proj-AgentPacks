#!/usr/bin/env python3
"""Validate a Markdown document for safe structure and documentation metadata."""
from __future__ import annotations
import argparse
import re
import sys
from pathlib import Path

SECRET_PATTERNS = [r"ghp_[A-Za-z0-9]{20,}", r"github_pat_[A-Za-z0-9_]{20,}", r"-----BEGIN (?:RSA|OPENSSH|EC) PRIVATE KEY-----", r"(?i)(password|secret|api[_ -]?key|token)\s*[:=]\s*[A-Za-z0-9+/]{16,}"]

def validate(path: Path, allow_template: bool = False) -> list[str]:
    text = path.read_text(encoding="utf-8")
    errors = []
    lines = text.splitlines()
    if path.suffix.lower() in {".md", ".mdx"} and not text.strip():
        errors.append("document is empty")
    if text.startswith("---\n") and "\n---\n" not in text[4:]:
        errors.append("frontmatter is not closed")
    levels = [len(m.group(1)) for line in lines if (m := re.match(r"^(#{1,6})\s+", line))]
    if levels and levels[0] != 1:
        errors.append("first heading is not level 1")
    if any(b > a + 1 for a, b in zip(levels, levels[1:])):
        errors.append("heading levels skip a depth")
    if not allow_template and re.search(r"\[(?:Your |What |Describe |Replace |Optional |Person |One sentence|Short )[^\]]*\]", text, re.I):
        errors.append("unreplaced template placeholder")
    for pattern in SECRET_PATTERNS:
        if re.search(pattern, text):
            errors.append("secret-like value detected")
            break
    if re.search(r"(?i)\b(click here|lorem ipsum)\b", text):
        errors.append("non-actionable or placeholder prose detected")
    return errors

def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("paths", nargs="+")
    parser.add_argument("--allow-template", action="store_true")
    args = parser.parse_args()
    failures = []
    for raw in args.paths:
        path = Path(raw)
        if not path.is_file():
            failures.append(f"missing: {path}")
            continue
        for error in validate(path, args.allow_template):
            failures.append(f"{path}: {error}")
    if failures:
        print("FAIL")
        print(chr(10).join(f"- {failure}" for failure in failures))
        return 1
    print("PASS")
    return 0

if __name__ == "__main__":
    raise SystemExit(main())
