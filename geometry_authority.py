"""Deterministic, geometry-authoritative PV table placement.

Build 025A intentionally contains no electrical physics. It establishes immutable
module placement and a canonical geometry receipt for later topology and routing.
"""

from __future__ import annotations

from dataclasses import asdict, dataclass
from hashlib import sha256
import json
import math
from typing import Literal


Orientation = Literal["portrait", "landscape"]


@dataclass(frozen=True, slots=True)
class Point2D:
    """A point in site-local metres."""

    x_m: float
    y_m: float

    def __post_init__(self) -> None:
        if not math.isfinite(self.x_m) or not math.isfinite(self.y_m):
            raise ValueError("Point coordinates must be finite")


@dataclass(frozen=True, slots=True)
class ModuleDimensions:
    """Physical module face dimensions before orientation is applied."""

    width_m: float
    height_m: float

    def __post_init__(self) -> None:
        if not math.isfinite(self.width_m) or self.width_m <= 0:
            raise ValueError("Module width must be finite and positive")
        if not math.isfinite(self.height_m) or self.height_m <= 0:
            raise ValueError("Module height must be finite and positive")

    def oriented(self, orientation: Orientation) -> tuple[float, float]:
        if orientation == "portrait":
            return self.width_m, self.height_m
        if orientation == "landscape":
            return self.height_m, self.width_m
        raise ValueError(f"Unsupported module orientation: {orientation!r}")


@dataclass(frozen=True, slots=True)
class TableLayoutRequest:
    """Canonical request for a regular rectangular PV table."""

    table_id: str
    module_count: int
    rows: int
    columns: int
    module_dimensions: ModuleDimensions
    orientation: Orientation = "portrait"
    horizontal_gap_m: float = 0.02
    vertical_gap_m: float = 0.02
    origin: Point2D = Point2D(0.0, 0.0)
    rotation_deg: float = 0.0

    def __post_init__(self) -> None:
        if not self.table_id.strip():
            raise ValueError("table_id must not be empty")
        if self.module_count <= 0:
            raise ValueError("module_count must be positive")
        if self.rows <= 0 or self.columns <= 0:
            raise ValueError("rows and columns must be positive")
        if self.module_count > self.rows * self.columns:
            raise ValueError("rows × columns cannot contain module_count")
        if self.orientation not in ("portrait", "landscape"):
            raise ValueError("orientation must be portrait or landscape")
        for name, value in (
            ("horizontal_gap_m", self.horizontal_gap_m),
            ("vertical_gap_m", self.vertical_gap_m),
        ):
            if not math.isfinite(value) or value < 0:
                raise ValueError(f"{name} must be finite and non-negative")
        if not math.isfinite(self.rotation_deg):
            raise ValueError("rotation_deg must be finite")


@dataclass(frozen=True, slots=True)
class ModulePlacement:
    """One module's authoritative centre point and oriented envelope."""

    module_id: str
    ordinal: int
    row_index: int
    column_index: int
    centre: Point2D
    width_m: float
    height_m: float
    rotation_deg: float


@dataclass(frozen=True, slots=True)
class TableBounds:
    min_x_m: float
    min_y_m: float
    max_x_m: float
    max_y_m: float


@dataclass(frozen=True, slots=True)
class TableGeometryReceipt:
    schema_version: str
    table_id: str
    module_count: int
    rows: int
    columns: int
    orientation: Orientation
    origin: Point2D
    rotation_deg: float
    bounds: TableBounds
    placements: tuple[ModulePlacement, ...]
    geometry_hash: str


def _canonical_float(value: float) -> float:
    """Normalise insignificant binary noise before hashing receipts."""

    rounded = round(value, 9)
    return 0.0 if rounded == -0.0 else rounded


def _rotate_translate(local_x: float, local_y: float, request: TableLayoutRequest) -> Point2D:
    theta = math.radians(request.rotation_deg)
    cos_theta = math.cos(theta)
    sin_theta = math.sin(theta)
    return Point2D(
        _canonical_float(request.origin.x_m + local_x * cos_theta - local_y * sin_theta),
        _canonical_float(request.origin.y_m + local_x * sin_theta + local_y * cos_theta),
    )


def _corners(placement: ModulePlacement) -> tuple[Point2D, Point2D, Point2D, Point2D]:
    half_w = placement.width_m / 2.0
    half_h = placement.height_m / 2.0
    theta = math.radians(placement.rotation_deg)
    cos_theta = math.cos(theta)
    sin_theta = math.sin(theta)
    points: list[Point2D] = []
    for dx, dy in ((-half_w, -half_h), (half_w, -half_h), (half_w, half_h), (-half_w, half_h)):
        points.append(
            Point2D(
                _canonical_float(placement.centre.x_m + dx * cos_theta - dy * sin_theta),
                _canonical_float(placement.centre.y_m + dx * sin_theta + dy * cos_theta),
            )
        )
    return tuple(points)  # type: ignore[return-value]


def _canonical_payload(
    request: TableLayoutRequest,
    placements: tuple[ModulePlacement, ...],
    bounds: TableBounds,
) -> dict[str, object]:
    return {
        "schema_version": "0.1.0",
        "table_id": request.table_id,
        "module_count": request.module_count,
        "rows": request.rows,
        "columns": request.columns,
        "orientation": request.orientation,
        "module_dimensions_m": {
            "width": _canonical_float(request.module_dimensions.width_m),
            "height": _canonical_float(request.module_dimensions.height_m),
        },
        "horizontal_gap_m": _canonical_float(request.horizontal_gap_m),
        "vertical_gap_m": _canonical_float(request.vertical_gap_m),
        "origin_m": [_canonical_float(request.origin.x_m), _canonical_float(request.origin.y_m)],
        "rotation_deg": _canonical_float(request.rotation_deg),
        "bounds_m": [
            _canonical_float(bounds.min_x_m),
            _canonical_float(bounds.min_y_m),
            _canonical_float(bounds.max_x_m),
            _canonical_float(bounds.max_y_m),
        ],
        "placements": [
            {
                "module_id": item.module_id,
                "ordinal": item.ordinal,
                "row_index": item.row_index,
                "column_index": item.column_index,
                "centre_m": [
                    _canonical_float(item.centre.x_m),
                    _canonical_float(item.centre.y_m),
                ],
                "width_m": _canonical_float(item.width_m),
                "height_m": _canonical_float(item.height_m),
                "rotation_deg": _canonical_float(item.rotation_deg),
            }
            for item in placements
        ],
    }


def generate_table_geometry(request: TableLayoutRequest) -> TableGeometryReceipt:
    """Generate deterministic row-major module placements and a content hash.

    The first module is centred at half a module width/height from the table-local
    origin. Unused cells, when capacity exceeds module_count, occur at the end of
    row-major ordering. String assignment is deliberately deferred to Build 025B.
    """

    module_width_m, module_height_m = request.module_dimensions.oriented(request.orientation)
    pitch_x = module_width_m + request.horizontal_gap_m
    pitch_y = module_height_m + request.vertical_gap_m

    placements: list[ModulePlacement] = []
    for ordinal in range(request.module_count):
        row_index, column_index = divmod(ordinal, request.columns)
        local_x = module_width_m / 2.0 + column_index * pitch_x
        local_y = module_height_m / 2.0 + row_index * pitch_y
        placements.append(
            ModulePlacement(
                module_id=f"{request.table_id}-MOD-{ordinal + 1:04d}",
                ordinal=ordinal,
                row_index=row_index,
                column_index=column_index,
                centre=_rotate_translate(local_x, local_y, request),
                width_m=module_width_m,
                height_m=module_height_m,
                rotation_deg=_canonical_float(request.rotation_deg),
            )
        )

    immutable_placements = tuple(placements)
    all_corners = [corner for placement in immutable_placements for corner in _corners(placement)]
    bounds = TableBounds(
        min_x_m=_canonical_float(min(point.x_m for point in all_corners)),
        min_y_m=_canonical_float(min(point.y_m for point in all_corners)),
        max_x_m=_canonical_float(max(point.x_m for point in all_corners)),
        max_y_m=_canonical_float(max(point.y_m for point in all_corners)),
    )

    payload = _canonical_payload(request, immutable_placements, bounds)
    encoded = json.dumps(payload, sort_keys=True, separators=(",", ":"), ensure_ascii=True).encode("utf-8")
    geometry_hash = f"sha256:{sha256(encoded).hexdigest()}"

    return TableGeometryReceipt(
        schema_version="0.1.0",
        table_id=request.table_id,
        module_count=request.module_count,
        rows=request.rows,
        columns=request.columns,
        orientation=request.orientation,
        origin=request.origin,
        rotation_deg=_canonical_float(request.rotation_deg),
        bounds=bounds,
        placements=immutable_placements,
        geometry_hash=geometry_hash,
    )


def receipt_as_dict(receipt: TableGeometryReceipt) -> dict[str, object]:
    """Return a JSON-compatible representation for evidence and browser transport."""

    return asdict(receipt)


def reference_24_by_30_table(
    *,
    table_id: str = "TABLE-001",
    origin: Point2D = Point2D(0.0, 0.0),
    rotation_deg: float = 0.0,
) -> TableGeometryReceipt:
    """Build the initial 24-string × 30-module geometry fixture.

    This function establishes 24 rows of 30 modules. String membership is not yet
    asserted; Build 025B will bind each row to an ordered string explicitly.
    """

    return generate_table_geometry(
        TableLayoutRequest(
            table_id=table_id,
            module_count=720,
            rows=24,
            columns=30,
            module_dimensions=ModuleDimensions(width_m=1.134, height_m=2.278),
            orientation="portrait",
            horizontal_gap_m=0.02,
            vertical_gap_m=0.02,
            origin=origin,
            rotation_deg=rotation_deg,
        )
    )
