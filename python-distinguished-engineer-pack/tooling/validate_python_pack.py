"""Read-only syntax inventory helper; does not import or execute target source."""
from __future__ import annotations
import argparse
import ast
from pathlib import Path

SKIP = {".git", ".venv", "venv", "node_modules", "dist", "build", "__pycache__", ".pytest_cache"}


def inspect(root: Path) -> tuple[int, list[str]]:
    count, errors = 0, []
    for path in root.rglob("*.py"):
        if any(part in SKIP for part in path.relative_to(root).parts) or path.is_symlink():
            continue
        if not path.resolve().is_relative_to(root.resolve()):
            continue
        count += 1
        try:
            ast.parse(path.read_text(encoding="utf-8-sig"), filename=str(path))
        except (OSError, SyntaxError, UnicodeError) as exc:
            errors.append(str(path.relative_to(root)) + ": " + type(exc).__name__)
    return count, errors


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("root", nargs="?", type=Path, default=Path.cwd())
    args = parser.parse_args()
    count, errors = inspect(args.root.resolve())
    print("Parsed", count, "Python files in memory.")
    print("\n".join(errors) if errors else "Syntax inventory passed; tests, imports and runtime behavior are not established.")
    return int(bool(errors))


if __name__ == "__main__":
    raise SystemExit(main())
