from __future__ import annotations

import dataclasses

import pytest

from solar_topology.calculation_receipts import calculation_receipt_payload
from solar_topology.cartridges import SequentialCartridge
from solar_topology.circuit import EvidenceClass
from solar_topology.circuit_adapters import (
    adapt_segment_chain_to_circuit,
    circuit_boundary_terminal_ids,
    source_segment_ids,
)
from solar_topology.circuit_calculations import calculate_complete_circuit
from solar_topology.circuit_traversal import verify_ordered_circuit
from solar_topology.evidence import (
    VerificationState,
    canonical_evidence_descriptor,
)
from solar_topology.products import (
    EXTERNAL_STRING_6MM2,
    FACTORY_LEAD_4MM2,
)
from solar_topology.resistance_evidence import (
    ResistanceBasis,
    ResistanceValueKind,
    ResolvedConductorResistance,
    register_conductor_resistance,
    resistance_evidence_hash,
    resistance_registry_hash,
    strongest_resistance_record,
)
from solar_topology.segments import TopologyInputs, archetype_strings
from solar_topology.uncertainty import (
    Interval,
    OperatingState,
    calculate_complete_circuit_with_uncertainty,
)


def _rows(modules: int = 6):
    inputs = TopologyInputs(
        modules_per_string=modules,
        inverter_count=1,
        total_site_string_count=24,
        positive_factory_lead_m=1.4,
        negative_factory_lead_m=1.4,
    )
    definition = archetype_strings(inputs)[0]
    return SequentialCartridge().build_segments(inputs, definition)


def _model_and_traversal(rows):
    model = adapt_segment_chain_to_circuit(rows)
    start, end = circuit_boundary_terminal_ids(model)
    traversal = verify_ordered_circuit(
        model,
        start,
        end,
        expected_segment_ids=source_segment_ids(rows),
    )
    assert traversal.valid
    return model, traversal


def _current_evidence():
    return canonical_evidence_descriptor(
        EvidenceClass.MANUFACTURER_DECLARED,
        verification_state=VerificationState.CANDIDATE,
        source_reference="resistance-evidence-test-current",
    )


def _calculate(rows):
    model, traversal = _model_and_traversal(rows)
    return calculate_complete_circuit(
        model,
        traversal,
        current_a=17.35,
        current_evidence=_current_evidence(),
    )


def _record(
    *,
    basis: ResistanceBasis,
    value_kind: ResistanceValueKind,
    r20: float = 0.003,
    source_revision: str = "test-v1",
) -> ResolvedConductorResistance:
    return ResolvedConductorResistance(
        product_id="test-product",
        r20_ohm_per_m=r20,
        basis=basis,
        value_kind=value_kind,
        source_reference="test-source",
        source_revision=source_revision,
        verification_state=VerificationState.CANDIDATE,
    )


def test_default_products_use_explicit_standard_maximum_evidence() -> None:
    for product in (FACTORY_LEAD_4MM2, EXTERNAL_STRING_6MM2):
        product.validate()
        resistance = product.resolved_resistance
        assert resistance.basis is ResistanceBasis.STANDARD_MAXIMUM
        assert resistance.value_kind is ResistanceValueKind.STANDARD_MAXIMUM
        assert resistance.evidence_class is EvidenceClass.EXTERNAL_REFERENCE
        assert (
            resistance.verification_state
            is VerificationState.STANDARDS_REVIEW_REQUIRED
        )
        assert resistance.source_revision == "edition-not-yet-encoded"
        assert resistance.r20_ohm_per_m == product.r20_ohm_per_m


def test_resistance_hash_changes_with_basis_source_or_value() -> None:
    standard = _record(
        basis=ResistanceBasis.STANDARD_MAXIMUM,
        value_kind=ResistanceValueKind.STANDARD_MAXIMUM,
    )
    manufacturer = _record(
        basis=ResistanceBasis.MANUFACTURER_DECLARED,
        value_kind=ResistanceValueKind.MANUFACTURER_NOMINAL,
    )
    revised = dataclasses.replace(standard, source_revision="test-v2")
    changed_value = dataclasses.replace(standard, r20_ohm_per_m=0.0031)

    hashes = {
        resistance_evidence_hash(record)
        for record in (standard, manufacturer, revised, changed_value)
    }
    assert len(hashes) == 4


def test_strongest_record_does_not_allow_weak_override() -> None:
    measured = _record(
        basis=ResistanceBasis.INDEPENDENTLY_MEASURED,
        value_kind=ResistanceValueKind.MEASURED,
    )
    manufacturer = _record(
        basis=ResistanceBasis.MANUFACTURER_DECLARED,
        value_kind=ResistanceValueKind.MANUFACTURER_MAXIMUM,
    )
    assumed = _record(
        basis=ResistanceBasis.ASSUMED,
        value_kind=ResistanceValueKind.ASSUMED,
    )

    assert strongest_resistance_record((assumed, manufacturer, measured)) is measured


def test_calculation_receipt_exports_resistance_basis_and_registry_hash() -> None:
    receipt = _calculate(_rows())
    payload = calculation_receipt_payload(receipt)

    assert receipt.resistance_registry_hash == resistance_registry_hash()
    assert payload["resistance_registry_hash"] == resistance_registry_hash()
    assert receipt.segment_results
    assert all(
        result.resistance_evidence.basis
        is ResistanceBasis.STANDARD_MAXIMUM
        for result in receipt.segment_results
    )
    for segment in payload["segment_results"]:
        evidence = segment["resistance_evidence"]
        assert evidence["basis"] == "standard_maximum"
        assert evidence["value_kind"] == "standard_maximum"
        assert evidence["source_revision"] == "edition-not-yet-encoded"
        assert evidence["temperature_coefficient_per_c"] == pytest.approx(
            0.00393
        )


def test_r20_override_is_calculated_but_evidence_is_downgraded() -> None:
    rows = list(_rows(modules=1))
    source = rows[0]
    baseline = _calculate((source,))
    overridden_row = dataclasses.replace(
        source,
        r20_ohm_per_m=source.r20_ohm_per_m * 1.10,
        source_reference="test-r20-override",
    )
    overridden = _calculate((overridden_row,))
    result = overridden.segment_results[0]

    assert result.r20_ohm_per_m == pytest.approx(
        source.r20_ohm_per_m * 1.10
    )
    assert result.resistance_evidence.basis is ResistanceBasis.ASSUMED
    assert result.resistance_evidence.value_kind is ResistanceValueKind.ASSUMED
    assert result.resistance_evidence.evidence_class is EvidenceClass.ASSUMED
    assert result.conductor_resistance_ohm > (
        baseline.segment_results[0].conductor_resistance_ohm
    )
    assert result.voltage_drop_v > baseline.segment_results[0].voltage_drop_v
    assert result.resistive_loss_w > baseline.segment_results[0].resistive_loss_w
    assert any(
        "downgraded to assumed" in warning
        for warning in overridden.warnings
    )


def test_uncertainty_uses_resolved_product_temperature_coefficient() -> None:
    record = register_conductor_resistance(
        ResolvedConductorResistance(
            product_id="test-measured-alpha-product",
            r20_ohm_per_m=0.004,
            basis=ResistanceBasis.INDEPENDENTLY_MEASURED,
            value_kind=ResistanceValueKind.MEASURED,
            source_reference="laboratory-four-wire-test",
            source_revision="test-2026-07-31",
            verification_state=VerificationState.VERIFIED,
            temperature_coefficient_per_c=0.0042,
            temperature_coefficient_basis="measured_product_fit",
            measurement_conditions="four-wire measurement at 20 C",
        )
    )
    source = _rows(modules=1)[0]
    row = dataclasses.replace(
        source,
        conductor_product_id=record.product_id,
        r20_ohm_per_m=record.r20_ohm_per_m,
        temperature_c=70.0,
        connector_count=0,
        connector_resistance_ohm_each=0.0,
        provenance="measured",
        source_reference=record.source_reference,
    )
    model, traversal = _model_and_traversal((row,))
    nominal = calculate_complete_circuit(
        model,
        traversal,
        current_a=17.35,
        current_evidence=_current_evidence(),
    )
    uncertain = calculate_complete_circuit_with_uncertainty(
        model,
        traversal,
        operating_state=OperatingState(
            state_id="measured-alpha-exact-state",
            current_a=Interval.exact(17.35, "A"),
            current_evidence=_current_evidence(),
            string_vmp_v=Interval.exact(1100.0, "V"),
            string_vmp_evidence=canonical_evidence_descriptor(
                EvidenceClass.MANUFACTURER_DECLARED,
                verification_state=VerificationState.CANDIDATE,
                source_reference="resistance-evidence-test-vmp",
            ),
        ),
    )
    expected = (
        row.conductor_length_m
        * record.r20_ohm_per_m
        * (1 + record.temperature_coefficient_per_c * (70.0 - 20.0))
    )

    assert nominal.segment_results[0].conductor_resistance_ohm == pytest.approx(
        expected
    )
    assert uncertain.segment_results[0].conductor_resistance_ohm == (
        Interval.exact(expected, "ohm")
    )
    assert uncertain.total_resistance_ohm == Interval.exact(
        nominal.total_resistance_ohm,
        "ohm",
    )


def test_incompatible_basis_and_value_kind_is_rejected() -> None:
    with pytest.raises(ValueError, match="incompatible"):
        _record(
            basis=ResistanceBasis.IDEAL_BULK_ESTIMATE,
            value_kind=ResistanceValueKind.MANUFACTURER_NOMINAL,
        )
