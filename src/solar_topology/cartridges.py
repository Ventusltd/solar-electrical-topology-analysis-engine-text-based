"""Topology cartridges that emit one shared ordered segment schema."""

from __future__ import annotations

from abc import ABC, abstractmethod
from collections import defaultdict
from dataclasses import asdict
import hashlib
import json
from typing import Iterable, Iterator, Sequence

from .segments import (
    FeasibilityResult,
    Point3D,
    SegmentBuilder,
    SegmentRow,
    StringDefinition,
    TopologyInputs,
    canonical_input_hash,
    fleet_string_definitions,
)


class TopologyCartridge(ABC):
    """A cartridge generates physical segments and no electrical totals."""

    name: str
    version: str

    @abstractmethod
    def feasibility(
        self,
        inputs: TopologyInputs,
    ) -> FeasibilityResult:
        """Return whether the physical topology passes its build screen."""

    @abstractmethod
    def module_order(
        self,
        module_count: int,
    ) -> tuple[int, ...]:
        """Return the electrical module order for one physical row."""

    @abstractmethod
    def build_segments(
        self,
        inputs: TopologyInputs,
        definition: StringDefinition,
    ) -> tuple[SegmentRow, ...]:
        """Build one complete positive-to-negative ordered segment chain."""

    def manifest(
        self,
        inputs: TopologyInputs,
        segments: Sequence[SegmentRow],
        source_commit: str = "unknown",
    ) -> dict:
        ordered = sorted(
            segments,
            key=lambda row: (
                row.inverter_id,
                row.string_id,
                row.segment_index,
            ),
        )
        warnings = sorted(
            {
                warning
                for row in ordered
                for warning in row.warnings.split(";")
                if warning
            }
        )
        cartridge_hash = hashlib.sha256(
            f"{self.name}:{self.version}".encode("utf-8")
        ).hexdigest()
        feasibility = self.feasibility(inputs)

        return {
            "schema_version": "topology_segments_v1",
            "cartridge_name": self.name,
            "cartridge_version": self.version,
            "method_version": "cartridge_segments_v1",
            "source_commit": source_commit,
            "input_hash": canonical_input_hash(inputs),
            "cartridge_hash": cartridge_hash,
            "segment_row_count": len(ordered),
            "distinct_string_count": len(
                {row.string_id for row in ordered}
            ),
            "first_segment_key": (
                ordered[0].segment_id if ordered else None
            ),
            "last_segment_key": (
                ordered[-1].segment_id if ordered else None
            ),
            "feasibility_status": feasibility.status,
            "saving_available": feasibility.feasible,
            "warning_count": len(warnings),
            "warnings": warnings,
            "data_law_result": "PENDING_PARQUET_AUDIT",
        }


def _point_at_module(
    definition: StringDefinition,
    inputs: TopologyInputs,
    module_index: int,
) -> Point3D:
    return Point3D(
        x=(
            definition.row_start_x_m
            + (module_index - 0.5) * inputs.module_pitch_m
        ),
        y=definition.row_y_m,
        z=0.0,
    )


def _midpoint(first: Point3D, second: Point3D) -> Point3D:
    return Point3D(
        x=(first.x + second.x) / 2,
        y=(first.y + second.y) / 2,
        z=(first.z + second.z) / 2,
    )


def _near_terminal(definition: StringDefinition) -> Point3D:
    return Point3D(
        definition.row_start_x_m,
        definition.row_y_m,
        0.0,
    )


def _far_terminal(definition: StringDefinition) -> Point3D:
    return Point3D(
        definition.row_end_x_m,
        definition.row_y_m,
        0.0,
    )


def _inverter_terminal(definition: StringDefinition) -> Point3D:
    return Point3D(
        definition.inverter_x_m,
        definition.inverter_y_m,
        0.0,
    )


def _build_module_chain(
    *,
    builder: SegmentBuilder,
    inputs: TopologyInputs,
    definition: StringDefinition,
    order: Sequence[int],
    first_terminal: Point3D,
    last_terminal: Point3D,
) -> None:
    centres = {
        module_index: _point_at_module(
            definition,
            inputs,
            module_index,
        )
        for module_index in order
    }

    previous_connector_node = "string:terminal:positive"
    previous_connector_point = first_terminal

    for position, module_index in enumerate(order, start=1):
        module_id = f"{definition.string_id}-M{module_index:02d}"
        centre = centres[module_index]

        if position == len(order):
            outgoing_point = last_terminal
        else:
            next_module = order[position]
            outgoing_point = _midpoint(
                centre,
                centres[next_module],
            )

        internal_node = f"{module_id}:internal"
        outgoing_node = (
            "string:terminal:negative"
            if position == len(order)
            else f"string:connector:{position}:a"
        )

        builder.append(
            segment_type="module_factory_positive_lead",
            polarity="series",
            from_node_id=previous_connector_node,
            to_node_id=internal_node,
            start=previous_connector_point,
            end=centre,
            conductor_length_m=inputs.positive_factory_lead_m,
            separation_mm=inputs.factory_pair_separation_mm,
            formation="spaced_pair",
            installation_class="under_module",
            conductor=inputs.factory_lead_conductor,
            temperature_c=inputs.factory_lead_temperature_c,
            effective_epsilon_r=inputs.effective_epsilon_r,
            module_id=module_id,
            provenance="oem_declared",
            source_reference="factory_lead_length_input",
            warnings=builder.feasibility.warnings,
        )
        builder.append(
            segment_type="module_factory_negative_lead",
            polarity="series",
            from_node_id=internal_node,
            to_node_id=outgoing_node,
            start=centre,
            end=outgoing_point,
            conductor_length_m=inputs.negative_factory_lead_m,
            separation_mm=inputs.factory_pair_separation_mm,
            formation="spaced_pair",
            installation_class="under_module",
            conductor=inputs.factory_lead_conductor,
            temperature_c=inputs.factory_lead_temperature_c,
            effective_epsilon_r=inputs.effective_epsilon_r,
            module_id=module_id,
            provenance="oem_declared",
            source_reference="factory_lead_length_input",
            warnings=builder.feasibility.warnings,
        )

        if position < len(order):
            next_connector_node = (
                f"string:connector:{position}:b"
            )
            builder.append(
                segment_type="module_interconnect",
                polarity="series",
                from_node_id=outgoing_node,
                to_node_id=next_connector_node,
                start=outgoing_point,
                end=outgoing_point,
                conductor_length_m=0.0,
                separation_mm=inputs.factory_pair_separation_mm,
                formation="touching_pair",
                installation_class="under_module",
                conductor=inputs.factory_lead_conductor,
                temperature_c=inputs.factory_lead_temperature_c,
                effective_epsilon_r=inputs.effective_epsilon_r,
                connector_count=2,
                provenance="assumed",
                source_reference="module_connector_contact_model",
                warnings=builder.feasibility.warnings,
            )
            previous_connector_node = next_connector_node
            previous_connector_point = outgoing_point


def _append_positive_home_run(
    builder: SegmentBuilder,
    inputs: TopologyInputs,
    definition: StringDefinition,
) -> None:
    builder.append(
        segment_type="external_positive_home_run",
        polarity="positive",
        from_node_id="inverter:positive",
        to_node_id="string:terminal:positive",
        start=_inverter_terminal(definition),
        end=_near_terminal(definition),
        conductor_length_m=definition.near_route_m,
        separation_mm=inputs.external_pair_separation_mm,
        formation="spaced_pair",
        installation_class="open_air",
        conductor=inputs.external_conductor,
        temperature_c=inputs.external_temperature_c,
        effective_epsilon_r=inputs.effective_epsilon_r,
        connector_count=2,
        provenance="assumed",
        source_reference="geometry_derived_external_route",
        warnings=builder.feasibility.warnings,
    )


def _append_negative_home_run(
    builder: SegmentBuilder,
    inputs: TopologyInputs,
    definition: StringDefinition,
    from_node_id: str,
    start: Point3D,
) -> None:
    builder.append(
        segment_type="external_negative_home_run",
        polarity="negative",
        from_node_id=from_node_id,
        to_node_id="inverter:negative",
        start=start,
        end=_inverter_terminal(definition),
        conductor_length_m=definition.near_route_m,
        separation_mm=inputs.external_pair_separation_mm,
        formation="spaced_pair",
        installation_class="open_air",
        conductor=inputs.external_conductor,
        temperature_c=inputs.external_temperature_c,
        effective_epsilon_r=inputs.effective_epsilon_r,
        connector_count=2,
        provenance="assumed",
        source_reference="geometry_derived_external_route",
        warnings=builder.feasibility.warnings,
    )


class SequentialCartridge(TopologyCartridge):
    name = "sequential"
    version = "1.0.0"

    def feasibility(
        self,
        inputs: TopologyInputs,
    ) -> FeasibilityResult:
        inputs.validate()
        return FeasibilityResult(
            status="FEASIBLE_BASE_TOPOLOGY",
            feasible=True,
            required_reach_m=0.0,
            available_reach_m=(
                inputs.positive_factory_lead_m
                + inputs.negative_factory_lead_m
            ),
            margin_m=0.0,
            extension_required_m=0.0,
            basis="SEQUENTIAL_BASELINE",
        )

    def module_order(
        self,
        module_count: int,
    ) -> tuple[int, ...]:
        if module_count < 1:
            raise ValueError("module_count must be positive")
        return tuple(range(1, module_count + 1))

    def build_segments(
        self,
        inputs: TopologyInputs,
        definition: StringDefinition,
    ) -> tuple[SegmentRow, ...]:
        feasibility = self.feasibility(inputs)
        builder = SegmentBuilder(
            run_id=canonical_input_hash(inputs),
            topology=self.name,
            cartridge_version=self.version,
            definition=definition,
            feasibility=feasibility,
        )
        near = _near_terminal(definition)
        far = _far_terminal(definition)

        _append_positive_home_run(builder, inputs, definition)
        _build_module_chain(
            builder=builder,
            inputs=inputs,
            definition=definition,
            order=self.module_order(inputs.modules_per_string),
            first_terminal=near,
            last_terminal=far,
        )
        builder.append(
            segment_type="external_sequential_row_return",
            polarity="negative",
            from_node_id="string:terminal:negative",
            to_node_id="string:terminal:negative:near",
            start=far,
            end=near,
            conductor_length_m=inputs.row_span_m,
            separation_mm=inputs.sequential_return_separation_mm,
            formation="single_pole",
            installation_class="under_module",
            conductor=inputs.external_conductor,
            temperature_c=inputs.external_temperature_c,
            effective_epsilon_r=inputs.effective_epsilon_r,
            provenance="assumed",
            source_reference="sequential_far_end_return",
        )
        _append_negative_home_run(
            builder,
            inputs,
            definition,
            "string:terminal:negative:near",
            near,
        )
        return tuple(builder.rows)


class LeapfrogCartridge(TopologyCartridge):
    name = "leapfrog"
    version = "1.0.0"

    def feasibility(
        self,
        inputs: TopologyInputs,
    ) -> FeasibilityResult:
        inputs.validate()
        measured = inputs.measured_leapfrog_span_m
        required = (
            measured
            if measured is not None and measured > 0
            else 2 * inputs.module_pitch_m
        )
        available = (
            inputs.positive_factory_lead_m
            + inputs.negative_factory_lead_m
        )
        margin = available - required
        feasible = margin >= 0
        warning = (
            ()
            if feasible
            else ("LEAPFROG_LENGTH_SCREEN_FAILED",)
        )
        return FeasibilityResult(
            status=(
                "FEASIBLE_LENGTH_SCREEN"
                if feasible
                else "INFEASIBLE_LENGTH_SCREEN"
            ),
            feasible=feasible,
            required_reach_m=required,
            available_reach_m=available,
            margin_m=margin,
            extension_required_m=max(0.0, -margin),
            basis=(
                "MEASURED_ROUTED_SPAN"
                if measured is not None and measured > 0
                else "TWO_MODULE_PITCH_SCREEN"
            ),
            warnings=warning,
        )

    def module_order(
        self,
        module_count: int,
    ) -> tuple[int, ...]:
        if module_count < 1:
            raise ValueError("module_count must be positive")
        odds = tuple(range(1, module_count + 1, 2))
        evens = tuple(range(
            module_count if module_count % 2 == 0 else module_count - 1,
            1,
            -2,
        ))
        return odds + evens

    def build_segments(
        self,
        inputs: TopologyInputs,
        definition: StringDefinition,
    ) -> tuple[SegmentRow, ...]:
        feasibility = self.feasibility(inputs)
        builder = SegmentBuilder(
            run_id=canonical_input_hash(inputs),
            topology=self.name,
            cartridge_version=self.version,
            definition=definition,
            feasibility=feasibility,
        )
        near = _near_terminal(definition)

        _append_positive_home_run(builder, inputs, definition)
        _build_module_chain(
            builder=builder,
            inputs=inputs,
            definition=definition,
            order=self.module_order(inputs.modules_per_string),
            first_terminal=near,
            last_terminal=near,
        )
        _append_negative_home_run(
            builder,
            inputs,
            definition,
            "string:terminal:negative",
            near,
        )
        return tuple(builder.rows)


INITIAL_CARTRIDGES: tuple[TopologyCartridge, ...] = (
    SequentialCartridge(),
    LeapfrogCartridge(),
)


def build_fleet_segments(
    inputs: TopologyInputs,
    cartridges: Iterable[TopologyCartridge] = INITIAL_CARTRIDGES,
) -> Iterator[SegmentRow]:
    definitions = tuple(fleet_string_definitions(inputs))
    for cartridge in cartridges:
        for definition in definitions:
            yield from cartridge.build_segments(inputs, definition)


def validate_segment_chains(
    segments: Iterable[SegmentRow],
) -> None:
    groups: dict[tuple[str, str], list[SegmentRow]] = defaultdict(list)
    keys: set[tuple[str, str, int]] = set()

    for row in segments:
        row.validate()
        key = (row.topology, row.string_id, row.segment_index)
        if key in keys:
            raise ValueError(f"Duplicate segment key: {key}")
        keys.add(key)
        groups[(row.topology, row.string_id)].append(row)

    for group_key, rows in groups.items():
        ordered = sorted(rows, key=lambda row: row.segment_index)
        expected = list(range(1, len(ordered) + 1))
        actual = [row.segment_index for row in ordered]
        if actual != expected:
            raise ValueError(
                f"Non-contiguous segment indices for {group_key}"
            )
        for first, second in zip(ordered, ordered[1:]):
            if first.to_node_id != second.from_node_id:
                raise ValueError(
                    "Discontinuous node chain for "
                    f"{group_key}: {first.segment_id} -> "
                    f"{second.segment_id}"
                )


def validate_cross_cartridge_invariants(
    segments: Iterable[SegmentRow],
) -> None:
    rows = tuple(segments)
    validate_segment_chains(rows)
    by_string: dict[str, dict[str, list[SegmentRow]]] = defaultdict(
        lambda: defaultdict(list)
    )

    for row in rows:
        by_string[row.string_id][row.topology].append(row)

    for string_id, topologies in by_string.items():
        if set(topologies) != {"sequential", "leapfrog"}:
            raise ValueError(
                f"Both initial cartridges are required for {string_id}"
            )

        def factory_total(items: Sequence[SegmentRow]) -> float:
            return sum(
                row.conductor_length_m
                for row in items
                if row.segment_type in {
                    "module_factory_positive_lead",
                    "module_factory_negative_lead",
                    "extension_lead",
                }
            )

        def ordinary_connectors(items: Sequence[SegmentRow]) -> int:
            return sum(
                row.connector_count
                for row in items
                if row.segment_type != "extension_lead"
            )

        sequential = topologies["sequential"]
        leapfrog = topologies["leapfrog"]
        if not math_isclose(
            factory_total(sequential),
            factory_total(leapfrog),
        ):
            raise ValueError(
                f"Factory-lead conductor differs for {string_id}"
            )
        if ordinary_connectors(sequential) != ordinary_connectors(
            leapfrog
        ):
            raise ValueError(
                f"Connector count differs for {string_id}"
            )


def math_isclose(
    first: float,
    second: float,
    tolerance: float = 1e-12,
) -> bool:
    return abs(first - second) <= tolerance


def segments_as_json(
    segments: Iterable[SegmentRow],
) -> str:
    payload = [
        row.as_dict()
        for row in sorted(
            segments,
            key=lambda item: (
                item.topology,
                item.band,
                item.inverter_id,
                item.string_id,
                item.segment_index,
            ),
        )
    ]
    return json.dumps(
        payload,
        sort_keys=True,
        separators=(",", ":"),
    )
