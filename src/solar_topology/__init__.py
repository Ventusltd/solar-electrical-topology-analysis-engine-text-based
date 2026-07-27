"""Solar electrical topology physics, cartridges and fleet data core."""

from .cartridges import (
    INITIAL_CARTRIDGES,
    LeapfrogCartridge,
    SequentialCartridge,
    TopologyCartridge,
    build_fleet_segments,
    validate_cross_cartridge_invariants,
    validate_segment_chains,
)
from .formulas import (
    cold_string_voc,
    dc_resistance,
    stored_electric_energy,
    stored_magnetic_energy,
    two_wire_parameters,
)
from .parquet_store import build_deterministic_store, build_store
from .products import (
    ConductorSpec,
    EXTERNAL_STRING_6MM2,
    FACTORY_LEAD_4MM2,
)
from .segments import (
    FeasibilityResult,
    Point3D,
    SegmentRow,
    StringDefinition,
    TopologyInputs,
    archetype_strings,
    fleet_string_definitions,
    string_counts_per_inverter,
)
from .topology import (
    FormationConfig,
    GeometryConfig,
    Segment,
    StringTopology,
    build_export,
    build_site_model,
    build_string_segments,
    validate_no_user_route_lengths,
)


__all__ = [
    "INITIAL_CARTRIDGES",
    "LeapfrogCartridge",
    "SequentialCartridge",
    "TopologyCartridge",
    "build_fleet_segments",
    "validate_cross_cartridge_invariants",
    "validate_segment_chains",
    "cold_string_voc",
    "dc_resistance",
    "stored_electric_energy",
    "stored_magnetic_energy",
    "two_wire_parameters",
    "build_deterministic_store",
    "build_store",
    "ConductorSpec",
    "EXTERNAL_STRING_6MM2",
    "FACTORY_LEAD_4MM2",
    "FeasibilityResult",
    "Point3D",
    "SegmentRow",
    "StringDefinition",
    "TopologyInputs",
    "archetype_strings",
    "fleet_string_definitions",
    "string_counts_per_inverter",
    "FormationConfig",
    "GeometryConfig",
    "Segment",
    "StringTopology",
    "build_export",
    "build_site_model",
    "build_string_segments",
    "validate_no_user_route_lengths",
]
