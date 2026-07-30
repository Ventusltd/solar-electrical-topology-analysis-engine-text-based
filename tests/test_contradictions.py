import pytest

from solar_topology.contradictions import (
    Claim,
    Contradiction,
    ContradictionSeverity,
    ContradictionStatus,
    build_contradiction_register,
    contradiction_register_hash,
    contradiction_register_json,
    unresolved_contradictions,
)
from solar_topology.identifiers import EntityLevel, project_id


def _subject():
    project = project_id("public-study")
    site = project.child(EntityLevel.SITE, "site-01")
    return site.child(EntityLevel.SYSTEM, "dc-array")


def _claim(claim_id, value, source_id="public-source"):
    return Claim(
        claim_id=claim_id,
        subject_identifier=_subject(),
        predicate="string-count",
        value=value,
        unit="count",
        source_id=source_id,
    )


def test_register_is_deterministic_under_input_reordering():
    first = Contradiction(
        "ctr-002", _claim("claim-b", 24), _claim("claim-c", 32),
        ContradictionSeverity.MATERIAL,
    )
    second = Contradiction(
        "ctr-001", _claim("claim-a", 24), _claim("claim-d", 28),
        ContradictionSeverity.INFORMATIONAL,
    )
    a = build_contradiction_register([first, second])
    b = build_contradiction_register([second, first])
    assert contradiction_register_json(a) == contradiction_register_json(b)
    assert contradiction_register_hash(a) == contradiction_register_hash(b)


def test_equal_values_are_not_a_contradiction():
    with pytest.raises(ValueError, match="equal claim values"):
        Contradiction(
            "ctr-001", _claim("claim-a", 24), _claim("claim-b", 24),
            ContradictionSeverity.MATERIAL,
        )


def test_closed_contradiction_requires_resolution_note():
    with pytest.raises(ValueError, match="resolution_note"):
        Contradiction(
            "ctr-001", _claim("claim-a", 24), _claim("claim-b", 32),
            ContradictionSeverity.MATERIAL,
            status=ContradictionStatus.RESOLVED,
        )


def test_duplicate_claim_pair_is_rejected_even_when_reversed():
    left = _claim("claim-a", 24)
    right = _claim("claim-b", 32)
    with pytest.raises(ValueError, match="claim pair"):
        build_contradiction_register([
            Contradiction("ctr-001", left, right, ContradictionSeverity.MATERIAL),
            Contradiction("ctr-002", right, left, ContradictionSeverity.MATERIAL),
        ])


def test_unresolved_filter_honours_severity_threshold():
    register = build_contradiction_register([
        Contradiction(
            "ctr-info", _claim("claim-a", 24), _claim("claim-b", 25),
            ContradictionSeverity.INFORMATIONAL,
        ),
        Contradiction(
            "ctr-safety", _claim("claim-c", 24), _claim("claim-d", 32),
            ContradictionSeverity.SAFETY_CRITICAL,
        ),
        Contradiction(
            "ctr-resolved", _claim("claim-e", 24), _claim("claim-f", 30),
            ContradictionSeverity.MATERIAL,
            status=ContradictionStatus.RESOLVED,
            resolution_note="public survey superseded the earlier estimate",
        ),
    ])
    result = unresolved_contradictions(
        register, minimum_severity=ContradictionSeverity.MATERIAL
    )
    assert [item.contradiction_id for item in result] == ["ctr-safety"]
