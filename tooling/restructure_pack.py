#!/usr/bin/env python3
"""Restructure a prompt-v1 pack (folder or full-pack .zip) into the v2.2 layout, deterministically.

What it does (every step is reversible from the source, which is never modified):
  1. unzip (if a .zip was given) into <dest>
  2. apm.yml: keep name, description, author, license; set version (minor bump), repository, keywords, targets
  3. agents: drop `tools` (APM copies it verbatim and Kiro rejects foreign names) and record the intent in
     compatibility/tool-permissions.yml; everything else in the frontmatter is kept
  4. instructions/ and prompts/ move under .apm/; instructions get a description when missing
  5. hooks/*.json become hooks/samples/*.sample.json with repository paths replaced by <PACK_HOME>
  6. remove generated and stale content: targets/, dist/, top-level vendor folders, root archives,
     __pycache__, INSTALL.md, the old catalog and validation report, per-pack copies of the shared tooling,
     tests/behavior-results.json
  7. copilot-instructions.md at the root moves to examples/repository/
  8. PORTABLE_AGENT_SKILL_PACK_AUTHORING_PROMPT.md becomes the current master prompt

What it cannot do: rewrite prose. It ends by running the shared validator and printing every content
failure, which is the list a person (or an AI reviewer) must resolve by hand.

Usage: python tooling/restructure_pack.py <source folder or zip> <dest folder> --prompt <master prompt .md>
"""
from __future__ import annotations

import argparse
import json
import re
import shutil
import subprocess
import sys
import zipfile
from pathlib import Path

HERE = Path(__file__).resolve().parent
ALIAS_INTENT = {"read": "read", "search": "read", "edit": "edit", "execute": "shell", "agent": "delegate", "web": "web", "todo": "todo"}
KEEP_MANIFEST = ("name", "description", "author", "license")
VENDOR_DIRS = ("claude-code", "gemini-cli", "github-copilot", "openai-codex", "targets", "dist")
TARGETS = ["copilot", "claude", "codex", "kiro", "gemini", "agent-skills"]


def fm_split(text: str) -> tuple[str | None, str]:
    m = re.match(r"\A---\r?\n(.*?)\r?\n---\r?\n(.*)\Z", text, re.DOTALL)
    return (m.group(1), m.group(2)) if m else (None, text)


def parse_tools(raw: str) -> list[str]:
    raw = raw.strip()
    try:
        value = json.loads(raw)
        return [str(v) for v in value] if isinstance(value, list) else [str(value)]
    except json.JSONDecodeError:
        return [t.strip().strip("'\"") for t in raw.strip("[]").split(",") if t.strip()]


def bump(version: str) -> str:
    parts = [int(x) for x in re.findall(r"\d+", version)[:3]] or [0, 0, 0]
    while len(parts) < 3:
        parts.append(0)
    return f"{parts[0]}.{parts[1] + 1}.0"


def restructure(src: Path, dest: Path, prompt: Path, repository: str, author: str) -> list[str]:
    log: list[str] = []
    if dest.exists():
        raise SystemExit(f"destination exists, refusing to overwrite: {dest}")
    if src.suffix.lower() == ".zip":
        with zipfile.ZipFile(src) as archive:
            names = archive.namelist()
            roots = {n.split("/", 1)[0] for n in names if "/" in n}
            archive.extractall(dest)
            inner = dest / next(iter(roots)) if len(roots) == 1 and not (dest / "apm.yml").is_file() else None
        if inner and (inner / "apm.yml").is_file():
            for child in list(inner.iterdir()):
                shutil.move(str(child), str(dest / child.name))
            inner.rmdir()
        log.append(f"unzipped {src.name}")
    else:
        shutil.copytree(src, dest, ignore=shutil.ignore_patterns("__pycache__", "*.pyc", "*.zip", "~OPEN"))
        log.append(f"copied {src}")
    if not (dest / "apm.yml").is_file() or not (dest / ".apm" / "agents").is_dir():
        raise SystemExit("not a prompt-v1 pack: apm.yml and .apm/agents are required")

    # manifest
    old: dict[str, str] = {}
    for line in (dest / "apm.yml").read_text(encoding="utf-8").splitlines():
        m = re.match(r"^([A-Za-z_]+):\s*(.+)$", line)
        if m and m.group(1) in KEEP_MANIFEST + ("version",):
            old[m.group(1)] = m.group(2).strip().strip("\"'")
    name = old.get("name") or dest.name.removesuffix("-pack")
    keywords = sorted({w for w in re.split(r"[^a-z0-9]+", name.lower()) if len(w) > 2})
    (dest / "apm.yml").write_text(
        f"name: {name}\nversion: {bump(old.get('version', '1.0.0'))}\ndescription: {old.get('description', name)}\n"
        f"author: {old.get('author', author)}\nlicense: {old.get('license', 'MIT')}\nrepository: {repository}\n"
        f"keywords: [{', '.join(keywords)}]\ntargets:\n" + "".join(f"  - {t}\n" for t in TARGETS), encoding="utf-8")
    log.append(f"apm.yml rewritten: {name} {bump(old.get('version', '1.0.0'))}")

    # agents
    perm: dict[str, list[str]] = {}
    for path in sorted((dest / ".apm" / "agents").glob("*.agent.md")):
        fm, body = fm_split(path.read_text(encoding="utf-8"))
        if fm is None:
            log.append(f"WARNING agent without frontmatter: {path.name}")
            continue
        kept, tools = [], None
        for line in fm.splitlines():
            if re.match(r"^tools\s*:", line):
                tools = parse_tools(line.split(":", 1)[1])
                continue
            kept.append(line)
        agent_name = next((l.split(":", 1)[1].strip() for l in kept if l.startswith("name:")), path.name[: -len(".agent.md")])
        intents = sorted({ALIAS_INTENT.get(t.lower(), "mcp" if "/" in t else t) for t in (tools or [])}) or ["inherit"]
        perm[agent_name] = intents
        path.write_text("---\n" + "\n".join(kept) + "\n---\n" + body, encoding="utf-8")
        log.append(f"agent {agent_name}: tools {tools} -> intent {intents}")
    comp = dest / "compatibility"
    comp.mkdir(exist_ok=True)
    lines = ["# Declared tool permissions per agent (source of truth for vendor-specific generation).",
             "# APM copies the agents' frontmatter verbatim and does not translate tool names, so the",
             "# canonical agents omit `tools` and inherit the host's tools. Installers that generate",
             "# vendor files themselves map these intents: read, edit, shell, web, delegate, todo, mcp.",
             "version: 1", "agents:"]
    for agent_name, intents in perm.items():
        lines += [f"  {agent_name}:", f"    intent: [{', '.join(intents)}]"]
    (comp / "tool-permissions.yml").write_text("\n".join(lines) + "\n", encoding="utf-8")

    # instructions and prompts
    inst_dst = dest / ".apm" / "instructions"
    inst_dst.mkdir(exist_ok=True)
    for path in sorted((dest / "instructions").glob("*.instructions.md")) if (dest / "instructions").is_dir() else []:
        fm, body = fm_split(path.read_text(encoding="utf-8"))
        fm = fm or 'applyTo: "**"'
        if "description:" not in fm:
            h1 = re.search(r"^#\s+(.+)$", body, re.M)
            first = re.search(r"^(?!#)(\S.{20,})$", body, re.M)
            desc = (first.group(1) if first else (h1.group(1) if h1 else path.stem)).strip().rstrip(".")[:200]
            fm = f'description: "{desc.replace(chr(34), chr(39))}"\n' + fm
        (inst_dst / path.name).write_text("---\n" + fm.strip() + "\n---\n" + body, encoding="utf-8")
        log.append(f"instruction {path.name} -> .apm/instructions")
    if (dest / "instructions").is_dir():
        shutil.rmtree(dest / "instructions")
    pr_dst = dest / ".apm" / "prompts"
    pr_dst.mkdir(exist_ok=True)
    if (dest / "prompts").is_dir():
        for path in sorted((dest / "prompts").glob("*.prompt.md")):
            shutil.move(str(path), str(pr_dst / path.name))
            log.append(f"prompt {path.name} -> .apm/prompts")
        shutil.rmtree(dest / "prompts")

    # hooks
    hooks = dest / "hooks"
    hooks.mkdir(exist_ok=True)
    samples = hooks / "samples"
    for path in list(hooks.glob("*.json")) + (list((dest / ".apm" / "hooks").glob("*.json")) if (dest / ".apm" / "hooks").is_dir() else []):
        samples.mkdir(exist_ok=True)
        text = path.read_text(encoding="utf-8")
        text = re.sub(r"\.github/hooks/scripts/", "<PACK_HOME>/hooks/", text)
        text = text.replace('{\n  "version"', '{\n  "_comment": "Sample only, not installed by APM. Replace <PACK_HOME> with the installed pack path; the Code Workflow installer does this.",\n  "version"', 1)
        (samples / f"{path.stem}.sample.json").write_text(text, encoding="utf-8")
        path.unlink()
        log.append(f"hook {path.name} -> hooks/samples (sample, not deployed)")
    if (dest / ".apm" / "hooks").is_dir():
        shutil.rmtree(dest / ".apm" / "hooks")
    if not (hooks / "README.md").is_file():
        (hooks / "README.md").write_text("# Hooks\n\nThis pack ships no native hook definitions. APM copies hook commands verbatim and never deploys the scripts they call. Any sample under `samples/` is for review; the Code Workflow installer wires hooks to its own pack home.\n", encoding="utf-8")

    # stale and generated content
    for rel in VENDOR_DIRS + ("INSTALL.md", "AGENT-PACK-README.md", "VALIDATION_REPORT.md", "tooling/validate_pack.py",
                              "tooling/build_pack.py", "tests/behavior-results.json"):
        p = dest / rel
        if p.is_dir():
            shutil.rmtree(p)
            log.append(f"removed {rel}/")
        elif p.is_file():
            p.unlink()
            log.append(f"removed {rel}")
    for p in list(dest.rglob("__pycache__")):
        shutil.rmtree(p, ignore_errors=True)
    for p in list(dest.rglob("*.pyc")) + list(dest.glob("*.zip")):
        p.unlink()
    for rel in ("examples", "templates", "docs", "tests", "tooling"):
        (dest / rel).mkdir(exist_ok=True)
    if (dest / "copilot-instructions.md").is_file():
        (dest / "examples" / "repository").mkdir(parents=True, exist_ok=True)
        shutil.move(str(dest / "copilot-instructions.md"), str(dest / "examples" / "repository" / "copilot-instructions.md"))
        log.append("copilot-instructions.md -> examples/repository/")
    shutil.copy(prompt, dest / "PORTABLE_AGENT_SKILL_PACK_AUTHORING_PROMPT.md")
    log.append("authoring prompt replaced with the current master prompt")
    return log


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    parser.add_argument("source")
    parser.add_argument("dest")
    parser.add_argument("--prompt", required=True, help="current master prompt file")
    parser.add_argument("--repository", default="https://github.com/saulpatinojr/Proj-Agent_Packs")
    parser.add_argument("--author", default="saulpatinojr")
    args = parser.parse_args()
    log = restructure(Path(args.source).resolve(), Path(args.dest).resolve(), Path(args.prompt).resolve(), args.repository, args.author)
    print("\n".join(log))
    print("\n== validator (content failures below need a person or an AI reviewer) ==")
    proc = subprocess.run([sys.executable, "-I", str(HERE / "validate_pack.py"), args.dest, "--no-report"], text=True)
    return proc.returncode


if __name__ == "__main__":
    raise SystemExit(main())
