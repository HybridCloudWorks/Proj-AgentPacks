#!/usr/bin/env python3
"""Copy each shared primitive into every pack that ships it, or check that every copy is identical.

A shared primitive (skill, agent, instruction or prompt) ships under the same name in several packs. All of those
packs install it into the same user-profile location, so a later install overwrites an earlier one harmlessly only
when every copy is identical. The canonical copies live in shared-primitives/, laid out like a pack's .apm/ folder:

  shared-primitives/skills/<name>/                      -> <pack>/.apm/skills/<name>/
  shared-primitives/agents/<name>.agent.md              -> <pack>/.apm/agents/<name>.agent.md
  shared-primitives/instructions/<name>.instructions.md -> <pack>/.apm/instructions/<name>.instructions.md
  shared-primitives/prompts/<name>.prompt.md            -> <pack>/.apm/prompts/<name>.prompt.md

shared-primitives/consumers.json lists, per kind, the packs that ship each name. Edit the canonical copy, then run
this script; never edit a pack's copy.

Usage: python tooling/sync_shared.py [--check]
  --check  write nothing; exit 1 when a copy differs from its canonical copy, a listed pack is missing, or a pack
           that is not listed ships a primitive with a shared name
After copying, the script regenerates tests/skill-coverage.yml for every pack whose skills changed.
"""
from __future__ import annotations

import argparse
import json
import shutil
import sys
from pathlib import Path

REPO = Path(__file__).resolve().parents[1]
SHARED = "shared-primitives"
IGNORED = {"__pycache__", ".pytest_cache"}
# kind -> (folder under .apm and under shared-primitives, file suffix; None means the primitive is a folder)
KINDS = {"skills": ("skills", None), "agents": ("agents", ".agent.md"),
         "instructions": ("instructions", ".instructions.md"), "prompts": ("prompts", ".prompt.md")}


def files(path: Path) -> dict[str, bytes]:
    """Relative path to content for a primitive file or folder, ignoring caches and line-ending differences."""
    if path.is_file():
        return {path.name: path.read_bytes().replace(b"\r\n", b"\n")}
    if not path.is_dir():
        return {}
    return {p.relative_to(path).as_posix(): p.read_bytes().replace(b"\r\n", b"\n") for p in sorted(path.rglob("*"))
            if p.is_file() and not (IGNORED & set(p.relative_to(path).parts)) and p.suffix != ".pyc"}


def locate(root: Path, kind: str, name: str) -> Path:
    folder, suffix = KINDS[kind]
    return root / folder / (name if suffix is None else name + suffix)


def manifest(repo: Path = REPO) -> dict[str, dict[str, list[str]]]:
    data = json.loads((repo / SHARED / "consumers.json").read_text(encoding="utf-8"))
    unknown = set(data) - set(KINDS) - {"about"}
    if unknown:
        raise SystemExit(f"{SHARED}/consumers.json has unknown sections: {sorted(unknown)}")
    return {kind: data.get(kind, {}) for kind in KINDS}


def packs_in(repo: Path) -> list[str]:
    return sorted(p.name for p in repo.iterdir() if p.is_dir() and (p / "apm.yml").is_file())


def drift(repo: Path = REPO) -> list[str]:
    """Every way the packs disagree with shared-primitives/; empty when all copies are current."""
    problems = []
    packs = packs_in(repo)
    for kind, names in manifest(repo).items():
        for name, listed in sorted(names.items()):
            canonical_path = locate(repo / SHARED, kind, name)
            canonical = files(canonical_path)
            if not canonical or (kind == "skills" and "SKILL.md" not in canonical):
                problems.append(f"{canonical_path.relative_to(repo).as_posix()} is missing")
                continue
            for pack in listed:
                if pack not in packs:
                    problems.append(f"{pack} is listed for {kind} {name} but is not a pack in this repository")
                    continue
                copy_path = locate(repo / pack / ".apm", kind, name)
                copy = files(copy_path)
                if copy != canonical:
                    changed = sorted(k for k in set(copy) | set(canonical) if copy.get(k) != canonical.get(k))
                    problems.append(f"{copy_path.relative_to(repo).as_posix()} differs from the shared copy: {', '.join(changed[:6])}")
            for pack in packs:
                if pack not in listed and locate(repo / pack / ".apm", kind, name).exists():
                    problems.append(f"{pack} ships {kind[:-1]} {name} but is not listed for it in {SHARED}/consumers.json")
    return problems


def sync(repo: Path = REPO) -> list[str]:
    """Copy each canonical primitive into its listed packs; return the packs that changed."""
    changed, skills_changed = set(), set()
    for kind, names in manifest(repo).items():
        for name, listed in sorted(names.items()):
            source = locate(repo / SHARED, kind, name)
            for pack in listed:
                if not (repo / pack / "apm.yml").is_file():
                    continue
                dest = locate(repo / pack / ".apm", kind, name)
                if files(dest) == files(source):
                    continue
                if dest.is_dir():
                    shutil.rmtree(dest)
                dest.parent.mkdir(parents=True, exist_ok=True)
                if source.is_dir():
                    shutil.copytree(source, dest, ignore=shutil.ignore_patterns(*IGNORED, "*.pyc"))
                    skills_changed.add(pack)
                else:
                    shutil.copyfile(source, dest)
                changed.add(pack)
    if skills_changed:
        sys.path.insert(0, str(Path(__file__).resolve().parent))
        import skill_coverage  # noqa: E402
        for pack in sorted(skills_changed):
            (repo / pack / "tests" / "skill-coverage.yml").write_text(skill_coverage.render(skill_coverage.build(repo / pack)), encoding="utf-8")
    return sorted(changed)


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    parser.add_argument("--check", action="store_true")
    args = parser.parse_args()
    if not args.check:
        changed = sync()
        print(f"updated {len(changed)} pack(s): {', '.join(changed) or 'none'}")
    problems = drift()
    for line in problems:
        print(line)
    counts = {kind: (len(names), sum(len(v) for v in names.values())) for kind, names in manifest().items()}
    summary = ", ".join(f"{n} {kind} in {c} copies" for kind, (n, c) in counts.items() if n)
    print(f"shared: {summary}; {'all identical' if not problems else f'{len(problems)} problem(s)'}")
    return 1 if problems else 0


if __name__ == "__main__":
    raise SystemExit(main())
