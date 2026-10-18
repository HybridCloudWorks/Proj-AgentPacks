#!/usr/bin/env python3
"""Run safe, non-deploying static checks for infrastructure review.

The helper detects relevant files and installed tools. By default it avoids
network restores/downloads and never runs plan, apply, deploy, what-if,
Ansible check mode, Pester, Terraform/OpenTofu tests, or target-side commands.

Exit codes:
  0: all executed checks passed (some checks may have been skipped)
  1: one or more executed checks failed
  2: invalid arguments or repository path
"""

from __future__ import annotations

import argparse
import json
import os
import shutil
import subprocess
import sys
import tempfile
from dataclasses import dataclass
from pathlib import Path
from typing import Iterable, Sequence


EXCLUDED_DIRS = {
    ".git",
    ".terraform",
    ".tox",
    ".venv",
    "__pycache__",
    "bin",
    "dist",
    "node_modules",
    "obj",
    "vendor",
}
MAX_CAPTURE = 16_000


@dataclass
class CheckResult:
    name: str
    status: str  # pass, fail, skip
    detail: str
    command: list[str] | None = None


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("root", nargs="?", default=".", help="Repository root")
    parser.add_argument(
        "--allow-downloads",
        action="store_true",
        help="Allow dependency restore/init for checks that otherwise run offline",
    )
    parser.add_argument(
        "--iac-cli",
        choices=("auto", "terraform", "tofu"),
        default="auto",
        help="Select Terraform/OpenTofu CLI when HCL files are present",
    )
    parser.add_argument(
        "--timeout",
        type=int,
        default=180,
        help="Per-command timeout in seconds (default: 180)",
    )
    return parser.parse_args()


def iter_files(root: Path) -> Iterable[Path]:
    for current, dirs, files in os.walk(root):
        dirs[:] = sorted(d for d in dirs if d not in EXCLUDED_DIRS)
        current_path = Path(current)
        for filename in sorted(files):
            yield current_path / filename


def relative(path: Path, root: Path) -> str:
    try:
        return str(path.relative_to(root))
    except ValueError:
        return str(path)


def display_command(command: Sequence[str]) -> str:
    return " ".join(repr(part) if any(ch.isspace() for ch in part) else part for part in command)


def run_command(
    name: str,
    command: Sequence[str],
    cwd: Path,
    timeout: int,
    env: dict[str, str] | None = None,
) -> CheckResult:
    try:
        result = subprocess.run(
            list(command),
            cwd=cwd,
            env=env,
            check=False,
            text=True,
            stdout=subprocess.PIPE,
            stderr=subprocess.STDOUT,
            timeout=timeout,
        )
    except FileNotFoundError:
        return CheckResult(name, "skip", f"command not installed: {command[0]}")
    except subprocess.TimeoutExpired as exc:
        output = (exc.stdout or "") if isinstance(exc.stdout, str) else ""
        return CheckResult(
            name,
            "fail",
            f"timed out after {timeout}s\n{output[-MAX_CAPTURE:]}",
            list(command),
        )
    except OSError as exc:
        return CheckResult(name, "fail", f"unable to execute: {exc}", list(command))

    output = result.stdout.strip()
    if len(output) > MAX_CAPTURE:
        output = "[output truncated]\n" + output[-MAX_CAPTURE:]
    status = "pass" if result.returncode == 0 else "fail"
    detail = output or f"exit code {result.returncode}"
    return CheckResult(name, status, detail, list(command))


def looks_like_ansible(path: Path, root: Path) -> bool:
    parts = {part.lower() for part in path.relative_to(root).parts}
    if parts.intersection({"ansible", "playbooks", "roles", "inventories", "inventory"}):
        return True
    if path.name.lower() in {"galaxy.yml", "requirements.yml", "ansible.cfg"}:
        return True
    if path.suffix.lower() not in {".yml", ".yaml"}:
        return False
    try:
        sample = path.read_text(encoding="utf-8", errors="ignore")[:8192]
    except OSError:
        return False
    markers = ("\nhosts:", "\n  hosts:", "ansible.builtin.", "ansible.windows.")
    normalized = "\n" + sample
    return any(marker in normalized for marker in markers)


def looks_like_kubernetes(path: Path, root: Path) -> bool:
    name = path.name.lower()
    if name in {"chart.yaml", "kustomization.yaml", "kustomization.yml"}:
        return True
    parts = {part.lower() for part in path.relative_to(root).parts}
    if parts.intersection({"charts", "helm", "k8s", "kubernetes", "manifests", "overlays"}):
        return True
    if path.suffix.lower() not in {".yml", ".yaml"}:
        return False
    try:
        sample = path.read_text(encoding="utf-8", errors="ignore")[:8192]
    except OSError:
        return False
    return "apiVersion:" in sample and "kind:" in sample


def module_directories(tf_files: Sequence[Path]) -> list[Path]:
    return sorted({path.parent for path in tf_files})


def choose_iac_cli(requested: str) -> str | None:
    if requested != "auto":
        return requested if shutil.which(requested) else None
    if shutil.which("terraform"):
        return "terraform"
    if shutil.which("tofu"):
        return "tofu"
    return None


def check_json(files: Sequence[Path], root: Path) -> list[CheckResult]:
    failures: list[str] = []
    checked = 0
    for path in files:
        try:
            if path.stat().st_size > 5_000_000:
                continue
            json.loads(path.read_text(encoding="utf-8"))
            checked += 1
        except (OSError, UnicodeError, json.JSONDecodeError) as exc:
            failures.append(f"{relative(path, root)}: {exc}")
    if failures:
        return [CheckResult("JSON parser validation", "fail", "\n".join(failures))]
    if checked:
        return [CheckResult("JSON parser validation", "pass", f"parsed {checked} JSON file(s)")]
    return []


def powershell_checker_script() -> str:
    return r'''param([Parameter(Mandatory=$true)][string]$Root)
$ErrorActionPreference = 'Stop'
$parseFailures = [System.Collections.Generic.List[string]]::new()
$files = Get-ChildItem -LiteralPath $Root -Recurse -File -Include *.ps1,*.psm1,*.psd1 |
  Where-Object { $_.FullName -notmatch '[\\/](\.git|node_modules|vendor|bin|obj)[\\/]' }
foreach ($file in $files) {
  $tokens = $null
  $errors = $null
  [void][System.Management.Automation.Language.Parser]::ParseFile(
    $file.FullName, [ref]$tokens, [ref]$errors)
  foreach ($parseError in $errors) {
    $parseFailures.Add("$($file.FullName):$($parseError.Extent.StartLineNumber): $($parseError.Message)")
  }
}
if ($parseFailures.Count -gt 0) {
  $parseFailures | ForEach-Object { Write-Output $_ }
  exit 1
}
Write-Output "PowerShell parser: parsed $($files.Count) file(s)."
if (Get-Module -ListAvailable -Name PSScriptAnalyzer) {
  Import-Module PSScriptAnalyzer -ErrorAction Stop
  $diagnostics = Invoke-ScriptAnalyzer -Path $Root -Recurse -ErrorAction Stop
  if ($diagnostics) {
    $diagnostics | Format-Table -AutoSize | Out-String | Write-Output
    exit 1
  }
  Write-Output 'PSScriptAnalyzer: no diagnostics.'
} else {
  Write-Output 'PSScriptAnalyzer: skipped (module not installed).'
}
'''


def has_remote_kustomize_reference(path: Path) -> bool:
    try:
        text = path.read_text(encoding="utf-8", errors="ignore").lower()
    except OSError:
        return False
    markers = ("http://", "https://", "github.com/", "git::", "oci://")
    return any(marker in text for marker in markers)


def print_result(result: CheckResult) -> None:
    label = result.status.upper()
    print(f"\n[{label}] {result.name}")
    if result.command:
        print(f"command: {display_command(result.command)}")
    if result.detail:
        print(result.detail)


def main() -> int:
    args = parse_args()
    root = Path(args.root).resolve()
    if not root.is_dir():
        print(f"ERROR: repository root does not exist: {root}", file=sys.stderr)
        return 2

    files = list(iter_files(root))
    tf_files = [p for p in files if p.suffix.lower() == ".tf"]
    bicep_files = [p for p in files if p.suffix.lower() == ".bicep"]
    ps_files = [p for p in files if p.suffix.lower() in {".ps1", ".psm1", ".psd1"}]
    yaml_files = [p for p in files if p.suffix.lower() in {".yml", ".yaml"}]
    json_files = [p for p in files if p.suffix.lower() == ".json"]
    shell_files = [p for p in files if p.suffix.lower() in {".sh", ".bash"}]
    workflow_files = [
        p
        for p in yaml_files
        if ".github" in p.parts and "workflows" in p.parts
    ]
    ansible_files = [p for p in files if looks_like_ansible(p, root)]
    kube_files = [p for p in files if looks_like_kubernetes(p, root)]
    chart_dirs = sorted({p.parent for p in files if p.name.lower() == "chart.yaml"})
    kustomization_files = [
        p
        for p in files
        if p.name.lower() in {"kustomization.yaml", "kustomization.yml"}
    ]

    print("Infrastructure review static checks")
    print(f"root: {root}")
    print(
        "detected: "
        f"terraform/opentofu={len(tf_files)}, bicep={len(bicep_files)}, "
        f"powershell={len(ps_files)}, ansible-related={len(ansible_files)}, "
        f"workflows={len(workflow_files)}, shell={len(shell_files)}, "
        f"kubernetes-related={len(kube_files)}, json={len(json_files)}"
    )

    results: list[CheckResult] = []

    if (root / ".git").exists() and shutil.which("git"):
        results.append(run_command("Git whitespace validation", ["git", "diff", "--check"], root, args.timeout))
    else:
        results.append(CheckResult("Git whitespace validation", "skip", "Git work tree not detected"))

    results.extend(check_json(json_files, root))

    iac_cli = choose_iac_cli(args.iac_cli)
    if tf_files:
        if not iac_cli:
            results.append(CheckResult("Terraform/OpenTofu checks", "skip", f"requested CLI not installed: {args.iac_cli}"))
        else:
            results.append(
                run_command(
                    f"{iac_cli} format validation",
                    [iac_cli, "fmt", "-check", "-diff", "-recursive", str(root)],
                    root,
                    args.timeout,
                )
            )
            for module_dir in module_directories(tf_files):
                rel = relative(module_dir, root)
                initialized = (module_dir / ".terraform").is_dir()
                if args.allow_downloads and not initialized:
                    results.append(
                        run_command(
                            f"{iac_cli} init without backend: {rel}",
                            [iac_cli, f"-chdir={module_dir}", "init", "-backend=false", "-input=false", "-no-color"],
                            root,
                            args.timeout,
                        )
                    )
                    initialized = (module_dir / ".terraform").is_dir()
                if initialized:
                    results.append(
                        run_command(
                            f"{iac_cli} validate: {rel}",
                            [iac_cli, f"-chdir={module_dir}", "validate", "-no-color"],
                            root,
                            args.timeout,
                        )
                    )
                else:
                    results.append(
                        CheckResult(
                            f"{iac_cli} validate: {rel}",
                            "skip",
                            "module is not initialized; use --allow-downloads to permit init -backend=false",
                        )
                    )

    if bicep_files:
        bicep = shutil.which("bicep")
        if not bicep:
            results.append(CheckResult("Bicep checks", "skip", "bicep CLI not installed"))
        else:
            for path in bicep_files:
                rel = relative(path, root)
                no_restore = [] if args.allow_downloads else ["--no-restore"]
                results.append(
                    run_command(
                        f"Bicep lint: {rel}",
                        [bicep, "lint", *no_restore, str(path)],
                        root,
                        args.timeout,
                    )
                )
                results.append(
                    run_command(
                        f"Bicep build: {rel}",
                        [bicep, "build", *no_restore, str(path), "--stdout"],
                        root,
                        args.timeout,
                    )
                )

    if ps_files:
        pwsh = shutil.which("pwsh")
        if not pwsh:
            results.append(CheckResult("PowerShell parser and analyzer", "skip", "pwsh not installed"))
        else:
            with tempfile.TemporaryDirectory(prefix="infra-review-") as temp_dir:
                checker = Path(temp_dir) / "check-powershell.ps1"
                checker.write_text(powershell_checker_script(), encoding="utf-8")
                results.append(
                    run_command(
                        "PowerShell parser and PSScriptAnalyzer",
                        [pwsh, "-NoLogo", "-NoProfile", "-NonInteractive", "-File", str(checker), "-Root", str(root)],
                        root,
                        args.timeout,
                    )
                )

    if ansible_files:
        ansible_lint = shutil.which("ansible-lint")
        if ansible_lint:
            env = os.environ.copy()
            env["ANSIBLE_LINT_SKIP_SCHEMA_UPDATE"] = "1"
            results.append(
                run_command(
                    "Ansible lint and syntax validation",
                    [ansible_lint, "--offline", "-f", "pep8", str(root)],
                    root,
                    args.timeout,
                    env,
                )
            )
        else:
            results.append(CheckResult("Ansible lint and syntax validation", "skip", "ansible-lint not installed"))

    if yaml_files:
        yamllint = shutil.which("yamllint")
        if yamllint:
            results.append(run_command("YAML lint", [yamllint, str(root)], root, args.timeout))
        else:
            results.append(CheckResult("YAML lint", "skip", "yamllint not installed"))

    if workflow_files:
        actionlint = shutil.which("actionlint")
        if actionlint:
            results.append(run_command("GitHub Actions validation", [actionlint], root, args.timeout))
        else:
            results.append(CheckResult("GitHub Actions validation", "skip", "actionlint not installed"))

    if shell_files:
        shellcheck = shutil.which("shellcheck")
        if shellcheck:
            results.append(
                run_command(
                    "ShellCheck",
                    [shellcheck, "--", *[str(path) for path in shell_files]],
                    root,
                    args.timeout,
                )
            )
        else:
            results.append(CheckResult("ShellCheck", "skip", "shellcheck not installed"))

    if chart_dirs:
        helm = shutil.which("helm")
        if helm:
            for chart_dir in chart_dirs:
                results.append(
                    run_command(
                        f"Helm lint: {relative(chart_dir, root)}",
                        [helm, "lint", str(chart_dir)],
                        root,
                        args.timeout,
                    )
                )
        else:
            results.append(CheckResult("Helm lint", "skip", "helm not installed"))

    if kustomization_files:
        kustomize = shutil.which("kustomize")
        if not kustomize:
            results.append(CheckResult("Kustomize build", "skip", "kustomize not installed"))
        else:
            for path in kustomization_files:
                if has_remote_kustomize_reference(path) and not args.allow_downloads:
                    results.append(
                        CheckResult(
                            f"Kustomize build: {relative(path.parent, root)}",
                            "skip",
                            "remote reference detected; use --allow-downloads to permit resolution",
                        )
                    )
                    continue
                results.append(
                    run_command(
                        f"Kustomize build: {relative(path.parent, root)}",
                        [kustomize, "build", str(path.parent)],
                        root,
                        args.timeout,
                    )
                )

    if not any((tf_files, bicep_files, ps_files, ansible_files, workflow_files, shell_files, kube_files, json_files)):
        results.append(CheckResult("Technology detection", "skip", "no supported infrastructure or automation files detected"))

    for result in results:
        print_result(result)

    passed = sum(result.status == "pass" for result in results)
    failed = sum(result.status == "fail" for result in results)
    skipped = sum(result.status == "skip" for result in results)
    print(f"\nSummary: passed={passed}, failed={failed}, skipped={skipped}")
    print("Skipped checks and clean static analysis still require semantic review.")
    return 1 if failed else 0


if __name__ == "__main__":
    raise SystemExit(main())
