"""Installed public API for the Build 025 whole-table array authority.

Build 025.5 places every implementation module inside this package. The original
repository-root module names remain compatibility imports only. Internal aliases
are installed in dependency order so the unchanged, already validated Build 025
module bodies retain object identity and deterministic receipt behaviour while
all production logic is owned by the installed package.
"""

from __future__ import annotations

from importlib import import_module
import sys
from types import ModuleType


def _authoritative_module(name: str) -> ModuleType:
    module = import_module(f".{name}", __name__)
    # Replace, rather than setdefault, so importing an old root compatibility
    # module first cannot leave a partially initialised module in the graph.
    sys.modules[name] = module
    return module


# Dependency order is part of the migration contract.
_geometry_authority = _authoritative_module("geometry_authority")
_table_string_assignment = _authoritative_module("table_string_assignment")
_table_string_hashing = _authoritative_module("table_string_hashing")
_table_string_validation = _authoritative_module("table_string_validation")
_array_topology = _authoritative_module("array_topology")
_array_route_types = _authoritative_module("array_route_types")
_array_route_geometry = _authoritative_module("array_route_geometry")
_array_routing = _authoritative_module("array_routing")
_array_engine = _authoritative_module("array_engine")

from .array_engine import (  # noqa: E402
    BUILD_025_SCHEMA_VERSION,
    STRATEGY_COMPARISON_SCHEMA_VERSION,
    Build025Receipt,
    MetricDelta,
    StrategyComparisonReceipt,
    build025_payload,
    build_complete_table,
    compare_reference_24_by_30,
    compare_wiring_strategies,
    reference_24_by_30_build,
    strategy_comparison_payload,
)
from .array_route_types import (  # noqa: E402
    ConductorRoute,
    ConductorScope,
    InstalledLengthPolicy,
    InstalledLengthReceipt,
    InstallationMethod,
    InverterPlacement,
    ModuleTerminalLayout,
    RouteClass,
    RoutePolarity,
    RouteSegment,
    RoutingConfig,
    StringRouteMetrics,
    StringRoutingReceipt,
    TableRouteMetrics,
    TableRoutingReceipt,
)
from .array_topology import (  # noqa: E402
    DEFAULT_BUILD_025_LIMITS,
    Build025Limits,
    EquipmentProfile,
    InputAllocationReceipt,
    NodeKind,
    StringAllocationReceipt,
    TableTopologyReceipt,
    WiringStrategy,
    allocate_physical_inputs,
    allocate_strings,
    attach_input_topology,
    build_table_topology,
    uniform_equipment_profile,
)
from .geometry_authority import (  # noqa: E402
    ModuleDimensions,
    ModulePlacement,
    Orientation,
    Point2D,
    TableBounds,
    TableGeometryReceipt,
    TableLayoutRequest,
    generate_table_geometry,
    receipt_as_dict,
    reference_24_by_30_table,
)


ARRAY_AUTHORITY_STATUS = "canonical_candidate"
ARRAY_AUTHORITY_MIGRATION_STAGE = "build-025.5-package-authority"
COMPATIBILITY_MODULES = (
    "geometry_authority",
    "table_string_assignment",
    "table_string_hashing",
    "table_string_validation",
    "array_topology",
    "array_route_types",
    "array_route_geometry",
    "array_routing",
    "array_engine",
)


__all__ = [
    "ARRAY_AUTHORITY_MIGRATION_STAGE",
    "ARRAY_AUTHORITY_STATUS",
    "BUILD_025_SCHEMA_VERSION",
    "COMPATIBILITY_MODULES",
    "STRATEGY_COMPARISON_SCHEMA_VERSION",
    "Build025Limits",
    "Build025Receipt",
    "ConductorRoute",
    "ConductorScope",
    "DEFAULT_BUILD_025_LIMITS",
    "EquipmentProfile",
    "InputAllocationReceipt",
    "InstalledLengthPolicy",
    "InstalledLengthReceipt",
    "InstallationMethod",
    "InverterPlacement",
    "MetricDelta",
    "ModuleDimensions",
    "ModulePlacement",
    "ModuleTerminalLayout",
    "NodeKind",
    "Orientation",
    "Point2D",
    "RouteClass",
    "RoutePolarity",
    "RouteSegment",
    "RoutingConfig",
    "StrategyComparisonReceipt",
    "StringAllocationReceipt",
    "StringRouteMetrics",
    "StringRoutingReceipt",
    "TableBounds",
    "TableGeometryReceipt",
    "TableLayoutRequest",
    "TableRouteMetrics",
    "TableRoutingReceipt",
    "TableTopologyReceipt",
    "WiringStrategy",
    "allocate_physical_inputs",
    "allocate_strings",
    "attach_input_topology",
    "build025_payload",
    "build_complete_table",
    "build_table_topology",
    "compare_reference_24_by_30",
    "compare_wiring_strategies",
    "generate_table_geometry",
    "receipt_as_dict",
    "reference_24_by_30_build",
    "reference_24_by_30_table",
    "strategy_comparison_payload",
    "uniform_equipment_profile",
]
