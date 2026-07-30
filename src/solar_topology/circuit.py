"""Canonical V10 physical-object, terminal and connection records.

This module owns data representation only. Validation is deliberately implemented in
``circuit_validation.py`` so model construction and verification remain separate.
"""

from __future__ import annotations

from dataclasses import dataclass
from enum import StrEnum
import json
from typing import TypeAlias

from .segments import Point3D


CIRCUIT_SCHEMA_VERSION = "globalgrid2050.solar-dc.circuit.v10.1"

ScalarValue: TypeAlias = str | int | float | bool | None
AttributeItems: TypeAlias = tuple[tuple[str, ScalarValue], ...]


class ObjectKind(StrEnum):
    MODULE = "module"
    JUNCTION_BOX = "junction_box"
    FACTORY_LEAD = "factory_lead"
    CONNECTOR = "connector"
    FIELD_CONDUCTOR = "field_conductor"
    HARNESS_BRANCH = "harness_branch"
    HARNESS_NODE = "harness_node"
    HARNESS_TRUNK = "harness_trunk"
    STRING = "string"
    MPPT_INPUT = "mppt_input"
    DC_BUS = "dc_bus"
    INVERTER = "inverter"
    PROTECTIVE_DEVICE = "protective_device"
    SPD = "spd"
    EARTH = "earth"
    MEASUREMENT = "measurement"
    OTHER = "other"


class TerminalPolarity(StrEnum):
    POSITIVE = "positive"
    NEGATIVE = "negative"
    EARTH = "earth"
    INTERNAL = "internal"
    UNSPECIFIED = "unspecified"


class ConnectionKind(StrEnum):
    ELECTRICAL = "electrical"
    INTERNAL = "internal"
    EARTH_BOND = "earth_bond"
    MEASUREMENT = "measurement"


class EvidenceClass(StrEnum):
    MANUFACTURER_DECLARED = "manufacturer_declared"
    FIELD_MEASURED = "field_measured"
    PUBLIC_OBSERVATION = "public_observation"
    USER_CREATED = "user_created"
    DERIVED = "derived"
    GENERIC_EXAMPLE = "generic_example"
    ASSUMED = "assumed"
    EXTERNAL_REFERENCE = "external_reference"


@dataclass(frozen=True)
class Terminal:
    terminal_id: str
    object_id: str
    polarity: TerminalPolarity
    position: Point3D | None = None
    required_connection: bool = True
    max_connections: int = 1
    evidence_class: EvidenceClass = EvidenceClass.ASSUMED
    source_reference: str | None = None


@dataclass(frozen=True)
class PhysicalObject:
    object_id: str
    kind: ObjectKind
    terminals: tuple[Terminal, ...]
    parent_object_id: str | None = None
    evidence_class: EvidenceClass = EvidenceClass.ASSUMED
    source_reference: str | None = None
    attributes: AttributeItems = ()


@dataclass(frozen=True)
class Connection:
    connection_id: str
    from_terminal_id: str
    to_terminal_id: str
    kind: ConnectionKind = ConnectionKind.ELECTRICAL
    segment_id: str | None = None
    evidence_class: EvidenceClass = EvidenceClass.ASSUMED
    source_reference: str | None = None


@dataclass(frozen=True)
class CircuitModel:
    model_id: str
    objects: tuple[PhysicalObject, ...]
    connections: tuple[Connection, ...]
    schema_version: str = CIRCUIT_SCHEMA_VERSION
    metadata: AttributeItems = ()


def _point_payload(point: Point3D | None) -> dict[str, float] | None:
    if point is None:
        return None
    return {"x": point.x, "y": point.y, "z": point.z}


def _attribute_payload(items: AttributeItems) -> dict[str, ScalarValue]:
    return {key: value for key, value in sorted(items, key=lambda item: item[0])}


def canonical_circuit_payload(model: CircuitModel) -> dict:
    """Return a deterministic representation without asserting validity."""

    objects = []
    for obj in sorted(model.objects, key=lambda item: item.object_id):
        terminals = [
            {
                "terminal_id": terminal.terminal_id,
                "object_id": terminal.object_id,
                "polarity": str(terminal.polarity),
                "position": _point_payload(terminal.position),
                "required_connection": terminal.required_connection,
                "max_connections": terminal.max_connections,
                "evidence_class": str(terminal.evidence_class),
                "source_reference": terminal.source_reference,
            }
            for terminal in sorted(obj.terminals, key=lambda item: item.terminal_id)
        ]
        objects.append(
            {
                "object_id": obj.object_id,
                "kind": str(obj.kind),
                "terminals": terminals,
                "parent_object_id": obj.parent_object_id,
                "evidence_class": str(obj.evidence_class),
                "source_reference": obj.source_reference,
                "attributes": _attribute_payload(obj.attributes),
            }
        )

    connections = [
        {
            "connection_id": connection.connection_id,
            "from_terminal_id": connection.from_terminal_id,
            "to_terminal_id": connection.to_terminal_id,
            "kind": str(connection.kind),
            "segment_id": connection.segment_id,
            "evidence_class": str(connection.evidence_class),
            "source_reference": connection.source_reference,
        }
        for connection in sorted(
            model.connections,
            key=lambda item: item.connection_id,
        )
    ]

    return {
        "schema_version": model.schema_version,
        "model_id": model.model_id,
        "objects": objects,
        "connections": connections,
        "metadata": _attribute_payload(model.metadata),
    }


def canonical_circuit_json(model: CircuitModel) -> str:
    """Serialise the deterministic circuit payload for hashing or export."""

    return json.dumps(
        canonical_circuit_payload(model),
        sort_keys=True,
        separators=(",", ":"),
        ensure_ascii=False,
    )
