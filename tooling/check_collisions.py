#!/usr/bin/env python3
"""Report agent and skill names that appear in more than one pack.

Every pack installs into the same user-profile folders (for example ~/.claude/agents and ~/.claude/skills),
so two packs that ship an agent or skill with the same name overwrite each other on install.

Usage: python tooling/check_collisions.py [--strict] [--github]
  --strict  exit 1 when any collision exists
  --github  also print GitHub Actions warning annotations
"""
from __future__ import annotations

import argparse
from collections import defaultdict
from pathlib import Path

REPO = Path(__file__).resolve().parents[1]


def collisions(repo: Path = REPO) -> dict[str, dict[str, list[str]]]:
    agents: dict[str, list[str]] = defaultdict(list)
    skills: dict[str, list[str]] = defaultdict(list)
    for pack in sorted(p for p in repo.iterdir() if p.is_dir() and (p / "apm.yml").is_file()):
        for agent in (pack / ".apm" / "agents").glob("*.agent.md"):
            agents[agent.name[: -len(".agent.md")]].append(pack.name)
        skills_dir = pack / ".apm" / "skills"
        for skill in (p for p in skills_dir.iterdir() if p.is_dir()) if skills_dir.is_dir() else []:
            skills[skill.name].append(pack.name)
    return {"agents": {k: v for k, v in sorted(agents.items()) if len(v) > 1},
            "skills": {k: v for k, v in sorted(skills.items()) if len(v) > 1}}


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
    print(f"{total} collision(s): {len(found['agents'])} agent, {len(found['skills'])} skill")
    return 1 if (args.strict and total) else 0


if __name__ == "__main__":
    raise SystemExit(main())
