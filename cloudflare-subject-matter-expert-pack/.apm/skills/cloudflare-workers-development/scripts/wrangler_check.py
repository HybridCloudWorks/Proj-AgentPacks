#!/usr/bin/env python3
"""Read-only checker for Cloudflare Wrangler configuration.

Parses wrangler.jsonc, wrangler.json or wrangler.toml without running project code or contacting
Cloudflare, and prints findings as JSON. Values of secret-like keys are never printed; binding
names are listed, resource IDs are not.

Usage: python3 wrangler_check.py [project-dir] [--max-age-days N] [--today YYYY-MM-DD]
Exit 0 when no error-level finding, 1 when an error is found, 2 when no configuration could be read.
"""
from __future__ import annotations

import argparse
import datetime as dt
import fnmatch
import json
import re
import sys
from pathlib import Path
from typing import Any

CONFIG_NAMES = ("wrangler.jsonc", "wrangler.json", "wrangler.toml")
MAX_BYTES = 512 * 1024
SECRET_KEY = re.compile(r"(?i)(secret|token|passw(or)?d|api[_-]?key|private[_-]?key|credential|auth[_-]?key|signing[_-]?key)")
LOCAL_SECRET_FILES = (".dev.vars", ".env")
# Binding collections and the field that names each binding.
BINDING_FIELDS = {
    "kv_namespaces": "binding", "d1_databases": "binding", "r2_buckets": "binding", "vectorize": "binding",
    "hyperdrive": "binding", "services": "binding", "analytics_engine_datasets": "binding", "workflows": "binding",
    "secrets_store_secrets": "binding", "send_email": "name", "dispatch_namespaces": "binding",
    "mtls_certificates": "binding", "pipelines": "binding",
}
SINGLE_BINDINGS = ("ai", "browser", "images", "assets", "version_metadata")
# Wrangler does not inherit these keys from the top level into named environments.
NON_INHERITED = ("vars", "kv_namespaces", "d1_databases", "r2_buckets", "durable_objects", "queues", "services",
                 "vectorize", "hyperdrive", "workflows", "secrets_store_secrets", "analytics_engine_datasets", "ai")


def strip_jsonc(text: str) -> str:
    """Remove // and /* */ comments and trailing commas outside strings."""
    out: list[str] = []
    i, n, in_str = 0, len(text), False
    while i < n:
        c = text[i]
        if in_str:
            out.append(c)
            if c == "\\" and i + 1 < n:
                out.append(text[i + 1])
                i += 2
                continue
            in_str = c != '"'
            i += 1
            continue
        if c == '"':
            in_str = True
        elif c == "/" and text.startswith("//", i):
            end = text.find("\n", i)
            i = n if end == -1 else end
            continue
        elif c == "/" and text.startswith("/*", i):
            end = text.find("*/", i + 2)
            if end == -1:
                raise ValueError("unterminated block comment")
            i = end + 2
            continue
        out.append(c)
        i += 1
    stripped, result, in_str = "".join(out), [], False
    for i, c in enumerate(stripped):
        if in_str:
            result.append(c)
            if c == '"' and not _escaped(stripped, i):
                in_str = False
            continue
        if c == '"':
            in_str = True
        elif c == ",":
            rest = stripped[i + 1:].lstrip()
            if rest[:1] in ("}", "]"):
                continue
        result.append(c)
    return "".join(result)


def _escaped(text: str, index: int) -> bool:
    count, j = 0, index - 1
    while j >= 0 and text[j] == "\\":
        count += 1
        j -= 1
    return count % 2 == 1


def load_config(path: Path) -> dict[str, Any]:
    text = path.read_text(encoding="utf-8").lstrip("\ufeff")
    if path.suffix == ".toml":
        import tomllib  # Python 3.11+
        data = tomllib.loads(text)
    else:
        data = json.loads(strip_jsonc(text))
    if not isinstance(data, dict):
        raise ValueError("configuration root is not an object")
    return data


def _finding(level: str, code: str, message: str) -> dict[str, str]:
    return {"level": level, "code": code, "message": message}


def _items(value: Any) -> list[dict[str, Any]]:
    return [v for v in value if isinstance(v, dict)] if isinstance(value, list) else []


def _strings(value: Any) -> list[str]:
    return [v for v in value if isinstance(v, str)] if isinstance(value, list) else []


def bindings_of(scope: dict[str, Any]) -> dict[str, list[str]]:
    found: dict[str, list[str]] = {}
    for key, field in BINDING_FIELDS.items():
        names = [str(v.get(field)) for v in _items(scope.get(key)) if v.get(field)]
        if names:
            found[key] = names
    queues = scope.get("queues") if isinstance(scope.get("queues"), dict) else {}
    producers = [str(v.get("binding")) for v in _items(queues.get("producers")) if v.get("binding")]
    consumers = [str(v.get("queue")) for v in _items(queues.get("consumers")) if v.get("queue")]
    if producers:
        found["queues.producers"] = producers
    if consumers:
        found["queues.consumers"] = consumers
    do = scope.get("durable_objects") if isinstance(scope.get("durable_objects"), dict) else {}
    do_names = [str(v.get("name")) for v in _items(do.get("bindings")) if v.get("name")]
    if do_names:
        found["durable_objects"] = do_names
    for key in SINGLE_BINDINGS:
        value = scope.get(key)
        if isinstance(value, dict) and value.get("binding"):
            found[key] = [str(value["binding"])]
    return found


def _check_vars(scope: dict[str, Any], label: str, findings: list[dict[str, str]]) -> None:
    variables = scope.get("vars")
    if not isinstance(variables, dict):
        return
    for key, value in variables.items():
        text = value if isinstance(value, str) else ""
        if (SECRET_KEY.search(str(key)) and text.strip()) or ("PRIVATE KEY" in text and "-----BEGIN" in text):
            findings.append(_finding("error", "secret-in-vars",
                                     f"{label} vars.{key} looks like a credential; use a secret binding or the Secrets Store and rotate it if it was committed"))


def _check_durable_objects(config: dict[str, Any], findings: list[dict[str, str]]) -> None:
    migrations = _items(config.get("migrations"))
    tags = [str(m.get("tag")) for m in migrations if m.get("tag") is not None]
    for tag in sorted({t for t in tags if tags.count(t) > 1}):
        findings.append(_finding("error", "duplicate-migration-tag", f"migration tag {tag} appears more than once"))
    migrated: set[str] = set()
    for m in migrations:
        for key in ("new_classes", "new_sqlite_classes"):
            migrated |= {c for c in _strings(m.get(key))}
        for rename in _items(m.get("renamed_classes")):
            migrated.discard(str(rename.get("from")))
            if rename.get("to"):
                migrated.add(str(rename["to"]))
        migrated -= set(_strings(m.get("deleted_classes")))
        if _strings(m.get("new_classes")):
            findings.append(_finding("info", "kv-backed-durable-object",
                                     f"migration {m.get('tag')} uses new_classes; new Durable Object classes should use new_sqlite_classes"))
    environments = config.get("env") if isinstance(config.get("env"), dict) else {}
    scopes = [config] + [e for e in environments.values() if isinstance(e, dict)]
    for scope in scopes:
        do = scope.get("durable_objects") if isinstance(scope.get("durable_objects"), dict) else {}
        for binding in _items(do.get("bindings")):
            cls = binding.get("class_name")
            if cls and not binding.get("script_name") and str(cls) not in migrated:
                findings.append(_finding("warn", "durable-object-without-migration",
                                         f"Durable Object class {cls} is bound but no migration declares it"))


def _ignored(name: str, patterns: list[str]) -> bool:
    ignored = False
    for pattern in patterns:
        negate = pattern.startswith("!")
        body = pattern[1:] if negate else pattern
        body = body.lstrip("/").rstrip("/")
        if body and (fnmatch.fnmatch(name, body) or fnmatch.fnmatch(name, body.split("/")[-1])):
            ignored = not negate
    return ignored


def _check_local_secret_files(root: Path, findings: list[dict[str, str]]) -> None:
    gitignore = root / ".gitignore"
    patterns: list[str] = []
    if gitignore.is_file() and not gitignore.is_symlink() and gitignore.stat().st_size <= MAX_BYTES:
        patterns = [line.strip() for line in gitignore.read_text(encoding="utf-8", errors="replace").splitlines()
                    if line.strip() and not line.strip().startswith("#")]
    candidates = [p for p in root.iterdir() if p.is_file() and (p.name in LOCAL_SECRET_FILES or p.name.startswith(".dev.vars."))]
    for path in sorted(candidates):
        if not _ignored(path.name, patterns):
            findings.append(_finding("warn", "local-secrets-not-ignored",
                                     f"{path.name} exists but .gitignore does not appear to ignore it (heuristic; confirm with git check-ignore)"))


def check_project(root: Path, today: dt.date | None = None, max_age_days: int = 180) -> dict[str, Any]:
    root = root.resolve()
    today = today or dt.date.today()
    present = [name for name in CONFIG_NAMES if (root / name).is_file()]
    result: dict[str, Any] = {"tool": "wrangler_check", "version": 1, "config": None, "findings": [], "bindings": {}, "environments": []}
    findings: list[dict[str, str]] = result["findings"]
    if not present:
        findings.append(_finding("info", "no-config", "no Wrangler configuration in this folder"))
        return result
    if len(present) > 1:
        findings.append(_finding("warn", "multiple-configs", f"several configuration files present ({', '.join(present)}); confirm which one Wrangler reads and remove the others"))
    path = root / present[0]
    result["config"] = present[0]
    if path.is_symlink() or path.resolve().parent != root or path.stat().st_size > MAX_BYTES:
        findings.append(_finding("error", "config-out-of-bounds", "configuration is a symlink, outside the folder, or larger than the checker reads"))
        return result
    try:
        config = load_config(path)
    except (ValueError, OSError, ImportError) as exc:
        line = getattr(exc, "lineno", None)
        findings.append(_finding("error", "parse-error", f"{type(exc).__name__}" + (f" at line {line}" if line else "")))
        return result

    if not config.get("name"):
        findings.append(_finding("warn", "missing-name", "no top-level name; deploys need one"))
    if not config.get("main") and not isinstance(config.get("assets"), dict):
        findings.append(_finding("warn", "no-entry-point", "neither main nor assets is configured"))

    date_value = config.get("compatibility_date")
    if not date_value:
        findings.append(_finding("error", "missing-compatibility-date", "compatibility_date is not set"))
    else:
        try:
            date = dt.date.fromisoformat(str(date_value))
        except ValueError:
            findings.append(_finding("error", "invalid-compatibility-date", "compatibility_date is not YYYY-MM-DD"))
        else:
            age = (today - date).days
            result["compatibility_date"] = date.isoformat()
            result["compatibility_date_age_days"] = age
            if age < 0:
                findings.append(_finding("error", "future-compatibility-date", "compatibility_date is in the future"))
            elif age > max_age_days:
                findings.append(_finding("warn", "old-compatibility-date", f"compatibility_date is {age} days old; review the compatibility changes since then before bumping"))

    if not any(f.startswith("nodejs_compat") for f in _strings(config.get("compatibility_flags"))):
        findings.append(_finding("info", "no-nodejs-compat", "nodejs_compat is not enabled; libraries that need Node.js built-ins will fail"))

    observability = config.get("observability")
    if not isinstance(observability, dict) or observability.get("enabled") is not True:
        findings.append(_finding("warn", "observability-off", "observability is not enabled; Workers Logs will not be collected"))
    else:
        rate = observability.get("head_sampling_rate")
        if rate is not None and (not isinstance(rate, (int, float)) or isinstance(rate, bool) or not 0 <= rate <= 1):
            findings.append(_finding("error", "invalid-sampling-rate", "observability.head_sampling_rate must be between 0 and 1"))

    _check_vars(config, "top-level", findings)
    environments = config.get("env") if isinstance(config.get("env"), dict) else {}
    result["environments"] = sorted(environments)
    top_level_keys = [k for k in NON_INHERITED if config.get(k)]
    for env_name, env in sorted(environments.items()):
        if not isinstance(env, dict):
            continue
        _check_vars(env, f"env.{env_name}", findings)
        missing = [k for k in top_level_keys if not env.get(k)]
        if missing:
            findings.append(_finding("info", "bindings-not-inherited",
                                     f"env.{env_name} does not redeclare {', '.join(missing)}; these are not inherited from the top level"))
    _check_durable_objects(config, findings)

    routes = config.get("routes") or ([config["route"]] if config.get("route") else [])
    routes = routes if isinstance(routes, list) else [routes]
    if routes:
        findings.append(_finding("info", "production-routes", f"{len(routes)} route or custom-domain entries attach this Worker to zone traffic"))
        if config.get("workers_dev") is True:
            findings.append(_finding("info", "workers-dev-enabled", "workers_dev is also enabled; the workers.dev hostname stays reachable"))
    if isinstance(config.get("limits"), dict) and config["limits"].get("cpu_ms"):
        findings.append(_finding("info", "custom-cpu-limit", "limits.cpu_ms is set; confirm the plan allows it"))

    _check_local_secret_files(root, findings)
    result["bindings"] = bindings_of(config)
    return result


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    parser.add_argument("project", nargs="?", default=".", type=Path)
    parser.add_argument("--max-age-days", type=int, default=180)
    parser.add_argument("--today", type=dt.date.fromisoformat, default=None)
    args = parser.parse_args()
    if not args.project.is_dir():
        print(json.dumps({"tool": "wrangler_check", "error": "project folder not found"}))
        return 2
    result = check_project(args.project, args.today, args.max_age_days)
    print(json.dumps(result, indent=2))
    codes = {f["code"] for f in result["findings"]}
    if result["config"] is None or codes & {"parse-error", "config-out-of-bounds"}:
        return 2
    return 1 if any(f["level"] == "error" for f in result["findings"]) else 0


if __name__ == "__main__":
    sys.exit(main())
