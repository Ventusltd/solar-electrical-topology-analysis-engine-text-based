"""Deterministic module-to-string membership for Build 025B.

This module binds authoritative table placements into stable string membership.
It deliberately does not choose sequential or leapfrog electrical routing; those
strategies consume the same membership receipt in Build 025C.
"""

from __future__ import annotations

from dataclasses import asdict, dataclass
from hashlib import sha256
import json
from typing import Literal

from geometry_authority import TableGeometryReceipt


Polarity = Literal["positive", "negative"]
STRING_ASSIGNMENT_SCHEMA_VERSION = "0.1.0"
STRING_ORDER_BASIS = "placement_ordinal"


@dataclass(frozen=True, slots=True)
class StringFreeTerminal:
    """A logical string boundary terminal, before route geometry is generated."""

    terminal_id: str
    string_id: str
    polarity: Polarity

    def __post_init__(self) -> None:
        if not self.terminal_id.strip():
            raise ValueError("terminal_id must not be empty")
        if not self.string_id.strip():
            raise ValueError("string_id must not be empty")
        if self.polarity not in ("positive", "negative"):
            raise ValueError("polarity must be positive or negative")


@dataclass(frozen=True, slots=True)
class OrderedStringMembership:
    """One string's stable module membership in physical placement order."""

    string_id: str
    ordinal: int
    ordered_module_ids: tuple[str, ...]
    order_basis: str
    positive_free_terminal: StringFreeTerminal
    negative_free_terminal: StringFreeTerminal

    def __post_init__(self) -> None:
        if not self.string_id.strip():
            raise ValueError("string_id must not be empty")
        if self.ordinal < 0:
            raise ValueError("ordinal must be non-negative")
        if not self.ordered_module_ids:
            raise ValueError("ordered_module_ids must not be empty")
        if len(set(self.ordered_module_ids)) != len(self.ordered_module_ids):
            raise ValueError("ordered_module_ids must be unique within a string")
        if not self.order_basis.strip():
            raise ValueError("order_basis must not be empty")
        for terminal, polarity in (
            (self.positive_free_terminal, "positive"),
            (self.negative_free_terminal, "negative"),
        ):
            if terminal.string_id != self.string_id:
                raise ValueError("free terminal string_id must match membership string_id")
            if terminal.polarity != polarity:
                raise ValueError(f"expected {polarity} free terminal")


@dataclass(frozen=True, slots=True)
class TableStringAssignmentReceipt:
    """Content-addressed string membership bound to one geometry receipt."""

    schema_version: str
    table_id: str
    geometry_hash: str
    string_count: int
    modules_per_string: int
    strings: tuple[OrderedStringMembership, ...]
    assignment_hash: str


def _canonical_payload(
    *,
    geometry: TableGeometryReceipt,
    string_count: int,
    modules_per_string: int,
    strings: tuple[OrderedStringMembership, ...],
) -> dict[str, object]:
    return {
        "schema_version": STRING_ASSIGNMENT_SCHEMA_VERSION,
        "table_id": geometry.table_id,
        "geometry_hash": geometry.geometry_hash,
        "string_count": string_count,
        "modules_per_string": modules_per_string,
        "strings": [
            {
                "string_id": item.string_id,
                "ordinal": item.ordinal,
                "ordered_module_ids": list(item.ordered_module_ids),
                "order_basis": item.order_basis,
                "positive_free_terminal": {
                    "terminal_id": item.positive_free_terminal.terminal_id,
                    "string_id": item.positive_free_terminal.string_id,
                    "polarity": item.positive_free_terminal.polarity,
                },
                "negative_free_terminal": {
                    "terminal_id": item.negative_free_terminal.terminal_id,
                    "string_id": item.negative_free_terminal.string_id,
                    "polarity": item.negative_free_terminal.polarity,
                },
            }
            for item in strings
        ],
    }


def assign_modules_to_strings(
    geometry: TableGeometryReceipt,
    *,
    string_count: int,
    modules_per_string: int,
) -> TableStringAssignmentReceipt:
    """Bind placements to strings in deterministic placement-ordinal chunks.

    The order records physical membership only. Sequential and leapfrog cartridges
    may later traverse these same members in different electrical orders without
    changing the assignment hash.
    """

    if string_count <= 0:
        raise ValueError("string_count must be positive")
    if modules_per_string <= 0:
        raise ValueError("modules_per_string must be positive")
    expected_module_count = string_count * modules_per_string
    if geometry.module_count != expected_module_count:
        raise ValueError(
            "geometry module_count must equal string_count × modules_per_string"
        )
    if len(geometry.placements) != geometry.module_count:
        raise ValueError("geometry placement count must equal geometry module_count")

    placements = tuple(sorted(geometry.placements, key=lambda item: item.ordinal))
    expected_ordinals = tuple(range(geometry.module_count))
    actual_ordinals = tuple(item.ordinal for item in placements)
    if actual_ordinals != expected_ordinals:
        raise ValueError("geometry placement ordinals must be unique and contiguous")

    module_ids = tuple(item.module_id for item in placements)
    if len(set(module_ids)) != len(module_ids):
        raise ValueError("geometry module identifiers must be unique")

    memberships: list[OrderedStringMembership] = []
    for string_ordinal in range(string_count):
        string_id = f"{geometry.table_id}-STR-{string_ordinal + 1:03d}"
        start = string_ordinal * modules_per_string
        stop = start + modules_per_string
        memberships.append(
            OrderedStringMembership(
                string_id=string_id,
                ordinal=string_ordinal,
                ordered_module_ids=module_ids[start:stop],
                order_basis=STRING_ORDER_BASIS,
                positive_free_terminal=StringFreeTerminal(
                    terminal_id=f"{string_id}-TERM-POS",
                    string_id=string_id,
                    polarity="positive",
                ),
                negative_free_terminal=StringFreeTerminal(
                    terminal_id=f"{string_id}-TERM-NEG",
                    string_id=string_id,
                    polarity="negative",
                ),
            )
        )

    immutable_memberships = tuple(memberships)
    payload = _canonical_payload(
        geometry=geometry,
        string_count=string_count,
        modules_per_string=modules_per_string,
        strings=immutable_memberships,
    )
    encoded = json.dumps(
        payload,
        sort_keys=True,
        separators=(",", ":"),
        ensure_ascii=True,
    ).encode("utf-8")
    assignment_hash = f"sha256:{sha256(encoded).hexdigest()}"

    return TableStringAssignmentReceipt(
        schema_version=STRING_ASSIGNMENT_SCHEMA_VERSION,
        table_id=geometry.table_id,
        geometry_hash=geometry.geometry_hash,
        string_count=string_count,
        modules_per_string=modules_per_string,
        strings=immutable_memberships,
        assignment_hash=assignment_hash,
    )


def assignment_as_dict(receipt: TableStringAssignmentReceipt) -> dict[str, object]:
    """Return a JSON-compatible representation for evidence transport."""

    return asdict(receipt)
