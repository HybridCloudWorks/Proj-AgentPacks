#!/usr/bin/env python3
"""Install a pinned APM CLI release on a CI runner (Linux, Windows or macOS) and verify its SHA-256.

Downloads the platform archive from github.com/microsoft/apm releases, checks it against the published
.sha256 file, extracts it, and appends the folder holding the executable to $GITHUB_PATH when running in
GitHub Actions. Prints that folder.

Usage: python tooling/ci_install_apm.py [--version X.Y.Z|latest] [--dest DIR]
The default version is read from tooling/apm-version.txt.
"""
from __future__ import annotations

import argparse
import hashlib
import json
import os
import platform
import shutil
import sys
import tarfile
import tempfile
import urllib.request
import zipfile
from pathlib import Path

HERE = Path(__file__).resolve().parent
RELEASES = "https://github.com/microsoft/apm/releases"
API_LATEST = "https://api.github.com/repos/microsoft/apm/releases/latest"


def asset_name() -> str:
    system, machine = platform.system().lower(), platform.machine().lower()
    arch = "arm64" if machine in ("arm64", "aarch64") else "x86_64"
    if system == "linux":
        return f"apm-linux-{arch}.tar.gz"
    if system == "darwin":
        return f"apm-darwin-{arch}.tar.gz"
    if system == "windows":
        return "apm-windows-x86_64.zip"
    raise SystemExit(f"unsupported platform: {system} {machine}")


def fetch(url: str) -> bytes:
    request = urllib.request.Request(url, headers={"User-Agent": "proj-agent-packs-ci"})
    token = os.environ.get("GITHUB_TOKEN")
    if token and "api.github.com" in url:
        request.add_header("Authorization", f"Bearer {token}")
    with urllib.request.urlopen(request, timeout=120) as response:
        return response.read()


def resolve_version(requested: str) -> str:
    if requested != "latest":
        return requested.lstrip("v")
    return json.loads(fetch(API_LATEST))["tag_name"].lstrip("v")


def safe_extract(archive: Path, dest: Path) -> None:
    root = dest.resolve()
    if archive.suffix == ".zip":
        with zipfile.ZipFile(archive) as zf:
            for member in zf.namelist():
                if not (root / member).resolve().is_relative_to(root):
                    raise SystemExit(f"unsafe path in archive: {member}")
            zf.extractall(dest)
    else:
        with tarfile.open(archive) as tf:
            for member in tf.getmembers():
                if not (root / member.name).resolve().is_relative_to(root) or member.issym() or member.islnk():
                    if member.issym() or member.islnk():
                        continue
                    raise SystemExit(f"unsafe path in archive: {member.name}")
            tf.extractall(dest, filter="data") if sys.version_info >= (3, 12) else tf.extractall(dest)


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    parser.add_argument("--version", default=(HERE / "apm-version.txt").read_text(encoding="utf-8").strip())
    parser.add_argument("--dest", default=os.path.join(os.environ.get("RUNNER_TEMP", tempfile.gettempdir()), "apm"))
    args = parser.parse_args()
    version = resolve_version(args.version)
    asset = asset_name()
    base = f"{RELEASES}/download/v{version}/{asset}"
    data = fetch(base)
    expected = fetch(base + ".sha256").decode("utf-8").split()[0].strip().lower()
    actual = hashlib.sha256(data).hexdigest()
    if actual != expected:
        raise SystemExit(f"checksum mismatch for {asset}: expected {expected}, got {actual}")
    dest = Path(args.dest)
    if dest.exists():
        shutil.rmtree(dest)
    dest.mkdir(parents=True)
    archive = dest / asset
    archive.write_bytes(data)
    safe_extract(archive, dest)
    archive.unlink()
    exe_name = "apm.exe" if platform.system().lower() == "windows" else "apm"
    exe = next((p for p in dest.rglob(exe_name) if p.is_file()), None)
    if exe is None:
        raise SystemExit(f"{exe_name} not found in {asset}")
    if os.name != "nt":
        exe.chmod(0o755)
    if os.environ.get("GITHUB_PATH"):
        with open(os.environ["GITHUB_PATH"], "a", encoding="utf-8") as handle:
            handle.write(str(exe.parent) + "\n")
    print(f"apm {version} ({asset}, sha256 verified) at {exe.parent}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
