"""Adapt ordered cartridge segment chains into the canonical V10 circuit model.

The adapter preserves the existing segment rows as evidence-bearing object attributes.
It does not recalculate lengths, resistance, loss, feasibility or electromagnetic values.
"""

from __future__ import annotations

from collections import Counter
import hashlib
import json
import math
from typing import Iterable, Sequence

from .cartridges import (
    LeapfrogCartridge,
    SequentialCartridge,
    validate_segment_chains,
)
from .circuit import (
    CircuitModel,
    Connection,
    ConnectionKind,
    EvidenceClass,
    ObjectKind,
    PhysicalObject,
    Terminal,
    TerminalPolarity,
)
from .segments import Point3D, SegmentRow, StringDefinition, TopologyInputs


CARTRIDGE_ADAPTER_VERSION = (
    "globalgrid2050.solar-dc.cartridge-circuit-adapter.v10.1"
)

_PROVENANCE_TO_EVIDENCE = {
    "measured": EvidenceClass.FIELD_MEASURED,
    "oem_declared": EvidenceClass.MANUFACTURER_DECLARED,
    "assumed": EvidenceClass.ASSUMED,
    "defaulted": EvidenceClass.ASSUMED,
}

_FACTORY_SEGMENTS = {
    "module_factory_positive_lead",
    "module_factory_negative_lead",
}
_CONNECTOR_SEGMENTS = {
    "module_interconnect",
    "string_turnaround",
}


def _point(x: float, y: float, z: float) -> Point3D:
    return Point3D(float(x), float(y), float(z))


def _points_match(first: Point3D, second: Point3D) -> bool:
    return all(
        math.isclose(a, b, rel_tol=0.0, abs_tol=1e-9)
        for a, b in zip(
            (first.x, first.y, first.z),
            (second.x, second.y, second.z),
        )
    )


def _evidence_class(row: SegmentRow) -> EvidenceClass:
    try:
        return _PROVENANCE_TO_EVIDENCE[row.provenance]
    except KeyError as exc:
        raise ValueError(
            f"unsupported segment provenance for V10 adapter: {row.provenance}"
        ) from exc


def _object_kind(row: SegmentRow) -> ObjectKind:
    if row.segment_type in _FACTORY_SEGMENTS:
        return ObjectKind.FACTORY_LEAD
    if row.segment_type in _CONNECTOR_SEGMENTS:
        return ObjectKind.CONNECTOR
    if row.segment_type.startswith("external_") or row.segment_type == (
        "extension_lead"
    ):
        return ObjectKind.FIELD_CONDUCTOR
    return ObjectKind.OTHER


def _terminal_polarity(row: SegmentRow) -> TerminalPolarity:
    if row.polarity == "positive":
        return TerminalPolarity.POSITIVE
    if row.polarity == "negative":
        return TerminalPolarity.NEGATIVE
    return TerminalPolarity.UNSPECIFIED


def _source_payload(rows: Sequence[SegmentRow]) -> str:
    return json.dumps(
        [row.as_dict() for row in rows],
        sort_keys=True,
        separators=(",", ":"),
    )


def segment_chain_hash(rows: Iterable[SegmentRow]) -> str:
    """Return a deterministic hash of one validated ordered segment chain."""

    ordered = _normalise_segment_chain(rows)
    digest = hashlib.sha256(_source_payload(ordered).encode("utf-8")).hexdigest()
    return f"sha256:{digest}"


def _normalise_segment_chain(
    rows: Iterable[SegmentRow],
) -> tuple[SegmentRow, ...]:
    materialised = tuple(rows)
    if not materialised:
        raise ValueError("at least one segment row is required")

    validate_segment_chains(materialised)

    grouping_fields = {
        "topology": {row.topology for row in materialised},
        "run_id": {row.run_id for row in materialised},
        "string_id": {row.string_id for row in materialised},
        "inverter_id": {row.inverter_id for row in materialised},
        "mppt_id": {row.mppt_id for row in materialised},
        "cartridge_version": {
            row.cartridge_version for row in materialised
        },
        "schema_version": {row.schema_version for row in materialised},
    }
    mixed = [
        field_name
        for field_name, values in grouping_fields.items()
        if len(values) != 1
    ]
    if mixed:
        raise ValueError(
            "adapter accepts exactly one cartridge string chain; mixed fields: "
            + ", ".join(sorted(mixed))
        )

    ordered = tuple(sorted(materialised, key=lambda row: row.segment_index))
    segment_ids = [row.segment_id for row in ordered]
    duplicates = sorted(
        segment_id
        for segment_id, count in Counter(segment_ids).items()
        if count > 1
    )
    if duplicates:
        raise ValueError(
            "duplicate source segment identifiers: " + ", ".join(duplicates)
        )
    return ordered


def _node_coordinates(
    rows: Sequence[SegmentRow],
) -> dict[str, Point3D]:
    coordinates: dict[str, Point3D] = {}
    for row in rows:
        endpoints = (
            (row.from_node_id, _point(row.from_x, row.from_y, row.from_z)),
            (row.to_node_id, _point(row.to_x, row.to_y, row.to_z)),
        )
        for node_id, position in endpoints:
            existing = coordinates.get(node_id)
            if existing is not None and not _points_match(existing, position):
                raise ValueError(
                    "source node has inconsistent coordinates: "
                    f"{node_id!r}"
                )
            coordinates[node_id] = position
    return coordinates


def _node_object_id(string_id: str, node_id: str) -> str:
    return f"NODE:{string_id}:{node_id}"


def _node_terminal_id(string_id: str, node_id: str) -> str:
    return f"{_node_object_id(string_id, node_id)}:TERMINAL"


def _segment_object_id(segment_id: str) -> str:
    return f"SEGMENT:{segment_id}"


def _segment_terminal_id(segment_id: str, end: str) -> str:
    return f"{_segment_object_id(segment_id)}:{end}"


def _metadata_dict(model: CircuitModel) -> dict[str, object]:
    return {key: value for key, value in model.metadata}


def circuit_boundary_terminal_ids(model: CircuitModel) -> tuple[str, str]:
    """Return adapter-declared start and end boundary terminal identifiers."""

    metadata = _metadata_dict(model)
    start = metadata.get("start_terminal_id")
    end = metadata.get("end_terminal_id")
    if not isinstance(start, str) or not start:
        raise ValueError("circuit model has no adapter start_terminal_id")
    if not isinstance(end, str) or not end:
        raise ValueError("circuit model has no adapter end_terminal_id")
    return start, end


def source_segment_ids(rows: Iterable[SegmentRow]) -> tuple[str, ...]:
    """Return source segment identifiers in validated electrical order."""

    return tuple(row.segment_id for row in _normalise_segment_chain(rows))


def adapt_segment_chain_to_circuit(
    rows: Iterable[SegmentRow],
    *,
    model_id: str | None = None,
) -> CircuitModel:
    """Adapt one ordered cartridge string chain without changing its numbers."""

    ordered = _normalise_segment_chain(rows)
    first = ordered[0]
    last = ordered[-1]
    node_positions = _node_coordinates(ordered)
    node_incidence = Counter(
        node_id
        for row in ordered
        for node_id in (row.from_node_id, row.to_node_id)
    )

    inverter_object_id = f"INVERTER:{first.inverter_id}"
    mppt_object_id = f"MPPT:{first.inverter_id}:{first.mppt_id}"
    string_object_id = f"STRING:{first.string_id}"

    objects: list[PhysicalObject] = [
        PhysicalObject(
            object_id=inverter_object_id,
            kind=ObjectKind.INVERTER,
            terminals=(),
            evidence_class=EvidenceClass.DERIVED,
            source_reference="cartridge_segment_chain",
            attributes=(("inverter_id", first.inverter_id),),
        ),
        PhysicalObject(
            object_id=mppt_object_id,
            kind=ObjectKind.MPPT_INPUT,
            terminals=(),
            parent_object_id=inverter_object_id,
            evidence_class=EvidenceClass.DERIVED,
            source_reference="cartridge_segment_chain",
            attributes=(
                ("inverter_id", first.inverter_id),
                ("mppt_id", first.mppt_id),
            ),
        ),
        PhysicalObject(
            object_id=string_object_id,
            kind=ObjectKind.STRING,
            terminals=(),
            parent_object_id=mppt_object_id,
            evidence_class=EvidenceClass.DERIVED,
            source_reference="cartridge_segment_chain",
            attributes=(
                ("string_id", first.string_id),
                ("topology", first.topology),
            ),
        ),
    ]

    for node_id in sorted(node_positions):
        node_object_id = _node_object_id(first.string_id, node_id)
        node_parent = (
            mppt_object_id
            if node_id.startswith("inverter:")
            else string_object_id
        )
        objects.append(
            PhysicalObject(
                object_id=node_object_id,
                kind=ObjectKind.OTHER,
                terminals=(
                    Terminal(
                        terminal_id=_node_terminal_id(
                            first.string_id,
                            node_id,
                        ),
                        object_id=node_object_id,
                        polarity=TerminalPolarity.UNSPECIFIED,
                        position=node_positions[node_id],
                        required_connection=True,
                        max_connections=node_incidence[node_id],
                        evidence_class=EvidenceClass.DERIVED,
                        source_reference="cartridge_segment_node",
                    ),
                ),
                parent_object_id=node_parent,
                evidence_class=EvidenceClass.DERIVED,
                source_reference="cartridge_segment_node",
                attributes=(
                    ("node_id", node_id),
                    ("role", "electrical_node"),
                ),
            )
        )

    connections: list[Connection] = []
    for row in ordered:
        segment_object_id = _segment_object_id(row.segment_id)
        polarity = _terminal_polarity(row)
        evidence_class = _evidence_class(row)
        from_terminal_id = _segment_terminal_id(row.segment_id, "FROM")
        to_terminal_id = _segment_terminal_id(row.segment_id, "TO")

        objects.append(
            PhysicalObject(
                object_id=segment_object_id,
                kind=_object_kind(row),
                terminals=(
                    Terminal(
                        terminal_id=from_terminal_id,
                        object_id=segment_object_id,
                        polarity=polarity,
                        position=_point(row.from_x, row.from_y, row.from_z),
                        required_connection=True,
                        max_connections=2,
                        evidence_class=evidence_class,
                        source_reference=row.source_reference,
                    ),
                    Terminal(
                        terminal_id=to_terminal_id,
                        object_id=segment_object_id,
                        polarity=polarity,
                        position=_point(row.to_x, row.to_y, row.to_z),
                        required_connection=True,
                        max_connections=2,
                        evidence_class=evidence_class,
                        source_reference=row.source_reference,
                    ),
                ),
                parent_object_id=string_object_id,
                evidence_class=evidence_class,
                source_reference=row.source_reference,
                attributes=tuple(sorted(row.as_dict().items())),
            )
        )

        connections.extend(
            (
                Connection(
                    connection_id=f"NODE_LINK_FROM:{row.segment_id}",
                    from_terminal_id=_node_terminal_id(
                        first.string_id,
                        row.from_node_id,
                    ),
                    to_terminal_id=from_terminal_id,
                    kind=ConnectionKind.ELECTRICAL,
                    evidence_class=EvidenceClass.DERIVED,
                    source_reference="cartridge_adapter_endpoint",
                ),
                Connection(
                    connection_id=f"SEGMENT_INTERNAL:{row.segment_id}",
                    from_terminal_id=from_terminal_id,
                    to_terminal_id=to_terminal_id,
                    kind=ConnectionKind.INTERNAL,
                    segment_id=row.segment_id,
                    evidence_class=evidence_class,
                    source_reference=row.source_reference,
                ),
                Connection(
                    connection_id=f"NODE_LINK_TO:{row.segment_id}",
                    from_terminal_id=to_terminal_id,
                    to_terminal_id=_node_terminal_id(
                        first.string_id,
                        row.to_node_id,
                    ),
                    kind=ConnectionKind.ELECTRICAL,
                    evidence_class=EvidenceClass.DERIVED,
                    source_reference="cartridge_adapter_endpoint",
                ),
            )
        )

    warning_count = len(
        {
            warning
            for row in ordered
            for warning in row.warnings.split(";")
            if warning
        }
    )
    source_hash = hashlib.sha256(
        _source_payload(ordered).encode("utf-8")
    ).hexdigest()

    return CircuitModel(
        model_id=(
            model_id
            or f"V10:{first.topology}:{first.string_id}:canonical-circuit"
        ),
        objects=tuple(objects),
        connections=tuple(connections),
        metadata=(
            ("adapter_version", CARTRIDGE_ADAPTER_VERSION),
            ("source_schema_version", first.schema_version),
            ("source_run_id", first.run_id),
            ("source_topology", first.topology),
            ("source_cartridge_version", first.cartridge_version),
            ("source_inverter_id", first.inverter_id),
            ("source_mppt_id", first.mppt_id),
            ("source_string_id", first.string_id),
            ("source_segment_count", len(ordered)),
            ("source_segment_hash", f"sha256:{source_hash}"),
            ("start_node_id", first.from_node_id),
            ("end_node_id", last.to_node_id),
            (
                "start_terminal_id",
                _node_terminal_id(first.string_id, first.from_node_id),
            ),
            (
                "end_terminal_id",
                _node_terminal_id(first.string_id, last.to_node_id),
            ),
            ("feasibility_status", first.feasibility_status),
            ("saving_available", first.saving_available),
            ("source_warning_count", warning_count),
        ),
    )


def build_sequential_circuit(
    inputs: TopologyInputs,
    definition: StringDefinition,
) -> CircuitModel:
    """Build and adapt one sequential cartridge string."""

    rows = SequentialCartridge().build_segments(inputs, definition)
    return adapt_segment_chain_to_circuit(rows)


def build_leapfrog_circuit(
    inputs: TopologyInputs,
    definition: StringDefinition,
) -> CircuitModel:
    """Build and adapt one leapfrog cartridge string."""

    rows = LeapfrogCartridge().build_segments(inputs, definition)
    return adapt_segment_chain_to_circuit(rows)
