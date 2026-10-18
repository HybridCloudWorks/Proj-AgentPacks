#!/usr/bin/env python3
"""Copy each shared skill into every pack that ships it, or check that every copy is identical.

A shared skill ships under the same name in several packs, so all packs install the same folder into the same
user-profile location and a later install overwrites an earlier one harmlessly. The canonical folder lives in
shared-skills/<skill>/, and shared-skills/consumers.json lists the packs that ship it. Edit the canonical folder,
then run this script; never edit a pack's copy.

Usage: python tooling/sync_shared_skills.py [--check]
  --check  write nothing; exit 1 when a copy differs from the canonical folder, a listed pack is missing,
           or a pack that is not listed ships a skill with a shared skill's name
After copying, the script regenerates tests/skill-coverage.yml for every pack it changed.
"""
from __future__ import annotations

import argparse
import json
import shutil
import sys
from pathlib import Path

REPO = Path(__file__).resolve().parents[1]
SHARED = "shared-skills"
IGNORED = {"__pycache__", ".pytest_cache"}


def files(folder: Path) -> dict[str, bytes]:
    """Relative path to content for every file in a skill folder, ignoring caches and line-ending differences."""
    if not folder.is_dir():
        return {}
    return {p.relative_to(folder).as_posix(): p.read_bytes().replace(b"\r\n", b"\n") for p in sorted(folder.rglob("*"))
            if p.is_file() and not (IGNORED & set(p.relative_to(folder).parts)) and p.suffix != ".pyc"}


def manifest(repo: Path = REPO) -> dict[str, list[str]]:
    return json.loads((repo / SHARED / "consumers.json").read_text(encoding="utf-8"))["skills"]


def drift(repo: Path = REPO) -> list[str]:
    """Every way the packs disagree with shared-skills/; empty when all copies are current."""
    problems = []
    consumers = manifest(repo)
    packs = sorted(p.name for p in repo.iterdir() if p.is_dir() and (p / "apm.yml").is_file())
    for skill, listed in sorted(consumers.items()):
        canonical = files(repo / SHARED / skill)
        if "SKILL.md" not in canonical:
            problems.append(f"{SHARED}/{skill}/SKILL.md is missing")
            continue
        for pack in listed:
            if pack not in packs:
                problems.append(f"{pack} is listed for {skill} but is not a pack in this repository")
                continue
            copy = files(repo / pack / ".apm" / "skills" / skill)
            if copy != canonical:
                changed = sorted(k for k in set(copy) | set(canonical) if copy.get(k) != canonical.get(k))
                problems.append(f"{pack}/.apm/skills/{skill} differs from {SHARED}/{skill}: {', '.join(changed[:6])}")
        for pack in packs:
            if pack not in listed and (repo / pack / ".apm" / "skills" / skill).is_dir():
                problems.append(f"{pack} ships a skill named {skill} but is not listed for it in {SHARED}/consumers.json")
    return problems


def sync(repo: Path = REPO) -> list[str]:
    """Copy each canonical skill into its listed packs; return the packs that changed."""
    changed = set()
    for skill, listed in sorted(manifest(repo).items()):
        source = repo / SHARED / skill
        for pack in listed:
            dest = repo / pack / ".apm" / "skills" / skill
            if not (repo / pack / "apm.yml").is_file() or files(dest) == files(source):
                continue
            if dest.exists():
                shutil.rmtree(dest)
            shutil.copytree(source, dest, ignore=shutil.ignore_patterns(*IGNORED, "*.pyc"))
            changed.add(pack)
    if changed:
        sys.path.insert(0, str(Path(__file__).resolve().parent))
        import skill_coverage  # noqa: E402
        for pack in sorted(changed):
            (repo / pack / "tests" / "skill-coverage.yml").write_text(skill_coverage.render(skill_coverage.build(repo / pack)), encoding="utf-8")
    return sorted(changed)


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    parser.add_argument("--check", action="store_true")
    args = parser.parse_args()
    if args.check:
        problems = drift()
        for line in problems:
            print(line)
        total = sum(len(v) for v in manifest().values())
        print(f"{len(manifest())} shared skills, {total} copies: {'all identical' if not problems else f'{len(problems)} problem(s)'}")
        return 1 if problems else 0
    changed = sync()
    print(f"updated {len(changed)} pack(s): {', '.join(changed) or 'none'}")
    problems = drift()
    for line in problems:
        print(line)
    return 1 if problems else 0


if __name__ == "__main__":
    raise SystemExit(main())
