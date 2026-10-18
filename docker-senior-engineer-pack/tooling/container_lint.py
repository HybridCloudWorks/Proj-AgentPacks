"""Static, heuristic checks for Dockerfiles and Compose files.

Reads text only: never builds, runs, pulls or contacts anything, never follows symlinks out of the
root, and never echoes the value of anything that looks like a secret. It complements, and does not
replace, `docker build --check`, hadolint and `docker compose config`.

Usage: python tooling/container_lint.py [PATH ...] [--format text|json] [--fail-on SEVERITY]
Exit 0 when no finding reaches --fail-on (default High), 1 otherwise, 2 on usage errors.
"""
from __future__ import annotations

import argparse
import json
import os
import re
import sys
from dataclasses import asdict, dataclass
from pathlib import Path

SEVERITIES = ("Blocker", "High", "Medium", "Low", "Suggestion", "Question")
MAX_FILE_BYTES = 1_048_576
MAX_FILES = 500
SKIP_DIRS = {".git", ".hg", ".svn", "node_modules", "vendor", ".venv", "venv", "dist", "build", "target",
             "__pycache__", ".terraform", ".tox", ".mypy_cache", ".pytest_cache"}
KNOWN_INSTRUCTIONS = {"FROM", "RUN", "CMD", "LABEL", "MAINTAINER", "EXPOSE", "ENV", "ADD", "COPY", "ENTRYPOINT",
                      "VOLUME", "USER", "WORKDIR", "ARG", "ONBUILD", "STOPSIGNAL", "HEALTHCHECK", "SHELL"}
SECRET_NAME = re.compile(r"PASSWORD|PASSWD|SECRET|TOKEN|API_?KEY|PRIVATE_?KEY|ACCESS_?KEY|CREDENTIAL", re.I)
# Names that point at a secret rather than holding one.
SECRET_REFERENCE_SUFFIX = re.compile(r"_(FILE|PATH|DIR|URL|URI|ENDPOINT|NAME|ID)$", re.I)
ROOT_USERS = {"root", "0", "0:0", "root:root", "root:0", "0:root"}


@dataclass(frozen=True)
class Finding:
    rule: str
    severity: str
    file: str
    line: int
    message: str
    fix: str


def classify(name: str) -> str | None:
    lower = name.lower()
    if lower == ".dockerignore" or lower.endswith(".dockerignore"):
        return "ignore"
    if re.fullmatch(r"docker-bake(\.[\w-]+)?\.(hcl|json)", lower):
        return "bake"
    if re.fullmatch(r"(docker-)?compose(\.[\w-]+)?\.ya?ml", lower) or re.search(r"\.compose\.ya?ml$", lower):
        return "compose"
    if re.fullmatch(r"(dockerfile|containerfile)(\.[\w.-]+)?", lower) or lower.endswith((".dockerfile", ".containerfile")):
        return "dockerfile"
    return None


def discover(root: Path) -> dict[str, object]:
    """Inventory container files under root without reading them. Symlinks and skipped folders are ignored."""
    found: dict[str, list[Path]] = {"dockerfile": [], "compose": [], "bake": [], "ignore": []}
    count, truncated = 0, False
    real_root = root.resolve()
    for current, dirs, files in os.walk(real_root):
        dirs[:] = sorted(d for d in dirs if d not in SKIP_DIRS and not (Path(current) / d).is_symlink())
        for name in sorted(files):
            kind = classify(name)
            path = Path(current) / name
            if kind is None or path.is_symlink():
                continue
            if count >= MAX_FILES:
                truncated = True
                break
            found[kind].append(path)
            count += 1
        if truncated:
            break
    return {**found, "truncated": truncated}


def logical_lines(text: str) -> list[tuple[int, str]]:
    """Join continuation lines, drop comments and heredoc bodies; return (first line number, text)."""
    raw_lines = text.splitlines()
    escape = "\\"
    for raw in raw_lines:
        directive = re.match(r"^#\s*([A-Za-z]+)\s*=\s*(\S+)\s*$", raw)
        if not directive:
            break
        if directive.group(1).lower() == "escape" and directive.group(2) in ("\\", "`"):
            escape = directive.group(2)
    result: list[tuple[int, str]] = []
    buffer: list[str] = []
    start = 0
    heredoc: str | None = None
    for number, raw in enumerate(raw_lines, 1):
        if heredoc is not None:
            if raw.strip() == heredoc:
                heredoc = None
            continue
        stripped = raw.strip()
        if not stripped or stripped.startswith("#"):
            continue
        if not buffer:
            start = number
        if raw.rstrip().endswith(escape):
            buffer.append(raw.rstrip()[:-1].strip())
            continue
        buffer.append(stripped)
        logical = " ".join(part for part in buffer if part)
        buffer = []
        result.append((start, logical))
        marker = re.search(r"(?<!<)<<-?\s*[\"']?([A-Za-z_][A-Za-z0-9_]*)[\"']?", logical)
        if marker and re.match(r"(?i)(RUN|COPY|ADD)\s", logical):
            heredoc = marker.group(1)
    if buffer:
        result.append((start, " ".join(part for part in buffer if part)))
    return result


def _names(instruction: str, rest: str) -> list[tuple[str, bool]]:
    """Return (name, has_literal_value) pairs declared by ARG or ENV."""
    if instruction == "ENV" and "=" not in rest.split(" ", 1)[0]:
        parts = rest.split(None, 1)  # legacy form: ENV NAME value
        return [(parts[0], len(parts) > 1)] if parts else []
    pairs = []
    for token in re.findall(r"([A-Za-z_][A-Za-z0-9_]*)(=(\"[^\"]*\"|'[^']*'|\S*))?", rest):
        name, assignment, value = token
        pairs.append((name, bool(assignment) and value not in ("", '""', "''")))
    return pairs


def _substitute(image: str, args: dict[str, str]) -> str:
    def repl(match: re.Match[str]) -> str:
        name = match.group(1) or match.group(2)
        return args.get(name, match.group(0))
    return re.sub(r"\$\{([A-Za-z_][A-Za-z0-9_]*)\}|\$([A-Za-z_][A-Za-z0-9_]*)", repl, image)


def _tag(image: str) -> tuple[str | None, bool]:
    """Return (tag, has_digest). A colon in the first path segment is a registry port, not a tag."""
    has_digest = "@sha256:" in image
    name = image.split("@", 1)[0]
    last = name.rsplit("/", 1)[-1]
    return (last.rsplit(":", 1)[1] if ":" in last else None), has_digest


def _ignore_file_present(dockerfile: Path) -> bool:
    return (dockerfile.parent / ".dockerignore").is_file() or (dockerfile.parent / (dockerfile.name + ".dockerignore")).is_file()


def lint_dockerfile(path: Path, rel: str, text: str) -> list[Finding]:
    findings: list[Finding] = []

    def add(rule: str, severity: str, line: int, message: str, fix: str) -> None:
        findings.append(Finding(rule, severity, rel, line, message, fix))

    global_args: dict[str, str] = {}
    stages: list[dict[str, object]] = []
    copy_all_reported = False
    for line, logical in logical_lines(text):
        match = re.match(r"^([A-Za-z]+)\s*(.*)$", logical)
        if not match:
            continue
        instruction, rest = match.group(1).upper(), match.group(2).strip()
        if instruction not in KNOWN_INSTRUCTIONS:
            add("DF017", "Question", line, f"unknown instruction {instruction[:20]}", "Check the spelling or the frontend version.")
            continue
        if instruction == "ARG" and not stages:
            for name, default in re.findall(r"([A-Za-z_][A-Za-z0-9_]*)(?:=(\S*))?", rest):
                if default.strip("\"'"):  # an argument without a default cannot be resolved statically
                    global_args[name] = default.strip("\"'")
        if instruction == "FROM":
            tokens = [t for t in rest.split() if not t.startswith("--")]
            image = tokens[0] if tokens else ""
            alias = tokens[2].lower() if len(tokens) >= 3 and tokens[1].lower() == "as" else None
            resolved = _substitute(image, global_args)
            parent = next((s for s in stages if s["name"] == resolved.lower()), None)
            stages.append({"name": alias, "user": None, "user_line": None, "cmd_shell_line": None,
                           "parent": parent, "image": resolved, "line": line})
            if parent is not None or resolved.lower() == "scratch":
                continue
            if "$" in resolved:
                add("DF016", "Question", line, "base image depends on a build argument without a default",
                    "Give the argument a pinned default so the base can be reviewed.")
                continue
            tag, has_digest = _tag(resolved)
            if tag is None or tag == "latest":
                add("DF001", "Medium", line, f"base image {resolved.split('@')[0]} uses latest or no tag",
                    "Pin a specific version tag, and a digest where builds must be reproducible.")
            elif not has_digest:
                add("DF002", "Low", line, f"base image {resolved} is not pinned by digest",
                    "Use name:tag@sha256:... and automate digest updates.")
            continue
        stage = stages[-1] if stages else None
        if instruction in ("ARG", "ENV"):
            for name, has_value in _names(instruction, rest):
                if SECRET_NAME.search(name) and not SECRET_REFERENCE_SUFFIX.search(name):
                    where = "image history and provenance" if instruction == "ARG" else "every container and docker inspect"
                    add("DF005", "High", line, f"{instruction} {name} looks like a secret; its value reaches {where}",
                        "Use a build secret mount at build time and a runtime secret file at run time.")
        elif instruction == "USER" and stage is not None:
            stage["user"] = rest.split()[0] if rest else ""
            stage["user_line"] = line
        elif instruction in ("CMD", "ENTRYPOINT") and stage is not None:
            stage["cmd_shell_line"] = None if rest.startswith("[") else line
        elif instruction == "ADD":
            if re.search(r"\bhttps?://", rest) and "--checksum" not in rest:
                add("DF006", "Medium", line, "ADD downloads a remote file without --checksum",
                    "Add --checksum=sha256:... or download and verify explicitly.")
        elif instruction == "MAINTAINER":
            add("DF014", "Suggestion", line, "MAINTAINER is deprecated", "Use LABEL org.opencontainers.image.authors.")
        if instruction in ("COPY", "ADD") and not copy_all_reported:
            sources = [t for t in rest.split() if not t.startswith("--")][:-1]
            if any(s in (".", "./") for s in sources) and not _ignore_file_present(path):
                copy_all_reported = True
                add("DF008", "Medium", line, "copies the whole build context and no ignore file sits beside this Dockerfile",
                    "Add a .dockerignore at the context root (or <Dockerfile>.dockerignore) and copy explicit paths.")
        if instruction == "RUN":
            cache_mount = "--mount=type=cache" in rest
            if re.search(r"\b(curl|wget)\b[^|;&]*\|\s*(sudo\s+)?(ba|z|da)?sh\b", rest):
                add("DF009", "Medium", line, "pipes a download into a shell without verification",
                    "Download to a file, verify a checksum or signature, then run it.")
            if re.search(r"\bchmod\s+(-R\s+)?0?777\b", rest):
                add("DF010", "Medium", line, "sets world-writable permissions", "Grant only the owner and group that need access.")
            if re.search(r"\bsudo\b", rest):
                add("DF015", "Low", line, "uses sudo inside the build", "Run build steps as root before USER, or drop the need.")
            if re.search(r"\bapt-get\s+(-\S+\s+)*install\b", rest):
                if "/var/lib/apt/lists" not in rest and not cache_mount:
                    add("DF011", "Low", line, "apt-get install leaves package lists in the layer",
                        "Remove /var/lib/apt/lists/* in the same RUN or use cache mounts.")
                if "--no-install-recommends" not in rest:
                    add("DF012", "Suggestion", line, "apt-get install pulls recommended packages",
                        "Add --no-install-recommends.")
            if re.search(r"\bapk\s+add\b", rest) and "--no-cache" not in rest and not cache_mount:
                add("DF013", "Low", line, "apk add keeps its package cache", "Use apk add --no-cache or a cache mount.")
    if stages:
        final = stages[-1]
        user, user_line = final["user"], final["user_line"]
        ancestor = final["parent"]
        while user is None and isinstance(ancestor, dict):
            user, user_line, ancestor = ancestor["user"], ancestor["user_line"], ancestor["parent"]
        if isinstance(user, str) and user.lower() in ROOT_USERS:
            add("DF003", "High", int(user_line or final["line"]), "the final stage runs as root",
                "Set a numeric non-root USER in the runtime stage.")
        elif user is None and "nonroot" not in str(final["image"]).lower():
            add("DF004", "Medium", int(final["line"]), "the final stage sets no USER and inherits the base image's user, usually root",
                "Set a numeric non-root USER, or confirm the base image already does.")
        if final["cmd_shell_line"]:
            add("DF007", "Low", int(final["cmd_shell_line"]), "shell-form CMD or ENTRYPOINT makes a shell PID 1, which does not forward SIGTERM",
                "Use exec form, for example [\"/app/server\"].")
    return findings


def lint_compose(rel: str, text: str) -> list[Finding]:
    findings: list[Finding] = []

    def add(rule: str, severity: str, line: int, message: str, fix: str) -> None:
        findings.append(Finding(rule, severity, rel, line, message, fix))

    cap_add_indent: int | None = None
    for number, raw in enumerate(text.splitlines(), 1):
        stripped = raw.strip()
        if not stripped or stripped.startswith("#"):
            continue
        indent = len(raw) - len(raw.lstrip())
        if cap_add_indent is not None and (indent <= cap_add_indent or not stripped.startswith("-")):
            cap_add_indent = None
        if cap_add_indent is not None and re.search(r"\b(ALL|SYS_ADMIN)\b", stripped):
            add("CP004", "High", number, "adds ALL or SYS_ADMIN capabilities", "Add only the specific capability the service needs.")
        cap = re.match(r"^cap_add:\s*(.*)$", stripped)
        if cap:
            if re.search(r"\b(ALL|SYS_ADMIN)\b", cap.group(1)):
                add("CP004", "High", number, "adds ALL or SYS_ADMIN capabilities", "Add only the specific capability the service needs.")
            elif not cap.group(1):
                cap_add_indent = indent
        if indent == 0 and re.match(r"^version\s*:", raw):
            add("CP005", "Suggestion", number, "the top-level version key is obsolete in the Compose Specification", "Remove it.")
        if re.match(r"^privileged:\s*[\"']?true\b", stripped):
            add("CP001", "High", number, "runs a privileged container", "Remove privileged and grant specific capabilities or devices.")
        if re.search(r"docker\.sock", stripped):
            add("CP002", "High", number, "mounts the Docker socket, which gives the container control of the host",
                "Remove the mount or use a restricted API proxy after a security review.")
        if re.match(r"^(network_mode|pid|ipc|userns_mode):\s*[\"']?host\b", stripped):
            add("CP003", "Medium", number, "shares a host namespace", "Use project networks and the default namespaces.")
        if re.search(r"(seccomp|apparmor)[:=]\s*unconfined|label[:=]\s*disable", stripped):
            add("CP008", "High", number, "disables a security profile", "Keep the default profile or supply a custom one.")
        image = re.match(r"^image:\s*[\"']?([^\s\"'#]+)", stripped)
        if image and "$" not in image.group(1):
            tag, _ = _tag(image.group(1))
            if tag is None or tag == "latest":
                add("CP007", "Medium", number, f"image {image.group(1).split('@')[0]} uses latest or no tag",
                    "Pin a version tag or digest.")
        secret = re.match(r"^-?\s*[\"']?([A-Z0-9_]+)[\"']?\s*[:=]\s*(.*)$", stripped)
        if secret and SECRET_NAME.search(secret.group(1)) and not SECRET_REFERENCE_SUFFIX.search(secret.group(1)):
            value = secret.group(2).strip().strip("\"'")
            if value and not value.startswith("$"):
                add("CP006", "High", number, f"{secret.group(1)} has a literal value in the Compose file",
                    "Use top-level secrets or interpolate from an uncommitted source.")
    return findings


def lint_paths(root: Path, files: dict[str, object]) -> list[Finding]:
    real_root = root.resolve()
    findings: list[Finding] = []
    for kind in ("dockerfile", "compose"):
        for path in files.get(kind, []):  # type: ignore[union-attr]
            assert isinstance(path, Path)
            try:
                rel = path.resolve().relative_to(real_root).as_posix()
            except ValueError:
                rel = path.name
            try:
                if path.is_symlink() or not path.resolve().is_relative_to(real_root):
                    raise ValueError("outside root")
                if path.stat().st_size > MAX_FILE_BYTES:
                    findings.append(Finding("LINT001", "Question", rel, 0, "file skipped: larger than the size limit", "Review it manually."))
                    continue
                text = path.read_text(encoding="utf-8-sig")
            except (OSError, UnicodeError, ValueError):
                findings.append(Finding("LINT001", "Question", rel, 0, "file skipped: unreadable or outside the root", "Review it manually."))
                continue
            findings += lint_dockerfile(path, rel, text) if kind == "dockerfile" else lint_compose(rel, text)
    return findings


def summarize(findings: list[Finding]) -> dict[str, dict[str, int]]:
    by_severity = {s: 0 for s in SEVERITIES}
    by_rule: dict[str, int] = {}
    for finding in findings:
        by_severity[finding.severity] += 1
        by_rule[finding.rule] = by_rule.get(finding.rule, 0) + 1
    return {"by_severity": {k: v for k, v in by_severity.items() if v}, "by_rule": dict(sorted(by_rule.items()))}


def collect(paths: list[Path]) -> tuple[Path, dict[str, object]]:
    """Resolve CLI paths: one directory is scanned; explicit files are classified by name."""
    if len(paths) == 1 and paths[0].is_dir():
        return paths[0], discover(paths[0])
    root = Path(os.path.commonpath([str(p.resolve().parent) for p in paths]))
    files: dict[str, object] = {"dockerfile": [], "compose": [], "bake": [], "ignore": [], "truncated": False}
    for path in paths:
        kind = classify(path.name)
        if not path.is_file() or kind is None:
            raise ValueError(f"not a recognised container file: {path.name}")
        files[kind].append(path)  # type: ignore[union-attr]
    return root, files


def at_or_above(severity: str, threshold: str) -> bool:
    return SEVERITIES.index(severity) <= SEVERITIES.index(threshold)


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    parser.add_argument("paths", nargs="*", type=Path, default=[Path(".")])
    parser.add_argument("--format", choices=["text", "json"], default="text")
    parser.add_argument("--fail-on", choices=SEVERITIES, default="High")
    args = parser.parse_args(argv)
    try:
        root, files = collect(args.paths)
    except (OSError, ValueError) as exc:
        print(json.dumps({"error": str(exc)}) if args.format == "json" else f"error: {exc}")
        return 2
    findings = lint_paths(root, files)
    checked = len(files["dockerfile"]) + len(files["compose"])  # type: ignore[arg-type]
    if args.format == "json":
        print(json.dumps({"files": checked, "truncated": files["truncated"], "findings": [asdict(f) for f in findings],
                          "summary": summarize(findings)}, indent=2))
    else:
        for f in findings:
            print(f"{f.file}:{f.line}: {f.severity} {f.rule} {f.message}. {f.fix}")
        print(f"{checked} files checked, {len(findings)} findings. Static heuristics only; builds and runtime behaviour are not established.")
    return int(any(at_or_above(f.severity, args.fail_on) for f in findings))


if __name__ == "__main__":
    raise SystemExit(main())
