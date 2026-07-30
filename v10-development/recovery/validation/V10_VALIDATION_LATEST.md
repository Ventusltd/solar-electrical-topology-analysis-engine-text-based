# V10 Validation Receipt

Generated UTC: `2026-07-30T13:25:48Z`  
Repository head: `811c3d65ce2b2a698b46a7400112a4d6bab10a16`  
Overall result: `FAIL`  
Schema version: `globalgrid2050.v10-validation-receipt.v1`

## Declared suites

### python

Result: `FAIL`  
Return code: `2`  
Duration: `0.919 s`  
Working directory: `.`  
Command:

```text
/opt/hostedtoolcache/Python/3.11.15/x64/bin/python -m pytest -q
```

Output:

```text

==================================== ERRORS ====================================
_________________ ERROR collecting tests/test_batch_011_013.py _________________
tests/test_batch_011_013.py:6: in <module>
    from solar_topology.cartridges import SequentialCartridge
src/solar_topology/__init__.py:86: in <module>
    from .study_registry import (
src/solar_topology/study_registry.py:218: in <module>
    StudyDefinition(
<string>:11: in __init__
    ???
src/solar_topology/study_registry.py:50: in __post_init__
    raise ValueError("required_evidence_roles must be unique and sorted")
E   ValueError: required_evidence_roles must be unique and sorted
_____________ ERROR collecting tests/test_circuit_calculations.py ______________
tests/test_circuit_calculations.py:8: in <module>
    from solar_topology.calculation_receipts import (
src/solar_topology/__init__.py:86: in <module>
    from .study_registry import (
src/solar_topology/study_registry.py:218: in <module>
    StudyDefinition(
<string>:11: in __init__
    ???
src/solar_topology/study_registry.py:50: in __post_init__
    raise ValueError("required_evidence_roles must be unique and sorted")
E   ValueError: required_evidence_roles must be unique and sorted
________________ ERROR collecting tests/test_contradictions.py _________________
tests/test_contradictions.py:3: in <module>
    from solar_topology.contradictions import (
src/solar_topology/__init__.py:86: in <module>
    from .study_registry import (
src/solar_topology/study_registry.py:218: in <module>
    StudyDefinition(
<string>:11: in __init__
    ???
src/solar_topology/study_registry.py:50: in __post_init__
    raise ValueError("required_evidence_roles must be unique and sorted")
E   ValueError: required_evidence_roles must be unique and sorted
_____________ ERROR collecting tests/test_diagnostic_public_api.py _____________
tests/test_diagnostic_public_api.py:1: in <module>
    import solar_topology as api
src/solar_topology/__init__.py:86: in <module>
    from .study_registry import (
src/solar_topology/study_registry.py:218: in <module>
    StudyDefinition(
<string>:11: in __init__
    ???
src/solar_topology/study_registry.py:50: in __post_init__
    raise ValueError("required_evidence_roles must be unique and sorted")
E   ValueError: required_evidence_roles must be unique and sorted
____________ ERROR collecting tests/test_diagnostics_and_studies.py ____________
tests/test_diagnostics_and_studies.py:26: in <module>
    from solar_topology.study_registry import (
src/solar_topology/__init__.py:86: in <module>
    from .study_registry import (
src/solar_topology/study_registry.py:218: in <module>
    StudyDefinition(
<string>:11: in __init__
    ???
src/solar_topology/study_registry.py:50: in __post_init__
    raise ValueError("required_evidence_roles must be unique and sorted")
E   ValueError: required_evidence_roles must be unique and sorted
_______________ ERROR collecting tests/test_evidence_boundary.py _______________
tests/test_evidence_boundary.py:4: in <module>
    from solar_topology.evidence import canonical_evidence_descriptor
src/solar_topology/__init__.py:86: in <module>
    from .study_registry import (
src/solar_topology/study_registry.py:218: in <module>
    StudyDefinition(
<string>:11: in __init__
    ???
src/solar_topology/study_registry.py:50: in __post_init__
    raise ValueError("required_evidence_roles must be unique and sorted")
E   ValueError: required_evidence_roles must be unique and sorted
___________________ ERROR collecting tests/test_formulas.py ____________________
tests/test_formulas.py:6: in <module>
    import solar_topology.formulas as formulas
src/solar_topology/__init__.py:86: in <module>
    from .study_registry import (
src/solar_topology/study_registry.py:218: in <module>
    StudyDefinition(
<string>:11: in __init__
    ???
src/solar_topology/study_registry.py:50: in __post_init__
    raise ValueError("required_evidence_roles must be unique and sorted")
E   ValueError: required_evidence_roles must be unique and sorted
__________________ ERROR collecting tests/test_identifiers.py __________________
tests/test_identifiers.py:3: in <module>
    from solar_topology.identifiers import (
src/solar_topology/__init__.py:86: in <module>
    from .study_registry import (
src/solar_topology/study_registry.py:218: in <module>
    StudyDefinition(
<string>:11: in __init__
    ???
src/solar_topology/study_registry.py:50: in __post_init__
    raise ValueError("required_evidence_roles must be unique and sorted")
E   ValueError: required_evidence_roles must be unique and sorted
_________________ ERROR collecting tests/test_parquet_store.py _________________
tests/test_parquet_store.py:7: in <module>
    from solar_topology.fleet_store import (
src/solar_topology/__init__.py:86: in <module>
    from .study_registry import (
src/solar_topology/study_registry.py:218: in <module>
    StudyDefinition(
<string>:11: in __init__
    ???
src/solar_topology/study_registry.py:50: in __post_init__
    raise ValueError("required_evidence_roles must be unique and sorted")
E   ValueError: required_evidence_roles must be unique and sorted
__________________ ERROR collecting tests/test_persistence.py __________________
tests/test_persistence.py:5: in <module>
    from solar_topology.persistence import (
src/solar_topology/__init__.py:86: in <module>
    from .study_registry import (
src/solar_topology/study_registry.py:218: in <module>
    StudyDefinition(
<string>:11: in __init__
    ???
src/solar_topology/study_registry.py:50: in __post_init__
    raise ValueError("required_evidence_roles must be unique and sorted")
E   ValueError: required_evidence_roles must be unique and sorted
________________ ERROR collecting tests/test_public_topology.py ________________
tests/test_public_topology.py:4: in <module>
    from solar_topology.evidence import VerificationState, canonical_evidence_descriptor
src/solar_topology/__init__.py:86: in <module>
    from .study_registry import (
src/solar_topology/study_registry.py:218: in <module>
    StudyDefinition(
<string>:11: in __init__
    ???
src/solar_topology/study_registry.py:50: in __post_init__
    raise ValueError("required_evidence_roles must be unique and sorted")
E   ValueError: required_evidence_roles must be unique and sorted
___________________ ERROR collecting tests/test_topology.py ____________________
tests/test_topology.py:5: in <module>
    from solar_topology.topology import (
src/solar_topology/__init__.py:86: in <module>
    from .study_registry import (
src/solar_topology/study_registry.py:218: in <module>
    StudyDefinition(
<string>:11: in __init__
    ???
src/solar_topology/study_registry.py:50: in __post_init__
    raise ValueError("required_evidence_roles must be unique and sorted")
E   ValueError: required_evidence_roles must be unique and sorted
__________________ ERROR collecting tests/test_uncertainty.py __________________
tests/test_uncertainty.py:13: in <module>
    from solar_topology.evidence import (
src/solar_topology/__init__.py:86: in <module>
    from .study_registry import (
src/solar_topology/study_registry.py:218: in <module>
    StudyDefinition(
<string>:11: in __init__
    ???
src/solar_topology/study_registry.py:50: in __post_init__
    raise ValueError("required_evidence_roles must be unique and sorted")
E   ValueError: required_evidence_roles must be unique and sorted
________________ ERROR collecting tests/test_v10_public_api.py _________________
tests/test_v10_public_api.py:1: in <module>
    import solar_topology as engine
src/solar_topology/__init__.py:86: in <module>
    from .study_registry import (
src/solar_topology/study_registry.py:218: in <module>
    StudyDefinition(
<string>:11: in __init__
    ???
src/solar_topology/study_registry.py:50: in __post_init__
    raise ValueError("required_evidence_roles must be unique and sorted")
E   ValueError: required_evidence_roles must be unique and sorted
=========================== short test summary info ============================
ERROR tests/test_batch_011_013.py - ValueError: required_evidence_roles must be unique and sorted
ERROR tests/test_circuit_calculations.py - ValueError: required_evidence_roles must be unique and sorted
ERROR tests/test_contradictions.py - ValueError: required_evidence_roles must be unique and sorted
ERROR tests/test_diagnostic_public_api.py - ValueError: required_evidence_roles must be unique and sorted
ERROR tests/test_diagnostics_and_studies.py - ValueError: required_evidence_roles must be unique and sorted
ERROR tests/test_evidence_boundary.py - ValueError: required_evidence_roles must be unique and sorted
ERROR tests/test_formulas.py - ValueError: required_evidence_roles must be unique and sorted
ERROR tests/test_identifiers.py - ValueError: required_evidence_roles must be unique and sorted
ERROR tests/test_parquet_store.py - ValueError: required_evidence_roles must be unique and sorted
ERROR tests/test_persistence.py - ValueError: required_evidence_roles must be unique and sorted
ERROR tests/test_public_topology.py - ValueError: required_evidence_roles must be unique and sorted
ERROR tests/test_topology.py - ValueError: required_evidence_roles must be unique and sorted
ERROR tests/test_uncertainty.py - ValueError: required_evidence_roles must be unique and sorted
ERROR tests/test_v10_public_api.py - ValueError: required_evidence_roles must be unique and sorted
!!!!!!!!!!!!!!!!!!! Interrupted: 14 errors during collection !!!!!!!!!!!!!!!!!!!
14 errors in 0.50s
```

### v8

Result: `PASS`  
Return code: `0`  
Duration: `0.076 s`  
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
  duration_ms: 36.801526
  ...
1..1
# tests 1
# suites 0
# pass 1
# fail 0
# cancelled 0
# skipped 0
# todo 0
# duration_ms 41.602251
```

### v9

Result: `PASS`  
Return code: `0`  
Duration: `0.037 s`  
Working directory: `.`  
Command:

```text
node v9-sandbox/debug/run-tests.mjs
```

Output:

```text
{
  "schema": "globalgrid2050.solar-dc-debug-test-report.v1",
  "generatedAt": "2026-07-30T13:25:48.091Z",
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
Duration: `0.229 s`  
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
  duration_ms: 2.715295
  ...
# Subtest: quantity rejects unsupported units and propagates weakest provenance
ok 2 - quantity rejects unsupported units and propagates weakest provenance
  ---
  duration_ms: 2.165291
  ...
# Subtest: kernel computes geometry-derived resistance, voltage drop and power loss
ok 3 - kernel computes geometry-derived resistance, voltage drop and power loss
  ---
  duration_ms: 1.616499
  ...
# Subtest: kernel preserves uncertainty intervals through resistance and voltage drop
ok 4 - kernel preserves uncertainty intervals through resistance and voltage drop
  ---
  duration_ms: 0.531439
  ...
# Subtest: cold Voc candidate calculation is traceable and interval bounded
ok 5 - cold Voc candidate calculation is traceable and interval bounded
  ---
  duration_ms: 1.006803
  ...
# Subtest: kernel output is deterministic for identical JSON input
ok 6 - kernel output is deterministic for identical JSON input
  ---
  duration_ms: 1.774236
  ...
# Subtest: sequential order is deterministic
ok 7 - sequential order is deterministic
  ---
  duration_ms: 1.819411
  ...
# Subtest: mirrored sequential order is deterministic
ok 8 - mirrored sequential order is deterministic
  ---
  duration_ms: 0.170711
  ...
# Subtest: canonical leapfrog order is a complete permutation
ok 9 - canonical leapfrog order is a complete permutation
  ---
  duration_ms: 0.305845
  ...
# Subtest: custom order rejects duplicates and omissions
ok 10 - custom order rejects duplicates and omissions
  ---
  duration_ms: 0.354216
  ...
# Subtest: sequential path for 30 modules equals 29 pitches
ok 11 - sequential path for 30 modules equals 29 pitches
  ---
  duration_ms: 1.534585
  ...
# Subtest: canonical leapfrog path for 30 modules equals 57 pitches
ok 12 - canonical leapfrog path for 30 modules equals 57 pitches
  ---
  duration_ms: 0.208462
  ...
# Subtest: geometry output is deterministic
ok 13 - geometry output is deterministic
  ---
  duration_ms: 0.40432
  ...
1..13
# tests 13
# suites 0
# pass 13
# fail 0
# cancelled 0
# skipped 0
# todo 0
# duration_ms 84.559686
```

## Gate

One or more declared suites failed; authority promotion is blocked.

This receipt records execution only. It does not by itself promote an implementation to engineering authority.
