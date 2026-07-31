from dataclasses import replace

from geometry_authority import reference_24_by_30_table
from table_string_assignment import assign_modules_to_strings
from table_string_validation import validate_table_string_assignment


def _reference_receipts():
    geometry = reference_24_by_30_table()
    assignment = assign_modules_to_strings(
        geometry,
        string_count=24,
        modules_per_string=30,
    )
    return geometry, assignment


def test_reference_assignment_passes_independent_validation() -> None:
    geometry, assignment = _reference_receipts()

    result = validate_table_string_assignment(geometry, assignment)

    assert result.valid is True
    assert result.checked_string_count == 24
    assert result.checked_module_count == 720
    assert result.issues == ()


def test_cross_string_duplicate_and_omission_are_detected() -> None:
    geometry, assignment = _reference_receipts()
    first = assignment.strings[0]
    second = assignment.strings[1]
    altered_second = replace(
        second,
        ordered_module_ids=(first.ordered_module_ids[0],) + second.ordered_module_ids[1:],
    )
    altered_assignment = replace(
        assignment,
        strings=(first, altered_second) + assignment.strings[2:],
    )

    result = validate_table_string_assignment(geometry, altered_assignment)
    issue_codes = {issue.code for issue in result.issues}

    assert result.valid is False
    assert "DUPLICATE_MODULE_ASSIGNMENT" in issue_codes
    assert "OMITTED_MODULES" in issue_codes
    assert "PHYSICAL_ORDER_MISMATCH" in issue_codes


def test_geometry_binding_mismatch_is_detected() -> None:
    geometry, assignment = _reference_receipts()
    altered_assignment = replace(assignment, geometry_hash="sha256:not-the-geometry")

    result = validate_table_string_assignment(geometry, altered_assignment)

    assert result.valid is False
    assert {issue.code for issue in result.issues} == {"GEOMETRY_HASH_MISMATCH"}


def test_collapsed_free_terminal_identifiers_are_detected() -> None:
    geometry, assignment = _reference_receipts()
    first = assignment.strings[0]
    altered_positive = replace(
        first.positive_free_terminal,
        terminal_id=first.negative_free_terminal.terminal_id,
    )
    altered_first = replace(first, positive_free_terminal=altered_positive)
    altered_assignment = replace(
        assignment,
        strings=(altered_first,) + assignment.strings[1:],
    )

    result = validate_table_string_assignment(geometry, altered_assignment)
    issue_codes = {issue.code for issue in result.issues}

    assert result.valid is False
    assert "COLLAPSED_FREE_TERMINALS" in issue_codes
    assert "DUPLICATE_FREE_TERMINAL_ID" in issue_codes
