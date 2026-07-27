"""Generic declared conductor records used by topology cartridges."""

from __future__ import annotations

from dataclasses import asdict, dataclass
import math


@dataclass(frozen=True)
class ConductorSpec:
    """Finished-cable values kept separate from nominal identifying size."""

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

    def as_dict(self) -> dict:
        self.validate()
        return asdict(self)


FACTORY_LEAD_4MM2 = ConductorSpec(
    product_id="factory_module_lead_4mm2_metal_coated_class5",
    nominal_csa_mm2=4.0,
    conductor_diameter_mm=2.45,
    cable_od_mm=5.5,
    r20_ohm_per_m=5.09e-3,
)


EXTERNAL_STRING_6MM2 = ConductorSpec(
    product_id="external_string_6mm2_metal_coated_class5",
    nominal_csa_mm2=6.0,
    conductor_diameter_mm=3.00,
    cable_od_mm=6.1,
    r20_ohm_per_m=3.39e-3,
)


for _specification in (FACTORY_LEAD_4MM2, EXTERNAL_STRING_6MM2):
    _specification.validate()
