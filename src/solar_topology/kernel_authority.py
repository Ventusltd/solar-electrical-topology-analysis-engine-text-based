"""Authority assessment for deterministic steady-state calculation receipts."""

from __future__ import annotations

from dataclasses import dataclass
from enum import StrEnum
import math

from .calculation_receipts import (
    CALCULATION_RECEIPT_SCHEMA_VERSION,
    COMPLETE_CIRCUIT_METHOD_VERSION,
    OrderedCircuitCalculationReceipt,
    calculation_receipt_hash,
)


KERNEL_AUTHORITY_SCHEMA_VERSION = (
    "globalgrid2050.solar-dc.kernel-authority.v10.1"
)
REQUIRED_STEADY_STATE_FORMULA_IDS = (
    "V10-R-001:Rconductor=R20*L*(1+alpha20*(T-20C))",
    "V10-R-002:Rcontacts=N*R20contact*(1+alpha20*(T-20C))",
    "V10-V-001:dV=I*R",
    "V10-P-001:Ploss=I^2*R",
)


class KernelAuthorityStatus(StrEnum):
    AUTHORITATIVE = "authoritative"
    PROVISIONAL = "provisional"
    REJECTED = "rejected"


@dataclass(frozen=True)
class KernelAuthorityAssessment:
    status: KernelAuthorityStatus
    receipt_hash: str | None
    reasons: tuple[str, ...]
    schema_version: str = KERNEL_AUTHORITY_SCHEMA_VERSION

    @property
    def authoritative(self) -> bool:
        return self.status == KernelAuthorityStatus.AUTHORITATIVE

    def require_authoritative(self) -> None:
        if not self.authoritative:
            raise ValueError(
                "steady-state receipt is not authoritative: "
                + ", ".join(self.reasons)
            )


def _close(first: float, second: float) -> bool:
    return math.isclose(first, second, rel_tol=1e-12, abs_tol=1e-12)


def assess_steady_state_receipt(
    receipt: OrderedCircuitCalculationReceipt,
) -> KernelAuthorityAssessment:
    """Independently assess whether a receipt may act as steady-state authority."""

    if not isinstance(receipt, OrderedCircuitCalculationReceipt):
        return KernelAuthorityAssessment(
            KernelAuthorityStatus.REJECTED,
            None,
            ("INVALID_RECEIPT_TYPE",),
        )

    reasons: list[str] = []
    if receipt.schema_version != CALCULATION_RECEIPT_SCHEMA_VERSION:
        reasons.append("UNSUPPORTED_RECEIPT_SCHEMA")
    if receipt.method_version != COMPLETE_CIRCUIT_METHOD_VERSION:
        reasons.append("UNSUPPORTED_METHOD_VERSION")
    if tuple(receipt.formula_ids) != REQUIRED_STEADY_STATE_FORMULA_IDS:
        reasons.append("FORMULA_CONTRACT_MISMATCH")
    if not receipt.validated_circuit_hash.startswith("sha256:"):
        reasons.append("MISSING_VALIDATED_CIRCUIT_HASH")
    if not receipt.ordered_segment_ids:
        reasons.append("EMPTY_ORDERED_SEGMENT_SET")
    if tuple(result.segment_id for result in receipt.segment_results) != tuple(
        receipt.ordered_segment_ids
    ):
        reasons.append("SEGMENT_ORDER_MISMATCH")

    numeric_values = (
        receipt.current_a,
        receipt.total_conductor_length_m,
        receipt.total_conductor_resistance_ohm,
        receipt.total_connector_resistance_ohm,
        receipt.total_resistance_ohm,
        receipt.voltage_drop_v,
        receipt.resistive_loss_w,
    )
    if any(not math.isfinite(float(value)) or value < 0 for value in numeric_values):
        reasons.append("INVALID_NON_NEGATIVE_TOTAL")

    conductor_sum = math.fsum(
        result.conductor_resistance_ohm for result in receipt.segment_results
    )
    connector_sum = math.fsum(
        result.connector_resistance_ohm for result in receipt.segment_results
    )
    length_sum = math.fsum(
        result.conductor_length_m for result in receipt.segment_results
    )
    resistance_sum = conductor_sum + connector_sum

    if not _close(length_sum, receipt.total_conductor_length_m):
        reasons.append("CONDUCTOR_LENGTH_TOTAL_MISMATCH")
    if not _close(conductor_sum, receipt.total_conductor_resistance_ohm):
        reasons.append("CONDUCTOR_RESISTANCE_TOTAL_MISMATCH")
    if not _close(connector_sum, receipt.total_connector_resistance_ohm):
        reasons.append("CONNECTOR_RESISTANCE_TOTAL_MISMATCH")
    if not _close(resistance_sum, receipt.total_resistance_ohm):
        reasons.append("TOTAL_RESISTANCE_MISMATCH")
    if not _close(receipt.current_a * resistance_sum, receipt.voltage_drop_v):
        reasons.append("VOLTAGE_DROP_MISMATCH")
    if not _close(receipt.current_a**2 * resistance_sum, receipt.resistive_loss_w):
        reasons.append("RESISTIVE_LOSS_MISMATCH")

    receipt_hash = calculation_receipt_hash(receipt)
    status = (
        KernelAuthorityStatus.AUTHORITATIVE
        if not reasons
        else KernelAuthorityStatus.REJECTED
    )
    return KernelAuthorityAssessment(
        status,
        receipt_hash,
        tuple(sorted(set(reasons))),
    )
