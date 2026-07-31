"""Complete-circuit steady-state calculations gated by V10 validation and traversal."""

from __future__ import annotations

import hashlib
import json
import math

from .calculation_receipts import (
    COMPLETE_CIRCUIT_METHOD_VERSION,
    OrderedCircuitCalculationReceipt,
    SegmentCalculationResult,
)
from .circuit import CircuitModel, EvidenceClass, PhysicalObject
from .circuit_adapters import circuit_boundary_terminal_ids
from .circuit_traversal import (
    OrderedCircuitTraversal,
    verify_ordered_circuit,
)
from .circuit_validation import validated_circuit_hash
from .evidence import (
    EvidenceDescriptor,
    segment_provenance_descriptor,
    weakest_evidence_class,
)
from .resistance_evidence import (
    ResistanceBasis,
    resistance_registry_hash,
    resolve_conductor_resistance,
)


ALPHA_CU_20_PER_C = 0.00393


def _attributes(obj: PhysicalObject) -> dict[str, object]:
    return {key: value for key, value in obj.attributes}


def _required_text(
    attributes: dict[str, object],
    key: str,
    segment_id: str,
) -> str:
    value = attributes.get(key)
    if not isinstance(value, str) or not value:
        raise ValueError(
            f"segment {segment_id!r} requires non-empty text attribute {key}"
        )
    return value


def _finite_number(
    attributes: dict[str, object],
    key: str,
    segment_id: str,
    *,
    minimum: float | None = None,
    strictly_positive: bool = False,
) -> float:
    value = attributes.get(key)
    if (
        not isinstance(value, (int, float))
        or isinstance(value, bool)
        or not math.isfinite(float(value))
    ):
        raise ValueError(
            f"segment {segment_id!r} requires finite numeric attribute {key}"
        )
    number = float(value)
    if strictly_positive and number <= 0:
        raise ValueError(
            f"segment {segment_id!r} attribute {key} must be positive"
        )
    if minimum is not None and number < minimum:
        raise ValueError(
            f"segment {segment_id!r} attribute {key} must be >= {minimum}"
        )
    return number


def _non_negative_integer(
    attributes: dict[str, object],
    key: str,
    segment_id: str,
) -> int:
    value = attributes.get(key)
    if (
        not isinstance(value, int)
        or isinstance(value, bool)
        or value < 0
    ):
        raise ValueError(
            f"segment {segment_id!r} attribute {key} "
            "must be a non-negative integer"
        )
    return value


def _segment_object_by_id(
    model: CircuitModel,
) -> dict[str, PhysicalObject]:
    result: dict[str, PhysicalObject] = {}
    for obj in model.objects:
        attributes = _attributes(obj)
        segment_id = attributes.get("segment_id")
        if not isinstance(segment_id, str) or not segment_id:
            continue
        if segment_id in result:
            raise ValueError(
                f"canonical circuit repeats source segment {segment_id!r}"
            )
        result[segment_id] = obj
    return result


def _receipt_id(
    circuit_hash: str,
    current_a: float,
    current_evidence: EvidenceDescriptor,
    registry_hash: str,
) -> str:
    payload = {
        "method_version": COMPLETE_CIRCUIT_METHOD_VERSION,
        "validated_circuit_hash": circuit_hash,
        "resistance_registry_hash": registry_hash,
        "current_a": current_a,
        "current_evidence": {
            "evidence_class": str(current_evidence.evidence_class),
            "verification_state": str(
                current_evidence.verification_state
            ),
            "source_reference": current_evidence.source_reference,
            "source_vocabulary": current_evidence.source_vocabulary,
            "source_value": current_evidence.source_value,
        },
    }
    digest = hashlib.sha256(
        json.dumps(
            payload,
            sort_keys=True,
            separators=(",", ":"),
        ).encode("utf-8")
    ).hexdigest()
    return f"CALC:{digest}"


def calculate_complete_circuit(
    model: CircuitModel,
    traversal: OrderedCircuitTraversal,
    *,
    current_a: float,
    current_evidence: EvidenceDescriptor,
    receipt_id: str | None = None,
) -> OrderedCircuitCalculationReceipt:
    """Calculate R, voltage drop and I²R loss only after independent proof.

    Source segment attributes are read from the canonical circuit model in
    graph-derived order. No user-entered total length is accepted. R20 remains
    the numeric segment input, but its product basis and provenance are resolved
    independently and included in every calculation result.
    """

    if (
        not isinstance(current_a, (int, float))
        or isinstance(current_a, bool)
        or not math.isfinite(float(current_a))
        or current_a < 0
    ):
        raise ValueError("current_a must be a finite non-negative number")
    current_a = float(current_a)
    if not isinstance(current_evidence, EvidenceDescriptor):
        raise TypeError("current_evidence must be an EvidenceDescriptor")
    if not isinstance(traversal, OrderedCircuitTraversal):
        raise TypeError("traversal must be an OrderedCircuitTraversal")
    traversal.raise_for_errors()

    start_terminal_id, end_terminal_id = circuit_boundary_terminal_ids(model)
    if (
        traversal.start_terminal_id != start_terminal_id
        or traversal.end_terminal_id != end_terminal_id
    ):
        raise ValueError(
            "traversal boundaries do not match the canonical circuit model"
        )

    independently_verified = verify_ordered_circuit(
        model,
        start_terminal_id,
        end_terminal_id,
        expected_segment_ids=traversal.ordered_segment_ids,
    )
    independently_verified.raise_for_errors()
    if (
        independently_verified.ordered_terminal_ids
        != traversal.ordered_terminal_ids
        or independently_verified.ordered_connection_ids
        != traversal.ordered_connection_ids
        or independently_verified.ordered_segment_ids
        != traversal.ordered_segment_ids
    ):
        raise ValueError(
            "supplied traversal differs from independently derived order"
        )

    circuit_hash = validated_circuit_hash(model)
    registry_hash = resistance_registry_hash()
    segment_objects = _segment_object_by_id(model)
    if set(segment_objects) != set(traversal.ordered_segment_ids):
        missing = sorted(
            set(traversal.ordered_segment_ids) - set(segment_objects)
        )
        extra = sorted(
            set(segment_objects) - set(traversal.ordered_segment_ids)
        )
        raise ValueError(
            "canonical segment-object set differs from traversal: "
            f"missing={missing}, extra={extra}"
        )

    segment_results: list[SegmentCalculationResult] = []
    evidence_classes: list[EvidenceClass] = [
        current_evidence.evidence_class
    ]
    warnings: set[str] = {
        "Candidate steady-state result; not a standards-compliance conclusion.",
        "Connector temperature correction retains the existing copper-alpha approximation pending a connector-specific evidence model.",
    }

    for segment_id in traversal.ordered_segment_ids:
        obj = segment_objects[segment_id]
        attributes = _attributes(obj)
        if attributes.get("segment_id") != segment_id:
            raise ValueError(
                f"segment object identity mismatch for {segment_id!r}"
            )

        segment_type = _required_text(
            attributes,
            "segment_type",
            segment_id,
        )
        conductor_product_id = _required_text(
            attributes,
            "conductor_product_id",
            segment_id,
        )
        source_reference = _required_text(
            attributes,
            "source_reference",
            segment_id,
        )
        provenance = _required_text(
            attributes,
            "provenance",
            segment_id,
        )
        conductor_length_m = _finite_number(
            attributes,
            "conductor_length_m",
            segment_id,
            minimum=0.0,
        )
        r20_ohm_per_m = _finite_number(
            attributes,
            "r20_ohm_per_m",
            segment_id,
            strictly_positive=True,
        )
        resistance_evidence = resolve_conductor_resistance(
            product_id=conductor_product_id,
            r20_ohm_per_m=r20_ohm_per_m,
            legacy_provenance=provenance,
            legacy_source_reference=source_reference,
        )
        temperature_c = _finite_number(
            attributes,
            "temperature_c",
            segment_id,
        )
        connector_count = _non_negative_integer(
            attributes,
            "connector_count",
            segment_id,
        )
        connector_resistance_ohm_each = _finite_number(
            attributes,
            "connector_resistance_ohm_each",
            segment_id,
            minimum=0.0,
        )

        conductor_temperature_factor = (
            1
            + resistance_evidence.temperature_coefficient_per_c
            * (temperature_c - 20.0)
        )
        connector_temperature_factor = (
            1 + ALPHA_CU_20_PER_C * (temperature_c - 20.0)
        )
        if conductor_temperature_factor <= 0:
            raise ValueError(
                f"segment {segment_id!r} has non-positive "
                "conductor temperature correction factor"
            )
        if connector_temperature_factor <= 0:
            raise ValueError(
                f"segment {segment_id!r} has non-positive "
                "connector temperature correction factor"
            )

        conductor_resistance_ohm = (
            conductor_length_m
            * r20_ohm_per_m
            * conductor_temperature_factor
        )
        connector_resistance_ohm = (
            connector_count
            * connector_resistance_ohm_each
            * connector_temperature_factor
        )
        total_resistance_ohm = (
            conductor_resistance_ohm
            + connector_resistance_ohm
        )
        source_evidence = segment_provenance_descriptor(
            provenance,
            source_reference=source_reference,
        )
        evidence_classes.extend(
            (
                source_evidence.evidence_class,
                resistance_evidence.evidence_class,
            )
        )
        warnings.update(resistance_evidence.warnings)
        if resistance_evidence.basis is ResistanceBasis.IDEAL_BULK_ESTIMATE:
            warnings.add(
                "Ideal bulk-copper resistance is a lower-bound screening estimate, not a finished-cable declared value."
            )

        warning_text = attributes.get("warnings")
        if isinstance(warning_text, str):
            warnings.update(
                warning
                for warning in warning_text.split(";")
                if warning
            )

        segment_results.append(
            SegmentCalculationResult(
                segment_id=segment_id,
                segment_type=segment_type,
                conductor_product_id=conductor_product_id,
                conductor_length_m=conductor_length_m,
                r20_ohm_per_m=r20_ohm_per_m,
                resistance_evidence=resistance_evidence,
                temperature_c=temperature_c,
                conductor_resistance_ohm=(
                    conductor_resistance_ohm
                ),
                connector_count=connector_count,
                connector_resistance_ohm_each=(
                    connector_resistance_ohm_each
                ),
                connector_resistance_ohm=(
                    connector_resistance_ohm
                ),
                total_resistance_ohm=total_resistance_ohm,
                voltage_drop_v=current_a * total_resistance_ohm,
                resistive_loss_w=(
                    current_a**2 * total_resistance_ohm
                ),
                source_evidence=source_evidence,
            )
        )

    total_conductor_length_m = math.fsum(
        result.conductor_length_m for result in segment_results
    )
    total_conductor_resistance_ohm = math.fsum(
        result.conductor_resistance_ohm
        for result in segment_results
    )
    total_connector_resistance_ohm = math.fsum(
        result.connector_resistance_ohm
        for result in segment_results
    )
    total_resistance_ohm = math.fsum(
        result.total_resistance_ohm
        for result in segment_results
    )

    return OrderedCircuitCalculationReceipt(
        receipt_id=(
            receipt_id
            or _receipt_id(
                circuit_hash,
                current_a,
                current_evidence,
                registry_hash,
            )
        ),
        circuit_model_id=model.model_id,
        validated_circuit_hash=circuit_hash,
        traversal_schema_version=traversal.schema_version,
        ordered_terminal_ids=traversal.ordered_terminal_ids,
        ordered_connection_ids=traversal.ordered_connection_ids,
        ordered_segment_ids=traversal.ordered_segment_ids,
        current_a=current_a,
        current_evidence=current_evidence,
        segment_results=tuple(segment_results),
        total_conductor_length_m=total_conductor_length_m,
        total_conductor_resistance_ohm=(
            total_conductor_resistance_ohm
        ),
        total_connector_resistance_ohm=(
            total_connector_resistance_ohm
        ),
        total_resistance_ohm=total_resistance_ohm,
        voltage_drop_v=current_a * total_resistance_ohm,
        resistive_loss_w=current_a**2 * total_resistance_ohm,
        resistance_registry_hash=registry_hash,
        input_evidence_floor=weakest_evidence_class(
            evidence_classes
        ),
        warnings=tuple(sorted(warnings)),
    )
