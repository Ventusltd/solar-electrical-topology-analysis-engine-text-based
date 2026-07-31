#!/usr/bin/env python3
"""Build, install and exercise the public Build 025 API outside the checkout."""

from __future__ import annotations

import json
import os
from pathlib import Path
import shutil
import subprocess
import sys
import tempfile


ROOT = Path(__file__).resolve().parents[1]


def run(command: list[str], *, cwd: Path, env: dict[str, str] | None = None) -> None:
    subprocess.run(
        command,
        cwd=cwd,
        env=env,
        check=True,
        text=True,
    )


def venv_python(venv: Path) -> Path:
    if os.name == "nt":
        return venv / "Scripts" / "python.exe"
    return venv / "bin" / "python"


def main() -> int:
    with tempfile.TemporaryDirectory(prefix="solar-topology-wheel-") as raw:
        workspace = Path(raw).resolve()
        dist = workspace / "dist"
        environment = workspace / "venv"
        probe_dir = workspace / "probe"
        dist.mkdir()
        probe_dir.mkdir()

        run(
            [
                sys.executable,
                "-m",
                "build",
                "--wheel",
                "--outdir",
                str(dist),
            ],
            cwd=ROOT,
        )
        wheels = sorted(dist.glob("*.whl"))
        if len(wheels) != 1:
            raise RuntimeError(f"expected one wheel, found {wheels}")

        run([sys.executable, "-m", "venv", str(environment)], cwd=workspace)
        python = venv_python(environment)
        run(
            [
                str(python),
                "-m",
                "pip",
                "install",
                "--disable-pip-version-check",
                str(wheels[0]),
            ],
            cwd=workspace,
        )

        probe = probe_dir / "probe.py"
        probe.write_text(
            """from __future__ import annotations

import importlib.metadata
import json
import math
import os
from pathlib import Path

import array_engine
import geometry_authority
import solar_topology.array as array_api

source_root = Path(os.environ["SOURCE_ROOT"]).resolve()
module_paths = {
    "solar_topology.array": Path(array_api.__file__).resolve(),
    "array_engine": Path(array_engine.__file__).resolve(),
    "geometry_authority": Path(geometry_authority.__file__).resolve(),
}
for name, path in module_paths.items():
    if path.is_relative_to(source_root):
        raise AssertionError(f"{name} resolved from repository source: {path}")

first = array_api.compare_reference_24_by_30()
second = array_api.compare_reference_24_by_30()
if first.comparison_hash != second.comparison_hash:
    raise AssertionError("strategy comparison is not deterministic")
if first.sequential.receipt_hash != second.sequential.receipt_hash:
    raise AssertionError("sequential Build 025 receipt is not deterministic")
if first.leapfrog.receipt_hash != second.leapfrog.receipt_hash:
    raise AssertionError("leapfrog Build 025 receipt is not deterministic")

sequential = first.sequential.routing.metrics
leapfrog = first.leapfrog.routing.metrics
expected = {
    "sequential_total_m": 2513.328,
    "leapfrog_total_m": 2560.128,
    "field_reduction_m": 798.288,
    "factory_increase_m": 845.088,
    "total_change_m": 46.8,
}
actual = {
    "sequential_total_m": sequential.total_circuit_conductor_length_m,
    "leapfrog_total_m": leapfrog.total_circuit_conductor_length_m,
    "field_reduction_m": (
        sequential.inverter_home_run_length_m
        - leapfrog.inverter_home_run_length_m
    ),
    "factory_increase_m": (
        leapfrog.series_interconnect_length_m
        - sequential.series_interconnect_length_m
    ),
    "total_change_m": (
        leapfrog.total_circuit_conductor_length_m
        - sequential.total_circuit_conductor_length_m
    ),
}
for key, expected_value in expected.items():
    if not math.isclose(actual[key], expected_value, rel_tol=0.0, abs_tol=1e-9):
        raise AssertionError(
            f"installed API {key}={actual[key]!r}, expected {expected_value!r}"
        )

payload = {
    "pass": True,
    "distribution_version": importlib.metadata.version(
        "solar-electrical-topology-engine"
    ),
    "authority_status": array_api.ARRAY_AUTHORITY_STATUS,
    "migration_stage": array_api.ARRAY_AUTHORITY_MIGRATION_STAGE,
    "comparison_hash": first.comparison_hash,
    "module_paths": {name: str(path) for name, path in module_paths.items()},
    "metrics": actual,
}
print(json.dumps(payload, sort_keys=True))
""",
            encoding="utf-8",
        )

        child_env = os.environ.copy()
        child_env.pop("PYTHONPATH", None)
        child_env["PYTHONNOUSERSITE"] = "1"
        child_env["SOURCE_ROOT"] = str(ROOT)
        run([str(python), str(probe)], cwd=probe_dir, env=child_env)

        shutil.rmtree(dist, ignore_errors=True)

    return 0


if __name__ == "__main__":
    raise SystemExit(main())
