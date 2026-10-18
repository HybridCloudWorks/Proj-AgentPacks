#!/usr/bin/env python3
"""Report agent, skill, instruction and prompt names that appear in more than one pack.

Every pack installs into the same user-profile folders (for example ~/.claude/agents, ~/.claude/skills,
~/.claude/rules and ~/.claude/commands), so two packs that ship a primitive with the same name overwrite each other
on install. When every copy is byte-identical (a shared primitive kept in sync from shared-primitives/), the
overwrite is harmless: those names are reported as shared, not as collisions.

Usage: python tooling/check_collisions.py [--strict] [--github]
  --strict  exit 1 when any collision exists
  --github  also print GitHub Actions warning annotations
"""
from __future__ import annotations

import argparse
import hashlib
from collections import defaultdict
from pathlib import Path

REPO = Path(__file__).resolve().parents[1]


def digest(path: Path) -> str:
    """Content hash of an agent file or a whole skill folder, ignoring caches and line-ending differences."""
    h = hashlib.sha256()
    items = [path] if path.is_file() else sorted(p for p in path.rglob("*") if p.is_file()
                                                 and "__pycache__" not in p.parts and p.suffix != ".pyc")
    for item in items:
        h.update((item.relative_to(path).as_posix() if item != path else "").encode() + b"\0")
        h.update(item.read_bytes().replace(b"\r\n", b"\n") + b"\0")
    return h.hexdigest()


def inventory(repo: Path = REPO) -> dict[str, dict[str, dict[str, str]]]:
    """kind -> name -> pack -> content hash, for every agent, skill, instruction and prompt in every pack."""
    found: dict[str, dict[str, dict[str, str]]] = {kind: defaultdict(dict) for kind in ("agents", "skills", "instructions", "prompts")}
    for pack in sorted(p for p in repo.iterdir() if p.is_dir() and (p / "apm.yml").is_file()):
        for kind, suffix in (("agents", ".agent.md"), ("instructions", ".instructions.md"), ("prompts", ".prompt.md")):
            for item in (pack / ".apm" / kind).glob("*" + suffix):
                found[kind][item.name[: -len(suffix)]][pack.name] = digest(item)
        skills_dir = pack / ".apm" / "skills"
        for skill in (p for p in skills_dir.iterdir() if p.is_dir()) if skills_dir.is_dir() else []:
            found["skills"][skill.name][pack.name] = digest(skill)
    return found


def collisions(repo: Path = REPO) -> dict[str, dict[str, list[str]]]:
    """Names shipped by more than one pack with different content: a later install silently replaces the other."""
    return {kind: {name: sorted(packs) for name, packs in sorted(names.items()) if len(packs) > 1 and len(set(packs.values())) > 1}
            for kind, names in inventory(repo).items()}


def shared(repo: Path = REPO) -> dict[str, dict[str, list[str]]]:
    """Names shipped by more than one pack with identical content: harmless on install."""
    return {kind: {name: sorted(packs) for name, packs in sorted(names.items()) if len(packs) > 1 and len(set(packs.values())) == 1}
            for kind, names in inventory(repo).items()}


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    parser.add_argument("--strict", action="store_true")
    parser.add_argument("--github", action="store_true")
    args = parser.parse_args()
    found = collisions()
    total = sum(len(v) for v in found.values())
    for kind, names in found.items():
        for name, packs in names.items():
            line = f"{kind[:-1]} '{name}' is shipped by {len(packs)} packs: {', '.join(packs)}"
            print(line)
            if args.github:
                print(f"::warning title=Install collision::{line}")
    same = shared()
    for kind, names in same.items():
        for name, packs in names.items():
            print(f"{kind[:-1]} '{name}' is shared: {len(packs)} packs ship identical copies ({', '.join(packs)})")
    print(f"{total} collision(s): " + ", ".join(f"{len(found[k])} {k[:-1]}" for k in found) + "; "
          f"{sum(len(v) for v in same.values())} shared name(s) with identical copies")
    return 1 if (args.strict and total) else 0


if __name__ == "__main__":
    raise SystemExit(main())
