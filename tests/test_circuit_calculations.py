import dataclasses
import inspect
import json
from pathlib import Path

import pytest

from solar_topology.calculation_receipts import (
    calculation_receipt_hash,
    calculation_receipt_json,
)
from solar_topology.cartridges import (
    LeapfrogCartridge,
    SequentialCartridge,
)
from solar_topology.circuit import EvidenceClass
from solar_topology.circuit_adapters import (
    adapt_segment_chain_to_circuit,
    circuit_boundary_terminal_ids,
    source_segment_ids,
)
from solar_topology.circuit_calculations import (
    calculate_complete_circuit,
)
from solar_topology.circuit_traversal import (
    TraversalIssue,
    verify_ordered_circuit,
)
from solar_topology.evidence import (
    VerificationState,
    canonical_evidence_descriptor,
    javascript_provenance_descriptor,
    segment_provenance_descriptor,
)
from solar_topology.segments import TopologyInputs, archetype_strings


FIXTURE_PATH = (
    Path(__file__).parents[1]
    / "v10-development"
    / "fixtures"
    / "steady_state_cross_language_v1.json"
)


def _rows(cartridge, *, modules=30):
    inputs = TopologyInputs(
        modules_per_string=modules,
        inverter_count=1,
        total_site_string_count=24,
        positive_factory_lead_m=1.4,
        negative_factory_lead_m=1.4,
    )
    definition = archetype_strings(inputs)[0]
    return cartridge.build_segments(inputs, definition)


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
        source_reference="known_answer_current",
    )


def test_provenance_vocabularies_reconcile_without_silent_promotion():
    defaulted = segment_provenance_descriptor("defaulted")
    datasheet = javascript_provenance_descriptor("datasheet")
    standards = javascript_provenance_descriptor("standardsDerived")
    hypothesis = javascript_provenance_descriptor("researchHypothesis")

    assert defaulted.evidence_class == EvidenceClass.ASSUMED
    assert defaulted.source_value == "defaulted"
    assert datasheet.evidence_class == EvidenceClass.MANUFACTURER_DECLARED
    assert standards.evidence_class == EvidenceClass.DERIVED
    assert (
        standards.verification_state
        == VerificationState.STANDARDS_REVIEW_REQUIRED
    )
    assert hypothesis.evidence_class == EvidenceClass.ASSUMED
    assert (
        hypothesis.verification_state
        == VerificationState.RESEARCH_HYPOTHESIS
    )


@pytest.mark.parametrize(
    ("cartridge", "expected_resistance", "expected_drop", "expected_loss"),
    (
        (
            SequentialCartridge(),
            0.78836961445,
            13.6782128107075,
            237.316992265775,
        ),
        (
            LeapfrogCartridge(),
            0.627462739,
            10.88647852165,
            188.880402350628,
        ),
    ),
)
def test_complete_circuit_known_answer_includes_all_series_elements(
    cartridge,
    expected_resistance,
    expected_drop,
    expected_loss,
):
    rows = _rows(cartridge)
    model, traversal = _model_and_traversal(rows)

    receipt = calculate_complete_circuit(
        model,
        traversal,
        current_a=17.35,
        current_evidence=_current_evidence(),
    )

    assert receipt.ordered_segment_ids == tuple(
        row.segment_id for row in rows
    )
    assert receipt.total_conductor_length_m == pytest.approx(
        sum(row.conductor_length_m for row in rows)
    )
    assert receipt.total_resistance_ohm == pytest.approx(
        expected_resistance,
        rel=1e-12,
    )
    assert receipt.voltage_drop_v == pytest.approx(
        expected_drop,
        rel=1e-12,
    )
    assert receipt.resistive_loss_w == pytest.approx(
        expected_loss,
        rel=1e-12,
    )
    assert receipt.total_connector_resistance_ohm > 0
    assert receipt.input_evidence_floor == EvidenceClass.ASSUMED
    assert receipt.segment_results[0].segment_id == rows[0].segment_id
    assert receipt.segment_results[-1].segment_id == rows[-1].segment_id
    assert calculation_receipt_hash(receipt).startswith("sha256:")


def test_calculation_receipt_is_deterministic():
    rows = _rows(SequentialCartridge(), modules=6)
    first_model, first_traversal = _model_and_traversal(rows)
    second_model, second_traversal = _model_and_traversal(
        tuple(reversed(rows))
    )

    first = calculate_complete_circuit(
        first_model,
        first_traversal,
        current_a=10.0,
        current_evidence=_current_evidence(),
    )
    second = calculate_complete_circuit(
        second_model,
        second_traversal,
        current_a=10.0,
        current_evidence=_current_evidence(),
    )

    assert calculation_receipt_json(first) == calculation_receipt_json(
        second
    )
    assert calculation_receipt_hash(first) == calculation_receipt_hash(
        second
    )


def test_calculation_refuses_invalid_or_forged_traversal():
    rows = _rows(SequentialCartridge(), modules=6)
    model, traversal = _model_and_traversal(rows)
    invalid = dataclasses.replace(
        traversal,
        issues=(
            TraversalIssue(
                code="TEST_INVALID",
                message="test-invalid traversal",
            ),
        ),
    )

    with pytest.raises(
        ValueError,
        match="invalid ordered circuit traversal",
    ):
        calculate_complete_circuit(
            model,
            invalid,
            current_a=10.0,
            current_evidence=_current_evidence(),
        )

    forged = dataclasses.replace(
        traversal,
        ordered_connection_ids=tuple(
            reversed(traversal.ordered_connection_ids)
        ),
    )
    with pytest.raises(
        ValueError,
        match="differs from independently derived order",
    ):
        calculate_complete_circuit(
            model,
            forged,
            current_a=10.0,
            current_evidence=_current_evidence(),
        )


def test_calculation_api_has_no_free_total_length_input():
    parameters = inspect.signature(
        calculate_complete_circuit
    ).parameters
    assert "total_length" not in parameters
    assert "route_length" not in parameters
    assert "user_length" not in parameters


def test_python_matches_shared_javascript_formula_fixture():
    fixture = json.loads(FIXTURE_PATH.read_text(encoding="utf-8"))

    for case in fixture["cases"]:
        rows = list(_rows(SequentialCartridge(), modules=1))
        source = rows[0]
        one_segment = dataclasses.replace(
            source,
            segment_index=1,
            segment_id=f"fixture:{case['id']}",
            from_node_id="fixture:start",
            to_node_id="fixture:end",
            conductor_length_m=case["length_m"],
            r20_ohm_per_m=case["resistance_ohm_per_m"],
            temperature_c=20.0,
            connector_count=0,
            connector_resistance_ohm_each=0.0,
            warnings="",
        )
        model, traversal = _model_and_traversal((one_segment,))
        receipt = calculate_complete_circuit(
            model,
            traversal,
            current_a=case["current_a"],
            current_evidence=_current_evidence(),
        )

        assert receipt.total_resistance_ohm == pytest.approx(
            case["expected"]["resistance_ohm"],
            rel=1e-12,
        )
        assert receipt.voltage_drop_v == pytest.approx(
            case["expected"]["voltage_drop_v"],
            rel=1e-12,
        )
        assert receipt.resistive_loss_w == pytest.approx(
            case["expected"]["resistive_loss_w"],
            rel=1e-12,
        )
