from __future__ import annotations

from copy import deepcopy
import hashlib
import json
from pathlib import Path

import pytest
import solar_topology as topology

from scripts.build_authority_bundle import (
    AUTHORITY_BUNDLE_PATH,
    authority_response_json,
    authority_response_payload,
    canonical_json,
)
from scripts.validate_authority_bundle import (
    AUTHORITY_RESPONSE_SCHEMA_PATH,
    AuthorityBundleValidationError,
    load_json_object,
    validate_authority_bundle_file,
    validate_authority_bundle_payload,
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
    assert json.loads(authority_response_json()) == payload


def test_bundle_schema_accepts_canonical_reference_authority() -> None:
    schema = load_json_object(AUTHORITY_RESPONSE_SCHEMA_PATH)
    summary = validate_authority_bundle_file()

    assert schema["$schema"] == "https://json-schema.org/draft/2020-12/schema"
    assert schema["properties"]["schema_version"]["const"] == (
        "globalgrid2050.solar-dc.authority-response.v1"
    )
    assert summary["pass"] is True
    assert summary["strategy"] == "leapfrog"
    assert summary["module_count"] == 720
    assert summary["string_count"] == 24
    assert summary["modules_per_string"] == 30
    assert summary["dc_nameplate_power_kwp"] == 475.2
    assert summary["inverter_apparent_power_kva"] == 352.0
    assert summary["evidence_state"] == "incomplete_evidence"
    assert summary["missing_evidence_count"] == 47


@pytest.mark.parametrize(
    "path",
    (
        ("response_hash",),
        ("inverter_block", "receipt_hash"),
        ("build025", "receipt_hash"),
        ("inverter_block", "table_receipts", 0, "routing_hash"),
    ),
)
def test_bundle_schema_rejects_missing_authority_hashes(
    path: tuple[str | int, ...],
) -> None:
    payload = deepcopy(authority_response_payload())
    target: object = payload
    for part in path[:-1]:
        target = target[part]  # type: ignore[index]
    del target[path[-1]]  # type: ignore[index]

    with pytest.raises(AuthorityBundleValidationError, match="missing required fields"):
        validate_authority_bundle_payload(payload)


@pytest.mark.parametrize(
    ("field", "invented"),
    (
        ("mppt_count", 12),
        ("mppt_count_verification_state", "verified"),
        ("mppt_mapping_verification_states", ["verified"]),
        ("internal_dc_topology", "common_bus"),
        ("reverse_current_blocking", "present"),
        ("pce_backfeed_current_a", 1.0),
        ("routing_fixture_mppt_labels_are_equipment_evidence", True),
    ),
)
def test_bundle_schema_rejects_invented_input_evidence(
    field: str,
    invented: object,
) -> None:
    payload = deepcopy(authority_response_payload())
    payload["inverter_block"]["input_authority"][field] = invented

    with pytest.raises(AuthorityBundleValidationError):
        validate_authority_bundle_payload(payload)


def test_bundle_schema_rejects_changed_product_boundary_arithmetic() -> None:
    payload = deepcopy(authority_response_payload())
    payload["inverter_block"]["product_boundary"][
        "dc_nameplate_power_kwp"
    ] = 475.3

    with pytest.raises(
        AuthorityBundleValidationError,
        match="dc_nameplate_power_kwp must equal 475.2",
    ):
        validate_authority_bundle_payload(payload)


def test_bundle_schema_rejects_tampered_response_hash() -> None:
    payload = deepcopy(authority_response_payload())
    payload["response_hash"] = "sha256:" + "0" * 64

    with pytest.raises(AuthorityBundleValidationError, match="response_hash"):
        validate_authority_bundle_payload(payload)


def test_bundle_schema_rejects_broken_child_hash_binding() -> None:
    payload = deepcopy(authority_response_payload())
    payload["inverter_block"]["table_receipts"][0]["routing_hash"] = (
        "sha256:" + "1" * 64
    )
    basis = dict(payload)
    basis.pop("response_hash")
    payload["response_hash"] = "sha256:" + hashlib.sha256(
        canonical_json(basis).encode("utf-8")
    ).hexdigest()

    with pytest.raises(AuthorityBundleValidationError, match="routing hash binding"):
        validate_authority_bundle_payload(payload)
