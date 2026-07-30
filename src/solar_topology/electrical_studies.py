"""Evidence-controlled electrical study receipts for V10.

The module calculates quantities from declared inputs and only creates an acceptance
verdict when an explicit, unit-matched criterion is supplied.
"""

from __future__ import annotations

from dataclasses import dataclass
import hashlib
import json
import math

from .diagnostics import (
    Diagnostic,
    DiagnosticCategory,
    DiagnosticReport,
    DiagnosticSeverity,
    StudyCoverage,
    StudyState,
    build_diagnostic_report,
)
from .formulas import cold_string_voc
from .study_applicability import AcceptanceCriterion, StudyKind, evaluate_criterion

ELECTRICAL_STUDY_SCHEMA_VERSION = "globalgrid2050.solar-dc.electrical-study.v10.1"


@dataclass(frozen=True)
class ElectricalStudyReceipt:
    study_id: str
    subject_id: str
    value: float
    unit: str
    input_values: tuple[tuple[str, float], ...]
    input_source_ids: tuple[str, ...]
    method_reference: str
    criterion: AcceptanceCriterion | None
    passed: bool | None
    diagnostic_report: DiagnosticReport
    schema_version: str = ELECTRICAL_STUDY_SCHEMA_VERSION

    def __post_init__(self) -> None:
        if not self.study_id or not self.subject_id or not self.unit:
            raise ValueError("study_id, subject_id and unit are required")
        if not math.isfinite(self.value):
            raise ValueError("study value must be finite")
        keys = [key for key, _ in self.input_values]
        if keys != sorted(keys) or len(keys) != len(set(keys)):
            raise ValueError("input_values must use unique sorted keys")
        if tuple(sorted(set(self.input_source_ids))) != self.input_source_ids:
            raise ValueError("input_source_ids must be unique and sorted")
        if self.criterion is None and self.passed is not None:
            raise ValueError("passed must be null when no criterion is supplied")


def _criterion_diagnostics(
    *,
    study_id: str,
    subject_id: str,
    value: float,
    unit: str,
    criterion: AcceptanceCriterion | None,
) -> tuple[bool | None, DiagnosticReport]:
    if criterion is None:
        return None, build_diagnostic_report(
            (),
            (
                StudyCoverage(
                    study_id=study_id,
                    state=StudyState.CHECKED_WARNING,
                    subject_id=subject_id,
                    reason=(
                        "quantity calculated but no acceptance criterion was supplied; "
                        "no compliance verdict is made"
                    ),
                ),
            ),
        )
    passed = evaluate_criterion(value, unit, criterion)
    if passed:
        diagnostics = ()
        state = StudyState.CHECKED_PASS
    else:
        diagnostics = (
            Diagnostic(
                code=f"ELECTRICAL.{study_id.upper().replace('-', '_')}.LIMIT",
                severity=DiagnosticSeverity.ERROR,
                category=DiagnosticCategory.ELECTRICAL,
                message=f"{study_id} result does not satisfy the declared criterion",
                subject_id=subject_id,
                observed_value=value,
                expected_constraint=(
                    f"{criterion.operator.value} {criterion.threshold} {criterion.unit}"
                ),
                method_reference=criterion.method_reference,
                source_reference=criterion.source_id,
                remediation="review design inputs, topology and the sourced acceptance basis",
            ),
        )
        state = StudyState.CHECKED_FAIL
    return passed, build_diagnostic_report(
        diagnostics,
        (
            StudyCoverage(
                study_id=study_id,
                state=state,
                subject_id=subject_id,
                method_reference=criterion.method_reference,
                evidence_source_ids=(criterion.source_id,),
            ),
        ),
    )


def calculate_cold_voc_study(
    *,
    subject_id: str,
    module_voc_v: float,
    modules_per_string: int,
    beta_voc_percent_per_k: float,
    cold_cell_temperature_c: float,
    input_source_ids: tuple[str, ...],
    criterion: AcceptanceCriterion | None = None,
) -> ElectricalStudyReceipt:
    if criterion is not None and criterion.study_kind is not StudyKind.COLD_VOC:
        raise ValueError("criterion must be for cold Voc")
    value = cold_string_voc(
        module_voc_v,
        modules_per_string,
        beta_voc_percent_per_k,
        cold_cell_temperature_c,
    )
    passed, report = _criterion_diagnostics(
        study_id="cold-voc-limit",
        subject_id=subject_id,
        value=value,
        unit="V",
        criterion=criterion,
    )
    return ElectricalStudyReceipt(
        study_id="cold-voc-limit",
        subject_id=subject_id,
        value=value,
        unit="V",
        input_values=tuple(
            sorted(
                (
                    ("beta_voc_percent_per_k", float(beta_voc_percent_per_k)),
                    ("cold_cell_temperature_c", float(cold_cell_temperature_c)),
                    ("module_voc_v", float(module_voc_v)),
                    ("modules_per_string", float(modules_per_string)),
                )
            )
        ),
        input_source_ids=tuple(sorted(set(input_source_ids))),
        method_reference="globalgrid2050.solar-dc.cold-voc.v10.1",
        criterion=criterion,
        passed=passed,
        diagnostic_report=report,
    )


def evaluate_numeric_study(
    *,
    study_id: str,
    study_kind: StudyKind,
    subject_id: str,
    value: float,
    unit: str,
    input_values: tuple[tuple[str, float], ...],
    input_source_ids: tuple[str, ...],
    method_reference: str,
    criterion: AcceptanceCriterion | None = None,
) -> ElectricalStudyReceipt:
    if criterion is not None and criterion.study_kind is not study_kind:
        raise ValueError("criterion study kind does not match study")
    if not math.isfinite(value):
        raise ValueError("study value must be finite")
    passed, report = _criterion_diagnostics(
        study_id=study_id,
        subject_id=subject_id,
        value=float(value),
        unit=unit,
        criterion=criterion,
    )
    return ElectricalStudyReceipt(
        study_id=study_id,
        subject_id=subject_id,
        value=float(value),
        unit=unit,
        input_values=input_values,
        input_source_ids=tuple(sorted(set(input_source_ids))),
        method_reference=method_reference,
        criterion=criterion,
        passed=passed,
        diagnostic_report=report,
    )


def electrical_study_payload(receipt: ElectricalStudyReceipt) -> dict[str, object]:
    criterion = receipt.criterion
    return {
        "schema_version": receipt.schema_version,
        "study_id": receipt.study_id,
        "subject_id": receipt.subject_id,
        "value": receipt.value,
        "unit": receipt.unit,
        "input_values": {key: value for key, value in receipt.input_values},
        "input_source_ids": list(receipt.input_source_ids),
        "method_reference": receipt.method_reference,
        "criterion": (
            None
            if criterion is None
            else {
                "criterion_id": criterion.criterion_id,
                "study_kind": criterion.study_kind.value,
                "operator": criterion.operator.value,
                "threshold": criterion.threshold,
                "unit": criterion.unit,
                "source_id": criterion.source_id,
                "method_reference": criterion.method_reference,
                "public_support": criterion.public_support,
            }
        ),
        "passed": receipt.passed,
        "diagnostic_report_id": receipt.diagnostic_report.report_id,
    }


def electrical_study_json(receipt: ElectricalStudyReceipt) -> str:
    return json.dumps(
        electrical_study_payload(receipt),
        sort_keys=True,
        separators=(",", ":"),
        ensure_ascii=False,
    )


def electrical_study_hash(receipt: ElectricalStudyReceipt) -> str:
    digest = hashlib.sha256(
        electrical_study_json(receipt).encode("utf-8")
    ).hexdigest()
    return f"sha256:{digest}"
