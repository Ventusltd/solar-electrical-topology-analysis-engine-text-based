from __future__ import annotations

from pathlib import Path
import subprocess

import pytest


ROOT = Path(__file__).resolve().parents[1]


def run_git(*args: str) -> subprocess.CompletedProcess[str]:
    return subprocess.run(
        ["git", *args],
        cwd=ROOT,
        check=False,
        capture_output=True,
        text=True,
        timeout=10,
    )


@pytest.mark.parametrize(
    "candidate",
    (
        "__pycache__/module.cpython-311.pyc",
        ".venv/bin/python",
        "build/lib/package.py",
        "dist/package.whl",
        "src/package.egg-info/PKG-INFO",
        ".pytest_cache/v/cache/nodeids",
        ".ruff_cache/content",
        ".mypy_cache/3.11/cache.json",
        "node_modules/package/index.js",
        ".microbuild/candidates/reference-inverter-block.json",
        ".DS_Store",
    ),
)
def test_declared_generated_candidates_are_ignored(candidate: str) -> None:
    completed = run_git("check-ignore", "--no-index", "--quiet", candidate)
    assert completed.returncode == 0, (
        f"expected generated candidate to be ignored: {candidate}\n"
        f"stdout={completed.stdout!r}\nstderr={completed.stderr!r}"
    )


def test_no_tracked_engineering_file_becomes_ignored() -> None:
    completed = run_git("ls-files", "-ci", "--exclude-standard")
    assert completed.returncode == 0, completed.stderr
    assert completed.stdout == "", (
        "tracked files must never be hidden by the root .gitignore:\n"
        + completed.stdout
    )


def test_repository_tree_is_clean_after_python_suite_setup() -> None:
    completed = run_git("status", "--porcelain=v1", "--untracked-files=all")
    assert completed.returncode == 0, completed.stderr
    assert completed.stdout == "", (
        "the Python validation setup left repository state behind:\n"
        + completed.stdout
    )
