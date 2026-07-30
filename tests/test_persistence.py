import json

import pytest

from solar_topology.persistence import (
    PersistedRecord,
    build_deterministic_record_store,
    deterministic_store_hash,
    deterministic_store_json,
    persist_record,
    read_back_store,
)


def _record(record_id, value):
    return persist_record(
        record_id=record_id,
        record_type="fixture",
        source_schema_version="fixture.v1",
        payload={"value": value, "nested": {"b": 2, "a": 1}},
    )


def test_store_is_deterministic_under_record_reordering():
    first = build_deterministic_record_store([_record("b", 2), _record("a", 1)])
    second = build_deterministic_record_store([_record("a", 1), _record("b", 2)])
    assert deterministic_store_json(first) == deterministic_store_json(second)
    assert deterministic_store_hash(first) == deterministic_store_hash(second)


def test_read_back_reconstructs_identical_store():
    store = build_deterministic_record_store([_record("a", 1), _record("b", 2)])
    serialised = deterministic_store_json(store)
    recovered = read_back_store(serialised)
    assert recovered == store
    assert deterministic_store_hash(recovered) == deterministic_store_hash(store)


def test_tampered_payload_is_rejected():
    record = _record("a", 1)
    with pytest.raises(ValueError, match="payload_hash"):
        PersistedRecord(
            record_id=record.record_id,
            record_type=record.record_type,
            source_schema_version=record.source_schema_version,
            payload_json='{"value":2}',
            payload_hash=record.payload_hash,
        )


def test_noncanonical_serialisation_is_rejected_on_read_back():
    store = build_deterministic_record_store([_record("a", 1)])
    noncanonical = json.dumps(json.loads(deterministic_store_json(store)), indent=2)
    with pytest.raises(ValueError, match="not canonical"):
        read_back_store(noncanonical)


def test_duplicate_record_identifiers_are_rejected():
    with pytest.raises(ValueError, match="identifiers must be unique"):
        build_deterministic_record_store([_record("a", 1), _record("a", 2)])
