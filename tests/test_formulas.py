import inspect
import math
import pytest

from solar_topology.formulas import (
    Q_, ureg, conductor_diameter_from_area, dc_resistance,
    two_wire_parameters, module_frame_capacitance,
    cold_string_voc, derived_route_length,
)


def test_6mm2_equivalent_conductor_diameter():
    d = conductor_diameter_from_area(Q_(6, ureg.mm**2))
    assert d.to(ureg.mm).magnitude == pytest.approx(math.sqrt(24 / math.pi), rel=1e-12)


def test_two_wire_uses_conductor_diameter_and_has_internal_inductance():
    d = conductor_diameter_from_area(Q_(6, ureg.mm**2))
    p = two_wire_parameters(Q_(20, ureg.mm), d, 2.3)
    expected_internal = 1e-7  # μ0/(4π), two conductors in the loop
    assert p.internal_inductance_per_length.to(ureg.H / ureg.m).magnitude == pytest.approx(expected_internal)
    assert p.inductance_per_length > p.external_inductance_per_length
    assert p.characteristic_impedance.to(ureg.ohm).magnitude > 0


def test_rank_pitch_has_no_walkway_allowance():
    module_length = Q_(2.384, ureg.m)
    clamp_gap = Q_(0.020, ureg.m)
    rank_pitch = module_length + clamp_gap
    assert rank_pitch.magnitude == pytest.approx(2.404)


def test_route_length_is_derived_from_geometry_only():
    length = derived_route_length(Q_(39.67, ureg.m), 4, Q_(2.404, ureg.m), Q_(2, ureg.m))
    assert length.to(ureg.m).magnitude == pytest.approx(51.286)
    # The API intentionally has no route_length/user_length parameter.
    parameters = inspect.signature(derived_route_length).parameters
    assert 'route_length' not in parameters
    assert 'user_length' not in parameters


def test_user_cannot_supply_final_route_length():
    with pytest.raises(TypeError):
        derived_route_length(
            Q_(0, ureg.m), 0, Q_(2.404, ureg.m), Q_(2, ureg.m),
            route_length=Q_(999, ureg.m),
        )


def test_temperature_corrected_resistance_golden_value():
    r = dc_resistance(Q_(100, ureg.m), Q_(6, ureg.mm**2), Q_(70, ureg.degC))
    expected = 1.724e-8 * 100 / 6e-6 * (1 + 0.00393 * 50)
    assert r.to(ureg.ohm).magnitude == pytest.approx(expected, rel=1e-12)


def test_module_frame_capacitance_parallel_plate():
    c = module_frame_capacitance(Q_(1.303 * 2.384, ureg.m**2), Q_(2, ureg.mm), 6)
    expected = 8.8541878128e-12 * 6 * (1.303 * 2.384) / 0.002
    assert c.to(ureg.F).magnitude == pytest.approx(expected, rel=1e-12)


def test_cold_voc_30_module_default():
    v = cold_string_voc(Q_(45.9, ureg.V), 30, -0.25, Q_(-10, ureg.degC))
    assert v.to(ureg.V).magnitude == pytest.approx(30 * 45.9 * 1.0875)
