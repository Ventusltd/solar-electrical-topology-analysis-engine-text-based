import pytest

from geometry_authority import reference_24_by_30_table
from table_string_assignment import assign_modules_to_strings


def _reference_assignment():
    geometry = reference_24_by_30_table()
    assignment = assign_modules_to_strings(
        geometry,
        string_count=24,
        modules_per_string=30,
    )
    return geometry, assignment


def test_reference_assignment_covers_all_720_modules_once() -> None:
    geometry, assignment = _reference_assignment()

    assigned_module_ids = tuple(
        module_id
        for string in assignment.strings
        for module_id in string.ordered_module_ids
    )
    geometry_module_ids = tuple(
        placement.module_id
        for placement in sorted(geometry.placements, key=lambda item: item.ordinal)
    )

    assert assignment.string_count == 24
    assert len(assignment.strings) == 24
    assert all(len(string.ordered_module_ids) == 30 for string in assignment.strings)
    assert len(assigned_module_ids) == 720
    assert len(set(assigned_module_ids)) == 720
    assert assigned_module_ids == geometry_module_ids


def test_reference_assignment_has_one_free_terminal_per_polarity() -> None:
    _, assignment = _reference_assignment()

    terminal_ids = []
    for string in assignment.strings:
        assert string.positive_free_terminal.string_id == string.string_id
        assert string.positive_free_terminal.polarity == "positive"
        assert string.negative_free_terminal.string_id == string.string_id
        assert string.negative_free_terminal.polarity == "negative"
        terminal_ids.extend(
            (
                string.positive_free_terminal.terminal_id,
                string.negative_free_terminal.terminal_id,
            )
        )

    assert len(terminal_ids) == 48
    assert len(set(terminal_ids)) == 48


def test_reference_assignment_is_deterministic() -> None:
    _, first = _reference_assignment()
    _, second = _reference_assignment()

    assert first == second
    assert first.assignment_hash == second.assignment_hash


def test_reference_assignment_preserves_physical_placement_order() -> None:
    _, assignment = _reference_assignment()

    assert assignment.strings[0].string_id == "TABLE-001-STR-001"
    assert assignment.strings[0].ordered_module_ids[0] == "TABLE-001-MOD-0001"
    assert assignment.strings[0].ordered_module_ids[-1] == "TABLE-001-MOD-0030"
    assert assignment.strings[-1].string_id == "TABLE-001-STR-024"
    assert assignment.strings[-1].ordered_module_ids[0] == "TABLE-001-MOD-0691"
    assert assignment.strings[-1].ordered_module_ids[-1] == "TABLE-001-MOD-0720"


def test_incompatible_string_dimensions_are_rejected() -> None:
    geometry = reference_24_by_30_table()

    with pytest.raises(ValueError, match="module_count"):
        assign_modules_to_strings(
            geometry,
            string_count=23,
            modules_per_string=30,
        )
