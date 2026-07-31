"""Immutable records for Build 025 route and length authority."""

from __future__ import annotations

from dataclasses import dataclass
from enum import StrEnum
from hashlib import sha256
import json
import math

from geometry_authority import Point2D
from array_topology import WiringStrategy


ROUTING_SCHEMA_VERSION = "globalgrid2050.solar-dc.table-routing.v2"
LENGTH_RECEIPT_SCHEMA_VERSION = "globalgrid2050.solar-dc.installed-length.v1"
ROUTING_METHOD_VERSION = "explicit-polyline-table-routing.v1"
LOOP_AREA_METHOD_VERSION = "closed-path-winding-area.v1"
SEPARATION_METHOD_VERSION = "segment-midpoint-nearest-route.v1"
EPSILON = 1e-9


class RoutePolarity(StrEnum):
    POSITIVE = "positive"
    NEGATIVE = "negative"
    SERIES = "series"


class RouteClass(StrEnum):
    MODULE_INTERCONNECT = "module_interconnect"
    STRING_EXIT = "string_exit"
    COLLECTION_RUN = "collection_run"
    INVERTER_ENTRY = "inverter_entry"
    INPUT_TAIL = "input_tail"


class InstallationMethod(StrEnum):
    EXPOSED_UNSHIELDED = "exposed_unshielded"
    BURIED = "buried"
    SCREENED = "screened"
    ARMOURED = "armoured"
    BONDED_METALLIC_CONTAINMENT = "bonded_metallic_containment"
    BONDED_SCREEN = "bonded_screen"


class ConductorScope(StrEnum):
    FACTORY_FITTED = "factory_fitted"
    FIELD_INSTALLED = "field_installed"


@dataclass(frozen=True, slots=True)
class LocalPoint2D:
    u_m: float
    v_m: float

    def __post_init__(self) -> None:
        if not math.isfinite(self.u_m) or not math.isfinite(self.v_m):
            raise ValueError("local coordinates must be finite")


@dataclass(frozen=True, slots=True)
class InverterPlacement:
    inverter_id: str
    position: Point2D

    def __post_init__(self) -> None:
        if not self.inverter_id.strip():
            raise ValueError("inverter_id must not be empty")


@dataclass(frozen=True, slots=True)
class ModuleTerminalLayout:
    """Replaceable local terminal coordinates on every module envelope.

    The default keeps the electrically distinct terminals at one unresolved
    junction-box reference coordinate. Manufacturer or field geometry can replace
    the offsets without changing topology or routing algorithms.
    """

    negative_offset_u_m: float = 0.0
    negative_offset_v_m: float = 0.0
    positive_offset_u_m: float = 0.0
    positive_offset_v_m: float = 0.0
    evidence_class: str = "generic_unresolved"
    source_reference: str = "build_025_junction_box_centre_reference"

    def __post_init__(self) -> None:
        values = (
            self.negative_offset_u_m,
            self.negative_offset_v_m,
            self.positive_offset_u_m,
            self.positive_offset_v_m,
        )
        if not all(math.isfinite(value) for value in values):
            raise ValueError("terminal offsets must be finite")
        if not self.evidence_class.strip() or not self.source_reference.strip():
            raise ValueError("terminal geometry requires visible evidence metadata")


@dataclass(frozen=True, slots=True)
class RoutingConfig:
    collection_offset_u_m: float = 0.50
    inverter_entry_offset_u_m: float = 0.50
    pole_separation_m: float = 0.05
    interconnect_lane_offset_m: float = 0.05
    sequential_row_return_offset_m: float = 0.50
    parallel_pairing_max_separation_m: float = 0.20
    home_run_installation_method: InstallationMethod = (
        InstallationMethod.EXPOSED_UNSHIELDED
    )
    interconnect_installation_method: InstallationMethod = (
        InstallationMethod.EXPOSED_UNSHIELDED
    )
    terminal_layout: ModuleTerminalLayout = ModuleTerminalLayout()

    def __post_init__(self) -> None:
        values = (
            ("collection_offset_u_m", self.collection_offset_u_m),
            ("inverter_entry_offset_u_m", self.inverter_entry_offset_u_m),
            ("pole_separation_m", self.pole_separation_m),
            ("interconnect_lane_offset_m", self.interconnect_lane_offset_m),
            ("sequential_row_return_offset_m", self.sequential_row_return_offset_m),
            (
                "parallel_pairing_max_separation_m",
                self.parallel_pairing_max_separation_m,
            ),
        )
        for name, value in values:
            if not math.isfinite(value) or value < 0:
                raise ValueError(f"{name} must be finite and non-negative")


@dataclass(frozen=True, slots=True)
class RouteSegment:
    segment_id: str
    string_id: str
    polarity: RoutePolarity
    start: Point2D
    end: Point2D
    route_class: RouteClass
    installation_method: InstallationMethod
    buried: bool
    screened: bool
    armoured: bool
    earthed_metallic_containment: bool
    bonded_screen: bool
    support_path_id: str
    geometric_length_m: float
    from_node_id: str
    to_node_id: str
    conductor_scope: ConductorScope

    def __post_init__(self) -> None:
        if not self.segment_id.strip() or not self.string_id.strip():
            raise ValueError("route segment identifiers must not be empty")
        if not self.support_path_id.strip():
            raise ValueError("support_path_id must not be empty")
        expected = math.dist(
            (self.start.x_m, self.start.y_m),
            (self.end.x_m, self.end.y_m),
        )
        if not math.isfinite(self.geometric_length_m) or self.geometric_length_m < 0:
            raise ValueError("geometric route length must be finite and non-negative")
        if not math.isclose(
            self.geometric_length_m,
            expected,
            rel_tol=0.0,
            abs_tol=1e-8,
        ):
            raise ValueError(
                f"segment {self.segment_id!r} stored length does not equal its vertices"
            )


@dataclass(frozen=True, slots=True)
class ConductorRoute:
    route_id: str
    string_id: str
    polarity: RoutePolarity
    conductor_scope: ConductorScope
    from_node_id: str
    to_node_id: str
    vertices: tuple[Point2D, ...]
    segments: tuple[RouteSegment, ...]
    geometric_length_m: float
    route_hash: str


@dataclass(frozen=True, slots=True)
class StringRouteMetrics:
    string_id: str
    positive_conductor_length_m: float
    negative_conductor_length_m: float
    series_interconnect_length_m: float
    total_circuit_conductor_length_m: float
    inverter_home_run_length_m: float
    maximum_pole_separation_m: float
    mean_pole_separation_m: float
    parallel_run_distance_m: float
    crossings: int
    signed_loop_area_m2: float
    absolute_enclosed_loop_area_m2: float
    separation_weight_m: float


@dataclass(frozen=True, slots=True)
class StringRoutingReceipt:
    string_id: str
    topology_hash: str
    allocation_hash: str
    inverter_id: str
    input_id: str
    mppt_id: str
    free_negative_point: Point2D
    free_positive_point: Point2D
    input_negative_point: Point2D
    input_positive_point: Point2D
    positive_route: ConductorRoute
    negative_route: ConductorRoute
    interconnect_routes: tuple[ConductorRoute, ...]
    circuit_loop_vertices: tuple[Point2D, ...]
    metrics: StringRouteMetrics
    routing_hash: str


@dataclass(frozen=True, slots=True)
class TableRouteMetrics:
    positive_conductor_length_m: float
    negative_conductor_length_m: float
    series_interconnect_length_m: float
    total_circuit_conductor_length_m: float
    inverter_home_run_length_m: float
    maximum_pole_separation_m: float
    mean_pole_separation_m: float
    parallel_run_distance_m: float
    crossings: int
    signed_loop_area_m2: float
    absolute_enclosed_loop_area_m2: float


@dataclass(frozen=True, slots=True)
class TableRoutingReceipt:
    table_id: str
    geometry_hash: str
    assignment_hash: str
    topology_hash: str
    input_allocation_hash: str
    strategy: WiringStrategy
    inverter: InverterPlacement
    routing_config: RoutingConfig
    strings: tuple[StringRoutingReceipt, ...]
    metrics: TableRouteMetrics
    routing_hash: str
    schema_version: str = ROUTING_SCHEMA_VERSION
    method_version: str = ROUTING_METHOD_VERSION


@dataclass(frozen=True, slots=True)
class InstalledLengthPolicy:
    connector_approach_m_per_route_end: float = 0.0
    harness_offset_m_per_route: float = 0.0
    bend_allowance_m_per_bend: float = 0.0
    support_offset_m_per_segment: float = 0.0
    service_loop_m_per_route: float = 0.0
    termination_allowance_m_per_route_end: float = 0.0
    construction_tolerance_fraction: float = 0.0
    procurement_spare_fraction: float = 0.0
    procurement_waste_fraction: float = 0.0
    drum_length_m: float | None = None

    def __post_init__(self) -> None:
        lengths = (
            self.connector_approach_m_per_route_end,
            self.harness_offset_m_per_route,
            self.bend_allowance_m_per_bend,
            self.support_offset_m_per_segment,
            self.service_loop_m_per_route,
            self.termination_allowance_m_per_route_end,
        )
        if not all(math.isfinite(value) and value >= 0 for value in lengths):
            raise ValueError("installed-length allowances must be finite and non-negative")
        fractions = (
            self.construction_tolerance_fraction,
            self.procurement_spare_fraction,
            self.procurement_waste_fraction,
        )
        if not all(math.isfinite(value) and 0 <= value < 1 for value in fractions):
            raise ValueError("length fractions must be finite and in [0, 1)")
        if self.drum_length_m is not None and (
            not math.isfinite(self.drum_length_m) or self.drum_length_m <= 0
        ):
            raise ValueError("drum_length_m must be finite and positive when supplied")


@dataclass(frozen=True, slots=True)
class RouteInstalledLength:
    route_id: str
    string_id: str
    polarity: RoutePolarity
    geometric_length_m: float
    connector_approach_m: float
    harness_offset_m: float
    bend_allowance_m: float
    support_offset_m: float
    service_loop_m: float
    termination_allowance_m: float
    pre_tolerance_installed_length_m: float
    construction_tolerance_m: float
    installed_length_m: float


@dataclass(frozen=True, slots=True)
class InstalledLengthReceipt:
    table_id: str
    routing_hash: str
    route_allowances: tuple[RouteInstalledLength, ...]
    field_geometric_length_m: float
    factory_fitted_geometric_length_m: float
    total_geometric_conductor_length_m: float
    installed_field_length_m: float
    procurement_spare_m: float
    procurement_waste_m: float
    procurement_pre_round_m: float
    drum_rounding_m: float
    procurement_length_m: float
    receipt_hash: str
    schema_version: str = LENGTH_RECEIPT_SCHEMA_VERSION


def canonical_float(value: float) -> float:
    rounded = round(value, 9)
    return 0.0 if rounded == -0.0 else rounded


def canonical_json(payload: object) -> str:
    return json.dumps(
        payload,
        sort_keys=True,
        separators=(",", ":"),
        ensure_ascii=True,
    )


def hash_payload(payload: object) -> str:
    digest = sha256(canonical_json(payload).encode("utf-8")).hexdigest()
    return f"sha256:{digest}"


def same_point(first: Point2D, second: Point2D) -> bool:
    return math.isclose(first.x_m, second.x_m, abs_tol=1e-9) and math.isclose(
        first.y_m,
        second.y_m,
        abs_tol=1e-9,
    )


def method_flags(
    method: InstallationMethod,
) -> tuple[bool, bool, bool, bool, bool]:
    if method is InstallationMethod.BURIED:
        return True, False, False, False, False
    if method is InstallationMethod.SCREENED:
        return False, True, False, False, False
    if method is InstallationMethod.ARMOURED:
        return False, False, True, False, False
    if method is InstallationMethod.BONDED_METALLIC_CONTAINMENT:
        return False, False, False, True, False
    if method is InstallationMethod.BONDED_SCREEN:
        return False, True, False, False, True
    return False, False, False, False, False
