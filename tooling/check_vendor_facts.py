#!/usr/bin/env python3
"""Check that every fact in a facts file is still stated on its official page.

Fetches each page once and looks for the fact's phrase in the page's plain text, or in its raw HTML when the fact
sets "raw": true (download file names, for example, appear only inside links). A missing phrase or an unreachable
page means the vendor changed or moved something, so whatever the facts back must be re-verified.

Usage: python tooling/check_vendor_facts.py --facts shared-primitives/diagram-facts.json [--markdown OUT]
Exit 1 when any fact could not be confirmed.
"""
from __future__ import annotations

import argparse
import gzip
import html
import json
import re
import sys
import urllib.error
import urllib.request
import zlib
from pathlib import Path


def normalize(text: str) -> str:
    text = re.sub(r"(?is)<(script|style|noscript)\b.*?</\1>", " ", text)
    text = re.sub(r"(?s)<[^>]+>", " ", text)
    text = html.unescape(text).replace("’", "'").replace("`", "").replace("*", "").replace("​", "")
    return re.sub(r"\s*/\s*", "/", " ".join(text.split()).lower())


def fetch(url: str) -> str:
    if not url.startswith("https://"):
        raise ValueError(f"only https URLs are fetched, not {url}")
    request = urllib.request.Request(url, headers={"User-Agent": "Mozilla/5.0 (compatible; agent-packs-facts/1.0)",  # noqa: S310
                                                   "Accept": "text/html,text/markdown,text/plain;q=0.9,*/*;q=0.8",
                                                   "Accept-Encoding": "gzip, deflate"})
    # Safe: only https URLs reach this point.
    with urllib.request.urlopen(request, timeout=60) as response:  # noqa: S310  # nosec B310
        body = response.read()
        # Some CDNs compress even when not asked; urllib never decompresses, so do it here.
        encoding = (response.headers.get("Content-Encoding") or "").lower()
        if encoding == "gzip" or body[:2] == b"\x1f\x8b":
            body = gzip.decompress(body)
        elif encoding == "deflate":
            body = zlib.decompress(body)
        return body.decode(response.headers.get_content_charset() or "utf-8", errors="replace")


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    parser.add_argument("--facts", required=True)
    parser.add_argument("--markdown", help="write a Markdown report of unconfirmed facts to this file")
    args = parser.parse_args()
    facts = json.loads(Path(args.facts).read_text(encoding="utf-8"))["facts"]
    pages: dict[str, str | Exception] = {}
    for url in sorted({f["url"] for f in facts}):
        try:
            pages[url] = fetch(url)
        except (urllib.error.URLError, TimeoutError, OSError, ValueError) as exc:
            pages[url] = exc
    problems = []
    for fact in facts:
        page = pages[fact["url"]]
        if isinstance(page, Exception):
            status = f"page unreachable ({page})"
        elif fact.get("raw"):
            status = "confirmed" if fact["phrase"].lower() in page.lower() else "phrase not found"
        else:
            status = "confirmed" if normalize(fact["phrase"]) in normalize(page) else "phrase not found"
        print(f"{status:<18} {fact['id']:<28} {fact['url']}")
        if status != "confirmed":
            problems.append((fact, status))
    print(f"{len(facts) - len(problems)} of {len(facts)} facts confirmed")
    if args.markdown and problems:
        lines = [f"These facts from `{args.facts}` could not be confirmed on their official pages. The vendor may have "
                 "published something new or moved the page; re-verify what the facts back.", "",
                 "| Source | Fact | Result | Page | Expected phrase |", "|---|---|---|---|---|"]
        lines += [f"| {f['client']} | {f['fact']} | {s} | {f['url']} | `{f['phrase']}` |" for f, s in problems]
        Path(args.markdown).write_text("\n".join(lines) + "\n", encoding="utf-8")
    return 1 if problems else 0


if __name__ == "__main__":
    sys.exit(main())
