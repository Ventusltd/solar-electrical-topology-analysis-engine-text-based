# V10 Validation Receipt

Generated UTC: `2026-07-30T01:50:50Z`  
Repository head: `3abf9a2a76ea25bd2c71b2b583ae46b23f576258`  
Overall result: `FAIL`  
Schema version: `globalgrid2050.v10-validation-receipt.v1`

## Declared suites

### python

Result: `FAIL`  
Return code: `1`  
Duration: `3.768 s`  
Working directory: `.`  
Command:

```text
/opt/hostedtoolcache/Python/3.11.15/x64/bin/python -m pytest -q
```

Output:

```text
..........................................F..........                    [100%]
=================================== FAILURES ===================================
_________ test_deterministic_partitioned_store_and_actual_string_count _________

tmp_path = PosixPath('/tmp/pytest-of-runner/pytest-0/test_deterministic_partitioned0')

    def test_deterministic_partitioned_store_and_actual_string_count(tmp_path):
        inputs = TopologyInputs(
            inverter_count=2,
            total_site_string_count=47,
            positive_factory_lead_m=1.4,
            negative_factory_lead_m=1.4,
        )
        output = tmp_path / "store"
        result = build_deterministic_store(
            inputs,
            output,
            source_commit="test-commit",
        )
    
        assert result["deterministic"] is True
        assert result["string_count"] == 47
        assert result["generated_segment_rows"] == 47 * 183
    
        partitions = sorted(
            output.glob("segments/topology=*/band=*/data_*.parquet")
        )
        result_partitions = sorted(
            output.glob("results/segments/topology=*/band=*/data_*.parquet")
        )
        assert len(partitions) == 6
        assert len(result_partitions) == 6
    
        connection = duckdb.connect()
        try:
            comparison = read_one(
                connection,
                output / "aggregates" / "comparison.parquet",
            )
            assert comparison[0] == 47
            assert comparison[3] == pytest.approx(47 * 39.67)
            assert comparison[4] == pytest.approx(47 * 39.67)
            assert comparison[5] is True
    
            site = connection.execute(
                """
                SELECT topology, string_count
                FROM read_parquet(?)
                ORDER BY topology
                """,
                [str(output / "aggregates" / "site.parquet")],
            ).fetchall()
            assert site == [("leapfrog", 47), ("sequential", 47)]
    
            factory = connection.execute(
                """
                SELECT
                    topology,
                    min(factory_lead_m),
                    max(factory_lead_m),
                    min(connector_count),
                    max(connector_count)
                FROM read_parquet(?)
                GROUP BY topology
                ORDER BY topology
                """,
                [str(output / "aggregates" / "strings.parquet")],
            ).fetchall()
>           assert factory == [
                ("leapfrog", 84.0, 84.0, 62, 62),
                ("sequential", 84.0, 84.0, 62, 62),
            ]
E           AssertionError: assert [('leapfrog',..., 62.0, 62.0)] == [('leapfrog',...84.0, 62, 62)]
E             
E             At index 0 diff: ('leapfrog', 84.00000000000004, 84.00000000000004, 62.0, 62.0) != ('leapfrog', 84.0, 84.0, 62, 62)
E             
E             Full diff:
E               [
E                   (
E                       'leapfrog',
E             -         84.0,
E             -         84.0,
E             +         84.00000000000004,
E             +         84.00000000000004,
E             -         62,
E             +         62.0,
E             ?           ++
E             -         62,
E             +         62.0,
E             ?           ++
E                   ),
E                   (
E                       'sequential',
E             -         84.0,
E             -         84.0,
E             +         84.00000000000004,
E             +         84.00000000000004,
E             -         62,
E             +         62.0,
E             ?           ++
E             -         62,
E             +         62.0,
E             ?           ++
E                   ),
E               ]

tests/test_parquet_store.py:83: AssertionError
=========================== short test summary info ============================
FAILED tests/test_parquet_store.py::test_deterministic_partitioned_store_and_actual_string_count - AssertionError: assert [('leapfrog',..., 62.0, 62.0)] == [('leapfrog',...84.0, 62, 62)]
  
  At index 0 diff: ('leapfrog', 84.00000000000004, 84.00000000000004, 62.0, 62.0) != ('leapfrog', 84.0, 84.0, 62, 62)
  
  Full diff:
    [
        (
            'leapfrog',
  -         84.0,
  -         84.0,
  +         84.00000000000004,
  +         84.00000000000004,
  -         62,
  +         62.0,
  ?           ++
  -         62,
  +         62.0,
  ?           ++
        ),
        (
            'sequential',
  -         84.0,
  -         84.0,
  +         84.00000000000004,
  +         84.00000000000004,
  -         62,
  +         62.0,
  ?           ++
  -         62,
  +         62.0,
  ?           ++
        ),
    ]
1 failed, 52 passed in 3.32s
```

### v8

Result: `PASS`  
Return code: `0`  
Duration: `0.073 s`  
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
  duration_ms: 36.04762
  ...
1..1
# tests 1
# suites 0
# pass 1
# fail 0
# cancelled 0
# skipped 0
# todo 0
# duration_ms 40.550019
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
  "generatedAt": "2026-07-30T01:50:49.852Z",
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
Duration: `0.209 s`  
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
  duration_ms: 1.376374
  ...
# Subtest: kernel computes geometry-derived resistance, voltage drop and power loss
ok 2 - kernel computes geometry-derived resistance, voltage drop and power loss
  ---
  duration_ms: 1.023257
  ...
# Subtest: kernel preserves uncertainty intervals through resistance and voltage drop
ok 3 - kernel preserves uncertainty intervals through resistance and voltage drop
  ---
  duration_ms: 0.362541
  ...
# Subtest: cold Voc candidate calculation is traceable and interval bounded
ok 4 - cold Voc candidate calculation is traceable and interval bounded
  ---
  duration_ms: 0.704031
  ...
# Subtest: kernel output is deterministic for identical JSON input
ok 5 - kernel output is deterministic for identical JSON input
  ---
  duration_ms: 1.093463
  ...
# Subtest: sequential order is deterministic
ok 6 - sequential order is deterministic
  ---
  duration_ms: 1.625126
  ...
# Subtest: mirrored sequential order is deterministic
ok 7 - mirrored sequential order is deterministic
  ---
  duration_ms: 0.163825
  ...
# Subtest: canonical leapfrog order is a complete permutation
ok 8 - canonical leapfrog order is a complete permutation
  ---
  duration_ms: 0.267579
  ...
# Subtest: custom order rejects duplicates and omissions
ok 9 - custom order rejects duplicates and omissions
  ---
  duration_ms: 0.346487
  ...
# Subtest: sequential path for 30 modules equals 29 pitches
ok 10 - sequential path for 30 modules equals 29 pitches
  ---
  duration_ms: 1.423495
  ...
# Subtest: canonical leapfrog path for 30 modules equals 57 pitches
ok 11 - canonical leapfrog path for 30 modules equals 57 pitches
  ---
  duration_ms: 0.196834
  ...
# Subtest: geometry output is deterministic
ok 12 - geometry output is deterministic
  ---
  duration_ms: 0.434419
  ...
1..12
# tests 12
# suites 0
# pass 12
# fail 0
# cancelled 0
# skipped 0
# todo 0
# duration_ms 68.025614
```

## Gate

One or more declared suites failed; authority promotion is blocked.

This receipt records execution only. It does not by itself promote an implementation to engineering authority.
