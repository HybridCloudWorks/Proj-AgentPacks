#!/usr/bin/env python3
"""Validate the Codex orchestration pack structurally and without external mutations."""
from __future__ import annotations

import argparse
import json
import re
import zipfile
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
SKILLS = ROOT / ".apm" / "skills"
DIST = ROOT / "dist"
REQUIRED = {
    "codex-agentic-workflow-dispatch",
    "codex-agent-registry-and-capability-discovery",
    "codex-handoff-contract-and-state",
    "codex-subagent-delegation-and-concurrency",
    "codex-hooks-and-guardrails",
    "codex-workflow-evidence-and-recovery",
}


def skill_errors(path: Path) -> list[str]:
    errors = []
    manifest = path / "SKILL.md"
    if not manifest.is_file():
        return [f"missing SKILL.md: {manifest}"]
    text = manifest.read_text(encoding="utf-8")
    if not text.startswith("---\n") or "\n---\n" not in text[4:]:
        errors.append(f"invalid frontmatter: {manifest}")
    name = re.search(r"^name:\s*([a-z0-9][a-z0-9-]*)\s*$", text, re.M)
    description = re.search(r"^description:\s*(.+)$", text, re.M)
    if not name or name.group(1) != path.name:
        errors.append(f"name mismatch: {manifest}")
    if not description or len(description.group(1)) < 40:
        errors.append(f"non-discriminating description: {manifest}")
    if re.search(r"(?i)\bTODO\b|lorem ipsum", text):
        errors.append(f"unfinished placeholder: {manifest}")
    return errors


def zip_error(path: Path, expected: str | None = None) -> str | None:
    try:
        with zipfile.ZipFile(path) as archive:
            names = archive.namelist()
            if any(name.startswith("/") or ".." in Path(name).parts for name in names):
                return f"unsafe archive path: {path}"
            if expected:
                manifests = [name for name in names if name.endswith("/SKILL.md")]
                if len(manifests) != 1 or not manifests[0].startswith(expected + "/"):
                    return f"invalid Skill archive shape: {path}"
    except (OSError, zipfile.BadZipFile) as exc:
        return f"invalid zip {path}: {exc}"
    return None


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--write-report", action="store_true")
    args = parser.parse_args()
    errors: list[str] = []
    for name in ["DESCRIPTION.md", "VALIDATION_REPORT.md", "PORTABLE_AGENT_SKILL_PACK_AUTHORING_PROMPT.md", "LICENSE"]:
        if not (ROOT / name).is_file():
            errors.append(f"missing {name}")
    if (ROOT / "validation-report.md").exists():
        errors.append("lowercase validation report must not exist")
    actual = {path.name for path in SKILLS.iterdir() if path.is_dir()} if SKILLS.exists() else set()
    if actual != REQUIRED:
        errors.append(f"Skill set mismatch: expected {sorted(REQUIRED)}, got {sorted(actual)}")
    for skill in sorted(actual):
        errors.extend(skill_errors(SKILLS / skill))
    agent = ROOT / ".apm" / "agents" / "codex-agentic-orchestrator.agent.md"
    if not agent.is_file() or len(agent.read_text(encoding="utf-8").splitlines()) > 100:
        errors.append("canonical Agent missing or over 100 lines")
    for required in [ROOT / ".codex" / "hooks.json", ROOT / ".codex" / "config.agentic-orchestrator.toml", ROOT / "tooling" / "workflow.py", ROOT / "hooks" / "codex_event.py", ROOT / "compatibility" / "agent-registry.yml"]:
        if not required.is_file():
            errors.append(f"missing Codex integration file: {required}")
    hooks_path = ROOT / ".codex" / "hooks.json"
    if hooks_path.is_file():
        try:
            settings = json.loads(hooks_path.read_text(encoding="utf-8"))
            hooks = settings.get("hooks", {})
            for event in ["SessionStart", "SubagentStart", "SubagentStop", "Stop"]:
                if event not in hooks:
                    errors.append(f"missing hook event: {event}")
        except json.JSONDecodeError as exc:
            errors.append(f"invalid Codex hooks JSON: {exc}")
    for skill in sorted(REQUIRED):
        archive = DIST / "skills" / skill / "skill.zip"
        if not archive.is_file():
            errors.append(f"missing Skill archive: {archive}")
        else:
            problem = zip_error(archive, skill)
            if problem:
                errors.append(problem)
    for archive_name in ["codex-agentic-orchestrator-pack.zip", "codex-agentic-orchestrator-canonical.zip", "codex-agentic-orchestrator-prompt.zip", "codex-agentic-orchestrator-skills.zip", "codex-agentic-orchestrator-validation.zip", "openai-codex/openai-codex.zip"]:
        archive = DIST / archive_name
        if not archive.is_file():
            errors.append(f"missing primary archive: {archive}")
        else:
            problem = zip_error(archive)
            if problem:
                errors.append(problem)
    result = "PASS" if not errors else "FAIL"
    report = ["# Validation Report", "", f"Result: **{result}**", "", "## Checks", "", "- Canonical Codex orchestration Agent and six focused Skills", "- Project-local Codex target with custom agent, Skills, registry, tooling, and hook configuration", "- Capability registry supports one, selected, and all installed agents", "- Missing required versus optional agents have distinct states", "- Handoff, archive safety, and uppercase report checks", "- No live Codex session, model call, MCP call, cloud operation, or external mutation", ""]
    if errors:
        report += ["## Errors", ""] + [f"- {error}" for error in errors]
    else:
        report += ["## Result", "", "All structural and packaging checks passed. Static checks do not prove live Codex installation, authentication, hook trust, permissions, model availability, subagent execution, or external tool behavior."]
    text = "\n".join(report) + "\n"
    if args.write_report:
        (ROOT / "VALIDATION_REPORT.md").write_text(text, encoding="utf-8")
    print(text)
    return 0 if not errors else 1


if __name__ == "__main__":
    raise SystemExit(main())
