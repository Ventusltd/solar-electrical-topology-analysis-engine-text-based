from __future__ import annotations

import hashlib
import json
from pathlib import Path

import solar_topology as topology

from scripts.build_authority_bundle import (
    AUTHORITY_BUNDLE_PATH,
    authority_response_json,
    authority_response_payload,
    canonical_json,
)


ROOT = Path(__file__).resolve().parents[1]
CANDIDATE_PATH = (
    ROOT / ".microbuild" / "candidates" / "reference-inverter-block.json"
)


def test_authority_bundle_regeneration_matches_committed_file_exactly() -> None:
    committed = AUTHORITY_BUNDLE_PATH.read_text(encoding="utf-8")
    expected = authority_response_json() + "\n"

    assert committed == expected


def test_authority_bundle_regeneration_candidate_matches_generator() -> None:
    assert CANDIDATE_PATH.is_file()
    assert CANDIDATE_PATH.read_text(encoding="utf-8") == (
        authority_response_json() + "\n"
    )


def test_authority_bundle_regeneration_binds_receipts_and_hash() -> None:
    payload = authority_response_payload()
    authority = topology.build_reference_inverter_block()
    basis = dict(payload)
    response_hash = basis.pop("response_hash")
    recomputed = "sha256:" + hashlib.sha256(
        canonical_json(basis).encode("utf-8")
    ).hexdigest()

    assert response_hash == recomputed
    assert payload["strategy"] == "leapfrog"
    block = payload["inverter_block"]
    build025 = payload["build025"]
    binding = block["table_receipts"][0]
    child = authority.table_receipts[0]

    assert binding["build025_receipt_hash"] == build025["receipt_hash"]
    assert binding["build025_receipt_hash"] == child.receipt_hash
    assert binding["geometry_hash"] == build025["geometry"]["geometry_hash"]
    assert binding["geometry_hash"] == child.geometry.geometry_hash
    assert binding["routing_hash"] == child.routing.routing_hash
    assert build025["routing"]["table_id"] == child.routing.table_id
    assert len(build025["routing"]["string_routes"]) == 24
    assert json.loads(authority_response_json()) == payload
