"""Independent structural validation for Build 025B string membership."""

from __future__ import annotations

from dataclasses import dataclass

from geometry_authority import TableGeometryReceipt
from table_string_assignment import (
    STRING_ORDER_BASIS,
    TableStringAssignmentReceipt,
)


@dataclass(frozen=True, slots=True)
class StringAssignmentValidationIssue:
    code: str
    message: str


@dataclass(frozen=True, slots=True)
class StringAssignmentValidationResult:
    table_id: str
    valid: bool
    checked_string_count: int
    checked_module_count: int
    issues: tuple[StringAssignmentValidationIssue, ...]


def validate_table_string_assignment(
    geometry: TableGeometryReceipt,
    assignment: TableStringAssignmentReceipt,
) -> StringAssignmentValidationResult:
    """Validate membership without trusting the assignment builder."""

    issues: list[StringAssignmentValidationIssue] = []

    def add(code: str, message: str) -> None:
        issues.append(StringAssignmentValidationIssue(code=code, message=message))

    if assignment.table_id != geometry.table_id:
        add("TABLE_ID_MISMATCH", "assignment table_id does not match geometry")
    if assignment.geometry_hash != geometry.geometry_hash:
        add("GEOMETRY_HASH_MISMATCH", "assignment is not bound to this geometry receipt")
    if assignment.string_count != len(assignment.strings):
        add("STRING_COUNT_MISMATCH", "declared string_count does not match string records")
    if assignment.string_count <= 0:
        add("INVALID_STRING_COUNT", "string_count must be positive")
    if assignment.modules_per_string <= 0:
        add("INVALID_MODULES_PER_STRING", "modules_per_string must be positive")

    string_ids = tuple(item.string_id for item in assignment.strings)
    if len(set(string_ids)) != len(string_ids):
        add("DUPLICATE_STRING_ID", "string identifiers must be unique")

    ordinals = tuple(item.ordinal for item in assignment.strings)
    if ordinals != tuple(range(len(assignment.strings))):
        add("NON_CONTIGUOUS_STRING_ORDINALS", "string ordinals must be contiguous and ordered")

    terminal_ids: list[str] = []
    assigned_module_ids: list[str] = []
    for string in assignment.strings:
        if len(string.ordered_module_ids) != assignment.modules_per_string:
            add(
                "STRING_MODULE_COUNT_MISMATCH",
                f"{string.string_id} does not contain modules_per_string members",
            )
        if string.order_basis != STRING_ORDER_BASIS:
            add(
                "UNSUPPORTED_ORDER_BASIS",
                f"{string.string_id} uses unsupported order basis {string.order_basis!r}",
            )

        positive = string.positive_free_terminal
        negative = string.negative_free_terminal
        if positive.string_id != string.string_id or positive.polarity != "positive":
            add(
                "INVALID_POSITIVE_FREE_TERMINAL",
                f"{string.string_id} positive free terminal is inconsistent",
            )
        if negative.string_id != string.string_id or negative.polarity != "negative":
            add(
                "INVALID_NEGATIVE_FREE_TERMINAL",
                f"{string.string_id} negative free terminal is inconsistent",
            )
        if positive.terminal_id == negative.terminal_id:
            add(
                "COLLAPSED_FREE_TERMINALS",
                f"{string.string_id} positive and negative free terminals share one identifier",
            )

        terminal_ids.extend((positive.terminal_id, negative.terminal_id))
        assigned_module_ids.extend(string.ordered_module_ids)

    if len(set(terminal_ids)) != len(terminal_ids):
        add("DUPLICATE_FREE_TERMINAL_ID", "free terminal identifiers must be globally unique")

    geometry_placements = tuple(sorted(geometry.placements, key=lambda item: item.ordinal))
    geometry_module_ids = tuple(item.module_id for item in geometry_placements)
    if len(geometry_module_ids) != geometry.module_count:
        add("GEOMETRY_PLACEMENT_COUNT_MISMATCH", "geometry placement count is inconsistent")
    if len(set(geometry_module_ids)) != len(geometry_module_ids):
        add("DUPLICATE_GEOMETRY_MODULE_ID", "geometry module identifiers must be unique")

    if len(assigned_module_ids) != geometry.module_count:
        add("ASSIGNED_MODULE_COUNT_MISMATCH", "assigned module count does not match geometry")
    if len(set(assigned_module_ids)) != len(assigned_module_ids):
        add("DUPLICATE_MODULE_ASSIGNMENT", "a module is assigned to more than one string position")

    assigned_set = set(assigned_module_ids)
    geometry_set = set(geometry_module_ids)
    missing = sorted(geometry_set - assigned_set)
    unexpected = sorted(assigned_set - geometry_set)
    if missing:
        add("OMITTED_MODULES", f"assignment omits {len(missing)} geometry modules")
    if unexpected:
        add("UNKNOWN_MODULES", f"assignment contains {len(unexpected)} unknown modules")

    if (
        all(string.order_basis == STRING_ORDER_BASIS for string in assignment.strings)
        and tuple(assigned_module_ids) != geometry_module_ids
    ):
        add(
            "PHYSICAL_ORDER_MISMATCH",
            "placement_ordinal membership does not preserve authoritative geometry order",
        )

    expected_total = assignment.string_count * assignment.modules_per_string
    if expected_total != geometry.module_count:
        add(
            "ASSIGNMENT_CAPACITY_MISMATCH",
            "string_count × modules_per_string does not equal geometry module_count",
        )

    immutable_issues = tuple(issues)
    return StringAssignmentValidationResult(
        table_id=assignment.table_id,
        valid=not immutable_issues,
        checked_string_count=len(assignment.strings),
        checked_module_count=len(assigned_module_ids),
        issues=immutable_issues,
    )
