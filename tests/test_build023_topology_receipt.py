from __future__ import annotations

from dataclasses import replace

import pytest

from solar_topology.circuit import (
    CircuitModel,
    Connection,
    ConnectionKind,
    ObjectKind,
    PhysicalObject,
    Terminal,
    TerminalPolarity,
)
from solar_topology.topology_authority import (
    issue_topology_receipt,
    require_topology_receipt,
)


def _model(model_id: str = "receipt-model") -> CircuitModel:
    t1 = Terminal("left", "wire", TerminalPolarity.POSITIVE)
    t2 = Terminal("right", "wire", TerminalPolarity.NEGATIVE)
    wire = PhysicalObject("wire", ObjectKind.FIELD_CONDUCTOR, (t1, t2))
    edge = Connection(
        "wire-internal",
        "left",
        "right",
        kind=ConnectionKind.INTERNAL,
        segment_id="wire-segment",
    )
    return CircuitModel(model_id=model_id, objects=(wire,), connections=(edge,))


def test_receipt_is_issued_only_for_complete_valid_topology() -> None:
    model = _model()
    receipt = issue_topology_receipt(
        model,
        "left",
        "right",
        expected_segment_ids=("wire-segment",),
    )
    assert receipt.circuit_hash.startswith("sha256:")
    assert receipt.ordered_terminal_ids == ("left", "right")
    require_topology_receipt(model, receipt)


def test_receipt_rejects_foreign_model_identity() -> None:
    model = _model()
    receipt = issue_topology_receipt(model, "left", "right")
    with pytest.raises(ValueError, match="model_id"):
        require_topology_receipt(_model("other-model"), receipt)


def test_receipt_rejects_stale_circuit_hash() -> None:
    model = _model()
    receipt = issue_topology_receipt(model, "left", "right")
    stale = replace(receipt, circuit_hash="sha256:" + "0" * 64)
    with pytest.raises(ValueError, match="stale"):
        require_topology_receipt(model, stale)


def test_receipt_rejects_tampered_order() -> None:
    model = _model()
    receipt = issue_topology_receipt(model, "left", "right")
    tampered = replace(receipt, ordered_terminal_ids=("right", "left"))
    with pytest.raises(ValueError, match="terminal order"):
        require_topology_receipt(model, tampered)
