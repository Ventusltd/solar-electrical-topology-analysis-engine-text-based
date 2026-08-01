from __future__ import annotations

from dataclasses import replace
import json
import math

import pytest

from solar_topology.circuit import EvidenceClass
from solar_topology.equipment_profiles import (
    GENERIC_REFERENCE_EQUIPMENT_CONTRACT,
    ConnectorCompatibilityState,
    InternalDcTopology,
    ModuleTechnology,
    QualifiedValue,
    ReverseCurrentBlockingState,
    build_generic_reference_equipment_contract,
    reference_equipment_contract_hash,
    reference_equipment_contract_json,
    reference_equipment_contract_payload,
    reference_equipment_missing_evidence,
    validate_reference_equipment_contract,
)
from solar_topology.evidence import VerificationState
from solar_topology.products import EXTERNAL_STRING_6MM2, FACTORY_LEAD_4MM2
from solar_topology.resistance_qualification import (
    ResistanceSourceStatus,
    assess_resistance_source,
)


def test_reference_equipment_contract_has_exact_product_boundary() -> None:
    contract = build_generic_reference_equipment_contract()

    assert contract.module.technology.value == str(ModuleTechnology.BIFACIAL)
    assert contract.module.rated_power_wp.value == 660.0
    assert contract.modules_per_string == 30
    assert contract.string_count == 24
    assert contract.module_count == 720
    assert math.isclose(contract.string_rated_power_kwp, 19.8, abs_tol=1e-12)
    assert math.isclose(contract.dc_nameplate_power_kwp, 475.2, abs_tol=1e-12)
    assert contract.inverter.apparent_power_kva.value == 352.0
    assert math.isclose(contract.dc_ac_nameplate_ratio, 1.35, abs_tol=1e-12)


def test_reference_inverter_exposes_24_unique_physical_input_pairs() -> None:
    contract = GENERIC_REFERENCE_EQUIPMENT_CONTRACT
    inputs = contract.inverter.dc_inputs

    assert contract.inverter.physical_dc_input_count.value == 24
    assert len(inputs) == 24
    assert [item.input_id for item in inputs] == [
        f"dc_input_{index:02d}" for index in range(1, 25)
    ]
    assert len({item.positive_terminal_id for item in inputs}) == 24
    assert len({item.negative_terminal_id for item in inputs}) == 24
    assert len(
        {
            terminal
            for item in inputs
            for terminal in (item.positive_terminal_id, item.negative_terminal_id)
        }
    ) == 48
    assert all(item.mppt_id.value is None for item in inputs)
    assert all(
        item.mppt_id.verification_state is VerificationState.UNKNOWN
        for item in inputs
    )


def test_internal_input_relationships_remain_explicitly_unresolved() -> None:
    inverter = GENERIC_REFERENCE_EQUIPMENT_CONTRACT.inverter

    assert inverter.mppt_count.value is None
    assert inverter.internal_dc_topology.value == str(InternalDcTopology.UNKNOWN)
    assert inverter.reverse_current_blocking.value == str(
        ReverseCurrentBlockingState.UNKNOWN
    )
    assert inverter.pce_backfeed_current_a.value is None
    assert inverter.maximum_dc_voltage_v.value is None
    assert inverter.maximum_dc_input_power_kwp.value is None
    for item in (
        inverter.mppt_count,
        inverter.internal_dc_topology,
        inverter.reverse_current_blocking,
        inverter.pce_backfeed_current_a,
        inverter.maximum_dc_voltage_v,
        inverter.maximum_dc_input_power_kwp,
    ):
        assert not item.verified


def test_connector_leads_dimensions_and_electrical_module_data_remain_missing() -> None:
    contract = GENERIC_REFERENCE_EQUIPMENT_CONTRACT
    connector = contract.connector
    module = contract.module

    assert connector.mating_compatibility.value == str(
        ConnectorCompatibilityState.UNKNOWN
    )
    assert connector.contact_resistance_ohm_per_mated_pair.value is None
    assert connector.rated_current_a.value is None
    assert connector.rated_voltage_v.value is None
    assert contract.factory_leads.positive_lead_length_m.value is None
    assert contract.factory_leads.negative_lead_length_m.value is None
    assert module.voc_v.value is None
    assert module.isc_a.value is None
    assert module.vmp_v.value is None
    assert module.imp_a.value is None
    assert module.maximum_overcurrent_protection_rating_a.value is None
    assert module.bifaciality_factor.value is None
    assert module.width_m.value is None
    assert module.length_m.value is None


def test_conductor_products_are_referenced_without_silent_promotion() -> None:
    contract = GENERIC_REFERENCE_EQUIPMENT_CONTRACT

    assert contract.factory_leads.conductor_product_id == FACTORY_LEAD_4MM2.product_id
    assert contract.field_conductor.conductor_product_id == EXTERNAL_STRING_6MM2.product_id
    assert assess_resistance_source(
        FACTORY_LEAD_4MM2.resolved_resistance
    ).status is ResistanceSourceStatus.CANDIDATE
    assert assess_resistance_source(
        EXTERNAL_STRING_6MM2.resolved_resistance
    ).status is ResistanceSourceStatus.CANDIDATE
    payload = reference_equipment_contract_payload(contract)
    assert payload["factory_leads"]["resistance_source_status"] == "candidate"
    assert payload["field_conductor"]["resistance_source_status"] == "candidate"


def test_missing_evidence_is_deterministic_and_includes_input_mapping() -> None:
    missing = reference_equipment_missing_evidence(
        GENERIC_REFERENCE_EQUIPMENT_CONTRACT
    )

    assert missing == tuple(sorted(missing))
    assert "inverter.dc_inputs.dc_input_01.mppt_id" in missing
    assert "inverter.dc_inputs.dc_input_24.mppt_id" in missing
    assert "inverter.internal_dc_topology" in missing
    assert "inverter.reverse_current_blocking" in missing
    assert "inverter.pce_backfeed_current_a" in missing
    assert "connector.mating_compatibility" in missing
    assert "factory_leads.conductor_resistance_source" in missing
    assert "field_conductor.conductor_resistance_source" in missing
    assert "module.rated_power_wp" not in missing
    assert "inverter.apparent_power_kva" not in missing
    assert "inverter.physical_dc_input_count" not in missing


def test_contract_serialisation_and_hash_are_deterministic() -> None:
    first = build_generic_reference_equipment_contract()
    second = build_generic_reference_equipment_contract()

    assert first == second
    assert reference_equipment_contract_payload(first) == (
        reference_equipment_contract_payload(second)
    )
    assert reference_equipment_contract_json(first) == (
        reference_equipment_contract_json(second)
    )
    assert reference_equipment_contract_hash(first) == (
        reference_equipment_contract_hash(second)
    )
    assert reference_equipment_contract_hash(first).startswith("sha256:")
    assert len(reference_equipment_contract_hash(first)) == 71
    assert json.loads(reference_equipment_contract_json(first)) == (
        reference_equipment_contract_payload(first)
    )


def test_hash_changes_when_a_bound_equipment_value_changes() -> None:
    contract = build_generic_reference_equipment_contract()
    changed_power = replace(
        contract.module.rated_power_wp,
        value=661.0,
    )
    changed_module = replace(contract.module, rated_power_wp=changed_power)
    changed = replace(contract, module=changed_module)

    with pytest.raises(ValueError, match="475.2 kWp"):
        validate_reference_equipment_contract(changed)

    changed_fixture = replace(
        contract,
        module=replace(
            contract.module,
            rated_power_wp=QualifiedValue(
                value=660.0,
                unit="Wp",
                evidence_class=EvidenceClass.USER_CREATED,
                verification_state=VerificationState.VERIFIED,
                source_reference="product_owner_reference_fixture",
                source_revision="2026-08-01-revised",
                note="Changed source revision only.",
            ),
        ),
    )
    assert reference_equipment_contract_hash(changed_fixture) != (
        reference_equipment_contract_hash(contract)
    )


def test_unresolved_value_cannot_claim_verified_evidence() -> None:
    invalid = QualifiedValue(
        value=None,
        unit="V",
        evidence_class=EvidenceClass.ASSUMED,
        verification_state=VerificationState.VERIFIED,
        source_reference=None,
        source_revision=None,
    )

    with pytest.raises(ValueError, match="unresolved qualified value"):
        invalid.validate()


def test_serialised_contract_contains_no_identity_fields() -> None:
    serialised = reference_equipment_contract_json(
        GENERIC_REFERENCE_EQUIPMENT_CONTRACT
    ).lower()

    for prohibited in (
        "manufacturer_name",
        "project_name",
        "client_name",
        "site_name",
    ):
        assert prohibited not in serialised
