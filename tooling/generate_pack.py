#!/usr/bin/env python3
"""Generate an agent pack from reference material with AI, stage it, check it, and promote it on approval.

Commands:
  generate  Build a staging workspace, run headless Claude Code against tooling/generation-brief.md, then run
            the independent checks. The pack lands in staging/<name>/out/<name>-pack, never in the repository.
  check     Re-run the independent checks on a staging workspace and rewrite its STAGING_REPORT.md.
  promote   Copy a staged pack into the repository root. Refuses unless the last check passed. This is the
            approval step: run it only after reviewing STAGING_REPORT.md and the pack.

Independent checks (the generator's own claims are not trusted):
  1. tooling/validate_pack.py --install-check (APM install for every target)
  2. tooling/skill_coverage.py --check
  3. leakage: the exemplar's pack name, agent names and contract name must not appear in the generated pack;
     skill names shared with the exemplar are listed for review
  4. verbatim copying: long lines identical to the reference material are counted per file

Usage:
  python tooling/generate_pack.py generate --reference <folder> --name <slug> --role "<role>" \
      --source <url> --license <spdx|unknown> [--model M] [--max-turns 300] [--timeout-min 120]
  python tooling/generate_pack.py check staging/<name>
  python tooling/generate_pack.py status staging/<name>      # % complete from a 20-item milestone checklist
  python tooling/generate_pack.py publish staging/<name>     # open a pull request; merging it is the approval
  python tooling/generate_pack.py promote staging/<name> [--replace]   # local alternative to publish
"""
from __future__ import annotations

import argparse
import datetime as dt
import json
import re
import shutil
import string
import subprocess
import sys
import time
from pathlib import Path

REPO = Path(__file__).resolve().parents[1]
TOOLING = REPO / "tooling"
STAGING = REPO / "staging"
DEFAULT_STANDARD = REPO.parent / "Proj-Code_Workflow" / "docs"
DEFAULT_EXEMPLAR = REPO / "python-distinguished-engineer-pack"
SLUG = re.compile(r"^[a-z0-9][a-z0-9-]*[a-z0-9]$")
ALLOWED_TOOLS = ["Read", "Glob", "Grep", "Write", "Edit", "MultiEdit", "TodoWrite",
                 "Bash(python tooling/validate_pack.py:*)", "Bash(python tooling/validate_pack.py *)",
                 "Bash(python tooling/skill_coverage.py:*)", "Bash(python tooling/skill_coverage.py *)"]
DISALLOWED_TOOLS = ["WebFetch", "WebSearch", "Agent", "Task"]
MIT = ("MIT License\n\nCopyright (c) 2026 saulpatinojr\n\nPermission is hereby granted, free of charge, to any person obtaining a copy "
       "of this software and associated documentation files (the \"Software\"), to deal in the Software without restriction, including "
       "without limitation the rights to use, copy, modify, merge, publish, distribute, sublicense, and/or sell copies of the Software, and "
       "to permit persons to whom the Software is furnished to do so, subject to the following conditions:\n\nThe above copyright notice and "
       "this permission notice shall be included in all copies or substantial portions of the Software.\n\nTHE SOFTWARE IS PROVIDED \"AS IS\", "
       "WITHOUT WARRANTY OF ANY KIND, EXPRESS OR IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY, FITNESS FOR A "
       "PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER "
       "LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM, OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR "
       "OTHER DEALINGS IN THE SOFTWARE.\n")


def copytree(src: Path, dst: Path) -> None:
    shutil.copytree(src, dst, ignore=shutil.ignore_patterns("__pycache__", "*.pyc", "dist", ".git", "~OPEN", "*.url"))


def prepare(args: argparse.Namespace) -> Path:
    if not SLUG.match(args.name):
        raise SystemExit(f"invalid pack name: {args.name}")
    ws = STAGING / args.name
    if ws.exists():
        raise SystemExit(f"staging workspace exists: {ws} (remove it or choose another name)")
    reference, standard, exemplar = Path(args.reference).resolve(), Path(args.standard).resolve(), Path(args.exemplar).resolve()
    for path, what in ((reference, "reference"), (standard / "agent-pack-prompt.md", "master prompt"),
                       (standard / "client-locations.md", "client locations"), (exemplar / "apm.yml", "exemplar")):
        if not path.exists():
            raise SystemExit(f"{what} not found: {path}")
    pack_dir = f"{args.name}-pack"
    (ws / "standard").mkdir(parents=True)
    shutil.copy(standard / "agent-pack-prompt.md", ws / "standard" / "agent-pack-prompt.md")
    shutil.copy(standard / "client-locations.md", ws / "standard" / "client-locations.md")
    copytree(exemplar, ws / "exemplar")
    for name in ("VALIDATION_REPORT.md", "AGENT-PACK-README.md"):
        (ws / "exemplar" / name).unlink(missing_ok=True)
    copytree(reference, ws / "reference")
    (ws / "tooling").mkdir()
    for name in ("validate_pack.py", "skill_coverage.py"):
        shutil.copy(TOOLING / name, ws / "tooling" / name)
    out = ws / "out" / pack_dir
    out.mkdir(parents=True)
    (out / "LICENSE").write_text(MIT, encoding="utf-8")
    shutil.copy(standard / "agent-pack-prompt.md", out / "PORTABLE_AGENT_SKILL_PACK_AUTHORING_PROMPT.md")
    brief = string.Template((TOOLING / "generation-brief.md").read_text(encoding="utf-8")).substitute(
        role=args.role, name=args.name, pack_dir=pack_dir, source=args.source, license=args.license)
    (ws / "BRIEF.md").write_text(brief, encoding="utf-8")
    meta = {"name": args.name, "role": args.role, "source": args.source, "license": args.license,
            "reference": str(reference), "exemplar": str(exemplar), "created": dt.datetime.now().isoformat(timespec="seconds")}
    (ws / "workspace.json").write_text(json.dumps(meta, indent=2) + "\n", encoding="utf-8")
    return ws


FILL_ARTIFACTS = {"examples": "examples/", "templates": "templates/", ".apm/prompts": ".apm/prompts/"}
PROTECTED = (".apm/agents/", ".apm/skills/", ".apm/instructions/", "apm.yml", "compatibility/tool-permissions.yml",
             "LICENSE", "PORTABLE_AGENT_SKILL_PACK_AUTHORING_PROMPT.md")


def missing_artifacts(pack: Path) -> list[str]:
    return [rel for rel in FILL_ARTIFACTS if not ((pack / rel).is_dir() and any(f.is_file() for f in (pack / rel).rglob("*")))]


def file_hashes(root: Path) -> dict[str, str]:
    import hashlib
    return {p.relative_to(root).as_posix(): hashlib.sha256(p.read_bytes()).hexdigest()
            for p in root.rglob("*") if p.is_file() and not ({"dist", "__pycache__"} & set(p.relative_to(root).parts))}


def prepare_fill(args: argparse.Namespace) -> Path:
    pack = (REPO / args.pack).resolve() if not Path(args.pack).is_absolute() else Path(args.pack)
    if not (pack / "apm.yml").is_file():
        raise SystemExit(f"not a pack: {pack}")
    name = pack.name.removesuffix("-pack")
    missing = missing_artifacts(pack)
    if not missing:
        raise SystemExit(f"{pack.name} is not missing any fillable artifact")
    ws = STAGING / f"{name}-fill"
    if ws.exists():
        raise SystemExit(f"staging workspace exists: {ws}")
    standard, exemplar = Path(args.standard).resolve(), Path(args.exemplar).resolve()
    (ws / "standard").mkdir(parents=True)
    shutil.copy(standard / "agent-pack-prompt.md", ws / "standard" / "agent-pack-prompt.md")
    shutil.copy(standard / "client-locations.md", ws / "standard" / "client-locations.md")
    copytree(exemplar, ws / "exemplar")
    for extra in ("VALIDATION_REPORT.md", "AGENT-PACK-README.md"):
        (ws / "exemplar" / extra).unlink(missing_ok=True)
    (ws / "tooling").mkdir()
    for tool in ("validate_pack.py", "skill_coverage.py"):
        shutil.copy(TOOLING / tool, ws / "tooling" / tool)
    out = ws / "out" / pack.name
    shutil.copytree(pack, out, ignore=shutil.ignore_patterns("dist", "__pycache__", "*.pyc"))
    for stale in ("VALIDATION_REPORT.md", "AGENT-PACK-README.md"):  # regenerated by the engine; a stale PASS would mislead status
        (out / stale).unlink(missing_ok=True)
    shutil.copy(standard / "agent-pack-prompt.md", out / "PORTABLE_AGENT_SKILL_PACK_AUTHORING_PROMPT.md")
    baseline = file_hashes(out)
    descriptions = {"examples": "`examples/`: worked walkthroughs of the pack's main workflows",
                    "templates": "`templates/`: reusable documents the skills tell the agent to produce",
                    ".apm/prompts": "`.apm/prompts/`: one prompt per primary workflow"}
    brief = string.Template((TOOLING / "fill-brief.md").read_text(encoding="utf-8")).substitute(
        pack_dir=pack.name, missing="\n".join(f"- {descriptions[m]}" for m in missing), date=dt.date.today().isoformat())
    (ws / "BRIEF.md").write_text(brief, encoding="utf-8")
    meta = {"mode": "fill", "name": name, "role": f"gap fill of {pack.name}", "source": f"existing pack {pack.name}",
            "license": "n/a", "reference": "", "exemplar": str(exemplar), "missing": missing, "baseline": baseline,
            "created": dt.datetime.now().isoformat(timespec="seconds")}
    (ws / "workspace.json").write_text(json.dumps(meta, indent=2) + "\n", encoding="utf-8")
    return ws


def bump_minor(pack: Path) -> str:
    path = pack / "apm.yml"
    text = path.read_text(encoding="utf-8")
    m = re.search(r"^version:\s*(\d+)\.(\d+)\.(\d+)\s*$", text, re.M)
    if not m:
        return "?"
    new = f"{m.group(1)}.{int(m.group(2)) + 1}.0"
    path.write_text(text[: m.start()] + f"version: {new}" + text[m.end():], encoding="utf-8")
    return new


def record_version_bump(ws: Path, meta: dict) -> str:
    """Bump the pack's minor version and record the new apm.yml as the baseline, so the protected-file guard
    does not mistake the engine's own change for the generator's."""
    pack = ws / "out" / f"{meta['name']}-pack"
    version = bump_minor(pack)
    meta["baseline"]["apm.yml"] = file_hashes(pack)["apm.yml"]
    meta["version_bumped_by_engine"] = version
    (ws / "workspace.json").write_text(json.dumps(meta, indent=2) + "\n", encoding="utf-8")
    return version


def run_generator(ws: Path, model: str | None, max_turns: int, timeout_min: int) -> dict:
    claude = shutil.which("claude")
    if not claude:
        raise SystemExit("claude CLI not found on PATH")
    cmd = [claude, "-p", "--output-format", "json", "--permission-mode", "dontAsk", "--strict-mcp-config",
           "--no-session-persistence", "--max-turns", str(max_turns), "--allowedTools", *ALLOWED_TOOLS,
           "--disallowedTools", *DISALLOWED_TOOLS]
    if model:
        cmd += ["--model", model]
    started = time.time()
    try:
        proc = subprocess.run(cmd, cwd=ws, input=(ws / "BRIEF.md").read_text(encoding="utf-8"), capture_output=True,
                              text=True, encoding="utf-8", timeout=timeout_min * 60)
        stdout, stderr, code, timed_out = proc.stdout, proc.stderr, proc.returncode, False
    except subprocess.TimeoutExpired as exc:
        stdout = exc.stdout.decode("utf-8", "replace") if isinstance(exc.stdout, bytes) else (exc.stdout or "")
        stderr, code, timed_out = "timed out", None, True
    result: dict = {"exit_code": code, "timed_out": timed_out, "seconds": round(time.time() - started)}
    try:
        result["claude"] = json.loads(stdout)
    except json.JSONDecodeError:
        result["stdout_tail"] = stdout[-4000:]
    result["stderr_tail"] = (stderr or "")[-2000:]
    (ws / "generation-log.json").write_text(json.dumps(result, indent=2) + "\n", encoding="utf-8")
    return result


def identity_terms(exemplar: Path) -> tuple[set[str], set[str]]:
    hard, skills = set(), set()
    for line in (exemplar / "apm.yml").read_text(encoding="utf-8").splitlines():
        if line.startswith("name:"):
            hard.add(line.split(":", 1)[1].strip())
    hard |= {p.name[: -len(".agent.md")] for p in (exemplar / ".apm" / "agents").glob("*.agent.md")}
    hard |= {p.name[: -len(".instructions.md")] for p in (exemplar / ".apm" / "instructions").glob("*contract*.instructions.md")}
    skills = {p.name for p in (exemplar / ".apm" / "skills").iterdir() if p.is_dir()}
    return hard, skills


def normalized_lines(root: Path, min_len: int = 80) -> set[str]:
    out = set()
    for path in root.rglob("*"):
        if path.is_file() and path.suffix in (".md", ".txt", ".yml", ".yaml", ".json"):
            for line in path.read_text(encoding="utf-8", errors="replace").splitlines():
                norm = " ".join(line.split()).lower()
                if len(norm) >= min_len:
                    out.add(norm)
    return out


def check(ws: Path) -> dict:
    meta = json.loads((ws / "workspace.json").read_text(encoding="utf-8"))
    pack = ws / "out" / f"{meta['name']}-pack"
    report: dict = {"pack": str(pack), "checked": dt.datetime.now().isoformat(timespec="seconds"), "mode": meta.get("mode", "generate")}
    if not (pack / "apm.yml").is_file():
        report["status"] = "FAIL"
        report["reason"] = "generator produced no apm.yml"
        write_report(ws, meta, report)
        return report
    shutil.rmtree(pack / "dist", ignore_errors=True)
    proc = subprocess.run([sys.executable, str(TOOLING / "validate_pack.py"), str(pack), "--install-check"], capture_output=True, text=True)
    report["validator"] = {"exit_code": proc.returncode, "summary": proc.stdout.strip().splitlines()[0] if proc.stdout.strip() else "",
                           "failures": [line.strip() for line in proc.stdout.splitlines() if line.startswith("  FAIL")]}
    proc = subprocess.run([sys.executable, str(TOOLING / "skill_coverage.py"), str(pack), "--check"], capture_output=True, text=True)
    report["skill_coverage_current"] = proc.returncode == 0

    hard, exemplar_skills = identity_terms(ws / "exemplar")
    leaks: dict[str, list[str]] = {}
    for path in pack.rglob("*"):
        if path.is_file() and path.name != "PORTABLE_AGENT_SKILL_PACK_AUTHORING_PROMPT.md" and path.suffix in (".md", ".yml", ".yaml", ".json", ".py", ".toml"):
            text = path.read_text(encoding="utf-8", errors="replace")
            hits = sorted(t for t in hard if re.search(rf"(?<![\w-]){re.escape(t)}(?![\w-])", text))
            if hits:
                leaks[path.relative_to(pack).as_posix()] = hits
    report["leakage"] = leaks
    shared = sorted(exemplar_skills & {p.name for p in (pack / ".apm" / "skills").iterdir() if p.is_dir()}) if (pack / ".apm" / "skills").is_dir() else []
    report["skills_shared_with_exemplar"] = shared

    if meta.get("mode") == "fill":
        now_hashes = file_hashes(pack)
        base = meta.get("baseline", {})
        touched = sorted(rel for rel in set(base) | set(now_hashes) if base.get(rel) != now_hashes.get(rel)
                         and rel.startswith(PROTECTED) and rel != "VALIDATION_REPORT.md")
        report["protected_changes"] = touched
        report["still_missing"] = missing_artifacts(pack)
        report["added_files"] = sorted(set(now_hashes) - set(base))
    ref_lines = normalized_lines(ws / "reference") if (ws / "reference").is_dir() else set()
    copied: dict[str, int] = {}
    for path in (pack / ".apm").rglob("*.md") if (pack / ".apm").is_dir() else []:
        n = sum(1 for line in path.read_text(encoding="utf-8", errors="replace").splitlines() if " ".join(line.split()).lower() in ref_lines)
        if n:
            copied[path.relative_to(pack).as_posix()] = n
    report["verbatim_lines_from_reference"] = copied
    report["verbatim_total"] = sum(copied.values())

    counts = {"agents": len(list((pack / ".apm" / "agents").glob("*.agent.md"))) if (pack / ".apm" / "agents").is_dir() else 0,
              "skills": len([p for p in (pack / ".apm" / "skills").iterdir() if p.is_dir()]) if (pack / ".apm" / "skills").is_dir() else 0,
              "instructions": len(list((pack / ".apm" / "instructions").glob("*.md"))) if (pack / ".apm" / "instructions").is_dir() else 0,
              "prompts": len(list((pack / ".apm" / "prompts").glob("*.md"))) if (pack / ".apm" / "prompts").is_dir() else 0,
              "files": len([p for p in pack.rglob("*") if p.is_file()])}
    report["counts"] = counts
    ok = report["validator"]["exit_code"] == 0 and report["skill_coverage_current"] and not leaks
    if meta.get("mode") == "fill":
        ok = ok and not report["protected_changes"] and not report["still_missing"]
    report["status"] = "PASS" if ok else "FAIL"
    report["needs_review"] = [f"{f}: {n} lines identical to reference" for f, n in copied.items() if n >= 5] + \
                             [f"skill shares a name with the exemplar: {s}" for s in shared]
    write_report(ws, meta, report)
    (ws / "check.json").write_text(json.dumps(report, indent=2) + "\n", encoding="utf-8")
    return report


def write_report(ws: Path, meta: dict, report: dict) -> None:
    log = json.loads((ws / "generation-log.json").read_text(encoding="utf-8")) if (ws / "generation-log.json").is_file() else {}
    c = log.get("claude", {}) if isinstance(log.get("claude"), dict) else {}
    models = ", ".join(c.get("modelUsage", {}).keys()) if isinstance(c.get("modelUsage"), dict) else ""
    lines = [f"# Staging report: {meta['name']}", "",
             f"Status: **{report.get('status')}**. Checked {report.get('checked')}.", "",
             f"- Role: {meta['role']}", f"- Reference: {meta['source']} (license: {meta['license']})",
             f"- Generator: exit {log.get('exit_code')}, {log.get('seconds', '?')} s, turns {c.get('num_turns', '?')}, "
             f"cost USD {c.get('total_cost_usd', '?')}, model {models or '?'}{', TIMED OUT' if log.get('timed_out') else ''}",
             f"- Counts: {report.get('counts', {})}", ""]
    if report.get("reason"):
        lines += [f"Reason: {report['reason']}", ""]
    v = report.get("validator", {})
    lines += ["## Independent checks", "",
              f"- Validator: {v.get('summary', 'not run')}", *[f"  - {f}" for f in v.get("failures", [])],
              f"- Skill coverage file current: {report.get('skill_coverage_current')}",
              f"- Exemplar identity leakage: {report.get('leakage') or 'none'}",
              f"- Verbatim lines from reference: {report.get('verbatim_total', 0)}"]
    if report.get("mode") == "fill":
        lines += [f"- Protected files changed (must be none): {report.get('protected_changes') or 'none'}",
                  f"- Artifacts still missing (must be none): {report.get('still_missing') or 'none'}",
                  f"- Files added: {len(report.get('added_files', []))}"]
    lines += [""]
    if report.get("needs_review"):
        lines += ["## Needs human review", ""] + [f"- {n}" for n in report["needs_review"]] + [""]
    if c.get("result"):
        lines += ["## Generator's closing summary (its claim, not evidence)", "", str(c["result"]).strip(), ""]
    lines += ["## Approve", "", f"Review `out/{meta['name']}-pack`, then run:", "",
              "```", f"python tooling/generate_pack.py promote staging/{meta['name']}", "```", ""]
    (ws / "STAGING_REPORT.md").write_text("\n".join(lines), encoding="utf-8")


def promote(ws: Path, replace: bool) -> int:
    meta = json.loads((ws / "workspace.json").read_text(encoding="utf-8"))
    report = json.loads((ws / "check.json").read_text(encoding="utf-8")) if (ws / "check.json").is_file() else {}
    if report.get("status") != "PASS":
        print(f"refusing to promote: last check status is {report.get('status')}; run check first")
        return 1
    src = ws / "out" / f"{meta['name']}-pack"
    dst = REPO / src.name
    if dst.exists() and not replace:
        print(f"refusing to promote: {dst} exists (use --replace)")
        return 1
    if dst.exists():
        shutil.rmtree(dst)
    shutil.copytree(src, dst, ignore=shutil.ignore_patterns("dist", "__pycache__", "*.pyc"))
    print(f"promoted {src.name} into {REPO}; review with git diff, then commit")
    return 0


def milestones(ws: Path) -> list[tuple[str, bool]]:
    """Twenty equally weighted milestones: what a finished pack contains, then validation, then the engine checks."""
    meta = json.loads((ws / "workspace.json").read_text(encoding="utf-8"))
    pack = ws / "out" / f"{meta['name']}-pack"
    apm = pack / ".apm"

    def any_in(folder: Path, pattern: str) -> bool:
        return folder.is_dir() and any(folder.glob(pattern))

    report = pack / "VALIDATION_REPORT.md"
    report_text = report.read_text(encoding="utf-8", errors="replace") if report.is_file() else ""
    if meta.get("mode") == "fill":
        items = [(f"{rel} written", (pack / rel).is_dir() and any(f.is_file() for f in (pack / rel).rglob("*"))) for rel in meta["missing"]]
        items += [("validator has run", report.is_file()), ("validator reports PASS", "Status: PASS" in report_text),
                  ("engine checks complete", (ws / "STAGING_REPORT.md").is_file())]
        return items
    primary = any("user-invocable: true" in a.read_text(encoding="utf-8", errors="replace")
                  for a in (apm / "agents").glob("*.agent.md")) if (apm / "agents").is_dir() else False
    return [
        ("apm.yml", (pack / "apm.yml").is_file()),
        ("an agent", any_in(apm / "agents", "*.agent.md")),
        ("the user-invocable primary agent", primary),
        ("a skill", any_in(apm / "skills", "*/SKILL.md")),
        ("the contract instruction", any_in(apm / "instructions", "*contract*.instructions.md")),
        ("a prompt", any_in(apm / "prompts", "*.prompt.md")),
        ("tool-permissions.yml", (pack / "compatibility" / "tool-permissions.yml").is_file()),
        ("DESCRIPTION.md", (pack / "DESCRIPTION.md").is_file()),
        ("README.md", (pack / "README.md").is_file()),
        ("docs", any_in(pack / "docs", "*.md")),
        ("examples", any_in(pack / "examples", "*")),
        ("templates", any_in(pack / "templates", "*")),
        ("hooks/README.md", (pack / "hooks" / "README.md").is_file()),
        ("capability-coverage.yml", (pack / "tests" / "capability-coverage.yml").is_file()),
        ("trigger-cases.yml", (pack / "tests" / "trigger-cases.yml").is_file()),
        ("report-contract.yml", (pack / "tests" / "report-contract.yml").is_file()),
        ("skill-coverage.yml", (pack / "tests" / "skill-coverage.yml").is_file()),
        ("validator has run", report.is_file()),
        ("validator reports PASS", "Status: PASS" in report_text),
        ("engine checks complete", (ws / "STAGING_REPORT.md").is_file()),
    ]


def status(ws: Path) -> int:
    meta = json.loads((ws / "workspace.json").read_text(encoding="utf-8"))
    pack = ws / "out" / f"{meta['name']}-pack"
    items = milestones(ws)
    done = sum(1 for _, ok in items if ok)
    created = dt.datetime.fromisoformat(meta["created"])
    elapsed = dt.datetime.now() - created
    files = [p for p in pack.rglob("*") if p.is_file()] if pack.is_dir() else []
    size_kb = round(sum(p.stat().st_size for p in files) / 1024)
    apm = pack / ".apm"
    def count(folder: Path, pattern: str) -> int:
        return len(list(folder.glob(pattern))) if folder.is_dir() else 0
    print(f"{meta['name']}: {done * 100 // len(items)}% complete ({done} of {len(items)} milestones), "
          f"elapsed {int(elapsed.total_seconds() // 60)} min {int(elapsed.total_seconds() % 60)} s")
    print(f"files {len(files)} ({size_kb} KB): agents {count(apm / 'agents', '*.agent.md')}, skills {count(apm / 'skills', '*/SKILL.md')}, "
          f"prompts {count(apm / 'prompts', '*.prompt.md')}, instructions {count(apm / 'instructions', '*.instructions.md')}")
    pending = [label for label, ok in items if not ok]
    print("next: " + (", ".join(pending[:4]) if pending else "nothing; finished"))
    for path in sorted(files, key=lambda p: p.stat().st_mtime)[-3:]:
        print(f"  {dt.datetime.fromtimestamp(path.stat().st_mtime).strftime('%H:%M:%S')}  {path.relative_to(pack).as_posix()}")
    if (ws / "STAGING_REPORT.md").is_file():
        print("FINISHED: see " + str(ws / "STAGING_REPORT.md"))
    return 0


COMMIT_TRAILER = "Co-Authored-By: Claude Opus 5.5 <noreply@anthropic.com>"
PR_TRAILER = "\U0001F916 Generated with [Claude Code](https://claude.com/claude-code)"


def git(*args: str, cwd: Path = REPO, check: bool = True) -> subprocess.CompletedProcess:
    proc = subprocess.run(["git", "-c", "core.safecrlf=false", *args], cwd=cwd, capture_output=True, text=True)
    if check and proc.returncode != 0:
        raise SystemExit(f"git {' '.join(args)} failed:\n{proc.stdout}\n{proc.stderr}")
    return proc


def publish(ws: Path, base: str = "main") -> int:
    """Open (or update) a pull request that adds the staged pack. Merging the pull request is the approval."""
    import tempfile
    meta = json.loads((ws / "workspace.json").read_text(encoding="utf-8"))
    report = json.loads((ws / "check.json").read_text(encoding="utf-8")) if (ws / "check.json").is_file() else {}
    if report.get("status") != "PASS":
        print(f"refusing to publish: last check status is {report.get('status')}; run check first")
        return 1
    gh = shutil.which("gh")
    if not gh:
        raise SystemExit("gh CLI not found on PATH")
    name = meta["name"]
    src = ws / "out" / f"{name}-pack"
    subprocess.run([sys.executable, str(TOOLING / "build_pack.py"), str(src)], check=True, capture_output=True)
    shutil.rmtree(src / "dist", ignore_errors=True)
    branch = f"pack/{name}-fill" if meta.get("mode") == "fill" else f"pack/{name}"
    git("fetch", "origin", base)
    tmp = Path(tempfile.mkdtemp(prefix=f"pack-pr-{name}-"))
    tree = tmp / "tree"
    try:
        git("worktree", "add", "-B", branch, str(tree), f"origin/{base}")
        dst = tree / src.name
        if dst.exists():
            shutil.rmtree(dst)
        shutil.copytree(src, dst, ignore=shutil.ignore_patterns("dist", "__pycache__", "*.pyc"))
        git("add", "-A", src.name, cwd=tree)
        if not git("status", "--porcelain", cwd=tree).stdout.strip():
            print("nothing to publish: the branch already holds this pack")
            return 0
        version = next((line.split(":", 1)[1].strip() for line in (src / "apm.yml").read_text(encoding="utf-8").splitlines()
                        if line.startswith("version:")), "?")
        counts = report.get("counts", {})
        verb = "Fill missing artifacts in" if meta.get("mode") == "fill" else "Add"
        message = (f"{verb} {name} {version} (generated)\n\n"
                   f"Generated by tooling/generate_pack.py from: {meta['source']} (license: {meta['license']}).\n"
                   f"{counts.get('agents')} agents, {counts.get('skills')} skills, {counts.get('prompts')} prompts, {counts.get('files')} files.\n"
                   f"Engine checks: {report.get('validator', {}).get('summary', '')}; leakage none; "
                   f"{report.get('verbatim_total', 0)} lines identical to the reference.\n\n{COMMIT_TRAILER}\n")
        subprocess.run(["git", "-c", "core.safecrlf=false", "commit", "-q", "-F", "-"], cwd=tree, input=message, text=True, check=True)
        git("push", "--force-with-lease", "-u", "origin", branch, cwd=tree)
    finally:
        git("worktree", "remove", "--force", str(tree), check=False)
        shutil.rmtree(tmp, ignore_errors=True)
    body = (ws / "STAGING_REPORT.md").read_text(encoding="utf-8")
    approve = ("\n\n## Approve\n\nMerging this pull request is the approval: it adds the pack to main. "
               "CI validates the pack on this branch.\n\n")
    body = body.split("## Approve", 1)[0].rstrip() + approve + PR_TRAILER + "\n"
    body_file = ws / "PR_BODY.md"
    body_file.write_text(body, encoding="utf-8")
    existing = subprocess.run([gh, "pr", "list", "--head", branch, "--state", "open", "--json", "url", "--jq", ".[0].url"],
                              cwd=REPO, capture_output=True, text=True).stdout.strip()
    if existing:
        subprocess.run([gh, "pr", "edit", existing, "--body-file", str(body_file)], cwd=REPO, check=True, capture_output=True)
        print(f"updated pull request: {existing}")
    else:
        title = f"Fill missing artifacts in {name} pack" if meta.get("mode") == "fill" else f"Add {name} pack (generated)"
        proc = subprocess.run([gh, "pr", "create", "--base", base, "--head", branch, "--title", title,
                               "--body-file", str(body_file)], cwd=REPO, capture_output=True, text=True)
        if proc.returncode != 0:
            raise SystemExit(f"gh pr create failed:\n{proc.stdout}\n{proc.stderr}")
        print(f"opened pull request: {proc.stdout.strip()}")
    return 0


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    sub = parser.add_subparsers(dest="command", required=True)
    g = sub.add_parser("generate")
    g.add_argument("--reference", required=True)
    g.add_argument("--name", required=True)
    g.add_argument("--role", required=True)
    g.add_argument("--source", required=True)
    g.add_argument("--license", required=True)
    g.add_argument("--standard", default=str(DEFAULT_STANDARD), help="folder holding agent-pack-prompt.md and client-locations.md")
    g.add_argument("--exemplar", default=str(DEFAULT_EXEMPLAR))
    g.add_argument("--model")
    g.add_argument("--max-turns", type=int, default=300)
    g.add_argument("--timeout-min", type=int, default=120)
    g.add_argument("--prepare-only", action="store_true", help="build the workspace and brief without running the generator")
    f = sub.add_parser("fill", help="complete an existing pack's missing examples, templates and prompts")
    f.add_argument("pack", help="pack folder, for example terraform-expert-engineer-pack")
    f.add_argument("--standard", default=str(DEFAULT_STANDARD))
    f.add_argument("--exemplar", default=str(DEFAULT_EXEMPLAR))
    f.add_argument("--model")
    f.add_argument("--max-turns", type=int, default=200)
    f.add_argument("--timeout-min", type=int, default=90)
    f.add_argument("--prepare-only", action="store_true")
    c = sub.add_parser("check")
    c.add_argument("workspace")
    pub = sub.add_parser("publish")
    pub.add_argument("workspace")
    pub.add_argument("--base", default="main")
    s = sub.add_parser("status")
    s.add_argument("workspace")
    p = sub.add_parser("promote")
    p.add_argument("workspace")
    p.add_argument("--replace", action="store_true")
    args = parser.parse_args()
    if args.command == "generate":
        ws = prepare(args)
        print(f"workspace: {ws}")
        if args.prepare_only:
            return 0
        result = run_generator(ws, args.model, args.max_turns, args.timeout_min)
        print(f"generator: exit {result['exit_code']}, {result['seconds']} s{' (timed out)' if result['timed_out'] else ''}")
        report = check(ws)
        print(f"check: {report['status']}; see {ws / 'STAGING_REPORT.md'}")
        return 0 if report["status"] == "PASS" else 1
    if args.command == "fill":
        ws = prepare_fill(args)
        print(f"workspace: {ws} (missing: {', '.join(json.loads((ws / 'workspace.json').read_text(encoding='utf-8'))['missing'])})")
        if args.prepare_only:
            return 0
        result = run_generator(ws, args.model, args.max_turns, args.timeout_min)
        print(f"generator: exit {result['exit_code']}, {result['seconds']} s{' (timed out)' if result['timed_out'] else ''}")
        report = check(ws)
        if report["status"] == "PASS":
            meta = json.loads((ws / "workspace.json").read_text(encoding="utf-8"))
            version = record_version_bump(ws, meta)
            report = check(ws)
            print(f"version bumped to {version}")
        print(f"check: {report['status']}; see {ws / 'STAGING_REPORT.md'}")
        return 0 if report["status"] == "PASS" else 1
    if args.command == "publish":
        return publish(Path(args.workspace).resolve(), args.base)
    if args.command == "status":
        return status(Path(args.workspace).resolve())
    if args.command == "check":
        report = check(Path(args.workspace).resolve())
        print(f"check: {report['status']}")
        return 0 if report["status"] == "PASS" else 1
    return promote(Path(args.workspace).resolve(), args.replace)


if __name__ == "__main__":
    raise SystemExit(main())
