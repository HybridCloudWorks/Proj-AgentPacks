#!/usr/bin/env python3
"""Create a read-only inventory for a pre-press review."""
from __future__ import annotations

import argparse
import json
import subprocess
from pathlib import Path


def git(root: Path, *args: str) -> str:
    result = subprocess.run(["git", "-C", str(root), *args], capture_output=True, text=True)
    if result.returncode != 0:
        return ""
    return result.stdout


def classify(path: str) -> list[str]:
    lower = path.lower().replace("\\", "/")
    labels: list[str] = []
    if any(token in lower for token in (".tf", "terraform", ".bicep", "arm", "azure.yaml", "policy")):
        labels.append("infrastructure")
    if any(token in lower for token in ("workflow", ".github", "pipeline", "dockerfile", "lock")):
        labels.append("delivery-or-supply-chain")
    if any(token in lower for token in ("secret", ".env", "credential", "key", "certificate")):
        labels.append("sensitive-or-identity")
    if any(token in lower for token in ("test", "spec", "fixture")):
        labels.append("tests")
    if not labels:
        labels.append("application-or-documentation")
    return labels


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("root", nargs="?", type=Path, default=Path.cwd())
    parser.add_argument("--output", type=Path)
    args = parser.parse_args()
    root = args.root.resolve()
    status = git(root, "status", "--short").splitlines()
    names = git(root, "diff", "--name-only", "HEAD").splitlines()
    if not names:
        names = [line[3:] for line in status if len(line) > 3]
    changed = [{"path": path, "classifications": classify(path)} for path in sorted(set(names))]
    payload = {
        "repository": str(root),
        "status_entries": status,
        "changed_files": changed,
        "risk_flags": sorted({label for item in changed for label in item["classifications"] if label != "application-or-documentation"}),
        "available_tools": {name: bool(__import__("shutil").which(name)) for name in ("git", "az", "azd", "terraform", "bicep", "docker")},
        "mutation_performed": False,
    }
    text = json.dumps(payload, indent=2) + "\n"
    if args.output:
        args.output.write_text(text, encoding="utf-8")
    print(text, end="")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
