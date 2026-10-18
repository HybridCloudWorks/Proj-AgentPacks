#!/usr/bin/env python3
"""Build or check the draw.io icon catalog used by the shared diagram-validation-and-evidence skill.

The catalog lists the AWS, Azure and Google Cloud icon names that draw.io's own shape libraries offer at one
release, so the skill's scripts/check_drawio.py can tell a current icon from a legacy, retired or misspelled one
without draw.io installed. It is built from draw.io's public source at a release tag:

  AWS           Sidebar-AWS4.js: the current "AWS <year>" library, and its "AWS (retired)" palette
                Sidebar-AWS4b.js: the "AWS18" library, legacy
  Azure         the img/lib/azure2 image files, and Sidebar-Azure2.js for the ones the Azure palette offers
  Google Cloud  Sidebar-GCP3.js: "Google Cloud Platform 2026", category and core product icons

Usage: python tooling/build_icon_catalog.py [--tag latest|vX.Y.Z] [--check] [--markdown OUT]
  --tag       draw.io release tag to read (default: latest)
  --check     compare with the committed catalog instead of writing it; exit 1 when an icon list differs
  --markdown  with --check, also write the differences as Markdown (used by the weekly watch issue)
"""
from __future__ import annotations

import argparse
import datetime as dt
import json
import os
import re
import sys
import urllib.request
from pathlib import Path

REPO = Path(__file__).resolve().parents[1]
CATALOG = REPO / "shared-primitives" / "skills" / "diagram-validation-and-evidence" / "scripts" / "icon_catalog.json"
API = "https://api.github.com/repos/jgraph/drawio"
RAW = "https://raw.githubusercontent.com/jgraph/drawio/{tag}/src/main/webapp/js/diagramly/sidebar/{name}"
AZURE_IMAGES = "src/main/webapp/img/lib/azure2/"
LISTS = [("aws4", "current"), ("aws4", "retired"), ("aws4", "legacy"), ("azure2", "current"), ("azure2", "legacy"),
         ("gcp3", "core"), ("gcp3", "categories")]


def get(url: str) -> bytes:
    if not url.startswith(("https://api.github.com/", "https://raw.githubusercontent.com/")):
        raise ValueError(f"only GitHub https URLs are fetched, not {url}")
    headers = {"User-Agent": "proj-agent-packs-icon-catalog", "Accept": "application/vnd.github+json"}
    token = os.environ.get("GITHUB_TOKEN") or os.environ.get("GH_TOKEN")
    if token and url.startswith("https://api.github.com/"):
        headers["Authorization"] = f"Bearer {token}"
    request = urllib.request.Request(url, headers=headers)  # noqa: S310
    # Safe: only GitHub https URLs reach this point.
    with urllib.request.urlopen(request, timeout=120) as response:  # noqa: S310  # nosec B310
        return response.read()


def function_bodies(js: str) -> dict[str, str]:
    """Map each `Sidebar.prototype.<name> = function` in a sidebar file to its source text."""
    starts = [(m.group(1), m.start()) for m in re.finditer(r"Sidebar\.prototype\.(\w+)\s*=\s*function", js)]
    return {name: js[start: starts[i + 1][1] if i + 1 < len(starts) else len(js)] for i, (name, start) in enumerate(starts)}


def aws_names(js: str) -> set[str]:
    """Every mxgraph.aws4 shape, resIcon, grIcon or prIcon name a piece of AWS sidebar source offers."""
    prefix_vars = set(re.findall(r"\bvar (\w+)\s*=[^\n]*mxgraph\.aws4\.[\"'];", js))
    names = set(re.findall(r"\bgn \+ '\.([a-z0-9_]+)", js))
    names |= set(re.findall(r"mxgraph\.aws4\.([a-z0-9_]+)", js))
    if prefix_vars:
        names |= set(re.findall(r"\b(?:" + "|".join(sorted(prefix_vars)) + r") \+ '([A-Za-z0-9_]+)[;']", js))
    names |= set(re.findall(r"\b(?:svc|res|res0)\('[^']*'\) \+ '([A-Za-z0-9_]+)[;']", js))
    names |= set(re.findall(r"\barvr \+ '([A-Za-z0-9_]+)[;']", js))
    return names


def parse_aws(aws4_js: str, aws4b_js: str) -> dict[str, list[str]]:
    bodies = function_bodies(aws4_js)
    retired_body = next((b for n, b in bodies.items() if "Retired" in n), "")
    current = aws_names(aws4_js.replace(retired_body, "")) if retired_body else aws_names(aws4_js)
    retired = aws_names(retired_body) - current
    legacy = aws_names(aws4b_js) - current - retired
    return {"current": sorted(current), "retired": sorted(retired), "legacy": sorted(legacy)}


def parse_azure(azure2_js: str, image_paths: list[str]) -> dict[str, list[str]]:
    categories = dict(re.findall(r"this\.(addAzure2\w+Palette)\([^)]*s \+ '([a-z_]+)/'\)", azure2_js))
    offered: set[str] = set()
    for name, body in function_bodies(azure2_js).items():
        category = categories.get(name)
        if category:
            offered |= {f"{category}/{f}" for f in re.findall(r"'([A-Za-z0-9_().+-]+\.svg)", body)}
    files = {p for p in image_paths if p.endswith(".svg")}
    return {"current": sorted(offered & files), "legacy": sorted(files - offered)}


def parse_gcp3(gcp3_js: str) -> dict[str, list[str]]:
    bodies = function_bodies(gcp3_js)

    def names(fragment: str) -> list[str]:
        body = next((b for n, b in bodies.items() if fragment in n), "")
        return sorted(set(re.findall(r"\bn \+ '([a-z0-9_]+);", body)))
    return {"core": names("CoreProducts"), "categories": names("Categories")}


def build(tag: str) -> dict:
    if tag == "latest":
        tag = json.loads(get(f"{API}/releases/latest"))["tag_name"]
    source = {name: get(RAW.format(tag=tag, name=name)).decode("utf-8")
              for name in ("Sidebar-AWS4.js", "Sidebar-AWS4b.js", "Sidebar-Azure2.js", "Sidebar-GCP3.js")}
    tree = json.loads(get(f"{API}/git/trees/{tag}?recursive=1"))
    if tree.get("truncated"):
        raise SystemExit("the draw.io file tree came back truncated; cannot list the Azure images")
    images = [t["path"][len(AZURE_IMAGES):] for t in tree["tree"] if t["path"].startswith(AZURE_IMAGES) and t["type"] == "blob"]
    catalog = {
        "about": "Icon names offered by draw.io's AWS, Azure and Google Cloud libraries, generated by tooling/build_icon_catalog.py "
                 "in the Proj-Agent_Packs repository. Read by check_drawio.py. Do not edit by hand.",
        "drawio_version": tag.lstrip("v"),
        "built": dt.date.today().isoformat(),
        "aws4": parse_aws(source["Sidebar-AWS4.js"], source["Sidebar-AWS4b.js"]),
        "azure2": parse_azure(source["Sidebar-Azure2.js"], images),
        "gcp3": parse_gcp3(source["Sidebar-GCP3.js"]),
    }
    for library, kind in LISTS:
        if library != "aws4" or kind == "current":
            if not catalog[library][kind] and (library, kind) != ("azure2", "legacy"):
                raise SystemExit(f"parsing found no {library} {kind} icons; the draw.io source layout may have changed")
    return catalog


def differences(old: dict, new: dict) -> list[str]:
    lines = []
    for library, kind in LISTS:
        before, after = set(old.get(library, {}).get(kind, [])), set(new[library][kind])
        if before != after:
            added, removed = sorted(after - before), sorted(before - after)
            lines.append(f"{library} {kind}: +{len(added)} -{len(removed)}"
                         + (f"; added {', '.join(added[:25])}{' ...' if len(added) > 25 else ''}" if added else "")
                         + (f"; removed {', '.join(removed[:25])}{' ...' if len(removed) > 25 else ''}" if removed else ""))
    return lines


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    parser.add_argument("--tag", default="latest")
    parser.add_argument("--check", action="store_true")
    parser.add_argument("--markdown")
    args = parser.parse_args()
    new = build(args.tag)
    counts = ", ".join(f"{lib} {kind} {len(new[lib][kind])}" for lib, kind in LISTS)
    if not args.check:
        CATALOG.parent.mkdir(parents=True, exist_ok=True)
        CATALOG.write_text(json.dumps(new, indent=0) + "\n", encoding="utf-8")
        print(f"wrote {CATALOG.relative_to(REPO).as_posix()} from draw.io {new['drawio_version']}: {counts}")
        return 0
    old = json.loads(CATALOG.read_text(encoding="utf-8")) if CATALOG.is_file() else {}
    diff = differences(old, new)
    print(f"committed catalog: draw.io {old.get('drawio_version', 'none')}; checked against draw.io {new['drawio_version']}")
    print("\n".join(diff) if diff else "icon lists unchanged")
    if diff and args.markdown:
        body = [f"draw.io **{new['drawio_version']}** changed the icon libraries that the shared diagram skills check "
                f"(the committed catalog was built from draw.io {old.get('drawio_version', 'none')}).", ""]
        body += [f"- {line}" for line in diff]
        body += ["", "To adopt it: run `python tooling/build_icon_catalog.py --tag v" + new["drawio_version"] + "`, then "
                 "`python tooling/sync_shared.py`, review `shared-primitives/skills/drawio-core-generation/references/providers.md` "
                 "for anything the change makes wrong, and open a pull request."]
        Path(args.markdown).write_text("\n".join(body) + "\n", encoding="utf-8")
    return 1 if diff else 0


if __name__ == "__main__":
    sys.exit(main())
