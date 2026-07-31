import pytest

from geometry_authority import (
    ModuleDimensions,
    TableLayoutRequest,
    generate_table_geometry,
    reference_24_by_30_table,
)
from array_topology import (
    EdgeKind,
    NodeKind,
    WiringStrategy,
    allocate_physical_inputs,
    allocate_strings,
    build_table_topology,
    electrical_module_order,
    uniform_equipment_profile,
)


def test_reference_allocation_is_a_complete_720_module_partition() -> None:
    geometry = reference_24_by_30_table()
    receipt = allocate_strings(
        geometry,
        string_count=24,
        modules_per_string=30,
    )

    assigned = [
        module_id
        for string in receipt.assignments
        for module_id in string.physical_module_ids
    ]
    assert len(receipt.assignments) == 24
    assert all(
        len(string.physical_module_ids) == 30
        for string in receipt.assignments
    )
    assert len(assigned) == 720
    assert len(set(assigned)) == 720
    assert set(assigned) == {
        placement.module_id
        for placement in geometry.placements
    }
    assert receipt.assignments[0].physical_module_ids == tuple(
        placement.module_id
        for placement in geometry.placements[:30]
    )


def test_allocation_hash_is_membership_deterministic() -> None:
    geometry = reference_24_by_30_table()
    first = allocate_strings(
        geometry,
        string_count=24,
        modules_per_string=30,
    )
    second = allocate_strings(
        geometry,
        string_count=24,
        modules_per_string=30,
    )

    assert first == second
    assert first.assignment_hash == second.assignment_hash


def test_explicit_groups_must_be_complete_and_unique() -> None:
    geometry = generate_table_geometry(
        TableLayoutRequest(
            table_id="SMALL",
            module_count=8,
            rows=2,
            columns=4,
            module_dimensions=ModuleDimensions(
                width_m=1.0,
                height_m=2.0,
            ),
        )
    )
    ids = [placement.module_id for placement in geometry.placements]

    with pytest.raises(
        ValueError,
        match="one-to-one partition",
    ):
        allocate_strings(
            geometry,
            string_count=2,
            modules_per_string=4,
            explicit_module_groups=(
                ids[:4],
                (ids[3], ids[5], ids[6], ids[7]),
            ),
        )


def test_leapfrog_order_is_one_complete_permutation() -> None:
    ids = tuple(
        f"M{index:02d}"
        for index in range(1, 31)
    )
    result = electrical_module_order(
        ids,
        WiringStrategy.LEAPFROG,
    )

    assert result[:5] == (
        "M01",
        "M03",
        "M05",
        "M07",
        "M09",
    )
    assert result[-5:] == (
        "M10",
        "M08",
        "M06",
        "M04",
        "M02",
    )
    assert len(result) == 30
    assert len(set(result)) == 30
    assert set(result) == set(ids)


def test_each_string_has_terminals_connectors_and_free_ends() -> None:
    allocation = allocate_strings(
        reference_24_by_30_table(),
        string_count=24,
        modules_per_string=30,
    )
    receipt = build_table_topology(
        allocation,
        WiringStrategy.LEAPFROG,
    )
    string = receipt.strings[0]
    membership = allocation.strings[0]

    assert sum(
        node.kind is NodeKind.MODULE_NEGATIVE_TERMINAL
        for node in string.nodes
    ) == 30
    assert sum(
        node.kind is NodeKind.MODULE_POSITIVE_TERMINAL
        for node in string.nodes
    ) == 30
    assert sum(
        node.kind is NodeKind.CONNECTOR
        for node in string.nodes
    ) == 58
    assert sum(
        node.kind is NodeKind.STRING_NEGATIVE_FREE_END
        for node in string.nodes
    ) == 1
    assert sum(
        node.kind is NodeKind.STRING_POSITIVE_FREE_END
        for node in string.nodes
    ) == 1
    assert sum(
        edge.kind is EdgeKind.MODULE_INTERNAL
        for edge in string.edges
    ) == 30
    assert sum(
        edge.kind is EdgeKind.CONNECTOR_MATE
        for edge in string.edges
    ) == 29
    assert (
        string.free_negative_node_id
        == membership.negative_free_terminal.terminal_id
    )
    assert (
        string.free_positive_node_id
        == membership.positive_free_terminal.terminal_id
    )


def test_strategy_changes_topology_not_physical_membership() -> None:
    allocation = allocate_strings(
        reference_24_by_30_table(),
        string_count=24,
        modules_per_string=30,
    )
    sequential = build_table_topology(
        allocation,
        WiringStrategy.SEQUENTIAL,
    )
    leapfrog = build_table_topology(
        allocation,
        WiringStrategy.LEAPFROG,
    )

    assert sequential.assignment_hash == leapfrog.assignment_hash
    assert sequential.topology_hash != leapfrog.topology_hash
    assert (
        sequential.strings[0].physical_module_ids
        == leapfrog.strings[0].physical_module_ids
    )
    assert (
        sequential.strings[0].electrical_module_ids
        != leapfrog.strings[0].electrical_module_ids
    )


def test_physical_inputs_are_distinct_from_mppt_labels() -> None:
    allocation = allocate_strings(
        reference_24_by_30_table(),
        string_count=24,
        modules_per_string=30,
    )
    profile = uniform_equipment_profile(
        mppt_count=12,
        inputs_per_mppt=2,
    )
    receipt = allocate_physical_inputs(
        allocation,
        profile,
    )

    assert len(receipt.assignments) == 24
    assert len({item.input_id for item in receipt.assignments}) == 24
    assert len({item.mppt_id for item in receipt.assignments}) == 12
    assert receipt.assignments[0].mppt_id == receipt.assignments[1].mppt_id
    assert receipt.assignments[0].input_id != receipt.assignments[1].input_id
    assert receipt.unused_input_ids == ()
    assert receipt.unused_mppt_ids == ()


def test_duplicate_physical_input_assignment_fails_before_routing() -> None:
    geometry = generate_table_geometry(
        TableLayoutRequest(
            table_id="INPUT-FAIL",
            module_count=4,
            rows=2,
            columns=2,
            module_dimensions=ModuleDimensions(
                width_m=1.0,
                height_m=2.0,
            ),
        )
    )
    allocation = allocate_strings(
        geometry,
        string_count=2,
        modules_per_string=2,
    )
    profile = uniform_equipment_profile(
        mppt_count=1,
        inputs_per_mppt=2,
    )
    first_input = profile.physical_inputs[0].input_id
    explicit = {
        assignment.string_id: first_input
        for assignment in allocation.assignments
    }

    with pytest.raises(
        ValueError,
        match="exceeds its string capacity",
    ):
        allocate_physical_inputs(
            allocation,
            profile,
            explicit_input_by_string=explicit,
        )
