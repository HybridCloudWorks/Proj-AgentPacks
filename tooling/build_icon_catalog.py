#!/usr/bin/env python3
"""Build or check the draw.io icon catalog used by the shared diagram-validation-and-evidence skill.

The catalog records every AWS, Azure and Google Cloud palette entry that draw.io's own shape libraries offer at one
release: the palette title (the product name draw.io shows), the palette it sits in, its form (AWS service icon,
resource stencil or group; Azure image; Google Cloud core product or category icon), the default size, and the full
style string draw.io inserts. The skill's scripts/check_drawio.py uses it to tell a current icon from a legacy,
retired or misspelled one, and to spot an icon whose colours differ from the palette (it then draws incompletely or
recoloured), without draw.io installed. It is built from draw.io's public source at a release tag:

  AWS           Sidebar-AWS4.js: the current "AWS <year>" library, and its "AWS (retired)" palette
                Sidebar-AWS4b.js: the "AWS18" library, legacy
  Azure         the img/lib/azure2 image files, and Sidebar-Azure2.js for the ones the Azure palette offers
  Google Cloud  Sidebar-GCP3.js: "Google Cloud Platform 2026", category and core product icons

The sidebar files build each style by concatenating strings held in variables and function parameters, so the
script evaluates that small subset of JavaScript (string and number literals, variables, +, *, /, -, parentheses and
one-line helper functions) rather than matching names with patterns. An entry it cannot evaluate stops the build.

The skill's hand-maintained scripts/icon_preferences.json (which Azure file to use where draw.io offers several) is
not generated here; --check reports any path it names that the new catalog no longer offers, so it is re-verified.

Usage: python tooling/build_icon_catalog.py [--tag latest|vX.Y.Z] [--check] [--markdown OUT]
  --tag       draw.io release tag to read (default: latest)
  --check     compare with the committed catalog instead of writing it
  --markdown  with --check, also write the differences as Markdown (used by the weekly watch issue)
Exit status: 0 written, or unchanged with --check; 1 with --check, an icon list or palette style differs, or an
icon preference names a path the catalog no longer offers; 2 draw.io's source could not be fetched or parsed (a
failure of this run, not a change in draw.io's libraries).
"""
from __future__ import annotations

import argparse
import datetime as dt
import http.client
import json
import os
import re
import sys
import time
import urllib.error
import urllib.request
from pathlib import Path

REPO = Path(__file__).resolve().parents[1]
CATALOG = REPO / "shared-primitives" / "skills" / "diagram-validation-and-evidence" / "scripts" / "icon_catalog.json"
PREFERENCES = CATALOG.parent / "icon_preferences.json"
API = "https://api.github.com/repos/jgraph/drawio"
RAW = "https://raw.githubusercontent.com/jgraph/drawio/{tag}/src/main/webapp/js/diagramly/sidebar/{name}"
AZURE_IMAGES = "src/main/webapp/img/lib/azure2/"
AZURE_PREFIX = "img/lib/azure2/"
SCHEMA = 2
LISTS = [("aws4", "current"), ("aws4", "retired"), ("aws4", "legacy"), ("azure2", "current"), ("azure2", "legacy"),
         ("gcp3", "core"), ("gcp3", "categories")]
# Style prefixes shorter than this are not worth sharing between entries.
MIN_PREFIX = 40


class SourceError(Exception):
    """draw.io's source could not be fetched or parsed: the run failed, which says nothing about icon changes."""


ATTEMPTS = 3


def _retryable(exc: BaseException) -> bool:
    """Network trouble that a later attempt may not meet. An HTTP client error (a missing tag is a 404) will not
    change on retry, except 429 Too Many Requests."""
    if isinstance(exc, urllib.error.HTTPError):
        return exc.code >= 500 or exc.code == 429
    return True


def get(url: str) -> bytes:
    if not url.startswith(("https://api.github.com/", "https://raw.githubusercontent.com/")):
        raise ValueError(f"only GitHub https URLs are fetched, not {url}")
    headers = {"User-Agent": "proj-agent-packs-icon-catalog", "Accept": "application/vnd.github+json"}
    token = os.environ.get("GITHUB_TOKEN") or os.environ.get("GH_TOKEN")
    if token and url.startswith("https://api.github.com/"):
        headers["Authorization"] = f"Bearer {token}"
    request = urllib.request.Request(url, headers=headers)  # noqa: S310
    for attempt in range(ATTEMPTS):
        try:
            # Safe: only GitHub https URLs reach this point.
            with urllib.request.urlopen(request, timeout=120) as response:  # noqa: S310  # nosec B310
                return response.read()
        # OSError covers URLError and HTTPError (DNS, refused, HTTP status), ConnectionError, TimeoutError and, on
        # Python 3.9, socket.timeout; HTTPException covers IncompleteRead and other broken responses.
        except (http.client.HTTPException, OSError) as exc:
            if attempt == ATTEMPTS - 1 or not _retryable(exc):
                raise SourceError(f"could not read {url} (attempt {attempt + 1} of {ATTEMPTS}): {exc}") from exc
            time.sleep(5 * (attempt + 1))
    raise AssertionError("unreachable")


def get_json(url: str):
    try:
        return json.loads(get(url))
    except ValueError as exc:  # json.JSONDecodeError, or bytes that are not UTF-8
        raise SourceError(f"{url} did not return JSON: {exc}") from exc


# ---------------------------------------------------------------------------------------------------------------
# A tiny evaluator for the JavaScript expressions draw.io's sidebar files use to build styles
# ---------------------------------------------------------------------------------------------------------------

class Unresolved(Exception):
    """The expression uses something this evaluator does not model."""


class JsFunction:
    """`var name = function(params) { return <expression>; };`"""

    def __init__(self, params: list[str], body: str, env: dict) -> None:
        self.params, self.body, self.env = params, body, env


UNRESOLVED = object()
CONSTANTS = {"mxConstants.STYLE_SHAPE": "shape", "null": None, "true": True, "false": False}
_TOKEN = re.compile(r"""\s*(?:(?P<str>'(?:\\.|[^'\\\n])*'|"(?:\\.|[^"\\\n])*")|(?P<num>\d+(?:\.\d+)?)"""
                    r"""|(?P<name>[A-Za-z_$][\w$]*(?:\.[A-Za-z_$][\w$]*)*)|(?P<op>[-+*/(),]))""")
_ESCAPES = {"n": "\n", "t": "\t", "r": "\r"}


def strip_comments(js: str) -> str:
    """Remove // and /* */ comments outside string literals (the sidebar files use no regular expression literals)."""
    out, i, quote = [], 0, ""
    while i < len(js):
        ch = js[i]
        if quote:
            out.append(ch)
            if ch == "\\" and i + 1 < len(js):
                out.append(js[i + 1])
                i += 1
            elif ch == quote or ch == "\n":
                quote = ""
        elif ch in "'\"":
            quote = ch
            out.append(ch)
        elif js.startswith("//", i):
            end = js.find("\n", i)
            i = len(js) if end < 0 else end
            continue
        elif js.startswith("/*", i):
            end = js.find("*/", i + 2)
            i = len(js) if end < 0 else end + 2
            continue
        else:
            out.append(ch)
        i += 1
    return "".join(out)


def scan(text: str, start: int, stops: str) -> int:
    """Index of the first character in `stops` at bracket depth 0 and outside strings, from `start`."""
    depth, quote, i = 0, "", start
    while i < len(text):
        ch = text[i]
        if quote:
            if ch == "\\":
                i += 1
            elif ch == quote:
                quote = ""
        elif ch in "'\"":
            quote = ch
        elif ch in "([{":
            depth += 1
        elif ch in ")]}":
            if depth == 0 and ch in stops:
                return i
            depth -= 1
        elif depth == 0 and ch in stops:
            return i
        i += 1
    return len(text)


def call_args(text: str, open_paren: int) -> tuple[list[str], int]:
    """Split the argument list that starts at text[open_paren] == '(' into argument texts."""
    args, i = [], open_paren + 1
    while True:
        end = scan(text, i, ",)")
        piece = text[i:end].strip()
        if piece:
            args.append(piece)
        if end >= len(text) or text[end] == ")":
            return args, end
        i = end + 1


def js_str(value) -> str:
    if value is None:
        return "null"
    if isinstance(value, bool):
        return "true" if value else "false"
    if isinstance(value, float):
        return str(int(value)) if value.is_integer() else repr(value)
    return str(value)


def evaluate(text: str, env: dict):
    """Evaluate one expression built from literals, names, + - * /, parentheses and calls to JsFunction values."""
    tokens = []
    pos, text = 0, text.strip()
    while pos < len(text):
        match = _TOKEN.match(text, pos)
        if not match or match.end() == pos:
            raise Unresolved(f"cannot read {text[pos:pos + 40]!r}")
        kind = match.lastgroup
        raw = match.group(kind)
        if kind == "str":
            raw = re.sub(r"\\(.)", lambda m: _ESCAPES.get(m.group(1), m.group(1)), raw[1:-1])
        elif kind == "num":
            raw = float(raw)
        tokens.append((kind, raw))
        pos = match.end()
    parser = _Parser(tokens, env)
    value = parser.additive()
    if parser.i != len(tokens):
        raise Unresolved(f"unexpected {tokens[parser.i][1]!r}")
    return value


class _Parser:
    def __init__(self, tokens: list, env: dict) -> None:
        self.tokens, self.env, self.i = tokens, env, 0

    def peek(self) -> tuple:
        return self.tokens[self.i] if self.i < len(self.tokens) else ("end", None)

    def take(self, op: str | None = None) -> tuple:
        token = self.peek()
        if token[0] == "end" or (op is not None and token != ("op", op)):
            raise Unresolved(f"expected {op or 'a value'}, found {token[1]!r}")
        self.i += 1
        return token

    def additive(self):
        value = self.multiplicative()
        while self.peek() in (("op", "+"), ("op", "-")):
            op = self.take()[1]
            right = self.multiplicative()
            if op == "+" and (isinstance(value, str) or isinstance(right, str)):
                value = js_str(value) + js_str(right)
            elif isinstance(value, float) and isinstance(right, float):
                value = value + right if op == "+" else value - right
            else:
                raise Unresolved("arithmetic on a non-number")
        return value

    def multiplicative(self):
        value = self.unary()
        while self.peek() in (("op", "*"), ("op", "/")):
            op = self.take()[1]
            right = self.unary()
            if not (isinstance(value, float) and isinstance(right, float)):
                raise Unresolved("arithmetic on a non-number")
            value = value * right if op == "*" else value / right
        return value

    def unary(self):
        if self.peek() == ("op", "-"):
            self.take()
            value = self.unary()
            if not isinstance(value, float):
                raise Unresolved("negation of a non-number")
            return -value
        return self.primary()

    def primary(self):
        kind, raw = self.take()
        if kind in ("str", "num"):
            return raw
        if kind == "op" and raw == "(":
            value = self.additive()
            self.take(")")
            return value
        if kind != "name":
            raise Unresolved(f"unexpected {raw!r}")
        if self.peek() == ("op", "("):
            self.take("(")
            args = []
            while self.peek() != ("op", ")"):
                args.append(self.additive())
                if self.peek() == ("op", ","):
                    self.take(",")
            self.take(")")
            function = self.env.get(raw)
            if not isinstance(function, JsFunction):
                raise Unresolved(f"call to {raw}")
            scope = dict(function.env)
            scope.update(zip(function.params, args))
            return evaluate(function.body, scope)
        if raw in CONSTANTS:
            return CONSTANTS[raw]
        value = self.env.get(raw, UNRESOLVED)
        if value is UNRESOLVED or isinstance(value, JsFunction):
            raise Unresolved(f"unknown name {raw}")
        return value


_FUNCTION = re.compile(r"Sidebar\.prototype\.(\w+)\s*=\s*function\s*\(([^)]*)\)")
_VAR = re.compile(r"\bvar\s+([A-Za-z_$][\w$]*)\s*=\s*")
_LOCAL_FUNCTION = re.compile(r"function\s*\(([^)]*)\)\s*\{\s*return\b")
_CALL = re.compile(r"\bthis\.(\w+)\s*\(")


def function_bodies(js: str) -> dict[str, tuple[list[str], str]]:
    """Map each `Sidebar.prototype.<name> = function(<params>)` to its parameters and source text."""
    js = strip_comments(js)
    starts = [(m.group(1), [p.strip() for p in m.group(2).split(",") if p.strip()], m.start(), m.end())
              for m in _FUNCTION.finditer(js)]
    out = {}
    for i, (name, params, _, body_start) in enumerate(starts):
        end = starts[i + 1][2] if i + 1 < len(starts) else len(js)
        out[name] = (params, js[body_start:end])
    return out


def local_env(body: str, env: dict) -> dict:
    """Add each `var` of a function body to env, in source order; anything unevaluable becomes UNRESOLVED."""
    env = dict(env)
    for match in _VAR.finditer(body):
        name, start = match.group(1), match.end()
        helper = _LOCAL_FUNCTION.match(body, start)
        if helper:
            end = scan(body, helper.end(), ";}")
            params = [p.strip() for p in helper.group(1).split(",") if p.strip()]
            env[name] = JsFunction(params, body[helper.end():end], env)
            continue
        end = scan(body, start, ";")
        try:
            env[name] = evaluate(body[start:end], env)
        except Unresolved:
            env[name] = UNRESOLVED
    return env


def sidebar_entries(js: str) -> list[dict]:
    """Every createVertexTemplateEntry in a sidebar file, evaluated: function, palette title, style, size, title.

    A palette function's parameters are bound from the place another function in the same file calls it, so
    `this.addAzure2DatabasesPalette(gn, r, sb, s + 'databases/')` gives the callee's `s` its full image prefix."""
    functions = function_bodies(js)
    callers: dict[str, list[str]] = {}
    for name, (_, body) in functions.items():
        for match in _CALL.finditer(body):
            if match.group(1) in functions and match.group(1) != name:
                callers.setdefault(match.group(1), []).append(name)
    envs: dict[str, dict] = {}

    def env_of(name: str, stack: tuple = ()) -> dict:
        if name in envs:
            return envs[name]
        params, body = functions[name]
        bound: dict = {p: UNRESOLVED for p in params}
        caller = next((c for c in callers.get(name, []) if c not in stack), None)
        if caller:
            caller_env = env_of(caller, stack + (name,))
            caller_body = functions[caller][1]
            for match in _CALL.finditer(caller_body):
                if match.group(1) == name:
                    args, _ = call_args(caller_body, match.end() - 1)
                    for param, arg in zip(params, args):
                        try:
                            bound[param] = evaluate(arg, caller_env)
                        except Unresolved:
                            bound[param] = UNRESOLVED
                    break
        envs[name] = local_env(body, bound)
        return envs[name]

    entries = []
    for name, (_, body) in functions.items():
        env = env_of(name)
        palette = ""
        for match in re.finditer(r"\bthis\.addPalette(?:Functions)?\s*\(", body):
            args, _ = call_args(body, match.end() - 1)
            try:
                palette = str(evaluate(args[1], env)) if len(args) > 1 else ""
            except Unresolved:
                palette = ""
            break
        for match in re.finditer(r"\bthis\.createVertexTemplateEntry\s*\(", body):
            args, _ = call_args(body, match.end() - 1)
            entry: dict = {"function": name, "palette": palette}
            try:
                values = [evaluate(a, env) for a in args[:5]]
                style, width, height = values[0], values[1], values[2]
                value = values[3] if len(values) > 3 else None
                title = values[4] if len(values) > 4 else None
                if not isinstance(style, str) or not isinstance(width, float) or not isinstance(height, float):
                    raise Unresolved("style is not a string or size is not a number")
                label = title if isinstance(title, str) and title else value if isinstance(value, str) else ""
                entry.update(style=style, w=round(width, 2), h=round(height, 2), title=" ".join(label.split()))
            except (Unresolved, IndexError) as exc:
                entry["error"] = f"{exc}: {args[0][:80] if args else ''}"
            entries.append(entry)
    return entries


# ---------------------------------------------------------------------------------------------------------------
# Per-provider classification
# ---------------------------------------------------------------------------------------------------------------

def parse_style(style: str) -> dict[str, str]:
    out: dict[str, str] = {}
    for part in (style or "").split(";"):
        if part:
            key, sep, value = part.partition("=")
            out[key.strip()] = value.strip() if sep else ""
    return out


_POINTS = re.compile(r"points=\[[^;]*\];?")


def without_points(style: str) -> str:
    """A palette style without its `points=[...]` connection constraints, which do not change how the icon draws."""
    return _POINTS.sub("", style)


def _drop(prefix: str, text: str) -> str:
    return text[len(prefix):] if text.startswith(prefix) else text


def aws_form(style: dict[str, str]) -> tuple[str, str]:
    """(form, name) of an AWS style: service (resourceIcon), resource (a stencil), group, product (AWS18) or plain."""
    shape = style.get("shape", "")
    if not shape.startswith("mxgraph.aws4."):
        return "plain", ""
    base = shape[len("mxgraph.aws4."):]
    if base == "resourceIcon":
        return "service", _drop("mxgraph.aws4.", style.get("resIcon", ""))
    if base in ("group", "groupCenter"):
        return "group", _drop("mxgraph.aws4.", style.get("grIcon", "")) or base
    if base == "productIcon":
        return "product", _drop("mxgraph.aws4.", style.get("prIcon", ""))
    return "resource", base


def _require(entries: list[dict], what: str) -> list[dict]:
    broken = [e for e in entries if "error" in e]
    if broken:
        sample = "; ".join(f"{e['function']}: {e['error']}" for e in broken[:5])
        raise SourceError(f"{len(broken)} {what} palette entries could not be evaluated ({sample}); "
                         "the draw.io source layout may have changed")
    return entries


def parse_aws(aws4_js: str, aws4b_js: str) -> list[dict]:
    out = []
    for source, legacy in ((aws4_js, False), (aws4b_js, True)):
        for entry in _require(sidebar_entries(source), "AWS"):
            form, name = aws_form(parse_style(entry["style"]))
            status = "legacy" if legacy else "retired" if "Retired" in entry["function"] else "current"
            out.append({"name": name, "form": form, "status": status, "title": entry["title"],
                        "palette": entry["palette"], "w": entry["w"], "h": entry["h"], "style": without_points(entry["style"])})
    return out


def parse_azure(azure2_js: str, image_paths: list[str]) -> tuple[list[dict], list[str], dict[str, str]]:
    """Azure palette entries, the image files no entry offers (legacy), and palette paths whose letter case differs
    from the file in draw.io's source tree (palette spelling -> file spelling). Entries offered through a full
    `image=img/lib/azure2/...` string count as well as those built from a palette's category prefix.

    A palette spelling that differs from the file only in letter case draws a broken image: draw.io Desktop 32.6.1
    rendered the palette spelling broken and the file spelling correctly, and app.diagrams.net answered 404 and 200
    (checked 2026-11-01). Such an entry is recorded under the file's spelling, so a style taken from the catalog draws."""
    files = sorted(p for p in image_paths if p.endswith(".svg"))
    by_lower: dict[str, str] = {p.lower(): p for p in files}
    entries, case = [], {}
    for entry in _require(sidebar_entries(azure2_js), "Azure"):
        image = parse_style(entry["style"]).get("image", "")
        if not image.startswith(AZURE_PREFIX):
            continue
        path = image[len(AZURE_PREFIX):]
        style = without_points(entry["style"])
        if path not in files and path.lower() in by_lower:
            case[path] = by_lower[path.lower()]
            style = style.replace(AZURE_PREFIX + path, AZURE_PREFIX + case[path])
            path = case[path]
        entries.append({"name": path, "form": "image", "status": "current", "title": entry["title"],
                        "palette": entry["palette"], "w": entry["w"], "h": entry["h"], "style": style})
    offered = {e["name"] for e in entries}
    return entries, [p for p in files if p not in offered], case


def parse_gcp3(gcp3_js: str) -> list[dict]:
    out = []
    for entry in _require(sidebar_entries(gcp3_js), "Google Cloud"):
        shape = parse_style(entry["style"]).get("shape", "")
        if not shape.startswith("mxgraph.gcp3."):
            continue
        form = "core" if "Core" in entry["function"] else "category" if "Categor" in entry["function"] else "other"
        out.append({"name": shape[len("mxgraph.gcp3."):], "form": form, "status": "current", "title": entry["title"],
                    "palette": entry["palette"], "w": entry["w"], "h": entry["h"], "style": without_points(entry["style"])})
    return out


# ---------------------------------------------------------------------------------------------------------------
# Catalog layout: entries keep their full style, with long shared prefixes stored once
# ---------------------------------------------------------------------------------------------------------------

ENTRY_FIELDS = ["name", "form", "status", "title", "palette", "w", "h"]


def _number(value: float):
    return int(value) if float(value).is_integer() else value


def pack_entries(libraries: dict[str, list[dict]]) -> tuple[list[str], list[str], dict[str, list[list]]]:
    """Compact rows [name, form, status, title, palette index, w, h, prefix index or -1, rest of the style], with
    each palette title and each style prefix that several entries share stored once."""
    counts: dict[str, int] = {}
    for entries in libraries.values():
        for entry in entries:
            style = entry["style"]
            for cut in (m.end() for m in re.finditer(";", style)):
                if cut >= MIN_PREFIX:
                    counts[style[:cut]] = counts.get(style[:cut], 0) + 1
    shared = {p for p, n in counts.items() if n > 1}
    prefixes: list[str] = []
    palettes: list[str] = []
    rows: dict[str, list[list]] = {}

    def index(table: list[str], value: str) -> int:
        if value not in table:
            table.append(value)
        return table.index(value)

    for library, entries in libraries.items():
        rows[library] = []
        for entry in entries:
            style = entry["style"]
            cuts = [m.end() for m in re.finditer(";", style) if m.end() < len(style)]
            best = next((style[:c] for c in reversed(cuts) if style[:c] in shared), "")
            rows[library].append([entry["name"], entry["form"], entry["status"], entry["title"],
                                  index(palettes, entry["palette"]), _number(entry["w"]), _number(entry["h"]),
                                  index(prefixes, best) if best else -1, style[len(best):]])
    return palettes, prefixes, rows


def unpack_entries(catalog: dict, library: str) -> list[dict]:
    """The palette entries of one library as dicts with the palette title and full `style`; empty for schema 1."""
    prefixes, palettes = catalog.get("prefixes", []), catalog.get("palettes", [])
    out = []
    for row in catalog.get(library, {}).get("entries", []):
        entry = dict(zip(ENTRY_FIELDS, row))
        entry["palette"] = palettes[row[4]]
        entry["style"] = (prefixes[row[7]] if row[7] >= 0 else "") + row[8]
        out.append(entry)
    return out


def lists(catalog: dict) -> dict[tuple[str, str], set[str]]:
    """The name lists the weekly watch compares, from either catalog schema."""
    if catalog.get("schema", 1) < SCHEMA:
        return {(lib, kind): set(catalog.get(lib, {}).get(kind, [])) for lib, kind in LISTS}
    aws = unpack_entries(catalog, "aws4")
    named = [(e["status"], e["name"]) for e in aws if e["form"] != "plain" and e["name"]]
    current = {n for s, n in named if s == "current"}
    retired = {n for s, n in named if s == "retired"} - current
    gcp = unpack_entries(catalog, "gcp3")
    return {("aws4", "current"): current, ("aws4", "retired"): retired,
            ("aws4", "legacy"): {n for s, n in named if s == "legacy"} - current - retired,
            ("azure2", "current"): {e["name"] for e in unpack_entries(catalog, "azure2")},
            ("azure2", "legacy"): set(catalog.get("azure2", {}).get("legacy", [])),
            ("gcp3", "core"): {e["name"] for e in gcp if e["form"] == "core"},
            ("gcp3", "categories"): {e["name"] for e in gcp if e["form"] == "category"}}


def assemble(tag: str, source: dict[str, str], images: list[str], built: str | None = None) -> dict:
    azure, azure_legacy, case = parse_azure(source["Sidebar-Azure2.js"], images)
    libraries = {"aws4": parse_aws(source["Sidebar-AWS4.js"], source["Sidebar-AWS4b.js"]), "azure2": azure,
                 "gcp3": parse_gcp3(source["Sidebar-GCP3.js"])}
    palettes, prefixes, rows = pack_entries(libraries)
    catalog = {
        "about": "Every AWS, Azure and Google Cloud palette entry draw.io offers at one release, generated by "
                 "tooling/build_icon_catalog.py in the Proj-Agent_Packs repository. Read by check_drawio.py; look an "
                 "icon up with `check_drawio.py --find`. Do not edit by hand. Each entry row is [name, form, status, "
                 "title, palette, w, h, prefix, style]: the palette title is palettes[palette], and the full style is "
                 "prefixes[prefix] + style, or style alone when prefix is -1. Styles omit the palette's connection "
                 "points, which do not change how an icon draws.",
        "schema": SCHEMA,
        "drawio_version": tag.lstrip("v"),
        "built": built or dt.date.today().isoformat(),
        "palettes": palettes,
        "prefixes": prefixes,
        "aws4": {"entries": rows["aws4"]},
        "azure2": {"entries": rows["azure2"], "legacy": azure_legacy, "case_mismatch": case},
        "gcp3": {"entries": rows["gcp3"]},
    }
    found = lists(catalog)
    for library, kind in LISTS:
        if not found[(library, kind)] and (library, kind) != ("azure2", "legacy"):
            raise SourceError(f"parsing found no {library} {kind} icons; the draw.io source layout may have changed")
    return catalog


def build(tag: str) -> dict:
    """Fetch draw.io's source at a tag and assemble the catalog. Raises SourceError when anything cannot be fetched
    or read."""
    try:
        if tag == "latest":
            tag = get_json(f"{API}/releases/latest")["tag_name"]
        source = {name: get(RAW.format(tag=tag, name=name)).decode("utf-8")
                  for name in ("Sidebar-AWS4.js", "Sidebar-AWS4b.js", "Sidebar-Azure2.js", "Sidebar-GCP3.js")}
        tree = get_json(f"{API}/git/trees/{tag}?recursive=1")
        if tree.get("truncated"):
            raise SourceError("the draw.io file tree came back truncated; cannot list the Azure images")
        images = [t["path"][len(AZURE_IMAGES):] for t in tree["tree"]
                  if t["path"].startswith(AZURE_IMAGES) and t["type"] == "blob"]
    except (KeyError, TypeError, AttributeError, UnicodeDecodeError) as exc:
        raise SourceError(f"draw.io's release or file listing has an unexpected shape: {exc!r}") from exc
    return assemble(tag, source, images)


def preference_paths(preferences: dict) -> list[str]:
    """Every Azure path the skill's hand-maintained icon_preferences.json names."""
    paths = []
    for rule in preferences.get("azure2", []):
        paths += [rule.get("preferred", "")] + list(rule.get("superseded", {})) + list(rule.get("same_icon", []))
    return [p for p in paths if p]


def stale_preferences(catalog: dict, preferences: dict) -> list[str]:
    """A difference line when icon_preferences.json names an Azure path the catalog does not offer as current."""
    offered = lists(catalog)[("azure2", "current")]
    missing = sorted(p for p in preference_paths(preferences) if p not in offered)
    if not missing:
        return []
    return [f"icon_preferences.json names Azure paths the catalog no longer offers: {', '.join(missing)}; re-verify "
            "those rules against Microsoft's current icon sets"]


def differences(old: dict, new: dict) -> list[str]:
    lines = []
    before_lists, after_lists = lists(old), lists(new)
    for library, kind in LISTS:
        before, after = before_lists[(library, kind)], after_lists[(library, kind)]
        if before != after:
            added, removed = sorted(after - before), sorted(before - after)
            lines.append(f"{library} {kind}: +{len(added)} -{len(removed)}"
                         + (f"; added {', '.join(added[:25])}{' ...' if len(added) > 25 else ''}" if added else "")
                         + (f"; removed {', '.join(removed[:25])}{' ...' if len(removed) > 25 else ''}" if removed else ""))
    if old.get("schema", 1) < SCHEMA:
        lines.append("the committed catalog uses the older name-list layout; regenerate it")
        return lines
    changed = []
    for library in ("aws4", "azure2", "gcp3"):
        styles: dict[tuple, list[list[str]]] = {}
        for side, catalog in enumerate((old, new)):
            for entry in unpack_entries(catalog, library):
                key = (entry["status"], entry["form"], entry["name"], entry["title"], entry["palette"])
                styles.setdefault(key, [[], []])[side].append(entry["style"])
        changed += [f"{library} {key[1]} {key[2] or key[3]}" for key, (before, after) in styles.items()
                    if before and after and sorted(before) != sorted(after)]
    if changed:
        lines.append(f"palette styles changed: {len(changed)}; {', '.join(changed[:25])}{' ...' if len(changed) > 25 else ''}")
    if old.get("azure2", {}).get("case_mismatch") != new["azure2"]["case_mismatch"]:
        lines.append(f"azure2 palette paths whose letter case differs from the file: {new['azure2']['case_mismatch']}")
    return lines


def dump(value, indent: str = "") -> str:
    """JSON with one list element per line, so a regenerated catalog diffs entry by entry."""
    inner = indent + " "
    if isinstance(value, dict) and value:
        items = [f"{inner}{json.dumps(k)}: {dump(v, inner)}" for k, v in value.items()]
        return "{\n" + ",\n".join(items) + "\n" + indent + "}"
    if isinstance(value, list) and value:
        return "[\n" + ",\n".join(inner + json.dumps(v, ensure_ascii=False) for v in value) + "\n" + indent + "]"
    return json.dumps(value, ensure_ascii=False)


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    parser.add_argument("--tag", default="latest")
    parser.add_argument("--check", action="store_true")
    parser.add_argument("--markdown")
    args = parser.parse_args()
    # Exit 1 must mean only "draw.io's libraries changed", so every failure to get that far exits 2.
    try:
        new = build(args.tag)
        preferences = json.loads(PREFERENCES.read_text(encoding="utf-8")) if PREFERENCES.is_file() else {}
        old = json.loads(CATALOG.read_text(encoding="utf-8")) if args.check and CATALOG.is_file() else {}
    except SourceError as exc:
        print(f"cannot build the catalog from draw.io {args.tag}: {exc}", file=sys.stderr)
        return 2
    except Exception as exc:  # noqa: BLE001  # an unexpected failure is still a failed run, not a change
        print(f"cannot build the catalog from draw.io {args.tag}: unexpected {exc!r}", file=sys.stderr)
        return 2
    found = lists(new)
    counts = ", ".join(f"{lib} {kind} {len(found[(lib, kind)])}" for lib, kind in LISTS)
    stale = stale_preferences(new, preferences)
    if not args.check:
        CATALOG.parent.mkdir(parents=True, exist_ok=True)
        CATALOG.write_text(dump(new) + "\n", encoding="utf-8")
        print(f"wrote {CATALOG.relative_to(REPO).as_posix()} from draw.io {new['drawio_version']}: {counts}; "
              f"azure2 case mismatches {len(new['azure2']['case_mismatch'])}")
        for line in stale:
            print(f"warning: {line}", file=sys.stderr)
        return 0
    try:
        diff = differences(old, new) + stale
    except Exception as exc:  # noqa: BLE001  # a committed catalog that cannot be read is a failed run, not a change
        print(f"cannot compare with the committed catalog: unexpected {exc!r}", file=sys.stderr)
        return 2
    print(f"committed catalog: draw.io {old.get('drawio_version', 'none')}; checked against draw.io {new['drawio_version']}")
    print("\n".join(diff) if diff else "icon lists and palette styles unchanged")
    if diff and args.markdown:
        body = [f"draw.io **{new['drawio_version']}** changed the icon libraries that the shared diagram skills check "
                f"(the committed catalog was built from draw.io {old.get('drawio_version', 'none')}).", ""]
        body += [f"- {line}" for line in diff]
        body += ["", "To adopt it: run `python tooling/build_icon_catalog.py --tag v" + new["drawio_version"] + "`, then "
                 "`python tooling/sync_shared.py`, review `shared-primitives/skills/diagram-validation-and-evidence/scripts/icon_preferences.json` "
                 "and `shared-primitives/skills/drawio-core-generation/references/providers.md` for anything the change "
                 "makes wrong, and open a pull request."]
        Path(args.markdown).write_text("\n".join(body) + "\n", encoding="utf-8")
    return 1 if diff else 0


if __name__ == "__main__":
    sys.exit(main())
