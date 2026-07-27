# Binding Build Recovery Instructions for ChatGPT

Repository: `Ventusltd/solar-electrical-topology-analysis-engine-text-based`

Branch: `main`

Status: binding execution brief for recovery and continuation of the V8 topology build.

## 1. Governing objective

Recover the topology engine from the current mixture of oversized JavaScript lines, overlapping V6/V7/V8 responsibilities and browser-only scaling limits.

The immediate product is a correct, readable and testable V8 comparison of conventional sequential string wiring against leapfrog string wiring.

The durable product is a topology-cartridge engine in which each wiring topology produces the same segment schema, while one shared physics chassis calculates resistance, voltage drop, inductance, capacitance, loop area, propagation and aggregation without knowing which cartridge produced the segments.

The fleet target is approximately 18,918 strings. A fleet of that size must be built and audited as partitioned Parquet with DuckDB in GitHub Actions. It must not be placed into one browser JSON object.

## 2. Non-negotiable repository rules

1. Work on `main`. Do not create feature branches.
2. Create a dated restore-point folder before each material change.
3. Do not alter the working V6 or V7 executable pages while repairing V8.
4. V6 remains the complete-circuit comparison reference.
5. V7 remains the electromagnetic and evidence-discipline comparison reference.
6. V8 is the active sequential-versus-leapfrog cable-schedule build.
7. Do not delete earlier restore points.
8. Every material formula change requires a fixture or data-law test before the change is treated as complete.
9. The browser is a presentation and single-string interaction layer. It is not the fleet data store.
10. No electrical result may be calculated independently in both JavaScript and Python after the Parquet pipeline becomes authoritative.

## 3. Code-formatting law

The first repair is formatting, not physics.

1. Run all V8 JavaScript, CSS, HTML, Python and YAML through a formatter.
2. Target normal readable line width, preferably 80 to 100 characters and never deliberately above 120 characters except unavoidable URLs or generated data.
3. Do not place multiple functions on one line.
4. Do not place a complete parser, generator, aggregation function or renderer on one line.
5. Do not commit minified source as the editable source of truth.
6. Generated or minified browser assets, if ever required, must be produced by a build step and kept separate from readable source.
7. Add a CI formatting check so the mega-line failure mode cannot return.
8. Prefer small modules with one concern per file over one expanding `app.js`.

Suggested V8 browser split:

- `v8-leapfrog/index.html`
- `v8-leapfrog/styles.css`
- `v8-leapfrog/ui.js`
- `v8-leapfrog/format.js`
- `v8-leapfrog/diagram.js`
- `v8-leapfrog/client-model.js` only while the browser model remains temporary

The long-term source of truth will be Python and Parquet, not duplicated JavaScript physics.

## 4. Immediate V8 repair order

Perform these tasks in this exact sequence.

### 4.1 Format V8

Format every V8 source file before changing calculations. Confirm the resulting diff is human-readable and localised.

### 4.2 Correct leapfrog feasibility

Leapfrog is not automatically feasible merely because the topology is selected.

Required inputs:

- positive factory lead length per module;
- negative factory lead length per module;
- module width along row;
- inter-module gap;
- optional measured routed leapfrog span;
- provenance for every lead and span input.

Geometry:

`module_pitch = module_width + inter_module_gap`

Default geometric screening reach:

`required_leapfrog_reach = 2 × module_pitch`

This represents the connector-to-connector reach required to skip the intervening portrait module. Where an actual routed connector-to-connector span has been measured, the measured span may replace the geometric screening value and must carry measured provenance.

Available combined lead reach:

`available_lead_reach = positive_factory_lead + negative_factory_lead`

Margin:

`lead_margin = available_lead_reach - required_leapfrog_reach`

States:

- `UNRESOLVED` when required geometry or lead evidence is missing;
- `FEASIBLE_LENGTH_SCREEN` when margin is zero or positive;
- `INFEASIBLE_LENGTH_SCREEN` when margin is negative.

When infeasible:

1. Do not show cable saving as an available design outcome.
2. Show the shortfall in metres.
3. Show the minimum additional extension length that would be required.
4. State that extra extensions add connector interfaces and must not be treated as a free solution.
5. Keep bend radius, support, connector orientation and slack as separate unresolved checks.

The default manufacturer catalogue leads must not be silently treated as the actual delivered leads. Site photographs may justify an assumed scenario but not a measured state.

### 4.3 Correct fleet aggregation

Do not calculate fleet saving as:

`archetype saving per inverter × inverter count`

unless every inverter is proven to carry the full archetype string count.

Add an explicit input:

`total_site_string_count`

Default working value:

`18,918 strings`

Fleet external cable saving, when leapfrog is feasible, is:

`row_span × total_site_string_count`

The 24-string inverter remains an archetype for the drawing and per-inverter schedule. It must not overwrite the actual fleet string count.

Report both:

- archetype strings per inverter;
- total site strings;
- inverter count;
- average site strings per inverter.

A difference between archetype and fleet average is evidence, not an error.

### 4.4 Preserve the copper invariant

Factory module-lead conductor exists in the circuit under both sequential and leapfrog wiring. It may be coiled or deployed, but it is still purchased with the module and remains electrically in circuit.

Therefore:

- factory lead conductor length must be identical across sequential and leapfrog cartridges for the same module data;
- connector count must remain identical unless the topology genuinely requires extra extension interfaces;
- only the external EPC-installed DC string cable may be reduced by the basic leapfrog topology;
- any cartridge that changes module-lead conductor without explicit extension logic must fail its invariant test.

### 4.5 Retain correct V8 cable arithmetic

For one string:

Let:

- `R` be the derived row span;
- `D` be the near-end distance to the inverter;
- `O` be the band offset.

Sequential external cable:

`2 × (D + O) + R`

Leapfrog external cable:

`2 × (D + O)`

Basic saving per feasible string:

`R`

The inverter distance changes the unavoidable base pair in both modes. It does not change the row-return saving.

V8 must clearly separate:

- unavoidable positive-and-negative base pair;
- additional sequential row return;
- leapfrog row return, which is zero when feasible;
- factory module leads;
- extension leads, if required;
- total external EPC-installed cable.

### 4.6 Finish V8 regression tests

Required browser and Node fixtures:

1. Default row span equals 39.67 m for 30 modules, 1.303 m width and 0.020 m gaps.
2. Default archetype contains 24 strings.
3. Sequential versus leapfrog basic saving equals one row span per feasible string.
4. Saving does not change when inverter distance changes from 10 m to 20 m or 30 m.
5. Fleet saving uses total site string count, not inverter count.
6. Default catalogue leads fail the two-pitch feasibility screen.
7. A pair of 1.2 m leads fails a 2.646 m required reach by approximately 0.246 m.
8. A pair of 1.4 m leads passes the same screen.
9. Sequential and leapfrog cartridges contain equal factory module-lead length.
10. No derived route length can be supplied directly by a user.
11. East and west polarity labels may mirror, but total cable quantity must remain invariant.
12. JSON export states whether savings are available, unavailable or unresolved.

## 5. Write the segment data contract before cartridge code

Create `DATA_CONTRACT_SEGMENTS.md` before implementing the cartridge architecture.

### Grain

One row per physical conductor segment, per string, per topology, per model run.

### Primary key

At minimum:

`run_id + topology_id + string_id + segment_index`

For fleet partitions, include `inverter_id` in both the row and physical path.

### Required segment fields

Identity:

- `run_id`
- `topology_id`
- `topology_version`
- `inverter_id`
- `mppt_id`
- `string_id`
- `segment_index`
- `segment_id`

Topology and electrical role:

- `segment_type`
- `polarity`
- `from_node_id`
- `to_node_id`
- `series_order`

Geometry:

- `start_x_m`
- `start_y_m`
- `start_z_m`
- `end_x_m`
- `end_y_m`
- `end_z_m`
- `displacement_m`
- `conductor_length_m`
- `plan_length_m`
- `slope_length_m`
- `loop_area_contribution_m2`

Formation:

- `formation_type`
- `paired_with_segment_id`
- `conductor_separation_m`
- `height_above_reference_m`
- `installation_class`
- `support_type`

Conductor:

- `conductor_product_id`
- `nominal_csa_mm2`
- `conductor_diameter_mm`
- `cable_od_mm`
- `material`
- `r20_ohm_per_m`

Evidence:

- `segment_provenance`
- `length_provenance`
- `separation_provenance`
- `formation_provenance`
- `source_reference`
- `user_override`
- `confidence_state`

Assurance:

- `method_version`
- `input_hash`
- `cartridge_hash`
- `warnings`

### Segment types

Initial controlled vocabulary:

- `module_factory_positive_lead`
- `module_factory_negative_lead`
- `module_interconnect`
- `string_turnaround`
- `external_positive_home_run`
- `external_negative_home_run`
- `external_sequential_row_return`
- `extension_lead`
- `coiled_surplus`
- `structure_drop`
- `surface_route`
- `trench_route`
- `inverter_approach`
- `termination_allowance`

A zero-displacement coil may have real conductor length and must not be discarded.

## 6. Cartridge interface

A topology cartridge has one responsibility: generate segment rows.

Every cartridge must expose:

1. `name`
2. `version`
3. `feasibility(inputs)`
4. `build_segments(inputs)`
5. `manifest(inputs, segments)`

The shared chassis passes geometry, module data, inverter position and route rules to the cartridge. The cartridge returns an ordered segment table and no calculated resistance, inductance or capacitance totals.

Initial cartridges:

- `sequential`
- `leapfrog`

Future cartridges:

- `mirrored`
- `balanced_return`
- `custom_manual`

No downstream calculation may ask:

`if topology == leapfrog`

If a physics function needs to know the topology name, the cartridge boundary is wrong. Physics consumes segments only.

### Cross-cartridge invariants

For identical module and project inputs:

- module count is equal;
- string voltage basis is equal;
- factory module-lead conductor length is equal;
- normal module connector count is equal;
- conductor material and product data are equal;
- only topology-dependent external and extension segments may differ;
- sum of ordered segment lengths equals the exported string conductor length;
- segment indices are contiguous and unique;
- start and end nodes form a continuous electrical path.

## 7. Parquet and DuckDB architecture

The working patterns in `data-gb-electricity` and `data-federation-map-for-globalgrid2050-all-repos` shall be reused rather than re-invented.

### 7.1 Why the change is required

Approximately 18,918 strings at around 100 segments per string produce roughly 1.9 million segment rows. This is modest for Parquet and DuckDB but inappropriate for one browser JSON document.

### 7.2 Authoritative build language

The fleet topology and physics core shall be Python plus DuckDB SQL.

JavaScript remains for:

- single-string interactive preview;
- drawing controls;
- selection and explanation;
- loading small generated summaries.

JavaScript shall not remain a second independent fleet physics implementation.

### 7.3 Physical output layout

Recommended current store:

`data/topology/current/segments/provenance=derived/topology=sequential/inverter_id=0001/data_0.parquet`

`data/topology/current/segments/provenance=derived/topology=leapfrog/inverter_id=0001/data_0.parquet`

Recommended snapshots:

`data/topology/snapshots/year=YYYY/month=MM/week=WW/...`

Recommended manifests:

`data/topology/current/manifests/topology=leapfrog/inverter_id=0001/manifest.json`

Recommended aggregate stores:

- `data/topology/current/aggregates/strings.parquet`
- `data/topology/current/aggregates/mppts.parquet`
- `data/topology/current/aggregates/inverters.parquet`
- `data/topology/current/aggregates/site.parquet`

Use Parquet with zstd compression.

### 7.4 Partition discipline

Partition by fields that are used to isolate meaningful slices:

- topology;
- inverter;
- row-level segment provenance where appropriate.

Do not create a partition for every string unless measurements prove it is beneficial. An inverter partition provides a practical browser and audit slice.

### 7.5 Manifest

Each cartridge manifest must include:

- cartridge name and version;
- method version;
- source commit;
- input hash;
- output segment row count;
- distinct string count;
- first and last segment key;
- schema version;
- file SHA-256;
- feasibility result;
- warning count;
- data-law result.

A deterministic manifest must not contain an uncontrolled wall-clock timestamp. Put operational timestamps in a separate audit report if required.

## 8. DuckDB calculation and aggregation

The topology cartridges write segment rows. Physics operates on those rows.

### 8.1 Segment-level results

Create a derived segment-result table containing, where applicable:

- operating resistance;
- voltage-drop contribution;
- I2R loss contribution;
- external differential inductance;
- low-frequency internal inductance;
- differential capacitance;
- common-mode capacitance estimate;
- propagation delay contribution;
- loop-area contribution;
- evidence and validity flags.

### 8.2 Aggregation levels

Use DuckDB group-bys to build:

1. per segment;
2. per string;
3. per MPPT;
4. per inverter;
5. per site.

Do not hand-write separate fleet loops for every aggregation layer.

### 8.3 Mode separation

Differential and common-mode outputs remain separate first-class columns or tables.

Do not sum module pole-to-pole capacitance with module-to-frame capacitance.

Do not use low-frequency internal inductance in propagation velocity or surge impedance.

## 9. Data law and verification

The build is not trusted because a workflow is green. It is trusted when the declared data law passes.

Required checks:

- row count equals distinct primary-key count;
- no null or empty key fields;
- segment indices are contiguous within every string;
- no route discontinuities;
- no negative conductor lengths;
- zero-displacement segments are allowed only where conductor length is positive and segment type permits them;
- no user-supplied value appears in a derived route-length column;
- cartridge manifest row count equals Parquet row count;
- string aggregate equals sum of its segment rows;
- MPPT aggregate equals sum of its strings;
- inverter aggregate equals sum of its MPPTs;
- site aggregate equals sum of actual site strings;
- factory lead total is equal across sequential and leapfrog cartridges;
- leapfrog saving is unavailable when its feasibility gate fails;
- provenance values belong to a controlled vocabulary;
- no derived rows appear in a declared-only base partition;
- no dangling node endpoints.

Write the audit result to a machine-readable JSON report and a short Markdown receipt.

## 10. Determinism harness

Build the same topology twice from identical inputs into two separate temporary directories.

Requirements:

1. Sort rows by the full primary key before writing.
2. Use fixed schemas and writer settings.
3. Avoid uncontrolled timestamps in deterministic artefacts.
4. Hash every Parquet file and manifest.
5. Fail the workflow if corresponding hashes differ.
6. Record the determinism result in the audit report.

Golden values protect known answers. The determinism harness additionally protects repeatability and ordering.

Both are required.

## 11. Independent audit rule

The builder must not grade its own work as the only proof.

Create a separate auditor script that:

1. opens committed Parquet from a fresh checkout;
2. re-runs all data-law queries independently;
3. recomputes headline V8 values directly from segment rows;
4. compares them with committed aggregate Parquet and JSON summaries;
5. exits non-zero on any mismatch.

The audit must read the exact commit that is being assessed.

## 12. GitHub Actions build pattern

Follow the established data-repository pattern:

1. check out the repository;
2. install Python, DuckDB, PyArrow and test dependencies;
3. run formatting and unit tests;
4. build into a temporary directory;
5. run the second deterministic build;
6. compare hashes;
7. run the independent auditor;
8. write current Parquet, snapshots, manifests and audit reports;
9. commit only declared output paths when applying;
10. publish a small browser summary artefact.

Provide both audit and apply modes.

The default pull-request or push workflow should audit without blindly rewriting fleet data. A manually triggered apply workflow may commit verified generated outputs.

## 13. Browser boundary

GitHub Pages cannot execute the server-side DuckDB fleet build.

Therefore:

- Actions builds fleet Parquet;
- the browser reads a small site summary;
- the browser may request one inverter or one string slice;
- the browser remains fully interactive for one archetype string;
- the browser must never load all site segments as JSON;
- exports must state schema version and source build hash.

The browser may draw GeoJSON or SVG generated from a small selected segment set. The drawing is a readout, not the fleet data store.

## 14. Immediate file plan

Create these files in order:

1. `DATA_CONTRACT_SEGMENTS.md`
2. `topology_core/schema.py`
3. `topology_core/types.py`
4. `topology_core/cartridges/base.py`
5. `topology_core/cartridges/sequential.py`
6. `topology_core/cartridges/leapfrog.py`
7. `topology_core/build_segments.py`
8. `topology_core/physics.py`
9. `topology_core/aggregate.sql`
10. `topology_core/verify.py`
11. `topology_core/determinism.py`
12. `tests/test_segment_contract.py`
13. `tests/test_cartridge_invariants.py`
14. `tests/test_v8_headlines.py`
15. `.github/workflows/topology_audit.yml`
16. `.github/workflows/topology_apply.yml`

Do not start with capacitance, PEEC or fleet mutual coupling before the segment contract and two basic cartridges pass.

## 15. Execution phases and gates

### Phase A — repair V8 browser

Complete when:

- all source is formatted;
- lead feasibility uses two module pitches or measured routed span;
- infeasible leapfrog does not claim savings;
- fleet uses actual total string count;
- all-string schedule is visible;
- golden tests pass.

### Phase B — segment contract and cartridges

Complete when:

- sequential and leapfrog emit the same schema;
- no physics function checks topology name;
- factory lead invariant passes;
- route continuity passes;
- headline V8 quantities reproduce from segment sums.

### Phase C — Parquet and DuckDB

Complete when:

- 18,918-string synthetic fleet builds successfully;
- outputs are zstd Parquet;
- row keys are unique;
- aggregate tables reconcile;
- deterministic double build is byte-identical;
- independent audit passes.

### Phase D — browser consumption

Complete when:

- the V8 page displays generated site summary;
- one inverter and one string can be inspected without loading fleet JSON;
- exported data carries schema and build hashes;
- V6 and V7 remain available and unchanged.

### Phase E — advanced electrical physics

Only after Phases A to D pass may the build add:

- segmented inductance;
- loop-area aggregation;
- differential and common-mode capacitance;
- frequency-dependent resistance bounds;
- water-film parameter studies;
- inverter termination models;
- reflection coefficients;
- PEEC validation for selected archetypes.

## 16. Prohibited shortcuts

Do not:

- return to mega-line source;
- put the 18,918-string fleet into one JSON file;
- multiply the 24-string archetype by inverter count and call it site truth;
- show leapfrog saving when factory leads fail the reach screen;
- change factory lead conductor between topologies;
- mix topology generation and physics calculations in one cartridge;
- duplicate formulas in Python and JavaScript;
- rely on file count, file size or a green workflow as proof;
- silently use cable outside diameter as conductor diameter;
- silently use internal inductance in propagation velocity;
- merge differential and common-mode capacitance;
- reproduce confidential or licensed project material in public outputs.

## 17. First action on resumption

On the next build turn, do not begin by adding more physics.

Begin by:

1. creating a restore point;
2. formatting current V8 source;
3. adding `total_site_string_count`;
4. replacing the current lead gate with the two-module-pitch rule;
5. updating and running fixtures;
6. writing `DATA_CONTRACT_SEGMENTS.md`;
7. reporting the exact commits and live test links.

This sequence is binding unless a repository law proves a conflict.