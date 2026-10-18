#!/usr/bin/env python3
"""Decide which packs and runner operating systems a validation run covers. Writes GitHub Actions outputs.

  push / pull_request : packs changed since the base commit, on Linux, with the pinned APM.
                        A change under tooling/ or .github/ revalidates every pack.
  schedule / dispatch : every pack, on Linux, Windows and macOS, with the latest APM.

Usage: python tooling/ci_plan.py --event <github.event_name> [--base <sha>]
"""
from __future__ import annotations

import argparse
import json
import os
import subprocess
from pathlib import Path

REPO = Path(__file__).resolve().parents[1]
ALL_OS = ["ubuntu-latest", "windows-latest", "macos-latest"]


def all_packs() -> list[str]:
    return sorted(p.name for p in REPO.iterdir() if p.is_dir() and (p / "apm.yml").is_file())


def changed_paths(base: str) -> list[str] | None:
    if not base or set(base) == {"0"}:
        return None
    proc = subprocess.run(["git", "diff", "--name-only", f"{base}...HEAD"], cwd=REPO, capture_output=True, text=True)
    if proc.returncode != 0:
        proc = subprocess.run(["git", "diff", "--name-only", base, "HEAD"], cwd=REPO, capture_output=True, text=True)
    return proc.stdout.split() if proc.returncode == 0 else None


def plan(event: str, base: str, scope: str = "all") -> dict[str, object]:
    packs = all_packs()
    if event == "schedule" or (event == "workflow_dispatch" and scope != "changed"):
        return {"packs": packs, "os": ALL_OS, "apm": "latest"}
    if event == "workflow_dispatch":
        base = "origin/main"
    changed = changed_paths(base)
    if changed is None or any(p.startswith(("tooling/", ".github/")) for p in changed):
        selected = packs
    else:
        selected = sorted({p.split("/", 1)[0] for p in changed} & set(packs))
    return {"packs": selected, "os": ["ubuntu-latest"], "apm": "pinned"}


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    parser.add_argument("--event", required=True)
    parser.add_argument("--base", default="")
    parser.add_argument("--scope", default="all", choices=["all", "changed"])
    args = parser.parse_args()
    result = plan(args.event, args.base, args.scope)
    lines = [f"packs={json.dumps(result['packs'])}", f"os={json.dumps(result['os'])}", f"apm={result['apm']}",
             f"any={'true' if result['packs'] else 'false'}"]
    if os.environ.get("GITHUB_OUTPUT"):
        with open(os.environ["GITHUB_OUTPUT"], "a", encoding="utf-8") as handle:
            handle.write("\n".join(lines) + "\n")
    print("\n".join(lines))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
