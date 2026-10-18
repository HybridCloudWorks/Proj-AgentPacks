#!/usr/bin/env python3
"""Generate or check <pack>/tests/skill-coverage.yml: one entry per canonical skill with its activation text.

The file is derived from each SKILL.md (name, description, and the first "Use when" or activation sentence),
so it always matches the skills that ship. The shared validator fails a pack whose file is missing or stale.

Usage: python tooling/skill_coverage.py <pack> [--check]
"""
from __future__ import annotations

import argparse
import json
import re
import sys
from pathlib import Path


def frontmatter(path: Path) -> tuple[dict[str, str], str]:
    text = path.read_text(encoding="utf-8", errors="replace")
    m = re.match(r"\A---\r?\n(.*?)\r?\n---\r?\n(.*)\Z", text, re.DOTALL)
    if not m:
        return {}, text
    fields: dict[str, str] = {}
    for line in m.group(1).splitlines():
        km = re.match(r"^([A-Za-z_][\w-]*):\s*(.*)$", line)
        if km:
            fields[km.group(1)] = km.group(2).strip().strip("\"'")
    return fields, m.group(2)


def activation(description: str, body: str) -> str:
    m = re.search(r"(Use (?:this )?(?:Skill |skill )?when[^.]*\.)", description) or re.search(r"(Use (?:this )?(?:Skill |skill )?when[^.]*\.)", body)
    if m:
        return m.group(1).strip()
    m = re.search(r"^##\s+(?:Activation|Purpose|When to use)[^\n]*\n+([^\n#]+)", body, re.M | re.I)
    if m:
        return m.group(1).strip()[:240]
    return description.split(". ")[0].strip()[:240]


def build(root: Path) -> dict[str, dict[str, str]]:
    out: dict[str, dict[str, str]] = {}
    for skill in sorted(p for p in (root / ".apm" / "skills").iterdir() if p.is_dir()):
        fm, body = frontmatter(skill / "SKILL.md") if (skill / "SKILL.md").is_file() else ({}, "")
        out[skill.name] = {"description": fm.get("description", ""), "activation": activation(fm.get("description", ""), body),
                           "source": f".apm/skills/{skill.name}/SKILL.md"}
    return out


def render(data: dict[str, dict[str, str]]) -> str:
    return json.dumps({"version": 1, "generated_from": ".apm/skills/*/SKILL.md", "skills": data}, indent=2) + "\n"


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    parser.add_argument("pack")
    parser.add_argument("--check", action="store_true", help="exit 1 if the file is missing or stale instead of writing it")
    args = parser.parse_args()
    root = Path(args.pack).resolve()
    target = root / "tests" / "skill-coverage.yml"
    expected = render(build(root))
    if args.check:
        current = target.read_text(encoding="utf-8") if target.is_file() else ""
        if current != expected:
            print(f"{root.name}: tests/skill-coverage.yml is {'missing' if not current else 'stale'}; run tooling/skill_coverage.py {root.name}")
            return 1
        print(f"{root.name}: tests/skill-coverage.yml is current")
        return 0
    target.parent.mkdir(exist_ok=True)
    target.write_text(expected, encoding="utf-8")
    print(f"{root.name}: wrote tests/skill-coverage.yml for {len(build(root))} skills")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
