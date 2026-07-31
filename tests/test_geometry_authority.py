import math

import pytest

from geometry_authority import (
    ModuleDimensions,
    Point2D,
    TableLayoutRequest,
    generate_table_geometry,
    reference_24_by_30_table,
)


def test_reference_table_places_720_unique_modules() -> None:
    receipt = reference_24_by_30_table()

    assert receipt.module_count == 720
    assert len(receipt.placements) == 720
    assert len({placement.module_id for placement in receipt.placements}) == 720
    assert receipt.placements[0].row_index == 0
    assert receipt.placements[0].column_index == 0
    assert receipt.placements[-1].row_index == 23
    assert receipt.placements[-1].column_index == 29


def test_reference_geometry_is_deterministic() -> None:
    first = reference_24_by_30_table()
    second = reference_24_by_30_table()

    assert first == second
    assert first.geometry_hash == second.geometry_hash


def test_moving_origin_changes_coordinates_and_hash() -> None:
    original = reference_24_by_30_table()
    moved = reference_24_by_30_table(origin=Point2D(100.0, -25.0))

    assert moved.placements[0].centre.x_m == pytest.approx(original.placements[0].centre.x_m + 100.0)
    assert moved.placements[0].centre.y_m == pytest.approx(original.placements[0].centre.y_m - 25.0)
    assert moved.geometry_hash != original.geometry_hash


def test_rotation_changes_geometry_without_changing_module_count() -> None:
    original = reference_24_by_30_table()
    rotated = reference_24_by_30_table(rotation_deg=90.0)

    assert rotated.module_count == original.module_count
    assert rotated.geometry_hash != original.geometry_hash
    assert rotated.placements[0].centre.x_m == pytest.approx(-original.placements[0].centre.y_m)
    assert rotated.placements[0].centre.y_m == pytest.approx(original.placements[0].centre.x_m)


def test_landscape_orientation_swaps_module_envelope() -> None:
    request = TableLayoutRequest(
        table_id="LANDSCAPE",
        module_count=1,
        rows=1,
        columns=1,
        module_dimensions=ModuleDimensions(width_m=1.0, height_m=2.0),
        orientation="landscape",
    )

    receipt = generate_table_geometry(request)
    placement = receipt.placements[0]

    assert placement.width_m == pytest.approx(2.0)
    assert placement.height_m == pytest.approx(1.0)
    assert receipt.bounds.max_x_m - receipt.bounds.min_x_m == pytest.approx(2.0)
    assert receipt.bounds.max_y_m - receipt.bounds.min_y_m == pytest.approx(1.0)


def test_partial_final_row_is_supported() -> None:
    receipt = generate_table_geometry(
        TableLayoutRequest(
            table_id="PARTIAL",
            module_count=7,
            rows=2,
            columns=4,
            module_dimensions=ModuleDimensions(width_m=1.0, height_m=2.0),
        )
    )

    assert len(receipt.placements) == 7
    assert receipt.placements[-1].row_index == 1
    assert receipt.placements[-1].column_index == 2


@pytest.mark.parametrize(
    "request",
    [
        TableLayoutRequest,
    ],
)
def test_public_request_type_exists(request: object) -> None:
    assert request is TableLayoutRequest


def test_invalid_capacity_is_rejected() -> None:
    with pytest.raises(ValueError, match="cannot contain"):
        TableLayoutRequest(
            table_id="INVALID",
            module_count=5,
            rows=1,
            columns=4,
            module_dimensions=ModuleDimensions(width_m=1.0, height_m=2.0),
        )


def test_non_finite_geometry_is_rejected() -> None:
    with pytest.raises(ValueError, match="finite"):
        Point2D(math.inf, 0.0)
