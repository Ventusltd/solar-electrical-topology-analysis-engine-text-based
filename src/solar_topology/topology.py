"""Headless geometry-to-segment topology generation.

The renderer is deliberately absent. Geometry produces strings and typed conductor
segments; studies and exports can therefore run without any browser dependency.
"""
from __future__ import annotations

from dataclasses import asdict, dataclass
import math
from typing import Iterable, Sequence

from .formulas import Q_, ureg


@dataclass(frozen=True)
class Point3D:
    x_m: float
    y_m: float
    z_m: float


@dataclass(frozen=True)
class Segment:
    segment_id: str
    string_id: str
    sequence_index: int
    segment_type: str
    points_3d: tuple[Point3D, ...]
    geometric_displacement_m: float
    installed_conductor_length_m: float
    formation_type: str
    conductor_separation_mm: float
    provenance: str
    route_length_source: str = "derived_from_segment_geometry"


@dataclass(frozen=True)
class StringTopology:
    string_id: str
    face: str
    band_index: int
    rank_index: int
    module_count: int
    segments: tuple[Segment, ...]

    @property
    def installed_conductor_length_m(self) -> float:
        return sum(segment.installed_conductor_length_m for segment in self.segments)


@dataclass(frozen=True)
class GeometryConfig:
    modules_along_row: int = 30
    modules_per_string: int = 30
    ranks_per_face: int = 5
    faces_per_table: int = 2
    module_width_m: float = 1.303
    module_length_m: float = 2.384
    clamp_gap_m: float = 0.020
    along_gap_m: float = 0.020
    tilt_deg: float = 10.0
    structure_drop_m: float = 2.0
    east_bands: tuple[int, ...] = (5, 5, 2)
    west_bands: tuple[int, ...] = (5, 5, 2)
    inverter_x_m: float = -4.0
    inverter_y_m: float = 0.0


@dataclass(frozen=True)
class FormationConfig:
    module_interconnect_spacing_mm: float = 8.0
    return_spacing_mm: float = 20.0
    coil_surplus_length_m: float = 0.20
    coil_diameter_mm: float = 80.0
    trench_spacing_mm: float = 40.0


def _polyline_length(points: Sequence[Point3D]) -> float:
    return sum(
        math.dist((a.x_m, a.y_m, a.z_m), (b.x_m, b.y_m, b.z_m))
        for a, b in zip(points, points[1:])
    )


def _segment(
    *, string_id: str, sequence_index: int, segment_type: str,
    points: Sequence[Point3D], installed_length_m: float | None,
    formation_type: str, separation_mm: float, provenance: str,
) -> Segment:
    displacement = _polyline_length(points)
    length = displacement if installed_length_m is None else installed_length_m
    if length < 0:
        raise ValueError("Segment installed length cannot be negative")
    return Segment(
        segment_id=f"{string_id}-S{sequence_index:03d}",
        string_id=string_id,
        sequence_index=sequence_index,
        segment_type=segment_type,
        points_3d=tuple(points),
        geometric_displacement_m=displacement,
        installed_conductor_length_m=length,
        formation_type=formation_type,
        conductor_separation_mm=separation_mm,
        provenance=provenance,
    )


def build_string_segments(
    string_id: str,
    face: str,
    band_index: int,
    rank_index: int,
    band_x0_m: float,
    geometry: GeometryConfig,
    formations: FormationConfig,
) -> StringTopology:
    """Build one complete segment chain from physical geometry only."""
    if face not in {"E", "W"}:
        raise ValueError("face must be E or W")
    if geometry.modules_along_row < 1 or geometry.modules_per_string < 1:
        raise ValueError("module counts must be positive")
    if rank_index < 0:
        raise ValueError("rank_index cannot be negative")

    sign = -1 if face == "E" else 1
    theta = math.radians(geometry.tilt_deg)
    rank_pitch_slope = geometry.module_length_m + geometry.clamp_gap_m
    rank_pitch_plan = rank_pitch_slope * math.cos(theta)
    rank_rise = rank_pitch_slope * math.sin(theta)
    module_pitch = geometry.module_width_m + geometry.along_gap_m
    band_length = geometry.modules_along_row * module_pitch - geometry.along_gap_m
    x1 = band_x0_m + band_length
    y = sign * (rank_index + 0.5) * rank_pitch_plan
    z = (rank_index + 0.5) * rank_rise
    sequence = 1
    segments: list[Segment] = []

    for module_index in range(geometry.modules_per_string - 1):
        xa = band_x0_m + (module_index + 0.5) * module_pitch
        xb = band_x0_m + (module_index + 1.5) * module_pitch
        segments.append(_segment(
            string_id=string_id, sequence_index=sequence,
            segment_type="module_interconnect",
            points=(Point3D(xa, y, z), Point3D(xb, y, z)),
            installed_length_m=None, formation_type="rail_mounted_pair",
            separation_mm=formations.module_interconnect_spacing_mm,
            provenance="manufacturer_and_geometry",
        ))
        sequence += 1

    for module_index in range(geometry.modules_per_string):
        x = band_x0_m + (module_index + 0.5) * module_pitch
        for _lead in ("positive", "negative"):
            point = Point3D(x, y, z)
            segments.append(_segment(
                string_id=string_id, sequence_index=sequence,
                segment_type="coiled_surplus", points=(point, point),
                installed_length_m=formations.coil_surplus_length_m,
                formation_type="coiled_pair",
                separation_mm=formations.coil_diameter_mm,
                provenance="defaulted",
            ))
            sequence += 1

    return_y = y + sign * formations.return_spacing_mm / 1000
    segments.append(_segment(
        string_id=string_id, sequence_index=sequence,
        segment_type="along_rank_return",
        points=(Point3D(x1, y, z), Point3D(x1, return_y, z), Point3D(band_x0_m, return_y, z)),
        installed_length_m=None, formation_type="rail_mounted_return",
        separation_mm=formations.return_spacing_mm, provenance="assumed",
    ))
    sequence += 1

    transfer_slope = rank_index * rank_pitch_slope
    transfer_plan = rank_index * rank_pitch_plan
    transfer_rise = rank_index * rank_rise
    transfer_end = Point3D(band_x0_m, sign * 0.08, max(0.0, z - transfer_rise))
    segments.append(_segment(
        string_id=string_id, sequence_index=sequence,
        segment_type="across_table_transfer",
        points=(Point3D(band_x0_m, return_y, z), transfer_end),
        installed_length_m=transfer_slope,
        formation_type="structure_mounted_pair",
        separation_mm=formations.return_spacing_mm,
        provenance="derived",
    ))
    sequence += 1

    drop_end = Point3D(band_x0_m, sign * 0.08, max(0.0, transfer_end.z_m - geometry.structure_drop_m))
    segments.append(_segment(
        string_id=string_id, sequence_index=sequence,
        segment_type="structure_drop",
        points=(transfer_end, drop_end), installed_length_m=geometry.structure_drop_m,
        formation_type="free_air_drop", separation_mm=formations.return_spacing_mm,
        provenance="assumed",
    ))
    sequence += 1

    ground_start = Point3D(band_x0_m, sign * 0.08, 0.0)
    inverter = Point3D(geometry.inverter_x_m, geometry.inverter_y_m, 0.0)
    segments.append(_segment(
        string_id=string_id, sequence_index=sequence,
        segment_type="surface_or_trench_run",
        points=(ground_start, inverter), installed_length_m=None,
        formation_type="buried_or_surface_pair",
        separation_mm=formations.trench_spacing_mm,
        provenance="geometry_and_assumed_formation",
    ))

    return StringTopology(
        string_id=string_id, face=face, band_index=band_index,
        rank_index=rank_index, module_count=geometry.modules_per_string,
        segments=tuple(segments),
    )


def build_site_model(
    geometry: GeometryConfig = GeometryConfig(),
    formations: FormationConfig = FormationConfig(),
) -> tuple[StringTopology, ...]:
    """Build the full site topology headlessly, with arbitrary band lists."""
    result: list[StringTopology] = []
    module_pitch = geometry.module_width_m + geometry.along_gap_m
    band_length = geometry.modules_along_row * module_pitch - geometry.along_gap_m
    band_gap = max(0.5, geometry.along_gap_m * 5)
    definitions: Iterable[tuple[str, tuple[int, ...]]] = (
        ("E", geometry.east_bands),
        ("W", geometry.west_bands if geometry.faces_per_table == 2 else ()),
    )
    for face, bands in definitions:
        x0 = 0.0
        for band_index, rank_count in enumerate(bands):
            for rank_index in range(rank_count):
                string_id = f"{face}-B{band_index+1}-R{rank_index+1}"
                result.append(build_string_segments(
                    string_id, face, band_index, rank_index, x0, geometry, formations,
                ))
            x0 += band_length + band_gap
    return tuple(result)


def build_export(
    strings: Sequence[StringTopology],
    geometry: GeometryConfig,
    formations: FormationConfig,
) -> dict:
    """Return a complete headless export with no user-supplied route length field."""
    string_rows = []
    for string in strings:
        route_length = string.installed_conductor_length_m
        string_rows.append({
            "string_id": string.string_id,
            "face": string.face,
            "band_index": string.band_index,
            "rank_index": string.rank_index,
            "module_count": string.module_count,
            "route_length": {
                "value_m": route_length,
                "source": "segment_list",
                "provenance": "derived",
            },
            "segments": [asdict(segment) for segment in string.segments],
        })
    return {
        "schema_version": "2.0.0-segment-chain",
        "geometry": asdict(geometry),
        "formations": asdict(formations),
        "strings": string_rows,
        "aggregates": {
            "string_count": len(strings),
            "site_installed_conductor_m": sum(s.installed_conductor_length_m for s in strings),
        },
    }


def validate_no_user_route_lengths(export: dict) -> None:
    """Fail if any final route length is not derived from its exported segment list."""
    forbidden_input_keys = {
        "string_length", "route_length", "home_run_length",
        "positive_total_length", "negative_total_length",
    }
    geometry_keys = set(export.get("geometry", {}))
    formation_keys = set(export.get("formations", {}))
    overlap = forbidden_input_keys & (geometry_keys | formation_keys)
    if overlap:
        raise ValueError(f"Forbidden final length input(s): {sorted(overlap)}")

    for string in export.get("strings", []):
        route = string["route_length"]
        segment_sum = sum(s["installed_conductor_length_m"] for s in string["segments"])
        if route.get("source") != "segment_list" or route.get("provenance") != "derived":
            raise ValueError(f"{string['string_id']} route length was not derived")
        if not math.isclose(route["value_m"], segment_sum, rel_tol=1e-12, abs_tol=1e-12):
            raise ValueError(f"{string['string_id']} route length differs from segment sum")
