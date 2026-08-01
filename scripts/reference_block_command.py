#!/usr/bin/env python3
"""Print the authoritative reference inverter-block JSON."""

from __future__ import annotations

import sys

import solar_topology as topology


def reference_block_json() -> str:
    receipt = topology.build_reference_inverter_block()
    topology.validate_inverter_block_receipt(receipt)
    return topology.inverter_block_json(receipt)


def main() -> int:
    sys.stdout.write(reference_block_json() + "\n")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
