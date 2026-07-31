from __future__ import annotations

import pytest

from solar_topology.array import (
    ARRAY_AUTHORITY_MIGRATION_STAGE,
    ARRAY_AUTHORITY_STATUS,
    WiringStrategy,
    compare_reference_24_by_30,
    reference_24_by_30_build,
)


def test_installed_array_api_exposes_build_025_authority() -> None:
    assert ARRAY_AUTHORITY_STATUS == "canonical_candidate"
    assert ARRAY_AUTHORITY_MIGRATION_STAGE == "build-025.5-installed-api"

    build = reference_24_by_30_build(strategy=WiringStrategy.LEAPFROG)

    assert build.geometry.module_count == 720
    assert len(build.routing.strings) == 24
    assert build.routing.metrics.total_circuit_conductor_length_m > 0
    assert build.receipt_hash.startswith("sha256:")


def test_installed_array_api_reconciles_strategy_accounting() -> None:
    comparison = compare_reference_24_by_30()
    sequential = comparison.sequential.routing.metrics
    leapfrog = comparison.leapfrog.routing.metrics

    assert sequential.total_circuit_conductor_length_m == pytest.approx(
        2513.328
    )
    assert leapfrog.total_circuit_conductor_length_m == pytest.approx(
        2560.128
    )
    assert (
        sequential.inverter_home_run_length_m
        - leapfrog.inverter_home_run_length_m
    ) == pytest.approx(798.288)
    assert (
        leapfrog.series_interconnect_length_m
        - sequential.series_interconnect_length_m
    ) == pytest.approx(845.088)
    assert (
        leapfrog.total_circuit_conductor_length_m
        - sequential.total_circuit_conductor_length_m
    ) == pytest.approx(46.8)
    assert (
        100
        * (
            sequential.absolute_enclosed_loop_area_m2
            - leapfrog.absolute_enclosed_loop_area_m2
        )
        / sequential.absolute_enclosed_loop_area_m2
    ) == pytest.approx(79.801548963)
