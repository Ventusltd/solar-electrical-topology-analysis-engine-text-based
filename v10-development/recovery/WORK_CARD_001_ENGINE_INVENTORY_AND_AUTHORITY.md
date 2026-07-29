# Work Card 001 — Engine Inventory and Authority Selection

## Objective

Establish the exact computation paths already present in the repository, freeze their current behaviour, and select one provisional authoritative kernel before new engineering functions are added.

## Why this work comes first

The repository already contains a Python package, multiple JavaScript generations, cartridge logic, topology generation, tests and browser code. Adding new equations before these paths are reconciled would create further duplication and make later validation harder.

The browser is not the authority. Geometry, topology and calculations must remain executable without a renderer.

## Confirmed Python core

Package: `src/solar_topology/`

The package currently exports:

- topology cartridges and cross-cartridge validation;
- deterministic fleet-store generation;
- resistance, cold Voc, electric-energy, magnetic-energy and two-wire parameter functions;
- conductor product records;
- physical segment, string and topology inputs;
- headless geometry-to-segment generation and export.

### Confirmed formula path

File: `src/solar_topology/formulas.py`

Current functions and treatment:

| Function | Present purpose | Current authority treatment |
|---|---|---|
| `dc_resistance` | Finished-cable resistance with conductor-temperature correction | Provisional authoritative Tier 1 function |
| `two_wire_parameters` | External and internal inductance, capacitance, characteristic impedance and propagation velocity from declared geometry | Provisional authoritative Tier 1 function; requires benchmark validation |
| `module_frame_capacitance` | Indicative parallel-plate module-to-frame capacitance | Research/indicative only; not a compliance result |
| `cold_string_voc` | Linear cell-temperature screen for maximum string Voc | Provisional physical screen; standards-prescribed methods must remain separate |
| `derived_route_length` | Geometry-derived route length without a user-entered final route value | Provisional authoritative geometry rule |
| `stored_magnetic_energy` | Lumped magnetic stored energy | Provisional authoritative Tier 1 function |
| `stored_electric_energy` | Lumped electric stored energy | Provisional authoritative Tier 1 function |

### Confirmed topology path

File: `src/solar_topology/topology.py`

Current objects:

- `Point3D`
- `Segment`
- `StringTopology`
- `GeometryConfig`
- `FormationConfig`

Current functions:

- `_polyline_length`
- `_segment`
- `build_string_segments`
- `build_site_model`
- `build_export`
- `validate_no_user_route_lengths`

Current strengths:

- headless operation;
- typed segment sequence;
- installed length separated from geometric displacement;
- explicit formation and conductor separation;
- provenance field on every segment;
- final route length derived from the segment list rather than accepted as a free user input.

Current restrictions and risks:

- topology currently embeds assumptions such as coil surplus, return spacing, trench spacing and structure drop in configuration defaults;
- `build_string_segments` represents one particular physical route construction and is not yet a general terminal-and-connectivity graph;
- module leads, connector contacts, polarity and actual ordered terminals are not yet represented as first-class connected objects in this file;
- several provenance values are free text and need controlled enums plus evidence references;
- the current route builder must not be declared universal merely because it is executable.

## Confirmed test path

File: `tests/test_formulas.py`

The tests already enforce important engineering doctrine:

- nominal CSA must not be used to invent conductor diameter;
- internal inductance is separated from the external propagation term;
- propagation velocity uses external inductance only;
- invalid overlapping conductor geometry is rejected;
- rank pitch excludes an invented walkway allowance;
- route length is derived from geometry only;
- users cannot inject a final route length;
- declared finished-cable resistance is temperature corrected;
- a complete-circuit canary includes external cable, module leads and connector contacts;
- module-frame capacitance and cold Voc calculations have numerical checks.

## Work scope

### A. Complete Python inventory

Inspect and record every public class and function in:

- `src/solar_topology/cartridges.py`
- `src/solar_topology/segments.py`
- `src/solar_topology/products.py`
- `src/solar_topology/fleet_store.py`
- all files under `tests/`

For every capability record:

- exact file;
- function or class;
- inputs and units;
- output and units;
- physical equation or algorithm;
- assumptions and defaults;
- provenance treatment;
- tests;
- known defects;
- proposed authority status.

### B. Inventory JavaScript generations

Locate and record the exact V8, V9 and V10 calculation files and tests.

For each function classify it as:

- authoritative candidate;
- compatible duplicate;
- reference implementation;
- browser adapter;
- renderer-only;
- obsolete;
- unresolved.

### C. Inventory terminal-geometry work

Locate the terminal-geometry implementation and its tests. Record:

- object schema;
- terminal ordering;
- polarity representation;
- connectivity representation;
- physical lead geometry;
- the exact failing test and failure cause;
- capabilities absent from the current Python topology path.

### D. Freeze baseline behaviour

Record exact commands and results for:

- Python tests;
- V8 tests;
- V9 tests;
- V10 tests;
- terminal-geometry tests.

No numerical behaviour is to be changed during inventory except where required to make the test harness reproducible.

### E. Repair only confirmed defects

After the baseline is committed:

1. replace inappropriate exact floating-point equality with tolerance-based comparison where the engineering result is correct;
2. repair the terminal-geometry failure after identifying whether the defect is in the implementation, fixture or expectation.

Do not change equations merely to force tests to pass.

## Authority decision rule

The provisional authority should be selected capability by capability, not by version name.

A function can be authoritative only when it has:

- explicit units;
- declared physical inputs;
- no renderer dependency;
- traceable assumptions;
- deterministic output;
- numerical tests;
- a clear validity boundary;
- no silent substitution of nominal or assumed geometry for required measured/manufacturer data.

The expected architectural outcome is:

> Python becomes the provisional authoritative headless computation kernel. JavaScript becomes a validated adapter, compatibility implementation or browser client unless a specific JavaScript capability is demonstrably stronger and is deliberately migrated.

This is a hypothesis to be tested by the inventory, not a declaration made in advance.

## Deliverables

1. Populated V6–V10 migration ledger with exact files and symbols.
2. Engine inventory table covering Python, V8, V9, V10 and terminal geometry.
3. Frozen test-baseline record with commands and outputs.
4. Two defect records for the known failures.
5. Authority decision record for every existing capability.
6. A short list of capabilities to migrate into the canonical Python kernel first.

## Acceptance criteria

This work card closes only when:

- every executable calculation path has been located;
- every public calculation has an authority classification;
- all current test commands are reproducible;
- the two known failures are explained and either repaired or explicitly quarantined;
- no browser-rendered value is treated as authoritative without a mapped headless function;
- the next code change can be selected from evidence rather than assumption.

## First implementation queue

1. Inventory `cartridges.py` and its tests.
2. Inventory `segments.py` and its tests.
3. Inventory `products.py` and `fleet_store.py`.
4. Locate all JavaScript kernels and test runners.
5. Locate terminal-geometry files and reproduce its failing test.
6. Populate the migration ledger.
7. Commit the baseline.
8. Repair the two known failures.
9. Issue the authority decision.
