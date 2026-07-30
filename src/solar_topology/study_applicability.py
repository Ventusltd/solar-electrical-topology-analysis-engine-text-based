"""Applicability and acceptance-criterion controls for engineering studies.

The registry prevents a calculated quantity from being mistaken for a compliance
verdict. Acceptance limits must be declared with an evidence source and method.
"""

from __future__ import annotations

from dataclasses import dataclass
from enum import StrEnum
import math

from .diagnostics import StudyCoverage, StudyState


STUDY_APPLICABILITY_SCHEMA_VERSION = (
    "globalgrid2050.solar-dc.study-applicability.v10.1"
)


class StudyKind(StrEnum):
    COLD_VOC = "cold_voc"
    VOLTAGE_DROP = "voltage_drop"
    AMPACITY = "ampacity"
    LOOP_GEOMETRY = "loop_geometry"
    TRANSIENT = "transient"
    CAPACITANCE_TO_EARTH = "capacitance_to_earth"
    INSULATION_MONITORING = "insulation_monitoring"
    SPD_CRITICAL_LENGTH = "spd_critical_length"
    REVERSE_CURRENT = "reverse_current"


class CriterionOperator(StrEnum):
    MAXIMUM = "maximum"
    MINIMUM = "minimum"


@dataclass(frozen=True)
class AcceptanceCriterion:
    criterion_id: str
    study_kind: StudyKind
    operator: CriterionOperator
    threshold: float
    unit: str
    source_id: str
    method_reference: str
    public_support: bool = False
    schema_version: str = STUDY_APPLICABILITY_SCHEMA_VERSION

    def __post_init__(self) -> None:
        for name, value in (
            ("criterion_id", self.criterion_id),
            ("unit", self.unit),
            ("source_id", self.source_id),
            ("method_reference", self.method_reference),
        ):
            if not isinstance(value, str) or not value.strip():
                raise ValueError(f"{name} must be non-empty text")
        if not isinstance(self.study_kind, StudyKind):
            raise TypeError("study_kind must be StudyKind")
        if not isinstance(self.operator, CriterionOperator):
            raise TypeError("operator must be CriterionOperator")
        if (
            not isinstance(self.threshold, (int, float))
            or isinstance(self.threshold, bool)
            or not math.isfinite(float(self.threshold))
        ):
            raise ValueError("threshold must be a finite number")


@dataclass(frozen=True)
class StudyApplicability:
    study_kind: StudyKind
    applicable: bool
    subject_id: str | None = None
    required_input_ids: tuple[str, ...] = ()
    missing_input_ids: tuple[str, ...] = ()
    criterion: AcceptanceCriterion | None = None
    reason: str | None = None
    schema_version: str = STUDY_APPLICABILITY_SCHEMA_VERSION

    def __post_init__(self) -> None:
        if not isinstance(self.study_kind, StudyKind):
            raise TypeError("study_kind must be StudyKind")
        for values, label in (
            (self.required_input_ids, "required_input_ids"),
            (self.missing_input_ids, "missing_input_ids"),
        ):
            if tuple(sorted(set(values))) != values:
                raise ValueError(f"{label} must be unique and sorted")
        if any(value not in self.required_input_ids for value in self.missing_input_ids):
            raise ValueError("missing inputs must be a subset of required inputs")
        if self.criterion is not None and self.criterion.study_kind is not self.study_kind:
            raise ValueError("criterion study kind must match applicability study kind")
        if not self.applicable and not self.reason:
            raise ValueError("non-applicable studies require a reason")

    @property
    def executable(self) -> bool:
        return self.applicable and not self.missing_input_ids

    @property
    def verdict_capable(self) -> bool:
        return self.executable and self.criterion is not None


def build_study_applicability(
    study_kind: StudyKind,
    *,
    subject_id: str | None = None,
    required_input_ids: tuple[str, ...] = (),
    available_input_ids: tuple[str, ...] = (),
    applicable: bool = True,
    criterion: AcceptanceCriterion | None = None,
    reason: str | None = None,
) -> StudyApplicability:
    required = tuple(sorted(set(required_input_ids)))
    available = set(available_input_ids)
    missing = tuple(value for value in required if value not in available)
    return StudyApplicability(
        study_kind=study_kind,
        applicable=applicable,
        subject_id=subject_id,
        required_input_ids=required,
        missing_input_ids=missing,
        criterion=criterion,
        reason=reason,
    )


def applicability_coverage(item: StudyApplicability) -> StudyCoverage:
    if not item.applicable:
        state = StudyState.NOT_APPLICABLE
        reason = item.reason
    elif item.missing_input_ids:
        state = StudyState.BLOCKED
        reason = "missing required inputs: " + ", ".join(item.missing_input_ids)
    else:
        state = StudyState.NOT_CHECKED
        reason = "study is applicable and ready but has not yet been executed"
    return StudyCoverage(
        study_id=item.study_kind.value,
        state=state,
        subject_id=item.subject_id,
        method_reference=(
            item.criterion.method_reference if item.criterion is not None else None
        ),
        evidence_source_ids=(
            (item.criterion.source_id,) if item.criterion is not None else ()
        ),
        reason=reason,
    )


def evaluate_criterion(
    value: float,
    unit: str,
    criterion: AcceptanceCriterion,
) -> bool:
    if not isinstance(value, (int, float)) or isinstance(value, bool) or not math.isfinite(float(value)):
        raise ValueError("study result must be a finite number")
    if unit != criterion.unit:
        raise ValueError("study result unit does not match acceptance criterion")
    if criterion.operator is CriterionOperator.MAXIMUM:
        return float(value) <= criterion.threshold
    return float(value) >= criterion.threshold
