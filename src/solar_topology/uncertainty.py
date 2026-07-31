"""Conservative interval propagation for validated V10 steady-state circuits.

This module is deliberately downstream of canonical circuit validation and
independent ordered traversal. It does not infer probability distributions or
claim statistical confidence: intervals are declared engineering bounds.
"""

from __future__ import annotations

from dataclasses import dataclass
import hashlib
import json
import math
from typing import Mapping

from .calculation_receipts import OrderedCircuitCalculationReceipt
from .circuit import CircuitModel, PhysicalObject
from .circuit_calculations import ALPHA_CU_20_PER_C, calculate_complete_circuit
from .circuit_traversal import OrderedCircuitTraversal
from .evidence import EvidenceDescriptor


UNCERTAINTY_SCHEMA_VERSION = "globalgrid2050.solar-dc.uncertainty.v10.2"
UNCERTAINTY_METHOD_VERSION = (
    "globalgrid2050.solar-dc.complete-circuit-interval-propagation.v10.3"
)


@dataclass(frozen=True)
class Interval:
    """Closed finite interval with a declared nominal value."""

    lower: float
    nominal: float
    upper: float
    unit: str

    def __post_init__(self) -> None:
        values = (self.lower, self.nominal, self.upper)
        if any(
            not isinstance(value, (int, float))
            or isinstance(value, bool)
            or not math.isfinite(float(value))
            for value in values
        ):
            raise ValueError("interval values must be finite numbers")
        if float(self.lower) > float(self.nominal) or float(self.nominal) > float(self.upper):
            raise ValueError("interval must satisfy lower <= nominal <= upper")
        if not isinstance(self.unit, str) or not self.unit:
            raise ValueError("interval unit must be non-empty text")

    @classmethod
    def exact(cls, value: float, unit: str) -> "Interval":
        return cls(float(value), float(value), float(value), unit)


@dataclass(frozen=True)
class OperatingState:
    """Immutable electrical operating inputs used by the calculation."""

    current_a: Interval
    current_evidence: EvidenceDescriptor
    string_vmp_v: Interval
    string_vmp_evidence: EvidenceDescriptor
    state_id: str = "operating-state"

    def __post_init__(self) -> None:
        if self.current_a.unit != "A":
            raise ValueError("current interval unit must be A")
        if self.string_vmp_v.unit != "V":
            raise ValueError("string Vmp interval unit must be V")
        if self.current_a.lower < 0:
            raise ValueError("current interval cannot be negative")
        if self.string_vmp_v.lower <= 0:
            raise ValueError("string Vmp interval must be strictly positive")
        if not isinstance(self.current_evidence, EvidenceDescriptor):
            raise TypeError("current_evidence must be an EvidenceDescriptor")
        if not isinstance(self.string_vmp_evidence, EvidenceDescriptor):
            raise TypeError("string_vmp_evidence must be an EvidenceDescriptor")
        if not isinstance(self.state_id, str) or not self.state_id:
            raise ValueError("state_id must be non-empty text")


@dataclass(frozen=True)
class SegmentInputIntervals:
    """Optional declared bounds for one canonical source segment."""

    conductor_length_m: Interval | None = None
    r20_ohm_per_m: Interval | None = None
    temperature_c: Interval | None = None
    connector_resistance_ohm_each: Interval | None = None


@dataclass(frozen=True)
class SegmentUncertaintyResult:
    segment_id: str
    conductor_resistance_ohm: Interval
    connector_resistance_ohm: Interval
    total_resistance_ohm: Interval


@dataclass(frozen=True)
class UncertainCircuitCalculationReceipt:
    receipt_id: str
    operating_state: OperatingState
    nominal_receipt: OrderedCircuitCalculationReceipt
    segment_results: tuple[SegmentUncertaintyResult, ...]
    total_resistance_ohm: Interval
    voltage_drop_v: Interval
    resistive_loss_w: Interval
    voltage_drop_percent: Interval
    warnings: tuple[str, ...]
    schema_version: str = UNCERTAINTY_SCHEMA_VERSION
    method_version: str = UNCERTAINTY_METHOD_VERSION


def _attributes(obj: PhysicalObject) -> dict[str, object]:
    return {key: value for key, value in obj.attributes}


def _segment_objects(model: CircuitModel) -> dict[str, PhysicalObject]:
    result: dict[str, PhysicalObject] = {}
    for obj in model.objects:
        segment_id = _attributes(obj).get("segment_id")
        if isinstance(segment_id, str) and segment_id:
            if segment_id in result:
                raise ValueError(f"canonical circuit repeats source segment {segment_id!r}")
            result[segment_id] = obj
    return result


def _number(attributes: dict[str, object], key: str, segment_id: str) -> float:
    value = attributes.get(key)
    if (
        not isinstance(value, (int, float))
        or isinstance(value, bool)
        or not math.isfinite(float(value))
    ):
        raise ValueError(f"segment {segment_id!r} requires finite numeric attribute {key}")
    return float(value)


def _declared_or_exact(
    declared: Interval | None,
    nominal: float,
    unit: str,
    *,
    non_negative: bool = False,
    strictly_positive: bool = False,
) -> Interval:
    interval = declared or Interval.exact(nominal, unit)
    if interval.unit != unit:
        raise ValueError(f"interval unit must be {unit}")
    if not math.isclose(interval.nominal, nominal, rel_tol=0.0, abs_tol=1e-15):
        raise ValueError("declared interval nominal must equal canonical model value")
    if non_negative and interval.lower < 0:
        raise ValueError("declared interval cannot include negative values")
    if strictly_positive and interval.lower <= 0:
        raise ValueError("declared interval must remain strictly positive")
    return interval


def _resistance_bounds(
    length: Interval,
    r20: Interval,
    temperature: Interval,
    *,
    temperature_coefficient_per_c: float,
) -> Interval:
    alpha = float(temperature_coefficient_per_c)
    if not math.isfinite(alpha) or alpha <= 0:
        raise ValueError("temperature coefficient must be finite and positive")
    lower_factor = 1 + alpha * (temperature.lower - 20.0)
    nominal_factor = 1 + alpha * (temperature.nominal - 20.0)
    upper_factor = 1 + alpha * (temperature.upper - 20.0)
    if lower_factor <= 0:
        raise ValueError("temperature interval creates a non-positive resistance factor")
    return Interval(
        length.lower * r20.lower * lower_factor,
        length.nominal * r20.nominal * nominal_factor,
        length.upper * r20.upper * upper_factor,
        "ohm",
    )


def _interval_payload(interval: Interval) -> dict[str, object]:
    return {
        "lower": interval.lower,
        "nominal": interval.nominal,
        "upper": interval.upper,
        "unit": interval.unit,
    }


def uncertainty_receipt_payload(
    receipt: UncertainCircuitCalculationReceipt,
) -> dict[str, object]:
    return {
        "schema_version": receipt.schema_version,
        "method_version": receipt.method_version,
        "receipt_id": receipt.receipt_id,
        "validated_circuit_hash": receipt.nominal_receipt.validated_circuit_hash,
        "nominal_calculation_receipt_id": receipt.nominal_receipt.receipt_id,
        "resistance_registry_hash": (
            receipt.nominal_receipt.resistance_registry_hash
        ),
        "operating_state": {
            "state_id": receipt.operating_state.state_id,
            "current_a": _interval_payload(receipt.operating_state.current_a),
            "string_vmp_v": _interval_payload(receipt.operating_state.string_vmp_v),
        },
        "segment_results": [
            {
                "segment_id": result.segment_id,
                "conductor_resistance_ohm": _interval_payload(
                    result.conductor_resistance_ohm
                ),
                "connector_resistance_ohm": _interval_payload(
                    result.connector_resistance_ohm
                ),
                "total_resistance_ohm": _interval_payload(
                    result.total_resistance_ohm
                ),
            }
            for result in receipt.segment_results
        ],
        "totals": {
            "resistance_ohm": _interval_payload(receipt.total_resistance_ohm),
            "voltage_drop_v": _interval_payload(receipt.voltage_drop_v),
            "resistive_loss_w": _interval_payload(receipt.resistive_loss_w),
            "voltage_drop_percent": _interval_payload(
                receipt.voltage_drop_percent
            ),
        },
        "warnings": list(receipt.warnings),
    }


def uncertainty_receipt_json(
    receipt: UncertainCircuitCalculationReceipt,
) -> str:
    return json.dumps(
        uncertainty_receipt_payload(receipt),
        sort_keys=True,
        separators=(",", ":"),
        ensure_ascii=False,
    )


def uncertainty_receipt_hash(
    receipt: UncertainCircuitCalculationReceipt,
) -> str:
    digest = hashlib.sha256(
        uncertainty_receipt_json(receipt).encode("utf-8")
    ).hexdigest()
    return f"sha256:{digest}"


def calculate_complete_circuit_with_uncertainty(
    model: CircuitModel,
    traversal: OrderedCircuitTraversal,
    *,
    operating_state: OperatingState,
    segment_intervals: Mapping[str, SegmentInputIntervals] | None = None,
    receipt_id: str | None = None,
) -> UncertainCircuitCalculationReceipt:
    """Propagate declared monotonic bounds after the normal validation gates.

    Correlation and probability are deliberately not inferred. The returned
    extrema are conservative combinations of the supplied independent bounds.
    Conductor temperature coefficients follow each segment's resolved resistance
    evidence; connector bounds retain the existing visible copper-alpha model.
    """

    if not isinstance(operating_state, OperatingState):
        raise TypeError("operating_state must be an OperatingState")
    overrides = dict(segment_intervals or {})

    nominal = calculate_complete_circuit(
        model,
        traversal,
        current_a=operating_state.current_a.nominal,
        current_evidence=operating_state.current_evidence,
    )
    segment_objects = _segment_objects(model)
    unknown = sorted(set(overrides) - set(nominal.ordered_segment_ids))
    if unknown:
        raise ValueError(f"uncertainty supplied for unknown segments: {unknown}")

    results: list[SegmentUncertaintyResult] = []
    for nominal_result in nominal.segment_results:
        segment_id = nominal_result.segment_id
        attributes = _attributes(segment_objects[segment_id])
        declared = overrides.get(segment_id, SegmentInputIntervals())

        length = _declared_or_exact(
            declared.conductor_length_m,
            nominal_result.conductor_length_m,
            "m",
            non_negative=True,
        )
        r20 = _declared_or_exact(
            declared.r20_ohm_per_m,
            nominal_result.r20_ohm_per_m,
            "ohm/m",
            strictly_positive=True,
        )
        temperature = _declared_or_exact(
            declared.temperature_c,
            nominal_result.temperature_c,
            "degC",
        )
        connector_each = _declared_or_exact(
            declared.connector_resistance_ohm_each,
            nominal_result.connector_resistance_ohm_each,
            "ohm",
            non_negative=True,
        )
        connector_count = int(_number(attributes, "connector_count", segment_id))

        conductor = _resistance_bounds(
            length,
            r20,
            temperature,
            temperature_coefficient_per_c=(
                nominal_result.resistance_evidence.temperature_coefficient_per_c
            ),
        )
        connector_unit = _resistance_bounds(
            Interval.exact(float(connector_count), "count"),
            Interval(
                connector_each.lower,
                connector_each.nominal,
                connector_each.upper,
                "ohm/count",
            ),
            temperature,
            temperature_coefficient_per_c=ALPHA_CU_20_PER_C,
        )
        connector = Interval(
            connector_unit.lower,
            connector_unit.nominal,
            connector_unit.upper,
            "ohm",
        )
        total = Interval(
            conductor.lower + connector.lower,
            conductor.nominal + connector.nominal,
            conductor.upper + connector.upper,
            "ohm",
        )
        results.append(
            SegmentUncertaintyResult(
                segment_id=segment_id,
                conductor_resistance_ohm=conductor,
                connector_resistance_ohm=connector,
                total_resistance_ohm=total,
            )
        )

    total_nominal_resistance = math.fsum(
        result.total_resistance_ohm.nominal for result in results
    )
    if total_nominal_resistance != nominal.total_resistance_ohm:
        raise AssertionError(
            "uncertainty and nominal calculations use different resistance accumulation"
        )
    total_r = Interval(
        math.fsum(result.total_resistance_ohm.lower for result in results),
        total_nominal_resistance,
        math.fsum(result.total_resistance_ohm.upper for result in results),
        "ohm",
    )
    current = operating_state.current_a
    voltage_drop_nominal = current.nominal * total_r.nominal
    if voltage_drop_nominal != nominal.voltage_drop_v:
        raise AssertionError(
            "uncertainty and nominal calculations use different voltage-drop accumulation"
        )
    voltage_drop = Interval(
        current.lower * total_r.lower,
        voltage_drop_nominal,
        current.upper * total_r.upper,
        "V",
    )
    loss_nominal = current.nominal**2 * total_r.nominal
    if loss_nominal != nominal.resistive_loss_w:
        raise AssertionError(
            "uncertainty and nominal calculations use different loss accumulation"
        )
    loss = Interval(
        current.lower**2 * total_r.lower,
        loss_nominal,
        current.upper**2 * total_r.upper,
        "W",
    )
    vmp = operating_state.string_vmp_v
    drop_percent = Interval(
        100.0 * voltage_drop.lower / vmp.upper,
        100.0 * voltage_drop.nominal / vmp.nominal,
        100.0 * voltage_drop.upper / vmp.lower,
        "%",
    )

    base_payload = {
        "method_version": UNCERTAINTY_METHOD_VERSION,
        "nominal_receipt_id": nominal.receipt_id,
        "resistance_registry_hash": nominal.resistance_registry_hash,
        "operating_state_id": operating_state.state_id,
        "segment_ids": list(nominal.ordered_segment_ids),
        "resistance": _interval_payload(total_r),
        "voltage_drop": _interval_payload(voltage_drop),
        "loss": _interval_payload(loss),
        "voltage_drop_percent": _interval_payload(drop_percent),
    }
    generated_id = "UNC:" + hashlib.sha256(
        json.dumps(base_payload, sort_keys=True, separators=(",", ":")).encode(
            "utf-8"
        )
    ).hexdigest()

    return UncertainCircuitCalculationReceipt(
        receipt_id=receipt_id or generated_id,
        operating_state=operating_state,
        nominal_receipt=nominal,
        segment_results=tuple(results),
        total_resistance_ohm=total_r,
        voltage_drop_v=voltage_drop,
        resistive_loss_w=loss,
        voltage_drop_percent=drop_percent,
        warnings=tuple(
            sorted(
                {
                    *nominal.warnings,
                    "Declared interval bounds; not a probability distribution or confidence interval.",
                    "Candidate steady-state result; not a standards-compliance conclusion.",
                }
            )
        ),
    )
