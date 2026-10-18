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
  python tooling/generate_pack.py promote staging/<name> [--replace]
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
    report: dict = {"pack": str(pack), "checked": dt.datetime.now().isoformat(timespec="seconds")}
    if not (pack / "apm.yml").is_file():
        report["status"] = "FAIL"
        report["reason"] = "generator produced no apm.yml"
        write_report(ws, meta, report)
        return report
    shutil.rmtree(pack / "dist", ignore_errors=True)
    proc = subprocess.run([sys.executable, str(TOOLING / "validate_pack.py"), str(pack), "--install-check"], capture_output=True, text=True)
    report["validator"] = {"exit_code": proc.returncode, "summary": proc.stdout.strip().splitlines()[0] if proc.stdout.strip() else "",
                           "failures": [l.strip() for l in proc.stdout.splitlines() if l.startswith("  FAIL")]}
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

    ref_lines = normalized_lines(ws / "reference")
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
              f"- Verbatim lines from reference: {report.get('verbatim_total', 0)}", ""]
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
    count = lambda folder, pattern: len(list(folder.glob(pattern))) if folder.is_dir() else 0
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
    c = sub.add_parser("check")
    c.add_argument("workspace")
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
    if args.command == "status":
        return status(Path(args.workspace).resolve())
    if args.command == "check":
        report = check(Path(args.workspace).resolve())
        print(f"check: {report['status']}")
        return 0 if report["status"] == "PASS" else 1
    return promote(Path(args.workspace).resolve(), args.replace)


if __name__ == "__main__":
    raise SystemExit(main())
