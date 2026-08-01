#!/usr/bin/env python3
"""Generate the deterministic reference inverter-block authority bundle."""

from __future__ import annotations

import argparse
import hashlib
import json
from pathlib import Path
import sys

import solar_topology as topology
import solar_topology.array as array_topology

from scripts.reference_block_command import REFERENCE_BLOCK_COMMAND_VERSION


ROOT = Path(__file__).resolve().parents[1]
AUTHORITY_RESPONSE_SCHEMA_VERSION = (
    "globalgrid2050.solar-dc.authority-response.v1"
)
AUTHORITY_BUNDLE_PATH = (
    ROOT / "authority-bundles" / "reference-inverter-block.json"
)


def canonical_json(payload: object) -> str:
    return json.dumps(
        payload,
        sort_keys=True,
        separators=(",", ":"),
        ensure_ascii=False,
    )


def authority_response_payload(strategy: str = "leapfrog") -> dict[str, object]:
    block = topology.build_reference_inverter_block(strategy=strategy)
    topology.validate_inverter_block_receipt(block)
    if len(block.table_receipts) != 1:
        raise ValueError("reference authority bundle requires one child Build 025 receipt")
    child = block.table_receipts[0]
    basis: dict[str, object] = {
        "schema_version": AUTHORITY_RESPONSE_SCHEMA_VERSION,
        "command_version": REFERENCE_BLOCK_COMMAND_VERSION,
        "strategy": strategy,
        "inverter_block": topology.inverter_block_payload(block),
        "build025": array_topology.build025_payload(child),
    }
    response_hash = "sha256:" + hashlib.sha256(
        canonical_json(basis).encode("utf-8")
    ).hexdigest()
    return {**basis, "response_hash": response_hash}


def authority_response_json(strategy: str = "leapfrog") -> str:
    return canonical_json(authority_response_payload(strategy))


def write_authority_bundle(
    path: Path = AUTHORITY_BUNDLE_PATH,
    *,
    strategy: str = "leapfrog",
) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(authority_response_json(strategy) + "\n", encoding="utf-8")


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument(
        "--strategy",
        choices=("leapfrog", "sequential"),
        default="leapfrog",
    )
    parser.add_argument("--write", action="store_true")
    parser.add_argument("--output", type=Path, default=AUTHORITY_BUNDLE_PATH)
    args = parser.parse_args(argv)

    if args.write:
        write_authority_bundle(args.output, strategy=args.strategy)
    else:
        sys.stdout.write(authority_response_json(args.strategy) + "\n")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
