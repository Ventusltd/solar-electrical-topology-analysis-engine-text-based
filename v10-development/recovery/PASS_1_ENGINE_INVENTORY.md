# Pass 1 — Engine Inventory

Status: completed repository inventory sufficient to begin capability reconciliation. This pass records what exists and where. It does not yet promote any implementation to final authority.

## 1. Python package and dependency boundary

Path: `pyproject.toml`

The Python package is `solar-electrical-topology-engine` version 0.3.0, requires Python 3.11 or newer, and depends on DuckDB, NumPy and Pint. Pytest is the declared test runner.

Provisional treatment: authoritative-kernel candidate.

## 2. Python public API

Path: `src/solar_topology/__init__.py`

The package exports formulas, products, segment objects, topology builders, sequential and leapfrog cartridges, fleet builders, validation functions and deterministic DuckDB/Parquet store builders.

## 3. Python formula layer

Path: `src/solar_topology/formulas.py`

Confirmed functions:

- `dc_resistance()` — finished-cable R20 with conductor-temperature correction;
- `two_wire_parameters()` — external and internal inductance, capacitance, characteristic impedance and propagation velocity;
- `module_frame_capacitance()` — indicative parallel-plate module-to-frame capacitance;
- `cold_string_voc()` — linear cold-Voc screen;
- `derived_route_length()` — geometry-derived route rule with no user final-length input;
- `stored_magnetic_energy()`;
- `stored_electric_energy()`.

Strengths:

- Pint unit safety;
- explicit physical guards;
- finished-cable resistance kept separate from nominal CSA;
- internal inductance separated from propagation inductance;
- deterministic closed-form calculations.

Provisional treatment: strongest formula authority candidate found.

## 4. Python topology-cartridge layer

Path: `src/solar_topology/cartridges.py`

Confirmed architecture:

- abstract `TopologyCartridge` contract;
- `SequentialCartridge` version 1.1.0;
- `LeapfrogCartridge` version 1.1.0;
- cartridge manifests with input hash, cartridge hash, source commit, feasibility and warnings;
- complete positive-to-negative ordered segment chains;
- explicit factory positive and negative leads;
- explicit module connector contacts;
- positive and negative home runs;
- sequential far-end return;
- leapfrog feasibility screen;
- fleet segment generator;
- contiguous segment and node-chain validation;
- cross-cartridge factory-lead and connector-count invariants.

Important findings:

- Cartridges emit topology and physical segments, not hidden electrical totals.
- Leapfrog order is odd modules ascending followed by even modules descending.
- Leapfrog feasibility currently uses a measured routed span when supplied, otherwise a two-module-pitch screen.
- Factory junction-box and lead geometry is still marked unresolved.
- Sequential return geometry is explicitly warned as requiring a loop model.

Provisional treatment: authoritative topology candidate, subject to terminal-geometry reconciliation.

## 5. Python shared segment schema

Path: `src/solar_topology/segments.py`

Confirmed objects:

- `Point3D`;
- `FeasibilityResult`;
- `TopologyInputs`;
- `StringDefinition`;
- `SegmentRow`;
- `SegmentBuilder`.

The segment row records:

- topology, inverter, MPPT, string and ordered segment identity;
- from/to nodes and 3D coordinates;
- displacement and installed conductor length;
- formation and installation class;
- conductor product, CSA, conductor diameter, cable OD and R20;
- temperature and effective relative permittivity;
- loop-parameter weight;
- coil and connector data;
- provenance, source reference, override status, feasibility and warnings.

Validation prevents missing keys, invalid indices, negative lengths, invalid loop weights, negative connector resistance, invalid provenance, impossible cable/conductor diameters and invalid R20.

Important limitation: the current allowed provenance vocabulary is narrower than the later engineering evidence register and will require schema reconciliation.

Provisional treatment: authoritative segment-schema candidate.

## 6. Python product layer

Path: `src/solar_topology/products.py`

Confirmed `ConductorSpec` fields:

- product identifier;
- nominal CSA;
- actual declared conductor diameter;
- cable outside diameter;
- finished-cable R20;
- provenance.

The code deliberately rejects deriving conductor diameter from nominal area and validates a plausible stranded-conductor envelope fill factor.

Current generic records:

- factory module lead 4 mm²;
- external string cable 6 mm².

Provisional treatment: authoritative product-record pattern; current records remain generic defaults, not project approvals.

## 7. Python fleet, DuckDB and Parquet layer

Path: `src/solar_topology/fleet_store.py`

Confirmed capabilities:

- deterministic segment CSV generation;
- DuckDB segment table;
- Parquet outputs;
- string, MPPT, inverter and site aggregation;
- sequential-versus-leapfrog comparison;
- data-law checks for keys, duplicates, contiguous indices, node continuity, lengths, loop weights, connector resistance, provenance, conductor geometry, pair geometry and cross-cartridge invariants;
- separate factory and external conductor totals;
- resistance, inductance and capacitance result aggregation.

Provisional treatment: authoritative persistence and aggregation candidate.

## 8. Separate Python headless geometry path

Path: `src/solar_topology/topology.py`

Confirmed capabilities:

- renderer-independent 3D geometry;
- typed segments and string topology;
- module interconnects, surplus coils, row return, table transfer, structure drop and surface/trench run;
- route lengths derived from segment geometry;
- complete site model and export.

Important architectural finding: this is a second Python geometry/segment representation alongside `segments.py` and `cartridges.py`. It must be reconciled rather than silently retained as a parallel authority.

Provisional treatment: recoverable geometry implementation; authority unresolved against the cartridge schema.

## 9. V8 JavaScript engine

Confirmed path: `v8-leapfrog/model.js`

Confirmed executable test: `tests/v8-model.test.js`

Confirmed capabilities from the regression contract:

- 24 strings per inverter;
- row-span geometry;
- sequential and leapfrog external cable totals;
- fleet cable-saving aggregation;
- invariance of topology saving to inverter-distance change;
- east/west near-route and far-route handling;
- embedded golden-test runner.

Known role: sequential-versus-leapfrog comparison workbench and historical reference implementation.

Provisional treatment: reference and regression source, not final authority.

## 10. V9 JavaScript debug engine

Paths:

- `v9-sandbox/debug/engine.js`;
- `v9-sandbox/debug/tests.js`;
- `v9-sandbox/debug/run-tests.mjs`.

Confirmed capabilities:

- sequential, mirrored-sequential, alternating-return, leapfrog and custom module order;
- custom-order exact-permutation validation;
- MPPT allocation with a 24-active-string cap;
- module and terminal objects;
- segment generation;
- centre-to-centre extension screening;
- cold Voc correction;
- copper resistance from bulk resistivity and nominal CSA;
- voltage drop and loss;
- deterministic project result excluding timestamp.

Important weaknesses relative to Python:

- accepts user-entered one-way route length;
- recreates resistance from bulk copper resistivity and nominal CSA rather than declared finished-cable R20;
- terminal coordinates are not modelled;
- module-centre separation is explicitly a screening estimate;
- only external resistance is included in its string loss calculation.

Provisional treatment: valuable UI, allocation and topology reference; not formula authority.

## 11. V10 JavaScript candidate kernel

Paths:

- `v10-development/src/kernel.mjs`;
- `v10-development/src/electrical.mjs`;
- `v10-development/src/topology.mjs`;
- `v10-development/src/quantity.mjs`;
- `v10-development/tests/kernel.test.mjs`;
- `v10-development/tests/topology.test.mjs`;
- `v10-development/schema/kernel-input.schema.json`.

Confirmed kernel capabilities:

- canonical quantity objects with provenance, source, evidence status and interval uncertainty;
- topology-derived path length;
- resistance, voltage drop and resistive loss;
- optional cold-corrected module and string Voc;
- deterministic schema-versioned result;
- explicit warnings that it is a candidate kernel and that terminal offsets, lead slack and routed field cable are absent.

Important weakness: its geometry currently follows module-centre path length and does not yet represent the complete physical conductor circuit.

Provisional treatment: schema and evidence-model reference; not calculation authority.

## 12. Browser boundary

The V10 browser imports or invokes the V10 JavaScript kernel, but the kernel itself warns that it is incomplete. No browser calculation is promoted to authority by this inventory.

Required architectural rule remains:

`physical objects -> geometry -> terminals and connectivity -> ordered circuit -> computation kernel -> evidence-rich result -> browser rendering`

## 13. Test locations found

Python:

- `tests/` as declared by `pyproject.toml`;
- formula tests include physical doctrine, units, geometry-only routes and complete-circuit canaries.

V8:

- `tests/v8-model.test.js`.

V9:

- `v9-sandbox/debug/tests.js`;
- runner `v9-sandbox/debug/run-tests.mjs`.

V10:

- `v10-development/tests/kernel.test.mjs`;
- `v10-development/tests/topology.test.mjs`;
- package command `node --test tests/*.test.mjs` within `v10-development`.

## 14. Terminal-geometry work

The inventory confirms that terminal geometry is a known missing boundary in V9 and V10 and is explicitly unresolved in the Python cartridge warnings. The separately reported terminal-geometry test branch must therefore be treated as a recovery source, not assumed to be merged into main.

Exact branch/ref and failing assertion remain to be recorded during baseline reproduction because the repository branch-search connector did not return a branch listing. This is now a named unresolved inventory item, not a hidden omission.

## 15. Duplicated or competing implementations requiring Pass 2 reconciliation

1. `segments.py`/`cartridges.py` versus `topology.py` Python geometry models.
2. Python declared-R20 resistance versus V9 bulk-resistivity/CSA resistance.
3. Python geometry-derived route doctrine versus V9 user-entered route.
4. V10 quantity/evidence schema versus Python result objects.
5. V8 fleet saving model versus Python cartridge/fleet-store comparison.
6. V9/V10 module-centre geometry versus missing junction-box terminal geometry.
7. Multiple provenance vocabularies.

## Pass 1 conclusion

The repository contains three materially distinct computation families:

1. Python physical topology, formulas, cartridges and deterministic fleet store;
2. V8/V9 browser-era JavaScript workbenches;
3. V10 JavaScript candidate kernel and evidence schema.

The Python family is the strongest provisional authority candidate because it combines unit-safe physics, declared finished-cable properties, ordered physical segments, cartridge validation and deterministic fleet persistence. V8 and V9 contain valuable topology, UI, MPPT-allocation and regression behaviour that must be migrated selectively. V10 contains the strongest browser-facing evidence and uncertainty contract but is explicitly incomplete as a physical circuit model.

Pass 2 shall now reconcile every capability and select one owner implementation for each function without deleting historical references.