from __future__ import annotations

from dataclasses import replace
import json
import math

import pytest

from solar_topology.array import WiringStrategy, reference_24_by_30_build
from solar_topology.equipment_profiles import (
    GENERIC_REFERENCE_EQUIPMENT_CONTRACT,
    reference_equipment_contract_hash,
)
from solar_topology.inverter_block import (
    INVERTER_BLOCK_SCHEMA_VERSION,
    REFERENCE_INVERTER_BLOCK_ID,
    InverterBlockEvidenceState,
    build_inverter_block,
    build_reference_inverter_block,
    inverter_block_hash,
    inverter_block_json,
    inverter_block_payload,
    validate_inverter_block_receipt,
)


def test_reference_inverter_block_binds_exact_product_boundary() -> None:
    receipt = build_reference_inverter_block()

    assert receipt.schema_version == INVERTER_BLOCK_SCHEMA_VERSION
    assert receipt.block_id == REFERENCE_INVERTER_BLOCK_ID
    assert receipt.module_count == 720
    assert receipt.string_count == 24
    assert receipt.modules_per_string == 30
    assert receipt.allocated_physical_input_count == 24
    assert len(receipt.table_receipts) == 1
    assert receipt.table_receipts[0].geometry.module_count == 720
    assert len(receipt.table_receipts[0].string_allocation.strings) == 24
    assert receipt.evidence_state is InverterBlockEvidenceState.INCOMPLETE_EVIDENCE
    assert len(receipt.equipment_missing_evidence) == 47
    assert receipt.receipt_hash.startswith("sha256:")
    assert len(receipt.receipt_hash) == 71

    contract = receipt.equipment_contract
    assert contract.module.rated_power_wp.value == 660.0
    assert math.isclose(contract.string_rated_power_kwp, 19.8, abs_tol=0.0)
    assert math.isclose(contract.dc_nameplate_power_kwp, 475.2, abs_tol=0.0)
    assert contract.inverter.apparent_power_kva.value == 352.0
    assert math.isclose(contract.dc_ac_nameplate_ratio, 1.35, abs_tol=0.0)


def test_inverter_block_payload_binds_existing_authority_hashes() -> None:
    table = reference_24_by_30_build()
    receipt = build_inverter_block(
        block_id=REFERENCE_INVERTER_BLOCK_ID,
        equipment_contract=GENERIC_REFERENCE_EQUIPMENT_CONTRACT,
        table_receipts=(table,),
    )
    payload = inverter_block_payload(receipt)
    binding = payload["table_receipts"][0]

    assert payload["equipment_contract"]["contract_hash"] == (
        reference_equipment_contract_hash(GENERIC_REFERENCE_EQUIPMENT_CONTRACT)
    )
    assert binding["build025_receipt_hash"] == table.receipt_hash
    assert binding["geometry_hash"] == table.geometry.geometry_hash
    assert binding["assignment_hash"] == table.string_allocation.assignment_hash
    assert binding["topology_hash"] == table.topology.topology_hash
    assert binding["input_allocation_hash"] == table.input_allocation.allocation_hash
    assert binding["routing_hash"] == table.routing.routing_hash
    assert binding["installed_length_hash"] == table.installed_length.receipt_hash


def test_inverter_block_preserves_unresolved_input_evidence() -> None:
    payload = inverter_block_payload(build_reference_inverter_block())
    authority = payload["input_authority"]
    evidence = payload["equipment_evidence"]

    assert authority["physical_dc_input_count"] == 24
    assert authority["allocated_physical_input_count"] == 24
    assert authority["mppt_count"] is None
    assert authority["mppt_count_verification_state"] == "unknown"
    assert authority["mppt_mapping_verification_states"] == ["unknown"]
    assert authority["internal_dc_topology"] == "unknown"
    assert authority["internal_dc_topology_verification_state"] == "unknown"
    assert authority["reverse_current_blocking"] == "unknown"
    assert authority["reverse_current_blocking_verification_state"] == "unknown"
    assert authority["pce_backfeed_current_a"] is None
    assert authority["pce_backfeed_verification_state"] == "unknown"
    assert authority["routing_fixture_mppt_labels_are_equipment_evidence"] is False
    assert evidence["state"] == "incomplete_evidence"
    assert evidence["missing_evidence_count"] == 47
    assert "inverter.internal_dc_topology" in evidence["missing_evidence"]
    assert "inverter.dc_inputs.dc_input_01.mppt_id" in evidence["missing_evidence"]


def test_inverter_block_serialisation_and_hash_are_deterministic() -> None:
    first = build_reference_inverter_block()
    second = build_reference_inverter_block()

    assert inverter_block_payload(first) == inverter_block_payload(second)
    assert inverter_block_json(first) == inverter_block_json(second)
    assert first.receipt_hash == second.receipt_hash
    assert inverter_block_hash(first) == first.receipt_hash
    assert json.loads(inverter_block_json(first)) == inverter_block_payload(first)
    validate_inverter_block_receipt(first)


def test_wiring_strategy_changes_block_hash_without_changing_product_boundary() -> None:
    sequential = build_reference_inverter_block(strategy=WiringStrategy.SEQUENTIAL)
    leapfrog = build_reference_inverter_block(strategy=WiringStrategy.LEAPFROG)

    assert sequential.receipt_hash != leapfrog.receipt_hash
    assert sequential.module_count == leapfrog.module_count == 720
    assert sequential.string_count == leapfrog.string_count == 24
    assert sequential.equipment_contract == leapfrog.equipment_contract
    assert (
        sequential.table_receipts[0].geometry.geometry_hash
        == leapfrog.table_receipts[0].geometry.geometry_hash
    )
    assert (
        sequential.table_receipts[0].string_allocation.assignment_hash
        == leapfrog.table_receipts[0].string_allocation.assignment_hash
    )


def test_duplicate_table_bindings_and_tampered_hash_are_rejected() -> None:
    table = reference_24_by_30_build()
    with pytest.raises(ValueError, match="table identifiers must be unique"):
        build_inverter_block(
            block_id=REFERENCE_INVERTER_BLOCK_ID,
            equipment_contract=GENERIC_REFERENCE_EQUIPMENT_CONTRACT,
            table_receipts=(table, table),
        )

    valid = build_reference_inverter_block()
    tampered = replace(valid, receipt_hash="sha256:" + "0" * 64)
    with pytest.raises(ValueError, match="hash mismatch"):
        validate_inverter_block_receipt(tampered)


def test_inverter_block_payload_contains_no_identity_or_standards_claims() -> None:
    serialised = inverter_block_json(build_reference_inverter_block()).lower()

    for prohibited in (
        "manufacturer_name",
        "project_name",
        "client_name",
        "site_name",
        "compliance_pass",
        "standards_compliant",
    ):
        assert prohibited not in serialised
