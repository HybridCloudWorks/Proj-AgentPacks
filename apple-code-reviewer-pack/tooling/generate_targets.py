#!/usr/bin/env python3
"""Generate native Apple Code Reviewer agent and skill layouts for supported clients."""

from __future__ import annotations

import argparse
import re
import shutil
import tomllib
from pathlib import Path

import yaml

ROOT = Path(__file__).resolve().parents[1]
CANONICAL_AGENT = ROOT / ".apm/agents/apple-code-reviewer.agent.md"
SKILLS = ROOT / ".apm/skills"
DIST = ROOT / "dist/targets"


def parse_markdown_frontmatter(path: Path) -> tuple[dict, str]:
    text = path.read_text(encoding="utf-8")
    match = re.match(r"^---\n(.*?)\n---\n?(.*)$", text, re.DOTALL)
    if not match:
        raise ValueError(f"missing YAML frontmatter: {path}")
    data = yaml.safe_load(match.group(1))
    if not isinstance(data, dict):
        raise ValueError(f"frontmatter is not a mapping: {path}")
    return data, match.group(2).lstrip("\n")


def yaml_agent(frontmatter: dict, body: str, target: str) -> str:
    description = frontmatter["description"]
    if target == "copilot":
        meta = {
            "name": "Apple Code Reviewer",
            "description": description,
            "tools": ["read", "search", "execute", "web", "github/*"],
        }
    elif target == "claude":
        meta = {
            "name": "apple-code-reviewer",
            "description": description,
            "tools": ["Read", "Grep", "Glob", "Bash", "WebFetch", "WebSearch", "Skill"],
            "disallowedTools": ["Write", "Edit", "MultiEdit", "NotebookEdit"],
            "permissionMode": "plan",
        }
    elif target == "gemini":
        meta = {
            "name": "apple-code-reviewer",
            "description": description,
            "kind": "local",
            "tools": [
                "list_directory", "read_file", "glob", "grep_search",
                "run_shell_command", "google_web_search", "activate_skill",
            ],
            "max_turns": 50,
            "timeout_mins": 30,
        }
    else:
        raise ValueError(target)
    dumped = yaml.safe_dump(meta, sort_keys=False, allow_unicode=False).rstrip()
    return f"---\n{dumped}\n---\n\n{body.rstrip()}\n"


def toml_string(value: str) -> str:
    return value.replace("\\", "\\\\").replace('"', '\\"').replace("\n", " ")


def codex_agent(frontmatter: dict, body: str) -> str:
    if '"""' in body:
        raise ValueError("canonical agent contains TOML triple-quote delimiter")
    return (
        f'name = "apple-code-reviewer"\n'
        f'description = "{toml_string(frontmatter["description"])}"\n'
        'sandbox_mode = "read-only"\n'
        'developer_instructions = """\n'
        f'{body.rstrip()}\n'
        '"""\n'
    )


def copy_skills(destination: Path) -> None:
    destination.mkdir(parents=True, exist_ok=True)
    for skill in sorted(SKILLS.iterdir()):
        if skill.is_dir():
            shutil.copytree(skill, destination / skill.name)


def write_install(target_root: Path, target: str) -> None:
    (target_root / "INSTALL.md").write_text(
        f"# Install {target.title()} Target\n\n"
        "Copy the hidden directories in this folder into the repository root. "
        "Generated files are read-only review adapters; edit the canonical `.apm/` source instead.\n",
        encoding="utf-8",
    )


def generate(selected: list[str]) -> None:
    frontmatter, body = parse_markdown_frontmatter(CANONICAL_AGENT)
    DIST.mkdir(parents=True, exist_ok=True)

    for target in selected:
        target_root = DIST / target
        if target_root.exists():
            shutil.rmtree(target_root)
        target_root.mkdir(parents=True)

        if target == "copilot":
            agent_path = target_root / ".github/agents/apple-code-reviewer.agent.md"
            skill_path = target_root / ".agents/skills"
            content = yaml_agent(frontmatter, body, target)
        elif target == "claude":
            agent_path = target_root / ".claude/agents/apple-code-reviewer.md"
            skill_path = target_root / ".claude/skills"
            content = yaml_agent(frontmatter, body, target)
        elif target == "codex":
            agent_path = target_root / ".codex/agents/apple-code-reviewer.toml"
            skill_path = target_root / ".agents/skills"
            content = codex_agent(frontmatter, body)
        elif target == "gemini":
            agent_path = target_root / ".gemini/agents/apple-code-reviewer.md"
            skill_path = target_root / ".agents/skills"
            content = yaml_agent(frontmatter, body, target)
        else:
            raise ValueError(f"unsupported target: {target}")

        agent_path.parent.mkdir(parents=True, exist_ok=True)
        agent_path.write_text(content, encoding="utf-8")
        copy_skills(skill_path)
        write_install(target_root, target)
        print(f"generated {target}: {target_root}")

    # Parse generated Codex TOML as a syntax check when present.
    codex = DIST / "codex/.codex/agents/apple-code-reviewer.toml"
    if codex.exists():
        with codex.open("rb") as fh:
            tomllib.load(fh)


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument(
        "--target", action="append", choices=("copilot", "claude", "codex", "gemini"),
        help="Generate one target; repeat for multiple. Default: all.",
    )
    args = parser.parse_args()
    generate(args.target or ["copilot", "claude", "codex", "gemini"])
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
