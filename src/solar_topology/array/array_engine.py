"""Public Build 025 whole-table geometry and topology orchestration.

The browser may serialise and display these receipts, but it does not create route
vertices, lengths, topology, input allocation, loop metrics or hashes.
"""

from __future__ import annotations

from dataclasses import dataclass
from hashlib import sha256
import json
from typing import Mapping, Sequence

from geometry_authority import (
    Point2D,
    TableGeometryReceipt,
    reference_24_by_30_table,
)
from array_topology import (
    DEFAULT_BUILD_025_LIMITS,
    Build025Limits,
    EquipmentProfile,
    InputAllocationReceipt,
    StringAllocationReceipt,
    TableTopologyReceipt,
    WiringStrategy,
    allocate_physical_inputs,
    allocate_strings,
    allocation_payload,
    attach_input_topology,
    build_table_topology,
    equipment_profile_payload,
    input_allocation_payload,
    topology_payload,
    uniform_equipment_profile,
)
from array_routing import (
    InstalledLengthPolicy,
    InstalledLengthReceipt,
    InverterPlacement,
    RoutingConfig,
    TableRouteMetrics,
    TableRoutingReceipt,
    build_table_routes,
    calculate_installed_length,
    installed_length_payload,
    routing_payload,
)


BUILD_025_SCHEMA_VERSION = "globalgrid2050.solar-dc.build-025.v1"
STRATEGY_COMPARISON_SCHEMA_VERSION = (
    "globalgrid2050.solar-dc.strategy-comparison.v1"
)


@dataclass(frozen=True, slots=True)
class Build025Receipt:
    geometry: TableGeometryReceipt
    string_allocation: StringAllocationReceipt
    topology: TableTopologyReceipt
    equipment_profile: EquipmentProfile
    input_allocation: InputAllocationReceipt
    routing: TableRoutingReceipt
    installed_length: InstalledLengthReceipt
    receipt_hash: str
    schema_version: str = BUILD_025_SCHEMA_VERSION


@dataclass(frozen=True, slots=True)
class MetricDelta:
    metric: str
    sequential_value: float | int
    leapfrog_value: float | int
    leapfrog_minus_sequential: float | int


@dataclass(frozen=True, slots=True)
class StrategyComparisonReceipt:
    table_id: str
    geometry_hash: str
    assignment_hash: str
    input_allocation_hash: str
    inverter: InverterPlacement
    sequential: Build025Receipt
    leapfrog: Build025Receipt
    deltas: tuple[MetricDelta, ...]
    comparison_hash: str
    schema_version: str = STRATEGY_COMPARISON_SCHEMA_VERSION


def _canonical_json(payload: object) -> str:
    return json.dumps(
        payload,
        sort_keys=True,
        separators=(",", ":"),
        ensure_ascii=True,
    )


def _hash_payload(payload: object) -> str:
    digest = sha256(_canonical_json(payload).encode("utf-8")).hexdigest()
    return f"sha256:{digest}"


def _geometry_summary(
    geometry: TableGeometryReceipt,
) -> dict[str, object]:
    return {
        "schema_version": geometry.schema_version,
        "table_id": geometry.table_id,
        "module_count": geometry.module_count,
        "rows": geometry.rows,
        "columns": geometry.columns,
        "orientation": geometry.orientation,
        "origin_m": [
            geometry.origin.x_m,
            geometry.origin.y_m,
        ],
        "rotation_deg": geometry.rotation_deg,
        "bounds_m": [
            geometry.bounds.min_x_m,
            geometry.bounds.min_y_m,
            geometry.bounds.max_x_m,
            geometry.bounds.max_y_m,
        ],
        "geometry_hash": geometry.geometry_hash,
        "placements": [
            {
                "module_id": item.module_id,
                "ordinal": item.ordinal,
                "row_index": item.row_index,
                "column_index": item.column_index,
                "centre_m": [
                    item.centre.x_m,
                    item.centre.y_m,
                ],
                "width_m": item.width_m,
                "height_m": item.height_m,
                "rotation_deg": item.rotation_deg,
            }
            for item in geometry.placements
        ],
    }


def build025_payload(
    receipt: Build025Receipt,
) -> dict[str, object]:
    return {
        "schema_version": receipt.schema_version,
        "receipt_hash": receipt.receipt_hash,
        "geometry": _geometry_summary(receipt.geometry),
        "string_allocation": allocation_payload(
            receipt.string_allocation
        ),
        "topology": topology_payload(receipt.topology),
        "equipment_profile": equipment_profile_payload(
            receipt.equipment_profile
        ),
        "input_allocation": input_allocation_payload(
            receipt.input_allocation
        ),
        "routing": routing_payload(receipt.routing),
        "installed_length": installed_length_payload(
            receipt.installed_length
        ),
    }


def build_complete_table(
    geometry: TableGeometryReceipt,
    *,
    string_count: int,
    modules_per_string: int,
    strategy: WiringStrategy | str,
    equipment_profile: EquipmentProfile,
    inverter: InverterPlacement,
    explicit_module_groups: Sequence[Sequence[str]] | None = None,
    explicit_input_by_string: Mapping[str, str] | None = None,
    routing_config: RoutingConfig = RoutingConfig(),
    installed_length_policy: InstalledLengthPolicy = InstalledLengthPolicy(),
    limits: Build025Limits = DEFAULT_BUILD_025_LIMITS,
) -> Build025Receipt:
    """Build one complete table without standards or electrical physics."""

    allocation = allocate_strings(
        geometry,
        string_count=string_count,
        modules_per_string=modules_per_string,
        explicit_module_groups=explicit_module_groups,
        limits=limits,
    )
    string_topology = build_table_topology(
        allocation,
        strategy,
    )
    input_allocation = allocate_physical_inputs(
        allocation,
        equipment_profile,
        explicit_input_by_string=explicit_input_by_string,
    )
    topology = attach_input_topology(
        string_topology,
        input_allocation,
        equipment_profile,
    )
    routing = build_table_routes(
        geometry,
        allocation,
        topology,
        input_allocation,
        equipment_profile,
        inverter,
        config=routing_config,
    )
    installed_length = calculate_installed_length(
        routing,
        policy=installed_length_policy,
    )
    basis = {
        "schema_version": BUILD_025_SCHEMA_VERSION,
        "geometry_hash": geometry.geometry_hash,
        "assignment_hash": allocation.assignment_hash,
        "topology_hash": topology.topology_hash,
        "equipment_profile": equipment_profile_payload(
            equipment_profile
        ),
        "input_allocation_hash": (
            input_allocation.allocation_hash
        ),
        "routing_hash": routing.routing_hash,
        "installed_length_hash": installed_length.receipt_hash,
    }
    return Build025Receipt(
        geometry=geometry,
        string_allocation=allocation,
        topology=topology,
        equipment_profile=equipment_profile,
        input_allocation=input_allocation,
        routing=routing,
        installed_length=installed_length,
        receipt_hash=_hash_payload(basis),
    )


def reference_24_by_30_build(
    *,
    strategy: WiringStrategy | str = WiringStrategy.LEAPFROG,
    inverter_position: Point2D = Point2D(-5.0, 27.0),
    equipment_profile: EquipmentProfile | None = None,
    routing_config: RoutingConfig = RoutingConfig(),
    installed_length_policy: InstalledLengthPolicy = InstalledLengthPolicy(),
) -> Build025Receipt:
    """Build the canonical 720-module acceptance fixture."""

    profile = equipment_profile or uniform_equipment_profile()
    return build_complete_table(
        reference_24_by_30_table(),
        string_count=24,
        modules_per_string=30,
        strategy=strategy,
        equipment_profile=profile,
        inverter=InverterPlacement(
            profile.inverter_id,
            inverter_position,
        ),
        routing_config=routing_config,
        installed_length_policy=installed_length_policy,
    )


def _metric_deltas(
    sequential: TableRouteMetrics,
    leapfrog: TableRouteMetrics,
) -> tuple[MetricDelta, ...]:
    metric_names = (
        "positive_conductor_length_m",
        "negative_conductor_length_m",
        "series_interconnect_length_m",
        "total_circuit_conductor_length_m",
        "inverter_home_run_length_m",
        "maximum_pole_separation_m",
        "mean_pole_separation_m",
        "parallel_run_distance_m",
        "crossings",
        "signed_loop_area_m2",
        "absolute_enclosed_loop_area_m2",
    )
    deltas: list[MetricDelta] = []
    for metric in metric_names:
        sequential_value = getattr(sequential, metric)
        leapfrog_value = getattr(leapfrog, metric)
        difference = leapfrog_value - sequential_value
        if isinstance(difference, float):
            difference = round(difference, 9)
        deltas.append(
            MetricDelta(
                metric=metric,
                sequential_value=sequential_value,
                leapfrog_value=leapfrog_value,
                leapfrog_minus_sequential=difference,
            )
        )
    return tuple(deltas)


def strategy_comparison_payload(
    receipt: StrategyComparisonReceipt,
) -> dict[str, object]:
    return {
        "schema_version": receipt.schema_version,
        "table_id": receipt.table_id,
        "geometry_hash": receipt.geometry_hash,
        "assignment_hash": receipt.assignment_hash,
        "input_allocation_hash": (
            receipt.input_allocation_hash
        ),
        "inverter": {
            "inverter_id": receipt.inverter.inverter_id,
            "position_m": [
                receipt.inverter.position.x_m,
                receipt.inverter.position.y_m,
            ],
        },
        "sequential_receipt_hash": (
            receipt.sequential.receipt_hash
        ),
        "leapfrog_receipt_hash": (
            receipt.leapfrog.receipt_hash
        ),
        "deltas": [
            {
                "metric": item.metric,
                "sequential_value": item.sequential_value,
                "leapfrog_value": item.leapfrog_value,
                "leapfrog_minus_sequential": (
                    item.leapfrog_minus_sequential
                ),
            }
            for item in receipt.deltas
        ],
        "comparison_hash": receipt.comparison_hash,
    }


def compare_wiring_strategies(
    geometry: TableGeometryReceipt,
    *,
    string_count: int,
    modules_per_string: int,
    equipment_profile: EquipmentProfile,
    inverter: InverterPlacement,
    explicit_module_groups: Sequence[Sequence[str]] | None = None,
    explicit_input_by_string: Mapping[str, str] | None = None,
    routing_config: RoutingConfig = RoutingConfig(),
    installed_length_policy: InstalledLengthPolicy = InstalledLengthPolicy(),
    limits: Build025Limits = DEFAULT_BUILD_025_LIMITS,
) -> StrategyComparisonReceipt:
    """Compare strategies over identical placement, inputs and inverter."""

    common = {
        "geometry": geometry,
        "string_count": string_count,
        "modules_per_string": modules_per_string,
        "equipment_profile": equipment_profile,
        "inverter": inverter,
        "explicit_module_groups": explicit_module_groups,
        "explicit_input_by_string": explicit_input_by_string,
        "routing_config": routing_config,
        "installed_length_policy": installed_length_policy,
        "limits": limits,
    }
    sequential = build_complete_table(
        strategy=WiringStrategy.SEQUENTIAL,
        **common,
    )
    leapfrog = build_complete_table(
        strategy=WiringStrategy.LEAPFROG,
        **common,
    )
    if (
        sequential.geometry.geometry_hash
        != leapfrog.geometry.geometry_hash
    ):
        raise AssertionError(
            "strategy comparison changed module geometry"
        )
    if (
        sequential.string_allocation.assignment_hash
        != leapfrog.string_allocation.assignment_hash
    ):
        raise AssertionError(
            "strategy comparison changed string membership"
        )
    if (
        sequential.input_allocation.allocation_hash
        != leapfrog.input_allocation.allocation_hash
    ):
        raise AssertionError(
            "strategy comparison changed physical-input allocation"
        )
    deltas = _metric_deltas(
        sequential.routing.metrics,
        leapfrog.routing.metrics,
    )
    preliminary = StrategyComparisonReceipt(
        table_id=geometry.table_id,
        geometry_hash=geometry.geometry_hash,
        assignment_hash=(
            sequential.string_allocation.assignment_hash
        ),
        input_allocation_hash=(
            sequential.input_allocation.allocation_hash
        ),
        inverter=inverter,
        sequential=sequential,
        leapfrog=leapfrog,
        deltas=deltas,
        comparison_hash="",
    )
    basis = strategy_comparison_payload(preliminary)
    basis.pop("comparison_hash")
    return StrategyComparisonReceipt(
        table_id=preliminary.table_id,
        geometry_hash=preliminary.geometry_hash,
        assignment_hash=preliminary.assignment_hash,
        input_allocation_hash=(
            preliminary.input_allocation_hash
        ),
        inverter=preliminary.inverter,
        sequential=preliminary.sequential,
        leapfrog=preliminary.leapfrog,
        deltas=preliminary.deltas,
        comparison_hash=_hash_payload(basis),
    )


def compare_reference_24_by_30(
    *,
    inverter_position: Point2D = Point2D(-5.0, 27.0),
    equipment_profile: EquipmentProfile | None = None,
    routing_config: RoutingConfig = RoutingConfig(),
    installed_length_policy: InstalledLengthPolicy = InstalledLengthPolicy(),
) -> StrategyComparisonReceipt:
    profile = equipment_profile or uniform_equipment_profile()
    return compare_wiring_strategies(
        reference_24_by_30_table(),
        string_count=24,
        modules_per_string=30,
        equipment_profile=profile,
        inverter=InverterPlacement(
            profile.inverter_id,
            inverter_position,
        ),
        routing_config=routing_config,
        installed_length_policy=installed_length_policy,
    )


__all__ = [
    "BUILD_025_SCHEMA_VERSION",
    "STRATEGY_COMPARISON_SCHEMA_VERSION",
    "Build025Receipt",
    "MetricDelta",
    "StrategyComparisonReceipt",
    "build025_payload",
    "build_complete_table",
    "compare_reference_24_by_30",
    "compare_wiring_strategies",
    "reference_24_by_30_build",
    "strategy_comparison_payload",
]
