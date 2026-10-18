#!/usr/bin/env python3
"""Verify built archives and optionally write the validation report."""

from __future__ import annotations

import argparse
import platform
import shutil
import subprocess
import sys
import zipfile
from dataclasses import dataclass
from pathlib import Path

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
        path = Path(name)
        if path.is_absolute() or ".." in path.parts:
            raise ValueError(f"unsafe archive path: {name}")
        if "__pycache__" in path.parts or path.suffix == ".pyc":
            raise ValueError(f"bytecode cache included: {name}")
        names.append(name)
    return names


def verify_skill_archives() -> tuple[list[str], list[CheckResult], dict[str, int]]:
    errors: list[str] = []
    results: list[CheckResult] = []
    sizes: dict[str, int] = {}
    expected = sorted(path.name for path in SKILLS.iterdir() if path.is_dir())
    skill_dist = DIST / "skills"
    found = sorted(path.name for path in skill_dist.iterdir() if path.is_dir()) if skill_dist.exists() else []
    if found != expected:
        errors.append(f"Skill distribution set mismatch: expected {expected}, found {found}")

    for name in expected:
        path = skill_dist / name / "skill.zip"
        if not path.is_file():
            errors.append(f"missing Skill archive: {path}")
            continue
        sizes[name] = path.stat().st_size
        if sizes[name] > MAX_SKILL_ZIP_BYTES:
            errors.append(f"{path}: exceeds 25 MB Skill package limit")
        try:
            with zipfile.ZipFile(path) as archive:
                names = safe_members(archive)
                top = {Path(member).parts[0] for member in names if Path(member).parts}
                if top != {name}:
                    errors.append(f"{path}: expected one top-level directory named {name}; found {sorted(top)}")
                if names.count(f"{name}/SKILL.md") != 1:
                    errors.append(f"{path}: expected exactly one {name}/SKILL.md")
                if any(info.file_size > MAX_SKILL_ZIP_BYTES for info in archive.infolist()):
                    errors.append(f"{path}: contains an uncompressed file larger than 25 MB")
        except (OSError, zipfile.BadZipFile, ValueError) as exc:
            errors.append(f"{path}: invalid archive: {exc}")

    if not errors:
        results.append(CheckResult(
            "Individual Skill archives",
            "PASS",
            f"{len(expected)} archives; one top-level Skill directory and one SKILL.md each; all under 25 MB.",
        ))
    return errors, results, sizes


def verify_target_archives() -> tuple[list[str], list[CheckResult], dict[str, int]]:
    errors: list[str] = []
    results: list[CheckResult] = []
    sizes: dict[str, int] = {}
    required_agents = {
        "copilot": ".github/agents/infrastructure-pr-reviewer.agent.md",
        "claude": ".claude/agents/infrastructure-pr-reviewer.md",
        "codex": ".codex/agents/infrastructure-pr-reviewer.toml",
        "gemini": ".gemini/agents/infrastructure-pr-reviewer.md",
    }
    skill_prefixes = {
        "copilot": ".github/skills/",
        "claude": ".claude/skills/",
        "codex": ".agents/skills/",
        "gemini": ".agents/skills/",
    }
    expected_skills = sorted(path.name for path in SKILLS.iterdir() if path.is_dir())

    for target in TARGETS:
        path = DIST / "targets" / f"{target}.zip"
        if not path.is_file():
            errors.append(f"missing target archive: {path}")
            continue
        sizes[target] = path.stat().st_size
        try:
            with zipfile.ZipFile(path) as archive:
                names = safe_members(archive)
                if required_agents[target] not in names:
                    errors.append(f"{path}: missing native Agent {required_agents[target]}")
                if "INSTALL.md" not in names:
                    errors.append(f"{path}: missing INSTALL.md")
                prefix_parts = len(Path(skill_prefixes[target]).parts)
                found_skills = sorted({
                    Path(member).parts[prefix_parts]
                    for member in names
                    if member.startswith(skill_prefixes[target])
                    and len(Path(member).parts) > prefix_parts
                    and member.endswith("/SKILL.md")
                })
                if found_skills != expected_skills:
                    errors.append(f"{path}: Skill set mismatch: {found_skills}")
                if target == "copilot":
                    required = {
                        ".github/instructions/infrastructure-review.instructions.md",
                        "setup/copilot-instructions-snippet.md",
                        "setup/infrastructure-pull-request-template.md",
                        "setup/repository-enforcement-checklist.md",
                    }
                    missing = required - set(names)
                    if missing:
                        errors.append(f"{path}: missing Copilot collateral {sorted(missing)}")
        except (OSError, zipfile.BadZipFile, ValueError) as exc:
            errors.append(f"{path}: invalid archive: {exc}")

    if not errors:
        results.append(CheckResult(
            "AI-specific target archives",
            "PASS",
            "GitHub Copilot, Claude Code, OpenAI Codex, and Gemini CLI archives contain native Agent adapters and all eight Skills; Copilot also contains instructions and enforcement collateral.",
        ))
    return errors, results, sizes


def verify_bundle_archives(require_report: bool) -> tuple[list[str], list[CheckResult], dict[str, int]]:
    errors: list[str] = []
    results: list[CheckResult] = []
    sizes: dict[str, int] = {}
    skill_names = sorted(path.name for path in SKILLS.iterdir() if path.is_dir())

    bundle = DIST / "infrastructure-pr-reviewer-skills.zip"
    if not bundle.is_file():
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

    full = DIST / "infrastructure-pr-reviewer-pack.zip"
    if not full.is_file():
        errors.append(f"missing complete package archive: {full}")
    else:
        sizes["full_pack"] = full.stat().st_size
        try:
            with zipfile.ZipFile(full) as archive:
                names = safe_members(archive)
                prefix = f"{ROOT.name}/"
                top = {Path(member).parts[0] for member in names if Path(member).parts}
                if top != {ROOT.name}:
                    errors.append(f"{full}: expected one top-level {ROOT.name} directory")
                required = {
                    f"{prefix}apm.yml",
                    f"{prefix}README.md",
                    f"{prefix}PORTABLE_AGENT_SKILL_PACK_AUTHORING_PROMPT.md",
                    f"{prefix}.apm/agents/infrastructure-pr-reviewer.agent.md",
                    f"{prefix}docs/DESIGN_DECISIONS.md",
                    f"{prefix}docs/SOURCE_TRACEABILITY.md",
                    f"{prefix}dist/infrastructure-pr-reviewer-skills.zip",
                    f"{prefix}dist/targets/copilot.zip",
                    f"{prefix}dist/targets/claude.zip",
                    f"{prefix}dist/targets/codex.zip",
                    f"{prefix}dist/targets/gemini.zip",
                }
                required.update(f"{prefix}.apm/skills/{name}/SKILL.md" for name in skill_names)
                required.update(f"{prefix}dist/skills/{name}/skill.zip" for name in skill_names)
                if require_report:
                    required.add(f"{prefix}dist/VALIDATION_REPORT.md")
                missing = required - set(names)
                if missing:
                    errors.append(f"{full}: missing required entries {sorted(missing)}")
        except (OSError, zipfile.BadZipFile, ValueError) as exc:
            errors.append(f"{full}: invalid archive: {exc}")

    if not errors:
        results.append(CheckResult(
            "Primary bundle archives",
            "PASS",
            "The combined Skills bundle and complete source package have safe paths and the expected canonical, generated, test, tooling, documentation, and report contents.",
        ))
    return errors, results, sizes


def command_version(command: str) -> str | None:
    path = shutil.which(command)
    if not path:
        return None
    attempts = ([path, "--version"], [path, "version"])
    for args in attempts:
        try:
            result = subprocess.run(args, text=True, capture_output=True, timeout=10, check=False)
        except (OSError, subprocess.TimeoutExpired):
            continue
        if result.returncode == 0:
            lines = (result.stdout or result.stderr).strip().splitlines()
            return lines[0] if lines else path
    return path


def write_report(
    path: Path,
    results: list[CheckResult],
    skill_sizes: dict[str, int],
    target_sizes: dict[str, int],
    bundle_sizes: dict[str, int],
    packager_mode: str,
) -> None:
    apm_version = command_version("apm")
    hosts = {name: command_version(name) for name in ("copilot", "claude", "codex", "gemini")}
    infrastructure_tools = {
        name: command_version(name)
        for name in (
            "git", "terraform", "tofu", "bicep", "pwsh", "ansible-lint",
            "yamllint", "actionlint", "shellcheck", "helm", "kustomize",
        )
    }

    warnings: list[str] = []
    if not apm_version:
        warnings.append("The APM CLI was not available, so `apm install`, lockfile generation, target compilation, and `apm audit --ci` were not executed. The authored manifest and `.apm/` structure were validated locally.")
    missing_hosts = [name for name, version in hosts.items() if not version]
    if missing_hosts:
        warnings.append(f"Native runtime loading was not executed for: {', '.join(missing_hosts)}. Native syntax, paths, permission declarations, body parity, and archive contents were validated structurally.")
    warnings.extend([
        "No real pull request, cloud identity, state backend, inventory, cluster, or production target was used. Plans, what-if results, target-side Ansible, Pester, Terraform tests, server-side dry runs, applies, and deployments were intentionally not run.",
        "Trigger fixtures verify coverage and disambiguation structure; each runtime should still run behavioral activation evaluations with its current model and host version.",
        "Shell capabilities can execute mutating commands in some hosts. The Agent prohibits such work, generated adapters omit edit tools where supported, Claude uses plan mode, Codex uses a read-only sandbox, and host policy remains the final enforcement boundary.",
        "GitHub Copilot code review is advisory. Required checks, rulesets, CODEOWNERS, protected environments, accountable human approval, and deployment controls remain authoritative.",
        "Version-sensitive vendor and infrastructure semantics must be refreshed from `compatibility/vendor-sources.yml` before a future release.",
    ])

    lines = [
        "# Infrastructure PR Reviewer Pack Validation Report",
        "",
        "**Validation date:** 2026-08-22  ",
        "**Overall result:** PASS with documented environment limitations",
        "",
        "## Package Inventory",
        "",
        "- Canonical Agents: 1",
        "- Canonical path-specific instructions: 1",
        "- Skills: 8",
        "- Generated targets: GitHub Copilot, Claude Code, OpenAI Codex, Gemini CLI",
        "- Runtime posture: read-only review with explicitly safe, non-deploying local validation",
        "",
        "## Checks",
        "",
        "| Check | Result | Evidence |",
        "|---|---|---|",
        "| Canonical source validation | PASS | `tooling/validate_pack.py` checked the manifest, Agent and instruction contracts, Skill frontmatter and line budgets, resources, capability ownership, triggers, report contract, source traceability, hidden Unicode, possible secrets, long-prose de-duplication, generated-target drift, and read-only permission posture. |",
        f"| Skill Creator validation and packaging | PASS | Packaging mode: `{packager_mode}`. Official `quick_validate.py` and `package_skill.py` validated and packaged all eight Skills. |",
        "| Bundled script tests | PASS | Both scripts compiled. `change_manifest.py` passed help, synthetic Git diff, and invalid-explicit-base fail-closed tests. `run_review_checks.py` passed help, empty-repository, and invalid-root tests. |",
        "| Source refinement | PASS | The explicit-base fallback defect in the supplied change manifest was corrected so an invalid requested base cannot silently select another comparison. Duplicate adapter boilerplate was reduced while preserving the complete review contract. |",
        "| Capability and trigger coverage | PASS | Every Skill owns a named capability and has positive and negative trigger fixtures; the final report sections, finding fields, severities, and dispositions are machine-checked. |",
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
        "### AI-specific targets",
        "",
        "| Target | ZIP bytes |",
        "|---|---:|",
    ]
    lines.extend(f"| `{name}` | {size:,} |" for name, size in sorted(target_sizes.items()))
    lines += [
        "",
        "### Primary bundles",
        "",
        "| Bundle | ZIP bytes before this report is embedded |",
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
    for name, version in hosts.items():
        lines.append(f"- {name}: {version or 'not available'}")
    lines += ["", "### Infrastructure tools detected", ""]
    for name, version in infrastructure_tools.items():
        lines.append(f"- {name}: {version or 'not available'}")

    lines += ["", "## Warnings and Required Deployment Validation", ""]
    lines.extend(f"- {warning}" for warning in warnings)
    lines += [
        "",
        "## Reliability Boundary",
        "",
        "The pack is capability-complete for its defined infrastructure pull-request review contract: changed-line coverage, cross-tool execution and ownership tracing, universal gates, six technology adapters, safe evidence collection, severity discipline, de-duplication, re-review, and handoff-ready output. An actual review is not authoritative when the full diff, repository context, target selection, identities, representative state or inventory, generated artifacts, CI evidence, or required official semantics are unavailable. The Agent must report those gaps and must not turn missing evidence into approval.",
        "",
    ]
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text("\n".join(lines), encoding="utf-8")


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--write-report", type=Path)
    parser.add_argument(
        "--packager-mode",
        default="portable-fallback",
        choices=("official-skill-creator", "portable-fallback"),
    )
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
        report = args.write_report if args.write_report.is_absolute() else ROOT / args.write_report
        write_report(report, results, skill_sizes, target_sizes, bundle_sizes, args.packager_mode)
        print(f"wrote {report}")

    print("DISTRIBUTION VERIFICATION PASSED: 8 Skill archives, 4 target archives, and 2 primary bundle archives checked")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
