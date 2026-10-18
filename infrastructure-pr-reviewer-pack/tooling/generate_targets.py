#!/usr/bin/env python3
"""Generate native Agent and Skill layouts for the supported AI runtimes."""

from __future__ import annotations

import argparse
import re
import shutil
import tomllib
from pathlib import Path
from typing import Any

import yaml

ROOT = Path(__file__).resolve().parents[1]
CANONICAL_AGENT = ROOT / ".apm/agents/infrastructure-pr-reviewer.agent.md"
CANONICAL_INSTRUCTION = ROOT / ".apm/instructions/infrastructure-review.instructions.md"
SKILLS = ROOT / ".apm/skills"
COPILOT_SETUP = ROOT / "setup/copilot"
DIST = ROOT / "dist/targets"
TARGETS = ("copilot", "claude", "codex", "gemini")


def parse_frontmatter(path: Path) -> tuple[dict[str, Any], str]:
    text = path.read_text(encoding="utf-8")
    match = re.match(r"^---\n(.*?)\n---\n?(.*)$", text, re.DOTALL)
    if not match:
        raise ValueError(f"missing YAML frontmatter: {path}")
    data = yaml.safe_load(match.group(1))
    if not isinstance(data, dict):
        raise ValueError(f"frontmatter is not a mapping: {path}")
    return data, match.group(2).lstrip("\n")


def render_yaml_agent(meta: dict[str, Any], body: str, target: str) -> str:
    description = str(meta["description"])
    if target == "copilot":
        target_meta: dict[str, Any] = {
            "name": "Infrastructure PR Reviewer",
            "description": description,
            "tools": ["read", "search", "execute", "web", "github/*"],
        }
    elif target == "claude":
        target_meta = {
            "name": "infrastructure-pr-reviewer",
            "description": description,
            "tools": ["Read", "Grep", "Glob", "Bash", "WebFetch", "WebSearch", "Skill"],
            "disallowedTools": ["Write", "Edit", "MultiEdit", "NotebookEdit"],
            "permissionMode": "plan",
        }
    elif target == "gemini":
        target_meta = {
            "name": "infrastructure-pr-reviewer",
            "description": description,
            "kind": "local",
            "tools": [
                "list_directory",
                "read_file",
                "glob",
                "grep_search",
                "run_shell_command",
                "google_web_search",
                "activate_skill",
            ],
            "max_turns": 70,
            "timeout_mins": 30,
        }
    else:
        raise ValueError(f"unsupported YAML Agent target: {target}")
    dumped = yaml.safe_dump(target_meta, sort_keys=False, allow_unicode=False).rstrip()
    return f"---\n{dumped}\n---\n\n{body.rstrip()}\n"


def toml_string(value: str) -> str:
    return value.replace("\\", "\\\\").replace('"', '\\"').replace("\n", " ")


def render_codex_agent(meta: dict[str, Any], body: str) -> str:
    if '"""' in body:
        raise ValueError("canonical Agent contains a TOML multiline-string delimiter")
    return (
        'name = "infrastructure-pr-reviewer"\n'
        f'description = "{toml_string(str(meta["description"]))}"\n'
        'sandbox_mode = "read-only"\n'
        'developer_instructions = """\n'
        f"{body.rstrip()}\n"
        '"""\n'
    )


def copy_skills(destination: Path) -> None:
    destination.mkdir(parents=True, exist_ok=True)
    for skill in sorted(SKILLS.iterdir()):
        if skill.is_dir():
            shutil.copytree(skill, destination / skill.name)


def copy_copilot_collateral(target_root: Path) -> None:
    instruction_target = target_root / ".github/instructions/infrastructure-review.instructions.md"
    instruction_target.parent.mkdir(parents=True, exist_ok=True)
    shutil.copy2(CANONICAL_INSTRUCTION, instruction_target)
    shutil.copytree(COPILOT_SETUP, target_root / "setup")


def write_install(target_root: Path, target: str) -> None:
    if target == "copilot":
        text = """# Install GitHub Copilot Target

Copy `.github/` into the repository root. Then:

1. Merge `setup/copilot-instructions-snippet.md` into the existing `.github/copilot-instructions.md` without overwriting unrelated instructions.
2. Adjust `.github/instructions/infrastructure-review.instructions.md` path globs for the repository.
3. Optionally merge the supplied pull-request template into the repository's template.
4. Complete `setup/repository-enforcement-checklist.md` for rulesets, required checks, CODEOWNERS, protected environments, approvals, and concurrency.
5. Enable and test Copilot code review with seeded infrastructure defects.

The generated Agent and Skills are adapters. Edit `.apm/` in the canonical source package, then rebuild.
"""
    elif target == "claude":
        text = """# Install Claude Code Target

Copy `.claude/` into the repository root. The Agent runs in plan mode, denies write/edit tools, and activates Skills only when their stack is present. Confirm project MCP permissions remain read-only for review tasks.

Edit `.apm/` in the canonical source package, then rebuild rather than editing generated files.
"""
    elif target == "codex":
        text = """# Install OpenAI Codex Target

Copy `.codex/` and `.agents/` into the repository root. The Agent uses a read-only sandbox. Review project-level MCP configuration separately because transformed or inherited tool access can exceed the Agent's intended review posture.

Edit `.apm/` in the canonical source package, then rebuild rather than editing generated files.
"""
    elif target == "gemini":
        text = """# Install Gemini CLI Target

Copy `.gemini/` and `.agents/` into the repository root. The Agent receives read/search/shell/web capabilities plus `activate_skill`, with no write tools in its allowlist. Review project MCP access and shell confirmation policy before use.

This native Gemini adapter is generated explicitly because APM support for Gemini Agent deployment may lag Gemini CLI's native subagent capability.
"""
    else:
        raise ValueError(target)
    (target_root / "INSTALL.md").write_text(text, encoding="utf-8")


def generate(selected: list[str]) -> None:
    meta, body = parse_frontmatter(CANONICAL_AGENT)
    DIST.mkdir(parents=True, exist_ok=True)

    for target in selected:
        target_root = DIST / target
        if target_root.exists():
            shutil.rmtree(target_root)
        target_root.mkdir(parents=True)

        if target == "copilot":
            agent_path = target_root / ".github/agents/infrastructure-pr-reviewer.agent.md"
            skill_path = target_root / ".github/skills"
            content = render_yaml_agent(meta, body, target)
            copy_copilot_collateral(target_root)
        elif target == "claude":
            agent_path = target_root / ".claude/agents/infrastructure-pr-reviewer.md"
            skill_path = target_root / ".claude/skills"
            content = render_yaml_agent(meta, body, target)
        elif target == "codex":
            agent_path = target_root / ".codex/agents/infrastructure-pr-reviewer.toml"
            skill_path = target_root / ".agents/skills"
            content = render_codex_agent(meta, body)
        elif target == "gemini":
            agent_path = target_root / ".gemini/agents/infrastructure-pr-reviewer.md"
            skill_path = target_root / ".agents/skills"
            content = render_yaml_agent(meta, body, target)
        else:
            raise ValueError(f"unsupported target: {target}")

        agent_path.parent.mkdir(parents=True, exist_ok=True)
        agent_path.write_text(content, encoding="utf-8")
        copy_skills(skill_path)
        write_install(target_root, target)
        print(f"generated {target}: {target_root}")

    codex_path = DIST / "codex/.codex/agents/infrastructure-pr-reviewer.toml"
    if codex_path.exists():
        with codex_path.open("rb") as handle:
            tomllib.load(handle)


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument(
        "--target",
        action="append",
        choices=TARGETS,
        help="Generate one target; repeat for multiple targets. Default: all.",
    )
    args = parser.parse_args()
    generate(args.target or list(TARGETS))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
