"""Authoritative topology receipts for calculation entry-point gating."""

from __future__ import annotations

from dataclasses import dataclass

from .circuit import CircuitModel
from .circuit_traversal import OrderedCircuitTraversal, verify_ordered_circuit
from .circuit_validation import (
    CircuitValidationResult,
    validate_circuit_model,
    validated_circuit_hash,
)


TOPOLOGY_RECEIPT_SCHEMA_VERSION = "globalgrid2050.solar-dc.topology-receipt.v10.1"


@dataclass(frozen=True)
class AuthoritativeTopologyReceipt:
    model_id: str
    circuit_hash: str
    start_terminal_id: str
    end_terminal_id: str
    ordered_terminal_ids: tuple[str, ...]
    ordered_connection_ids: tuple[str, ...]
    ordered_segment_ids: tuple[str, ...]
    schema_version: str = TOPOLOGY_RECEIPT_SCHEMA_VERSION


def issue_topology_receipt(
    model: CircuitModel,
    start_terminal_id: str,
    end_terminal_id: str,
    *,
    expected_segment_ids: tuple[str, ...] | None = None,
) -> AuthoritativeTopologyReceipt:
    """Issue a receipt only after independent validation and complete traversal."""

    validation: CircuitValidationResult = validate_circuit_model(model)
    validation.raise_for_errors()

    traversal: OrderedCircuitTraversal = verify_ordered_circuit(
        model,
        start_terminal_id,
        end_terminal_id,
        expected_segment_ids=expected_segment_ids,
    )
    traversal.raise_for_errors()

    return AuthoritativeTopologyReceipt(
        model_id=model.model_id,
        circuit_hash=validated_circuit_hash(model),
        start_terminal_id=start_terminal_id,
        end_terminal_id=end_terminal_id,
        ordered_terminal_ids=traversal.ordered_terminal_ids,
        ordered_connection_ids=traversal.ordered_connection_ids,
        ordered_segment_ids=traversal.ordered_segment_ids,
    )


def require_topology_receipt(
    model: CircuitModel,
    receipt: AuthoritativeTopologyReceipt,
) -> None:
    """Reject stale, foreign or structurally invalid receipts before calculation."""

    if not isinstance(receipt, AuthoritativeTopologyReceipt):
        raise TypeError("receipt must be an AuthoritativeTopologyReceipt")
    if receipt.schema_version != TOPOLOGY_RECEIPT_SCHEMA_VERSION:
        raise ValueError("unsupported topology receipt schema")
    if receipt.model_id != model.model_id:
        raise ValueError("topology receipt model_id does not match model")
    current_hash = validated_circuit_hash(model)
    if receipt.circuit_hash != current_hash:
        raise ValueError("topology receipt is stale for the supplied circuit model")

    traversal = verify_ordered_circuit(
        model,
        receipt.start_terminal_id,
        receipt.end_terminal_id,
        expected_segment_ids=receipt.ordered_segment_ids,
    )
    traversal.raise_for_errors()
    if traversal.ordered_terminal_ids != receipt.ordered_terminal_ids:
        raise ValueError("topology receipt terminal order does not match model")
    if traversal.ordered_connection_ids != receipt.ordered_connection_ids:
        raise ValueError("topology receipt connection order does not match model")
