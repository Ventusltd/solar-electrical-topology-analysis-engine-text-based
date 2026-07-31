import dataclasses

import pytest

from solar_topology.cartridges import SequentialCartridge
from solar_topology.circuit import EvidenceClass
from solar_topology.circuit_adapters import (
    adapt_segment_chain_to_circuit,
    circuit_boundary_terminal_ids,
    source_segment_ids,
)
from solar_topology.circuit_traversal import verify_ordered_circuit
from solar_topology.evidence import (
    VerificationState,
    canonical_evidence_descriptor,
)
from solar_topology.segments import TopologyInputs, archetype_strings
from solar_topology.uncertainty import (
    Interval,
    OperatingState,
    SegmentInputIntervals,
    calculate_complete_circuit_with_uncertainty,
    uncertainty_receipt_hash,
    uncertainty_receipt_json,
)


def _rows(modules=6):
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


def _evidence(source):
    return canonical_evidence_descriptor(
        EvidenceClass.MANUFACTURER_DECLARED,
        verification_state=VerificationState.CANDIDATE,
        source_reference=source,
    )


def _operating_state():
    return OperatingState(
        state_id="fixture:operating-state",
        current_a=Interval(16.0, 17.35, 18.0, "A"),
        current_evidence=_evidence("fixture:current"),
        string_vmp_v=Interval(1050.0, 1100.0, 1150.0, "V"),
        string_vmp_evidence=_evidence("fixture:vmp"),
    )


def _exact_operating_state():
    return OperatingState(
        state_id="fixture:exact-operating-state",
        current_a=Interval.exact(17.35, "A"),
        current_evidence=_evidence("fixture:exact-current"),
        string_vmp_v=Interval.exact(1100.0, "V"),
        string_vmp_evidence=_evidence("fixture:exact-vmp"),
    )


def test_interval_requires_ordered_finite_values_and_units():
    assert Interval.exact(10.0, "A") == Interval(10.0, 10.0, 10.0, "A")
    with pytest.raises(ValueError, match="lower <= nominal <= upper"):
        Interval(2.0, 1.0, 3.0, "A")
    with pytest.raises(ValueError, match="unit"):
        Interval(1.0, 1.0, 1.0, "")


def test_uncertainty_contains_nominal_and_reports_voltage_drop_percentage():
    rows = _rows()
    model, traversal = _model_and_traversal(rows)
    first = rows[0]
    overrides = {
        first.segment_id: SegmentInputIntervals(
            conductor_length_m=Interval(
                first.conductor_length_m * 0.98,
                first.conductor_length_m,
                first.conductor_length_m * 1.02,
                "m",
            ),
            r20_ohm_per_m=Interval(
                first.r20_ohm_per_m * 0.97,
                first.r20_ohm_per_m,
                first.r20_ohm_per_m * 1.03,
                "ohm/m",
            ),
            temperature_c=Interval(
                first.temperature_c - 5.0,
                first.temperature_c,
                first.temperature_c + 5.0,
                "degC",
            ),
            connector_resistance_ohm_each=Interval(
                first.connector_resistance_ohm_each * 0.9,
                first.connector_resistance_ohm_each,
                first.connector_resistance_ohm_each * 1.1,
                "ohm",
            ),
        )
    }

    receipt = calculate_complete_circuit_with_uncertainty(
        model,
        traversal,
        operating_state=_operating_state(),
        segment_intervals=overrides,
    )

    assert receipt.total_resistance_ohm.lower <= receipt.total_resistance_ohm.nominal
    assert receipt.total_resistance_ohm.nominal <= receipt.total_resistance_ohm.upper
    assert receipt.voltage_drop_v.nominal == pytest.approx(
        receipt.nominal_receipt.voltage_drop_v
    )
    assert receipt.resistive_loss_w.nominal == pytest.approx(
        receipt.nominal_receipt.resistive_loss_w
    )
    assert receipt.voltage_drop_percent.nominal == pytest.approx(
        100.0 * receipt.nominal_receipt.voltage_drop_v / 1100.0
    )
    assert receipt.voltage_drop_percent.lower < receipt.voltage_drop_percent.upper
    assert uncertainty_receipt_hash(receipt).startswith("sha256:")


@pytest.mark.parametrize("modules", range(1, 62))
def test_exact_uncertainty_collapses_to_nominal_across_module_counts(modules):
    rows = _rows(modules)
    model, traversal = _model_and_traversal(rows)

    receipt = calculate_complete_circuit_with_uncertainty(
        model,
        traversal,
        operating_state=_exact_operating_state(),
    )

    nominal = receipt.nominal_receipt
    assert receipt.total_resistance_ohm == Interval.exact(
        nominal.total_resistance_ohm,
        "ohm",
    )
    assert receipt.voltage_drop_v == Interval.exact(
        nominal.voltage_drop_v,
        "V",
    )
    assert receipt.resistive_loss_w == Interval.exact(
        nominal.resistive_loss_w,
        "W",
    )
    assert receipt.voltage_drop_percent.lower == receipt.voltage_drop_percent.nominal
    assert receipt.voltage_drop_percent.nominal == receipt.voltage_drop_percent.upper


def test_uncertainty_receipt_is_deterministic_under_source_row_reordering():
    rows = _rows()
    first_model, first_traversal = _model_and_traversal(rows)
    second_model, second_traversal = _model_and_traversal(tuple(reversed(rows)))

    first = calculate_complete_circuit_with_uncertainty(
        first_model,
        first_traversal,
        operating_state=_operating_state(),
    )
    second = calculate_complete_circuit_with_uncertainty(
        second_model,
        second_traversal,
        operating_state=_operating_state(),
    )

    assert uncertainty_receipt_json(first) == uncertainty_receipt_json(second)
    assert uncertainty_receipt_hash(first) == uncertainty_receipt_hash(second)


def test_uncertainty_rejects_unknown_segments_and_nominal_mismatch():
    rows = _rows()
    model, traversal = _model_and_traversal(rows)

    with pytest.raises(ValueError, match="unknown segments"):
        calculate_complete_circuit_with_uncertainty(
            model,
            traversal,
            operating_state=_operating_state(),
            segment_intervals={"missing": SegmentInputIntervals()},
        )

    first = rows[0]
    with pytest.raises(ValueError, match="nominal must equal canonical"):
        calculate_complete_circuit_with_uncertainty(
            model,
            traversal,
            operating_state=_operating_state(),
            segment_intervals={
                first.segment_id: SegmentInputIntervals(
                    conductor_length_m=Interval(
                        first.conductor_length_m,
                        first.conductor_length_m + 1.0,
                        first.conductor_length_m + 2.0,
                        "m",
                    )
                )
            },
        )


def test_invalid_operating_state_is_rejected():
    with pytest.raises(ValueError, match="strictly positive"):
        dataclasses.replace(
            _operating_state(),
            string_vmp_v=Interval(0.0, 1.0, 2.0, "V"),
        )
