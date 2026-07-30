"""Independent validation for the canonical V10 circuit model."""

from __future__ import annotations

from collections import Counter
from dataclasses import dataclass
from enum import StrEnum
import hashlib
import math

from .circuit import (
    CIRCUIT_SCHEMA_VERSION,
    CircuitModel,
    ConnectionKind,
    EvidenceClass,
    ObjectKind,
    ScalarValue,
    TerminalPolarity,
    canonical_circuit_json,
)


class IssueSeverity(StrEnum):
    ERROR = "error"
    WARNING = "warning"


@dataclass(frozen=True)
class ValidationIssue:
    code: str
    message: str
    severity: IssueSeverity = IssueSeverity.ERROR
    object_id: str | None = None
    terminal_id: str | None = None
    connection_id: str | None = None

    @property
    def sort_key(self) -> tuple[str, ...]:
        return (
            str(self.severity),
            self.code,
            self.object_id or "",
            self.terminal_id or "",
            self.connection_id or "",
            self.message,
        )


@dataclass(frozen=True)
class CircuitValidationResult:
    issues: tuple[ValidationIssue, ...]

    @property
    def valid(self) -> bool:
        return not any(
            issue.severity == IssueSeverity.ERROR
            for issue in self.issues
        )

    @property
    def error_codes(self) -> tuple[str, ...]:
        return tuple(
            sorted(
                {
                    issue.code
                    for issue in self.issues
                    if issue.severity == IssueSeverity.ERROR
                }
            )
        )

    def raise_for_errors(self) -> None:
        if self.valid:
            return
        codes = ", ".join(self.error_codes)
        raise ValueError(f"invalid circuit model: {codes}")


def _has_text(value: object) -> bool:
    return isinstance(value, str) and bool(value.strip())


def _valid_scalar(value: object) -> bool:
    if value is None or isinstance(value, (str, bool, int)):
        return True
    return isinstance(value, float) and math.isfinite(value)


def _check_attribute_items(
    items: tuple[tuple[str, ScalarValue], ...],
    *,
    owner_label: str,
    issue_factory,
) -> list[ValidationIssue]:
    issues: list[ValidationIssue] = []
    keys: list[str] = []
    for item in items:
        if not isinstance(item, tuple) or len(item) != 2:
            issues.append(
                issue_factory(
                    "INVALID_ATTRIBUTE_ITEM",
                    f"{owner_label} attributes must be key/value tuples",
                )
            )
            continue
        key, value = item
        if not _has_text(key):
            issues.append(
                issue_factory(
                    "INVALID_ATTRIBUTE_KEY",
                    f"{owner_label} attribute keys must be non-empty strings",
                )
            )
        else:
            keys.append(key)
        if not _valid_scalar(value):
            issues.append(
                issue_factory(
                    "INVALID_ATTRIBUTE_VALUE",
                    f"{owner_label} attribute values must be finite scalar values",
                )
            )

    for key, count in Counter(keys).items():
        if count > 1:
            issues.append(
                issue_factory(
                    "DUPLICATE_ATTRIBUTE_KEY",
                    f"{owner_label} repeats attribute key {key}",
                )
            )
    return issues


def _parent_cycle_issues(
    parent_by_object: dict[str, str | None],
) -> list[ValidationIssue]:
    issues: list[ValidationIssue] = []
    reported: set[tuple[str, ...]] = set()

    for start in sorted(parent_by_object):
        path: list[str] = []
        position: dict[str, int] = {}
        current: str | None = start

        while current is not None and current in parent_by_object:
            if current in position:
                cycle = tuple(path[position[current]:])
                canonical_cycle = tuple(sorted(cycle))
                if canonical_cycle not in reported:
                    reported.add(canonical_cycle)
                    issues.append(
                        ValidationIssue(
                            code="PARENT_CYCLE",
                            message=(
                                "object parent cycle contains "
                                + ", ".join(canonical_cycle)
                            ),
                            object_id=canonical_cycle[0],
                        )
                    )
                break
            position[current] = len(path)
            path.append(current)
            current = parent_by_object[current]

    return issues


def validate_circuit_model(model: CircuitModel) -> CircuitValidationResult:
    """Validate identity, ownership, connectivity and deterministic data laws."""

    issues: list[ValidationIssue] = []

    if not isinstance(model, CircuitModel):
        return CircuitValidationResult(
            (
                ValidationIssue(
                    code="INVALID_MODEL_TYPE",
                    message="model must be a CircuitModel",
                ),
            )
        )

    if not _has_text(model.model_id):
        issues.append(
            ValidationIssue(
                code="MISSING_MODEL_ID",
                message="model_id must be a non-empty string",
            )
        )
    if model.schema_version != CIRCUIT_SCHEMA_VERSION:
        issues.append(
            ValidationIssue(
                code="UNSUPPORTED_SCHEMA_VERSION",
                message=(
                    f"schema_version must be {CIRCUIT_SCHEMA_VERSION}"
                ),
            )
        )
    if not model.objects:
        issues.append(
            ValidationIssue(
                code="EMPTY_OBJECT_SET",
                message="a circuit model must contain at least one object",
            )
        )

    issues.extend(
        _check_attribute_items(
            model.metadata,
            owner_label="model",
            issue_factory=lambda code, message: ValidationIssue(
                code=code,
                message=message,
            ),
        )
    )

    object_counts = Counter(obj.object_id for obj in model.objects)
    for object_id, count in object_counts.items():
        if count > 1:
            issues.append(
                ValidationIssue(
                    code="DUPLICATE_OBJECT_ID",
                    message=f"object_id {object_id!r} occurs {count} times",
                    object_id=object_id,
                )
            )

    object_by_id = {}
    terminal_by_id = {}
    terminal_counts: Counter[str] = Counter()
    parent_by_object: dict[str, str | None] = {}

    for obj in model.objects:
        if not _has_text(obj.object_id):
            issues.append(
                ValidationIssue(
                    code="MISSING_OBJECT_ID",
                    message="object_id must be a non-empty string",
                )
            )
        elif obj.object_id not in object_by_id:
            object_by_id[obj.object_id] = obj
            parent_by_object[obj.object_id] = obj.parent_object_id

        if not isinstance(obj.kind, ObjectKind):
            issues.append(
                ValidationIssue(
                    code="INVALID_OBJECT_KIND",
                    message=f"object {obj.object_id!r} has an invalid kind",
                    object_id=obj.object_id,
                )
            )
        if not isinstance(obj.evidence_class, EvidenceClass):
            issues.append(
                ValidationIssue(
                    code="INVALID_EVIDENCE_CLASS",
                    message=(
                        f"object {obj.object_id!r} has an invalid evidence class"
                    ),
                    object_id=obj.object_id,
                )
            )
        if obj.parent_object_id is not None:
            if not _has_text(obj.parent_object_id):
                issues.append(
                    ValidationIssue(
                        code="INVALID_PARENT_OBJECT_ID",
                        message=(
                            "parent_object_id must be null or a non-empty string"
                        ),
                        object_id=obj.object_id,
                    )
                )
            elif obj.parent_object_id == obj.object_id:
                issues.append(
                    ValidationIssue(
                        code="SELF_PARENT",
                        message="an object cannot be its own parent",
                        object_id=obj.object_id,
                    )
                )

        issues.extend(
            _check_attribute_items(
                obj.attributes,
                owner_label=f"object {obj.object_id!r}",
                issue_factory=(
                    lambda code, message, object_id=obj.object_id: ValidationIssue(
                        code=code,
                        message=message,
                        object_id=object_id,
                    )
                ),
            )
        )

        local_terminal_ids = [
            terminal.terminal_id for terminal in obj.terminals
        ]
        for terminal_id, count in Counter(local_terminal_ids).items():
            if count > 1:
                issues.append(
                    ValidationIssue(
                        code="DUPLICATE_TERMINAL_ID_IN_OBJECT",
                        message=(
                            f"terminal_id {terminal_id!r} occurs {count} times "
                            f"inside object {obj.object_id!r}"
                        ),
                        object_id=obj.object_id,
                        terminal_id=terminal_id,
                    )
                )

        for terminal in obj.terminals:
            terminal_counts[terminal.terminal_id] += 1
            if terminal.terminal_id not in terminal_by_id:
                terminal_by_id[terminal.terminal_id] = terminal

            if not _has_text(terminal.terminal_id):
                issues.append(
                    ValidationIssue(
                        code="MISSING_TERMINAL_ID",
                        message="terminal_id must be a non-empty string",
                        object_id=obj.object_id,
                    )
                )
            if terminal.object_id != obj.object_id:
                issues.append(
                    ValidationIssue(
                        code="TERMINAL_OWNER_MISMATCH",
                        message=(
                            f"terminal {terminal.terminal_id!r} declares owner "
                            f"{terminal.object_id!r} but is stored on "
                            f"{obj.object_id!r}"
                        ),
                        object_id=obj.object_id,
                        terminal_id=terminal.terminal_id,
                    )
                )
            if not isinstance(terminal.polarity, TerminalPolarity):
                issues.append(
                    ValidationIssue(
                        code="INVALID_TERMINAL_POLARITY",
                        message=(
                            f"terminal {terminal.terminal_id!r} has invalid polarity"
                        ),
                        object_id=obj.object_id,
                        terminal_id=terminal.terminal_id,
                    )
                )
            if not isinstance(terminal.evidence_class, EvidenceClass):
                issues.append(
                    ValidationIssue(
                        code="INVALID_EVIDENCE_CLASS",
                        message=(
                            f"terminal {terminal.terminal_id!r} has invalid "
                            "evidence class"
                        ),
                        object_id=obj.object_id,
                        terminal_id=terminal.terminal_id,
                    )
                )
            if (
                not isinstance(terminal.max_connections, int)
                or isinstance(terminal.max_connections, bool)
                or terminal.max_connections < 1
            ):
                issues.append(
                    ValidationIssue(
                        code="INVALID_TERMINAL_CAPACITY",
                        message="max_connections must be a positive integer",
                        object_id=obj.object_id,
                        terminal_id=terminal.terminal_id,
                    )
                )
            if terminal.position is not None:
                coordinates = (
                    terminal.position.x,
                    terminal.position.y,
                    terminal.position.z,
                )
                if not all(
                    isinstance(value, (int, float))
                    and not isinstance(value, bool)
                    and math.isfinite(value)
                    for value in coordinates
                ):
                    issues.append(
                        ValidationIssue(
                            code="INVALID_TERMINAL_POSITION",
                            message=(
                                "terminal coordinates must be finite numbers"
                            ),
                            object_id=obj.object_id,
                            terminal_id=terminal.terminal_id,
                        )
                    )

    for terminal_id, count in terminal_counts.items():
        if count > 1:
            issues.append(
                ValidationIssue(
                    code="DUPLICATE_TERMINAL_ID",
                    message=f"terminal_id {terminal_id!r} occurs {count} times",
                    terminal_id=terminal_id,
                )
            )

    for object_id, parent_id in parent_by_object.items():
        if parent_id is not None and parent_id not in object_by_id:
            issues.append(
                ValidationIssue(
                    code="MISSING_PARENT_OBJECT",
                    message=(
                        f"object {object_id!r} references missing parent "
                        f"{parent_id!r}"
                    ),
                    object_id=object_id,
                )
            )
    issues.extend(_parent_cycle_issues(parent_by_object))

    connection_id_counts = Counter(
        connection.connection_id
        for connection in model.connections
    )
    for connection_id, count in connection_id_counts.items():
        if count > 1:
            issues.append(
                ValidationIssue(
                    code="DUPLICATE_CONNECTION_ID",
                    message=(
                        f"connection_id {connection_id!r} occurs {count} times"
                    ),
                    connection_id=connection_id,
                )
            )

    terminal_connection_counts: Counter[str] = Counter()
    seen_pairs: set[tuple[str, str, str]] = set()

    for connection in model.connections:
        if not _has_text(connection.connection_id):
            issues.append(
                ValidationIssue(
                    code="MISSING_CONNECTION_ID",
                    message="connection_id must be a non-empty string",
                )
            )
        if not isinstance(connection.kind, ConnectionKind):
            issues.append(
                ValidationIssue(
                    code="INVALID_CONNECTION_KIND",
                    message=(
                        f"connection {connection.connection_id!r} has invalid kind"
                    ),
                    connection_id=connection.connection_id,
                )
            )
        if not isinstance(connection.evidence_class, EvidenceClass):
            issues.append(
                ValidationIssue(
                    code="INVALID_EVIDENCE_CLASS",
                    message=(
                        f"connection {connection.connection_id!r} has invalid "
                        "evidence class"
                    ),
                    connection_id=connection.connection_id,
                )
            )
        if connection.segment_id is not None and not _has_text(
            connection.segment_id
        ):
            issues.append(
                ValidationIssue(
                    code="INVALID_SEGMENT_ID",
                    message="segment_id must be null or a non-empty string",
                    connection_id=connection.connection_id,
                )
            )

        endpoints = (
            connection.from_terminal_id,
            connection.to_terminal_id,
        )
        for terminal_id in endpoints:
            if not _has_text(terminal_id):
                issues.append(
                    ValidationIssue(
                        code="MISSING_CONNECTION_ENDPOINT",
                        message=(
                            "connection endpoints must be non-empty strings"
                        ),
                        connection_id=connection.connection_id,
                    )
                )
            elif terminal_id not in terminal_by_id:
                issues.append(
                    ValidationIssue(
                        code="UNRESOLVED_TERMINAL_REFERENCE",
                        message=(
                            f"connection {connection.connection_id!r} references "
                            f"missing terminal {terminal_id!r}"
                        ),
                        terminal_id=terminal_id,
                        connection_id=connection.connection_id,
                    )
                )
            else:
                terminal_connection_counts[terminal_id] += 1

        if (
            _has_text(connection.from_terminal_id)
            and connection.from_terminal_id == connection.to_terminal_id
        ):
            issues.append(
                ValidationIssue(
                    code="SELF_CONNECTION",
                    message="a connection cannot join a terminal to itself",
                    terminal_id=connection.from_terminal_id,
                    connection_id=connection.connection_id,
                )
            )

        if all(_has_text(terminal_id) for terminal_id in endpoints):
            pair = tuple(sorted(endpoints))
            pair_key = (pair[0], pair[1], str(connection.kind))
            if pair_key in seen_pairs:
                issues.append(
                    ValidationIssue(
                        code="DUPLICATE_CONNECTION_PAIR",
                        message=(
                            "the same terminal pair and connection kind "
                            "appears more than once"
                        ),
                        connection_id=connection.connection_id,
                    )
                )
            seen_pairs.add(pair_key)

    for terminal_id, terminal in terminal_by_id.items():
        count = terminal_connection_counts[terminal_id]
        if terminal.required_connection and count == 0:
            issues.append(
                ValidationIssue(
                    code="DANGLING_REQUIRED_TERMINAL",
                    message=(
                        f"required terminal {terminal_id!r} has no connection"
                    ),
                    object_id=terminal.object_id,
                    terminal_id=terminal_id,
                )
            )
        if (
            isinstance(terminal.max_connections, int)
            and not isinstance(terminal.max_connections, bool)
            and count > terminal.max_connections
        ):
            issues.append(
                ValidationIssue(
                    code="TERMINAL_CAPACITY_EXCEEDED",
                    message=(
                        f"terminal {terminal_id!r} has {count} connections, "
                        f"limit {terminal.max_connections}"
                    ),
                    object_id=terminal.object_id,
                    terminal_id=terminal_id,
                )
            )

    return CircuitValidationResult(
        tuple(sorted(issues, key=lambda issue: issue.sort_key))
    )


def validated_circuit_hash(model: CircuitModel) -> str:
    """Return a prefixed deterministic hash only for a valid circuit model."""

    result = validate_circuit_model(model)
    result.raise_for_errors()
    digest = hashlib.sha256(
        canonical_circuit_json(model).encode("utf-8")
    ).hexdigest()
    return f"sha256:{digest}"
