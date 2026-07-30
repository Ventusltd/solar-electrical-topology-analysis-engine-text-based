import dataclasses

import pytest

from solar_topology.cartridges import LeapfrogCartridge, SequentialCartridge
from solar_topology.circuit import (
    Connection,
    ConnectionKind,
    EvidenceClass,
    ObjectKind,
    PhysicalObject,
    Terminal,
    TerminalPolarity,
    canonical_circuit_json,
)
from solar_topology.circuit_adapters import (
    adapt_segment_chain_to_circuit,
    circuit_boundary_terminal_ids,
    source_segment_ids,
)
from solar_topology.circuit_traversal import verify_ordered_circuit
from solar_topology.circuit_validation import validate_circuit_model
from solar_topology.segments import Point3D, TopologyInputs, archetype_strings


def _cartridge_rows(cartridge):
    inputs = TopologyInputs(
        modules_per_string=6,
        inverter_count=1,
        total_site_string_count=24,
        positive_factory_lead_m=1.4,
        negative_factory_lead_m=1.4,
    )
    definition = archetype_strings(inputs)[0]
    return cartridge.build_segments(inputs, definition)


@pytest.mark.parametrize(
    "cartridge",
    (SequentialCartridge(), LeapfrogCartridge()),
)
def test_cartridge_chain_adapts_to_valid_ordered_circuit(cartridge):
    rows = _cartridge_rows(cartridge)
    model = adapt_segment_chain_to_circuit(rows)

    assert validate_circuit_model(model).valid
    start, end = circuit_boundary_terminal_ids(model)
    traversal = verify_ordered_circuit(
        model,
        start,
        end,
        expected_segment_ids=source_segment_ids(rows),
    )

    assert traversal.valid
    assert traversal.ordered_segment_ids == tuple(
        row.segment_id for row in rows
    )
    assert len(traversal.ordered_segment_ids) == len(rows)


def test_adapter_is_deterministic_under_reversed_input_records():
    rows = _cartridge_rows(SequentialCartridge())
    first = adapt_segment_chain_to_circuit(rows)
    second = adapt_segment_chain_to_circuit(tuple(reversed(rows)))

    assert canonical_circuit_json(first) == canonical_circuit_json(second)


def test_adapter_preserves_source_segment_numbers_and_evidence():
    rows = _cartridge_rows(SequentialCartridge())
    model = adapt_segment_chain_to_circuit(rows)
    source = rows[0]
    adapted = next(
        obj
        for obj in model.objects
        if obj.object_id == f"SEGMENT:{source.segment_id}"
    )
    attributes = dict(adapted.attributes)

    assert attributes["conductor_length_m"] == source.conductor_length_m
    assert attributes["displacement_m"] == source.displacement_m
    assert attributes["r20_ohm_per_m"] == source.r20_ohm_per_m
    assert attributes["temperature_c"] == source.temperature_c
    assert attributes["connector_count"] == source.connector_count
    assert attributes["feasibility_status"] == source.feasibility_status
    assert adapted.source_reference == source.source_reference


def test_adapter_rejects_inconsistent_coordinates_for_one_source_node():
    rows = list(_cartridge_rows(SequentialCartridge()))
    rows[1] = dataclasses.replace(rows[1], from_x=rows[1].from_x + 1.0)

    with pytest.raises(ValueError, match="inconsistent coordinates"):
        adapt_segment_chain_to_circuit(rows)


def test_adapter_rejects_mixed_cartridge_chains():
    sequential = _cartridge_rows(SequentialCartridge())
    leapfrog = _cartridge_rows(LeapfrogCartridge())

    with pytest.raises(ValueError, match="exactly one cartridge string chain"):
        adapt_segment_chain_to_circuit(sequential + leapfrog)


def _replace_terminal_capacity(model, terminal_ids, capacity):
    objects = []
    for obj in model.objects:
        terminals = tuple(
            dataclasses.replace(terminal, max_connections=capacity)
            if terminal.terminal_id in terminal_ids
            else terminal
            for terminal in obj.terminals
        )
        objects.append(dataclasses.replace(obj, terminals=terminals))
    return dataclasses.replace(model, objects=tuple(objects))


def test_independent_traversal_rejects_a_branch_even_when_base_model_valid():
    rows = _cartridge_rows(SequentialCartridge())
    model = adapt_segment_chain_to_circuit(rows)
    segment_objects = [
        obj for obj in model.objects if obj.object_id.startswith("SEGMENT:")
    ]
    first_terminal = segment_objects[0].terminals[0].terminal_id
    later_terminal = segment_objects[2].terminals[0].terminal_id
    branched = _replace_terminal_capacity(
        model,
        {first_terminal, later_terminal},
        3,
    )
    branched = dataclasses.replace(
        branched,
        connections=branched.connections
        + (
            Connection(
                connection_id="TEST:EXTRA_BRANCH",
                from_terminal_id=first_terminal,
                to_terminal_id=later_terminal,
                kind=ConnectionKind.ELECTRICAL,
                evidence_class=EvidenceClass.GENERIC_EXAMPLE,
                source_reference="test_fixture",
            ),
        ),
    )

    assert validate_circuit_model(branched).valid
    start, end = circuit_boundary_terminal_ids(branched)
    traversal = verify_ordered_circuit(branched, start, end)

    assert not traversal.valid
    assert "BRANCH_DETECTED" in traversal.error_codes


def test_independent_traversal_rejects_expected_order_mismatch():
    rows = _cartridge_rows(LeapfrogCartridge())
    model = adapt_segment_chain_to_circuit(rows)
    start, end = circuit_boundary_terminal_ids(model)
    traversal = verify_ordered_circuit(
        model,
        start,
        end,
        expected_segment_ids=tuple(reversed(source_segment_ids(rows))),
    )

    assert not traversal.valid
    assert "SEGMENT_ORDER_MISMATCH" in traversal.error_codes


def test_traversal_rejects_disconnected_but_individually_connected_component():
    rows = _cartridge_rows(SequentialCartridge())
    model = adapt_segment_chain_to_circuit(rows)
    extra_a = PhysicalObject(
        object_id="TEST:A",
        kind=ObjectKind.OTHER,
        terminals=(
            Terminal(
                terminal_id="TEST:A:T",
                object_id="TEST:A",
                polarity=TerminalPolarity.UNSPECIFIED,
                position=Point3D(0.0, 0.0, 0.0),
            ),
        ),
    )
    extra_b = PhysicalObject(
        object_id="TEST:B",
        kind=ObjectKind.OTHER,
        terminals=(
            Terminal(
                terminal_id="TEST:B:T",
                object_id="TEST:B",
                polarity=TerminalPolarity.UNSPECIFIED,
                position=Point3D(1.0, 0.0, 0.0),
            ),
        ),
    )
    disconnected = dataclasses.replace(
        model,
        objects=model.objects + (extra_a, extra_b),
        connections=model.connections
        + (
            Connection(
                connection_id="TEST:DISCONNECTED",
                from_terminal_id="TEST:A:T",
                to_terminal_id="TEST:B:T",
                evidence_class=EvidenceClass.GENERIC_EXAMPLE,
                source_reference="test_fixture",
            ),
        ),
    )

    assert validate_circuit_model(disconnected).valid
    start, end = circuit_boundary_terminal_ids(disconnected)
    traversal = verify_ordered_circuit(disconnected, start, end)

    assert not traversal.valid
    assert "DISCONNECTED_CIRCUIT_GRAPH" in traversal.error_codes
