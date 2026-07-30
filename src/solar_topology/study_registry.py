"""Applicability and coverage registry for V10 engineering studies.

The registry prevents absence of a diagnostic from being misread as a passed study.
Acceptance criteria remain evidence-bearing inputs rather than invented constants.
"""

from __future__ import annotations

from dataclasses import dataclass
from enum import StrEnum
import hashlib
import json
from typing import Iterable

from .diagnostics import StudyCoverage, StudyState

STUDY_REGISTRY_SCHEMA_VERSION = "globalgrid2050.solar-dc.study-registry.v10.1"


class StudyCategory(StrEnum):
    TOPOLOGY = "topology"
    STEADY_STATE = "steady_state"
    THERMAL = "thermal"
    INSULATION = "insulation"
    TRANSIENT = "transient"
    LIGHTNING = "lightning"
    EVIDENCE = "evidence"
    PUBLICATION = "publication"


def _validate_sorted_unique(
    values: tuple[str, ...], *, study_id: str, field_name: str
) -> None:
    """Fail fast with the exact registry declaration that is malformed."""
    expected = tuple(sorted(set(values)))
    if values != expected:
        raise ValueError(
            f"study_id={study_id!r} field={field_name!r} must be unique and sorted; "
            f"received={values!r}; expected={expected!r}"
        )


@dataclass(frozen=True)
class StudyDefinition:
    study_id: str
    category: StudyCategory
    title: str
    method_reference: str
    required_input_ids: tuple[str, ...] = ()
    required_evidence_roles: tuple[str, ...] = ()
    acceptance_criterion_required: bool = False
    public_description: str | None = None

    def __post_init__(self) -> None:
        if not self.study_id or not self.title or not self.method_reference:
            raise ValueError("study_id, title and method_reference are required")
        if not isinstance(self.category, StudyCategory):
            raise TypeError("category must be StudyCategory")
        _validate_sorted_unique(
            self.required_input_ids,
            study_id=self.study_id,
            field_name="required_input_ids",
        )
        _validate_sorted_unique(
            self.required_evidence_roles,
            study_id=self.study_id,
            field_name="required_evidence_roles",
        )


@dataclass(frozen=True)
class StudyAssessment:
    definition: StudyDefinition
    coverage: StudyCoverage
    missing_input_ids: tuple[str, ...] = ()
    missing_evidence_roles: tuple[str, ...] = ()
    acceptance_criterion_source: str | None = None


@dataclass(frozen=True)
class StudyRegistry:
    definitions: tuple[StudyDefinition, ...]
    assessments: tuple[StudyAssessment, ...]
    schema_version: str = STUDY_REGISTRY_SCHEMA_VERSION


def assess_study(
    definition: StudyDefinition,
    *,
    subject_id: str | None,
    available_input_ids: Iterable[str],
    available_evidence_roles: Iterable[str],
    applicable: bool = True,
    performed: bool = False,
    passed: bool | None = None,
    warning: bool = False,
    acceptance_criterion_source: str | None = None,
) -> StudyAssessment:
    inputs = set(available_input_ids)
    evidence = set(available_evidence_roles)
    missing_inputs = tuple(sorted(set(definition.required_input_ids) - inputs))
    missing_evidence = tuple(
        sorted(set(definition.required_evidence_roles) - evidence)
    )
    if not applicable:
        state = StudyState.NOT_APPLICABLE
        reason = "study is not applicable to the declared system boundary"
    elif missing_inputs or missing_evidence:
        state = StudyState.BLOCKED
        reason = "missing required inputs or evidence"
    elif definition.acceptance_criterion_required and not acceptance_criterion_source:
        state = StudyState.BLOCKED
        reason = "acceptance criterion source is not declared"
    elif not performed:
        state = StudyState.NOT_CHECKED
        reason = "study inputs are available but the study was not performed"
    elif passed is False:
        state = StudyState.CHECKED_FAIL
        reason = None
    elif warning:
        state = StudyState.CHECKED_WARNING
        reason = None
    else:
        state = StudyState.CHECKED_PASS
        reason = None
    coverage = StudyCoverage(
        study_id=definition.study_id,
        state=state,
        subject_id=subject_id,
        method_reference=definition.method_reference,
        reason=reason,
    )
    return StudyAssessment(
        definition=definition,
        coverage=coverage,
        missing_input_ids=missing_inputs,
        missing_evidence_roles=missing_evidence,
        acceptance_criterion_source=acceptance_criterion_source,
    )


def build_study_registry(
    assessments: Iterable[StudyAssessment],
) -> StudyRegistry:
    ordered = tuple(
        sorted(assessments, key=lambda item: item.definition.study_id)
    )
    ids = [item.definition.study_id for item in ordered]
    if len(ids) != len(set(ids)):
        raise ValueError("study definitions must be unique")
    return StudyRegistry(
        definitions=tuple(item.definition for item in ordered),
        assessments=ordered,
    )


def study_registry_payload(registry: StudyRegistry) -> dict[str, object]:
    return {
        "schema_version": registry.schema_version,
        "studies": [
            {
                "study_id": item.definition.study_id,
                "category": item.definition.category.value,
                "title": item.definition.title,
                "method_reference": item.definition.method_reference,
                "required_input_ids": list(item.definition.required_input_ids),
                "required_evidence_roles": list(
                    item.definition.required_evidence_roles
                ),
                "acceptance_criterion_required": (
                    item.definition.acceptance_criterion_required
                ),
                "public_description": item.definition.public_description,
                "state": item.coverage.state.value,
                "subject_id": item.coverage.subject_id,
                "reason": item.coverage.reason,
                "missing_input_ids": list(item.missing_input_ids),
                "missing_evidence_roles": list(item.missing_evidence_roles),
                "acceptance_criterion_source": (
                    item.acceptance_criterion_source
                ),
            }
            for item in registry.assessments
        ],
    }


def study_registry_json(registry: StudyRegistry) -> str:
    return json.dumps(
        study_registry_payload(registry),
        sort_keys=True,
        separators=(",", ":"),
        ensure_ascii=False,
    )


def study_registry_hash(registry: StudyRegistry) -> str:
    digest = hashlib.sha256(
        study_registry_json(registry).encode("utf-8")
    ).hexdigest()
    return f"sha256:{digest}"


INITIAL_STUDIES = (
    StudyDefinition(
        study_id="complete-circuit-resistance",
        category=StudyCategory.STEADY_STATE,
        title="Complete series-circuit resistance",
        method_reference="globalgrid2050.solar-dc.complete-circuit.v10.1",
        required_input_ids=("current-a", "ordered-segments"),
        required_evidence_roles=("conductor-data", "route-geometry"),
    ),
    StudyDefinition(
        study_id="voltage-drop-acceptance",
        category=StudyCategory.STEADY_STATE,
        title="Voltage-drop acceptance",
        method_reference="globalgrid2050.solar-dc.voltage-drop.v10.1",
        required_input_ids=("current-a", "string-vmp-v"),
        required_evidence_roles=("complete-circuit-resistance",),
        acceptance_criterion_required=True,
    ),
    StudyDefinition(
        study_id="cold-voc-limit",
        category=StudyCategory.STEADY_STATE,
        title="Cold string open-circuit voltage limit",
        method_reference="globalgrid2050.solar-dc.cold-voc.v10.1",
        required_input_ids=(
            "beta-voc-percent-per-k",
            "cold-cell-temperature-c",
            "module-voc-v",
            "modules-per-string",
            "system-maximum-voltage-v",
        ),
        required_evidence_roles=("module-datasheet", "system-voltage-basis"),
    ),
    StudyDefinition(
        study_id="loop-geometry",
        category=StudyCategory.TRANSIENT,
        title="Differential loop geometry",
        method_reference="globalgrid2050.solar-dc.geometry-receipt.v10.1",
        required_input_ids=("ordered-segments",),
        required_evidence_roles=("pole-separation", "route-geometry"),
    ),
    StudyDefinition(
        study_id="ampacity-acceptance",
        category=StudyCategory.THERMAL,
        title="Conductor ampacity acceptance",
        method_reference="globalgrid2050.solar-dc.ampacity.v10.1",
        required_input_ids=("design-current-a", "installation-class"),
        required_evidence_roles=("cable-rating-basis",),
        acceptance_criterion_required=True,
    ),
)
