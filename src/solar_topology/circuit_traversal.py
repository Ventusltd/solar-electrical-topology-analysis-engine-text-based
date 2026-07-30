"""Independent ordered-circuit traversal verification for V10.

The verifier derives order from the terminal graph. It does not trust object order,
connection order, browser order or source segment indices.
"""

from __future__ import annotations

from collections import Counter, defaultdict
from dataclasses import dataclass

from .circuit import CircuitModel, Connection, ConnectionKind
from .circuit_validation import validate_circuit_model


TRAVERSAL_SCHEMA_VERSION = (
    "globalgrid2050.solar-dc.ordered-traversal.v10.1"
)


@dataclass(frozen=True)
class TraversalIssue:
    code: str
    message: str
    terminal_id: str | None = None
    connection_id: str | None = None

    @property
    def sort_key(self) -> tuple[str, str, str, str]:
        return (
            self.code,
            self.terminal_id or "",
            self.connection_id or "",
            self.message,
        )


@dataclass(frozen=True)
class OrderedCircuitTraversal:
    start_terminal_id: str
    end_terminal_id: str
    ordered_terminal_ids: tuple[str, ...]
    ordered_connection_ids: tuple[str, ...]
    ordered_segment_ids: tuple[str, ...]
    issues: tuple[TraversalIssue, ...]
    schema_version: str = TRAVERSAL_SCHEMA_VERSION

    @property
    def valid(self) -> bool:
        return not self.issues

    @property
    def error_codes(self) -> tuple[str, ...]:
        return tuple(sorted({issue.code for issue in self.issues}))

    def raise_for_errors(self) -> None:
        if self.valid:
            return
        raise ValueError(
            "invalid ordered circuit traversal: "
            + ", ".join(self.error_codes)
        )


def _other_terminal(connection: Connection, terminal_id: str) -> str:
    if connection.from_terminal_id == terminal_id:
        return connection.to_terminal_id
    if connection.to_terminal_id == terminal_id:
        return connection.from_terminal_id
    raise ValueError(
        f"connection {connection.connection_id!r} is not incident to "
        f"terminal {terminal_id!r}"
    )


def _empty_result(
    start_terminal_id: str,
    end_terminal_id: str,
    issues: list[TraversalIssue],
) -> OrderedCircuitTraversal:
    return OrderedCircuitTraversal(
        start_terminal_id=start_terminal_id,
        end_terminal_id=end_terminal_id,
        ordered_terminal_ids=(),
        ordered_connection_ids=(),
        ordered_segment_ids=(),
        issues=tuple(sorted(issues, key=lambda issue: issue.sort_key)),
    )


def verify_ordered_circuit(
    model: CircuitModel,
    start_terminal_id: str,
    end_terminal_id: str,
    *,
    expected_segment_ids: tuple[str, ...] | None = None,
) -> OrderedCircuitTraversal:
    """Verify that the complete model is one unambiguous ordered path.

    ``expected_segment_ids`` is optional comparison evidence. The traversal order is
    always derived from the terminal graph first.
    """

    issues: list[TraversalIssue] = []
    base_validation = validate_circuit_model(model)
    if not base_validation.valid:
        issues.append(
            TraversalIssue(
                code="CIRCUIT_VALIDATION_FAILED",
                message=(
                    "canonical circuit validation failed before traversal: "
                    + ", ".join(base_validation.error_codes)
                ),
            )
        )
        return _empty_result(start_terminal_id, end_terminal_id, issues)

    terminal_ids = {
        terminal.terminal_id
        for obj in model.objects
        for terminal in obj.terminals
    }
    if start_terminal_id not in terminal_ids:
        issues.append(
            TraversalIssue(
                code="START_TERMINAL_NOT_FOUND",
                message="start terminal is not declared in the circuit model",
                terminal_id=start_terminal_id,
            )
        )
    if end_terminal_id not in terminal_ids:
        issues.append(
            TraversalIssue(
                code="END_TERMINAL_NOT_FOUND",
                message="end terminal is not declared in the circuit model",
                terminal_id=end_terminal_id,
            )
        )
    if start_terminal_id == end_terminal_id:
        issues.append(
            TraversalIssue(
                code="IDENTICAL_TRAVERSAL_BOUNDARIES",
                message="start and end terminals must be different",
                terminal_id=start_terminal_id,
            )
        )
    if issues:
        return _empty_result(start_terminal_id, end_terminal_id, issues)

    adjacency: dict[str, list[Connection]] = defaultdict(list)
    for connection in model.connections:
        adjacency[connection.from_terminal_id].append(connection)
        adjacency[connection.to_terminal_id].append(connection)

        if (
            connection.segment_id is not None
            and connection.kind != ConnectionKind.INTERNAL
        ):
            issues.append(
                TraversalIssue(
                    code="SEGMENT_REFERENCE_NOT_INTERNAL",
                    message=(
                        "a segment_id may identify only the internal edge of "
                        "its physical segment object"
                    ),
                    connection_id=connection.connection_id,
                )
            )

    segment_reference_counts = Counter(
        connection.segment_id
        for connection in model.connections
        if connection.segment_id is not None
    )
    for segment_id, count in segment_reference_counts.items():
        if count != 1:
            issues.append(
                TraversalIssue(
                    code="DUPLICATE_SEGMENT_REFERENCE",
                    message=(
                        f"segment_id {segment_id!r} appears on {count} "
                        "connections"
                    ),
                )
            )

    for terminal_id in sorted(terminal_ids):
        degree = len(adjacency[terminal_id])
        if terminal_id in {start_terminal_id, end_terminal_id}:
            if degree != 1:
                issues.append(
                    TraversalIssue(
                        code="BOUNDARY_DEGREE_INVALID",
                        message=(
                            f"boundary terminal must have degree 1, got {degree}"
                        ),
                        terminal_id=terminal_id,
                    )
                )
        elif degree == 0:
            issues.append(
                TraversalIssue(
                    code="DISCONNECTED_TERMINAL",
                    message="non-boundary terminal has no incident connection",
                    terminal_id=terminal_id,
                )
            )
        elif degree == 1:
            issues.append(
                TraversalIssue(
                    code="EXTRA_CIRCUIT_ENDPOINT",
                    message=(
                        "a complete ordered circuit may have only the declared "
                        "start and end endpoints"
                    ),
                    terminal_id=terminal_id,
                )
            )
        elif degree > 2:
            issues.append(
                TraversalIssue(
                    code="BRANCH_DETECTED",
                    message=(
                        f"terminal has degree {degree}; simple string traversal "
                        "requires degree 2 internally"
                    ),
                    terminal_id=terminal_id,
                )
            )

    reachable: set[str] = set()
    stack = [start_terminal_id]
    while stack:
        terminal_id = stack.pop()
        if terminal_id in reachable:
            continue
        reachable.add(terminal_id)
        for connection in adjacency[terminal_id]:
            neighbour = _other_terminal(connection, terminal_id)
            if neighbour not in reachable:
                stack.append(neighbour)

    unreachable = sorted(terminal_ids - reachable)
    if unreachable:
        issues.append(
            TraversalIssue(
                code="DISCONNECTED_CIRCUIT_GRAPH",
                message=(
                    f"{len(unreachable)} declared terminals are outside the "
                    "start-terminal component"
                ),
                terminal_id=unreachable[0],
            )
        )

    if len(model.connections) != len(terminal_ids) - 1:
        issues.append(
            TraversalIssue(
                code="NON_PATH_EDGE_COUNT",
                message=(
                    "a connected simple path must contain exactly one fewer "
                    "connection than terminals"
                ),
            )
        )

    if issues:
        return _empty_result(start_terminal_id, end_terminal_id, issues)

    ordered_terminals = [start_terminal_id]
    ordered_connections: list[str] = []
    ordered_segments: list[str] = []
    visited_connection_ids: set[str] = set()
    previous_connection_id: str | None = None
    current_terminal_id = start_terminal_id

    while current_terminal_id != end_terminal_id:
        candidates = [
            connection
            for connection in adjacency[current_terminal_id]
            if connection.connection_id != previous_connection_id
            and connection.connection_id not in visited_connection_ids
        ]
        if len(candidates) != 1:
            issues.append(
                TraversalIssue(
                    code="AMBIGUOUS_NEXT_CONNECTION",
                    message=(
                        "graph walk did not produce exactly one next connection"
                    ),
                    terminal_id=current_terminal_id,
                )
            )
            break

        connection = candidates[0]
        visited_connection_ids.add(connection.connection_id)
        ordered_connections.append(connection.connection_id)
        if connection.segment_id is not None:
            ordered_segments.append(connection.segment_id)

        next_terminal_id = _other_terminal(
            connection,
            current_terminal_id,
        )
        ordered_terminals.append(next_terminal_id)
        previous_connection_id = connection.connection_id
        current_terminal_id = next_terminal_id

    if not issues and len(visited_connection_ids) != len(model.connections):
        issues.append(
            TraversalIssue(
                code="UNTRAVERSED_CONNECTIONS",
                message=(
                    "the declared boundary walk did not consume every connection"
                ),
            )
        )

    if (
        not issues
        and expected_segment_ids is not None
        and tuple(ordered_segments) != tuple(expected_segment_ids)
    ):
        issues.append(
            TraversalIssue(
                code="SEGMENT_ORDER_MISMATCH",
                message=(
                    "graph-derived segment order differs from the supplied "
                    "comparison sequence"
                ),
            )
        )

    return OrderedCircuitTraversal(
        start_terminal_id=start_terminal_id,
        end_terminal_id=end_terminal_id,
        ordered_terminal_ids=tuple(ordered_terminals),
        ordered_connection_ids=tuple(ordered_connections),
        ordered_segment_ids=tuple(ordered_segments),
        issues=tuple(sorted(issues, key=lambda issue: issue.sort_key)),
    )
