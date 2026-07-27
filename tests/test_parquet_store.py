import json
import math

import duckdb
import pytest

from solar_topology.parquet_store import (
    build_deterministic_store,
    build_store,
)
from solar_topology.segments import TopologyInputs


def read_one(connection, path, columns="*"):
    return connection.execute(
        f"SELECT {columns} FROM read_parquet(?)",
        [str(path)],
    ).fetchone()


def test_deterministic_partitioned_store_and_actual_string_count(tmp_path):
    inputs = TopologyInputs(
        inverter_count=2,
        total_site_string_count=47,
        positive_factory_lead_m=1.4,
        negative_factory_lead_m=1.4,
    )
    output = tmp_path / "store"
    result = build_deterministic_store(
        inputs,
        output,
        source_commit="test-commit",
    )

    assert result["deterministic"] is True
    assert result["string_count"] == 47
    assert result["generated_segment_rows"] == 47 * 183

    partitions = sorted(
        output.glob("segments/topology=*/band=*/data_*.parquet")
    )
    result_partitions = sorted(
        output.glob("results/segments/topology=*/band=*/data_*.parquet")
    )
    assert len(partitions) == 6
    assert len(result_partitions) == 6

    connection = duckdb.connect()
    try:
        comparison = read_one(
            connection,
            output / "aggregates" / "comparison.parquet",
        )
        assert comparison[0] == 47
        assert comparison[3] == pytest.approx(47 * 39.67)
        assert comparison[4] == pytest.approx(47 * 39.67)
        assert comparison[5] is True

        site = connection.execute(
            """
            SELECT topology, string_count
            FROM read_parquet(?)
            ORDER BY topology
            """,
            [str(output / "aggregates" / "site.parquet")],
        ).fetchall()
        assert site == [("leapfrog", 47), ("sequential", 47)]

        factory = connection.execute(
            """
            SELECT
                topology,
                min(factory_lead_m),
                max(factory_lead_m),
                min(connector_count),
                max(connector_count)
            FROM read_parquet(?)
            GROUP BY topology
            ORDER BY topology
            """,
            [str(output / "aggregates" / "strings.parquet")],
        ).fetchall()
        assert factory == [
            ("leapfrog", 84.0, 84.0, 62, 62),
            ("sequential", 84.0, 84.0, 62, 62),
        ]

        result_glob = (
            output / "results" / "segments" / "**" / "*.parquet"
        )
        speeds = connection.execute(
            """
            SELECT
                min(propagation_velocity_m_per_s),
                max(propagation_velocity_m_per_s)
            FROM read_parquet(?, hive_partitioning = true)
            WHERE loop_parameter_weight > 0
            """,
            [str(result_glob)],
        ).fetchone()
        expected_velocity = 1 / math.sqrt(
            4 * math.pi * 1e-7
            * 8.8541878128e-12
            * inputs.effective_epsilon_r
        )
        assert speeds[0] == pytest.approx(expected_velocity)
        assert speeds[1] == pytest.approx(expected_velocity)
    finally:
        connection.close()

    manifest = json.loads(
        (
            output
            / "manifests"
            / "topology=leapfrog"
            / "manifest.json"
        ).read_text(encoding="utf-8")
    )
    assert manifest["data_law_result"] == "PASS"
    assert manifest["distinct_string_count"] == 47
    assert manifest["feasibility_status"] == "FEASIBLE_LENGTH_SCREEN"
    assert manifest["parquet_files"]


def test_infeasible_leapfrog_keeps_theory_but_blocks_available_saving(
    tmp_path,
):
    inputs = TopologyInputs(
        inverter_count=1,
        total_site_string_count=24,
    )
    output = tmp_path / "store"
    build_store(inputs, output, source_commit="test-commit")

    connection = duckdb.connect()
    try:
        comparison = read_one(
            connection,
            output / "aggregates" / "comparison.parquet",
        )
        assert comparison[0] == 24
        assert comparison[3] == pytest.approx(24 * 39.67)
        assert comparison[4] is None
        assert comparison[5] is False
    finally:
        connection.close()


def test_route_and_conductor_length_are_separate_columns(tmp_path):
    inputs = TopologyInputs(
        inverter_count=1,
        total_site_string_count=1,
        east_bands=(1,),
        west_bands=(),
        positive_factory_lead_m=1.4,
        negative_factory_lead_m=1.4,
    )
    output = tmp_path / "store"
    build_store(inputs, output, source_commit="test-commit")

    connection = duckdb.connect()
    try:
        rows = connection.execute(
            """
            SELECT
                topology,
                route_displacement_m,
                conductor_length_m
            FROM read_parquet(?)
            ORDER BY topology
            """,
            [str(output / "aggregates" / "strings.parquet")],
        ).fetchall()
        assert len(rows) == 2
        assert all(route != conductor for _, route, conductor in rows)
    finally:
        connection.close()
