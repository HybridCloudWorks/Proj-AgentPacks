#!/usr/bin/env python3
"""Detect Apple/Swift project files and locally available validation tools.

This script is read-only. It does not invoke Xcode, resolve dependencies, or modify
project files. It reports capabilities so a reviewer does not claim unavailable
build or test evidence.
"""

from __future__ import annotations

import argparse
import json
import os
import platform
import shutil
import sys
from pathlib import Path
from typing import Iterable

IGNORE_DIRS = {
    ".git", ".build", "DerivedData", "Pods", "Carthage", "node_modules",
    "apm_modules", "dist", ".swiftpm", ".idea",
}

FILE_MARKERS = {
    "swift_package": ("Package.swift",),
    "swift_lock": ("Package.resolved",),
    "cocoapods": ("Podfile", "Podfile.lock"),
    "carthage": ("Cartfile", "Cartfile.resolved"),
    "tuist": ("Project.swift", "Workspace.swift", "Tuist.swift"),
    "xcodegen": ("project.yml", "project.yaml"),
    "fastlane": ("Fastfile", "Appfile"),
    "ruby_bundle": ("Gemfile", "Gemfile.lock"),
    "privacy_manifest": ("PrivacyInfo.xcprivacy",),
}

TOOLS = (
    "xcodebuild", "xcrun", "swift", "git", "python3", "ruby", "bundle",
    "pod", "carthage", "tuist", "xcodegen", "fastlane",
)

CI_PATTERNS = (
    ".github/workflows/*.yml", ".github/workflows/*.yaml",
    ".azure-pipelines/*.yml", ".azure-pipelines/*.yaml",
    "azure-pipelines.yml", "azure-pipelines.yaml", ".gitlab-ci.yml",
    "Jenkinsfile", "bitrise.yml", ".circleci/config.yml",
)


def iter_paths(root: Path) -> Iterable[Path]:
    for current, dirs, files in os.walk(root):
        dirs[:] = [d for d in dirs if d not in IGNORE_DIRS]
        base = Path(current)
        for name in files:
            yield base / name
        for name in dirs:
            if name.endswith((".xcodeproj", ".xcworkspace")):
                yield base / name


def relative(path: Path, root: Path) -> str:
    try:
        return path.relative_to(root).as_posix()
    except ValueError:
        return path.as_posix()


def detect(root: Path) -> dict:
    all_paths = list(iter_paths(root))
    files_by_name: dict[str, list[str]] = {}
    projects: list[str] = []
    workspaces: list[str] = []
    tests: list[str] = []

    for path in all_paths:
        rel = relative(path, root)
        if path.name.endswith(".xcodeproj"):
            projects.append(rel)
        elif path.name.endswith(".xcworkspace"):
            workspaces.append(rel)
        else:
            files_by_name.setdefault(path.name, []).append(rel)
            low = rel.lower()
            if any(token in low for token in ("tests/", "test/", "tests.swift", "test.swift", "uitests")):
                tests.append(rel)

    markers: dict[str, list[str]] = {}
    for category, names in FILE_MARKERS.items():
        found = []
        for name in names:
            found.extend(files_by_name.get(name, []))
        markers[category] = sorted(set(found))

    ci_files: list[str] = []
    for pattern in CI_PATTERNS:
        ci_files.extend(relative(p, root) for p in root.glob(pattern) if p.is_file())

    tools = {name: shutil.which(name) for name in TOOLS}
    is_macos = platform.system() == "Darwin"
    has_xcode = is_macos and bool(tools["xcodebuild"] and tools["xcrun"])
    has_swift = bool(tools["swift"])

    limitations: list[str] = []
    if not has_xcode:
        limitations.append(
            "Apple app builds, simulator/device tests, signing, archives, and XCUITest are not authoritative without macOS and Xcode."
        )
    if not has_swift:
        limitations.append("No Swift toolchain was detected; Swift build and test commands are unavailable.")
    if platform.system() != "Darwin" and has_swift:
        limitations.append(
            "A non-macOS Swift toolchain may validate compatible pure Swift packages only; it does not validate Apple app targets."
        )

    capabilities = {
        "can_inspect_source": True,
        "can_run_xcodebuild": has_xcode,
        "can_run_swift_package_commands": has_swift,
        "can_run_apple_ui_tests": has_xcode,
        "can_validate_signing_or_archive": has_xcode,
    }

    return {
        "root": str(root),
        "environment": {
            "os": platform.system(),
            "os_release": platform.release(),
            "architecture": platform.machine(),
            "python": sys.version.split()[0],
        },
        "tools": tools,
        "projects": sorted(set(projects)),
        "workspaces": sorted(set(workspaces)),
        "markers": markers,
        "test_files_sample": sorted(set(tests))[:100],
        "ci_files": sorted(set(ci_files)),
        "capabilities": capabilities,
        "limitations": limitations,
    }


def to_markdown(data: dict) -> str:
    lines = [
        "# Apple Toolchain Capability Report",
        "",
        f"- Root: `{data['root']}`",
        f"- OS: {data['environment']['os']} {data['environment']['os_release']}",
        f"- Architecture: {data['environment']['architecture']}",
        "",
        "## Capabilities",
        "",
    ]
    for key, value in data["capabilities"].items():
        lines.append(f"- {key}: {'yes' if value else 'no'}")
    lines += ["", "## Project Markers", ""]
    lines.append(f"- Xcode projects: {len(data['projects'])}")
    lines.append(f"- Xcode workspaces: {len(data['workspaces'])}")
    for key, values in data["markers"].items():
        lines.append(f"- {key}: {len(values)}")
    lines += ["", "## CI", ""]
    if data["ci_files"]:
        lines.extend(f"- `{item}`" for item in data["ci_files"])
    else:
        lines.append("- No recognized CI file detected.")
    lines += ["", "## Limitations", ""]
    if data["limitations"]:
        lines.extend(f"- {item}" for item in data["limitations"])
    else:
        lines.append("- No baseline toolchain limitation detected; project-specific inputs may still be required.")
    return "\n".join(lines) + "\n"


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--root", default=".", help="Repository root to inspect (default: current directory).")
    parser.add_argument("--format", choices=("json", "markdown"), default="json", help="Output format.")
    return parser.parse_args()


def main() -> int:
    args = parse_args()
    root = Path(args.root).expanduser().resolve()
    if not root.exists() or not root.is_dir():
        print(f"error: repository root is not a directory: {root}", file=sys.stderr)
        return 2
    data = detect(root)
    if args.format == "json":
        print(json.dumps(data, indent=2, sort_keys=True))
    else:
        print(to_markdown(data), end="")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
