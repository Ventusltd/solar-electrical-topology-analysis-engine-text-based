from __future__ import annotations

from solar_topology.circuit import (
    CircuitModel,
    Connection,
    ConnectionKind,
    EvidenceClass,
    ObjectKind,
    PhysicalObject,
    Terminal,
    TerminalPolarity,
    canonical_circuit_json,
)
from solar_topology.circuit_traversal import verify_ordered_circuit
from solar_topology.circuit_validation import validate_circuit_model


def _terminal(object_id: str, suffix: str, polarity: TerminalPolarity) -> Terminal:
    return Terminal(
        terminal_id=f"{object_id}:{suffix}",
        object_id=object_id,
        polarity=polarity,
        max_connections=2,
        evidence_class=EvidenceClass.USER_CREATED,
    )


def _object(object_id: str, left: Terminal, right: Terminal) -> PhysicalObject:
    return PhysicalObject(
        object_id=object_id,
        kind=ObjectKind.MODULE,
        terminals=(left, right),
        evidence_class=EvidenceClass.USER_CREATED,
    )


def _valid_path() -> CircuitModel:
    a_left = _terminal("a", "left", TerminalPolarity.POSITIVE)
    a_right = _terminal("a", "right", TerminalPolarity.NEGATIVE)
    b_left = _terminal("b", "left", TerminalPolarity.POSITIVE)
    b_right = _terminal("b", "right", TerminalPolarity.NEGATIVE)
    return CircuitModel(
        model_id="build023-path",
        objects=(
            _object("a", a_left, a_right),
            _object("b", b_left, b_right),
        ),
        connections=(
            Connection(
                connection_id="c1",
                from_terminal_id=a_left.terminal_id,
                to_terminal_id=a_right.terminal_id,
                kind=ConnectionKind.INTERNAL,
                segment_id="segment-a",
                evidence_class=EvidenceClass.USER_CREATED,
            ),
            Connection(
                connection_id="c2",
                from_terminal_id=a_right.terminal_id,
                to_terminal_id=b_left.terminal_id,
                evidence_class=EvidenceClass.USER_CREATED,
            ),
            Connection(
                connection_id="c3",
                from_terminal_id=b_left.terminal_id,
                to_terminal_id=b_right.terminal_id,
                kind=ConnectionKind.INTERNAL,
                segment_id="segment-b",
                evidence_class=EvidenceClass.USER_CREATED,
            ),
        ),
    )


def test_valid_model_requires_independent_validation_and_complete_traversal() -> None:
    model = _valid_path()
    validation = validate_circuit_model(model)
    assert validation.valid, validation.issues

    traversal = verify_ordered_circuit(
        model,
        "a:left",
        "b:right",
        expected_segment_ids=("segment-a", "segment-b"),
    )
    assert traversal.valid, traversal.issues
    assert traversal.ordered_terminal_ids == (
        "a:left",
        "a:right",
        "b:left",
        "b:right",
    )
    assert traversal.ordered_connection_ids == ("c1", "c2", "c3")


def test_payload_and_traversal_do_not_trust_input_tuple_order() -> None:
    model = _valid_path()
    reordered = CircuitModel(
        model_id=model.model_id,
        objects=tuple(reversed(model.objects)),
        connections=tuple(reversed(model.connections)),
    )
    assert canonical_circuit_json(model) == canonical_circuit_json(reordered)
    traversal = verify_ordered_circuit(reordered, "a:left", "b:right")
    assert traversal.valid
    assert traversal.ordered_connection_ids == ("c1", "c2", "c3")


def test_duplicate_identifiers_are_blocking() -> None:
    model = _valid_path()
    duplicate = CircuitModel(
        model_id=model.model_id,
        objects=model.objects + (model.objects[0],),
        connections=model.connections,
    )
    result = validate_circuit_model(duplicate)
    assert not result.valid
    assert "DUPLICATE_OBJECT_ID" in result.error_codes
    assert "DUPLICATE_TERMINAL_ID" in result.error_codes


def test_missing_endpoint_blocks_traversal_before_graph_walk() -> None:
    model = _valid_path()
    broken = CircuitModel(
        model_id=model.model_id,
        objects=model.objects,
        connections=model.connections
        + (
            Connection(
                connection_id="missing-endpoint",
                from_terminal_id="b:right",
                to_terminal_id="ghost:terminal",
            ),
        ),
    )
    validation = validate_circuit_model(broken)
    assert not validation.valid
    traversal = verify_ordered_circuit(broken, "a:left", "b:right")
    assert traversal.error_codes == ("CIRCUIT_VALIDATION_FAILED",)


def test_branch_and_disconnected_island_are_explicit_failures() -> None:
    model = _valid_path()
    c_left = _terminal("c", "left", TerminalPolarity.POSITIVE)
    c_right = _terminal("c", "right", TerminalPolarity.NEGATIVE)
    branched = CircuitModel(
        model_id=model.model_id,
        objects=model.objects + (_object("c", c_left, c_right),),
        connections=model.connections
        + (
            Connection(
                connection_id="branch",
                from_terminal_id="a:right",
                to_terminal_id="c:left",
            ),
            Connection(
                connection_id="c-internal",
                from_terminal_id="c:left",
                to_terminal_id="c:right",
                kind=ConnectionKind.INTERNAL,
                segment_id="segment-c",
            ),
        ),
    )
    traversal = verify_ordered_circuit(branched, "a:left", "b:right")
    assert not traversal.valid
    assert "CIRCUIT_VALIDATION_FAILED" in traversal.error_codes or "BRANCH_DETECTED" in traversal.error_codes


def test_segment_reference_cannot_substitute_for_terminal_connectivity() -> None:
    model = _valid_path()
    bad = CircuitModel(
        model_id=model.model_id,
        objects=model.objects,
        connections=(
            Connection(
                connection_id="c1",
                from_terminal_id="a:left",
                to_terminal_id="a:right",
                kind=ConnectionKind.ELECTRICAL,
                segment_id="segment-a",
            ),
            *model.connections[1:],
        ),
    )
    traversal = verify_ordered_circuit(bad, "a:left", "b:right")
    assert not traversal.valid
    assert "SEGMENT_REFERENCE_NOT_INTERNAL" in traversal.error_codes
