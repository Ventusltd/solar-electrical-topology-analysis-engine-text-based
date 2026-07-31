# V10 Validation Receipt

Generated UTC: `2026-07-31T20:08:38Z`  
Repository head: `4375b4e2e70d722f5dafbf5df174f5a490d3b605`  
Overall result: `FAIL`  
Schema version: `globalgrid2050.v10-validation-receipt.v1`

## Declared suites

### python

Result: `PASS`  
Return code: `0`  
Duration: `12.039 s`  
Working directory: `.`  
Command:

```text
/opt/hostedtoolcache/Python/3.11.15/x64/bin/python -m pytest -q
```

Output:

```text
........................................................................ [ 29%]
........................................................................ [ 59%]
........................................................................ [ 88%]
...........................                                              [100%]
243 passed in 11.24s
```

### v8

Result: `FAIL`  
Return code: `1`  
Duration: `0.063 s`  
Working directory: `.`  
Command:

```text
node --test tests/v8-model.test.js
```

Output:

```text
TAP version 13
# node:internal/assert/utils:281
#     throw err;
#     ^
# AssertionError [ERR_ASSERTION]: The expression evaluated to a falsy value:
#   assert.ok(
#     close(
#       reconciliation.absoluteWindingAreaReductionPercent,
#       79.801546,
#       1e-6
#     )
#   )
#     at Object.<anonymous> (/home/runner/work/solar-electrical-topology-analysis-engine-text-based/solar-electrical-topology-analysis-engine-text-based/tests/v8-model.test.js:168:8)
#     at Module._compile (node:internal/modules/cjs/loader:1521:14)
#     at Module._extensions..js (node:internal/modules/cjs/loader:1623:10)
#     at Module.load (node:internal/modules/cjs/loader:1266:32)
#     at Module._load (node:internal/modules/cjs/loader:1091:12)
#     at Function.executeUserEntryPoint [as runMain] (node:internal/modules/run_main:164:12)
#     at node:internal/main/run_main_module:28:49 {
#   generatedMessage: true,
#   code: 'ERR_ASSERTION',
#   actual: false,
#   expected: true,
#   operator: '=='
# }
# Node.js v20.20.2
# Subtest: /home/runner/work/solar-electrical-topology-analysis-engine-text-based/solar-electrical-topology-analysis-engine-text-based/tests/v8-model.test.js
not ok 1 - /home/runner/work/solar-electrical-topology-analysis-engine-text-based/solar-electrical-topology-analysis-engine-text-based/tests/v8-model.test.js
  ---
  duration_ms: 35.094771
  location: '/home/runner/work/solar-electrical-topology-analysis-engine-text-based/solar-electrical-topology-analysis-engine-text-based/tests/v8-model.test.js:1:1'
  failureType: 'testCodeFailure'
  exitCode: 1
  signal: ~
  error: 'test failed'
  code: 'ERR_TEST_FAILURE'
  ...
1..1
# tests 1
# suites 0
# pass 0
# fail 1
# cancelled 0
# skipped 0
# todo 0
# duration_ms 38.341024
```

### v9

Result: `PASS`  
Return code: `0`  
Duration: `0.027 s`  
Working directory: `.`  
Command:

```text
node v9-sandbox/debug/run-tests.mjs
```

Output:

```text
{
  "schema": "globalgrid2050.solar-dc-debug-test-report.v1",
  "generatedAt": "2026-07-31T20:08:38.607Z",
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
Duration: `0.152 s`  
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
  duration_ms: 1.160616
  ...
# Subtest: quantity rejects unsupported units and propagates weakest provenance
ok 2 - quantity rejects unsupported units and propagates weakest provenance
  ---
  duration_ms: 1.269939
  ...
# Subtest: kernel computes geometry-derived resistance, voltage drop and power loss
ok 3 - kernel computes geometry-derived resistance, voltage drop and power loss
  ---
  duration_ms: 0.95901
  ...
# Subtest: kernel preserves uncertainty intervals through resistance and voltage drop
ok 4 - kernel preserves uncertainty intervals through resistance and voltage drop
  ---
  duration_ms: 0.306068
  ...
# Subtest: cold Voc candidate calculation is traceable and interval bounded
ok 5 - cold Voc candidate calculation is traceable and interval bounded
  ---
  duration_ms: 0.605934
  ...
# Subtest: kernel output is deterministic for identical JSON input
ok 6 - kernel output is deterministic for identical JSON input
  ---
  duration_ms: 1.001336
  ...
# Subtest: sequential order is deterministic
ok 7 - sequential order is deterministic
  ---
  duration_ms: 1.548666
  ...
# Subtest: mirrored sequential order is deterministic
ok 8 - mirrored sequential order is deterministic
  ---
  duration_ms: 0.144303
  ...
# Subtest: canonical leapfrog order is a complete permutation
ok 9 - canonical leapfrog order is a complete permutation
  ---
  duration_ms: 0.253801
  ...
# Subtest: custom order rejects duplicates and omissions
ok 10 - custom order rejects duplicates and omissions
  ---
  duration_ms: 0.306244
  ...
# Subtest: sequential path for 30 modules equals 29 pitches
ok 11 - sequential path for 30 modules equals 29 pitches
  ---
  duration_ms: 1.31693
  ...
# Subtest: canonical leapfrog path for 30 modules equals 57 pitches
ok 12 - canonical leapfrog path for 30 modules equals 57 pitches
  ---
  duration_ms: 0.186328
  ...
# Subtest: geometry output is deterministic
ok 13 - geometry output is deterministic
  ---
  duration_ms: 0.355591
  ...
1..13
# tests 13
# suites 0
# pass 13
# fail 0
# cancelled 0
# skipped 0
# todo 0
# duration_ms 58.093117
```

## Gate

One or more declared suites failed; authority promotion is blocked.

This receipt records execution only. It does not by itself promote an implementation to engineering authority.
