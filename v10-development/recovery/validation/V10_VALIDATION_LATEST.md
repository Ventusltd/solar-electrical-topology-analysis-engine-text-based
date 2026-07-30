# V10 Validation Receipt

Generated UTC: `2026-07-30T14:55:33Z`  
Repository head: `3b4d6369a50a3bd53f4904257738b6638c26c66b`  
Overall result: `FAIL`  
Schema version: `globalgrid2050.v10-validation-receipt.v1`

## Declared suites

### python

Result: `FAIL`  
Return code: `1`  
Duration: `4.905 s`  
Working directory: `.`  
Command:

```text
/opt/hostedtoolcache/Python/3.11.15/x64/bin/python -m pytest -q
```

Output:

```text
......FF...F............................................................ [ 52%]
................................................................         [100%]
=================================== FAILURES ===================================
___ test_valid_model_requires_independent_validation_and_complete_traversal ____

    def test_valid_model_requires_independent_validation_and_complete_traversal() -> None:
        model = _valid_path()
        validation = validate_circuit_model(model)
>       assert validation.valid, validation.issues
E       AssertionError: (ValidationIssue(code='TERMINAL_CAPACITY_EXCEEDED', message="terminal 'a:right' has 2 connections, limit 1", severity=...nnections, limit 1", severity=<IssueSeverity.ERROR: 'error'>, object_id='b', terminal_id='b:left', connection_id=None))
E       assert False
E        +  where False = CircuitValidationResult(issues=(ValidationIssue(code='TERMINAL_CAPACITY_EXCEEDED', message="terminal 'a:right' has 2 c...nections, limit 1", severity=<IssueSeverity.ERROR: 'error'>, object_id='b', terminal_id='b:left', connection_id=None))).valid

tests/test_build023_topology_invariants.py:77: AssertionError
__________ test_payload_and_traversal_do_not_trust_input_tuple_order ___________

    def test_payload_and_traversal_do_not_trust_input_tuple_order() -> None:
        model = _valid_path()
        reordered = CircuitModel(
            model_id=model.model_id,
            objects=tuple(reversed(model.objects)),
            connections=tuple(reversed(model.connections)),
        )
        assert canonical_circuit_json(model) == canonical_circuit_json(reordered)
        traversal = verify_ordered_circuit(reordered, "a:left", "b:right")
>       assert traversal.valid
E       AssertionError: assert False
E        +  where False = OrderedCircuitTraversal(start_terminal_id='a:left', end_terminal_id='b:right', ordered_terminal_ids=(), ordered_connec...Y_EXCEEDED', terminal_id=None, connection_id=None),), schema_version='globalgrid2050.solar-dc.ordered-traversal.v10.1').valid

tests/test_build023_topology_invariants.py:104: AssertionError
______ test_segment_reference_cannot_substitute_for_terminal_connectivity ______

    def test_segment_reference_cannot_substitute_for_terminal_connectivity() -> None:
        model = _valid_path()
        bad = CircuitModel(
            model_id=model.model_id,
            objects=model.objects,
            connections=(
                Connection(
                    connection_id="c1",
                    from_terminal_id="a:left",
                    to_terminal_id="a:right",
                    kind=ConnectionKind.ELECTRICAL,
                    segment_id="segment-a",
                ),
                *model.connections[1:],
            ),
        )
        traversal = verify_ordered_circuit(bad, "a:left", "b:right")
        assert not traversal.valid
>       assert "SEGMENT_REFERENCE_NOT_INTERNAL" in traversal.error_codes
E       AssertionError: assert 'SEGMENT_REFERENCE_NOT_INTERNAL' in ('CIRCUIT_VALIDATION_FAILED',)
E        +  where ('CIRCUIT_VALIDATION_FAILED',) = OrderedCircuitTraversal(start_terminal_id='a:left', end_terminal_id='b:right', ordered_terminal_ids=(), ordered_connec...Y_EXCEEDED', terminal_id=None, connection_id=None),), schema_version='globalgrid2050.solar-dc.ordered-traversal.v10.1').error_codes

tests/test_build023_topology_invariants.py:187: AssertionError
=========================== short test summary info ============================
FAILED tests/test_build023_topology_invariants.py::test_valid_model_requires_independent_validation_and_complete_traversal - AssertionError: (ValidationIssue(code='TERMINAL_CAPACITY_EXCEEDED', message="terminal 'a:right' has 2 connections, limit 1", severity=...nnections, limit 1", severity=<IssueSeverity.ERROR: 'error'>, object_id='b', terminal_id='b:left', connection_id=None))
assert False
 +  where False = CircuitValidationResult(issues=(ValidationIssue(code='TERMINAL_CAPACITY_EXCEEDED', message="terminal 'a:right' has 2 c...nections, limit 1", severity=<IssueSeverity.ERROR: 'error'>, object_id='b', terminal_id='b:left', connection_id=None))).valid
FAILED tests/test_build023_topology_invariants.py::test_payload_and_traversal_do_not_trust_input_tuple_order - AssertionError: assert False
 +  where False = OrderedCircuitTraversal(start_terminal_id='a:left', end_terminal_id='b:right', ordered_terminal_ids=(), ordered_connec...Y_EXCEEDED', terminal_id=None, connection_id=None),), schema_version='globalgrid2050.solar-dc.ordered-traversal.v10.1').valid
FAILED tests/test_build023_topology_invariants.py::test_segment_reference_cannot_substitute_for_terminal_connectivity - AssertionError: assert 'SEGMENT_REFERENCE_NOT_INTERNAL' in ('CIRCUIT_VALIDATION_FAILED',)
 +  where ('CIRCUIT_VALIDATION_FAILED',) = OrderedCircuitTraversal(start_terminal_id='a:left', end_terminal_id='b:right', ordered_terminal_ids=(), ordered_connec...Y_EXCEEDED', terminal_id=None, connection_id=None),), schema_version='globalgrid2050.solar-dc.ordered-traversal.v10.1').error_codes
3 failed, 133 passed in 4.34s
```

### v8

Result: `PASS`  
Return code: `0`  
Duration: `0.075 s`  
Working directory: `.`  
Command:

```text
node --test tests/v8-model.test.js
```

Output:

```text
TAP version 13
# V8 regression tests passed: 13/13
# Subtest: /home/runner/work/solar-electrical-topology-analysis-engine-text-based/solar-electrical-topology-analysis-engine-text-based/tests/v8-model.test.js
ok 1 - /home/runner/work/solar-electrical-topology-analysis-engine-text-based/solar-electrical-topology-analysis-engine-text-based/tests/v8-model.test.js
  ---
  duration_ms: 36.075241
  ...
1..1
# tests 1
# suites 0
# pass 1
# fail 0
# cancelled 0
# skipped 0
# todo 0
# duration_ms 40.985632
```

### v9

Result: `PASS`  
Return code: `0`  
Duration: `0.039 s`  
Working directory: `.`  
Command:

```text
node v9-sandbox/debug/run-tests.mjs
```

Output:

```text
{
  "schema": "globalgrid2050.solar-dc-debug-test-report.v1",
  "generatedAt": "2026-07-30T14:55:33.521Z",
  "passed": 10,
  "failed": 0,
  "results": [
    {
      "name": "sequential order",
      "status": "pass",
      "detail": "ok"
    },
    {
      "name": "leapfrog order for 30 modules",
      "status": "pass",
      "detail": "ok"
    },
    {
      "name": "custom order accepts module numbers above four",
      "status": "pass",
      "detail": "ok"
    },
    {
      "name": "invalid custom order is rejected",
      "status": "pass",
      "detail": "ok"
    },
    {
      "name": "MPPT allocation caps active strings at 24",
      "status": "pass",
      "detail": "ok"
    },
    {
      "name": "12 MPPT by two inputs produces 24 strings",
      "status": "pass",
      "detail": "ok"
    },
    {
      "name": "corrected Voc default exceeds 1500 V",
      "status": "pass",
      "detail": "ok"
    },
    {
      "name": "copper resistance at 20 C",
      "status": "pass",
      "detail": "ok"
    },
    {
      "name": "segment count is modules plus one",
      "status": "pass",
      "detail": "ok"
    },
    {
      "name": "deterministic result excluding timestamp",
      "status": "pass",
      "detail": "ok"
    }
  ],
  "reviewQuestions": [
    "Does each formula use the correct physical quantity and temperature basis?",
    "Does the electrical order pass through every module exactly once?",
    "Are known routes, factory leads and provisional extensions separated?",
    "Are screening estimates clearly distinguished from construction quantities?",
    "Which missing physical objects block trusted EMC or transient studies?"
  ]
}
```

### v10-javascript

Result: `PASS`  
Return code: `0`  
Duration: `0.225 s`  
Working directory: `v10-development`  
Command:

```text
npm test
```

Output:

```text

> test
> node --test tests/*.test.mjs

TAP version 13
# Subtest: JavaScript matches the shared 20 C steady-state formula fixture
ok 1 - JavaScript matches the shared 20 C steady-state formula fixture
  ---
  duration_ms: 2.778122
  ...
# Subtest: quantity rejects unsupported units and propagates weakest provenance
ok 2 - quantity rejects unsupported units and propagates weakest provenance
  ---
  duration_ms: 1.529638
  ...
# Subtest: kernel computes geometry-derived resistance, voltage drop and power loss
ok 3 - kernel computes geometry-derived resistance, voltage drop and power loss
  ---
  duration_ms: 1.121537
  ...
# Subtest: kernel preserves uncertainty intervals through resistance and voltage drop
ok 4 - kernel preserves uncertainty intervals through resistance and voltage drop
  ---
  duration_ms: 0.35462
  ...
# Subtest: cold Voc candidate calculation is traceable and interval bounded
ok 5 - cold Voc candidate calculation is traceable and interval bounded
  ---
  duration_ms: 0.674776
  ...
# Subtest: kernel output is deterministic for identical JSON input
ok 6 - kernel output is deterministic for identical JSON input
  ---
  duration_ms: 1.141414
  ...
# Subtest: sequential order is deterministic
ok 7 - sequential order is deterministic
  ---
  duration_ms: 2.950552
  ...
# Subtest: mirrored sequential order is deterministic
ok 8 - mirrored sequential order is deterministic
  ---
  duration_ms: 0.276354
  ...
# Subtest: canonical leapfrog order is a complete permutation
ok 9 - canonical leapfrog order is a complete permutation
  ---
  duration_ms: 0.552438
  ...
# Subtest: custom order rejects duplicates and omissions
ok 10 - custom order rejects duplicates and omissions
  ---
  duration_ms: 0.512955
  ...
# Subtest: sequential path for 30 modules equals 29 pitches
ok 11 - sequential path for 30 modules equals 29 pitches
  ---
  duration_ms: 2.14898
  ...
# Subtest: canonical leapfrog path for 30 modules equals 57 pitches
ok 12 - canonical leapfrog path for 30 modules equals 57 pitches
  ---
  duration_ms: 0.274531
  ...
# Subtest: geometry output is deterministic
ok 13 - geometry output is deterministic
  ---
  duration_ms: 0.623791
  ...
1..13
# tests 13
# suites 0
# pass 13
# fail 0
# cancelled 0
# skipped 0
# todo 0
# duration_ms 87.137727
```

## Gate

One or more declared suites failed; authority promotion is blocked.

This receipt records execution only. It does not by itself promote an implementation to engineering authority.
