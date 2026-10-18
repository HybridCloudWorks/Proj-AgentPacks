#!/usr/bin/env python3
"""Emit a bounded, read-only inventory for an existing engineering repository."""
from __future__ import annotations

import argparse
import json
import subprocess
from pathlib import Path

NAMES = {
    "package.json", "package-lock.json", "npm-shrinkwrap.json", "yarn.lock", "pnpm-lock.yaml",
    "tsconfig.json", "vite.config.ts", "next.config.js", "playwright.config.ts",
    "openapi.yaml", "openapi.yml", "dockerfile", "codeql-config.yml",
}
DIRECTORIES = {".github", ".claude", ".codex", ".gemini", ".agents", "src", "app", "apps", "packages", "tests", "test"}

def git(repo: Path, *args: str) -> str:
    try:
        return subprocess.check_output(["git", *args], cwd=repo, text=True, stderr=subprocess.STDOUT, timeout=10).strip()
    except (OSError, subprocess.SubprocessError) as exc:
        return f"unavailable: {exc}"

def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("repo", nargs="?", default=".")
    args = parser.parse_args()
    repo = Path(args.repo).resolve()
    files: list[str] = []
    for path in repo.rglob("*"):
        if not path.is_file() or any(part in {".git", "node_modules", "dist", "build", "coverage"} for part in path.parts):
            continue
        relative = path.relative_to(repo)
        if relative.name.lower() in {name.lower() for name in NAMES} or relative.parts[0] in DIRECTORIES or relative.suffix.lower() in {".md", ".yml", ".yaml"}:
            files.append(relative.as_posix())
    payload = {
        "repository": str(repo),
        "git_status": git(repo, "status", "--short"),
        "git_branch": git(repo, "branch", "--show-current"),
        "files": sorted(files)[:500],
        "truncated": len(files) > 500,
        "notes": ["Static inventory only; it does not prove runtime, cloud, authorization, or production state."],
    }
    print(json.dumps(payload, indent=2))
    return 0

if __name__ == "__main__":
    raise SystemExit(main())
