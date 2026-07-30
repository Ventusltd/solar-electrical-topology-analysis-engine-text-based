import pytest

from solar_topology.identifiers import (
    CanonicalIdentifier,
    EntityLevel,
    parse_identifier,
    project_id,
    require_unique_identifiers,
)


def _full_identifier():
    project = project_id("public-cleve-hill-study")
    site = project.child(EntityLevel.SITE, "site-001")
    system = site.child(EntityLevel.SYSTEM, "dc-array")
    equipment = system.child(EntityLevel.EQUIPMENT, "inverter-001")
    circuit = equipment.child(EntityLevel.CIRCUIT, "mppt-01-string-01")
    return circuit.child(EntityLevel.OBJECT, "segment-001")


def test_identifier_builds_deterministic_contiguous_path():
    identifier = _full_identifier()
    assert identifier.value == (
        "project:public-cleve-hill-study/site:site-001/system:dc-array/"
        "equipment:inverter-001/circuit:mppt-01-string-01/object:segment-001"
    )


def test_identifier_round_trip():
    identifier = _full_identifier()
    parsed = parse_identifier(identifier.value)
    assert parsed == identifier
    assert parsed.value == identifier.value


def test_identifier_rejects_noncanonical_tokens():
    with pytest.raises(ValueError, match="lowercase kebab-case"):
        project_id("Cleve Hill")
    with pytest.raises(ValueError, match="lowercase kebab-case"):
        project_id("cleve_hill")


def test_identifier_rejects_skipped_hierarchy_level():
    project = project_id("study")
    with pytest.raises(ValueError, match="immediately preceding"):
        CanonicalIdentifier(EntityLevel.SYSTEM, "dc-array", project)


def test_parser_rejects_noncontiguous_hierarchy():
    with pytest.raises(ValueError, match="contiguous"):
        parse_identifier("project:study/system:dc-array")


def test_uniqueness_gate_rejects_duplicates():
    identifier = _full_identifier()
    with pytest.raises(ValueError, match="unique"):
        require_unique_identifiers([identifier, identifier])


def test_identical_local_ids_are_allowed_under_distinct_parents():
    project = project_id("study")
    site_a = project.child(EntityLevel.SITE, "site-a")
    site_b = project.child(EntityLevel.SITE, "site-b")
    first = site_a.child(EntityLevel.SYSTEM, "dc-array")
    second = site_b.child(EntityLevel.SYSTEM, "dc-array")
    require_unique_identifiers([first, second])
    assert first.value != second.value
