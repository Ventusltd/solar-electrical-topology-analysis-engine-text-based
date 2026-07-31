"""Build 025C topology and physical-input allocation.

Build 025B membership is owned by ``table_string_assignment.py`` and independently
checked by ``table_string_validation.py``. This module consumes that canonical
receipt to add electrical traversal, connector nodes and equipment allocation. It
contains no cable routing, electrical physics, standards arithmetic or browser
logic.
"""

from __future__ import annotations

from collections import Counter
from dataclasses import dataclass, fields
from enum import StrEnum
from hashlib import sha256
import json
import math
from typing import Mapping, Sequence

from geometry_authority import TableGeometryReceipt
from table_string_assignment import (
    STRING_ASSIGNMENT_SCHEMA_VERSION,
    OrderedStringMembership,
    TableStringAssignmentReceipt,
    assign_modules_to_strings,
    assignment_as_dict,
)
from table_string_validation import validate_table_string_assignment


StringAssignment = OrderedStringMembership
StringAllocationReceipt = TableStringAssignmentReceipt
STRING_ALLOCATION_SCHEMA_VERSION = STRING_ASSIGNMENT_SCHEMA_VERSION
TOPOLOGY_SCHEMA_VERSION = "globalgrid2050.solar-dc.table-topology.v1"
INPUT_ALLOCATION_SCHEMA_VERSION = "globalgrid2050.solar-dc.input-allocation.v1"
EQUIPMENT_PROFILE_SCHEMA_VERSION = "globalgrid2050.solar-dc.equipment-profile.v1"


class WiringStrategy(StrEnum):
    SEQUENTIAL = "sequential"
    LEAPFROG = "leapfrog"


class NodeKind(StrEnum):
    MODULE_NEGATIVE_TERMINAL = "module_negative_terminal"
    MODULE_POSITIVE_TERMINAL = "module_positive_terminal"
    CONNECTOR = "connector"
    STRING_NEGATIVE_FREE_END = "string_negative_free_end"
    STRING_POSITIVE_FREE_END = "string_positive_free_end"
    PHYSICAL_INPUT_NEGATIVE = "physical_input_negative"
    PHYSICAL_INPUT_POSITIVE = "physical_input_positive"
    MPPT_INPUT = "mppt_input"
    INVERTER_DC_BUS = "inverter_dc_bus"
    PARALLEL_JUNCTION = "parallel_junction"
    STRING_FUSE = "string_fuse"
    GROUP_OVER_CURRENT_DEVICE = "group_over_current_device"
    COMBINER_BUS = "combiner_bus"
    SPD_CONNECTION = "spd_connection"
    PROTECTIVE_EARTH = "protective_earth"
    BONDING_NODE = "bonding_node"


class EdgeKind(StrEnum):
    MODULE_INTERNAL = "module_internal"
    FACTORY_LEAD = "factory_lead"
    CONNECTOR_MATE = "connector_mate"
    BOUNDARY_LINK = "boundary_link"
    INPUT_LINK = "input_link"
    MPPT_LINK = "mppt_link"
    PARALLEL_LINK = "parallel_link"
    PROTECTIVE_DEVICE_LINK = "protective_device_link"
    SPD_LINK = "spd_link"
    EARTH_BOND = "earth_bond"


@dataclass(frozen=True, slots=True)
class Build025Limits:
    """Application-test limits, not universal electrical limits."""

    maximum_modules_per_table: int = 2_000
    maximum_strings_per_table: int = 64
    maximum_modules_per_string: int = 60
    maximum_mppts_per_inverter: int = 32
    maximum_physical_inputs_per_inverter: int = 64
    maximum_inverters_per_table: int = 8

    def __post_init__(self) -> None:
        for item in fields(self):
            value = getattr(self, item.name)
            if value <= 0:
                raise ValueError(f"{item.name} must be positive")


DEFAULT_BUILD_025_LIMITS = Build025Limits()


@dataclass(frozen=True, slots=True)
class TopologyNode:
    node_id: str
    kind: NodeKind
    string_id: str | None = None
    module_id: str | None = None
    equipment_id: str | None = None


@dataclass(frozen=True, slots=True)
class TopologyEdge:
    edge_id: str
    kind: EdgeKind
    from_node_id: str
    to_node_id: str
    string_id: str | None = None
    module_id: str | None = None
    connection_ordinal: int | None = None


@dataclass(frozen=True, slots=True)
class StringTopology:
    string_id: str
    strategy: WiringStrategy
    physical_module_ids: tuple[str, ...]
    electrical_module_ids: tuple[str, ...]
    free_negative_node_id: str
    free_positive_node_id: str
    nodes: tuple[TopologyNode, ...]
    edges: tuple[TopologyEdge, ...]


@dataclass(frozen=True, slots=True)
class TableTopologyReceipt:
    table_id: str
    assignment_hash: str
    strategy: WiringStrategy
    strings: tuple[StringTopology, ...]
    node_count: int
    edge_count: int
    topology_hash: str
    schema_version: str = TOPOLOGY_SCHEMA_VERSION


@dataclass(frozen=True, slots=True)
class PhysicalInputSpec:
    """One physical inverter input, distinct from its MPPT label."""

    input_id: str
    mppt_id: str
    offset_u_m: float
    offset_v_m: float
    maximum_strings: int = 1
    isolated: bool = True
    parallel_node_id: str | None = None
    protective_device_node_id: str | None = None

    def __post_init__(self) -> None:
        if not self.input_id.strip() or not self.mppt_id.strip():
            raise ValueError("physical input and MPPT identifiers must not be empty")
        if not math.isfinite(self.offset_u_m) or not math.isfinite(self.offset_v_m):
            raise ValueError("physical-input offsets must be finite")
        if self.maximum_strings <= 0:
            raise ValueError("maximum_strings must be positive")
        if self.isolated and self.parallel_node_id is not None:
            raise ValueError("an isolated physical input cannot declare a parallel node")


@dataclass(frozen=True, slots=True)
class EquipmentProfile:
    profile_id: str
    inverter_id: str
    mppt_ids: tuple[str, ...]
    physical_inputs: tuple[PhysicalInputSpec, ...]
    dc_bus_node_id: str
    schema_version: str = EQUIPMENT_PROFILE_SCHEMA_VERSION

    def __post_init__(self) -> None:
        if not self.profile_id.strip() or not self.inverter_id.strip():
            raise ValueError("profile_id and inverter_id must not be empty")
        if not self.dc_bus_node_id.strip():
            raise ValueError("dc_bus_node_id must not be empty")
        if not self.mppt_ids:
            raise ValueError("an equipment profile requires at least one MPPT")
        if len(set(self.mppt_ids)) != len(self.mppt_ids):
            raise ValueError("MPPT identifiers must be unique")
        if not self.physical_inputs:
            raise ValueError("an equipment profile requires at least one physical input")
        input_ids = [item.input_id for item in self.physical_inputs]
        if len(set(input_ids)) != len(input_ids):
            raise ValueError("physical input identifiers must be unique")
        unknown = sorted({item.mppt_id for item in self.physical_inputs} - set(self.mppt_ids))
        if unknown:
            raise ValueError(f"physical inputs reference unknown MPPTs: {unknown}")


@dataclass(frozen=True, slots=True)
class InputAssignment:
    string_id: str
    input_id: str
    mppt_id: str


@dataclass(frozen=True, slots=True)
class InputAllocationReceipt:
    table_id: str
    assignment_hash: str
    equipment_profile_id: str
    inverter_id: str
    assignments: tuple[InputAssignment, ...]
    unused_input_ids: tuple[str, ...]
    unused_mppt_ids: tuple[str, ...]
    allocation_hash: str
    schema_version: str = INPUT_ALLOCATION_SCHEMA_VERSION


def _canonical_json(payload: object) -> str:
    return json.dumps(payload, sort_keys=True, separators=(",", ":"), ensure_ascii=True)


def _hash_payload(payload: object) -> str:
    digest = sha256(_canonical_json(payload).encode("utf-8")).hexdigest()
    return f"sha256:{digest}"


def allocation_payload(receipt: StringAllocationReceipt) -> dict[str, object]:
    return assignment_as_dict(receipt)


def allocate_strings(
    geometry: TableGeometryReceipt,
    *,
    string_count: int,
    modules_per_string: int,
    explicit_module_groups: Sequence[Sequence[str]] | None = None,
    limits: Build025Limits = DEFAULT_BUILD_025_LIMITS,
) -> StringAllocationReceipt:
    """Use the canonical Build 025B placement-ordinal membership receipt."""

    if geometry.module_count > limits.maximum_modules_per_table:
        raise ValueError("module count exceeds Build 025 application limit")
    if string_count > limits.maximum_strings_per_table:
        raise ValueError("string count exceeds Build 025 application limit")
    if modules_per_string > limits.maximum_modules_per_string:
        raise ValueError("modules per string exceeds Build 025 application limit")

    receipt = assign_modules_to_strings(
        geometry,
        string_count=string_count,
        modules_per_string=modules_per_string,
    )
    if explicit_module_groups is not None:
        normalised = tuple(tuple(group) for group in explicit_module_groups)
        canonical_groups = tuple(item.ordered_module_ids for item in receipt.strings)
        flattened = tuple(module_id for group in normalised for module_id in group)
        counts = Counter(flattened)
        placed_ids = {item.module_id for item in geometry.placements}
        duplicates = sorted(module_id for module_id, count in counts.items() if count > 1)
        omitted = sorted(placed_ids - set(flattened))
        unknown = sorted(set(flattened) - placed_ids)
        if duplicates or omitted or unknown:
            raise ValueError(
                "explicit module groups must be a complete one-to-one partition; "
                f"duplicates={duplicates}, omitted={omitted}, unknown={unknown}"
            )
        if normalised != canonical_groups:
            raise ValueError(
                "Build 025B currently authorises placement-ordinal membership only"
            )

    validation = validate_table_string_assignment(geometry, receipt)
    if not validation.valid:
        codes = ", ".join(issue.code for issue in validation.issues)
        raise ValueError(f"canonical string assignment failed independent validation: {codes}")
    return receipt


def electrical_module_order(
    physical_module_ids: Sequence[str],
    strategy: WiringStrategy | str,
) -> tuple[str, ...]:
    module_ids = tuple(physical_module_ids)
    if not module_ids:
        raise ValueError("at least one module is required")
    try:
        selected = WiringStrategy(strategy)
    except ValueError as exc:
        raise ValueError(f"unsupported wiring strategy: {strategy!r}") from exc
    if selected is WiringStrategy.SEQUENTIAL:
        return module_ids
    return module_ids[0::2] + tuple(reversed(module_ids[1::2]))


def _node(
    node_id: str,
    kind: NodeKind,
    string_id: str,
    module_id: str | None = None,
) -> TopologyNode:
    return TopologyNode(
        node_id=node_id,
        kind=kind,
        string_id=string_id,
        module_id=module_id,
    )


def _build_string_topology(
    assignment: StringAssignment,
    strategy: WiringStrategy,
) -> StringTopology:
    string_id = assignment.string_id
    physical_ids = assignment.ordered_module_ids
    electrical_ids = electrical_module_order(physical_ids, strategy)
    nodes: list[TopologyNode] = []
    edges: list[TopologyEdge] = []

    for module_id in physical_ids:
        negative_node_id = f"{module_id}:N"
        positive_node_id = f"{module_id}:P"
        nodes.extend(
            (
                _node(negative_node_id, NodeKind.MODULE_NEGATIVE_TERMINAL, string_id, module_id),
                _node(positive_node_id, NodeKind.MODULE_POSITIVE_TERMINAL, string_id, module_id),
            )
        )
        edges.append(
            TopologyEdge(
                edge_id=f"{module_id}:INTERNAL",
                kind=EdgeKind.MODULE_INTERNAL,
                from_node_id=negative_node_id,
                to_node_id=positive_node_id,
                string_id=string_id,
                module_id=module_id,
            )
        )

    free_negative = assignment.negative_free_terminal.terminal_id
    free_positive = assignment.positive_free_terminal.terminal_id
    nodes.extend(
        (
            _node(free_negative, NodeKind.STRING_NEGATIVE_FREE_END, string_id),
            _node(free_positive, NodeKind.STRING_POSITIVE_FREE_END, string_id),
        )
    )
    first_module = electrical_ids[0]
    last_module = electrical_ids[-1]
    edges.extend(
        (
            TopologyEdge(
                edge_id=f"{string_id}:BOUNDARY:N",
                kind=EdgeKind.BOUNDARY_LINK,
                from_node_id=free_negative,
                to_node_id=f"{first_module}:N",
                string_id=string_id,
            ),
            TopologyEdge(
                edge_id=f"{string_id}:BOUNDARY:P",
                kind=EdgeKind.BOUNDARY_LINK,
                from_node_id=f"{last_module}:P",
                to_node_id=free_positive,
                string_id=string_id,
            ),
        )
    )

    for ordinal, (left_module, right_module) in enumerate(
        zip(electrical_ids, electrical_ids[1:]),
        start=1,
    ):
        connector_a = f"{string_id}:CONN:{ordinal:03d}:A"
        connector_b = f"{string_id}:CONN:{ordinal:03d}:B"
        nodes.extend(
            (
                _node(connector_a, NodeKind.CONNECTOR, string_id),
                _node(connector_b, NodeKind.CONNECTOR, string_id),
            )
        )
        edges.extend(
            (
                TopologyEdge(
                    edge_id=f"{string_id}:LINK:{ordinal:03d}:LEAD:A",
                    kind=EdgeKind.FACTORY_LEAD,
                    from_node_id=f"{left_module}:P",
                    to_node_id=connector_a,
                    string_id=string_id,
                    module_id=left_module,
                    connection_ordinal=ordinal,
                ),
                TopologyEdge(
                    edge_id=f"{string_id}:LINK:{ordinal:03d}:MATE",
                    kind=EdgeKind.CONNECTOR_MATE,
                    from_node_id=connector_a,
                    to_node_id=connector_b,
                    string_id=string_id,
                    connection_ordinal=ordinal,
                ),
                TopologyEdge(
                    edge_id=f"{string_id}:LINK:{ordinal:03d}:LEAD:B",
                    kind=EdgeKind.FACTORY_LEAD,
                    from_node_id=connector_b,
                    to_node_id=f"{right_module}:N",
                    string_id=string_id,
                    module_id=right_module,
                    connection_ordinal=ordinal,
                ),
            )
        )

    result = StringTopology(
        string_id=string_id,
        strategy=strategy,
        physical_module_ids=physical_ids,
        electrical_module_ids=electrical_ids,
        free_negative_node_id=free_negative,
        free_positive_node_id=free_positive,
        nodes=tuple(nodes),
        edges=tuple(edges),
    )
    _validate_string_topology(result)
    return result


def _validate_string_topology(topology: StringTopology) -> None:
    if set(topology.physical_module_ids) != set(topology.electrical_module_ids):
        raise ValueError(f"string {topology.string_id!r} omits or invents modules")
    if len(topology.electrical_module_ids) != len(set(topology.electrical_module_ids)):
        raise ValueError(f"string {topology.string_id!r} repeats a module")
    node_ids = [node.node_id for node in topology.nodes]
    edge_ids = [edge.edge_id for edge in topology.edges]
    if len(node_ids) != len(set(node_ids)):
        raise ValueError(f"string {topology.string_id!r} has duplicate node identifiers")
    if len(edge_ids) != len(set(edge_ids)):
        raise ValueError(f"string {topology.string_id!r} has duplicate edge identifiers")
    node_set = set(node_ids)
    for edge in topology.edges:
        if edge.from_node_id not in node_set or edge.to_node_id not in node_set:
            raise ValueError(f"edge {edge.edge_id!r} references a missing node")
    if sum(node.kind is NodeKind.STRING_NEGATIVE_FREE_END for node in topology.nodes) != 1:
        raise ValueError("every string must have exactly one free negative end")
    if sum(node.kind is NodeKind.STRING_POSITIVE_FREE_END for node in topology.nodes) != 1:
        raise ValueError("every string must have exactly one free positive end")
    if sum(edge.kind is EdgeKind.MODULE_INTERNAL for edge in topology.edges) != len(
        topology.physical_module_ids
    ):
        raise ValueError("every module must have exactly one internal topology edge")
    if sum(edge.kind is EdgeKind.CONNECTOR_MATE for edge in topology.edges) != max(
        0, len(topology.physical_module_ids) - 1
    ):
        raise ValueError("connector topology is incomplete")


def topology_payload(receipt: TableTopologyReceipt) -> dict[str, object]:
    return {
        "schema_version": receipt.schema_version,
        "table_id": receipt.table_id,
        "assignment_hash": receipt.assignment_hash,
        "strategy": str(receipt.strategy),
        "node_count": receipt.node_count,
        "edge_count": receipt.edge_count,
        "topology_hash": receipt.topology_hash,
        "strings": [
            {
                "string_id": string.string_id,
                "strategy": str(string.strategy),
                "physical_module_ids": list(string.physical_module_ids),
                "electrical_module_ids": list(string.electrical_module_ids),
                "free_negative_node_id": string.free_negative_node_id,
                "free_positive_node_id": string.free_positive_node_id,
                "nodes": [
                    {
                        "node_id": node.node_id,
                        "kind": str(node.kind),
                        "string_id": node.string_id,
                        "module_id": node.module_id,
                        "equipment_id": node.equipment_id,
                    }
                    for node in string.nodes
                ],
                "edges": [
                    {
                        "edge_id": edge.edge_id,
                        "kind": str(edge.kind),
                        "from_node_id": edge.from_node_id,
                        "to_node_id": edge.to_node_id,
                        "string_id": edge.string_id,
                        "module_id": edge.module_id,
                        "connection_ordinal": edge.connection_ordinal,
                    }
                    for edge in string.edges
                ],
            }
            for string in receipt.strings
        ],
    }


def build_table_topology(
    allocation: StringAllocationReceipt,
    strategy: WiringStrategy | str,
) -> TableTopologyReceipt:
    selected = WiringStrategy(strategy)
    strings = tuple(_build_string_topology(assignment, selected) for assignment in allocation.strings)
    all_nodes = [node.node_id for string in strings for node in string.nodes]
    all_edges = [edge.edge_id for string in strings for edge in string.edges]
    if len(all_nodes) != len(set(all_nodes)):
        raise ValueError("topology node identifiers must be globally unique within a table")
    if len(all_edges) != len(set(all_edges)):
        raise ValueError("topology edge identifiers must be globally unique within a table")

    basis = {
        "schema_version": TOPOLOGY_SCHEMA_VERSION,
        "table_id": allocation.table_id,
        "assignment_hash": allocation.assignment_hash,
        "strategy": str(selected),
        "strings": [
            {
                "string_id": item.string_id,
                "physical_module_ids": list(item.physical_module_ids),
                "electrical_module_ids": list(item.electrical_module_ids),
                "free_negative_node_id": item.free_negative_node_id,
                "free_positive_node_id": item.free_positive_node_id,
                "nodes": [[node.node_id, str(node.kind), node.module_id] for node in item.nodes],
                "edges": [
                    [
                        edge.edge_id,
                        str(edge.kind),
                        edge.from_node_id,
                        edge.to_node_id,
                        edge.module_id,
                        edge.connection_ordinal,
                    ]
                    for edge in item.edges
                ],
            }
            for item in strings
        ],
    }
    return TableTopologyReceipt(
        table_id=allocation.table_id,
        assignment_hash=allocation.assignment_hash,
        strategy=selected,
        strings=strings,
        node_count=len(all_nodes),
        edge_count=len(all_edges),
        topology_hash=_hash_payload(basis),
    )


def uniform_equipment_profile(
    *,
    profile_id: str = "GENERIC-12-MPPT-24-INPUT",
    inverter_id: str = "INV-001",
    mppt_count: int = 12,
    inputs_per_mppt: int = 2,
    input_pitch_m: float = 0.16,
    input_bank_offset_u_m: float = 0.0,
    isolated_inputs: bool = True,
    limits: Build025Limits = DEFAULT_BUILD_025_LIMITS,
) -> EquipmentProfile:
    if mppt_count <= 0 or inputs_per_mppt <= 0:
        raise ValueError("mppt_count and inputs_per_mppt must be positive")
    if mppt_count > limits.maximum_mppts_per_inverter:
        raise ValueError("MPPT count exceeds Build 025 application limit")
    physical_count = mppt_count * inputs_per_mppt
    if physical_count > limits.maximum_physical_inputs_per_inverter:
        raise ValueError("physical input count exceeds Build 025 application limit")
    if not math.isfinite(input_pitch_m) or input_pitch_m <= 0:
        raise ValueError("input_pitch_m must be finite and positive")
    if not math.isfinite(input_bank_offset_u_m):
        raise ValueError("input_bank_offset_u_m must be finite")

    mppt_ids = tuple(f"MPPT-{index + 1:02d}" for index in range(mppt_count))
    inputs: list[PhysicalInputSpec] = []
    centred_origin = -((physical_count - 1) * input_pitch_m) / 2.0
    global_index = 0
    for mppt_id in mppt_ids:
        parallel_node_id = None if isolated_inputs else f"{inverter_id}:{mppt_id}:PARALLEL"
        for local_index in range(inputs_per_mppt):
            global_index += 1
            inputs.append(
                PhysicalInputSpec(
                    input_id=f"{inverter_id}:{mppt_id}:INPUT-{local_index + 1:02d}",
                    mppt_id=mppt_id,
                    offset_u_m=input_bank_offset_u_m,
                    offset_v_m=centred_origin + (global_index - 1) * input_pitch_m,
                    maximum_strings=1,
                    isolated=isolated_inputs,
                    parallel_node_id=parallel_node_id,
                )
            )
    return EquipmentProfile(
        profile_id=profile_id,
        inverter_id=inverter_id,
        mppt_ids=mppt_ids,
        physical_inputs=tuple(inputs),
        dc_bus_node_id=f"{inverter_id}:DC-BUS",
    )


def equipment_profile_payload(profile: EquipmentProfile) -> dict[str, object]:
    return {
        "schema_version": profile.schema_version,
        "profile_id": profile.profile_id,
        "inverter_id": profile.inverter_id,
        "mppt_ids": list(profile.mppt_ids),
        "dc_bus_node_id": profile.dc_bus_node_id,
        "physical_inputs": [
            {
                "input_id": item.input_id,
                "mppt_id": item.mppt_id,
                "offset_u_m": item.offset_u_m,
                "offset_v_m": item.offset_v_m,
                "maximum_strings": item.maximum_strings,
                "isolated": item.isolated,
                "parallel_node_id": item.parallel_node_id,
                "protective_device_node_id": item.protective_device_node_id,
            }
            for item in profile.physical_inputs
        ],
    }


def input_allocation_payload(receipt: InputAllocationReceipt) -> dict[str, object]:
    return {
        "schema_version": receipt.schema_version,
        "table_id": receipt.table_id,
        "assignment_hash": receipt.assignment_hash,
        "equipment_profile_id": receipt.equipment_profile_id,
        "inverter_id": receipt.inverter_id,
        "allocation_hash": receipt.allocation_hash,
        "unused_input_ids": list(receipt.unused_input_ids),
        "unused_mppt_ids": list(receipt.unused_mppt_ids),
        "assignments": [
            {"string_id": item.string_id, "input_id": item.input_id, "mppt_id": item.mppt_id}
            for item in receipt.assignments
        ],
    }


def allocate_physical_inputs(
    allocation: StringAllocationReceipt,
    profile: EquipmentProfile,
    *,
    explicit_input_by_string: Mapping[str, str] | None = None,
) -> InputAllocationReceipt:
    string_ids = tuple(item.string_id for item in allocation.strings)
    input_by_id = {item.input_id: item for item in profile.physical_inputs}
    assignments: list[InputAssignment] = []

    if explicit_input_by_string is None:
        available_slots: list[PhysicalInputSpec] = []
        for item in profile.physical_inputs:
            available_slots.extend([item] * item.maximum_strings)
        if len(string_ids) > len(available_slots):
            raise ValueError("equipment profile does not have enough physical-input capacity")
        selected_pairs = tuple(zip(string_ids, available_slots))
    else:
        supplied_strings = set(explicit_input_by_string)
        unknown_strings = sorted(supplied_strings - set(string_ids))
        omitted_strings = sorted(set(string_ids) - supplied_strings)
        unknown_inputs = sorted(set(explicit_input_by_string.values()) - set(input_by_id))
        if unknown_strings or omitted_strings or unknown_inputs:
            raise ValueError(
                "explicit input allocation must cover every known string and input; "
                f"unknown_strings={unknown_strings}, omitted_strings={omitted_strings}, "
                f"unknown_inputs={unknown_inputs}"
            )
        selected_pairs = tuple(
            (string_id, input_by_id[explicit_input_by_string[string_id]]) for string_id in string_ids
        )

    use_count: Counter[str] = Counter()
    for string_id, physical_input in selected_pairs:
        use_count[physical_input.input_id] += 1
        if use_count[physical_input.input_id] > physical_input.maximum_strings:
            raise ValueError(
                f"physical input {physical_input.input_id!r} exceeds its string capacity"
            )
        assignments.append(
            InputAssignment(
                string_id=string_id,
                input_id=physical_input.input_id,
                mppt_id=physical_input.mppt_id,
            )
        )

    assigned_inputs = {item.input_id for item in assignments}
    assigned_mppts = {item.mppt_id for item in assignments}
    unused_inputs = tuple(
        item.input_id for item in profile.physical_inputs if item.input_id not in assigned_inputs
    )
    unused_mppts = tuple(mppt_id for mppt_id in profile.mppt_ids if mppt_id not in assigned_mppts)
    basis = {
        "schema_version": INPUT_ALLOCATION_SCHEMA_VERSION,
        "table_id": allocation.table_id,
        "assignment_hash": allocation.assignment_hash,
        "equipment_profile": equipment_profile_payload(profile),
        "assignments": [[item.string_id, item.input_id, item.mppt_id] for item in assignments],
    }
    return InputAllocationReceipt(
        table_id=allocation.table_id,
        assignment_hash=allocation.assignment_hash,
        equipment_profile_id=profile.profile_id,
        inverter_id=profile.inverter_id,
        assignments=tuple(assignments),
        unused_input_ids=unused_inputs,
        unused_mppt_ids=unused_mppts,
        allocation_hash=_hash_payload(basis),
    )


def input_spec_by_string(
    receipt: InputAllocationReceipt,
    profile: EquipmentProfile,
) -> dict[str, PhysicalInputSpec]:
    if receipt.equipment_profile_id != profile.profile_id:
        raise ValueError("input allocation and equipment profile do not match")
    input_by_id = {item.input_id: item for item in profile.physical_inputs}
    resolved: dict[str, PhysicalInputSpec] = {}
    for assignment in receipt.assignments:
        item = input_by_id.get(assignment.input_id)
        if item is None:
            raise ValueError(f"allocation references missing physical input {assignment.input_id!r}")
        if item.mppt_id != assignment.mppt_id:
            raise ValueError("allocation MPPT label does not match the physical input profile")
        resolved[assignment.string_id] = item
    return resolved


__all__ = [
    "DEFAULT_BUILD_025_LIMITS",
    "EQUIPMENT_PROFILE_SCHEMA_VERSION",
    "INPUT_ALLOCATION_SCHEMA_VERSION",
    "STRING_ALLOCATION_SCHEMA_VERSION",
    "TOPOLOGY_SCHEMA_VERSION",
    "Build025Limits",
    "EdgeKind",
    "EquipmentProfile",
    "InputAllocationReceipt",
    "InputAssignment",
    "NodeKind",
    "PhysicalInputSpec",
    "StringAllocationReceipt",
    "StringAssignment",
    "StringTopology",
    "TableTopologyReceipt",
    "TopologyEdge",
    "TopologyNode",
    "WiringStrategy",
    "allocate_physical_inputs",
    "allocate_strings",
    "allocation_payload",
    "build_table_topology",
    "electrical_module_order",
    "equipment_profile_payload",
    "input_allocation_payload",
    "input_spec_by_string",
    "topology_payload",
    "uniform_equipment_profile",
]
