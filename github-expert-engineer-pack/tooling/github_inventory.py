#!/usr/bin/env python3
"""Create a bounded local GitHub review inventory without calling GitHub."""
from __future__ import annotations

import argparse
import json
import subprocess
from pathlib import Path

def run(*args: str) -> list[str]:
    result = subprocess.run(args, capture_output=True, text=True, check=False)
    return result.stdout.splitlines() if result.returncode == 0 else []

def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--root", default=".")
    parser.add_argument("--out", default="github-review-inventory.json")
    args = parser.parse_args()
    root = Path(args.root).resolve()
    files = []
    for path in sorted(root.rglob("*")):
        if not path.is_file() or ".git" in path.parts:
            continue
        rel = path.relative_to(root).as_posix()
        if rel.startswith((".github/", ".agents/", ".codex/", ".claude/", ".gemini/")) or path.name in {"CODEOWNERS", "README.md", "CONTRIBUTING.md", "SECURITY.md"}:
            files.append(rel)
    data = {"root": str(root), "git_status": run("git", "-C", str(root), "status", "--short"), "changed_files": run("git", "-C", str(root), "diff", "--name-status"), "github_files": files, "live_github_read": False}
    Path(args.out).write_text(json.dumps(data, indent=2) + chr(10), encoding="utf-8")
    print(json.dumps({"out": str(Path(args.out).resolve()), "github_files": len(files), "live_github_read": False}))
    return 0

if __name__ == "__main__":
    raise SystemExit(main())
