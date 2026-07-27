"""Authoritative closed-form Tier 1 formulae with explicit units and guards."""

from __future__ import annotations

from dataclasses import dataclass
import math

from pint import UnitRegistry


ureg = UnitRegistry()
Q_ = ureg.Quantity
MU0 = 4 * math.pi * 1e-7 * ureg.henry / ureg.metre
EPS0 = 8.8541878128e-12 * ureg.farad / ureg.metre
ALPHA_CU_20 = 0.00393 / ureg.kelvin


@dataclass(frozen=True)
class TwoWireParameters:
    """Two-wire parameters with external and internal inductance separated."""

    external_inductance_per_length: object
    internal_inductance_per_length: object
    inductance_per_length: object
    capacitance_per_length: object
    characteristic_impedance: object
    propagation_velocity: object


def dc_resistance(
    length,
    r20_per_length,
    temperature=Q_(20, ureg.degC),
):
    """Resistance from declared finished-cable R20 and conductor temperature.

    Nominal cross-sectional area is an identifying size. It is not used here to
    recreate a resistance from bulk material resistivity. The caller supplies the
    declared or measured finished-cable resistance per unit length.
    """

    length = length.to(ureg.metre)
    r20_per_length = r20_per_length.to(ureg.ohm / ureg.metre)
    delta_t = temperature.to(ureg.degC).magnitude - 20.0
    factor = 1 + ALPHA_CU_20.magnitude * delta_t

    return (length * r20_per_length * factor).to(ureg.ohm)


def two_wire_parameters(
    centre_spacing,
    conductor_diameter,
    epsilon_r: float = 1.0,
) -> TwoWireParameters:
    """Return round two-wire transmission and low-frequency parameters.

    The geometry term is ``acosh(D / d_conductor)``. The cable outside diameter
    must not be substituted for the declared stranded-conductor diameter.

    Characteristic impedance and propagation velocity use external inductance
    only. This preserves the TEM identity ``v = c / sqrt(epsilon_r)`` because the
    geometry term cancels between external inductance and capacitance.

    Low-frequency internal loop inductance is retained separately as
    ``mu0 / (4*pi)`` H/m, representing ``mu0 / (8*pi)`` for each conductor. It is
    included in the total low-frequency inductance for stored energy and lumped
    ``L di/dt`` studies, but not in propagation velocity or surge impedance.
    """

    spacing = centre_spacing.to(ureg.metre)
    diameter = conductor_diameter.to(ureg.metre)
    ratio = (spacing / diameter).to_base_units().magnitude

    if ratio <= 1:
        raise ValueError(
            "Conductor centre spacing must exceed conductor diameter"
        )
    if epsilon_r <= 0:
        raise ValueError("Relative permittivity must be positive")

    geometry = math.acosh(ratio)
    external_inductance = (
        MU0 / math.pi * geometry
    ).to(ureg.henry / ureg.metre)
    internal_inductance = (
        MU0 / (4 * math.pi)
    ).to(ureg.henry / ureg.metre)
    low_frequency_inductance = external_inductance + internal_inductance
    capacitance = (
        math.pi * EPS0 * epsilon_r / geometry
    ).to(ureg.farad / ureg.metre)
    characteristic_impedance = (
        external_inductance / capacitance
    ) ** 0.5
    propagation_velocity = (
        1 / (external_inductance * capacitance) ** 0.5
    ).to(ureg.metre / ureg.second)

    return TwoWireParameters(
        external_inductance,
        internal_inductance,
        low_frequency_inductance,
        capacitance,
        characteristic_impedance.to(ureg.ohm),
        propagation_velocity,
    )


def module_frame_capacitance(
    effective_area,
    dielectric_thickness,
    epsilon_r: float,
):
    """Parallel-plate indicative module-to-frame capacitance."""

    if epsilon_r <= 0:
        raise ValueError("Relative permittivity must be positive")

    return (
        EPS0
        * epsilon_r
        * effective_area.to(ureg.metre**2)
        / dielectric_thickness.to(ureg.metre)
    ).to(ureg.farad)


def cold_string_voc(
    module_voc,
    module_count: int,
    beta_voc_percent_per_c: float,
    cell_temperature,
):
    """Linear temperature-coefficient screen for cold string open circuit voltage."""

    if module_count < 1:
        raise ValueError("module_count must be at least one")

    temperature_delta = (
        cell_temperature.to(ureg.degC).magnitude - 25.0
    )
    factor = 1 + (
        beta_voc_percent_per_c / 100.0
    ) * temperature_delta

    return (module_count * module_voc * factor).to(ureg.volt)


def derived_route_length(
    near_end_distance,
    rank_index: int,
    rank_pitch,
    inverter_drop,
):
    """Geometry-only route rule with no user-supplied final length argument."""

    if rank_index < 0:
        raise ValueError("rank_index cannot be negative")

    return (
        near_end_distance
        + rank_index * rank_pitch
        + inverter_drop
    ).to(ureg.metre)


def stored_magnetic_energy(inductance, current):
    """Stored magnetic energy for a consistent total inductance."""

    return (0.5 * inductance * current**2).to(ureg.joule)


def stored_electric_energy(capacitance, voltage):
    """Stored electric energy for a consistent total capacitance."""

    return (0.5 * capacitance * voltage**2).to(ureg.joule)
