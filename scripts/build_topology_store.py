#!/usr/bin/env python3
"""Build the deterministic topology segment store."""

from __future__ import annotations

import argparse
import json
import os
from pathlib import Path

from solar_topology.parquet_store import build_deterministic_store
from solar_topology.segments import TopologyInputs


def parse_bands(value: str) -> tuple[int, ...]:
    parts = tuple(
        int(part.strip())
        for part in value.split(",")
        if part.strip()
    )
    if not parts or any(part < 1 for part in parts):
        raise argparse.ArgumentTypeError(
            "Bands must be a comma-separated list of positive integers"
        )
    return parts


def parser() -> argparse.ArgumentParser:
    result = argparse.ArgumentParser(
        description=(
            "Build zstd-compressed Hive-partitioned topology Parquet twice "
            "and fail if the outputs are not byte-identical."
        )
    )
    result.add_argument(
        "--output",
        type=Path,
        default=Path("data/topology/current"),
    )
    result.add_argument("--inverter-count", type=int, default=795)
    result.add_argument("--string-count", type=int, default=18_918)
    result.add_argument("--east-bands", type=parse_bands, default=(5, 5, 2))
    result.add_argument("--west-bands", type=parse_bands, default=(5, 5, 2))
    result.add_argument(
        "--positive-factory-lead-m",
        type=float,
        default=0.350,
    )
    result.add_argument(
        "--negative-factory-lead-m",
        type=float,
        default=0.280,
    )
    result.add_argument(
        "--measured-leapfrog-span-m",
        type=float,
        default=None,
    )
    result.add_argument(
        "--source-commit",
        default=os.environ.get("GITHUB_SHA", "unknown"),
    )
    result.add_argument(
        "--fixture",
        action="store_true",
        help="Build a small 47-string, two-inverter passing fixture.",
    )
    return result


def main() -> int:
    arguments = parser().parse_args()
    if arguments.fixture:
        arguments.inverter_count = 2
        arguments.string_count = 47
        arguments.positive_factory_lead_m = 1.4
        arguments.negative_factory_lead_m = 1.4

    inputs = TopologyInputs(
        inverter_count=arguments.inverter_count,
        total_site_string_count=arguments.string_count,
        east_bands=arguments.east_bands,
        west_bands=arguments.west_bands,
        positive_factory_lead_m=arguments.positive_factory_lead_m,
        negative_factory_lead_m=arguments.negative_factory_lead_m,
        measured_leapfrog_span_m=(
            arguments.measured_leapfrog_span_m
        ),
    )
    summary = build_deterministic_store(
        inputs,
        arguments.output,
        source_commit=arguments.source_commit,
    )
    print(json.dumps(summary, indent=2, sort_keys=True))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
