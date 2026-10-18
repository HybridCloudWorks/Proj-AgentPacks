#!/usr/bin/env python3
"""Classify a proposed gcloud, bq, gsutil, kubectl, terraform or tofu command by approval level. Never executes it.

Levels follow the Google Cloud Architect pack: 0 local help or version, 1 read-only inspection or reversible local
work, 2 anything that changes cloud resources, IAM, APIs or credentials, exposes secrets, bills, or cannot be classified.

  python command_guard.py classify -- gcloud compute instances list --project=my-project
  python command_guard.py hook < payload.json    # reads a hook payload from stdin and prints a neutral verdict
Exit 0 for Level 0 or 1 (or not a cloud command), 2 for Level 2, 3 for invalid input.

This is a safety aid, not an enforcement boundary: a shell can still run anything.
"""
from __future__ import annotations

import json
import re
import shlex
import sys
from pathlib import PurePath

MAX_PAYLOAD_BYTES = 262144
CONTROL_OPERATORS = {";", "&&", "||", "|", "&", "|&", ";;"}

GCLOUD_VALUE_FLAGS = {"--project", "--account", "--configuration", "--format", "--filter", "--limit", "--region",
                      "--zone", "--location", "--impersonate-service-account", "--verbosity", "--flags-file",
                      "--billing-project", "--sort-by", "--page-size"}
GCLOUD_READ = {"list", "describe", "get", "show", "read", "help", "info", "version", "topic", "cheat-sheet",
               "search-all-resources", "search-all-iam-policies", "analyze-iam-policy", "lint-condition",
               "troubleshoot", "ls", "du", "cat", "hash"}
GCLOUD_READ_PREFIXES = ("list-", "get-", "describe-", "search-", "analyze-")
GCLOUD_SENSITIVE = {"print-access-token": "prints an access token",
                    "print-identity-token": "prints an identity token",
                    "print-refresh-token": "prints a refresh token",
                    "access": "reads a secret value",
                    "sign-blob": "signs data as a service account",
                    "sign-jwt": "signs a token as a service account",
                    "login": "interactive authentication is the user's step",
                    "activate-service-account": "activates a service account key file",
                    "revoke": "changes local credentials",
                    "ssh": "opens an interactive session on a resource",
                    "scp": "copies files to or from a resource",
                    "connect": "opens a database session",
                    "start-iap-tunnel": "opens a tunnel to a resource"}
GCLOUD_LOCAL_WRITE = {"get-credentials": "writes local kubeconfig", "configure-docker": "writes local Docker configuration"}
GCLOUD_MUTATING = {"cp", "mv", "rm", "rsync", "compose", "deploy", "apply", "destroy", "import", "export", "restore", "submit",
                   "execute", "run", "call", "invoke", "publish", "pull", "ack", "seek", "promote", "failover",
                   "switchover", "clone", "rollback", "upgrade", "link", "unlink", "purchase", "approve", "reject"}
# A prefix matches the whole word or the word followed by a hyphen, so "attach" matches "attach-disk" but not
# the "attachments" command group, and "set" matches "set-iam-policy" but not "settings".
GCLOUD_MUTATING_PREFIXES = ("create", "delete", "update", "patch", "set", "unset", "add", "remove", "enable",
                            "disable", "reset", "start", "stop", "resize", "attach", "detach", "move", "undelete",
                            "cancel", "replace", "recreate", "abandon", "rolling", "migrate", "rotate", "renew",
                            "suspend", "resume", "acknowledge", "modify", "install", "reinstall")
GCLOUD_UNSCOPED_GROUPS = {"config", "auth", "help", "version", "info", "topic", "components", "organizations",
                          "billing", "asset", "projects", "cheat-sheet", "init"}
GOVERNANCE_GROUPS = {"billing", "organizations", "resource-manager", "org-policies", "access-context-manager"}

BQ_VALUE_FLAGS = {"--project_id", "--location", "--format", "--dataset_id", "--max_rows", "-n", "--api"}
BQ_READ = {"ls", "show", "help", "version", "info", "wait", "get-iam-policy"}
BQ_MUTATING = {"mk", "rm", "update", "load", "cp", "extract", "insert", "cancel", "partition", "truncate",
               "set-iam-policy", "add-iam-policy-binding", "remove-iam-policy-binding", "undelete"}
GSUTIL_READ = {"ls", "du", "cat", "stat", "hash", "version", "help"}
GSUTIL_SUBGROUPS = {"iam", "acl", "defacl", "lifecycle", "versioning", "label", "cors", "logging", "notification",
                    "retention", "web", "ubla", "pap", "autoclass", "kms", "requesterpays", "defstorageclass", "rpo"}
KUBECTL_VALUE_FLAGS = {"-n", "--namespace", "--context", "--kubeconfig", "--cluster", "--user", "-s", "--server"}
KUBECTL_READ = {"get", "describe", "logs", "top", "explain", "api-resources", "api-versions", "version",
                "cluster-info", "events", "wait", "diff"}
TF_READ = {"validate", "show", "providers", "version", "graph", "console", "get", "metadata", "modules", "fmt"}
TF_MUTATING = {"apply", "destroy", "import", "taint", "untaint", "force-unlock", "refresh", "login", "logout", "test"}

Verdict = tuple[int, list[str], list[str]]


def _program(token: str) -> str:
    name = PurePath(token.replace("\\", "/")).name.lower()
    for suffix in (".exe", ".cmd", ".bat", ".ps1"):
        if name.endswith(suffix):
            name = name[: -len(suffix)]
    return name


def _words(args: list[str], value_flags: set[str]) -> list[str]:
    """Positional words, skipping flags and the values of flags that take a separate value."""
    words, skip = [], False
    for arg in args:
        if skip:
            skip = False
            continue
        if arg.startswith("-"):
            skip = arg in value_flags
            continue
        words.append(arg)
    return words


def _has_flag(args: list[str], *names: str) -> bool:
    return any(a == n or a.startswith(n + "=") for a in args for n in names)


def _flag_value(args: list[str], name: str) -> str | None:
    for i, arg in enumerate(args):
        if arg.startswith(name + "="):
            return arg.split("=", 1)[1]
        if arg == name and i + 1 < len(args):
            return args[i + 1]
    return None


def _prefixed(word: str, prefixes: tuple[str, ...]) -> bool:
    return any(word == p or word.startswith(p + "-") for p in prefixes)


def _gcloud(args: list[str]) -> Verdict:
    words = _words(args, GCLOUD_VALUE_FLAGS)
    if words and words[0] in ("alpha", "beta", "preview"):
        words = words[1:]
    if not words or words[0] in ("help", "version", "info", "topic", "cheat-sheet"):
        return 0, ["help or version information"], []
    group = words[0]
    warnings: list[str] = []
    if group not in GCLOUD_UNSCOPED_GROUPS and not _has_flag(args, "--project", "--organization", "--folder", "--scope"):
        warnings.append("no explicit --project: the active configuration would choose the target")
    if group == "config":
        verb = words[1] if len(words) > 1 else "list"
        return 1, ["reads local gcloud configuration" if verb in ("list", "get", "get-value") else "changes local gcloud configuration only"], warnings
    if group == "components" and len(words) > 1 and words[1] != "list":
        return 2, ["installs or changes local software"], warnings
    for word in words[1:]:
        if word in GCLOUD_SENSITIVE:
            return 2, [GCLOUD_SENSITIVE[word]], warnings
        if word in GCLOUD_LOCAL_WRITE:
            return 1, ["read-only cloud call that " + GCLOUD_LOCAL_WRITE[word]], warnings
        if word in GCLOUD_MUTATING or _prefixed(word, GCLOUD_MUTATING_PREFIXES):
            if _has_flag(args, "--dry-run", "--validate-only"):
                return 1, [f"'{word}' with a preview flag; confirm the leaf command supports it with gcloud help"], warnings
            reasons = [f"'{word}' changes cloud state"]
            if "iam" in word or group == "iam":
                reasons.append("IAM change")
            if group == "kms":
                reasons.append("key operations can make data permanently unreadable")
            if group in GOVERNANCE_GROUPS:
                reasons.append("affects governance for many resources")
            return 2, reasons, warnings
        if word in GCLOUD_READ or word.startswith(GCLOUD_READ_PREFIXES):
            reasons = ["read-only inspection"]
            if word in ("cat", "read"):
                reasons.append("reads object or log content; query narrowly")
            return 1, reasons, warnings
    return 2, ["no known verb; cannot classify, review manually"], warnings


def _bq(args: list[str]) -> Verdict:
    words = _words(args, BQ_VALUE_FLAGS)
    if not words:
        return 0, ["help or version information"], []
    sub = words[0]
    if sub == "query":
        value = _flag_value(args, "--dry_run")
        dry = _has_flag(args, "--dry_run") and (value is None or value.lower() != "false")
        return (1, ["dry run estimates bytes without billing"], []) if dry else (2, ["billable query; dry-run first and get approval"], [])
    if sub == "head":
        return 1, ["reads table rows; query narrowly"], []
    if sub in BQ_READ:
        return 1, ["read-only inspection"], []
    if sub in BQ_MUTATING:
        return 2, [f"'bq {sub}' changes data or metadata"], []
    return 2, ["no known bq subcommand; cannot classify, review manually"], []


def _gsutil(args: list[str]) -> Verdict:
    words = _words(args, set())
    if not words:
        return 0, ["help or version information"], []
    sub = words[0]
    if sub in GSUTIL_SUBGROUPS:
        if len(words) > 1 and words[1] == "get":
            return 1, ["read-only inspection"], []
        return 2, [f"'gsutil {sub}' changes bucket configuration or access"], []
    if sub in GSUTIL_READ:
        return 1, ["read-only inspection"] + (["reads object content"] if sub == "cat" else []), []
    return 2, [f"'gsutil {sub}' can change or copy data"], []


def _kubectl(args: list[str]) -> Verdict:
    words = _words(args, KUBECTL_VALUE_FLAGS)
    if not words:
        return 0, ["help or version information"], []
    verb = words[0]
    if verb == "config":
        return 1, ["reads or changes local kubeconfig only"], []
    if verb == "auth":
        return (1, ["permission check"], []) if len(words) > 1 and words[1] == "can-i" else (2, ["changes RBAC"], [])
    if verb == "rollout":
        return (1, ["read-only inspection"], []) if len(words) > 1 and words[1] in ("status", "history") else (2, ["changes a rollout"], [])
    prints_output = any(a == "-o" or a.startswith("-o") or a.startswith("--output") for a in args)
    if verb == "get" and prints_output and any(w in ("secret", "secrets") or w.startswith("secret/") for w in words[1:]):
        return 2, ["prints secret data"], []
    if verb in KUBECTL_READ:
        return 1, ["read-only inspection"] + (["server-side preview"] if verb == "diff" else []), []
    dry = _flag_value(args, "--dry-run")
    if (dry is not None and dry != "none") or (dry is None and _has_flag(args, "--dry-run")):
        return 1, [f"'{verb}' with a dry run"], []
    return 2, [f"'kubectl {verb}' changes or accesses the cluster"], []


def _terraform(args: list[str]) -> Verdict:
    words = _words(args, set())
    if not words:
        return 0, ["help or version information"], []
    sub = words[0]
    action = words[1] if len(words) > 1 else ""
    if sub == "init":
        return 1, ["downloads providers and modules and may configure the backend"], []
    if sub == "plan":
        return 1, ["reads live resources and takes the state lock; read data sources and external programs first"], []
    if sub == "output":
        return 1, ["may print sensitive outputs"], []
    if sub == "state":
        if action in ("list", "show"):
            return 1, ["reads state"], []
        if action == "pull":
            return 2, ["prints full state, which can contain secrets"], []
        return 2, [f"'state {action}' changes state"], []
    if sub == "workspace":
        if action in ("list", "show", "select"):
            return 1, ["workspace inspection or local selection"], []
        return 2, ["changes workspaces in the backend"], []
    if sub in TF_READ:
        rewrites = sub == "fmt" and not _has_flag(args, "-check")
        return 1, ["local or read-only operation"] + (["rewrites files unless -check is used"] if rewrites else []), []
    if sub == "test":
        return 2, ["terraform test can create real resources"], []
    if sub in TF_MUTATING:
        return 2, [f"'{sub}' changes infrastructure, state or credentials"], []
    return 2, ["no known subcommand; cannot classify, review manually"], []


HANDLERS = {"gcloud": _gcloud, "bq": _bq, "gsutil": _gsutil, "kubectl": _kubectl, "terraform": _terraform, "tofu": _terraform}


def _split(tokens: list[str]) -> tuple[list[list[str]], list[str]]:
    segments: list[list[str]] = [[]]
    notes: list[str] = []
    skip_target = False
    for token in tokens:
        if skip_target:
            skip_target = False
            continue
        if token in CONTROL_OPERATORS:
            notes.append("compound command: run and review one command at a time")
            segments.append([])
        elif token and set(token) <= {">", "&"}:
            notes.append("redirects output to a local file")
            skip_target = True
        elif token == "<":
            skip_target = True
        else:
            segments[-1].append(token)
    return [s for s in segments if s], list(dict.fromkeys(notes))


def _tokens(command: str) -> list[str]:
    # Line continuations join lines; any other newline separates commands. Backslashes inside Windows paths
    # become forward slashes so that C:\tools\gcloud.cmd still names gcloud after shell-style unescaping.
    text = command.replace("\r\n", "\n").replace("\\\n", " ").replace("\n", " ; ")
    text = re.sub(r"\\(?=[A-Za-z0-9_.-])", "/", text)
    lexer = shlex.shlex(text, posix=True, punctuation_chars=";&|<>")
    lexer.whitespace_split = True
    lexer.commenters = ""
    return list(lexer)


def classify(command: str | list[str]) -> dict[str, object]:
    def ask(reason: str) -> dict[str, object]:
        return {"level": 2, "verdict": "ask", "tools": [], "reasons": [reason], "warnings": []}

    parts = command if isinstance(command, list) else [command]
    if any("$(" in p or "`" in p for p in parts):
        return ask("command substitution cannot be classified")
    try:
        tokens = list(command) if isinstance(command, list) else _tokens(command)
    except ValueError:
        return ask("unbalanced quoting; cannot classify")
    segments, notes = _split(tokens)
    levels: list[int] = []
    tools: list[str] = []
    reasons: list[str] = []
    warnings: list[str] = []
    for segment in segments:
        while segment and "=" in segment[0] and not segment[0].startswith("-"):
            segment = segment[1:]  # environment assignments such as CLOUDSDK_CORE_PROJECT=x
        if not segment:
            continue
        program = _program(segment[0])
        if program in ("sudo", "su", "runas"):
            levels.append(2)
            reasons.append("privilege elevation on the local machine")
            continue
        if program not in HANDLERS:
            continue
        level, why, warn = HANDLERS[program](segment[1:])
        tools.append(program)
        levels.append(level)
        reasons.extend(f"{program}: {r}" for r in why)
        warnings.extend(f"{program}: {w}" for w in warn)
    if not levels:
        return {"level": None, "verdict": "allow", "tools": [], "warnings": [],
                "reasons": ["not a Google Cloud or Kubernetes CLI command; outside this guard's scope"]}
    level = max(levels)
    if "redirects output to a local file" in notes:
        level = max(level, 1)
    return {"level": level, "verdict": "ask" if level >= 2 else "allow", "tools": tools,
            "reasons": reasons + notes, "warnings": warnings}


def command_from_payload(payload: object) -> str | None:
    """Find a shell command in a hook payload. Field names differ by client and are not verified for every client."""
    if not isinstance(payload, dict):
        return None
    tool_input = payload.get("tool_input")
    if isinstance(tool_input, dict) and isinstance(tool_input.get("command"), str):
        return tool_input["command"]
    tool_args = payload.get("toolArgs")
    if isinstance(tool_args, str):
        try:
            tool_args = json.loads(tool_args)
        except ValueError:
            tool_args = None
    if isinstance(tool_args, dict) and isinstance(tool_args.get("command"), str):
        return tool_args["command"]
    if isinstance(payload.get("command"), str):
        return payload["command"]
    return None


def main(argv: list[str]) -> int:
    if len(argv) >= 2 and argv[1] == "classify":
        rest = argv[2:]
        if rest and rest[0] == "--":
            rest = rest[1:]
        if not rest:
            print(json.dumps({"error": "usage: command_guard.py classify -- COMMAND ..."}))
            return 3
        result = classify(rest[0] if len(rest) == 1 else rest)
        print(json.dumps(result, indent=2))
        return 2 if result["level"] == 2 else 0
    if len(argv) == 2 and argv[1] == "hook":
        raw = sys.stdin.buffer.read(MAX_PAYLOAD_BYTES + 1)
        try:
            if len(raw) > MAX_PAYLOAD_BYTES:
                raise ValueError("payload too large")
            payload = json.loads(raw.decode("utf-8"))
        except (ValueError, UnicodeDecodeError):
            print(json.dumps({"error": "invalid hook input"}))
            return 3
        command = command_from_payload(payload)
        if command is None:
            print(json.dumps({"decision": "allow", "reason": "no shell command in payload"}))
            return 0
        result = classify(command)
        # The command text is not echoed back: it may contain secrets.
        print(json.dumps({"decision": result["verdict"], "level": result["level"], "tools": result["tools"], "reasons": result["reasons"]}))
        if result["level"] == 2:
            print("Level 2 command needs explicit approval: " + "; ".join(map(str, result["reasons"])), file=sys.stderr)
            return 2
        return 0
    print(json.dumps({"error": "usage: command_guard.py classify -- COMMAND ... | command_guard.py hook"}))
    return 3


if __name__ == "__main__":
    raise SystemExit(main(sys.argv))
