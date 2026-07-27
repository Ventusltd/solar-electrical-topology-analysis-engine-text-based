"""Deterministic DuckDB build for the partitioned topology segment store."""

from __future__ import annotations

import csv
from dataclasses import fields
import hashlib
import json
from pathlib import Path
import shutil
import tempfile

from .cartridges import INITIAL_CARTRIDGES, build_fleet_segments
from .segments import SegmentRow, TopologyInputs, canonical_input_hash


SEGMENT_COLUMNS = tuple(field.name for field in fields(SegmentRow))
NULL_TOKEN = "__NULL__"

SEGMENT_SCHEMA_SQL = """
CREATE TABLE segments (
    run_id VARCHAR,
    schema_version VARCHAR,
    topology VARCHAR,
    band INTEGER,
    cartridge_version VARCHAR,
    inverter_id INTEGER,
    mppt_id INTEGER,
    string_id VARCHAR,
    segment_index INTEGER,
    segment_id VARCHAR,
    segment_type VARCHAR,
    polarity VARCHAR,
    from_node_id VARCHAR,
    to_node_id VARCHAR,
    module_id VARCHAR,
    from_x DOUBLE,
    from_y DOUBLE,
    from_z DOUBLE,
    to_x DOUBLE,
    to_y DOUBLE,
    to_z DOUBLE,
    displacement_m DOUBLE,
    conductor_length_m DOUBLE,
    separation_mm DOUBLE,
    formation VARCHAR,
    installation_class VARCHAR,
    conductor_product_id VARCHAR,
    conductor_csa_mm2 DOUBLE,
    conductor_diameter_mm DOUBLE,
    cable_od_mm DOUBLE,
    r20_ohm_per_m DOUBLE,
    temperature_c DOUBLE,
    effective_epsilon_r DOUBLE,
    loop_parameter_weight DOUBLE,
    coil_turns DOUBLE,
    coil_diameter_mm DOUBLE,
    connector_count INTEGER,
    connector_resistance_ohm_each DOUBLE,
    provenance VARCHAR,
    source_reference VARCHAR,
    user_override BOOLEAN,
    feasibility_status VARCHAR,
    saving_available BOOLEAN,
    warnings VARCHAR
)
"""

PAIR_FORMATIONS = (
    "'touching_pair', 'spaced_pair', 'bundled'"
)
EXTERNAL_TYPES = (
    "'external_positive_home_run', "
    "'external_negative_home_run', "
    "'external_sequential_row_return'"
)
FACTORY_TYPES = (
    "'module_factory_positive_lead', "
    "'module_factory_negative_lead'"
)


def _duckdb_module():
    try:
        import duckdb
    except ImportError as error:
        raise RuntimeError(
            "DuckDB is required for the fleet Parquet build"
        ) from error
    return duckdb


def _sql_path(path: Path) -> str:
    return path.resolve().as_posix().replace("'", "''")


def _csv_record(segment: SegmentRow) -> dict:
    return {
        key: NULL_TOKEN if value is None else value
        for key, value in segment.as_dict().items()
    }


def _write_segment_csv(
    inputs: TopologyInputs,
    path: Path,
) -> int:
    path.parent.mkdir(parents=True, exist_ok=True)
    row_count = 0

    with path.open("w", encoding="utf-8", newline="") as handle:
        writer = csv.DictWriter(
            handle,
            fieldnames=SEGMENT_COLUMNS,
            lineterminator="\n",
        )
        writer.writeheader()
        for segment in build_fleet_segments(inputs):
            writer.writerow(_csv_record(segment))
            row_count += 1

    return row_count


def _scalar(connection, query: str):
    return connection.execute(query).fetchone()[0]


def _run_data_law(connection) -> dict[str, int]:
    checks = {
        "empty_or_null_keys": _scalar(
            connection,
            """
            SELECT count(*)
            FROM segments
            WHERE coalesce(run_id, '') = ''
               OR coalesce(topology, '') = ''
               OR coalesce(string_id, '') = ''
               OR coalesce(segment_id, '') = ''
               OR band IS NULL
               OR segment_index IS NULL
            """,
        ),
        "duplicate_keys": _scalar(
            connection,
            """
            SELECT count(*)
            FROM (
                SELECT topology, string_id, segment_index
                FROM segments
                GROUP BY topology, string_id, segment_index
                HAVING count(*) <> 1
            )
            """,
        ),
        "non_contiguous_indices": _scalar(
            connection,
            """
            SELECT count(*)
            FROM (
                SELECT
                    topology,
                    string_id,
                    min(segment_index) AS first_index,
                    max(segment_index) AS last_index,
                    count(*) AS row_count,
                    count(DISTINCT segment_index) AS distinct_count
                FROM segments
                GROUP BY topology, string_id
            )
            WHERE first_index <> 1
               OR last_index <> row_count
               OR distinct_count <> row_count
            """,
        ),
        "discontinuous_node_chains": _scalar(
            connection,
            """
            WITH ordered AS (
                SELECT
                    topology,
                    string_id,
                    segment_index,
                    to_node_id,
                    lead(from_node_id) OVER (
                        PARTITION BY topology, string_id
                        ORDER BY segment_index
                    ) AS next_from_node_id
                FROM segments
            )
            SELECT count(*)
            FROM ordered
            WHERE next_from_node_id IS NOT NULL
              AND to_node_id <> next_from_node_id
            """,
        ),
        "negative_lengths": _scalar(
            connection,
            """
            SELECT count(*)
            FROM segments
            WHERE displacement_m < 0
               OR conductor_length_m < 0
            """,
        ),
        "invalid_loop_weights": _scalar(
            connection,
            """
            SELECT count(*)
            FROM segments
            WHERE loop_parameter_weight < 0
               OR loop_parameter_weight > 1
            """,
        ),
        "invalid_connector_resistance": _scalar(
            connection,
            """
            SELECT count(*)
            FROM segments
            WHERE connector_resistance_ohm_each < 0
            """,
        ),
        "invalid_provenance": _scalar(
            connection,
            """
            SELECT count(*)
            FROM segments
            WHERE provenance NOT IN (
                'measured',
                'oem_declared',
                'assumed',
                'defaulted'
            )
            """,
        ),
        "invalid_envelope_fill": _scalar(
            connection,
            """
            SELECT count(*)
            FROM segments
            WHERE conductor_csa_mm2
                    / (pi() * conductor_diameter_mm
                        * conductor_diameter_mm / 4) < 0.70
               OR conductor_csa_mm2
                    / (pi() * conductor_diameter_mm
                        * conductor_diameter_mm / 4) > 0.95
            """,
        ),
        "invalid_pair_geometry": _scalar(
            connection,
            f"""
            SELECT count(*)
            FROM segments
            WHERE loop_parameter_weight > 0
              AND formation IN ({PAIR_FORMATIONS})
              AND separation_mm <= conductor_diameter_mm
            """,
        ),
        "factory_lead_mismatch": _scalar(
            connection,
            f"""
            WITH totals AS (
                SELECT
                    topology,
                    string_id,
                    sum(conductor_length_m) AS factory_m
                FROM segments
                WHERE segment_type IN ({FACTORY_TYPES})
                GROUP BY topology, string_id
            ),
            paired AS (
                SELECT
                    string_id,
                    max(
                        CASE WHEN topology = 'sequential'
                        THEN factory_m END
                    ) AS sequential_m,
                    max(
                        CASE WHEN topology = 'leapfrog'
                        THEN factory_m END
                    ) AS leapfrog_m
                FROM totals
                GROUP BY string_id
            )
            SELECT count(*)
            FROM paired
            WHERE sequential_m IS NULL
               OR leapfrog_m IS NULL
               OR abs(sequential_m - leapfrog_m) > 1e-12
            """,
        ),
        "connector_mismatch": _scalar(
            connection,
            """
            WITH totals AS (
                SELECT
                    topology,
                    string_id,
                    sum(connector_count) AS contacts
                FROM segments
                WHERE segment_type <> 'extension_lead'
                GROUP BY topology, string_id
            ),
            paired AS (
                SELECT
                    string_id,
                    max(
                        CASE WHEN topology = 'sequential'
                        THEN contacts END
                    ) AS sequential_contacts,
                    max(
                        CASE WHEN topology = 'leapfrog'
                        THEN contacts END
                    ) AS leapfrog_contacts
                FROM totals
                GROUP BY string_id
            )
            SELECT count(*)
            FROM paired
            WHERE sequential_contacts IS NULL
               OR leapfrog_contacts IS NULL
               OR sequential_contacts <> leapfrog_contacts
            """,
        ),
        "infeasible_saving_claims": _scalar(
            connection,
            """
            SELECT count(*)
            FROM segments
            WHERE topology = 'leapfrog'
              AND feasibility_status = 'INFEASIBLE_LENGTH_SCREEN'
              AND saving_available
            """,
        ),
    }
    failed = {name: value for name, value in checks.items() if value}
    if failed:
        raise ValueError(f"Topology segment data law failed: {failed}")
    return checks


def _create_segment_results(connection) -> None:
    connection.execute(
        "CREATE OR REPLACE MACRO acosh(x) "
        "AS ln(x + sqrt(x * x - 1))"
    )
    connection.execute(
        f"""
        CREATE TABLE segment_results AS
        WITH geometry AS (
            SELECT
                *,
                CASE
                    WHEN loop_parameter_weight > 0
                     AND formation IN ({PAIR_FORMATIONS})
                     AND separation_mm > conductor_diameter_mm
                    THEN acosh(
                        separation_mm / conductor_diameter_mm
                    )
                END AS geometry_term
            FROM segments
        ),
        per_unit AS (
            SELECT
                *,
                conductor_length_m
                    * r20_ohm_per_m
                    * (1 + 0.00393 * (temperature_c - 20))
                    + connector_count
                    * connector_resistance_ohm_each
                    * (1 + 0.00393 * (temperature_c - 20))
                    AS operating_resistance_ohm,
                CASE
                    WHEN geometry_term IS NOT NULL
                    THEN 4e-7 * geometry_term
                END AS external_l_h_per_m,
                CASE
                    WHEN geometry_term IS NOT NULL
                    THEN 1e-7
                END AS internal_l_h_per_m,
                CASE
                    WHEN geometry_term IS NOT NULL
                    THEN pi() * 8.8541878128e-12
                        * effective_epsilon_r / geometry_term
                END AS differential_c_f_per_m
            FROM geometry
        )
        SELECT
            *,
            external_l_h_per_m
                * conductor_length_m
                * loop_parameter_weight AS external_l_h,
            internal_l_h_per_m
                * conductor_length_m
                * loop_parameter_weight AS internal_l_h,
            differential_c_f_per_m
                * conductor_length_m
                * loop_parameter_weight AS differential_c_f,
            CASE
                WHEN external_l_h_per_m IS NOT NULL
                THEN sqrt(
                    external_l_h_per_m
                    / differential_c_f_per_m
                )
            END AS characteristic_impedance_ohm,
            CASE
                WHEN external_l_h_per_m IS NOT NULL
                THEN 1 / sqrt(
                    external_l_h_per_m
                    * differential_c_f_per_m
                )
            END AS propagation_velocity_m_per_s
        FROM per_unit
        """
    )


def _copy_query(
    connection,
    query: str,
    target: Path,
    *,
    partitioned: bool = False,
) -> None:
    target.parent.mkdir(parents=True, exist_ok=True)
    path = _sql_path(target)
    if partitioned:
        connection.execute(
            f"""
            COPY ({query}) TO '{path}' (
                FORMAT parquet,
                COMPRESSION zstd,
                PARTITION_BY (topology, band),
                FILENAME_PATTERN 'data_{{i}}'
            )
            """
        )
        return

    connection.execute(
        f"""
        COPY ({query}) TO '{path}' (
            FORMAT parquet,
            COMPRESSION zstd
        )
        """
    )


def _write_aggregates(connection, root: Path) -> None:
    results = root / "results" / "segments"
    _copy_query(
        connection,
        """
        SELECT *
        FROM segment_results
        ORDER BY
            topology,
            band,
            inverter_id,
            string_id,
            segment_index
        """,
        results,
        partitioned=True,
    )

    aggregate_root = root / "aggregates"
    aggregate_root.mkdir(parents=True, exist_ok=True)

    string_query = f"""
        SELECT
            topology,
            inverter_id,
            mppt_id,
            string_id,
            min(band) AS band,
            count(*) AS segment_count,
            sum(displacement_m) AS route_displacement_m,
            sum(conductor_length_m) AS conductor_length_m,
            sum(operating_resistance_ohm) AS resistance_ohm,
            sum(coalesce(external_l_h, 0)) AS external_l_h,
            sum(coalesce(internal_l_h, 0)) AS internal_l_h,
            sum(coalesce(differential_c_f, 0)) AS differential_c_f,
            sum(connector_count) AS connector_count,
            sum(
                CASE
                    WHEN segment_type IN ({EXTERNAL_TYPES})
                    THEN conductor_length_m
                    ELSE 0
                END
            ) AS external_cable_m,
            sum(
                CASE
                    WHEN segment_type IN ({FACTORY_TYPES})
                    THEN conductor_length_m
                    ELSE 0
                END
            ) AS factory_lead_m,
            min(
                CASE WHEN saving_available THEN 1 ELSE 0 END
            ) = 1 AS saving_available
        FROM segment_results
        GROUP BY
            topology,
            inverter_id,
            mppt_id,
            string_id
    """
    connection.execute(
        f"CREATE TABLE string_aggregates AS {string_query}"
    )
    _copy_query(
        connection,
        "SELECT * FROM string_aggregates ORDER BY topology, string_id",
        aggregate_root / "strings.parquet",
    )

    connection.execute(
        """
        CREATE TABLE mppt_aggregates AS
        SELECT
            topology,
            inverter_id,
            mppt_id,
            count(*) AS string_count,
            sum(segment_count) AS segment_count,
            sum(conductor_length_m) AS conductor_length_m,
            sum(resistance_ohm) AS resistance_ohm,
            sum(external_cable_m) AS external_cable_m,
            min(CASE WHEN saving_available THEN 1 ELSE 0 END) = 1
                AS saving_available
        FROM string_aggregates
        GROUP BY topology, inverter_id, mppt_id
        """
    )
    _copy_query(
        connection,
        """
        SELECT *
        FROM mppt_aggregates
        ORDER BY topology, inverter_id, mppt_id
        """,
        aggregate_root / "mppts.parquet",
    )

    connection.execute(
        """
        CREATE TABLE inverter_aggregates AS
        SELECT
            topology,
            inverter_id,
            count(*) AS mppt_count,
            sum(string_count) AS string_count,
            sum(segment_count) AS segment_count,
            sum(conductor_length_m) AS conductor_length_m,
            sum(resistance_ohm) AS resistance_ohm,
            sum(external_cable_m) AS external_cable_m,
            min(CASE WHEN saving_available THEN 1 ELSE 0 END) = 1
                AS saving_available
        FROM mppt_aggregates
        GROUP BY topology, inverter_id
        """
    )
    _copy_query(
        connection,
        """
        SELECT *
        FROM inverter_aggregates
        ORDER BY topology, inverter_id
        """,
        aggregate_root / "inverters.parquet",
    )

    connection.execute(
        """
        CREATE TABLE site_aggregates AS
        SELECT
            topology,
            count(*) AS inverter_count,
            sum(string_count) AS string_count,
            sum(segment_count) AS segment_count,
            sum(conductor_length_m) AS conductor_length_m,
            sum(resistance_ohm) AS resistance_ohm,
            sum(external_cable_m) AS external_cable_m,
            min(CASE WHEN saving_available THEN 1 ELSE 0 END) = 1
                AS saving_available
        FROM inverter_aggregates
        GROUP BY topology
        """
    )
    _copy_query(
        connection,
        "SELECT * FROM site_aggregates ORDER BY topology",
        aggregate_root / "site.parquet",
    )

    connection.execute(
        """
        CREATE TABLE comparison_aggregate AS
        SELECT
            sequential.string_count,
            sequential.external_cable_m
                AS sequential_external_cable_m,
            leapfrog.external_cable_m
                AS leapfrog_external_cable_m_theoretical,
            sequential.external_cable_m
                - leapfrog.external_cable_m
                AS theoretical_saving_m,
            CASE
                WHEN leapfrog.saving_available
                THEN sequential.external_cable_m
                    - leapfrog.external_cable_m
            END AS available_saving_m,
            leapfrog.saving_available
        FROM site_aggregates AS sequential
        CROSS JOIN site_aggregates AS leapfrog
        WHERE sequential.topology = 'sequential'
          AND leapfrog.topology = 'leapfrog'
        """
    )
    _copy_query(
        connection,
        "SELECT * FROM comparison_aggregate",
        aggregate_root / "comparison.parquet",
    )


def _write_browser_slices(connection, root: Path) -> None:
    browser_root = root / "browser"
    browser_root.mkdir(parents=True, exist_ok=True)

    site_rows = connection.execute(
        """
        SELECT *
        FROM site_aggregates
        ORDER BY topology
        """
    ).fetchdf().to_dict("records")
    comparison_rows = connection.execute(
        "SELECT * FROM comparison_aggregate"
    ).fetchdf().to_dict("records")
    summary = {
        "schema_version": "topology_segments_v1",
        "site": site_rows,
        "comparison": comparison_rows,
    }
    (browser_root / "site-summary.json").write_text(
        json.dumps(summary, indent=2, sort_keys=True) + "\n",
        encoding="utf-8",
    )

    string_id = _scalar(
        connection,
        "SELECT min(string_id) FROM segments",
    )
    selected = connection.execute(
        """
        SELECT *
        FROM segment_results
        WHERE string_id = ?
        ORDER BY topology, segment_index
        """,
        [string_id],
    ).fetchdf().to_dict("records")
    (browser_root / "selected-string.json").write_text(
        json.dumps(
            {
                "schema_version": "topology_segments_v1",
                "string_id": string_id,
                "segments": selected,
            },
            indent=2,
            sort_keys=True,
        )
        + "\n",
        encoding="utf-8",
    )


def _sha256(path: Path) -> str:
    digest = hashlib.sha256()
    with path.open("rb") as handle:
        for chunk in iter(lambda: handle.read(1024 * 1024), b""):
            digest.update(chunk)
    return digest.hexdigest()


def _file_hashes(root: Path) -> dict[str, str]:
    return {
        path.relative_to(root).as_posix(): _sha256(path)
        for path in sorted(root.rglob("*"))
        if path.is_file()
    }


def _write_manifests(
    connection,
    root: Path,
    inputs: TopologyInputs,
    source_commit: str,
    data_law: dict[str, int],
) -> None:
    manifest_root = root / "manifests"
    manifest_root.mkdir(parents=True, exist_ok=True)
    input_hash = canonical_input_hash(inputs)

    for cartridge in INITIAL_CARTRIDGES:
        statistics = connection.execute(
            """
            SELECT
                count(*) AS row_count,
                count(DISTINCT string_id) AS string_count,
                min(segment_id) AS first_key,
                max(segment_id) AS last_key,
                min(feasibility_status) AS feasibility_status,
                count(
                    DISTINCT CASE WHEN warnings <> '' THEN warnings END
                ) AS warning_count
            FROM segments
            WHERE topology = ?
            """,
            [cartridge.name],
        ).fetchone()
        topology_files = {
            path.relative_to(root).as_posix(): _sha256(path)
            for path in sorted(root.rglob("*.parquet"))
            if f"topology={cartridge.name}" in path.as_posix()
        }
        parquet_digest = hashlib.sha256(
            json.dumps(
                topology_files,
                sort_keys=True,
                separators=(",", ":"),
            ).encode("utf-8")
        ).hexdigest()
        manifest = {
            "schema_version": "topology_segments_v1",
            "cartridge_name": cartridge.name,
            "cartridge_version": cartridge.version,
            "method_version": "duckdb_parquet_store_v1",
            "source_commit": source_commit,
            "input_hash": input_hash,
            "segment_row_count": statistics[0],
            "distinct_string_count": statistics[1],
            "first_segment_key": statistics[2],
            "last_segment_key": statistics[3],
            "parquet_files": topology_files,
            "parquet_sha256": parquet_digest,
            "feasibility_status": statistics[4],
            "warning_count": statistics[5],
            "data_law_result": "PASS",
            "data_law_checks": data_law,
        }
        target = (
            manifest_root
            / f"topology={cartridge.name}"
            / "manifest.json"
        )
        target.parent.mkdir(parents=True, exist_ok=True)
        target.write_text(
            json.dumps(manifest, indent=2, sort_keys=True) + "\n",
            encoding="utf-8",
        )


def build_store(
    inputs: TopologyInputs,
    output_root: Path,
    source_commit: str = "unknown",
) -> dict:
    """Build one deterministic candidate store at ``output_root``."""

    inputs.validate()
    output_root = Path(output_root)
    if output_root.exists():
        shutil.rmtree(output_root)
    output_root.mkdir(parents=True, exist_ok=True)

    duckdb = _duckdb_module()
    with tempfile.TemporaryDirectory(
        prefix="topology-segments-csv-"
    ) as temporary:
        csv_path = Path(temporary) / "segments.csv"
        generated_rows = _write_segment_csv(inputs, csv_path)
        connection = duckdb.connect()
        try:
            connection.execute("SET threads = 1")
            connection.execute("SET preserve_insertion_order = true")
            connection.execute(SEGMENT_SCHEMA_SQL)
            connection.execute(
                f"""
                COPY segments
                FROM '{_sql_path(csv_path)}' (
                    FORMAT csv,
                    HEADER true,
                    DELIMITER ',',
                    NULLSTR '{NULL_TOKEN}'
                )
                """
            )
            loaded_rows = _scalar(
                connection,
                "SELECT count(*) FROM segments",
            )
            if generated_rows != loaded_rows:
                raise ValueError(
                    "Generated CSV row count differs from DuckDB row count"
                )

            data_law = _run_data_law(connection)
            _create_segment_results(connection)
            _copy_query(
                connection,
                """
                SELECT *
                FROM segments
                ORDER BY
                    topology,
                    band,
                    inverter_id,
                    string_id,
                    segment_index
                """,
                output_root / "segments",
                partitioned=True,
            )
            _write_aggregates(connection, output_root)
            _write_browser_slices(connection, output_root)
            _write_manifests(
                connection,
                output_root,
                inputs,
                source_commit,
                data_law,
            )
        finally:
            connection.close()

    summary = {
        "input_hash": canonical_input_hash(inputs),
        "generated_segment_rows": generated_rows,
        "string_count": inputs.total_site_string_count,
        "inverter_count": inputs.inverter_count,
        "file_hashes": _file_hashes(output_root),
    }
    (output_root / "build-summary.json").write_text(
        json.dumps(summary, indent=2, sort_keys=True) + "\n",
        encoding="utf-8",
    )
    return summary


def build_deterministic_store(
    inputs: TopologyInputs,
    output_root: Path,
    source_commit: str = "unknown",
) -> dict:
    """Build twice, compare hashes and publish byte-identical output."""

    output_root = Path(output_root)
    with tempfile.TemporaryDirectory(
        prefix="topology-determinism-"
    ) as temporary:
        temporary_root = Path(temporary)
        first = temporary_root / "first"
        second = temporary_root / "second"
        first_summary = build_store(inputs, first, source_commit)
        build_store(inputs, second, source_commit)
        first_hashes = _file_hashes(first)
        second_hashes = _file_hashes(second)

        if first_hashes != second_hashes:
            missing_first = sorted(
                set(second_hashes) - set(first_hashes)
            )
            missing_second = sorted(
                set(first_hashes) - set(second_hashes)
            )
            changed = sorted(
                path
                for path in set(first_hashes) & set(second_hashes)
                if first_hashes[path] != second_hashes[path]
            )
            raise ValueError(
                "Nondeterministic topology build: "
                f"missing_first={missing_first}, "
                f"missing_second={missing_second}, "
                f"changed={changed}"
            )

        if output_root.exists():
            shutil.rmtree(output_root)
        shutil.copytree(first, output_root)

    result = dict(first_summary)
    result["deterministic"] = True
    result["file_hashes"] = _file_hashes(output_root)
    return result
