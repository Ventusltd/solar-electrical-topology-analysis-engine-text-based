"""Deterministic DuckDB persistence for canonical segment rows."""

from __future__ import annotations

from dataclasses import fields
import hashlib
import json
from pathlib import Path
from typing import Iterable

import duckdb

from .segments import SegmentRow


DUCKDB_SEGMENT_SCHEMA_VERSION = "globalgrid2050.solar-dc.duckdb-segments.v10.1"
_TABLE = "segment_rows"
_PRIMARY_KEY = ("run_id", "topology", "string_id", "segment_index")


def _sql_type(name: str) -> str:
    if name in {
        "band", "inverter_id", "mppt_id", "segment_index", "connector_count"
    }:
        return "BIGINT"
    if name in {"user_override", "saving_available"}:
        return "BOOLEAN"
    if name in {
        "from_x", "from_y", "from_z", "to_x", "to_y", "to_z",
        "displacement_m", "conductor_length_m", "separation_mm",
        "conductor_csa_mm2", "conductor_diameter_mm", "cable_od_mm",
        "r20_ohm_per_m", "temperature_c", "effective_epsilon_r",
        "loop_parameter_weight", "coil_turns", "coil_diameter_mm",
        "connector_resistance_ohm_each",
    }:
        return "DOUBLE"
    return "VARCHAR"


def create_segment_table(connection: duckdb.DuckDBPyConnection) -> None:
    columns = [f'"{field.name}" {_sql_type(field.name)}' for field in fields(SegmentRow)]
    primary = ", ".join(f'"{name}"' for name in _PRIMARY_KEY)
    connection.execute(
        f'CREATE TABLE IF NOT EXISTS {_TABLE} ({", ".join(columns)}, '
        f'PRIMARY KEY ({primary}))'
    )


def write_segment_rows(
    connection: duckdb.DuckDBPyConnection,
    rows: Iterable[SegmentRow],
) -> int:
    ordered = sorted(
        rows,
        key=lambda row: (row.run_id, row.topology, row.string_id, row.segment_index),
    )
    for row in ordered:
        row.validate()
    create_segment_table(connection)
    names = [field.name for field in fields(SegmentRow)]
    placeholders = ", ".join("?" for _ in names)
    quoted = ", ".join(f'"{name}"' for name in names)
    statement = f'INSERT INTO {_TABLE} ({quoted}) VALUES ({placeholders})'
    connection.executemany(
        statement,
        [[getattr(row, name) for name in names] for row in ordered],
    )
    return len(ordered)


def read_segment_rows(connection: duckdb.DuckDBPyConnection) -> tuple[SegmentRow, ...]:
    names = [field.name for field in fields(SegmentRow)]
    quoted = ", ".join(f'"{name}"' for name in names)
    result = connection.execute(
        f'SELECT {quoted} FROM {_TABLE} '
        'ORDER BY run_id, topology, string_id, segment_index'
    ).fetchall()
    rows = tuple(SegmentRow(**dict(zip(names, values, strict=True))) for values in result)
    for row in rows:
        row.validate()
    return rows


def segment_rows_payload(rows: Iterable[SegmentRow]) -> dict[str, object]:
    ordered = sorted(
        rows,
        key=lambda row: (row.run_id, row.topology, row.string_id, row.segment_index),
    )
    return {
        "schema_version": DUCKDB_SEGMENT_SCHEMA_VERSION,
        "rows": [row.as_dict() for row in ordered],
    }


def segment_rows_hash(rows: Iterable[SegmentRow]) -> str:
    encoded = json.dumps(
        segment_rows_payload(rows), sort_keys=True, separators=(",", ":")
    ).encode("utf-8")
    return f"sha256:{hashlib.sha256(encoded).hexdigest()}"


def export_segment_parquet(
    connection: duckdb.DuckDBPyConnection,
    destination: str | Path,
) -> Path:
    path = Path(destination)
    path.parent.mkdir(parents=True, exist_ok=True)
    escaped = str(path).replace("'", "''")
    connection.execute(
        f"COPY (SELECT * FROM {_TABLE} ORDER BY run_id, topology, string_id, "
        f"segment_index) TO '{escaped}' (FORMAT PARQUET, COMPRESSION ZSTD)"
    )
    return path


def read_segment_parquet(path: str | Path) -> tuple[SegmentRow, ...]:
    connection = duckdb.connect(":memory:")
    try:
        escaped = str(Path(path)).replace("'", "''")
        connection.execute(
            f"CREATE TABLE {_TABLE} AS SELECT * FROM read_parquet('{escaped}')"
        )
        return read_segment_rows(connection)
    finally:
        connection.close()
