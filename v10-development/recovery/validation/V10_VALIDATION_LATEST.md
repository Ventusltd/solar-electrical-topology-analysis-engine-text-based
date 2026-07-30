# V10 Validation Receipt

Generated UTC: `2026-07-30T02:31:54Z`  
Repository head: `bb53defd4e1226f8c376bed290cc84e9cdbb3e2a`  
Overall result: `PASS`  
Schema version: `globalgrid2050.v10-validation-receipt.v1`

## Declared suites

### python

Result: `PASS`  
Return code: `0`  
Duration: `4.147 s`  
Working directory: `.`  
Command:

```text
/opt/hostedtoolcache/Python/3.11.15/x64/bin/python -m pytest -q
```

Output:

```text
.....................................................                    [100%]
53 passed in 3.33s
```

### v8

Result: `PASS`  
Return code: `0`  
Duration: `0.072 s`  
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
  duration_ms: 35.189282
  ...
1..1
# tests 1
# suites 0
# pass 1
# fail 0
# cancelled 0
# skipped 0
# todo 0
# duration_ms 39.719418
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
  "generatedAt": "2026-07-30T02:31:54.103Z",
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
Duration: `0.218 s`  
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
# Subtest: quantity rejects unsupported units and propagates weakest provenance
ok 1 - quantity rejects unsupported units and propagates weakest provenance
  ---
  duration_ms: 1.963398
  ...
# Subtest: kernel computes geometry-derived resistance, voltage drop and power loss
ok 2 - kernel computes geometry-derived resistance, voltage drop and power loss
  ---
  duration_ms: 1.168147
  ...
# Subtest: kernel preserves uncertainty intervals through resistance and voltage drop
ok 3 - kernel preserves uncertainty intervals through resistance and voltage drop
  ---
  duration_ms: 0.359877
  ...
# Subtest: cold Voc candidate calculation is traceable and interval bounded
ok 4 - cold Voc candidate calculation is traceable and interval bounded
  ---
  duration_ms: 0.706814
  ...
# Subtest: kernel output is deterministic for identical JSON input
ok 5 - kernel output is deterministic for identical JSON input
  ---
  duration_ms: 1.104808
  ...
# Subtest: sequential order is deterministic
ok 6 - sequential order is deterministic
  ---
  duration_ms: 1.625544
  ...
# Subtest: mirrored sequential order is deterministic
ok 7 - mirrored sequential order is deterministic
  ---
  duration_ms: 0.161922
  ...
# Subtest: canonical leapfrog order is a complete permutation
ok 8 - canonical leapfrog order is a complete permutation
  ---
  duration_ms: 0.291545
  ...
# Subtest: custom order rejects duplicates and omissions
ok 9 - custom order rejects duplicates and omissions
  ---
  duration_ms: 0.334369
  ...
# Subtest: sequential path for 30 modules equals 29 pitches
ok 10 - sequential path for 30 modules equals 29 pitches
  ---
  duration_ms: 1.559656
  ...
# Subtest: canonical leapfrog path for 30 modules equals 57 pitches
ok 11 - canonical leapfrog path for 30 modules equals 57 pitches
  ---
  duration_ms: 0.286197
  ...
# Subtest: geometry output is deterministic
ok 12 - geometry output is deterministic
  ---
  duration_ms: 0.580075
  ...
1..12
# tests 12
# suites 0
# pass 12
# fail 0
# cancelled 0
# skipped 0
# todo 0
# duration_ms 74.044691
```

## Gate

All declared Python, V8, V9 and V10 JavaScript suites passed.

This receipt records execution only. It does not by itself promote an implementation to engineering authority.
