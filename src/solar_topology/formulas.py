"""Authoritative closed-form Tier 1 formulae with explicit units and validity guards."""
from __future__ import annotations
from dataclasses import dataclass
import math
from pint import UnitRegistry

ureg = UnitRegistry()
Q_ = ureg.Quantity
MU0 = 4 * math.pi * 1e-7 * ureg.henry / ureg.metre
EPS0 = 8.8541878128e-12 * ureg.farad / ureg.metre
RHO_CU_20 = 1.724e-8 * ureg.ohm * ureg.metre
ALPHA_CU_20 = 0.00393 / ureg.kelvin

@dataclass(frozen=True)
class TwoWireParameters:
    external_inductance_per_length: object
    internal_inductance_per_length: object
    inductance_per_length: object
    capacitance_per_length: object
    characteristic_impedance: object
    propagation_velocity: object


def conductor_diameter_from_area(area):
    """Equivalent circular conductor diameter from metallic CSA; never cable outside diameter."""
    area = area.to(ureg.metre**2)
    return (2 * (area / math.pi) ** 0.5).to(ureg.millimetre)


def dc_resistance(length, area, temperature=Q_(20, ureg.degC)):
    """Copper resistance at operating temperature for supplied total metallic length."""
    length = length.to(ureg.metre)
    area = area.to(ureg.metre**2)
    delta_t = temperature.to(ureg.degC).magnitude - 20.0
    return (RHO_CU_20 * length / area * (1 + ALPHA_CU_20.magnitude * delta_t)).to(ureg.ohm)


def two_wire_parameters(centre_spacing, conductor_diameter, epsilon_r: float = 1.0) -> TwoWireParameters:
    """Round two-wire TEM screen using acosh(D/d_conductor), including low-frequency internal L.

    Internal loop inductance is μ0/(4π) H/m: μ0/(8π) for each of two conductors.
    """
    D = centre_spacing.to(ureg.metre)
    d = conductor_diameter.to(ureg.metre)
    ratio = (D / d).to_base_units().magnitude
    if ratio <= 1:
        raise ValueError("Conductor centre spacing must exceed conductor diameter")
    if epsilon_r <= 0:
        raise ValueError("Relative permittivity must be positive")
    geometry = math.acosh(ratio)
    external_lp = (MU0 / math.pi * geometry).to(ureg.henry / ureg.metre)
    internal_lp = (MU0 / (4 * math.pi)).to(ureg.henry / ureg.metre)
    lp = external_lp + internal_lp
    cp = (math.pi * EPS0 * epsilon_r / geometry).to(ureg.farad / ureg.metre)
    z0 = ((lp / cp) ** 0.5).to(ureg.ohm)
    velocity = (1 / (lp * cp) ** 0.5).to(ureg.metre / ureg.second)
    return TwoWireParameters(external_lp, internal_lp, lp, cp, z0, velocity)


def module_frame_capacitance(effective_area, dielectric_thickness, epsilon_r: float):
    """Parallel-plate indicative module-to-frame capacitance."""
    if epsilon_r <= 0:
        raise ValueError("Relative permittivity must be positive")
    return (EPS0 * epsilon_r * effective_area.to(ureg.metre**2) / dielectric_thickness.to(ureg.metre)).to(ureg.farad)


def cold_string_voc(module_voc, module_count: int, beta_voc_percent_per_c: float, cell_temperature):
    if module_count < 1:
        raise ValueError("module_count must be at least one")
    factor = 1 + (beta_voc_percent_per_c / 100.0) * (cell_temperature.to(ureg.degC).magnitude - 25.0)
    return (module_count * module_voc * factor).to(ureg.volt)


def derived_route_length(near_end_distance, rank_index: int, rank_pitch, inverter_drop):
    """Geometry-only route rule. No user-supplied final length argument exists."""
    if rank_index < 0:
        raise ValueError("rank_index cannot be negative")
    return (near_end_distance + rank_index * rank_pitch + inverter_drop).to(ureg.metre)


def stored_magnetic_energy(inductance, current):
    return (0.5 * inductance * current**2).to(ureg.joule)


def stored_electric_energy(capacitance, voltage):
    return (0.5 * capacitance * voltage**2).to(ureg.joule)
