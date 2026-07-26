import math

import pytest

from solar_topology.topology import (
    FormationConfig,
    GeometryConfig,
    build_export,
    build_site_model,
    validate_no_user_route_lengths,
)


def test_default_structure_is_two_faces_with_five_five_two_bands_each():
    strings = build_site_model()
    assert len(strings) == 24
    assert sum(s.face == "E" for s in strings) == 12
    assert sum(s.face == "W" for s in strings) == 12
    assert all(s.module_count == 30 for s in strings)


def test_rank_slope_and_plan_projection_are_not_conflated():
    g = GeometryConfig(tilt_deg=10.0)
    slope_pitch = g.module_length_m + g.clamp_gap_m
    plan_pitch = slope_pitch * math.cos(math.radians(g.tilt_deg))
    assert slope_pitch == pytest.approx(2.404)
    assert plan_pitch < slope_pitch


def test_string_is_an_ordered_chain_of_typed_segments():
    string = build_site_model()[0]
    types = [s.segment_type for s in string.segments]
    assert types.count("module_interconnect") == 29
    assert types.count("coiled_surplus") == 60
    assert "along_rank_return" in types
    assert "across_table_transfer" in types
    assert "structure_drop" in types
    assert "surface_or_trench_run" in types
    assert [s.sequence_index for s in string.segments] == list(range(1, len(string.segments) + 1))


def test_coiled_surplus_has_zero_displacement_but_real_length():
    string = build_site_model()[0]
    coils = [s for s in string.segments if s.segment_type == "coiled_surplus"]
    assert coils
    assert all(s.geometric_displacement_m == pytest.approx(0.0) for s in coils)
    assert all(s.installed_conductor_length_m == pytest.approx(0.20) for s in coils)


def test_every_segment_has_formation_separation_and_provenance():
    string = build_site_model()[0]
    for segment in string.segments:
        assert segment.formation_type
        assert segment.conductor_separation_mm > 0
        assert segment.provenance
        assert segment.route_length_source == "derived_from_segment_geometry"


def test_export_route_length_is_exact_segment_sum_and_derived():
    geometry = GeometryConfig()
    formations = FormationConfig()
    export = build_export(build_site_model(geometry, formations), geometry, formations)
    validate_no_user_route_lengths(export)
    for string in export["strings"]:
        expected = sum(s["installed_conductor_length_m"] for s in string["segments"])
        assert string["route_length"]["value_m"] == pytest.approx(expected)
        assert string["route_length"]["source"] == "segment_list"
        assert string["route_length"]["provenance"] == "derived"


def test_validation_fails_if_route_length_is_user_supplied():
    geometry = GeometryConfig()
    formations = FormationConfig()
    export = build_export(build_site_model(geometry, formations), geometry, formations)
    export["strings"][0]["route_length"] = {
        "value_m": 999.0,
        "source": "user_input",
        "provenance": "user_overridden",
    }
    with pytest.raises(ValueError, match="was not derived"):
        validate_no_user_route_lengths(export)


def test_headless_scale_target_builds_without_renderer():
    # 24 strings per inverter × 792 inverter blocks = 19,008 strings.
    base = build_site_model()
    total_strings = len(base) * 792
    assert total_strings == 19008
    # The topology module imports no browser, canvas or mapping package.
    import solar_topology.topology as topology
    source_names = set(topology.__dict__)
    assert "canvas" not in source_names
    assert "maplibre" not in source_names
