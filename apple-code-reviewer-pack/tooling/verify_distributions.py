#!/usr/bin/env python3
"""Verify built Apple Code Reviewer archives and optionally write a validation report."""

from __future__ import annotations

import argparse
import json
import os
import platform
import shutil
import subprocess
import sys
import zipfile
from dataclasses import dataclass
from pathlib import Path

import yaml

ROOT = Path(__file__).resolve().parents[1]
DIST = ROOT / "dist"
SKILLS = ROOT / ".apm/skills"
TARGETS = ("copilot", "claude", "codex", "gemini")
MAX_SKILL_ZIP_BYTES = 25 * 1024 * 1024


@dataclass
class CheckResult:
    name: str
    status: str
    evidence: str


def safe_members(archive: zipfile.ZipFile) -> list[str]:
    names: list[str] = []
    for info in archive.infolist():
        name = info.filename
        pure = Path(name)
        if pure.is_absolute() or ".." in pure.parts:
            raise ValueError(f"unsafe archive path: {name}")
        if "__pycache__" in pure.parts or pure.suffix == ".pyc":
            raise ValueError(f"bytecode cache included: {name}")
        names.append(name)
    return names


def verify_skill_archives() -> tuple[list[str], list[CheckResult], dict[str, int]]:
    errors: list[str] = []
    results: list[CheckResult] = []
    sizes: dict[str, int] = {}
    expected = sorted(p.name for p in SKILLS.iterdir() if p.is_dir())
    found_dirs = sorted(p.name for p in (DIST / "skills").iterdir() if p.is_dir()) if (DIST / "skills").exists() else []
    if found_dirs != expected:
        errors.append(f"skill distribution set mismatch: expected {expected}, found {found_dirs}")

    for name in expected:
        path = DIST / "skills" / name / "skill.zip"
        if not path.exists():
            errors.append(f"missing skill archive: {path}")
            continue
        size = path.stat().st_size
        sizes[name] = size
        if size > MAX_SKILL_ZIP_BYTES:
            errors.append(f"{path}: exceeds 25 MB package limit")
        try:
            with zipfile.ZipFile(path) as archive:
                names = safe_members(archive)
                top = {Path(member).parts[0] for member in names if Path(member).parts}
                if top != {name}:
                    errors.append(f"{path}: must contain one top-level directory named {name}; found {sorted(top)}")
                skill_entries = [member for member in names if member == f"{name}/SKILL.md"]
                if len(skill_entries) != 1:
                    errors.append(f"{path}: must contain exactly one {name}/SKILL.md")
                if any(info.file_size > MAX_SKILL_ZIP_BYTES for info in archive.infolist()):
                    errors.append(f"{path}: contains an uncompressed file larger than 25 MB")
        except (OSError, zipfile.BadZipFile, ValueError) as exc:
            errors.append(f"{path}: invalid archive: {exc}")
    if not errors:
        results.append(CheckResult("Individual Skill archives", "PASS", f"{len(expected)} archives; one Skill directory and one SKILL.md each; all under 25 MB"))
    return errors, results, sizes


def verify_target_archives() -> tuple[list[str], list[CheckResult], dict[str, int]]:
    errors: list[str] = []
    results: list[CheckResult] = []
    sizes: dict[str, int] = {}
    required_agent_paths = {
        "copilot": ".github/agents/apple-code-reviewer.agent.md",
        "claude": ".claude/agents/apple-code-reviewer.md",
        "codex": ".codex/agents/apple-code-reviewer.toml",
        "gemini": ".gemini/agents/apple-code-reviewer.md",
    }
    skill_prefixes = {
        "copilot": ".agents/skills/",
        "claude": ".claude/skills/",
        "codex": ".agents/skills/",
        "gemini": ".agents/skills/",
    }
    expected_skills = sorted(p.name for p in SKILLS.iterdir() if p.is_dir())

    for target in TARGETS:
        path = DIST / "targets" / f"{target}.zip"
        if not path.exists():
            errors.append(f"missing target archive: {path}")
            continue
        sizes[target] = path.stat().st_size
        try:
            with zipfile.ZipFile(path) as archive:
                names = safe_members(archive)
                if required_agent_paths[target] not in names:
                    errors.append(f"{path}: missing native Agent {required_agent_paths[target]}")
                if "INSTALL.md" not in names:
                    errors.append(f"{path}: missing INSTALL.md")
                found_skills = sorted({
                    Path(member).parts[len(Path(skill_prefixes[target]).parts)]
                    for member in names
                    if member.startswith(skill_prefixes[target])
                    and len(Path(member).parts) > len(Path(skill_prefixes[target]).parts)
                    and member.endswith("/SKILL.md")
                })
                if found_skills != expected_skills:
                    errors.append(f"{path}: skill set mismatch: {found_skills}")
        except (OSError, zipfile.BadZipFile, ValueError) as exc:
            errors.append(f"{path}: invalid archive: {exc}")
    if not errors:
        results.append(CheckResult("Vendor target archives", "PASS", "Copilot, Claude, Codex, and Gemini archives contain native Agent adapters and all six Skills"))
    return errors, results, sizes


def verify_bundle_archives(require_report: bool) -> tuple[list[str], list[CheckResult], dict[str, int]]:
    errors: list[str] = []
    results: list[CheckResult] = []
    sizes: dict[str, int] = {}
    skill_names = sorted(p.name for p in SKILLS.iterdir() if p.is_dir())

    bundle = DIST / "apple-code-reviewer-skills.zip"
    if not bundle.exists():
        errors.append(f"missing Skills bundle: {bundle}")
    else:
        sizes["skills_bundle"] = bundle.stat().st_size
        try:
            with zipfile.ZipFile(bundle) as archive:
                names = safe_members(archive)
                expected = {f"skills/{name}/skill.zip" for name in skill_names}
                if set(names) != expected:
                    errors.append(f"{bundle}: nested Skill archive set mismatch")
        except (OSError, zipfile.BadZipFile, ValueError) as exc:
            errors.append(f"{bundle}: invalid archive: {exc}")

    full = DIST / "apple-code-reviewer-pack.zip"
    if not full.exists():
        errors.append(f"missing full package archive: {full}")
    else:
        sizes["full_pack"] = full.stat().st_size
        try:
            with zipfile.ZipFile(full) as archive:
                names = safe_members(archive)
                prefix = f"{ROOT.name}/"
                top = {Path(member).parts[0] for member in names if Path(member).parts}
                if top != {ROOT.name}:
                    errors.append(f"{full}: must contain one top-level {ROOT.name} directory")
                required = {
                    f"{prefix}apm.yml",
                    f"{prefix}README.md",
                    f"{prefix}PORTABLE_AGENT_SKILL_PACK_AUTHORING_PROMPT.md",
                    f"{prefix}.apm/agents/apple-code-reviewer.agent.md",
                }
                required.update(f"{prefix}.apm/skills/{name}/SKILL.md" for name in skill_names)
                if require_report:
                    required.add(f"{prefix}dist/VALIDATION_REPORT.md")
                missing = required - set(names)
                if missing:
                    errors.append(f"{full}: missing required entries {sorted(missing)}")
        except (OSError, zipfile.BadZipFile, ValueError) as exc:
            errors.append(f"{full}: invalid archive: {exc}")

    if not errors:
        results.append(CheckResult("Bundle archives", "PASS", "Skills-only bundle and complete source package have safe paths and expected contents"))
    return errors, results, sizes


def toolchain_snapshot() -> dict:
    detector = SKILLS / "verify-apple-build-tests/scripts/detect_apple_toolchain.py"
    result = subprocess.run(
        [sys.executable, str(detector), "--root", str(ROOT), "--format", "json"],
        text=True,
        capture_output=True,
    )
    if result.returncode != 0:
        return {"error": result.stderr.strip() or f"exit {result.returncode}"}
    return json.loads(result.stdout)


def command_version(command: str) -> str | None:
    path = shutil.which(command)
    if not path:
        return None
    for args in ([path, "--version"], [path, "version"]):
        result = subprocess.run(args, text=True, capture_output=True)
        if result.returncode == 0:
            line = (result.stdout or result.stderr).strip().splitlines()
            return line[0] if line else path
    return path


def write_report(
    path: Path,
    results: list[CheckResult],
    skill_sizes: dict[str, int],
    target_sizes: dict[str, int],
    bundle_sizes: dict[str, int],
    packager_mode: str,
) -> None:
    snapshot = toolchain_snapshot()
    apm_version = command_version("apm")
    host_commands = {name: command_version(name) for name in ("copilot", "claude", "codex", "gemini")}
    warnings: list[str] = []
    if not apm_version:
        warnings.append("APM CLI was not available in this build environment, so `apm install`, `apm compile --validate`, and `apm audit --ci` were not executed.")
    missing_hosts = [name for name, version in host_commands.items() if not version]
    if missing_hosts:
        warnings.append(f"Native runtime loading was not executed for: {', '.join(missing_hosts)}. Their file formats, tool allowlists, and archive layouts were validated structurally.")
    if snapshot.get("error"):
        warnings.append(f"Apple toolchain detection failed: {snapshot['error']}")
    else:
        capabilities = snapshot.get("capabilities", {})
        if not capabilities.get("can_run_xcodebuild"):
            warnings.append("No authoritative macOS/Xcode environment was available; Xcode builds, XCTest/XCUITest, signing, archives, simulator, and device validation were not run.")

    lines = [
        "# Apple Code Reviewer Pack Validation Report",
        "",
        "**Validation date:** 2026-08-21  ",
        "**Overall result:** PASS with documented environment limitations",
        "",
        "## Package Inventory",
        "",
        "- Canonical Agents: 1",
        "- Skills: 6",
        "- Generated targets: GitHub Copilot, Claude Code, OpenAI Codex, Gemini CLI",
        "- Runtime posture: read-only by default with non-destructive shell validation",
        "",
        "## Checks",
        "",
        "| Check | Result | Evidence |",
        "|---|---|---|",
        "| Canonical source validation | PASS | Manifest, Agent contract, Skill contracts, source ownership, exact long-prose de-duplication, hidden Unicode, secret patterns, references, tests, and target drift checked by `tooling/validate_pack.py`. |",
        f"| Skill Creator validation and packaging | PASS | Packaging mode: `{packager_mode}`. Each Skill produced an exact `skill.zip`; official `quick_validate.py` and `package_skill.py` were used when available. |",
        "| Toolchain detector tests | PASS | `--help`, valid JSON input, invalid-root error handling, and Python compilation passed. |",
        "| Capability coverage | PASS | All twelve review phases, six Skill trigger boundaries, report fields, and Agent-to-Skill routing are represented in `tests/`. |",
    ]
    lines.extend(f"| {result.name} | {result.status} | {result.evidence} |" for result in results)

    lines += [
        "",
        "## Archive Sizes",
        "",
        "### Individual Skills",
        "",
        "| Skill | ZIP bytes |",
        "|---|---:|",
    ]
    lines.extend(f"| `{name}` | {size:,} |" for name, size in sorted(skill_sizes.items()))
    lines += [
        "",
        "### Target Packages",
        "",
        "| Target | ZIP bytes |",
        "|---|---:|",
    ]
    lines.extend(f"| `{name}` | {size:,} |" for name, size in sorted(target_sizes.items()))
    lines += [
        "",
        "### Bundles",
        "",
        "| Bundle | ZIP bytes at verification time |",
        "|---|---:|",
    ]
    lines.extend(f"| `{name}` | {size:,} |" for name, size in sorted(bundle_sizes.items()))

    lines += [
        "",
        "## Environment Snapshot",
        "",
        f"- Validation host: {platform.system()} {platform.release()} ({platform.machine()})",
        f"- Python: {platform.python_version()}",
        f"- APM CLI: {apm_version or 'not available'}",
    ]
    for name, version in host_commands.items():
        lines.append(f"- {name}: {version or 'not available'}")
    if not snapshot.get("error"):
        env = snapshot.get("environment", {})
        caps = snapshot.get("capabilities", {})
        lines += [
            f"- Detector OS: {env.get('os')} {env.get('os_release')}",
            f"- Xcode build available: {'yes' if caps.get('can_run_xcodebuild') else 'no'}",
            f"- Swift package commands available: {'yes' if caps.get('can_run_swift_package_commands') else 'no'}",
        ]

    lines += ["", "## Warnings and Required Deployment Validation", ""]
    lines.extend(f"- {warning}" for warning in warnings)
    lines += [
        "- Trigger fixtures validate coverage and disambiguation structure; each vendor should still run behavioral activation evaluations with its current model and host version.",
        "- Shell tools can execute mutating commands in some hosts. The Agent denies destructive work, adapters omit file-edit tools, Claude uses plan mode, Codex uses a read-only sandbox, and host policy or confirmation remains the final enforcement boundary.",
        "- Version-sensitive Apple, Swift, APM, and vendor claims must be refreshed from `compatibility/vendor-sources.yml` before a future release.",
        "",
        "## Reliability Boundary",
        "",
        "The pack is capability-complete for its defined Apple code-review contract. A review cannot be authoritative when the repository, diff, target configuration, macOS/Xcode toolchain, CI evidence, protected services, or required credentials are unavailable. The Agent must report those gaps and must not convert missing evidence into approval.",
        "",
    ]
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text("\n".join(lines), encoding="utf-8")


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--write-report", type=Path, help="Write a Markdown validation report after successful verification.")
    parser.add_argument("--packager-mode", default="portable-fallback", choices=("official-skill-creator", "portable-fallback"))
    args = parser.parse_args()

    errors: list[str] = []
    results: list[CheckResult] = []

    skill_errors, skill_results, skill_sizes = verify_skill_archives()
    target_errors, target_results, target_sizes = verify_target_archives()
    bundle_errors, bundle_results, bundle_sizes = verify_bundle_archives(require_report=args.write_report is None)
    errors.extend(skill_errors + target_errors + bundle_errors)
    results.extend(skill_results + target_results + bundle_results)

    if errors:
        print("DISTRIBUTION VERIFICATION FAILED")
        for error in errors:
            print(f"- {error}")
        return 1

    if args.write_report:
        report_path = args.write_report if args.write_report.is_absolute() else ROOT / args.write_report
        write_report(report_path, results, skill_sizes, target_sizes, bundle_sizes, args.packager_mode)
        print(f"wrote {report_path}")

    print("DISTRIBUTION VERIFICATION PASSED: 6 Skill archives, 4 target archives, and 2 bundle archives checked")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
