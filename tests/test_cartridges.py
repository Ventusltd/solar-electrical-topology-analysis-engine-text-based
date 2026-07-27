import pytest

from solar_topology.cartridges import (
    LeapfrogCartridge,
    SequentialCartridge,
    validate_cross_cartridge_invariants,
    validate_segment_chains,
)
from solar_topology.products import (
    EXTERNAL_STRING_6MM2,
    FACTORY_LEAD_4MM2,
)
from solar_topology.segments import (
    TopologyInputs,
    archetype_strings,
    fleet_string_definitions,
    string_counts_per_inverter,
)


def external_cable_total(rows):
    external_types = {
        "external_positive_home_run",
        "external_negative_home_run",
        "external_sequential_row_return",
    }
    return sum(
        row.conductor_length_m
        for row in rows
        if row.segment_type in external_types
    )


def factory_lead_total(rows):
    return sum(
        row.conductor_length_m
        for row in rows
        if row.segment_type in {
            "module_factory_positive_lead",
            "module_factory_negative_lead",
        }
    )


def connector_count(rows):
    return sum(row.connector_count for row in rows)


def test_declared_conductor_records_are_not_recreated_from_csa():
    assert EXTERNAL_STRING_6MM2.conductor_diameter_mm == 3.00
    assert EXTERNAL_STRING_6MM2.r20_ohm_per_m == pytest.approx(
        3.39e-3
    )
    assert FACTORY_LEAD_4MM2.conductor_diameter_mm == 2.45
    assert FACTORY_LEAD_4MM2.r20_ohm_per_m == pytest.approx(
        5.09e-3
    )
    assert 0.70 <= EXTERNAL_STRING_6MM2.envelope_fill_factor <= 0.95
    assert 0.70 <= FACTORY_LEAD_4MM2.envelope_fill_factor <= 0.95


def test_default_row_span_canary_is_39_67_metres():
    inputs = TopologyInputs()
    assert inputs.module_pitch_m == pytest.approx(1.323)
    assert inputs.row_span_m == pytest.approx(39.67)


def test_fleet_distribution_uses_actual_string_count():
    counts = string_counts_per_inverter(18_918, 795)
    assert len(counts) == 795
    assert sum(counts) == 18_918
    assert counts.count(24) == 633
    assert counts.count(23) == 162


def test_archetype_and_full_fleet_are_headless_and_deterministic():
    inputs = TopologyInputs()
    assert len(archetype_strings(inputs)) == 24

    first = list(fleet_string_definitions(inputs))
    second = list(fleet_string_definitions(inputs))
    assert first == second
    assert len(first) == 18_918
    assert first[0].string_id == "INV0001-E-B1-R01"
    assert first[-1].inverter_id == 795


def test_leapfrog_order_returns_to_the_near_end():
    cartridge = LeapfrogCartridge()
    assert cartridge.module_order(6) == (1, 3, 5, 6, 4, 2)
    assert cartridge.module_order(5) == (1, 3, 5, 4, 2)


def test_leapfrog_factory_lead_length_gate():
    cartridge = LeapfrogCartridge()
    default = cartridge.feasibility(TopologyInputs())
    assert default.required_reach_m == pytest.approx(2.646)
    assert default.available_reach_m == pytest.approx(0.630)
    assert default.feasible is False

    short = cartridge.feasibility(
        TopologyInputs(
            positive_factory_lead_m=1.2,
            negative_factory_lead_m=1.2,
        )
    )
    assert short.margin_m == pytest.approx(-0.246)
    assert short.extension_required_m == pytest.approx(0.246)

    passing = cartridge.feasibility(
        TopologyInputs(
            positive_factory_lead_m=1.4,
            negative_factory_lead_m=1.4,
        )
    )
    assert passing.feasible is True
    assert passing.margin_m == pytest.approx(0.154)


def test_cartridges_emit_one_shared_segment_contract():
    inputs = TopologyInputs(
        inverter_count=1,
        total_site_string_count=24,
    )
    definition = archetype_strings(inputs)[0]
    sequential = SequentialCartridge().build_segments(
        inputs,
        definition,
    )
    leapfrog = LeapfrogCartridge().build_segments(
        inputs,
        definition,
    )

    validate_segment_chains(sequential)
    validate_segment_chains(leapfrog)

    assert sequential[0].segment_type == "external_positive_home_run"
    assert sequential[-1].segment_type == "external_negative_home_run"
    assert leapfrog[0].segment_type == "external_positive_home_run"
    assert leapfrog[-1].segment_type == "external_negative_home_run"
    assert any(
        row.segment_type == "external_sequential_row_return"
        for row in sequential
    )
    assert not any(
        row.segment_type == "external_sequential_row_return"
        for row in leapfrog
    )


def test_factory_copper_and_connectors_are_cartridge_invariants():
    inputs = TopologyInputs(
        inverter_count=1,
        total_site_string_count=24,
    )
    definition = archetype_strings(inputs)[0]
    sequential = SequentialCartridge().build_segments(
        inputs,
        definition,
    )
    leapfrog = LeapfrogCartridge().build_segments(
        inputs,
        definition,
    )

    expected_factory = inputs.modules_per_string * (
        inputs.positive_factory_lead_m
        + inputs.negative_factory_lead_m
    )
    assert factory_lead_total(sequential) == pytest.approx(
        expected_factory
    )
    assert factory_lead_total(leapfrog) == pytest.approx(
        expected_factory
    )
    assert connector_count(sequential) == 62
    assert connector_count(leapfrog) == 62

    validate_cross_cartridge_invariants(sequential + leapfrog)


def test_only_external_row_return_creates_theoretical_saving():
    inputs = TopologyInputs(
        inverter_count=1,
        total_site_string_count=24,
    )
    definition = archetype_strings(inputs)[0]
    sequential = SequentialCartridge().build_segments(
        inputs,
        definition,
    )
    leapfrog = LeapfrogCartridge().build_segments(
        inputs,
        definition,
    )

    assert external_cable_total(sequential) == pytest.approx(59.67)
    assert external_cable_total(leapfrog) == pytest.approx(20.0)
    assert (
        external_cable_total(sequential)
        - external_cable_total(leapfrog)
    ) == pytest.approx(inputs.row_span_m)


def test_infeasible_leapfrog_rows_cannot_claim_available_saving():
    inputs = TopologyInputs(
        inverter_count=1,
        total_site_string_count=24,
    )
    definition = archetype_strings(inputs)[0]
    rows = LeapfrogCartridge().build_segments(inputs, definition)

    assert rows
    assert all(row.saving_available is False for row in rows)
    assert all(
        row.feasibility_status == "INFEASIBLE_LENGTH_SCREEN"
        for row in rows
    )


def test_measured_reach_override_is_explicit():
    inputs = TopologyInputs(
        measured_leapfrog_span_m=2.2,
        positive_factory_lead_m=1.2,
        negative_factory_lead_m=1.2,
    )
    feasibility = LeapfrogCartridge().feasibility(inputs)

    assert feasibility.basis == "MEASURED_ROUTED_SPAN"
    assert feasibility.feasible is True
    assert feasibility.margin_m == pytest.approx(0.2)
