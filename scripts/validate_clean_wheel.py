#!/usr/bin/env python3
"""Build, install and exercise the public Build 025 API outside the checkout."""

from __future__ import annotations

import os
from pathlib import Path
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

import hashlib
import importlib.metadata
import json
import math
import os
from pathlib import Path
import sys

import array_engine
import geometry_authority
import solar_topology as topology_api
import solar_topology.array as array_api
import solar_topology.equipment_profiles as equipment
import solar_topology.resistance_qualification as qualification

source_root = Path(os.environ["SOURCE_ROOT"]).resolve()
module_paths = {
    "solar_topology": Path(topology_api.__file__).resolve(),
    "solar_topology.array": Path(array_api.__file__).resolve(),
    "solar_topology.equipment_profiles": Path(equipment.__file__).resolve(),
    "solar_topology.resistance_qualification": Path(
        qualification.__file__
    ).resolve(),
    "array_engine": Path(array_engine.__file__).resolve(),
    "geometry_authority": Path(geometry_authority.__file__).resolve(),
}
for name, path in module_paths.items():
    if path.is_relative_to(source_root):
        raise AssertionError(f"{name} resolved from repository source: {path}")

if array_engine is not sys.modules["solar_topology.array.array_engine"]:
    raise AssertionError("legacy array_engine import is not the packaged authority")
if geometry_authority is not sys.modules[
    "solar_topology.array.geometry_authority"
]:
    raise AssertionError(
        "legacy geometry_authority import is not the packaged authority"
    )
for name in ("array_engine", "geometry_authority"):
    normalised = str(module_paths[name]).replace("\\\\", "/")
    if "/solar_topology/array/" not in normalised:
        raise AssertionError(f"{name} did not resolve inside packaged array authority")
if array_api.ARRAY_AUTHORITY_MIGRATION_STAGE != "build-025.5-package-authority":
    raise AssertionError("installed array API reports the wrong migration stage")

qualification_exports = (
    "RESISTANCE_QUALIFICATION_SCHEMA_VERSION",
    "ResistanceSourceAssessment",
    "ResistanceSourceStatus",
    "assess_resistance_source",
    "resistance_source_assessment_hash",
    "resistance_source_assessment_json",
    "resistance_source_assessment_payload",
)
for name in qualification_exports:
    if name not in topology_api.__all__:
        raise AssertionError(f"qualification export missing from package API: {name}")
    if topology_api.public_api_status(name) != topology_api.ApiStatus.PROVISIONAL:
        raise AssertionError(f"qualification export is not explicitly provisional: {name}")
if topology_api.assess_resistance_source is not qualification.assess_resistance_source:
    raise AssertionError("top-level qualification function is not the module authority")
if topology_api.ResistanceSourceStatus is not qualification.ResistanceSourceStatus:
    raise AssertionError("top-level qualification status is not the module authority")
if (
    topology_api.resistance_source_assessment_payload
    is not qualification.resistance_source_assessment_payload
):
    raise AssertionError("top-level assessment payload is not the module authority")
if (
    topology_api.resistance_source_assessment_json
    is not qualification.resistance_source_assessment_json
):
    raise AssertionError("top-level assessment JSON is not the module authority")
if (
    topology_api.resistance_source_assessment_hash
    is not qualification.resistance_source_assessment_hash
):
    raise AssertionError("top-level assessment hash is not the module authority")

qualification_results = {}
for product in (
    topology_api.FACTORY_LEAD_4MM2,
    topology_api.EXTERNAL_STRING_6MM2,
):
    assessment = topology_api.assess_resistance_source(
        product.resolved_resistance
    )
    if assessment.status != topology_api.ResistanceSourceStatus.CANDIDATE:
        raise AssertionError(
            f"generic product {product.product_id} was unexpectedly promoted"
        )
    if assessment.reasons != (
        "SOURCE_REVISION_PLACEHOLDER",
        "VERIFICATION_NOT_VERIFIED",
    ):
        raise AssertionError(
            f"unexpected qualification reasons for {product.product_id}: "
            f"{assessment.reasons!r}"
        )

    expected_payload = {
        "schema_version": assessment.schema_version,
        "record_hash": assessment.record_hash,
        "status": str(assessment.status),
        "reasons": list(assessment.reasons),
    }
    expected_json = json.dumps(
        expected_payload,
        sort_keys=True,
        separators=(",", ":"),
        ensure_ascii=False,
    )
    expected_hash = "sha256:" + hashlib.sha256(
        expected_json.encode("utf-8")
    ).hexdigest()

    actual_payload = topology_api.resistance_source_assessment_payload(assessment)
    actual_json = topology_api.resistance_source_assessment_json(assessment)
    actual_hash = topology_api.resistance_source_assessment_hash(assessment)
    if actual_payload != expected_payload:
        raise AssertionError(
            f"unexpected assessment payload for {product.product_id}: "
            f"{actual_payload!r}"
        )
    if actual_json != expected_json:
        raise AssertionError(
            f"unexpected assessment JSON for {product.product_id}: "
            f"{actual_json!r}"
        )
    if actual_hash != expected_hash:
        raise AssertionError(
            f"unexpected assessment hash for {product.product_id}: "
            f"{actual_hash!r}"
        )
    if qualification.resistance_source_assessment_payload(
        assessment
    ) != expected_payload:
        raise AssertionError("module and package assessment payloads differ")
    if qualification.resistance_source_assessment_json(
        assessment
    ) != expected_json:
        raise AssertionError("module and package assessment JSON differ")
    if qualification.resistance_source_assessment_hash(
        assessment
    ) != expected_hash:
        raise AssertionError("module and package assessment hashes differ")

    qualification_results[product.product_id] = {
        "status": str(assessment.status),
        "record_hash": assessment.record_hash,
        "reasons": list(assessment.reasons),
        "assessment_payload": actual_payload,
        "assessment_json": actual_json,
        "assessment_hash": actual_hash,
    }

equipment_exports = (
    "EQUIPMENT_PROFILE_SCHEMA_VERSION",
    "GENERIC_REFERENCE_CONTRACT_REVISION",
    "GENERIC_REFERENCE_EQUIPMENT_CONTRACT",
    "ReferenceEquipmentContract",
    "build_generic_reference_equipment_contract",
    "reference_equipment_contract_payload",
    "reference_equipment_contract_json",
    "reference_equipment_contract_hash",
    "reference_equipment_missing_evidence",
    "validate_reference_equipment_contract",
)
for name in equipment_exports:
    if name not in topology_api.__all__:
        raise AssertionError(f"equipment export missing from package API: {name}")
    if topology_api.public_api_status(name) != topology_api.ApiStatus.PROVISIONAL:
        raise AssertionError(f"equipment export is not explicitly provisional: {name}")
if topology_api.ReferenceEquipmentContract is not equipment.ReferenceEquipmentContract:
    raise AssertionError("top-level equipment contract type is not module authority")
if topology_api.build_generic_reference_equipment_contract is not (
    equipment.build_generic_reference_equipment_contract
):
    raise AssertionError("top-level equipment builder is not module authority")
if topology_api.reference_equipment_contract_hash is not (
    equipment.reference_equipment_contract_hash
):
    raise AssertionError("top-level equipment hash is not module authority")

contract = topology_api.build_generic_reference_equipment_contract()
second_contract = topology_api.build_generic_reference_equipment_contract()
if contract != second_contract:
    raise AssertionError("generic equipment contract is not deterministic")
if contract.module_count != 720:
    raise AssertionError("generic equipment contract does not contain 720 modules")
if not math.isclose(contract.string_rated_power_kwp, 19.8, abs_tol=1e-12):
    raise AssertionError("generic string is not 19.8 kWp")
if not math.isclose(contract.dc_nameplate_power_kwp, 475.2, abs_tol=1e-12):
    raise AssertionError("generic reference block is not 475.2 kWp")
if contract.inverter.apparent_power_kva.value != 352.0:
    raise AssertionError("generic inverter is not 352 kVA")
if not math.isclose(contract.dc_ac_nameplate_ratio, 1.35, abs_tol=1e-12):
    raise AssertionError("generic reference block does not have 1.35 DC/AC ratio")
if len(contract.inverter.dc_inputs) != 24:
    raise AssertionError("generic inverter does not expose 24 physical inputs")
if len({item.input_id for item in contract.inverter.dc_inputs}) != 24:
    raise AssertionError("generic physical input identifiers are not unique")
if len(
    {
        terminal
        for item in contract.inverter.dc_inputs
        for terminal in (item.positive_terminal_id, item.negative_terminal_id)
    }
) != 48:
    raise AssertionError("generic physical input terminal identifiers are not unique")
if any(item.mppt_id.value is not None for item in contract.inverter.dc_inputs):
    raise AssertionError("generic physical inputs silently invented MPPT assignments")
if contract.inverter.internal_dc_topology.value != "unknown":
    raise AssertionError("generic internal DC topology was silently resolved")
if contract.inverter.reverse_current_blocking.value != "unknown":
    raise AssertionError("generic reverse-current blocking was silently resolved")
if contract.inverter.pce_backfeed_current_a.value is not None:
    raise AssertionError("generic PCE backfeed was silently invented")

contract_payload = topology_api.reference_equipment_contract_payload(contract)
contract_json = topology_api.reference_equipment_contract_json(contract)
contract_hash = topology_api.reference_equipment_contract_hash(contract)
missing_evidence = topology_api.reference_equipment_missing_evidence(contract)
if contract_payload != equipment.reference_equipment_contract_payload(contract):
    raise AssertionError("module and package equipment payloads differ")
if contract_json != equipment.reference_equipment_contract_json(contract):
    raise AssertionError("module and package equipment JSON differ")
if contract_hash != equipment.reference_equipment_contract_hash(contract):
    raise AssertionError("module and package equipment hashes differ")
if contract_hash != topology_api.reference_equipment_contract_hash(second_contract):
    raise AssertionError("equipment contract hash is not deterministic")
if json.loads(contract_json) != contract_payload:
    raise AssertionError("equipment contract JSON does not reproduce payload")
if "inverter.dc_inputs.dc_input_01.mppt_id" not in missing_evidence:
    raise AssertionError("equipment contract does not expose missing MPPT mapping")
if "inverter.dc_inputs.dc_input_24.mppt_id" not in missing_evidence:
    raise AssertionError("equipment contract does not expose all input mappings")
if "inverter.internal_dc_topology" not in missing_evidence:
    raise AssertionError("equipment contract does not expose missing DC topology")
if "inverter.reverse_current_blocking" not in missing_evidence:
    raise AssertionError("equipment contract does not expose missing reverse blocking")
if "factory_leads.conductor_resistance_source" not in missing_evidence:
    raise AssertionError("factory-lead candidate resistance is not visible")
if "field_conductor.conductor_resistance_source" not in missing_evidence:
    raise AssertionError("field-conductor candidate resistance is not visible")
for prohibited in ("manufacturer_name", "project_name", "client_name", "site_name"):
    if prohibited in contract_json.lower():
        raise AssertionError(f"generic equipment contract contains {prohibited}")

equipment_result = {
    "contract_id": contract.contract_id,
    "revision": contract.revision,
    "contract_hash": contract_hash,
    "module_count": contract.module_count,
    "string_count": contract.string_count,
    "modules_per_string": contract.modules_per_string,
    "dc_nameplate_power_kwp": contract.dc_nameplate_power_kwp,
    "inverter_apparent_power_kva": contract.inverter.apparent_power_kva.value,
    "physical_dc_input_count": len(contract.inverter.dc_inputs),
    "internal_dc_topology": contract.inverter.internal_dc_topology.value,
    "reverse_current_blocking": contract.inverter.reverse_current_blocking.value,
    "missing_evidence_count": len(missing_evidence),
}

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
    "qualification": qualification_results,
    "equipment_contract": equipment_result,
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

    return 0


if __name__ == "__main__":
    raise SystemExit(main())
