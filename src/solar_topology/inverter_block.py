"""Deterministic inverter-block aggregate over existing engineering receipts.

This module adds no geometry, routing, electrical calculations, standards logic or
browser behaviour. It binds the existing Build 025 receipt authority to the
separate generic equipment-evidence contract without treating routing-fixture MPPT
labels as manufacturer evidence.
"""

from __future__ import annotations

from dataclasses import dataclass
from enum import StrEnum
import hashlib
import json
from typing import Iterable

from .array import (
    Build025Receipt,
    WiringStrategy,
    reference_24_by_30_build,
)
from .equipment_profiles import (
    GENERIC_REFERENCE_EQUIPMENT_CONTRACT,
    ReferenceEquipmentContract,
    reference_equipment_contract_hash,
    reference_equipment_missing_evidence,
    validate_reference_equipment_contract,
)


INVERTER_BLOCK_SCHEMA_VERSION = "globalgrid2050.solar-dc.inverter-block.v1"
REFERENCE_INVERTER_BLOCK_ID = "inverter_block_352kva_475_2kwp_001"


class InverterBlockEvidenceState(StrEnum):
    COMPLETE = "complete"
    INCOMPLETE_EVIDENCE = "incomplete_evidence"


@dataclass(frozen=True, slots=True)
class InverterBlockReceipt:
    """One inverter-centred aggregate retaining all child receipt identities."""

    block_id: str
    equipment_contract: ReferenceEquipmentContract
    table_receipts: tuple[Build025Receipt, ...]
    module_count: int
    string_count: int
    modules_per_string: int
    allocated_physical_input_count: int
    equipment_missing_evidence: tuple[str, ...]
    evidence_state: InverterBlockEvidenceState
    receipt_hash: str
    schema_version: str = INVERTER_BLOCK_SCHEMA_VERSION


def _canonical_json(payload: object) -> str:
    return json.dumps(
        payload,
        sort_keys=True,
        separators=(",", ":"),
        ensure_ascii=False,
    )


def _hash_payload(payload: object) -> str:
    digest = hashlib.sha256(_canonical_json(payload).encode("utf-8")).hexdigest()
    return f"sha256:{digest}"


def _qualified_state(value: object) -> str:
    verification_state = getattr(value, "verification_state", None)
    return str(verification_state) if verification_state is not None else "unknown"


def _table_binding(receipt: Build025Receipt) -> dict[str, object]:
    return {
        "table_id": receipt.geometry.table_id,
        "strategy": str(receipt.topology.strategy),
        "module_count": receipt.geometry.module_count,
        "string_count": len(receipt.string_allocation.strings),
        "geometry_hash": receipt.geometry.geometry_hash,
        "assignment_hash": receipt.string_allocation.assignment_hash,
        "topology_hash": receipt.topology.topology_hash,
        "input_allocation_hash": receipt.input_allocation.allocation_hash,
        "routing_hash": receipt.routing.routing_hash,
        "installed_length_hash": receipt.installed_length.receipt_hash,
        "build025_receipt_hash": receipt.receipt_hash,
        "routing_fixture_equipment_profile_id": receipt.equipment_profile.profile_id,
        "routing_fixture_inverter_id": receipt.equipment_profile.inverter_id,
    }


def inverter_block_payload(receipt: InverterBlockReceipt) -> dict[str, object]:
    """Return the deterministic aggregate payload without runtime metadata."""

    if not isinstance(receipt, InverterBlockReceipt):
        raise TypeError("receipt must be an InverterBlockReceipt")
    contract = receipt.equipment_contract
    inverter = contract.inverter
    return {
        "schema_version": receipt.schema_version,
        "block_id": receipt.block_id,
        "receipt_hash": receipt.receipt_hash,
        "equipment_contract": {
            "contract_id": contract.contract_id,
            "revision": contract.revision,
            "contract_hash": reference_equipment_contract_hash(contract),
        },
        "product_boundary": {
            "module_profile_id": contract.module.profile_id,
            "inverter_profile_id": inverter.profile_id,
            "module_technology": contract.module.technology.value,
            "module_rated_power_wp": contract.module.rated_power_wp.value,
            "modules_per_string": receipt.modules_per_string,
            "string_count": receipt.string_count,
            "module_count": receipt.module_count,
            "string_rated_power_kwp": contract.string_rated_power_kwp,
            "dc_nameplate_power_kwp": contract.dc_nameplate_power_kwp,
            "inverter_apparent_power_kva": inverter.apparent_power_kva.value,
            "dc_ac_nameplate_ratio": contract.dc_ac_nameplate_ratio,
        },
        "table_count": len(receipt.table_receipts),
        "table_receipts": [
            _table_binding(item)
            for item in receipt.table_receipts
        ],
        "input_authority": {
            "physical_dc_input_count": inverter.physical_dc_input_count.value,
            "allocated_physical_input_count": receipt.allocated_physical_input_count,
            "mppt_count": inverter.mppt_count.value,
            "mppt_count_verification_state": _qualified_state(inverter.mppt_count),
            "mppt_mapping_verification_states": sorted(
                {
                    _qualified_state(item.mppt_id)
                    for item in inverter.dc_inputs
                }
            ),
            "internal_dc_topology": inverter.internal_dc_topology.value,
            "internal_dc_topology_verification_state": _qualified_state(
                inverter.internal_dc_topology
            ),
            "reverse_current_blocking": inverter.reverse_current_blocking.value,
            "reverse_current_blocking_verification_state": _qualified_state(
                inverter.reverse_current_blocking
            ),
            "pce_backfeed_current_a": inverter.pce_backfeed_current_a.value,
            "pce_backfeed_verification_state": _qualified_state(
                inverter.pce_backfeed_current_a
            ),
            "routing_fixture_mppt_labels_are_equipment_evidence": False,
        },
        "equipment_evidence": {
            "state": str(receipt.evidence_state),
            "missing_evidence_count": len(receipt.equipment_missing_evidence),
            "missing_evidence": list(receipt.equipment_missing_evidence),
        },
    }


def inverter_block_json(receipt: InverterBlockReceipt) -> str:
    """Return canonical JSON for the inverter-block aggregate."""

    return _canonical_json(inverter_block_payload(receipt))


def inverter_block_hash(receipt: InverterBlockReceipt) -> str:
    """Recompute the aggregate hash from all bound engineering authorities."""

    payload = inverter_block_payload(receipt)
    payload.pop("receipt_hash")
    return _hash_payload(payload)


def _normalise_receipts(
    table_receipts: Iterable[Build025Receipt],
) -> tuple[Build025Receipt, ...]:
    receipts = tuple(table_receipts)
    if not receipts:
        raise ValueError("an inverter block requires at least one table receipt")
    if any(not isinstance(item, Build025Receipt) for item in receipts):
        raise TypeError("table_receipts must contain Build025Receipt objects")
    table_ids = [item.geometry.table_id for item in receipts]
    if len(table_ids) != len(set(table_ids)):
        raise ValueError("inverter-block table identifiers must be unique")
    return tuple(sorted(receipts, key=lambda item: item.geometry.table_id))


def build_inverter_block(
    *,
    block_id: str,
    equipment_contract: ReferenceEquipmentContract,
    table_receipts: Iterable[Build025Receipt],
) -> InverterBlockReceipt:
    """Bind existing table and equipment receipts into one deterministic block."""

    if not isinstance(block_id, str) or not block_id.strip():
        raise ValueError("block_id must be a non-empty string")
    if not isinstance(equipment_contract, ReferenceEquipmentContract):
        raise TypeError("equipment_contract must be a ReferenceEquipmentContract")
    validate_reference_equipment_contract(equipment_contract)
    receipts = _normalise_receipts(table_receipts)

    module_count = sum(item.geometry.module_count for item in receipts)
    string_count = sum(len(item.string_allocation.strings) for item in receipts)
    modules_per_string_values = {
        len(string_item.ordered_module_ids)
        for item in receipts
        for string_item in item.string_allocation.strings
    }
    if len(modules_per_string_values) != 1:
        raise ValueError("inverter-block strings must have one modules-per-string value")
    modules_per_string = modules_per_string_values.pop()
    allocated_inputs = [
        assignment.input_id
        for item in receipts
        for assignment in item.input_allocation.assignments
    ]
    if len(allocated_inputs) != len(set(allocated_inputs)):
        raise ValueError("physical input identifiers are duplicated across tables")

    if module_count != equipment_contract.module_count:
        raise ValueError(
            "table receipts do not match equipment-contract module count: "
            f"{module_count} != {equipment_contract.module_count}"
        )
    if string_count != equipment_contract.string_count:
        raise ValueError(
            "table receipts do not match equipment-contract string count: "
            f"{string_count} != {equipment_contract.string_count}"
        )
    if modules_per_string != equipment_contract.modules_per_string:
        raise ValueError(
            "table receipts do not match equipment-contract modules per string: "
            f"{modules_per_string} != {equipment_contract.modules_per_string}"
        )
    physical_input_count = equipment_contract.inverter.physical_dc_input_count.value
    if not isinstance(physical_input_count, int):
        raise ValueError("equipment physical DC input count is unresolved")
    if len(allocated_inputs) != string_count:
        raise ValueError("every block string must have one physical input allocation")
    if len(allocated_inputs) > physical_input_count:
        raise ValueError("allocated strings exceed equipment physical DC input count")

    missing = reference_equipment_missing_evidence(equipment_contract)
    evidence_state = (
        InverterBlockEvidenceState.INCOMPLETE_EVIDENCE
        if missing
        else InverterBlockEvidenceState.COMPLETE
    )
    preliminary = InverterBlockReceipt(
        block_id=block_id.strip(),
        equipment_contract=equipment_contract,
        table_receipts=receipts,
        module_count=module_count,
        string_count=string_count,
        modules_per_string=modules_per_string,
        allocated_physical_input_count=len(allocated_inputs),
        equipment_missing_evidence=missing,
        evidence_state=evidence_state,
        receipt_hash="",
    )
    return InverterBlockReceipt(
        block_id=preliminary.block_id,
        equipment_contract=preliminary.equipment_contract,
        table_receipts=preliminary.table_receipts,
        module_count=preliminary.module_count,
        string_count=preliminary.string_count,
        modules_per_string=preliminary.modules_per_string,
        allocated_physical_input_count=(
            preliminary.allocated_physical_input_count
        ),
        equipment_missing_evidence=preliminary.equipment_missing_evidence,
        evidence_state=preliminary.evidence_state,
        receipt_hash=inverter_block_hash(preliminary),
    )


def validate_inverter_block_receipt(receipt: InverterBlockReceipt) -> None:
    """Reject tampering without rebuilding or changing child receipts."""

    if not isinstance(receipt, InverterBlockReceipt):
        raise TypeError("receipt must be an InverterBlockReceipt")
    expected = inverter_block_hash(receipt)
    if receipt.receipt_hash != expected:
        raise ValueError("inverter-block receipt hash mismatch")
    rebuilt = build_inverter_block(
        block_id=receipt.block_id,
        equipment_contract=receipt.equipment_contract,
        table_receipts=receipt.table_receipts,
    )
    if rebuilt.receipt_hash != receipt.receipt_hash:
        raise ValueError("inverter-block receipt content is inconsistent")


def build_reference_inverter_block(
    *,
    strategy: WiringStrategy | str = WiringStrategy.LEAPFROG,
) -> InverterBlockReceipt:
    """Build the first complete 352 kVA / 475.2 kWp product fixture."""

    table_receipt = reference_24_by_30_build(strategy=strategy)
    return build_inverter_block(
        block_id=REFERENCE_INVERTER_BLOCK_ID,
        equipment_contract=GENERIC_REFERENCE_EQUIPMENT_CONTRACT,
        table_receipts=(table_receipt,),
    )


__all__ = [
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
]
