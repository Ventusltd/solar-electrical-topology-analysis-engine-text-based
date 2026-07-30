"""Immutable deterministic calculation receipts for validated V10 circuits."""

from __future__ import annotations

from dataclasses import dataclass
import hashlib
import json

from .circuit import EvidenceClass
from .evidence import EvidenceDescriptor


CALCULATION_RECEIPT_SCHEMA_VERSION = (
    "globalgrid2050.solar-dc.calculation-receipt.v10.1"
)
COMPLETE_CIRCUIT_METHOD_VERSION = (
    "globalgrid2050.solar-dc.complete-circuit-r-vdrop-loss.v10.1"
)


@dataclass(frozen=True)
class SegmentCalculationResult:
    segment_id: str
    segment_type: str
    conductor_product_id: str
    conductor_length_m: float
    r20_ohm_per_m: float
    temperature_c: float
    conductor_resistance_ohm: float
    connector_count: int
    connector_resistance_ohm_each: float
    connector_resistance_ohm: float
    total_resistance_ohm: float
    voltage_drop_v: float
    resistive_loss_w: float
    source_evidence: EvidenceDescriptor
    result_evidence_class: EvidenceClass = EvidenceClass.DERIVED


@dataclass(frozen=True)
class OrderedCircuitCalculationReceipt:
    receipt_id: str
    circuit_model_id: str
    validated_circuit_hash: str
    traversal_schema_version: str
    ordered_terminal_ids: tuple[str, ...]
    ordered_connection_ids: tuple[str, ...]
    ordered_segment_ids: tuple[str, ...]
    current_a: float
    current_evidence: EvidenceDescriptor
    segment_results: tuple[SegmentCalculationResult, ...]
    total_conductor_length_m: float
    total_conductor_resistance_ohm: float
    total_connector_resistance_ohm: float
    total_resistance_ohm: float
    voltage_drop_v: float
    resistive_loss_w: float
    input_evidence_floor: EvidenceClass
    warnings: tuple[str, ...] = ()
    schema_version: str = CALCULATION_RECEIPT_SCHEMA_VERSION
    method_version: str = COMPLETE_CIRCUIT_METHOD_VERSION
    formula_ids: tuple[str, ...] = (
        "V10-R-001:Rconductor=R20*L*(1+alpha20*(T-20C))",
        "V10-R-002:Rcontacts=N*R20contact*(1+alpha20*(T-20C))",
        "V10-V-001:dV=I*R",
        "V10-P-001:Ploss=I^2*R",
    )


def _evidence_payload(descriptor: EvidenceDescriptor) -> dict[str, object]:
    return {
        "schema_version": descriptor.schema_version,
        "evidence_class": str(descriptor.evidence_class),
        "verification_state": str(descriptor.verification_state),
        "source_reference": descriptor.source_reference,
        "source_vocabulary": descriptor.source_vocabulary,
        "source_value": descriptor.source_value,
    }


def _segment_payload(result: SegmentCalculationResult) -> dict[str, object]:
    return {
        "segment_id": result.segment_id,
        "segment_type": result.segment_type,
        "conductor_product_id": result.conductor_product_id,
        "conductor_length_m": result.conductor_length_m,
        "r20_ohm_per_m": result.r20_ohm_per_m,
        "temperature_c": result.temperature_c,
        "conductor_resistance_ohm": result.conductor_resistance_ohm,
        "connector_count": result.connector_count,
        "connector_resistance_ohm_each": (
            result.connector_resistance_ohm_each
        ),
        "connector_resistance_ohm": result.connector_resistance_ohm,
        "total_resistance_ohm": result.total_resistance_ohm,
        "voltage_drop_v": result.voltage_drop_v,
        "resistive_loss_w": result.resistive_loss_w,
        "source_evidence": _evidence_payload(result.source_evidence),
        "result_evidence_class": str(result.result_evidence_class),
    }


def calculation_receipt_payload(
    receipt: OrderedCircuitCalculationReceipt,
) -> dict[str, object]:
    """Return deterministic machine-readable evidence without a timestamp."""

    return {
        "schema_version": receipt.schema_version,
        "method_version": receipt.method_version,
        "receipt_id": receipt.receipt_id,
        "circuit_model_id": receipt.circuit_model_id,
        "validated_circuit_hash": receipt.validated_circuit_hash,
        "traversal_schema_version": receipt.traversal_schema_version,
        "ordered_terminal_ids": list(receipt.ordered_terminal_ids),
        "ordered_connection_ids": list(receipt.ordered_connection_ids),
        "ordered_segment_ids": list(receipt.ordered_segment_ids),
        "current_a": receipt.current_a,
        "current_evidence": _evidence_payload(receipt.current_evidence),
        "segment_results": [
            _segment_payload(result)
            for result in receipt.segment_results
        ],
        "totals": {
            "conductor_length_m": receipt.total_conductor_length_m,
            "conductor_resistance_ohm": (
                receipt.total_conductor_resistance_ohm
            ),
            "connector_resistance_ohm": (
                receipt.total_connector_resistance_ohm
            ),
            "resistance_ohm": receipt.total_resistance_ohm,
            "voltage_drop_v": receipt.voltage_drop_v,
            "resistive_loss_w": receipt.resistive_loss_w,
        },
        "input_evidence_floor": str(receipt.input_evidence_floor),
        "result_evidence_class": str(EvidenceClass.DERIVED),
        "formula_ids": list(receipt.formula_ids),
        "warnings": list(receipt.warnings),
    }


def calculation_receipt_json(
    receipt: OrderedCircuitCalculationReceipt,
) -> str:
    return json.dumps(
        calculation_receipt_payload(receipt),
        sort_keys=True,
        separators=(",", ":"),
        ensure_ascii=False,
    )


def calculation_receipt_hash(
    receipt: OrderedCircuitCalculationReceipt,
) -> str:
    digest = hashlib.sha256(
        calculation_receipt_json(receipt).encode("utf-8")
    ).hexdigest()
    return f"sha256:{digest}"
