# V10 Validation Receipt

Generated UTC: `2026-07-31T20:07:10Z`  
Repository head: `cc3f55c30df4e9c1f6c86ec2a760beeb2ebd3c79`  
Overall result: `FAIL`  
Schema version: `globalgrid2050.v10-validation-receipt.v1`

## Declared suites

### python

Result: `PASS`  
Return code: `0`  
Duration: `17.592 s`  
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
243 passed in 17.09s
```

### v8

Result: `FAIL`  
Return code: `1`  
Duration: `0.08 s`  
Working directory: `.`  
Command:

```text
node --test tests/v8-model.test.js
```

Output:

```text
TAP version 13
# node:assert:90
#   throw new AssertionError(obj);
#   ^
# AssertionError [ERR_ASSERTION]: [
#   {
#     "name": "Build 025 field-installed reduction is 798.288 m",
#     "pass": true,
#     "actual": 798.288,
#     "expected": 798.288
#   },
#   {
#     "name": "Build 025 factory-fitted increase is 845.088 m",
#     "pass": true,
#     "actual": 845.088,
#     "expected": 845.088
#   },
#   {
#     "name": "Build 025 total circuit conductor increases by 46.800 m",
#     "pass": true,
#     "actual": 46.80000000000018,
#     "expected": 46.8
#   },
#   {
#     "name": "Build 025 absolute winding area falls by about 79.8 percent",
#     "pass": false,
#     "actual": 79.80154896272015,
#     "expected": 79.801546
#   },
#   {
#     "name": "Reference declares unresolved terminal geometry",
#     "pass": true,
#     "actual": "generic_unresolved",
#     "expected": "generic_unresolved"
#   },
#   {
#     "name": "Reference declares plan-coordinate geometry",
#     "pass": true,
#     "actual": "plan_2d",
#     "expected": "plan_2d"
#   }
# ]
# false !== true
#     at Object.<anonymous> (/home/runner/work/solar-electrical-topology-analysis-engine-text-based/solar-electrical-topology-analysis-engine-text-based/tests/v8-model.test.js:158:8)
#     at Module._compile (node:internal/modules/cjs/loader:1521:14)
#     at Module._extensions..js (node:internal/modules/cjs/loader:1623:10)
#     at Module.load (node:internal/modules/cjs/loader:1266:32)
#     at Module._load (node:internal/modules/cjs/loader:1091:12)
#     at Function.executeUserEntryPoint [as runMain] (node:internal/modules/run_main:164:12)
#     at node:internal/main/run_main_module:28:49 {
#   generatedMessage: false,
#   code: 'ERR_ASSERTION',
#   actual: false,
#   expected: true,
#   operator: 'strictEqual'
# }
# Node.js v20.20.2
# Subtest: /home/runner/work/solar-electrical-topology-analysis-engine-text-based/solar-electrical-topology-analysis-engine-text-based/tests/v8-model.test.js
not ok 1 - /home/runner/work/solar-electrical-topology-analysis-engine-text-based/solar-electrical-topology-analysis-engine-text-based/tests/v8-model.test.js
  ---
  duration_ms: 43.028282
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
# duration_ms 47.494614
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
  "generatedAt": "2026-07-31T20:07:10.639Z",
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
Duration: `0.223 s`  
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
  duration_ms: 1.659475
  ...
# Subtest: quantity rejects unsupported units and propagates weakest provenance
ok 2 - quantity rejects unsupported units and propagates weakest provenance
  ---
  duration_ms: 1.997846
  ...
# Subtest: kernel computes geometry-derived resistance, voltage drop and power loss
ok 3 - kernel computes geometry-derived resistance, voltage drop and power loss
  ---
  duration_ms: 1.508848
  ...
# Subtest: kernel preserves uncertainty intervals through resistance and voltage drop
ok 4 - kernel preserves uncertainty intervals through resistance and voltage drop
  ---
  duration_ms: 0.465804
  ...
# Subtest: cold Voc candidate calculation is traceable and interval bounded
ok 5 - cold Voc candidate calculation is traceable and interval bounded
  ---
  duration_ms: 0.995062
  ...
# Subtest: kernel output is deterministic for identical JSON input
ok 6 - kernel output is deterministic for identical JSON input
  ---
  duration_ms: 1.592665
  ...
# Subtest: sequential order is deterministic
ok 7 - sequential order is deterministic
  ---
  duration_ms: 2.260693
  ...
# Subtest: mirrored sequential order is deterministic
ok 8 - mirrored sequential order is deterministic
  ---
  duration_ms: 0.244309
  ...
# Subtest: canonical leapfrog order is a complete permutation
ok 9 - canonical leapfrog order is a complete permutation
  ---
  duration_ms: 0.374836
  ...
# Subtest: custom order rejects duplicates and omissions
ok 10 - custom order rejects duplicates and omissions
  ---
  duration_ms: 0.472604
  ...
# Subtest: sequential path for 30 modules equals 29 pitches
ok 11 - sequential path for 30 modules equals 29 pitches
  ---
  duration_ms: 1.731904
  ...
# Subtest: canonical leapfrog path for 30 modules equals 57 pitches
ok 12 - canonical leapfrog path for 30 modules equals 57 pitches
  ---
  duration_ms: 0.285051
  ...
# Subtest: geometry output is deterministic
ok 13 - geometry output is deterministic
  ---
  duration_ms: 0.585624
  ...
1..13
# tests 13
# suites 0
# pass 13
# fail 0
# cancelled 0
# skipped 0
# todo 0
# duration_ms 85.074171
```

## Gate

One or more declared suites failed; authority promotion is blocked.

This receipt records execution only. It does not by itself promote an implementation to engineering authority.
