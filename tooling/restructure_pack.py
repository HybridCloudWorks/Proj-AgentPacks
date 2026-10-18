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


def restructure(src: Path, dest: Path, prompt: Path, repository: str, author: str, primary: str | None = None, drop: tuple[str, ...] = ()) -> list[str]:
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
    name = (old.get("name") or dest.name).removesuffix("-pack")
    keywords = sorted({w for w in re.split(r"[^a-z0-9]+", name.lower()) if len(w) > 2})
    (dest / "apm.yml").write_text(
        f"name: {name}\nversion: {bump(old.get('version', '1.0.0'))}\ndescription: {old.get('description', name)}\n"
        f"author: {old.get('author', author)}\nlicense: {old.get('license', 'MIT')}\nrepository: {repository}\n"
        f"keywords: [{', '.join(keywords)}]\ntargets:\n" + "".join(f"  - {t}\n" for t in TARGETS), encoding="utf-8")
    log.append(f"apm.yml rewritten: {name} {bump(old.get('version', '1.0.0'))}")

    # agents
    for agent_name in drop:
        victim = dest / ".apm" / "agents" / f"{agent_name}.agent.md"
        if victim.is_file():
            victim.unlink()
            log.append(f"dropped leaked agent {agent_name}")
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
        if primary:
            kept = [l for l in kept if not re.match(r"^user-invocable\s*:", l)]
            kept.append(f"user-invocable: {'true' if agent_name == primary else 'false'}")
        intents = sorted({ALIAS_INTENT.get(t.lower(), "mcp" if ("/" in t or "mcp" in t.lower()) else t) for t in (tools or [])}) or ["inherit"]
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

    for path in sorted(pr_dst.glob("*.prompt.md")):
        fm, body = fm_split(path.read_text(encoding="utf-8"))
        if fm is None or "description:" not in fm:
            h1 = re.search(r"^#\s+(.+)$", body, re.M)
            desc = (h1.group(1).strip() if h1 else path.name[: -len(".prompt.md")].replace("-", " ").capitalize())
            fm = f'description: "{desc.replace(chr(34), chr(39))}"' + ("\n" + fm if fm else "")
            path.write_text("---\n" + fm.strip() + "\n---\n" + body, encoding="utf-8")
            log.append(f"prompt {path.name}: description added from heading")

    # always-on contract instruction from the pack's own contract documents
    contract_name = f"{name}-contract"
    folded: list[str] = []
    if not any(inst_dst.glob("*contract*.instructions.md")):
        sections = []
        docs_dir = dest / "docs"
        for doc in sorted(docs_dir.glob("*.md")) if docs_dir.is_dir() else []:
            if re.search(r"CONTRACT|APPROVAL|HANDOFF|GOVERNANCE", doc.name):
                body = re.sub(r"^#\s+.*\n", "", doc.read_text(encoding="utf-8"), count=1).strip()
                body = re.sub(r"`?docs/([A-Za-z_-]+)\.md`?", lambda m: "the pack's " + m.group(1).replace("_", " ").lower() + " document (for maintainers, not installed)", body)
                body = re.sub(r"`?templates/([\w.-]+)`?", lambda m: "the pack's " + m.group(1) + " template (for maintainers, not installed)", body)
                title = doc.stem.replace("_", " ").capitalize()
                sections.append(f"## {title}\n\n{body}")
                folded.append(doc.name)
        rc_path = dest / "tests" / "report-contract.yml"
        if rc_path.is_file():
            rc_text = rc_path.read_text(encoding="utf-8")
            rc = None
            try:
                rc = json.loads(rc_text)
            except json.JSONDecodeError:
                try:
                    import yaml  # type: ignore
                    rc = yaml.safe_load(rc_text)
                except Exception:
                    rc = None
            if isinstance(rc, dict):
                parts = []
                for key, value in rc.items():
                    label = str(key).replace("_", " ")
                    if isinstance(value, list) and all(isinstance(v, str) for v in value):
                        parts.append(f"{label.capitalize()}: " + ", ".join(value) + ".")
                    elif isinstance(value, str):
                        parts.append(f"{label.capitalize()}: {value.rstrip('.')}.")
                    elif isinstance(value, dict):
                        inner = "; ".join(f"{k}: {', '.join(v) if isinstance(v, list) else v}" for k, v in value.items())
                        parts.append(f"{label.capitalize()}: {inner}.")
                if parts:
                    sections.append("## Completion report\n\n" + "\n\n".join(parts) +
                                    "\n\nNever describe an unexecuted check as passed; state what was not verified.")
        title = name.replace("-", " ")
        (inst_dst / f"{contract_name}.instructions.md").write_text(
            f'---\ndescription: "Approval, handoff and completion-report rules for the {title} pack. Always on; the agents, skills and prompts in this pack refer to it."\napplyTo: "**"\n---\n'
            f"# {title.capitalize()} contract\n\nThis instruction is installed with the pack so that every agent, skill and prompt can rely on it. "
            f"It replaces references to pack documents that are not installed.\n\n" +
            ("\n\n".join(sections) if sections else "Work read-only by default. Ask for authority before consequential actions. Report exact checks run, results, and what was not verified.") + "\n",
            encoding="utf-8")
        log.append(f"contract instruction synthesized ({contract_name}; folded: {', '.join(folded) or 'report-contract only'})")

    # installed content: references to folded docs become the contract instruction; other docs and templates
    # referenced by a skill are copied into that skill so the reference resolves after install
    for path in sorted((dest / ".apm").rglob("*.md")):
        text = path.read_text(encoding="utf-8")
        original = text
        for doc_name in folded:
            text = re.sub(r"`?docs/" + re.escape(doc_name) + r"`?", f"the installed `{contract_name}` instruction", text)
        skill_dir = path.parent if path.parent.parent.name == "skills" else (path.parent.parent if path.parent.parent.parent.name == "skills" else None)
        if skill_dir is not None:
            for m in re.finditer(r"`?(docs|templates)/([\w.-]+\.(?:md|py|json|yml))`?", text):
                source = dest / m.group(1) / m.group(2)
                if source.is_file():
                    shutil.copy(source, skill_dir / m.group(2))
                    text = text.replace(m.group(0), f"`{m.group(2)}`")
                    log.append(f"{path.relative_to(dest).as_posix()}: {m.group(1)}/{m.group(2)} copied into the skill")
        if text != original:
            path.write_text(text, encoding="utf-8")
            log.append(f"rewrote references in {path.relative_to(dest).as_posix()}")

    # pack docs: known phrases from the old layout
    phrase_map = [
        (r"four vendor packages", "vendor packages generated at build time"),
        (r"four vendor targets", "vendor files generated at install time"),
        (r"generated targets", "generated vendor files"),
        (r"[Tt]arget `INSTALL\.md` files", "generated vendor files"),
        (r"`?dist/targets/[^`\s]*`?", "`dist/`"),
        (r"[Vv]endor directories under `?[^`\s]*targets/`? are generated compatibility outputs and must not[^.]*\.", "Vendor files are generated from `.apm/` at install time and are never edited by hand."),
    ]
    for rel in ["README.md", "DESCRIPTION.md"] + [p.relative_to(dest).as_posix() for p in list((dest / "docs").glob("*.md")) + list((dest / "compatibility").glob("*.yml"))]:
        path = dest / rel
        if not path.is_file() or path.name == "DESIGN_DECISIONS.md":
            continue
        text = path.read_text(encoding="utf-8")
        original = text
        for pattern, repl in phrase_map:
            text = re.sub(pattern, repl, text)
        kept_lines = []
        for line in text.splitlines():
            if re.search(r"(?<![\w-])targets/", line):
                kept_lines.append("Vendor files are generated from `.apm/` by `apm install` or the Code Workflow installer; nothing is copied by hand.")
                log.append(f"{rel}: replaced a line that described hand-built targets")
            else:
                kept_lines.append(line)
        text = "\n".join(kept_lines) + ("\n" if text.endswith("\n") else "")
        if text != original:
            path.write_text(text, encoding="utf-8")
            log.append(f"{rel}: old-layout phrases replaced")

    # DESCRIPTION.md and LICENSE when missing
    if not (dest / "DESCRIPTION.md").is_file():
        readme = (dest / "README.md").read_text(encoding="utf-8") if (dest / "README.md").is_file() else ""
        paras = [p.strip() for p in re.split(r"\n\s*\n", re.sub(r"^#.*$", "", readme, flags=re.M)) if len(p.strip()) > 60]
        (dest / "DESCRIPTION.md").write_text(f"# {name.replace('-', ' ').title()}\n\n" + ("\n\n".join(paras[:2]) if paras else old.get("description", name)) + "\n", encoding="utf-8")
        log.append("DESCRIPTION.md synthesized from README (review it)")
    if not (dest / "LICENSE").is_file():
        (dest / "LICENSE").write_text(f"MIT License\n\nCopyright (c) 2026 {old.get('author', author)}\n\nPermission is hereby granted, free of charge, to any person obtaining a copy of this software and associated documentation files (the \"Software\"), to deal in the Software without restriction, including without limitation the rights to use, copy, modify, merge, publish, distribute, sublicense, and/or sell copies of the Software, and to permit persons to whom the Software is furnished to do so, subject to the following conditions:\n\nThe above copyright notice and this permission notice shall be included in all copies or substantial portions of the Software.\n\nTHE SOFTWARE IS PROVIDED \"AS IS\", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY, FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM, OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE SOFTWARE.\n", encoding="utf-8")
        log.append("LICENSE (MIT) added")

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
    subprocess.run([sys.executable, "-I", str(HERE / "skill_coverage.py"), str(dest)], check=True, capture_output=True)
    log.append("tests/skill-coverage.yml generated from the skills")
    return log


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    parser.add_argument("source")
    parser.add_argument("dest")
    parser.add_argument("--prompt", required=True, help="current master prompt file")
    parser.add_argument("--repository", default="https://github.com/saulpatinojr/Proj-Agent_Packs")
    parser.add_argument("--author", default="saulpatinojr")
    parser.add_argument("--primary", help="agent name to mark user-invocable; every other agent becomes a hidden specialist")
    parser.add_argument("--drop-agent", action="append", default=[], help="remove this leaked agent (repeatable)")
    args = parser.parse_args()
    log = restructure(Path(args.source).resolve(), Path(args.dest).resolve(), Path(args.prompt).resolve(), args.repository, args.author,
                      args.primary, tuple(args.drop_agent))
    print("\n".join(log))
    print("\n== validator (content failures below need a person or an AI reviewer) ==")
    proc = subprocess.run([sys.executable, str(HERE / "validate_pack.py"), args.dest, "--no-report"], text=True)  # not -I: PyYAML lives in user site
    return proc.returncode


if __name__ == "__main__":
    raise SystemExit(main())
