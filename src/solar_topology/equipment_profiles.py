"""Generic, evidence-qualified equipment profiles for the reference inverter block.

The profiles in this module deliberately contain no manufacturer or project names.
Known programme-fixture values are separated from unresolved equipment facts. The
module defines data and deterministic serialisation only; it does not change
geometry, topology, routing, electrical calculations or existing receipt hashes.
"""

from __future__ import annotations

from dataclasses import dataclass
from enum import StrEnum
import hashlib
import json
import math
from typing import TypeAlias

from .circuit import EvidenceClass
from .evidence import VerificationState
from .products import EXTERNAL_STRING_6MM2, FACTORY_LEAD_4MM2
from .resistance_qualification import (
    ResistanceSourceStatus,
    assess_resistance_source,
)


EQUIPMENT_PROFILE_SCHEMA_VERSION = (
    "globalgrid2050.solar-dc.equipment-profile.v1"
)
GENERIC_REFERENCE_CONTRACT_REVISION = "2026-08-01.1"

ScalarValue: TypeAlias = str | int | float | bool | None


class ModuleTechnology(StrEnum):
    BIFACIAL = "bifacial"


class InternalDcTopology(StrEnum):
    UNKNOWN = "unknown"
    INDEPENDENT_INPUTS = "independent_inputs"
    SHARED_DC_BUS = "shared_dc_bus"
    MIXED = "mixed"


class ReverseCurrentBlockingState(StrEnum):
    UNKNOWN = "unknown"
    PRESENT = "present"
    ABSENT = "absent"


class ConnectorCompatibilityState(StrEnum):
    UNKNOWN = "unknown"
    DECLARED_COMPATIBLE = "declared_compatible"
    DECLARED_INCOMPATIBLE = "declared_incompatible"


@dataclass(frozen=True)
class QualifiedValue:
    """One scalar value with explicit evidence and source qualification."""

    value: ScalarValue
    unit: str | None
    evidence_class: EvidenceClass
    verification_state: VerificationState
    source_reference: str | None
    source_revision: str | None
    note: str | None = None

    @property
    def resolved(self) -> bool:
        return self.value is not None

    @property
    def verified(self) -> bool:
        return self.resolved and self.verification_state is VerificationState.VERIFIED

    def validate(self) -> None:
        if self.unit is not None and not self.unit.strip():
            raise ValueError("qualified-value unit cannot be blank")
        if self.source_reference is not None and not self.source_reference.strip():
            raise ValueError("qualified-value source_reference cannot be blank")
        if self.source_revision is not None and not self.source_revision.strip():
            raise ValueError("qualified-value source_revision cannot be blank")
        if self.value is None and self.verification_state is VerificationState.VERIFIED:
            raise ValueError("an unresolved qualified value cannot be verified")
        if self.value is not None and isinstance(self.value, float):
            if not math.isfinite(self.value):
                raise ValueError("qualified numeric value must be finite")


@dataclass(frozen=True)
class ModuleEquipmentProfile:
    profile_id: str
    revision: str
    technology: QualifiedValue
    rated_power_wp: QualifiedValue
    voc_v: QualifiedValue
    isc_a: QualifiedValue
    vmp_v: QualifiedValue
    imp_a: QualifiedValue
    maximum_overcurrent_protection_rating_a: QualifiedValue
    bifaciality_factor: QualifiedValue
    width_m: QualifiedValue
    length_m: QualifiedValue


@dataclass(frozen=True)
class DcInputProfile:
    input_id: str
    positive_terminal_id: str
    negative_terminal_id: str
    mppt_id: QualifiedValue


@dataclass(frozen=True)
class InverterEquipmentProfile:
    profile_id: str
    revision: str
    apparent_power_kva: QualifiedValue
    physical_dc_input_count: QualifiedValue
    dc_inputs: tuple[DcInputProfile, ...]
    mppt_count: QualifiedValue
    internal_dc_topology: QualifiedValue
    reverse_current_blocking: QualifiedValue
    pce_backfeed_current_a: QualifiedValue
    maximum_dc_voltage_v: QualifiedValue
    maximum_dc_input_power_kwp: QualifiedValue


@dataclass(frozen=True)
class ConnectorEquipmentProfile:
    profile_id: str
    revision: str
    contact_resistance_ohm_per_mated_pair: QualifiedValue
    rated_current_a: QualifiedValue
    rated_voltage_v: QualifiedValue
    mating_compatibility: QualifiedValue


@dataclass(frozen=True)
class FactoryLeadSetProfile:
    profile_id: str
    revision: str
    conductor_product_id: str
    connector_profile_id: str
    positive_lead_length_m: QualifiedValue
    negative_lead_length_m: QualifiedValue


@dataclass(frozen=True)
class FieldConductorProfile:
    profile_id: str
    revision: str
    conductor_product_id: str
    installation_class: QualifiedValue


@dataclass(frozen=True)
class ReferenceEquipmentContract:
    contract_id: str
    revision: str
    module: ModuleEquipmentProfile
    inverter: InverterEquipmentProfile
    connector: ConnectorEquipmentProfile
    factory_leads: FactoryLeadSetProfile
    field_conductor: FieldConductorProfile
    modules_per_string: int
    string_count: int
    schema_version: str = EQUIPMENT_PROFILE_SCHEMA_VERSION

    @property
    def module_count(self) -> int:
        return self.modules_per_string * self.string_count

    @property
    def string_rated_power_kwp(self) -> float:
        value = self.module.rated_power_wp.value
        if not isinstance(value, (int, float)):
            raise ValueError("module rated power is unresolved")
        return float(value) * self.modules_per_string / 1000.0

    @property
    def dc_nameplate_power_kwp(self) -> float:
        return self.string_rated_power_kwp * self.string_count

    @property
    def dc_ac_nameplate_ratio(self) -> float:
        value = self.inverter.apparent_power_kva.value
        if not isinstance(value, (int, float)):
            raise ValueError("inverter apparent power is unresolved")
        return self.dc_nameplate_power_kwp / float(value)


def _known(value: ScalarValue, unit: str | None) -> QualifiedValue:
    return QualifiedValue(
        value=value,
        unit=unit,
        evidence_class=EvidenceClass.USER_CREATED,
        verification_state=VerificationState.VERIFIED,
        source_reference="product_owner_reference_fixture",
        source_revision="2026-08-01",
        note="Verified as the generic programme fixture, not as a manufacturer certification.",
    )


def _unknown(unit: str | None, note: str) -> QualifiedValue:
    return QualifiedValue(
        value=None,
        unit=unit,
        evidence_class=EvidenceClass.ASSUMED,
        verification_state=VerificationState.UNKNOWN,
        source_reference=None,
        source_revision=None,
        note=note,
    )


def _unknown_enum(enum_value: StrEnum, note: str) -> QualifiedValue:
    return QualifiedValue(
        value=str(enum_value),
        unit=None,
        evidence_class=EvidenceClass.ASSUMED,
        verification_state=VerificationState.UNKNOWN,
        source_reference=None,
        source_revision=None,
        note=note,
    )


def _dc_inputs(count: int) -> tuple[DcInputProfile, ...]:
    return tuple(
        DcInputProfile(
            input_id=f"dc_input_{index:02d}",
            positive_terminal_id=f"dc_input_{index:02d}_positive",
            negative_terminal_id=f"dc_input_{index:02d}_negative",
            mppt_id=_unknown(
                None,
                "Physical-input-to-MPPT control relationship requires evidence.",
            ),
        )
        for index in range(1, count + 1)
    )


def build_generic_reference_equipment_contract() -> ReferenceEquipmentContract:
    """Build the fixed generic contract for the first complete product boundary."""

    connector_profile_id = "generic_pv_connector_unresolved"
    module = ModuleEquipmentProfile(
        profile_id="generic_bifacial_module_660wp",
        revision=GENERIC_REFERENCE_CONTRACT_REVISION,
        technology=_known(str(ModuleTechnology.BIFACIAL), None),
        rated_power_wp=_known(660.0, "Wp"),
        voc_v=_unknown("V", "Open-circuit voltage requires source evidence."),
        isc_a=_unknown("A", "Short-circuit current requires source evidence."),
        vmp_v=_unknown("V", "Maximum-power voltage requires source evidence."),
        imp_a=_unknown("A", "Maximum-power current requires source evidence."),
        maximum_overcurrent_protection_rating_a=_unknown(
            "A",
            "Module maximum overcurrent protection rating requires source evidence.",
        ),
        bifaciality_factor=_unknown(
            None,
            "Bifaciality factor requires source evidence.",
        ),
        width_m=_unknown("m", "Module width requires dimensional evidence."),
        length_m=_unknown("m", "Module length requires dimensional evidence."),
    )
    inverter = InverterEquipmentProfile(
        profile_id="generic_string_inverter_352kva_24_input",
        revision=GENERIC_REFERENCE_CONTRACT_REVISION,
        apparent_power_kva=_known(352.0, "kVA"),
        physical_dc_input_count=_known(24, None),
        dc_inputs=_dc_inputs(24),
        mppt_count=_unknown(
            None,
            "MPPT count and input grouping require source evidence.",
        ),
        internal_dc_topology=_unknown_enum(
            InternalDcTopology.UNKNOWN,
            "Internal DC topology is not inferred from input or MPPT labels.",
        ),
        reverse_current_blocking=_unknown_enum(
            ReverseCurrentBlockingState.UNKNOWN,
            "Reverse-current blocking requires source evidence.",
        ),
        pce_backfeed_current_a=_unknown(
            "A",
            "PCE backfeed current requires source evidence.",
        ),
        maximum_dc_voltage_v=_unknown(
            "V",
            "Maximum DC voltage requires source evidence.",
        ),
        maximum_dc_input_power_kwp=_unknown(
            "kWp",
            "Maximum DC input power requires source evidence; the 475.2 kWp value is the reference block nameplate, not an inferred equipment limit.",
        ),
    )
    connector = ConnectorEquipmentProfile(
        profile_id=connector_profile_id,
        revision=GENERIC_REFERENCE_CONTRACT_REVISION,
        contact_resistance_ohm_per_mated_pair=_unknown(
            "ohm",
            "Contact resistance requires revision-controlled evidence or measurement.",
        ),
        rated_current_a=_unknown("A", "Connector current rating requires source evidence."),
        rated_voltage_v=_unknown("V", "Connector voltage rating requires source evidence."),
        mating_compatibility=_unknown_enum(
            ConnectorCompatibilityState.UNKNOWN,
            "Connector family and mating compatibility remain unresolved.",
        ),
    )
    factory_leads = FactoryLeadSetProfile(
        profile_id="generic_module_factory_lead_set",
        revision=GENERIC_REFERENCE_CONTRACT_REVISION,
        conductor_product_id=FACTORY_LEAD_4MM2.product_id,
        connector_profile_id=connector_profile_id,
        positive_lead_length_m=_unknown(
            "m",
            "Positive factory-lead length requires source or measured evidence.",
        ),
        negative_lead_length_m=_unknown(
            "m",
            "Negative factory-lead length requires source or measured evidence.",
        ),
    )
    field_conductor = FieldConductorProfile(
        profile_id="generic_external_string_conductor",
        revision=GENERIC_REFERENCE_CONTRACT_REVISION,
        conductor_product_id=EXTERNAL_STRING_6MM2.product_id,
        installation_class=_unknown(
            None,
            "Installation class is route-segment evidence and remains unresolved here.",
        ),
    )
    contract = ReferenceEquipmentContract(
        contract_id="generic_352kva_475_2kwp_reference_equipment",
        revision=GENERIC_REFERENCE_CONTRACT_REVISION,
        module=module,
        inverter=inverter,
        connector=connector,
        factory_leads=factory_leads,
        field_conductor=field_conductor,
        modules_per_string=30,
        string_count=24,
    )
    validate_reference_equipment_contract(contract)
    return contract


def _qualified_value_payload(item: QualifiedValue) -> dict[str, object]:
    item.validate()
    return {
        "value": item.value,
        "unit": item.unit,
        "evidence_class": str(item.evidence_class),
        "verification_state": str(item.verification_state),
        "source_reference": item.source_reference,
        "source_revision": item.source_revision,
        "note": item.note,
    }


def reference_equipment_contract_payload(
    contract: ReferenceEquipmentContract,
) -> dict[str, object]:
    """Return deterministic equipment-contract data without runtime metadata."""

    validate_reference_equipment_contract(contract)
    module = contract.module
    inverter = contract.inverter
    connector = contract.connector
    factory_leads = contract.factory_leads
    field_conductor = contract.field_conductor
    return {
        "schema_version": contract.schema_version,
        "contract_id": contract.contract_id,
        "revision": contract.revision,
        "reference_block": {
            "modules_per_string": contract.modules_per_string,
            "string_count": contract.string_count,
            "module_count": contract.module_count,
            "string_rated_power_kwp": contract.string_rated_power_kwp,
            "dc_nameplate_power_kwp": contract.dc_nameplate_power_kwp,
            "inverter_apparent_power_kva": inverter.apparent_power_kva.value,
            "dc_ac_nameplate_ratio": contract.dc_ac_nameplate_ratio,
        },
        "module": {
            "profile_id": module.profile_id,
            "revision": module.revision,
            "technology": _qualified_value_payload(module.technology),
            "rated_power_wp": _qualified_value_payload(module.rated_power_wp),
            "voc_v": _qualified_value_payload(module.voc_v),
            "isc_a": _qualified_value_payload(module.isc_a),
            "vmp_v": _qualified_value_payload(module.vmp_v),
            "imp_a": _qualified_value_payload(module.imp_a),
            "maximum_overcurrent_protection_rating_a": _qualified_value_payload(
                module.maximum_overcurrent_protection_rating_a
            ),
            "bifaciality_factor": _qualified_value_payload(module.bifaciality_factor),
            "width_m": _qualified_value_payload(module.width_m),
            "length_m": _qualified_value_payload(module.length_m),
        },
        "inverter": {
            "profile_id": inverter.profile_id,
            "revision": inverter.revision,
            "apparent_power_kva": _qualified_value_payload(inverter.apparent_power_kva),
            "physical_dc_input_count": _qualified_value_payload(
                inverter.physical_dc_input_count
            ),
            "dc_inputs": [
                {
                    "input_id": item.input_id,
                    "positive_terminal_id": item.positive_terminal_id,
                    "negative_terminal_id": item.negative_terminal_id,
                    "mppt_id": _qualified_value_payload(item.mppt_id),
                }
                for item in sorted(inverter.dc_inputs, key=lambda value: value.input_id)
            ],
            "mppt_count": _qualified_value_payload(inverter.mppt_count),
            "internal_dc_topology": _qualified_value_payload(
                inverter.internal_dc_topology
            ),
            "reverse_current_blocking": _qualified_value_payload(
                inverter.reverse_current_blocking
            ),
            "pce_backfeed_current_a": _qualified_value_payload(
                inverter.pce_backfeed_current_a
            ),
            "maximum_dc_voltage_v": _qualified_value_payload(
                inverter.maximum_dc_voltage_v
            ),
            "maximum_dc_input_power_kwp": _qualified_value_payload(
                inverter.maximum_dc_input_power_kwp
            ),
        },
        "connector": {
            "profile_id": connector.profile_id,
            "revision": connector.revision,
            "contact_resistance_ohm_per_mated_pair": _qualified_value_payload(
                connector.contact_resistance_ohm_per_mated_pair
            ),
            "rated_current_a": _qualified_value_payload(connector.rated_current_a),
            "rated_voltage_v": _qualified_value_payload(connector.rated_voltage_v),
            "mating_compatibility": _qualified_value_payload(
                connector.mating_compatibility
            ),
        },
        "factory_leads": {
            "profile_id": factory_leads.profile_id,
            "revision": factory_leads.revision,
            "conductor_product_id": factory_leads.conductor_product_id,
            "connector_profile_id": factory_leads.connector_profile_id,
            "positive_lead_length_m": _qualified_value_payload(
                factory_leads.positive_lead_length_m
            ),
            "negative_lead_length_m": _qualified_value_payload(
                factory_leads.negative_lead_length_m
            ),
            "resistance_source_status": str(
                assess_resistance_source(FACTORY_LEAD_4MM2.resolved_resistance).status
            ),
        },
        "field_conductor": {
            "profile_id": field_conductor.profile_id,
            "revision": field_conductor.revision,
            "conductor_product_id": field_conductor.conductor_product_id,
            "installation_class": _qualified_value_payload(
                field_conductor.installation_class
            ),
            "resistance_source_status": str(
                assess_resistance_source(EXTERNAL_STRING_6MM2.resolved_resistance).status
            ),
        },
    }


def reference_equipment_contract_json(
    contract: ReferenceEquipmentContract,
) -> str:
    return json.dumps(
        reference_equipment_contract_payload(contract),
        sort_keys=True,
        separators=(",", ":"),
        ensure_ascii=False,
    )


def reference_equipment_contract_hash(
    contract: ReferenceEquipmentContract,
) -> str:
    digest = hashlib.sha256(
        reference_equipment_contract_json(contract).encode("utf-8")
    ).hexdigest()
    return f"sha256:{digest}"


def _qualified_items(contract: ReferenceEquipmentContract) -> tuple[tuple[str, QualifiedValue], ...]:
    module = contract.module
    inverter = contract.inverter
    connector = contract.connector
    factory_leads = contract.factory_leads
    field_conductor = contract.field_conductor
    items: list[tuple[str, QualifiedValue]] = [
        ("module.technology", module.technology),
        ("module.rated_power_wp", module.rated_power_wp),
        ("module.voc_v", module.voc_v),
        ("module.isc_a", module.isc_a),
        ("module.vmp_v", module.vmp_v),
        ("module.imp_a", module.imp_a),
        (
            "module.maximum_overcurrent_protection_rating_a",
            module.maximum_overcurrent_protection_rating_a,
        ),
        ("module.bifaciality_factor", module.bifaciality_factor),
        ("module.width_m", module.width_m),
        ("module.length_m", module.length_m),
        ("inverter.apparent_power_kva", inverter.apparent_power_kva),
        ("inverter.physical_dc_input_count", inverter.physical_dc_input_count),
        ("inverter.mppt_count", inverter.mppt_count),
        ("inverter.internal_dc_topology", inverter.internal_dc_topology),
        ("inverter.reverse_current_blocking", inverter.reverse_current_blocking),
        ("inverter.pce_backfeed_current_a", inverter.pce_backfeed_current_a),
        ("inverter.maximum_dc_voltage_v", inverter.maximum_dc_voltage_v),
        (
            "inverter.maximum_dc_input_power_kwp",
            inverter.maximum_dc_input_power_kwp,
        ),
        (
            "connector.contact_resistance_ohm_per_mated_pair",
            connector.contact_resistance_ohm_per_mated_pair,
        ),
        ("connector.rated_current_a", connector.rated_current_a),
        ("connector.rated_voltage_v", connector.rated_voltage_v),
        ("connector.mating_compatibility", connector.mating_compatibility),
        (
            "factory_leads.positive_lead_length_m",
            factory_leads.positive_lead_length_m,
        ),
        (
            "factory_leads.negative_lead_length_m",
            factory_leads.negative_lead_length_m,
        ),
        ("field_conductor.installation_class", field_conductor.installation_class),
    ]
    items.extend(
        (f"inverter.dc_inputs.{item.input_id}.mppt_id", item.mppt_id)
        for item in inverter.dc_inputs
    )
    return tuple(sorted(items, key=lambda item: item[0]))


def reference_equipment_missing_evidence(
    contract: ReferenceEquipmentContract,
) -> tuple[str, ...]:
    validate_reference_equipment_contract(contract)
    missing = [path for path, item in _qualified_items(contract) if not item.verified]
    if assess_resistance_source(FACTORY_LEAD_4MM2.resolved_resistance).status is not ResistanceSourceStatus.VERIFIED:
        missing.append("factory_leads.conductor_resistance_source")
    if assess_resistance_source(EXTERNAL_STRING_6MM2.resolved_resistance).status is not ResistanceSourceStatus.VERIFIED:
        missing.append("field_conductor.conductor_resistance_source")
    return tuple(sorted(missing))


def validate_reference_equipment_contract(
    contract: ReferenceEquipmentContract,
) -> None:
    if not isinstance(contract, ReferenceEquipmentContract):
        raise TypeError("contract must be a ReferenceEquipmentContract")
    for identifier in (
        contract.contract_id,
        contract.module.profile_id,
        contract.inverter.profile_id,
        contract.connector.profile_id,
        contract.factory_leads.profile_id,
        contract.field_conductor.profile_id,
    ):
        if not identifier or identifier.lower() != identifier or " " in identifier:
            raise ValueError("equipment identifiers must be non-empty lowercase tokens")
    if contract.schema_version != EQUIPMENT_PROFILE_SCHEMA_VERSION:
        raise ValueError("unsupported equipment profile schema version")
    if contract.modules_per_string != 30 or contract.string_count != 24:
        raise ValueError("generic reference contract must preserve the 24 by 30 fixture")
    if contract.module_count != 720:
        raise ValueError("generic reference contract must contain 720 modules")
    if not math.isclose(contract.string_rated_power_kwp, 19.8, abs_tol=1e-12):
        raise ValueError("generic reference string must equal 19.8 kWp")
    if not math.isclose(contract.dc_nameplate_power_kwp, 475.2, abs_tol=1e-12):
        raise ValueError("generic reference block must equal 475.2 kWp")
    if not math.isclose(contract.dc_ac_nameplate_ratio, 1.35, abs_tol=1e-12):
        raise ValueError("generic reference block must have a 1.35 DC/AC ratio")
    if len(contract.inverter.dc_inputs) != 24:
        raise ValueError("generic inverter must expose 24 physical DC inputs")
    input_ids = [item.input_id for item in contract.inverter.dc_inputs]
    terminal_ids = [
        terminal_id
        for item in contract.inverter.dc_inputs
        for terminal_id in (item.positive_terminal_id, item.negative_terminal_id)
    ]
    if len(input_ids) != len(set(input_ids)):
        raise ValueError("physical DC input identifiers must be unique")
    if len(terminal_ids) != len(set(terminal_ids)):
        raise ValueError("physical DC input terminal identifiers must be unique")
    for _, item in _qualified_items(contract):
        item.validate()
    if contract.module.technology.value != str(ModuleTechnology.BIFACIAL):
        raise ValueError("generic module technology must be bifacial")
    if contract.inverter.internal_dc_topology.value != str(InternalDcTopology.UNKNOWN):
        raise ValueError("generic internal DC topology must remain unresolved")
    if contract.inverter.reverse_current_blocking.value != str(ReverseCurrentBlockingState.UNKNOWN):
        raise ValueError("generic reverse-current blocking must remain unresolved")
    if any(item.mppt_id.value is not None for item in contract.inverter.dc_inputs):
        raise ValueError("generic physical inputs must not invent MPPT assignments")
    if contract.factory_leads.conductor_product_id != FACTORY_LEAD_4MM2.product_id:
        raise ValueError("factory-lead conductor reference changed")
    if contract.field_conductor.conductor_product_id != EXTERNAL_STRING_6MM2.product_id:
        raise ValueError("field-conductor reference changed")
    payload_text = json.dumps(
        {
            "contract_id": contract.contract_id,
            "profile_ids": [
                contract.module.profile_id,
                contract.inverter.profile_id,
                contract.connector.profile_id,
                contract.factory_leads.profile_id,
                contract.field_conductor.profile_id,
            ],
        },
        sort_keys=True,
    ).lower()
    for prohibited in ("manufacturer_name", "project_name", "client_name"):
        if prohibited in payload_text:
            raise ValueError("generic equipment contract contains prohibited identity data")


GENERIC_REFERENCE_EQUIPMENT_CONTRACT = build_generic_reference_equipment_contract()
