"""Disposable B026-05 current-head bundle hook; never merge into production."""

from __future__ import annotations

import atexit
import base64
import hashlib
import json
import os
from pathlib import Path
import subprocess
import sys
import tempfile
import time
import zipfile


ROOT = Path(__file__).resolve().parents[1]
REPORT = ROOT / "v10-development" / "recovery" / "validation" / "V10_VALIDATION_LATEST.json"
EXCLUDED_PARTS = {
    ".git",
    ".microbuild",
    ".pytest_cache",
    "__pycache__",
    "build",
    "dist",
    "node_modules",
}


def _run(command: list[str], *, cwd: Path) -> None:
    subprocess.run(command, cwd=cwd, check=True, text=True)


def _repository_zip(target: Path) -> None:
    with zipfile.ZipFile(target, "w", compression=zipfile.ZIP_DEFLATED) as archive:
        for path in sorted(ROOT.rglob("*")):
            relative = path.relative_to(ROOT)
            if not path.is_file():
                continue
            if any(part in EXCLUDED_PARTS or part.endswith(".egg-info") for part in relative.parts):
                continue
            if path.suffix == ".pyc":
                continue
            archive.write(path, relative.as_posix())


def _write_bundle() -> None:
    started = time.monotonic()
    payload = json.loads(REPORT.read_text(encoding="utf-8"))
    try:
        with tempfile.TemporaryDirectory(prefix="b026-05-bundle-") as raw:
            workspace = Path(raw)
            wheelhouse = workspace / "wheelhouse"
            wheelhouse.mkdir()

            _run(
                [
                    sys.executable,
                    "-m",
                    "build",
                    "--wheel",
                    "--outdir",
                    str(wheelhouse),
                ],
                cwd=ROOT,
            )
            _run(
                [
                    sys.executable,
                    "-m",
                    "pip",
                    "download",
                    "--dest",
                    str(wheelhouse),
                    "--only-binary=:all:",
                    "--platform",
                    "manylinux_2_28_x86_64",
                    "--python-version",
                    "3.13",
                    "--implementation",
                    "cp",
                    "--abi",
                    "cp313",
                    "duckdb>=1.4,<2",
                    "numpy>=1.26",
                    "pint>=0.24",
                    "pytest>=8",
                    "build>=1.2",
                    "setuptools>=68",
                    "wheel",
                ],
                cwd=ROOT,
            )

            repository_zip = workspace / "repository.zip"
            _repository_zip(repository_zip)
            bundle = workspace / "b026-05-local-bundle.zip"
            with zipfile.ZipFile(bundle, "w", compression=zipfile.ZIP_DEFLATED) as archive:
                archive.write(repository_zip, "repository.zip")
                for wheel in sorted(wheelhouse.glob("*.whl")):
                    archive.write(wheel, f"wheelhouse/{wheel.name}")

            raw_bundle = bundle.read_bytes()
            payload["b026_05_local_bundle"] = {
                "encoding": "base64-zip",
                "sha256": "sha256:" + hashlib.sha256(raw_bundle).hexdigest(),
                "size_bytes": len(raw_bundle),
                "origin_head": "7ab62ad2fbe8915cbbe5a5bb3db6610afc1688a2",
                "python_target": "CPython 3.13 / manylinux_2_28_x86_64",
                "generated_seconds": round(time.monotonic() - started, 3),
                "data": base64.b64encode(raw_bundle).decode("ascii"),
            }
    except Exception as exc:
        payload["pass"] = False
        payload.setdefault("results", []).append(
            {
                "name": "b026-05-local-bundle",
                "command": [],
                "cwd": ".",
                "return_code": 1,
                "pass": False,
                "duration_seconds": round(time.monotonic() - started, 3),
                "output": f"bundle creation failed: {type(exc).__name__}: {exc}",
            }
        )
    REPORT.write_text(json.dumps(payload, indent=2, sort_keys=True) + "\n", encoding="utf-8")


if (
    os.environ.get("GITHUB_ACTIONS") == "true"
    and Path(sys.argv[0]).name == "run_v10_validation.py"
):
    atexit.register(_write_bundle)
