# V8 Recovery Progress

Date: 2026-07-27
Branch: `main`
Status: V8 browser recovery substantially implemented; cartridge and Parquet fleet stage not yet claimed complete.

## Completed

### V8 source recovery

- Reformatted V8 HTML, JavaScript, CSS and browser tests into readable source.
- Added a 120-character source-width law enforced by CI.
- Preserved V6 and V7 as separate comparison workbenches.
- Added runtime error reporting and browser golden-test status.

### Leapfrog feasibility

- Module pitch is derived from module width plus inter-module gap.
- Default leapfrog required reach is two module pitches.
- A measured routed connector-to-connector span may override the geometric screen.
- Available reach is positive factory lead plus negative factory lead.
- V8 reports margin and minimum extension required.
- V8 refuses to present theoretical cable reduction as an available saving when the lead screen fails.

Default geometry:

- module pitch: 1.323 m;
- required reach: 2.646 m;
- standard 0.350 m + 0.280 m leads: infeasible;
- 1.2 m + 1.2 m leads: short by 0.246 m;
- 1.4 m + 1.4 m leads: passes the length screen.

### Fleet aggregation

- The 24-string inverter is retained as an archetype.
- Actual site string count is a separate input.
- Default actual site string count is 18,918.
- Site cable difference is row span multiplied by actual total string count.
- Theoretical default site difference is approximately 750.477 km.
- The old 24 strings multiplied by inverter count shortcut is no longer used for site truth.

### Calculation discipline

- Sequential per string: `2(D + O) + R`.
- Leapfrog per string: `2(D + O)`.
- Theoretical difference per feasible string: one derived row span `R`.
- Factory module leads remain in circuit under both topologies and are not treated as saved copper.
- Resistance and voltage-drop reduction are reported per string.
- Power-loss reduction may be summed across parallel strings.

### Assurance files

- `BUILD_RECOVERY_INSTRUCTIONS_CHATGPT.md`
- `DATA_CONTRACT_SEGMENTS.md`
- `tests/v8-model.test.js`
- `tests/check_v8_source_width.py`
- `.github/workflows/v8-tests.yml`
- browser tests at `v8-leapfrog/tests.html`
- dated restore points under `restore_points/`

### Parallel physics work preserved

Concurrent commits on `main` improved the Python formula core and formula tests:

- declared finished-cable resistance replaces recreated bulk-copper resistance;
- actual conductor diameter is required rather than inferred from nominal CSA;
- propagation velocity and characteristic impedance use external inductance only;
- low-frequency internal inductance remains available for stored energy and lumped `L di/dt` studies.

Those changes do not conflict with the V8 browser recovery.

## Not yet complete

The following work is specified but not yet claimed as implemented:

- Python topology-cartridge base interface;
- sequential cartridge emitting contract-compliant segment rows;
- leapfrog cartridge emitting contract-compliant segment rows;
- cross-cartridge factory-lead invariant test;
- zstd Parquet segment output;
- DuckDB per-string, MPPT, inverter and site aggregation;
- deterministic double-build hash comparison;
- independent auditor reading committed Parquet;
- fleet build for all 18,918 strings;
- browser consumption of generated aggregate and selected-string slices.

## Next execution order

1. Create the Python cartridge base interface.
2. Implement sequential and leapfrog segment generators.
3. Prove route continuity and the factory-lead invariant.
4. Reproduce V8 headline values from segment sums.
5. Write zstd Parquet partitioned by topology and inverter.
6. Aggregate with DuckDB.
7. Build identical outputs twice and compare hashes.
8. Add an independent auditor.
9. Publish small browser summaries rather than fleet JSON.
10. Only then attach advanced R, L, C, propagation and transient physics to the shared segment chassis.

## Public test links

- V8: `https://ventusltd.github.io/solar-electrical-topology-analysis-engine-text-based/v8-leapfrog/`
- V8 browser tests: `https://ventusltd.github.io/solar-electrical-topology-analysis-engine-text-based/v8-leapfrog/tests.html`
- V6: `https://ventusltd.github.io/solar-electrical-topology-analysis-engine-text-based/`
- V7: `https://ventusltd.github.io/solar-electrical-topology-analysis-engine-text-based/v7-development/feed-i/`

## Verification caveat

The repository workflow has been configured to run source-width, JavaScript syntax and Node regression checks. At the time of this progress note, the connected GitHub status interface did not expose a completed push-workflow run, so the workflow must not yet be described as passed solely from this record. The browser test page provides the immediate visible fixture check while the Action completes or becomes visible.
