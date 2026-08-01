#!/usr/bin/env python3
"""Build a wheel and prove the inverter-block contract outside the checkout."""

from __future__ import annotations

import os
from pathlib import Path
import subprocess
import sys
import tempfile


ROOT = Path(__file__).resolve().parents[1]


def run(command: list[str], *, cwd: Path, env: dict[str, str] | None = None) -> None:
    subprocess.run(command, cwd=cwd, env=env, check=True, text=True)


def venv_python(venv: Path) -> Path:
    if os.name == "nt":
        return venv / "Scripts" / "python.exe"
    return venv / "bin" / "python"


def main() -> int:
    with tempfile.TemporaryDirectory(prefix="solar-inverter-block-wheel-") as raw:
        workspace = Path(raw).resolve()
        dist = workspace / "dist"
        environment = workspace / "venv"
        probe_dir = workspace / "probe"
        dist.mkdir()
        probe_dir.mkdir()

        run(
            [sys.executable, "-m", "build", "--wheel", "--outdir", str(dist)],
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

        probe = probe_dir / "probe_inverter_block.py"
        probe.write_text(
            '''from __future__ import annotations

import json
import math
import os
from pathlib import Path

import solar_topology as api
import solar_topology.array as array_api
import solar_topology.inverter_block as block_api

source_root = Path(os.environ["SOURCE_ROOT"]).resolve()
for module in (api, array_api, block_api):
    path = Path(module.__file__).resolve()
    if path.is_relative_to(source_root):
        raise AssertionError(f"module resolved from repository source: {path}")

exports = (
    "INVERTER_BLOCK_SCHEMA_VERSION",
    "REFERENCE_INVERTER_BLOCK_ID",
    "InverterBlockEvidenceState",
    "InverterBlockReceipt",
    "build_inverter_block",
    "build_reference_inverter_block",
    "inverter_block_hash",
    "inverter_block_json",
    "inverter_block_payload",
    "validate_inverter_block_receipt",
)
for name in exports:
    if name not in api.__all__:
        raise AssertionError(f"inverter-block export missing: {name}")
    if api.public_api_status(name) != api.ApiStatus.PROVISIONAL:
        raise AssertionError(f"inverter-block export not provisional: {name}")
    if getattr(api, name) is not getattr(block_api, name):
        raise AssertionError(f"top-level inverter-block identity differs: {name}")

first = api.build_reference_inverter_block()
second = api.build_reference_inverter_block()
api.validate_inverter_block_receipt(first)

if first != second:
    raise AssertionError("reference inverter block is not deterministic")
if first.receipt_hash != second.receipt_hash:
    raise AssertionError("reference inverter-block hash is not deterministic")
if api.inverter_block_hash(first) != first.receipt_hash:
    raise AssertionError("inverter-block receipt hash does not recompute")

payload = api.inverter_block_payload(first)
serialised = api.inverter_block_json(first)
if payload != block_api.inverter_block_payload(first):
    raise AssertionError("module and package inverter-block payloads differ")
if serialised != block_api.inverter_block_json(first):
    raise AssertionError("module and package inverter-block JSON differ")
if json.loads(serialised) != payload:
    raise AssertionError("inverter-block JSON does not reproduce its payload")

boundary = payload["product_boundary"]
expected = {
    "module_rated_power_wp": 660.0,
    "modules_per_string": 30,
    "string_count": 24,
    "module_count": 720,
    "string_rated_power_kwp": 19.8,
    "dc_nameplate_power_kwp": 475.2,
    "inverter_apparent_power_kva": 352.0,
    "dc_ac_nameplate_ratio": 1.35,
}
for key, expected_value in expected.items():
    actual = boundary[key]
    if isinstance(expected_value, float):
        if not math.isclose(actual, expected_value, rel_tol=0.0, abs_tol=1e-12):
            raise AssertionError(f"wrong {key}: {actual!r}")
    elif actual != expected_value:
        raise AssertionError(f"wrong {key}: {actual!r}")

if first.allocated_physical_input_count != 24:
    raise AssertionError("reference inverter block does not allocate 24 physical inputs")
if len(first.table_receipts) != 1:
    raise AssertionError("reference inverter block must bind one current fixture receipt")
table = first.table_receipts[0]
binding = payload["table_receipts"][0]
if binding["build025_receipt_hash"] != table.receipt_hash:
    raise AssertionError("child Build 025 receipt identity is not bound")
if binding["geometry_hash"] != table.geometry.geometry_hash:
    raise AssertionError("child geometry identity is not bound")
if binding["routing_hash"] != table.routing.routing_hash:
    raise AssertionError("child routing identity is not bound")

input_authority = payload["input_authority"]
if input_authority["mppt_count"] is not None:
    raise AssertionError("MPPT count was silently invented")
if input_authority["internal_dc_topology"] != "unknown":
    raise AssertionError("internal DC topology was silently resolved")
if input_authority["reverse_current_blocking"] != "unknown":
    raise AssertionError("reverse-current blocking was silently resolved")
if input_authority["pce_backfeed_current_a"] is not None:
    raise AssertionError("PCE backfeed was silently invented")
if input_authority["routing_fixture_mppt_labels_are_equipment_evidence"] is not False:
    raise AssertionError("routing fixture labels were promoted to equipment evidence")
if payload["equipment_evidence"]["state"] != "incomplete_evidence":
    raise AssertionError("missing equipment evidence is not visible")
if payload["equipment_evidence"]["missing_evidence_count"] != 47:
    raise AssertionError("unexpected equipment evidence count")

comparison = array_api.compare_reference_24_by_30()
expected_comparison_hash = (
    "sha256:413aa93c98d1b9fd5f9ffee4f577cfe29a6e74f48bd927a3ebe7f541545d6366"
)
if comparison.comparison_hash != expected_comparison_hash:
    raise AssertionError("established strategy comparison hash changed")

print(json.dumps({
    "pass": True,
    "block_id": first.block_id,
    "receipt_hash": first.receipt_hash,
    "equipment_contract_hash": payload["equipment_contract"]["contract_hash"],
    "build025_receipt_hash": binding["build025_receipt_hash"],
    "comparison_hash": comparison.comparison_hash,
    "module_count": first.module_count,
    "string_count": first.string_count,
    "modules_per_string": first.modules_per_string,
    "allocated_physical_input_count": first.allocated_physical_input_count,
    "evidence_state": str(first.evidence_state),
    "missing_evidence_count": len(first.equipment_missing_evidence),
}, sort_keys=True))
''',
            encoding="utf-8",
        )

        child_env = os.environ.copy()
        child_env.pop("PYTHONPATH", None)
        child_env["PYTHONNOUSERSITE"] = "1"
        child_env["SOURCE_ROOT"] = str(ROOT)
        run([str(python), str(probe)], cwd=probe_dir, env=child_env)

    return 0


if __name__ == "__main__":
    raise SystemExit(main())
