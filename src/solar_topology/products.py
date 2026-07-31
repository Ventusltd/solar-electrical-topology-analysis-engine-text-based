"""Generic conductor products with independently resolved resistance evidence."""

from __future__ import annotations

from dataclasses import asdict, dataclass
import math

from .resistance_evidence import (
    ResistanceBasis,
    ResistanceValueKind,
    ResolvedConductorResistance,
    register_conductor_resistance,
    resolve_conductor_resistance,
)


@dataclass(frozen=True)
class ConductorSpec:
    """Finished-cable geometry kept separate from resistance authority.

    This dataclass intentionally retains its pre-refinement serialised shape so
    geometry and topology input hashes do not change when resistance evidence is
    registered, verified or revised. Resistance authority is resolved by
    ``product_id`` through the independent registry.
    """

    product_id: str
    nominal_csa_mm2: float
    conductor_diameter_mm: float
    cable_od_mm: float
    r20_ohm_per_m: float
    provenance: str = "oem_declared"

    @property
    def envelope_fill_factor(self) -> float:
        envelope_area = (
            math.pi * self.conductor_diameter_mm**2 / 4
        )
        return self.nominal_csa_mm2 / envelope_area

    @property
    def resolved_resistance(self) -> ResolvedConductorResistance:
        return resolve_conductor_resistance(
            product_id=self.product_id,
            r20_ohm_per_m=self.r20_ohm_per_m,
            legacy_provenance=self.provenance,
            legacy_source_reference="legacy_conductor_spec",
        )

    def validate(self) -> None:
        if not self.product_id:
            raise ValueError("product_id is required")
        if self.nominal_csa_mm2 <= 0:
            raise ValueError("nominal_csa_mm2 must be positive")
        if self.conductor_diameter_mm <= 0:
            raise ValueError("conductor_diameter_mm must be positive")
        if self.cable_od_mm < self.conductor_diameter_mm:
            raise ValueError(
                "cable_od_mm cannot be smaller than conductor_diameter_mm"
            )
        if self.r20_ohm_per_m <= 0:
            raise ValueError("r20_ohm_per_m must be positive")
        if not 0.70 <= self.envelope_fill_factor <= 0.95:
            raise ValueError(
                "Declared conductor envelope fill must be between 70% and 95%"
            )
        if self.provenance not in {
            "measured",
            "oem_declared",
            "assumed",
            "defaulted",
        }:
            raise ValueError("unsupported legacy conductor provenance")
        resistance = self.resolved_resistance
        if resistance.product_id != self.product_id:
            raise ValueError(
                "resistance evidence product_id must match conductor product_id"
            )
        if not math.isclose(
            resistance.r20_ohm_per_m,
            self.r20_ohm_per_m,
            rel_tol=0.0,
            abs_tol=1e-15,
        ):
            raise ValueError(
                "resistance evidence R20 must match conductor R20"
            )

    def as_dict(self) -> dict:
        self.validate()
        return asdict(self)


register_conductor_resistance(
    ResolvedConductorResistance(
        product_id="factory_module_lead_4mm2_metal_coated_class5",
        r20_ohm_per_m=5.09e-3,
        basis=ResistanceBasis.STANDARD_MAXIMUM,
        value_kind=ResistanceValueKind.STANDARD_MAXIMUM,
        source_reference=(
            "IEC 60228 Class 5 metal-coated copper maximum-resistance table"
        ),
        source_revision="edition-not-yet-encoded",
        verification_state="standards_review_required",
        temperature_coefficient_per_c=0.00393,
        temperature_coefficient_basis=(
            "copper linear temperature correction from 20 C"
        ),
        warnings=(
            "Numeric standard source requires edition and table verification before certification use.",
        ),
    )
)

register_conductor_resistance(
    ResolvedConductorResistance(
        product_id="external_string_6mm2_metal_coated_class5",
        r20_ohm_per_m=3.39e-3,
        basis=ResistanceBasis.STANDARD_MAXIMUM,
        value_kind=ResistanceValueKind.STANDARD_MAXIMUM,
        source_reference=(
            "IEC 60228 Class 5 metal-coated copper maximum-resistance table"
        ),
        source_revision="edition-not-yet-encoded",
        verification_state="standards_review_required",
        temperature_coefficient_per_c=0.00393,
        temperature_coefficient_basis=(
            "copper linear temperature correction from 20 C"
        ),
        warnings=(
            "Numeric standard source requires edition and table verification before certification use.",
        ),
    )
)


FACTORY_LEAD_4MM2 = ConductorSpec(
    product_id="factory_module_lead_4mm2_metal_coated_class5",
    nominal_csa_mm2=4.0,
    conductor_diameter_mm=2.45,
    cable_od_mm=5.5,
    r20_ohm_per_m=5.09e-3,
    provenance="oem_declared",
)


EXTERNAL_STRING_6MM2 = ConductorSpec(
    product_id="external_string_6mm2_metal_coated_class5",
    nominal_csa_mm2=6.0,
    conductor_diameter_mm=3.00,
    cable_od_mm=6.1,
    r20_ohm_per_m=3.39e-3,
    provenance="oem_declared",
)


for _specification in (FACTORY_LEAD_4MM2, EXTERNAL_STRING_6MM2):
    _specification.validate()
