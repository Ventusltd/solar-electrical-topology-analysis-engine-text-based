from dataclasses import replace

from solar_topology.calculation_receipts import (
    OrderedCircuitCalculationReceipt,
    SegmentCalculationResult,
)
from solar_topology.circuit import EvidenceClass
from solar_topology.evidence import EvidenceDescriptor, VerificationState
from solar_topology.kernel_authority import (
    KernelAuthorityStatus,
    assess_steady_state_receipt,
)
from solar_topology.resistance_evidence import (
    ResistanceBasis,
    ResistanceValueKind,
    ResolvedConductorResistance,
    resistance_records_hash,
)


def _evidence() -> EvidenceDescriptor:
    return EvidenceDescriptor(
        evidence_class=EvidenceClass.MANUFACTURER_DECLARED,
        verification_state=VerificationState.VERIFIED,
        source_reference="fixture",
        source_vocabulary="build024",
        source_value="declared",
    )


def _resistance_evidence() -> ResolvedConductorResistance:
    return ResolvedConductorResistance(
        product_id="product-1",
        r20_ohm_per_m=0.003,
        basis=ResistanceBasis.MANUFACTURER_DECLARED,
        value_kind=ResistanceValueKind.MANUFACTURER_NOMINAL,
        source_reference="fixture-resistance",
        source_revision="build024-v1",
        verification_state="verified",
    )


def _receipt() -> OrderedCircuitCalculationReceipt:
    evidence = _evidence()
    resistance = _resistance_evidence()
    segment = SegmentCalculationResult(
        segment_id="segment-1",
        segment_type="external_positive",
        conductor_product_id="product-1",
        conductor_length_m=10.0,
        r20_ohm_per_m=0.003,
        resistance_evidence=resistance,
        temperature_c=20.0,
        conductor_resistance_ohm=0.03,
        connector_count=2,
        connector_resistance_ohm_each=0.001,
        connector_resistance_ohm=0.002,
        total_resistance_ohm=0.032,
        voltage_drop_v=0.32,
        resistive_loss_w=3.2,
        source_evidence=evidence,
    )
    return OrderedCircuitCalculationReceipt(
        receipt_id="CALC:fixture",
        circuit_model_id="model-1",
        validated_circuit_hash="sha256:" + "a" * 64,
        traversal_schema_version="globalgrid2050.solar-dc.ordered-traversal.v10.1",
        ordered_terminal_ids=("t1", "t2"),
        ordered_connection_ids=("c1",),
        ordered_segment_ids=("segment-1",),
        current_a=10.0,
        current_evidence=evidence,
        segment_results=(segment,),
        total_conductor_length_m=10.0,
        total_conductor_resistance_ohm=0.03,
        total_connector_resistance_ohm=0.002,
        total_resistance_ohm=0.032,
        voltage_drop_v=0.32,
        resistive_loss_w=3.2,
        resistance_evidence_set_hash=resistance_records_hash((resistance,)),
        input_evidence_floor=EvidenceClass.MANUFACTURER_DECLARED,
    )


def test_consistent_receipt_is_authoritative_and_hashed() -> None:
    assessment = assess_steady_state_receipt(_receipt())
    assert assessment.status == KernelAuthorityStatus.AUTHORITATIVE
    assert assessment.authoritative
    assert assessment.receipt_hash is not None
    assert assessment.receipt_hash.startswith("sha256:")
    assessment.require_authoritative()


def test_modified_total_is_rejected() -> None:
    assessment = assess_steady_state_receipt(
        replace(_receipt(), total_resistance_ohm=0.031)
    )
    assert assessment.status == KernelAuthorityStatus.REJECTED
    assert "TOTAL_RESISTANCE_MISMATCH" in assessment.reasons


def test_modified_formula_contract_is_rejected() -> None:
    assessment = assess_steady_state_receipt(
        replace(_receipt(), formula_ids=("wrong",))
    )
    assert "FORMULA_CONTRACT_MISMATCH" in assessment.reasons


def test_invalid_type_is_rejected_without_hash() -> None:
    assessment = assess_steady_state_receipt(object())
    assert assessment.status == KernelAuthorityStatus.REJECTED
    assert assessment.receipt_hash is None
    assert assessment.reasons == ("INVALID_RECEIPT_TYPE",)
