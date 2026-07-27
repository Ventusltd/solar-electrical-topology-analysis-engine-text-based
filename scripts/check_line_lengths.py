#!/usr/bin/env python3
"""Fail when active topology source lines exceed the reviewable limit."""

from __future__ import annotations

from pathlib import Path
import sys


LIMIT = 100
ROOT = Path(__file__).resolve().parents[1]
PATTERNS = (
    "src/solar_topology/**/*.py",
    "scripts/**/*.py",
    "tests/**/*.py",
    "tests/**/*.js",
    "v8-leapfrog/*.js",
    "v8-leapfrog/*.html",
    "v8-leapfrog/*.css",
    ".github/workflows/*.yml",
    ".github/workflows/*.yaml",
    "pyproject.toml",
)


def active_files() -> tuple[Path, ...]:
    files: set[Path] = set()
    for pattern in PATTERNS:
        files.update(
            path
            for path in ROOT.glob(pattern)
            if path.is_file()
        )
    return tuple(sorted(files))


def violations(path: Path) -> list[tuple[int, int]]:
    result = []
    for number, line in enumerate(
        path.read_text(encoding="utf-8").splitlines(),
        start=1,
    ):
        width = len(line.expandtabs(4))
        if width > LIMIT:
            result.append((number, width))
    return result


def main() -> int:
    failures: list[str] = []
    for path in active_files():
        for number, width in violations(path):
            relative = path.relative_to(ROOT).as_posix()
            failures.append(f"{relative}:{number}: {width} > {LIMIT}")

    if failures:
        print("Line-length failures:")
        for failure in failures:
            print(f"  {failure}")
        return 1

    print(
        f"Line-length check passed for {len(active_files())} active files "
        f"at <= {LIMIT} characters."
    )
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
