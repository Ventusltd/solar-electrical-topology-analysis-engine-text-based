"""Deterministic geometry screening receipts from ordered segment rows.

The method is an explicit engineering approximation. It integrates local
conductor length multiplied by declared pole separation and the segment's
loop-parameter participation weight. It is not a field solution and does not
invent missing return-path geometry.
"""

from __future__ import annotations

from dataclasses import dataclass
import hashlib
import json
import math
from typing import Iterable

from .segments import SegmentRow


GEOMETRY_RECEIPT_SCHEMA_VERSION = "globalgrid2050.solar-dc.geometry-receipt.v10.1"
GEOMETRY_METHOD_VERSION = "weighted-length-times-separation.v10.1"


@dataclass(frozen=True)
class SegmentGeometryResult:
    segment_id: str
    conductor_length_m: float
    separation_m: float
    participation_weight: float
    loop_area_contribution_m2: float


@dataclass(frozen=True)
class GeometryReceipt:
    receipt_id: str
    run_id: str
    topology: str
    string_id: str
    segment_results: tuple[SegmentGeometryResult, ...]
    loop_area_m2: float
    maximum_local_separation_m: float
    paired_route_length_m: float
    total_route_length_m: float
    paired_route_fraction: float
    warnings: tuple[str, ...]
    schema_version: str = GEOMETRY_RECEIPT_SCHEMA_VERSION
    method_version: str = GEOMETRY_METHOD_VERSION


def calculate_geometry_receipt(rows: Iterable[SegmentRow]) -> GeometryReceipt:
    ordered = tuple(sorted(rows, key=lambda row: row.segment_index))
    if not ordered:
        raise ValueError("at least one segment row is required")
    for row in ordered:
        row.validate()
    identities = {(row.run_id, row.topology, row.string_id) for row in ordered}
    if len(identities) != 1:
        raise ValueError("geometry receipt requires one run, topology and string")
    indexes = [row.segment_index for row in ordered]
    if indexes != list(range(1, len(ordered) + 1)):
        raise ValueError("segment indexes must be contiguous from one")

    results: list[SegmentGeometryResult] = []
    warnings: list[str] = []
    paired_length = 0.0
    total_length = math.fsum(row.conductor_length_m for row in ordered)
    for row in ordered:
        separation_m = row.separation_mm / 1000.0
        contribution = (
            row.conductor_length_m * separation_m * row.loop_parameter_weight
        )
        results.append(
            SegmentGeometryResult(
                segment_id=row.segment_id,
                conductor_length_m=row.conductor_length_m,
                separation_m=separation_m,
                participation_weight=row.loop_parameter_weight,
                loop_area_contribution_m2=contribution,
            )
        )
        if row.loop_parameter_weight > 0:
            paired_length += row.conductor_length_m
        if row.separation_mm <= 0 and row.loop_parameter_weight > 0:
            warnings.append(
                f"segment {row.segment_id!r} participates in loop geometry but has no separation"
            )
        if row.provenance in {"assumed", "defaulted"}:
            warnings.append(
                f"segment {row.segment_id!r} geometry uses {row.provenance} evidence"
            )

    loop_area = math.fsum(result.loop_area_contribution_m2 for result in results)
    maximum = max(result.separation_m for result in results)
    fraction = paired_length / total_length if total_length else 0.0
    run_id, topology, string_id = next(iter(identities))
    basis = {
        "method_version": GEOMETRY_METHOD_VERSION,
        "run_id": run_id,
        "topology": topology,
        "string_id": string_id,
        "segments": [
            [result.segment_id, result.conductor_length_m, result.separation_m,
             result.participation_weight]
            for result in results
        ],
    }
    digest = hashlib.sha256(
        json.dumps(basis, sort_keys=True, separators=(",", ":")).encode("utf-8")
    ).hexdigest()
    return GeometryReceipt(
        receipt_id=f"GEO:{digest}",
        run_id=run_id,
        topology=topology,
        string_id=string_id,
        segment_results=tuple(results),
        loop_area_m2=loop_area,
        maximum_local_separation_m=maximum,
        paired_route_length_m=paired_length,
        total_route_length_m=total_length,
        paired_route_fraction=fraction,
        warnings=tuple(sorted(set(warnings))),
    )


def geometry_receipt_payload(receipt: GeometryReceipt) -> dict[str, object]:
    return {
        "schema_version": receipt.schema_version,
        "method_version": receipt.method_version,
        "receipt_id": receipt.receipt_id,
        "run_id": receipt.run_id,
        "topology": receipt.topology,
        "string_id": receipt.string_id,
        "loop_area_m2": receipt.loop_area_m2,
        "maximum_local_separation_m": receipt.maximum_local_separation_m,
        "paired_route_length_m": receipt.paired_route_length_m,
        "total_route_length_m": receipt.total_route_length_m,
        "paired_route_fraction": receipt.paired_route_fraction,
        "warnings": list(receipt.warnings),
        "segments": [
            {
                "segment_id": result.segment_id,
                "conductor_length_m": result.conductor_length_m,
                "separation_m": result.separation_m,
                "participation_weight": result.participation_weight,
                "loop_area_contribution_m2": result.loop_area_contribution_m2,
            }
            for result in receipt.segment_results
        ],
    }


def geometry_receipt_json(receipt: GeometryReceipt) -> str:
    return json.dumps(
        geometry_receipt_payload(receipt),
        sort_keys=True,
        separators=(",", ":"),
        ensure_ascii=False,
    )


def geometry_receipt_hash(receipt: GeometryReceipt) -> str:
    digest = hashlib.sha256(geometry_receipt_json(receipt).encode("utf-8")).hexdigest()
    return f"sha256:{digest}"
