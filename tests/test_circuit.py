import dataclasses

import pytest

from solar_topology.circuit import (
    CircuitModel,
    Connection,
    EvidenceClass,
    ObjectKind,
    PhysicalObject,
    Terminal,
    TerminalPolarity,
    canonical_circuit_json,
)
from solar_topology.circuit_validation import (
    validate_circuit_model,
    validated_circuit_hash,
)
from solar_topology.segments import Point3D


def _terminal(
    object_id,
    suffix,
    polarity,
    *,
    required=True,
    max_connections=1,
):
    return Terminal(
        terminal_id=f"{object_id}:{suffix}",
        object_id=object_id,
        polarity=polarity,
        position=Point3D(0.0, 0.0, 0.0),
        required_connection=required,
        max_connections=max_connections,
        evidence_class=EvidenceClass.GENERIC_EXAMPLE,
        source_reference="test_fixture",
    )


def _two_module_series_model(*, reverse_records=False):
    inverter = PhysicalObject(
        object_id="INV01",
        kind=ObjectKind.INVERTER,
        terminals=(
            _terminal("INV01", "DC_POS", TerminalPolarity.POSITIVE),
            _terminal("INV01", "DC_NEG", TerminalPolarity.NEGATIVE),
        ),
        evidence_class=EvidenceClass.GENERIC_EXAMPLE,
        source_reference="test_fixture",
    )
    module_1 = PhysicalObject(
        object_id="M01",
        kind=ObjectKind.MODULE,
        terminals=(
            _terminal("M01", "POS", TerminalPolarity.POSITIVE),
            _terminal("M01", "NEG", TerminalPolarity.NEGATIVE),
        ),
        parent_object_id="STRING01",
        evidence_class=EvidenceClass.GENERIC_EXAMPLE,
        source_reference="test_fixture",
    )
    module_2 = PhysicalObject(
        object_id="M02",
        kind=ObjectKind.MODULE,
        terminals=(
            _terminal("M02", "POS", TerminalPolarity.POSITIVE),
            _terminal("M02", "NEG", TerminalPolarity.NEGATIVE),
        ),
        parent_object_id="STRING01",
        evidence_class=EvidenceClass.GENERIC_EXAMPLE,
        source_reference="test_fixture",
    )
    string = PhysicalObject(
        object_id="STRING01",
        kind=ObjectKind.STRING,
        terminals=(),
        evidence_class=EvidenceClass.GENERIC_EXAMPLE,
        source_reference="test_fixture",
    )

    objects = (inverter, string, module_1, module_2)
    connections = (
        Connection(
            connection_id="C01",
            from_terminal_id="INV01:DC_POS",
            to_terminal_id="M01:POS",
            evidence_class=EvidenceClass.GENERIC_EXAMPLE,
            source_reference="test_fixture",
        ),
        Connection(
            connection_id="C02",
            from_terminal_id="M01:NEG",
            to_terminal_id="M02:POS",
            evidence_class=EvidenceClass.GENERIC_EXAMPLE,
            source_reference="test_fixture",
        ),
        Connection(
            connection_id="C03",
            from_terminal_id="M02:NEG",
            to_terminal_id="INV01:DC_NEG",
            evidence_class=EvidenceClass.GENERIC_EXAMPLE,
            source_reference="test_fixture",
        ),
    )

    if reverse_records:
        objects = tuple(reversed(objects))
        connections = tuple(reversed(connections))

    return CircuitModel(
        model_id="SERIES-2",
        objects=objects,
        connections=connections,
        metadata=(("fixture", "two-module-series"),),
    )


def test_valid_series_circuit_has_deterministic_hash():
    first = _two_module_series_model()
    second = _two_module_series_model(reverse_records=True)

    assert validate_circuit_model(first).valid
    assert validate_circuit_model(second).valid
    assert canonical_circuit_json(first) == canonical_circuit_json(second)
    assert validated_circuit_hash(first) == validated_circuit_hash(second)
    assert validated_circuit_hash(first).startswith("sha256:")


def test_unresolved_terminal_reference_is_rejected():
    model = _two_module_series_model()
    broken = dataclasses.replace(
        model,
        connections=model.connections
        + (
            Connection(
                connection_id="C04",
                from_terminal_id="MISSING:POS",
                to_terminal_id="INV01:DC_NEG",
            ),
        ),
    )

    result = validate_circuit_model(broken)

    assert not result.valid
    assert "UNRESOLVED_TERMINAL_REFERENCE" in result.error_codes


def test_duplicate_terminal_id_is_rejected_globally():
    model = _two_module_series_model()
    duplicate = Terminal(
        terminal_id="M01:POS",
        object_id="M02",
        polarity=TerminalPolarity.POSITIVE,
        required_connection=False,
    )
    module_2 = dataclasses.replace(
        model.objects[-1],
        terminals=model.objects[-1].terminals + (duplicate,),
    )
    broken = dataclasses.replace(
        model,
        objects=model.objects[:-1] + (module_2,),
    )

    result = validate_circuit_model(broken)

    assert not result.valid
    assert "DUPLICATE_TERMINAL_ID" in result.error_codes


def test_required_dangling_terminal_is_rejected():
    model = _two_module_series_model()
    broken = dataclasses.replace(
        model,
        connections=model.connections[:-1],
    )

    result = validate_circuit_model(broken)

    assert not result.valid
    assert "DANGLING_REQUIRED_TERMINAL" in result.error_codes


def test_terminal_connection_capacity_is_enforced():
    model = _two_module_series_model()
    extra_object = PhysicalObject(
        object_id="M03",
        kind=ObjectKind.MODULE,
        terminals=(
            _terminal(
                "M03",
                "POS",
                TerminalPolarity.POSITIVE,
                required=False,
            ),
        ),
    )
    broken = dataclasses.replace(
        model,
        objects=model.objects + (extra_object,),
        connections=model.connections
        + (
            Connection(
                connection_id="C04",
                from_terminal_id="INV01:DC_POS",
                to_terminal_id="M03:POS",
            ),
        ),
    )

    result = validate_circuit_model(broken)

    assert not result.valid
    assert "TERMINAL_CAPACITY_EXCEEDED" in result.error_codes


def test_parent_cycles_are_rejected():
    first = PhysicalObject(
        object_id="A",
        kind=ObjectKind.STRING,
        terminals=(),
        parent_object_id="B",
    )
    second = PhysicalObject(
        object_id="B",
        kind=ObjectKind.STRING,
        terminals=(),
        parent_object_id="A",
    )
    model = CircuitModel(
        model_id="PARENT-CYCLE",
        objects=(first, second),
        connections=(),
    )

    result = validate_circuit_model(model)

    assert not result.valid
    assert "PARENT_CYCLE" in result.error_codes


def test_non_finite_terminal_coordinates_are_rejected():
    model = _two_module_series_model()
    module_1 = model.objects[2]
    invalid_terminal = dataclasses.replace(
        module_1.terminals[0],
        position=Point3D(float("nan"), 0.0, 0.0),
    )
    broken_module = dataclasses.replace(
        module_1,
        terminals=(invalid_terminal, module_1.terminals[1]),
    )
    broken = dataclasses.replace(
        model,
        objects=model.objects[:2]
        + (broken_module,)
        + model.objects[3:],
    )

    result = validate_circuit_model(broken)

    assert not result.valid
    assert "INVALID_TERMINAL_POSITION" in result.error_codes


def test_invalid_circuit_cannot_receive_authority_hash():
    model = _two_module_series_model()
    broken = dataclasses.replace(
        model,
        connections=(),
    )

    with pytest.raises(ValueError, match="invalid circuit model"):
        validated_circuit_hash(broken)
