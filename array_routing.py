"""Build 025 explicit conductor geometry, comparison and length receipts.

Topology states what connects. This module derives stored route vertices from that
validated topology and immutable module placement. Every reported length is the
sum of explicit line segments; the browser is not part of the authority path.
"""

from __future__ import annotations

from dataclasses import asdict, replace
import math
from typing import Mapping, Sequence

from geometry_authority import ModulePlacement, Point2D, TableGeometryReceipt
from array_topology import (
    EquipmentProfile,
    InputAllocationReceipt,
    PhysicalInputSpec,
    StringAllocationReceipt,
    StringTopology,
    TableTopologyReceipt,
    WiringStrategy,
    input_spec_by_string,
)
from array_route_types import *
from array_route_geometry import (
    absolute_winding_area,
    bend_count,
    build_interconnect_routes,
    build_route,
    circuit_loop_vertices,
    count_route_crossings,
    entry_u,
    home_route_vertices,
    local_to_world,
    module_row_v,
    parallel_run_distance,
    pole_separation_metrics,
    signed_polygon_area,
    terminal_points,
    world_to_local,
)


def _build_string_routing(
    *,
    geometry: TableGeometryReceipt,
    topology_receipt: TableTopologyReceipt,
    input_allocation: InputAllocationReceipt,
    topology: StringTopology,
    physical_input: PhysicalInputSpec,
    inverter: InverterPlacement,
    placement_by_id: Mapping[str, ModulePlacement],
    terminals: Mapping[str, tuple[Point2D, Point2D]],
    collection_u: float,
    config: RoutingConfig,
) -> StringRoutingReceipt:
    interconnect_routes = build_interconnect_routes(
        topology,
        geometry,
        terminals,
        config,
    )
    first_module = topology.electrical_module_ids[0]
    last_module = topology.electrical_module_ids[-1]
    free_negative = terminals[first_module][0]
    free_positive = terminals[last_module][1]

    inverter_local = world_to_local(inverter.position, geometry)
    input_base = LocalPoint2D(
        inverter_local.u_m + physical_input.offset_u_m,
        inverter_local.v_m + physical_input.offset_v_m,
    )
    half_separation = config.pole_separation_m / 2.0
    input_positive = local_to_world(
        LocalPoint2D(input_base.u_m, input_base.v_m + half_separation),
        geometry,
    )
    input_negative = local_to_world(
        LocalPoint2D(input_base.u_m, input_base.v_m - half_separation),
        geometry,
    )
    row_v = module_row_v(
        topology.physical_module_ids,
        placement_by_id,
        geometry,
    )
    positive_trunk_lane_v = row_v + half_separation
    negative_trunk_lane_v = row_v - half_separation
    positive_exit_lane_v = (
        row_v + config.sequential_row_return_offset_m
        if topology.strategy is WiringStrategy.SEQUENTIAL
        else positive_trunk_lane_v
    )
    entry = entry_u(
        collection_u,
        input_base.u_m,
        config.inverter_entry_offset_u_m,
    )

    positive_route = build_route(
        route_id=f"{topology.string_id}:HOME:P",
        string_id=topology.string_id,
        polarity=RoutePolarity.POSITIVE,
        conductor_scope=ConductorScope.FIELD_INSTALLED,
        from_node_id=f"{physical_input.input_id}:P",
        to_node_id=topology.free_positive_node_id,
        vertices=home_route_vertices(
            free_point=free_positive,
            input_point=input_positive,
            exit_lane_v=positive_exit_lane_v,
            trunk_lane_v=positive_trunk_lane_v,
            collection_u=collection_u,
            entry_u_m=entry,
            geometry=geometry,
            from_input=True,
        ),
        installation_method=config.home_run_installation_method,
        support_path_id=f"{topology.string_id}:HOME-RUN-PAIR",
        home_run=True,
    )
    negative_route = build_route(
        route_id=f"{topology.string_id}:HOME:N",
        string_id=topology.string_id,
        polarity=RoutePolarity.NEGATIVE,
        conductor_scope=ConductorScope.FIELD_INSTALLED,
        from_node_id=topology.free_negative_node_id,
        to_node_id=f"{physical_input.input_id}:N",
        vertices=home_route_vertices(
            free_point=free_negative,
            input_point=input_negative,
            exit_lane_v=negative_trunk_lane_v,
            trunk_lane_v=negative_trunk_lane_v,
            collection_u=collection_u,
            entry_u_m=entry,
            geometry=geometry,
            from_input=False,
        ),
        installation_method=config.home_run_installation_method,
        support_path_id=f"{topology.string_id}:HOME-RUN-PAIR",
        home_run=True,
    )
    circuit_loop = circuit_loop_vertices(
        topology,
        positive_route,
        negative_route,
        interconnect_routes,
        terminals,
    )
    maximum_separation, mean_separation, separation_weight = (
        pole_separation_metrics(positive_route, negative_route)
    )
    series_length = canonical_float(
        math.fsum(
            route.geometric_length_m
            for route in interconnect_routes
        )
    )
    home_length = canonical_float(
        positive_route.geometric_length_m
        + negative_route.geometric_length_m
    )
    all_routes = (
        positive_route,
        negative_route,
        *interconnect_routes,
    )
    metrics = StringRouteMetrics(
        string_id=topology.string_id,
        positive_conductor_length_m=(
            positive_route.geometric_length_m
        ),
        negative_conductor_length_m=(
            negative_route.geometric_length_m
        ),
        series_interconnect_length_m=series_length,
        total_circuit_conductor_length_m=canonical_float(
            series_length + home_length
        ),
        inverter_home_run_length_m=home_length,
        maximum_pole_separation_m=maximum_separation,
        mean_pole_separation_m=mean_separation,
        parallel_run_distance_m=parallel_run_distance(
            positive_route,
            negative_route,
            config.parallel_pairing_max_separation_m,
        ),
        crossings=count_route_crossings(all_routes),
        signed_loop_area_m2=canonical_float(
            signed_polygon_area(circuit_loop)
        ),
        absolute_enclosed_loop_area_m2=canonical_float(
            absolute_winding_area(circuit_loop)
        ),
        separation_weight_m=separation_weight,
    )
    preliminary = StringRoutingReceipt(
        string_id=topology.string_id,
        topology_hash=topology_receipt.topology_hash,
        allocation_hash=input_allocation.allocation_hash,
        inverter_id=inverter.inverter_id,
        input_id=physical_input.input_id,
        mppt_id=physical_input.mppt_id,
        free_negative_point=free_negative,
        free_positive_point=free_positive,
        input_negative_point=input_negative,
        input_positive_point=input_positive,
        positive_route=positive_route,
        negative_route=negative_route,
        interconnect_routes=interconnect_routes,
        circuit_loop_vertices=circuit_loop,
        metrics=metrics,
        routing_hash="",
    )
    basis = asdict(preliminary)
    basis.pop("routing_hash")
    return replace(
        preliminary,
        routing_hash=hash_payload(basis),
    )


def _table_metrics(
    strings: Sequence[StringRoutingReceipt],
) -> TableRouteMetrics:
    weights = math.fsum(
        item.metrics.separation_weight_m for item in strings
    )
    mean = (
        math.fsum(
            item.metrics.mean_pole_separation_m
            * item.metrics.separation_weight_m
            for item in strings
        )
        / weights
        if weights
        else 0.0
    )
    return TableRouteMetrics(
        positive_conductor_length_m=canonical_float(
            math.fsum(
                item.metrics.positive_conductor_length_m
                for item in strings
            )
        ),
        negative_conductor_length_m=canonical_float(
            math.fsum(
                item.metrics.negative_conductor_length_m
                for item in strings
            )
        ),
        series_interconnect_length_m=canonical_float(
            math.fsum(
                item.metrics.series_interconnect_length_m
                for item in strings
            )
        ),
        total_circuit_conductor_length_m=canonical_float(
            math.fsum(
                item.metrics.total_circuit_conductor_length_m
                for item in strings
            )
        ),
        inverter_home_run_length_m=canonical_float(
            math.fsum(
                item.metrics.inverter_home_run_length_m
                for item in strings
            )
        ),
        maximum_pole_separation_m=canonical_float(
            max(
                (
                    item.metrics.maximum_pole_separation_m
                    for item in strings
                ),
                default=0.0,
            )
        ),
        mean_pole_separation_m=canonical_float(mean),
        parallel_run_distance_m=canonical_float(
            math.fsum(
                item.metrics.parallel_run_distance_m
                for item in strings
            )
        ),
        crossings=sum(
            item.metrics.crossings for item in strings
        ),
        signed_loop_area_m2=canonical_float(
            math.fsum(
                item.metrics.signed_loop_area_m2
                for item in strings
            )
        ),
        absolute_enclosed_loop_area_m2=canonical_float(
            math.fsum(
                item.metrics.absolute_enclosed_loop_area_m2
                for item in strings
            )
        ),
    )


def routing_payload(
    receipt: TableRoutingReceipt,
) -> dict[str, object]:
    payload = asdict(receipt)
    payload["loop_area_method_version"] = LOOP_AREA_METHOD_VERSION
    payload["separation_method_version"] = SEPARATION_METHOD_VERSION
    return payload


def build_table_routes(
    geometry: TableGeometryReceipt,
    string_allocation: StringAllocationReceipt,
    topology: TableTopologyReceipt,
    input_allocation: InputAllocationReceipt,
    equipment_profile: EquipmentProfile,
    inverter: InverterPlacement,
    *,
    config: RoutingConfig = RoutingConfig(),
) -> TableRoutingReceipt:
    """Generate one complete deterministic table route receipt."""

    if (
        geometry.table_id != string_allocation.table_id
        or geometry.table_id != topology.table_id
    ):
        raise ValueError(
            "geometry, allocation and topology table identifiers must match"
        )
    if string_allocation.geometry_hash != geometry.geometry_hash:
        raise ValueError(
            "string allocation is not linked to the supplied geometry receipt"
        )
    if topology.assignment_hash != string_allocation.assignment_hash:
        raise ValueError(
            "topology is not linked to the supplied string assignment"
        )
    if input_allocation.assignment_hash != string_allocation.assignment_hash:
        raise ValueError(
            "input allocation is not linked to the supplied string assignment"
        )
    if inverter.inverter_id != equipment_profile.inverter_id:
        raise ValueError(
            "inverter placement and equipment profile identifiers must match"
        )
    if input_allocation.inverter_id != inverter.inverter_id:
        raise ValueError(
            "input allocation and inverter placement identifiers must match"
        )

    placement_by_id = {
        item.module_id: item
        for item in geometry.placements
    }
    if len(placement_by_id) != geometry.module_count:
        raise ValueError(
            "geometry receipt contains duplicate module identifiers"
        )
    terminals = terminal_points(
        geometry,
        config.terminal_layout,
    )
    input_by_string = input_spec_by_string(
        input_allocation,
        equipment_profile,
    )
    topology_by_string = {
        item.string_id: item
        for item in topology.strings
    }
    allocation_string_ids = {
        item.string_id
        for item in string_allocation.assignments
    }
    if not (
        allocation_string_ids
        == set(topology_by_string)
        == set(input_by_string)
    ):
        raise ValueError(
            "string, topology and physical-input identities must match exactly"
        )

    local_envelope_mins = []
    for placement in geometry.placements:
        centre = world_to_local(
            placement.centre,
            geometry,
        )
        local_envelope_mins.append(
            centre.u_m - placement.width_m / 2.0
        )
    collection_u = canonical_float(
        min(local_envelope_mins)
        - config.collection_offset_u_m
    )
    strings = tuple(
        _build_string_routing(
            geometry=geometry,
            topology_receipt=topology,
            input_allocation=input_allocation,
            topology=topology_by_string[string_id],
            physical_input=input_by_string[string_id],
            inverter=inverter,
            placement_by_id=placement_by_id,
            terminals=terminals,
            collection_u=collection_u,
            config=config,
        )
        for string_id in sorted(topology_by_string)
    )
    preliminary = TableRoutingReceipt(
        table_id=geometry.table_id,
        geometry_hash=geometry.geometry_hash,
        assignment_hash=string_allocation.assignment_hash,
        topology_hash=topology.topology_hash,
        input_allocation_hash=input_allocation.allocation_hash,
        strategy=topology.strategy,
        inverter=inverter,
        routing_config=config,
        strings=strings,
        metrics=_table_metrics(strings),
        routing_hash="",
    )
    basis = routing_payload(preliminary)
    basis.pop("routing_hash")
    return replace(
        preliminary,
        routing_hash=hash_payload(basis),
    )


def _field_routes(
    receipt: TableRoutingReceipt,
) -> tuple[ConductorRoute, ...]:
    return tuple(
        route
        for string in receipt.strings
        for route in (
            string.positive_route,
            string.negative_route,
        )
    )


def _factory_routes(
    receipt: TableRoutingReceipt,
) -> tuple[ConductorRoute, ...]:
    return tuple(
        route
        for string in receipt.strings
        for route in string.interconnect_routes
    )


def installed_length_payload(
    receipt: InstalledLengthReceipt,
) -> dict[str, object]:
    return asdict(receipt)


def calculate_installed_length(
    routing: TableRoutingReceipt,
    *,
    policy: InstalledLengthPolicy = InstalledLengthPolicy(),
) -> InstalledLengthReceipt:
    """Keep geometric, installed and procurement length layers separate."""

    route_allowances: list[RouteInstalledLength] = []
    for route in _field_routes(routing):
        connector_approach = (
            2.0
            * policy.connector_approach_m_per_route_end
        )
        harness_offset = policy.harness_offset_m_per_route
        bend_allowance = (
            bend_count(route)
            * policy.bend_allowance_m_per_bend
        )
        support_offset = (
            len(route.segments)
            * policy.support_offset_m_per_segment
        )
        service_loop = policy.service_loop_m_per_route
        termination = (
            2.0
            * policy.termination_allowance_m_per_route_end
        )
        pre_tolerance = math.fsum(
            (
                route.geometric_length_m,
                connector_approach,
                harness_offset,
                bend_allowance,
                support_offset,
                service_loop,
                termination,
            )
        )
        construction_tolerance = (
            pre_tolerance
            * policy.construction_tolerance_fraction
        )
        route_allowances.append(
            RouteInstalledLength(
                route_id=route.route_id,
                string_id=route.string_id,
                polarity=route.polarity,
                geometric_length_m=canonical_float(
                    route.geometric_length_m
                ),
                connector_approach_m=canonical_float(
                    connector_approach
                ),
                harness_offset_m=canonical_float(
                    harness_offset
                ),
                bend_allowance_m=canonical_float(
                    bend_allowance
                ),
                support_offset_m=canonical_float(
                    support_offset
                ),
                service_loop_m=canonical_float(
                    service_loop
                ),
                termination_allowance_m=canonical_float(
                    termination
                ),
                pre_tolerance_installed_length_m=(
                    canonical_float(pre_tolerance)
                ),
                construction_tolerance_m=canonical_float(
                    construction_tolerance
                ),
                installed_length_m=canonical_float(
                    pre_tolerance
                    + construction_tolerance
                ),
            )
        )

    field_geometric = math.fsum(
        route.geometric_length_m
        for route in _field_routes(routing)
    )
    factory_geometric = math.fsum(
        route.geometric_length_m
        for route in _factory_routes(routing)
    )
    installed_field = math.fsum(
        item.installed_length_m
        for item in route_allowances
    )
    spare = (
        installed_field
        * policy.procurement_spare_fraction
    )
    waste = (
        installed_field
        * policy.procurement_waste_fraction
    )
    pre_round = installed_field + spare + waste
    if policy.drum_length_m is None:
        procurement = pre_round
        rounding = 0.0
    else:
        procurement = (
            math.ceil(
                pre_round / policy.drum_length_m
            )
            * policy.drum_length_m
        )
        rounding = procurement - pre_round
    preliminary = InstalledLengthReceipt(
        table_id=routing.table_id,
        routing_hash=routing.routing_hash,
        route_allowances=tuple(route_allowances),
        field_geometric_length_m=canonical_float(
            field_geometric
        ),
        factory_fitted_geometric_length_m=(
            canonical_float(factory_geometric)
        ),
        total_geometric_conductor_length_m=(
            canonical_float(
                field_geometric + factory_geometric
            )
        ),
        installed_field_length_m=canonical_float(
            installed_field
        ),
        procurement_spare_m=canonical_float(spare),
        procurement_waste_m=canonical_float(waste),
        procurement_pre_round_m=canonical_float(
            pre_round
        ),
        drum_rounding_m=canonical_float(rounding),
        procurement_length_m=canonical_float(
            procurement
        ),
        receipt_hash="",
    )
    basis = installed_length_payload(preliminary)
    basis.pop("receipt_hash")
    return replace(
        preliminary,
        receipt_hash=hash_payload(basis),
    )


__all__ = [
    "ConductorRoute",
    "ConductorScope",
    "InstalledLengthPolicy",
    "InstalledLengthReceipt",
    "InstallationMethod",
    "InverterPlacement",
    "LENGTH_RECEIPT_SCHEMA_VERSION",
    "LOOP_AREA_METHOD_VERSION",
    "LocalPoint2D",
    "ModuleTerminalLayout",
    "ROUTING_METHOD_VERSION",
    "ROUTING_SCHEMA_VERSION",
    "RouteClass",
    "RouteInstalledLength",
    "RoutePolarity",
    "RouteSegment",
    "RoutingConfig",
    "SEPARATION_METHOD_VERSION",
    "StringRouteMetrics",
    "StringRoutingReceipt",
    "TableRouteMetrics",
    "TableRoutingReceipt",
    "build_table_routes",
    "calculate_installed_length",
    "installed_length_payload",
    "routing_payload",
]
