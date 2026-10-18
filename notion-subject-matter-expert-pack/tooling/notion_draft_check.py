"""Pre-publication check for Notion drafts and for Notion write tool calls.

Reads text and reports problems by line and check name; it never echoes matched content, never
executes anything and never contacts Notion. It is a safety net, not an access control.

File mode:  python tooling/notion_draft_check.py DRAFT.md [--audience internal|external] [--kind KIND]
            Exit 0 when clean, 1 when an error was found, 2 when the file cannot be read.
Hook mode:  python tooling/notion_draft_check.py --hook  (tool-call JSON on stdin)
            Scans the tool input for credentials only. Exit 0 to allow, 2 to block with a reason
            on stderr, 1 for unreadable input (reported, not blocked).
"""
from __future__ import annotations

import argparse
import json
import re
import sys
from pathlib import Path
from typing import Any

MAX_FILE_BYTES = 2_000_000
MAX_HOOK_BYTES = 2_000_000
MAX_DEPTH = 32

SECRET_PATTERNS = [
    ("notion-token", re.compile(r"\b(?:secret|ntn)_[A-Za-z0-9]{30,}")),
    ("private-key", re.compile(r"-----BEGIN [A-Z ]*PRIVATE KEY-----")),
    ("aws-access-key", re.compile(r"\bAKIA[0-9A-Z]{16}\b")),
    ("github-token", re.compile(r"\bgh[pousr]_[A-Za-z0-9]{36,}")),
    ("slack-token", re.compile(r"\bxox[abprs]-[A-Za-z0-9-]{10,}")),
    ("bearer-token", re.compile(r"(?i)\bbearer\s+[A-Za-z0-9._~+/-]{24,}")),
]
INTERNAL_MARKERS = re.compile(
    r"(?i)\binternal[- ](?:use[- ])?only\b|\bfor (?:the )?team only\b|\bdo not (?:share|forward)\b"
    r"|\bconfidential\b|\bpre-?read\b|^\W*internal\b")
PLACEHOLDERS = re.compile(
    r"(?i)\[(?:todo|tbd|fixme|placeholder|date|name|owner|link|url|insert[^\]\n]*)\]|\{\{[^{}\n]+\}\}|\blorem ipsum\b")
MENTION = re.compile(r"<mention-(page|database|user)\b([^>]*)>")
URL_ATTR = re.compile(r"""\burl\s*=\s*(["'])(.*?)\1""")
HEADING = re.compile(r"^\s{0,3}#{1,6}\s+(.+?)\s*#*\s*$")
LINK = re.compile(r"https?://\S+")

# Each inner tuple lists acceptable heading keywords for one required section.
REQUIRED_SECTIONS: dict[str, list[tuple[str, ...]]] = {
    "research": [("sources",)],
    "decision": [("context",), ("decision",), ("options", "alternatives"), ("consequences",)],
    "agenda": [("objective",), ("agenda",), ("action items",)],
    "howto": [("before you start", "prerequisites"), ("steps",)],
    "plan": [("phases",), ("success criteria", "acceptance criteria")],
    "task": [("acceptance criteria",)],
    "preread": [],
    "any": [],
}


def _finding(line: int, check: str) -> dict[str, Any]:
    return {"line": line, "check": check}


def secret_findings(text: str) -> list[dict[str, Any]]:
    found = []
    for number, line in enumerate(text.splitlines(), 1):
        for name, pattern in SECRET_PATTERNS:
            if pattern.search(line):
                found.append(_finding(number, "secret:" + name))
    return found


def scan_text(text: str, audience: str = "internal", kind: str = "any") -> dict[str, list[dict[str, Any]]]:
    errors = secret_findings(text)
    warnings: list[dict[str, Any]] = []
    lines = text.splitlines()
    headings = []
    in_code = False
    for number, line in enumerate(lines, 1):
        if line.lstrip().startswith("```"):
            in_code = not in_code
            continue
        if in_code:
            # Code blocks may legitimately hold template syntax; credentials are still caught above.
            continue
        if PLACEHOLDERS.search(line):
            errors.append(_finding(number, "unfilled-placeholder"))
        for match in MENTION.finditer(line):
            url = URL_ATTR.search(match.group(2))
            value = url.group(2).strip() if url else ""
            if not value.startswith(("https://", "http://")):
                errors.append(_finding(number, f"mention-{match.group(1)}-without-url"))
            elif match.group(1) == "user" and audience == "external":
                warnings.append(_finding(number, "person-mention-in-external-draft"))
        if audience == "external" and INTERNAL_MARKERS.search(line):
            errors.append(_finding(number, "internal-marker-in-external-draft"))
        heading = HEADING.match(line)
        if heading:
            headings.append(heading.group(1).lower())

    for keywords in REQUIRED_SECTIONS[kind]:
        if not any(keyword in heading for heading in headings for keyword in keywords):
            errors.append(_finding(0, "missing-section:" + keywords[0]))
    if kind == "research" and not (MENTION.search(text) or LINK.search(text)):
        errors.append(_finding(0, "research-without-citations"))
    if kind == "preread":
        opening = "\n".join(lines[:5])
        if not re.search(r"(?i)\binternal\b", opening):
            errors.append(_finding(0, "preread-not-marked-internal"))
        if audience == "external":
            errors.append(_finding(0, "preread-for-external-audience"))
    return {"errors": errors, "warnings": warnings}


def check_file(path: Path, audience: str, kind: str) -> dict[str, Any]:
    if path.stat().st_size > MAX_FILE_BYTES:
        raise ValueError("draft exceeds the scan bound")
    result = scan_text(path.read_text(encoding="utf-8-sig"), audience, kind)
    return {"file": path.name, "audience": audience, "kind": kind, **result}


def _strings(value: Any, depth: int = 0) -> list[str]:
    if depth > MAX_DEPTH:
        return []
    if isinstance(value, str):
        # Some hosts pass tool arguments as a JSON string; scan the decoded form too.
        out = [value]
        if value[:1] in "{[":
            try:
                out += _strings(json.loads(value), depth + 1)
            except ValueError:
                pass
        return out
    if isinstance(value, dict):
        return [s for item in value.values() for s in _strings(item, depth + 1)]
    if isinstance(value, list):
        return [s for item in value for s in _strings(item, depth + 1)]
    return []


def hook(raw: bytes) -> tuple[int, str]:
    """Return (exit code, stderr message) for one tool-call payload."""
    if len(raw) > MAX_HOOK_BYTES:
        return 2, "Blocked Notion write: the tool input exceeds the scan bound; split the content into smaller writes."
    try:
        payload = json.loads(raw.decode("utf-8"))
    except (UnicodeDecodeError, ValueError):
        return 1, "notion_draft_check: hook input was not valid JSON; nothing was scanned."
    if not isinstance(payload, dict):
        return 1, "notion_draft_check: hook input was not a JSON object; nothing was scanned."
    target = next((payload[k] for k in ("tool_input", "toolArgs", "arguments") if k in payload), payload)
    kinds = sorted({f["check"].split(":", 1)[1] for s in _strings(target) for f in secret_findings(s)})
    if kinds:
        return 2, ("Blocked Notion write: the content contains what looks like a credential (" + ", ".join(kinds)
                   + "). Remove it, use a reference to the secret store instead, and retry.")
    return 0, ""


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description="Pre-publication check for Notion drafts.")
    parser.add_argument("draft", nargs="?", type=Path)
    parser.add_argument("--audience", choices=["internal", "external"], default="internal")
    parser.add_argument("--kind", choices=sorted(REQUIRED_SECTIONS), default="any")
    parser.add_argument("--hook", action="store_true", help="read a tool-call payload on stdin")
    args = parser.parse_args(argv)
    if args.hook:
        code, message = hook(sys.stdin.buffer.read(MAX_HOOK_BYTES + 1))
        if message:
            print(message, file=sys.stderr)
        return code
    if args.draft is None:
        parser.error("a draft file is required unless --hook is given")
    try:
        result = check_file(args.draft, args.audience, args.kind)
    except (OSError, UnicodeDecodeError, ValueError):
        print(json.dumps({"error": "draft unreadable, not UTF-8 or too large"}))
        return 2
    print(json.dumps(result, indent=2))
    return int(bool(result["errors"]))


if __name__ == "__main__":
    raise SystemExit(main())
