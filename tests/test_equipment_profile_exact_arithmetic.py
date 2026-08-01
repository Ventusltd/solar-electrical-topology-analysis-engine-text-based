from __future__ import annotations

from solar_topology.equipment_profiles import (
    GENERIC_REFERENCE_EQUIPMENT_CONTRACT,
    reference_equipment_contract_json,
    reference_equipment_contract_payload,
)


def test_reference_block_payload_uses_exact_declared_decimal_values() -> None:
    contract = GENERIC_REFERENCE_EQUIPMENT_CONTRACT
    block = reference_equipment_contract_payload(contract)["reference_block"]

    assert contract.string_rated_power_kwp == 19.8
    assert contract.dc_nameplate_power_kwp == 475.2
    assert contract.dc_ac_nameplate_ratio == 1.35
    assert block["string_rated_power_kwp"] == 19.8
    assert block["dc_nameplate_power_kwp"] == 475.2
    assert block["dc_ac_nameplate_ratio"] == 1.35
    serialised = reference_equipment_contract_json(contract)
    assert '"dc_nameplate_power_kwp":475.2' in serialised
    assert "475.20000000000005" not in serialised
