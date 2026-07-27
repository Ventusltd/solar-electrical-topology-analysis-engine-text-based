import inspect
import math

import pytest

import solar_topology.formulas as formulas
from solar_topology.formulas import (
    EPS0,
    MU0,
    Q_,
    cold_string_voc,
    dc_resistance,
    derived_route_length,
    module_frame_capacitance,
    two_wire_parameters,
    ureg,
)


def test_nominal_csa_is_not_used_to_invent_conductor_diameter():
    assert not hasattr(formulas, "conductor_diameter_from_area")

    parameters = inspect.signature(two_wire_parameters).parameters
    assert "conductor_diameter" in parameters
    assert "area" not in parameters
    assert "nominal_csa" not in parameters


def test_two_wire_internal_inductance_is_low_frequency_energy_only():
    parameters = two_wire_parameters(
        Q_(20, ureg.mm),
        Q_(3.00, ureg.mm),
        2.3,
    )

    expected_internal = 1e-7
    actual_internal = parameters.internal_inductance_per_length.to(
        ureg.H / ureg.m
    ).magnitude

    assert actual_internal == pytest.approx(expected_internal)
    assert (
        parameters.inductance_per_length
        > parameters.external_inductance_per_length
    )


def test_velocity_identity_uses_external_inductance_only():
    epsilon_r = 2.3
    parameters = two_wire_parameters(
        Q_(20, ureg.mm),
        Q_(3.00, ureg.mm),
        epsilon_r,
    )

    expected_velocity = (
        1 / (MU0 * EPS0 * epsilon_r) ** 0.5
    ).to(ureg.m / ureg.s)

    actual = parameters.propagation_velocity.to(ureg.m / ureg.s).magnitude
    expected = expected_velocity.magnitude

    assert actual / expected == pytest.approx(1.0, rel=1e-12)

    expected_impedance = (
        parameters.external_inductance_per_length
        / parameters.capacitance_per_length
    ) ** 0.5

    assert parameters.characteristic_impedance.to(
        ureg.ohm
    ).magnitude == pytest.approx(
        expected_impedance.to(ureg.ohm).magnitude,
        rel=1e-12,
    )


def test_acosh_domain_guard_rejects_overlapping_conductors():
    with pytest.raises(
        ValueError,
        match="centre spacing must exceed conductor diameter",
    ):
        two_wire_parameters(
            Q_(3.00, ureg.mm),
            Q_(3.00, ureg.mm),
            2.3,
        )


def test_rank_pitch_has_no_walkway_allowance():
    module_length = Q_(2.384, ureg.m)
    clamp_gap = Q_(0.020, ureg.m)
    rank_pitch = module_length + clamp_gap

    assert rank_pitch.magnitude == pytest.approx(2.404)


def test_route_length_is_derived_from_geometry_only():
    length = derived_route_length(
        Q_(39.67, ureg.m),
        4,
        Q_(2.404, ureg.m),
        Q_(2, ureg.m),
    )

    assert length.to(ureg.m).magnitude == pytest.approx(51.286)

    parameters = inspect.signature(derived_route_length).parameters
    assert "route_length" not in parameters
    assert "user_length" not in parameters


def test_user_cannot_supply_final_route_length():
    with pytest.raises(TypeError):
        derived_route_length(
            Q_(0, ureg.m),
            0,
            Q_(2.404, ureg.m),
            Q_(2, ureg.m),
            route_length=Q_(999, ureg.m),
        )


def test_declared_finished_cable_resistance_at_temperature():
    resistance = dc_resistance(
        Q_(100, ureg.m),
        Q_(3.39e-3, ureg.ohm / ureg.m),
        Q_(70, ureg.degC),
    )
    expected = 100 * 3.39e-3 * (1 + 0.00393 * 50)

    assert resistance.to(ureg.ohm).magnitude == pytest.approx(
        expected,
        rel=1e-12,
    )


def test_declared_complete_circuit_canary_worst_case_compliant():
    external = dc_resistance(
        Q_(59.67, ureg.m),
        Q_(3.39e-3, ureg.ohm / ureg.m),
        Q_(70, ureg.degC),
    )
    module_leads = dc_resistance(
        Q_(21.0, ureg.m),
        Q_(5.09e-3, ureg.ohm / ureg.m),
        Q_(75, ureg.degC),
    )
    connector_contacts = Q_(
        62 * 0.35e-3 * (1 + 0.00393 * 55),
        ureg.ohm,
    )

    total = external + module_leads + connector_contacts
    current = Q_(17.35, ureg.ampere)
    string_vmp = Q_(30 * 38.1, ureg.volt)
    voltage_drop = current * total
    power_loss = current**2 * total
    drop_percent = 100 * voltage_drop / string_vmp

    assert total.to(ureg.ohm).magnitude == pytest.approx(
        0.39841430395,
        rel=1e-10,
    )
    assert voltage_drop.to(ureg.volt).magnitude == pytest.approx(
        6.91248817353,
        rel=1e-10,
    )
    assert drop_percent.to_base_units().magnitude == pytest.approx(
        0.604767119294,
        rel=1e-9,
    )
    assert power_loss.to(ureg.watt).magnitude == pytest.approx(
        119.931669811,
        rel=1e-9,
    )


def test_module_frame_capacitance_parallel_plate():
    capacitance = module_frame_capacitance(
        Q_(1.303 * 2.384, ureg.m**2),
        Q_(2, ureg.mm),
        6,
    )
    expected = 8.8541878128e-12 * 6 * (1.303 * 2.384) / 0.002

    assert capacitance.to(ureg.F).magnitude == pytest.approx(
        expected,
        rel=1e-12,
    )


def test_cold_voc_30_module_default():
    voltage = cold_string_voc(
        Q_(45.9, ureg.V),
        30,
        -0.25,
        Q_(-10, ureg.degC),
    )

    assert voltage.to(ureg.V).magnitude == pytest.approx(
        30 * 45.9 * 1.0875
    )
