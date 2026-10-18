#!/usr/bin/env python3
"""Create an exhaustive changed-line manifest from a Git diff.

This dependency-free helper inventories additions, deletions, renames, mode
changes, and binary-only changes so a reviewer can maintain complete coverage.
It never executes deployment tooling and writes nothing unless --output is supplied.
"""

from __future__ import annotations

import argparse
import json
import os
import re
import shlex
import subprocess
import sys
from dataclasses import asdict, dataclass
from pathlib import Path
from typing import Iterable


HUNK_RE = re.compile(
    r"^@@ -(\d+)(?:,(\d+))? \+(\d+)(?:,(\d+))? @@(?: ?(.*))?$"
)


@dataclass
class ChangedLine:
    kind: str
    old_line: int | None
    new_line: int | None
    text: str


@dataclass
class ChangedFile:
    path: str
    old_path: str | None
    status: str
    lines: list[ChangedLine]


def run_git(args: list[str], cwd: Path) -> str:
    result = subprocess.run(
        ["git", *args],
        cwd=cwd,
        check=False,
        text=True,
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE,
    )
    if result.returncode != 0:
        message = result.stderr.strip() or result.stdout.strip() or "git command failed"
        raise RuntimeError(message)
    return result.stdout


def ref_exists(ref: str, cwd: Path) -> bool:
    result = subprocess.run(
        ["git", "rev-parse", "--verify", "--quiet", ref],
        cwd=cwd,
        check=False,
        stdout=subprocess.DEVNULL,
        stderr=subprocess.DEVNULL,
    )
    return result.returncode == 0


def resolve_base(explicit: str | None, cwd: Path) -> str:
    if explicit:
        if not ref_exists(explicit, cwd):
            raise RuntimeError(f"Base revision does not exist: {explicit}")
        return explicit

    candidates: list[str] = []
    for env_name in ("GITHUB_BASE_SHA", "SYSTEM_PULLREQUEST_TARGETCOMMITID"):
        value = os.environ.get(env_name)
        if value:
            candidates.append(value)

    base_ref = os.environ.get("GITHUB_BASE_REF")
    if base_ref:
        candidates.extend([f"origin/{base_ref}", base_ref])

    candidates.extend(["origin/main", "origin/master", "main", "master", "HEAD^"])

    for candidate in candidates:
        if not ref_exists(candidate, cwd):
            continue
        if candidate in {"origin/main", "origin/master", "main", "master"}:
            try:
                merge_base = run_git(["merge-base", "HEAD", candidate], cwd).strip()
                if merge_base:
                    return merge_base
            except RuntimeError:
                pass
        return candidate

    raise RuntimeError(
        "Unable to determine a base revision. Pass --base explicitly or fetch the PR base branch."
    )


def decode_quoted_path(value: str) -> str:
    value = value.strip()
    if value.startswith('"') and value.endswith('"'):
        try:
            decoded = json.loads(value)
            if isinstance(decoded, str):
                return decoded
        except json.JSONDecodeError:
            pass
    return value


def parse_path(header_value: str, strip_prefix: bool = True) -> str | None:
    value = decode_quoted_path(header_value)
    if value == "/dev/null":
        return None
    if strip_prefix and (value.startswith("a/") or value.startswith("b/")):
        return value[2:]
    return value


def parse_diff_header_paths(raw_line: str) -> tuple[str | None, str | None]:
    value = raw_line[len("diff --git ") :]
    try:
        parts = shlex.split(value)
    except ValueError:
        parts = value.split(maxsplit=1)
    if len(parts) != 2:
        return None, None
    return parse_path(parts[0]), parse_path(parts[1])


def infer_status(old_path: str | None, new_path: str | None) -> str:
    if old_path is None:
        return "added"
    if new_path is None:
        return "deleted"
    if old_path != new_path:
        return "renamed"
    return "modified"


def parse_diff(diff_text: str) -> list[ChangedFile]:
    files: list[ChangedFile] = []
    current: ChangedFile | None = None
    pending_old_path: str | None = None
    old_line = 0
    new_line = 0
    in_hunk = False

    def finish_current() -> None:
        nonlocal current
        if current is not None:
            files.append(current)
            current = None

    for raw_line in diff_text.splitlines():
        if raw_line.startswith("diff --git "):
            finish_current()
            old_path, new_path = parse_diff_header_paths(raw_line)
            chosen_path = new_path or old_path or "unknown"
            current = ChangedFile(
                path=chosen_path,
                old_path=(old_path if old_path != new_path else None),
                status=infer_status(old_path, new_path),
                lines=[],
            )
            pending_old_path = old_path
            in_hunk = False
            continue

        if current is None:
            continue

        if raw_line.startswith("new file mode "):
            current.status = "added"
            current.old_path = None
            continue

        if raw_line.startswith("deleted file mode "):
            current.status = "deleted"
            continue

        if raw_line.startswith("old mode "):
            if current.status == "modified":
                current.status = "mode-changed"
            continue

        if raw_line.startswith("rename from "):
            old_path = parse_path(raw_line[len("rename from ") :], strip_prefix=False)
            current.old_path = old_path
            current.status = "renamed"
            continue

        if raw_line.startswith("rename to "):
            new_path = parse_path(raw_line[len("rename to ") :], strip_prefix=False)
            if new_path:
                current.path = new_path
            current.status = "renamed"
            continue

        if raw_line.startswith("--- "):
            pending_old_path = parse_path(raw_line[4:])
            continue

        if raw_line.startswith("+++ "):
            new_path = parse_path(raw_line[4:])
            old_path = pending_old_path
            current.path = new_path or old_path or current.path
            current.old_path = old_path if old_path != new_path and old_path else None
            current.status = infer_status(old_path, new_path)
            continue

        hunk_match = HUNK_RE.match(raw_line)
        if hunk_match:
            old_line = int(hunk_match.group(1))
            new_line = int(hunk_match.group(3))
            in_hunk = True
            continue

        if not in_hunk:
            continue

        if raw_line.startswith("+") and not raw_line.startswith("+++"):
            current.lines.append(ChangedLine("added", None, new_line, raw_line[1:]))
            new_line += 1
        elif raw_line.startswith("-") and not raw_line.startswith("---"):
            current.lines.append(ChangedLine("deleted", old_line, None, raw_line[1:]))
            old_line += 1
        elif raw_line.startswith(" "):
            old_line += 1
            new_line += 1
        elif raw_line.startswith("\\ No newline at end of file"):
            continue
        else:
            in_hunk = False

    finish_current()
    return files


def escape_markdown(value: str) -> str:
    return value.replace("|", "\\|").replace("`", "\\`")


def render_markdown(base: str, head: str, files: Iterable[ChangedFile]) -> str:
    file_list = list(files)
    additions = sum(
        1 for item in file_list for line in item.lines if line.kind == "added"
    )
    deletions = sum(
        1 for item in file_list for line in item.lines if line.kind == "deleted"
    )

    output = [
        "# Changed-line review manifest",
        "",
        f"- Base: `{escape_markdown(base)}`",
        f"- Head: `{escape_markdown(head)}`",
        f"- Changed files: {len(file_list)}",
        f"- Added lines: {additions}",
        f"- Deleted lines: {deletions}",
        "",
        "Use this as an internal coverage ledger. Do not treat line inventory as review evidence.",
        "",
    ]

    for item in file_list:
        heading = f"## {escape_markdown(item.path)} ({item.status})"
        if item.old_path:
            heading += f" from {escape_markdown(item.old_path)}"
        output.extend([heading, ""])

        if not item.lines:
            output.extend(
                [
                    "_No textual line changes. Review the rename, mode, or binary change itself._",
                    "",
                ]
            )
            continue

        output.extend(
            [
                "| Kind | Old line | New line | Text |",
                "|---|---:|---:|---|",
            ]
        )
        for line in item.lines:
            old_value = "" if line.old_line is None else str(line.old_line)
            new_value = "" if line.new_line is None else str(line.new_line)
            text = escape_markdown(line.text)
            output.append(
                f"| {line.kind} | {old_value} | {new_value} | `{text}` |"
            )
        output.append("")

    return "\n".join(output).rstrip() + "\n"


def render_json(base: str, head: str, files: Iterable[ChangedFile]) -> str:
    payload = {
        "base": base,
        "head": head,
        "files": [asdict(item) for item in files],
    }
    return json.dumps(payload, indent=2, sort_keys=False) + "\n"


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(
        description="Create an added/deleted line and file-change manifest from a Git diff."
    )
    parser.add_argument("--base", help="Base revision. Auto-detected when omitted.")
    parser.add_argument("--head", default="HEAD", help="Head revision. Default: HEAD")
    parser.add_argument(
        "--repo",
        default=".",
        help="Repository working directory. Default: current directory",
    )
    parser.add_argument(
        "--format",
        choices=("markdown", "json"),
        default="markdown",
        help="Output format. Default: markdown",
    )
    parser.add_argument("--output", help="Write to this path instead of stdout.")
    return parser.parse_args()


def main() -> int:
    args = parse_args()
    cwd = Path(args.repo).resolve()

    try:
        run_git(["rev-parse", "--show-toplevel"], cwd)
        base = resolve_base(args.base, cwd)
        if not ref_exists(args.head, cwd):
            raise RuntimeError(f"Head revision does not exist: {args.head}")
        diff_text = run_git(
            [
                "diff",
                "--no-color",
                "--no-ext-diff",
                "--find-renames",
                "--find-copies",
                "--unified=0",
                f"{base}...{args.head}",
                "--",
            ],
            cwd,
        )
        files = parse_diff(diff_text)
        rendered = (
            render_json(base, args.head, files)
            if args.format == "json"
            else render_markdown(base, args.head, files)
        )
    except RuntimeError as exc:
        print(f"change_manifest.py: {exc}", file=sys.stderr)
        return 2

    if args.output:
        output_path = Path(args.output)
        output_path.parent.mkdir(parents=True, exist_ok=True)
        output_path.write_text(rendered, encoding="utf-8")
    else:
        sys.stdout.write(rendered)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
