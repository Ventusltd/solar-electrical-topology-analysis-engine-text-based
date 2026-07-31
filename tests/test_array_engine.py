import math

import pytest

from geometry_authority import (
    ModuleDimensions,
    Point2D,
    TableLayoutRequest,
    generate_table_geometry,
)
from array_engine import (
    build_complete_table,
    compare_reference_24_by_30,
    reference_24_by_30_build,
)
from array_routing import (
    InstalledLengthPolicy,
    InstallationMethod,
    InverterPlacement,
    ModuleTerminalLayout,
    RoutingConfig,
)
from array_topology import NodeKind, WiringStrategy, uniform_equipment_profile


@pytest.fixture(scope="module")
def comparison():
    return compare_reference_24_by_30()


def test_reference_build_is_deterministic() -> None:
    first = reference_24_by_30_build()
    second = reference_24_by_30_build()

    assert first.receipt_hash == second.receipt_hash
    assert first.routing.routing_hash == second.routing.routing_hash
    assert (
        first.string_allocation.assignment_hash
        == second.string_allocation.assignment_hash
    )
    assert first.topology.topology_hash == second.topology.topology_hash


def test_every_reported_route_length_is_the_sum_of_stored_segments(
    comparison,
) -> None:
    for build in (comparison.sequential, comparison.leapfrog):
        route_total = 0.0
        for string in build.routing.strings:
            routes = (
                string.positive_route,
                string.negative_route,
                *string.interconnect_routes,
            )
            for route in routes:
                segment_sum = math.fsum(
                    segment.geometric_length_m
                    for segment in route.segments
                )
                assert segment_sum == pytest.approx(
                    route.geometric_length_m,
                    abs=1e-8,
                )
                route_total += route.geometric_length_m
        assert route_total == pytest.approx(
            build.routing.metrics.total_circuit_conductor_length_m,
            abs=1e-7,
        )


def test_strategy_comparison_preserves_common_authority_inputs(
    comparison,
) -> None:
    assert (
        comparison.sequential.geometry.geometry_hash
        == comparison.leapfrog.geometry.geometry_hash
    )
    assert (
        comparison.sequential.string_allocation.assignment_hash
        == comparison.leapfrog.string_allocation.assignment_hash
    )
    assert (
        comparison.sequential.input_allocation.allocation_hash
        == comparison.leapfrog.input_allocation.allocation_hash
    )
    assert (
        comparison.sequential.topology.topology_hash
        != comparison.leapfrog.topology.topology_hash
    )
    assert (
        comparison.sequential.routing.routing_hash
        != comparison.leapfrog.routing.routing_hash
    )


def test_comparison_reports_length_and_loop_geometry_independently(
    comparison,
) -> None:
    sequential = comparison.sequential.routing.metrics
    leapfrog = comparison.leapfrog.routing.metrics

    assert (
        leapfrog.positive_conductor_length_m
        < sequential.positive_conductor_length_m
    )
    assert (
        leapfrog.inverter_home_run_length_m
        < sequential.inverter_home_run_length_m
    )
    assert (
        leapfrog.absolute_enclosed_loop_area_m2
        < sequential.absolute_enclosed_loop_area_m2
    )
    assert (
        leapfrog.series_interconnect_length_m
        > sequential.series_interconnect_length_m
    )
    assert (
        leapfrog.total_circuit_conductor_length_m
        != sequential.total_circuit_conductor_length_m
    )
    assert (
        leapfrog.absolute_enclosed_loop_area_m2
        >= abs(leapfrog.signed_loop_area_m2)
    )
    assert (
        sequential.absolute_enclosed_loop_area_m2
        >= abs(sequential.signed_loop_area_m2)
    )


def test_moving_inverter_changes_only_dependent_home_geometry() -> None:
    original = reference_24_by_30_build(
        strategy=WiringStrategy.LEAPFROG,
        inverter_position=Point2D(-5.0, 27.0),
    )
    moved = reference_24_by_30_build(
        strategy=WiringStrategy.LEAPFROG,
        inverter_position=Point2D(-15.0, 31.0),
    )

    assert original.geometry.geometry_hash == moved.geometry.geometry_hash
    assert (
        original.string_allocation.assignment_hash
        == moved.string_allocation.assignment_hash
    )
    assert original.topology.topology_hash == moved.topology.topology_hash
    assert (
        original.input_allocation.allocation_hash
        == moved.input_allocation.allocation_hash
    )
    assert original.routing.routing_hash != moved.routing.routing_hash
    assert (
        original.routing.metrics.inverter_home_run_length_m
        != moved.routing.metrics.inverter_home_run_length_m
    )
    for before, after in zip(
        original.routing.strings,
        moved.routing.strings,
    ):
        assert [
            route.route_hash for route in before.interconnect_routes
        ] == [
            route.route_hash for route in after.interconnect_routes
        ]
        assert (
            before.positive_route.route_hash
            != after.positive_route.route_hash
        )
        assert (
            before.negative_route.route_hash
            != after.negative_route.route_hash
        )


def test_home_run_segments_preserve_same_string_pole_identity(
    comparison,
) -> None:
    for string in comparison.leapfrog.routing.strings:
        assert string.positive_route.string_id == string.string_id
        assert string.negative_route.string_id == string.string_id
        assert all(
            segment.string_id == string.string_id
            for segment in string.positive_route.segments
        )
        assert all(
            segment.string_id == string.string_id
            for segment in string.negative_route.segments
        )
        assert {
            segment.support_path_id
            for segment in string.positive_route.segments
        } == {
            segment.support_path_id
            for segment in string.negative_route.segments
        }


def test_every_route_endpoint_is_an_authoritative_topology_node() -> None:
    build = reference_24_by_30_build()
    node_ids = {
        node.node_id
        for string in build.topology.strings
        for node in string.nodes
    } | {
        node.node_id for node in build.topology.equipment_nodes
    }

    for string in build.routing.strings:
        for route in (
            string.positive_route,
            string.negative_route,
            *string.interconnect_routes,
        ):
            assert route.from_node_id in node_ids
            assert route.to_node_id in node_ids


def test_reference_topology_contains_input_mppt_and_bus_terminals() -> None:
    build = reference_24_by_30_build()
    kinds = [node.kind for node in build.topology.equipment_nodes]

    assert kinds.count(NodeKind.PHYSICAL_INPUT_NEGATIVE) == 24
    assert kinds.count(NodeKind.PHYSICAL_INPUT_POSITIVE) == 24
    assert kinds.count(NodeKind.MPPT_INPUT) == 24
    assert kinds.count(NodeKind.INVERTER_DC_BUS) == 2
    assert len(build.topology.equipment_edges) == 120


def test_installed_and_procurement_length_layers_are_receipted() -> None:
    policy = InstalledLengthPolicy(
        connector_approach_m_per_route_end=0.10,
        harness_offset_m_per_route=0.20,
        bend_allowance_m_per_bend=0.05,
        support_offset_m_per_segment=0.02,
        service_loop_m_per_route=0.50,
        termination_allowance_m_per_route_end=0.25,
        construction_tolerance_fraction=0.03,
        procurement_spare_fraction=0.02,
        procurement_waste_fraction=0.01,
        drum_length_m=500.0,
    )
    build = reference_24_by_30_build(
        installed_length_policy=policy
    )
    receipt = build.installed_length

    assert len(receipt.route_allowances) == 48
    assert receipt.field_geometric_length_m == pytest.approx(
        build.routing.metrics.inverter_home_run_length_m
    )
    assert receipt.factory_fitted_geometric_length_m == pytest.approx(
        build.routing.metrics.series_interconnect_length_m
    )
    assert receipt.total_geometric_conductor_length_m == pytest.approx(
        build.routing.metrics.total_circuit_conductor_length_m
    )
    assert (
        receipt.installed_field_length_m
        > receipt.field_geometric_length_m
    )
    assert (
        receipt.procurement_pre_round_m
        > receipt.installed_field_length_m
    )
    assert receipt.procurement_length_m % 500.0 == pytest.approx(0.0)
    assert receipt.drum_rounding_m >= 0
    assert all(
        item.connector_approach_m == pytest.approx(0.20)
        for item in receipt.route_allowances
    )
    assert all(
        item.termination_allowance_m == pytest.approx(0.50)
        for item in receipt.route_allowances
    )


def test_installation_classification_is_carried_by_each_segment() -> None:
    config = RoutingConfig(
        home_run_installation_method=InstallationMethod.BURIED
    )
    build = reference_24_by_30_build(routing_config=config)

    for string in build.routing.strings:
        for route in (string.positive_route, string.negative_route):
            assert all(segment.buried for segment in route.segments)
            assert all(
                not segment.screened for segment in route.segments
            )
            assert all(
                segment.installation_method
                is InstallationMethod.BURIED
                for segment in route.segments
            )


def test_parametric_small_rotated_table_uses_same_engine() -> None:
    geometry = generate_table_geometry(
        TableLayoutRequest(
            table_id="ROTATED",
            module_count=8,
            rows=2,
            columns=4,
            module_dimensions=ModuleDimensions(
                width_m=1.1,
                height_m=2.0,
            ),
            horizontal_gap_m=0.03,
            vertical_gap_m=0.30,
            origin=Point2D(100.0, -20.0),
            rotation_deg=35.0,
        )
    )
    profile = uniform_equipment_profile(
        profile_id="SMALL-INPUTS",
        inverter_id="INV-SMALL",
        mppt_count=2,
        inputs_per_mppt=1,
    )
    build = build_complete_table(
        geometry,
        string_count=2,
        modules_per_string=4,
        strategy=WiringStrategy.LEAPFROG,
        equipment_profile=profile,
        inverter=InverterPlacement(
            "INV-SMALL",
            Point2D(95.0, -16.0),
        ),
    )

    assert len(build.routing.strings) == 2
    assert build.routing.metrics.total_circuit_conductor_length_m > 0
    assert (
        build.routing.metrics.absolute_enclosed_loop_area_m2
        >= abs(build.routing.metrics.signed_loop_area_m2)
    )


def test_terminal_geometry_outside_module_envelope_is_rejected() -> None:
    invalid = RoutingConfig(
        terminal_layout=ModuleTerminalLayout(
            negative_offset_u_m=-10.0,
            positive_offset_u_m=10.0,
            source_reference="deliberately_invalid_test_fixture",
        )
    )

    with pytest.raises(ValueError, match="outside module"):
        reference_24_by_30_build(routing_config=invalid)
