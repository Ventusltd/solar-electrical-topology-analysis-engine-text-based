from __future__ import annotations

import solar_topology as api
import solar_topology.inverter_block as authority


PUBLIC_NAMES = (
    "INVERTER_BLOCK_SCHEMA_VERSION",
    "REFERENCE_INVERTER_BLOCK_ID",
    "InverterBlockEvidenceState",
    "InverterBlockReceipt",
    "build_inverter_block",
    "build_reference_inverter_block",
    "inverter_block_hash",
    "inverter_block_json",
    "inverter_block_payload",
    "validate_inverter_block_receipt",
)

IDENTITY_NAMES = (
    "InverterBlockEvidenceState",
    "InverterBlockReceipt",
    "build_inverter_block",
    "build_reference_inverter_block",
    "inverter_block_hash",
    "inverter_block_json",
    "inverter_block_payload",
    "validate_inverter_block_receipt",
)


def test_inverter_block_contract_is_exposed_by_supported_package_api() -> None:
    assert api.INVERTER_BLOCK_SCHEMA_VERSION == authority.INVERTER_BLOCK_SCHEMA_VERSION
    assert api.REFERENCE_INVERTER_BLOCK_ID == authority.REFERENCE_INVERTER_BLOCK_ID
    for name in IDENTITY_NAMES:
        assert getattr(api, name) is getattr(authority, name)
    assert all(name in api.__all__ for name in PUBLIC_NAMES)


def test_inverter_block_exports_are_explicitly_provisional() -> None:
    classified = api.explicitly_classified_public_names()
    for name in PUBLIC_NAMES:
        assert api.public_api_status(name) is api.ApiStatus.PROVISIONAL
        assert name in classified


def test_top_level_inverter_block_reproduces_authority_payload_and_hash() -> None:
    public_receipt = api.build_reference_inverter_block()
    authority_receipt = authority.build_reference_inverter_block()

    assert public_receipt == authority_receipt
    assert api.inverter_block_payload(public_receipt) == (
        authority.inverter_block_payload(authority_receipt)
    )
    assert api.inverter_block_json(public_receipt) == (
        authority.inverter_block_json(authority_receipt)
    )
    assert api.inverter_block_hash(public_receipt) == (
        authority.inverter_block_hash(authority_receipt)
    )
