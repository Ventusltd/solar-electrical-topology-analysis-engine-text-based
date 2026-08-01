#!/usr/bin/env python3
"""Print a versioned authoritative reference inverter-block response."""

from __future__ import annotations

import argparse
import sys

import solar_topology as topology


REFERENCE_BLOCK_COMMAND_VERSION = (
    "globalgrid2050.solar-dc.reference-block-command.v1"
)


def reference_block_json(strategy: str = "leapfrog") -> str:
    receipt = topology.build_reference_inverter_block(strategy=strategy)
    topology.validate_inverter_block_receipt(receipt)
    return topology.inverter_block_json(receipt)


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(
        description="Emit authoritative reference inverter-block JSON.",
    )
    parser.add_argument(
        "--strategy",
        choices=("leapfrog", "sequential"),
        default="leapfrog",
    )
    parser.add_argument(
        "--version",
        action="version",
        version=REFERENCE_BLOCK_COMMAND_VERSION,
    )
    return parser


def main(argv: list[str] | None = None) -> int:
    args = build_parser().parse_args(argv)
    sys.stdout.write(reference_block_json(args.strategy) + "\n")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
