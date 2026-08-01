from __future__ import annotations

import hashlib
import json
from pathlib import Path

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
    basis = dict(payload)
    response_hash = basis.pop("response_hash")
    recomputed = "sha256:" + hashlib.sha256(
        canonical_json(basis).encode("utf-8")
    ).hexdigest()

    assert response_hash == recomputed
    assert payload["strategy"] == "leapfrog"
    block = payload["inverter_block"]
    build025 = payload["build025"]
    assert block["receipt_hash"] == build025["receipt_hash"] or (
        block["table_receipts"][0]["build025_receipt_hash"]
        == build025["receipt_hash"]
    )
    assert block["table_receipts"][0]["geometry_hash"] == (
        build025["geometry"]["geometry_hash"]
    )
    assert block["table_receipts"][0]["routing_hash"] == (
        build025["routing"]["routing_hash"]
    )
    assert json.loads(authority_response_json()) == payload
