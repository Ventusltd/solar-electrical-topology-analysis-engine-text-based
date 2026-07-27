"""Shared segment rows and deterministic fleet geometry definitions."""

from __future__ import annotations

from dataclasses import asdict, dataclass, field
import hashlib
import json
import math
from typing import Iterable, Iterator

from .products import (
    ConductorSpec,
    EXTERNAL_STRING_6MM2,
    FACTORY_LEAD_4MM2,
)


SCHEMA_VERSION = "topology_segments_v1"
ALLOWED_PROVENANCE = {
    "measured",
    "oem_declared",
    "assumed",
    "defaulted",
}


@dataclass(frozen=True)
class Point3D:
    x: float
    y: float
    z: float


@dataclass(frozen=True)
class FeasibilityResult:
    status: str
    feasible: bool
    required_reach_m: float
    available_reach_m: float
    margin_m: float
    extension_required_m: float
    basis: str
    warnings: tuple[str, ...] = ()


@dataclass(frozen=True)
class TopologyInputs:
    modules_per_string: int = 30
    module_width_m: float = 1.303
    module_gap_m: float = 0.020
    module_length_m: float = 2.384
    clamp_gap_m: float = 0.020
    tilt_deg: float = 10.0
    band_gap_m: float = 0.500
    east_bands: tuple[int, ...] = (5, 5, 2)
    west_bands: tuple[int, ...] = (5, 5, 2)
    inverter_distance_m: float = 10.0
    inverter_count: int = 795
    total_site_string_count: int = 18_918
    positive_factory_lead_m: float = 0.350
    negative_factory_lead_m: float = 0.280
    measured_leapfrog_span_m: float | None = None
    external_temperature_c: float = 70.0
    factory_lead_temperature_c: float = 75.0
    connector_contact_ohm: float = 0.00035
    external_pair_separation_mm: float = 40.0
    factory_pair_separation_mm: float = 8.0
    sequential_return_separation_mm: float = 500.0
    effective_epsilon_r: float = 2.3
    external_conductor: ConductorSpec = EXTERNAL_STRING_6MM2
    factory_lead_conductor: ConductorSpec = FACTORY_LEAD_4MM2

    @property
    def module_pitch_m(self) -> float:
        return self.module_width_m + self.module_gap_m

    @property
    def row_span_m(self) -> float:
        return (
            self.modules_per_string * self.module_width_m
            + (self.modules_per_string - 1) * self.module_gap_m
        )

    @property
    def rank_plan_pitch_m(self) -> float:
        slope_pitch = self.module_length_m + self.clamp_gap_m
        return slope_pitch * math.cos(math.radians(self.tilt_deg))

    @property
    def archetype_string_count(self) -> int:
        return sum(self.east_bands) + sum(self.west_bands)

    def validate(self) -> None:
        if self.modules_per_string < 1:
            raise ValueError("modules_per_string must be positive")
        if self.module_width_m <= 0 or self.module_length_m <= 0:
            raise ValueError("module dimensions must be positive")
        if self.module_gap_m < 0 or self.band_gap_m < 0:
            raise ValueError("module and band gaps cannot be negative")
        if self.inverter_distance_m < 0:
            raise ValueError("inverter_distance_m cannot be negative")
        if self.inverter_count < 1:
            raise ValueError("inverter_count must be positive")
        if self.total_site_string_count < 1:
            raise ValueError("total_site_string_count must be positive")
        if any(value < 1 for value in self.east_bands + self.west_bands):
            raise ValueError("band counts must be positive")
        if self.archetype_string_count < 1:
            raise ValueError("at least one string band is required")
        capacity = self.inverter_count * self.archetype_string_count
        if self.total_site_string_count > capacity:
            raise ValueError(
                "total_site_string_count exceeds archetype capacity"
            )
        if self.effective_epsilon_r <= 0:
            raise ValueError("effective_epsilon_r must be positive")
        if self.connector_contact_ohm < 0:
            raise ValueError("connector_contact_ohm cannot be negative")
        self.external_conductor.validate()
        self.factory_lead_conductor.validate()


@dataclass(frozen=True)
class StringDefinition:
    inverter_id: int
    mppt_id: int
    string_id: str
    face: str
    band: int
    rank: int
    row_start_x_m: float
    row_end_x_m: float
    row_y_m: float
    inverter_x_m: float
    inverter_y_m: float

    @property
    def near_route_m(self) -> float:
        return abs(self.row_start_x_m - self.inverter_x_m)


@dataclass(frozen=True)
class SegmentRow:
    run_id: str
    schema_version: str
    topology: str
    band: int
    cartridge_version: str
    inverter_id: int
    mppt_id: int
    string_id: str
    segment_index: int
    segment_id: str
    segment_type: str
    polarity: str
    from_node_id: str
    to_node_id: str
    module_id: str | None
    from_x: float
    from_y: float
    from_z: float
    to_x: float
    to_y: float
    to_z: float
    displacement_m: float
    conductor_length_m: float
    separation_mm: float
    formation: str
    installation_class: str
    conductor_product_id: str
    conductor_csa_mm2: float
    conductor_diameter_mm: float
    cable_od_mm: float
    r20_ohm_per_m: float
    temperature_c: float
    effective_epsilon_r: float
    loop_parameter_weight: float
    coil_turns: float | None
    coil_diameter_mm: float | None
    connector_count: int
    connector_resistance_ohm_each: float
    provenance: str
    source_reference: str
    user_override: bool
    feasibility_status: str
    saving_available: bool
    warnings: str = ""

    def validate(self) -> None:
        required_text = {
            "run_id": self.run_id,
            "schema_version": self.schema_version,
            "topology": self.topology,
            "cartridge_version": self.cartridge_version,
            "string_id": self.string_id,
            "segment_id": self.segment_id,
            "segment_type": self.segment_type,
            "polarity": self.polarity,
            "from_node_id": self.from_node_id,
            "to_node_id": self.to_node_id,
            "formation": self.formation,
            "installation_class": self.installation_class,
            "conductor_product_id": self.conductor_product_id,
            "provenance": self.provenance,
            "feasibility_status": self.feasibility_status,
        }
        empty = [key for key, value in required_text.items() if not value]
        if empty:
            raise ValueError(f"Missing required segment fields: {empty}")
        if self.segment_index < 1:
            raise ValueError("segment_index must begin at one")
        if self.band < 1 or self.inverter_id < 1 or self.mppt_id < 1:
            raise ValueError("band, inverter_id and mppt_id must be positive")
        if self.displacement_m < 0 or self.conductor_length_m < 0:
            raise ValueError("segment lengths cannot be negative")
        if not 0 <= self.loop_parameter_weight <= 1:
            raise ValueError("loop_parameter_weight must be between 0 and 1")
        if self.connector_count < 0:
            raise ValueError("connector_count cannot be negative")
        if self.connector_resistance_ohm_each < 0:
            raise ValueError(
                "connector_resistance_ohm_each cannot be negative"
            )
        if self.provenance not in ALLOWED_PROVENANCE:
            raise ValueError(f"Invalid provenance: {self.provenance}")
        if self.conductor_diameter_mm <= 0:
            raise ValueError("conductor_diameter_mm must be positive")
        if self.cable_od_mm < self.conductor_diameter_mm:
            raise ValueError("cable OD cannot be below conductor diameter")
        if self.r20_ohm_per_m <= 0:
            raise ValueError("r20_ohm_per_m must be positive")

    def as_dict(self) -> dict:
        self.validate()
        return asdict(self)


@dataclass(frozen=True)
class SegmentBuilder:
    run_id: str
    topology: str
    cartridge_version: str
    definition: StringDefinition
    feasibility: FeasibilityResult
    rows: list[SegmentRow] = field(default_factory=list)

    def append(
        self,
        *,
        segment_type: str,
        polarity: str,
        from_node_id: str,
        to_node_id: str,
        start: Point3D,
        end: Point3D,
        conductor_length_m: float,
        separation_mm: float,
        formation: str,
        installation_class: str,
        conductor: ConductorSpec,
        temperature_c: float,
        effective_epsilon_r: float,
        loop_parameter_weight: float = 0.0,
        connector_count: int = 0,
        connector_resistance_ohm_each: float = 0.0,
        module_id: str | None = None,
        coil_turns: float | None = None,
        coil_diameter_mm: float | None = None,
        provenance: str = "assumed",
        source_reference: str = "generic_model_input",
        user_override: bool = False,
        warnings: Iterable[str] = (),
    ) -> SegmentRow:
        index = len(self.rows) + 1
        displacement = math.dist(
            (start.x, start.y, start.z),
            (end.x, end.y, end.z),
        )
        segment_id = (
            f"{self.topology}:{self.definition.string_id}:"
            f"{index:04d}"
        )
        row = SegmentRow(
            run_id=self.run_id,
            schema_version=SCHEMA_VERSION,
            topology=self.topology,
            band=self.definition.band,
            cartridge_version=self.cartridge_version,
            inverter_id=self.definition.inverter_id,
            mppt_id=self.definition.mppt_id,
            string_id=self.definition.string_id,
            segment_index=index,
            segment_id=segment_id,
            segment_type=segment_type,
            polarity=polarity,
            from_node_id=from_node_id,
            to_node_id=to_node_id,
            module_id=module_id,
            from_x=start.x,
            from_y=start.y,
            from_z=start.z,
            to_x=end.x,
            to_y=end.y,
            to_z=end.z,
            displacement_m=displacement,
            conductor_length_m=conductor_length_m,
            separation_mm=separation_mm,
            formation=formation,
            installation_class=installation_class,
            conductor_product_id=conductor.product_id,
            conductor_csa_mm2=conductor.nominal_csa_mm2,
            conductor_diameter_mm=conductor.conductor_diameter_mm,
            cable_od_mm=conductor.cable_od_mm,
            r20_ohm_per_m=conductor.r20_ohm_per_m,
            temperature_c=temperature_c,
            effective_epsilon_r=effective_epsilon_r,
            loop_parameter_weight=loop_parameter_weight,
            coil_turns=coil_turns,
            coil_diameter_mm=coil_diameter_mm,
            connector_count=connector_count,
            connector_resistance_ohm_each=(
                connector_resistance_ohm_each
            ),
            provenance=provenance,
            source_reference=source_reference,
            user_override=user_override,
            feasibility_status=self.feasibility.status,
            saving_available=self.feasibility.feasible,
            warnings=";".join(sorted(set(warnings))),
        )
        row.validate()
        self.rows.append(row)
        return row


def canonical_input_hash(inputs: TopologyInputs) -> str:
    inputs.validate()
    payload = asdict(inputs)
    canonical = json.dumps(
        payload,
        sort_keys=True,
        separators=(",", ":"),
    ).encode("utf-8")
    return hashlib.sha256(canonical).hexdigest()


def archetype_strings(
    inputs: TopologyInputs,
) -> tuple[StringDefinition, ...]:
    inputs.validate()
    definitions: list[StringDefinition] = []
    inverter_x = -inputs.inverter_distance_m
    local_number = 1

    for face, bands, sign in (
        ("E", inputs.east_bands, -1),
        ("W", inputs.west_bands, 1),
    ):
        for band_index, count in enumerate(bands, start=1):
            row_start = (
                (band_index - 1)
                * (inputs.row_span_m + inputs.band_gap_m)
            )
            row_end = row_start + inputs.row_span_m
            for rank in range(1, count + 1):
                y = sign * rank * inputs.rank_plan_pitch_m
                definitions.append(
                    StringDefinition(
                        inverter_id=1,
                        mppt_id=(local_number - 1) // 2 + 1,
                        string_id=(
                            f"INV0001-{face}-B{band_index}-R{rank:02d}"
                        ),
                        face=face,
                        band=band_index,
                        rank=rank,
                        row_start_x_m=row_start,
                        row_end_x_m=row_end,
                        row_y_m=y,
                        inverter_x_m=inverter_x,
                        inverter_y_m=y,
                    )
                )
                local_number += 1

    if not definitions:
        raise ValueError("At least one archetype string is required")
    return tuple(definitions)


def string_counts_per_inverter(
    total_string_count: int,
    inverter_count: int,
    maximum_strings: int,
) -> tuple[int, ...]:
    if inverter_count < 1 or total_string_count < 1:
        raise ValueError("string and inverter counts must be positive")
    if maximum_strings < 1:
        raise ValueError("maximum_strings must be positive")
    if total_string_count > inverter_count * maximum_strings:
        raise ValueError("string count exceeds inverter archetype capacity")

    minimum, remainder = divmod(total_string_count, inverter_count)
    if minimum > maximum_strings:
        raise ValueError("minimum allocation exceeds maximum_strings")

    counts = tuple(
        minimum + (1 if index < remainder else 0)
        for index in range(inverter_count)
    )
    if max(counts) > maximum_strings:
        raise ValueError("distributed count exceeds maximum_strings")
    if sum(counts) != total_string_count:
        raise AssertionError("fleet string distribution is not conservative")
    return counts


def fleet_string_definitions(
    inputs: TopologyInputs,
) -> Iterator[StringDefinition]:
    templates = archetype_strings(inputs)
    counts = string_counts_per_inverter(
        inputs.total_site_string_count,
        inputs.inverter_count,
        len(templates),
    )

    for inverter_id, count in enumerate(counts, start=1):
        for local_number, template in enumerate(
            templates[:count],
            start=1,
        ):
            yield StringDefinition(
                inverter_id=inverter_id,
                mppt_id=(local_number - 1) // 2 + 1,
                string_id=(
                    f"INV{inverter_id:04d}-{template.face}-"
                    f"B{template.band}-R{template.rank:02d}"
                ),
                face=template.face,
                band=template.band,
                rank=template.rank,
                row_start_x_m=template.row_start_x_m,
                row_end_x_m=template.row_end_x_m,
                row_y_m=template.row_y_m,
                inverter_x_m=template.inverter_x_m,
                inverter_y_m=template.inverter_y_m,
            )
