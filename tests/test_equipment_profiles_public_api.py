from __future__ import annotations

import solar_topology as api
import solar_topology.equipment_profiles as profiles


PUBLIC_NAMES = (
    "EQUIPMENT_PROFILE_SCHEMA_VERSION",
    "GENERIC_REFERENCE_CONTRACT_REVISION",
    "GENERIC_REFERENCE_EQUIPMENT_CONTRACT",
    "ConnectorCompatibilityState",
    "ConnectorEquipmentProfile",
    "DcInputProfile",
    "FactoryLeadSetProfile",
    "FieldConductorProfile",
    "InternalDcTopology",
    "InverterEquipmentProfile",
    "ModuleEquipmentProfile",
    "ModuleTechnology",
    "QualifiedValue",
    "ReferenceEquipmentContract",
    "ReverseCurrentBlockingState",
    "build_generic_reference_equipment_contract",
    "reference_equipment_contract_hash",
    "reference_equipment_contract_json",
    "reference_equipment_contract_payload",
    "reference_equipment_missing_evidence",
    "validate_reference_equipment_contract",
)


def test_equipment_contract_is_exposed_by_supported_package_api() -> None:
    assert api.EQUIPMENT_PROFILE_SCHEMA_VERSION == (
        profiles.EQUIPMENT_PROFILE_SCHEMA_VERSION
    )
    assert api.GENERIC_REFERENCE_EQUIPMENT_CONTRACT is (
        profiles.GENERIC_REFERENCE_EQUIPMENT_CONTRACT
    )
    assert api.ReferenceEquipmentContract is profiles.ReferenceEquipmentContract
    assert api.build_generic_reference_equipment_contract is (
        profiles.build_generic_reference_equipment_contract
    )
    assert api.reference_equipment_contract_hash is (
        profiles.reference_equipment_contract_hash
    )
    assert all(name in api.__all__ for name in PUBLIC_NAMES)


def test_equipment_contract_exports_are_explicitly_provisional() -> None:
    classified = api.explicitly_classified_public_names()
    for name in PUBLIC_NAMES:
        assert api.public_api_status(name) is api.ApiStatus.PROVISIONAL
        assert name in classified


def test_top_level_equipment_contract_reproduces_exact_authority_output() -> None:
    contract = api.build_generic_reference_equipment_contract()
    authority = profiles.build_generic_reference_equipment_contract()

    assert contract == authority
    assert api.reference_equipment_contract_payload(contract) == (
        profiles.reference_equipment_contract_payload(authority)
    )
    assert api.reference_equipment_contract_json(contract) == (
        profiles.reference_equipment_contract_json(authority)
    )
    assert api.reference_equipment_contract_hash(contract) == (
        profiles.reference_equipment_contract_hash(authority)
    )
    assert api.reference_equipment_missing_evidence(contract) == (
        profiles.reference_equipment_missing_evidence(authority)
    )
