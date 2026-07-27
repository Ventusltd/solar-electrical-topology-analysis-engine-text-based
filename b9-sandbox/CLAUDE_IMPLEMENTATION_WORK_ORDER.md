# Claude implementation work order — B9 multi-array electrical sandbox

## Binding instruction

Study the repository deeply before writing code. Inspect the root V6 workbench, all V7 development and FEED material, V8 leapfrog workbench, technical commentary, schemas, tests, restore points and repository history. Do not redesign blindly. Do not overwrite V6, V7 or V8. Work additively under `b9-sandbox/` unless a small root navigation update is separately justified.

Create a restore point before every risky edit. Work on `main` only. Keep GitHub Pages operable. Do not use confidential, customer-specific, employer-requirement, NDA, as-built or proprietary calibration data. Distil only generic engineering principles supported by public sources or first principles.

## Required return

Return both code and mathematics. A prose-only answer is a failure. A visual mock-up without a canonical data model is a failure. A calculation engine that cannot draw and edit multiple array archetypes is a failure.

Deliver:

1. a repository examination report identifying what V6, V7 and V8 actually do;
2. a UI architecture decision with alternatives considered;
3. a versioned canonical schema;
4. working B9 browser code;
5. cartridge definitions;
6. plan, side and circuit views;
7. ordered conductor-segment generation;
8. a technician summary;
9. Parquet, DuckDB and GeoJSON export/build code;
10. tests and independently calculated numerical fixtures;
11. a 1,000-word electrical study;
12. a limitations and measurement plan.

## Core product question

Design a serious engineering sandbox in which a user can assemble and manipulate PV arrays as directly as objects in a simulation game, while ensuring that every visible cable, module, terminal, connector, frame and route resolves to a traceable electrical topology.

The interface may take inspiration from the direct manipulation and layered inspection found in Unreal Engine and Kerbal Space Program, but it must remain an original engineering UI.

## Mechanical cartridges to implement first

Implement at least:

- fixed tilt, one in portrait;
- fixed tilt, two in portrait;
- east-west, one in portrait per face;
- east-west, five in portrait per face;
- legacy fixed tilt, six in landscape using editable smaller-module dimensions;
- tracker, one in portrait;
- tracker, two in portrait.

The cartridge system must make three, four, five or six in portrait/landscape straightforward additions rather than hard-coded rewrites.

Each cartridge shall expose module width, module length, gap, tilt, row pitch, face count, ridge gap, low-edge height, axis height, tracker angle, junction-box position, rail/pile positions and cable anchors as applicable.

## Electrical topology cartridges

Implement at least:

- sequential;
- leapfrog;
- mirrored sequential;
- alternating return;
- custom ordered path.

Mechanical arrangement and electrical ordering are independent selections. Leapfrog must alter connectivity and path lengths, not merely draw a different line colour.

## Views

### Plan view

Support long arrays, pan, zoom, selection, group duplication, row repetition, inverter placement, trench routes, route anchors and level of detail.

### Side view

Add an explicit `Side view` button. For east-west arrays show the elevation as a house-of-cards profile. For trackers show torque tube, rotation axis, module chord and operating/stow angles. Side-view geometry must supply electrical height and separation inputs.

### Circuit view

Show electrical order, module numbers, junction boxes, factory leads, field connectors, polarity, free terminals, MPPT and inverter termination.

All views shall use the same object IDs and canonical model.

## Canonical object model

Use versioned entities and stable IDs. Separate:

- object identity;
- geometry;
- terminals;
- connectivity;
- ordered conductor segments;
- material and environment;
- assumptions and measurements;
- study inputs and results.

At minimum provide typed representations for site, block, cartridge instance, table, face, tracker, module, junction box, connector, terminal, cable anchor, conductor, conductor segment, coil, route environment, frame, rail, pile, earth node, SPD, combiner, MPPT, inverter, assumption, measurement, study run, result and warning.

Do not store the entire model as opaque nested JSON only. JSON may be used for browser interchange, but analytical export must be tabular and typed.

## Storage and scale

Design for synthetic scenes of at least 100,000 modules and long utility rows.

Use:

- an indexed in-memory scene graph for interaction;
- Web Workers for expensive derivation;
- viewport culling and level of detail;
- Parquet as durable analytical output;
- DuckDB for local analytical queries over Parquet;
- GeoJSON for spatial interchange and map layers.

Explain whether DuckDB-Wasm belongs in the browser or in an offline build/export path. Benchmark both or justify the chosen split. Do not force the renderer to query DuckDB for every mouse move.

## Suggested Parquet tables

Provide schemas for:

- objects;
- geometries;
- terminals;
- connectivity;
- segments;
- materials;
- environments;
- assumptions;
- measurements;
- study runs;
- study results;
- warnings.

Every row shall include schema version and stable IDs. Units shall be explicit through column names or a unit registry. Provenance and evidence class shall be queryable.

## GeoJSON exports

Provide site boundaries, block polygons, row centre-lines, table footprints, inverter points, trench routes, electrical paths and warning locations. Preserve canonical IDs and CRS metadata. Avoid exporting millions of full module polygons by default; provide selectable detail levels.

## Electrical derivation

Generate ordered positive and negative conductor segments from topology and geometry. Each segment shall include length, coordinates, polarity, conductor material, nominal and actual CSA where known, temperature, return-path spacing, height above earth, frame distance, route environment, formation, connector boundaries and coil attributes.

### Resistance

Use:

`R_i(T_i) = ρ_20 l_i/A_i [1 + α(T_i - 20 °C)]`

Complete circuit:

`R_total = ΣR_positive + ΣR_negative + ΣR_factory_leads + ΣR_connectors + ΣR_terminations + ΣR_devices`

Keep cable-only and complete-circuit outputs separate.

### Copper mass

Expose both:

`m_commercial = A_nominal L_km × 9.6`

and

`m_physical = A_actual L_km ρ_Cu`

Label the first as the established commercial copper-weight basis and the second as a density/construction basis. Allow manufacturer-declared copper content to override estimates.

### Loop area

Calculate signed and absolute loop area from ordered positive and negative paths. Use a polygon/shoelace method after constructing the closed loop and document projection assumptions. Report local separation hotspots and the percentage of the route where conductors are paired.

### Differential inductance

For straight paired segments, implement and verify an appropriate two-wire closed-form expression such as:

`L'_diff ≈ (μ0/π) acosh(D/(2r))`

within its validity region. Distinguish low-frequency inductance including internal conductor inductance from high-frequency external inductance. Do not apply one spacing to the full route.

For irregular geometry, evaluate whether partial-element equivalent circuit methods are justified for a later cartridge. Do not claim full PEEC accuracy if only a segment approximation is implemented.

### Common mode

Create a separate common-mode network against frame, rail, pile, soil and remote earth. Do not infer common-mode inductance by reusing differential loop inductance.

### Coils

Represent surplus cable coils as explicit objects. Inputs: pole arrangement, number of turns, mean diameter, pitch, coiling of one pole or both poles, spacing and nearby conductive structure. If both poles are coiled together, account for cancellation rather than adding two independent solenoids.

### Capacitance

Keep separate:

- conductor-to-conductor differential capacitance;
- positive-to-frame/earth capacitance;
- negative-to-frame/earth capacitance;
- module internal/differential capacitance;
- module/frame/earth common-mode capacitance;
- inverter input and EMC capacitor branches.

Use visible bounding calculations such as:

`C = ε0 εr A/d`

only where geometry supports them.

Dry capacitance remains present when wet:

`C_total(f) = C_dry(f) + C_film(f,σ,geometry,contamination)`

Implement a frequency-dependent water-film participation model or, if not defensible in the first code release, provide a bounded dry/local-wet/global-wet model with prominent `measurement required` status. Never describe a full-area wet value as measured without evidence.

### Distributed line

Where per-unit-length parameters are available:

`Z0(f) = sqrt((R' + jωL')/(G' + jωC'))`

`γ(f) = sqrt((R' + jωL')(G' + jωC'))`

`τ = l/v_p`

Classify lumped versus distributed treatment by comparing event rise time and route delay. Do not assign the complete string one universal resonance.

### Stored energy and interruption

Calculate:

`W_L = 0.5LI²`

`W_C = 0.5CV²`

Use `L di/dt` only for cases where a lumped approximation is defensible. For fast events, show the travelling-wave/I×Z0 bound and termination dependence.

## Required 1,000-word study

Write an approximately 1,000-word public electrical study entitled:

`Inductive loops, module capacitance and distributed behaviour in configurable PV strings`

It must cover:

- why visible topology changes electrical behaviour;
- sequential versus leapfrog loop geometry;
- differential and common-mode separation;
- local route spacing and structure drops;
- factory leads, connectors and coils;
- dry module capacitance;
- wet-film participation and frequency dependence;
- insulation-monitoring boundaries;
- inverter termination uncertainty;
- event rise time versus propagation delay;
- lumped versus distributed models;
- required field and laboratory measurements;
- what is normative, engineering-derived and research-dependent.

Use equations, ranges and uncertainty. Do not fill the word count with marketing.

## UI decision task

Compare at least three UI architectures, for example:

1. single SVG scene;
2. Canvas/WebGL scene plus DOM inspector;
3. hybrid SVG for detailed table editing and Canvas/WebGL for site scale.

Assess performance, accessibility, hit testing, export quality, long-array rendering, side-view support, extension cartridges and maintainability. Select one and explain why.

The selected design must include:

- hierarchy tree;
- cartridge palette;
- property inspector;
- plan/side/circuit view switcher;
- layer manager;
- validation/warning panel;
- technician summary;
- study runner;
- export panel;
- deterministic undo/redo.

## Tests

Provide unit tests for:

- module/table geometry;
- side-view elevations;
- sequential path ordering;
- leapfrog path ordering;
- row-span cable saving;
- conductor segment lengths;
- resistance at multiple temperatures;
- commercial and physical copper mass;
- polygon loop area;
- two-wire inductance fixture;
- capacitance unit conversion;
- aggregation at string, MPPT and inverter boundaries;
- GeoJSON ID preservation;
- Parquet/DuckDB deterministic totals;
- import/export round trip.

Include hand-calculated fixtures. Do not test only that functions return numbers.

## Performance demonstration

Generate synthetic projects of:

- 30 modules;
- 10,000 modules;
- 100,000 modules.

Report generation time, segment count, memory use, render strategy and DuckDB aggregation time. The 100,000-module case need not display every connector simultaneously, but its topology and analytical data must remain available.

## Technician summary output

The technician summary must be plain, auditable and exportable. It shall state:

- cartridge and dimensions;
- module orientation and count;
- electrical order;
- terminal positions;
- positive and negative external lengths;
- factory lead length and feasibility;
- connector count;
- resistance and voltage drop;
- cable and copper mass;
- loop area and separation hotspots;
- coils;
- dry/wet capacitance range;
- monitoring boundary;
- propagation delay and modelling class;
- warnings and missing measurements.

## Development discipline

Do not modify the stable workbenches merely to make B9 easier. Reuse concepts, not hidden global state. Document all copied code and why it was copied. Avoid monolithic HTML when modules can be separated cleanly. Preserve a no-build fallback if practical, but do not sacrifice testability and scale merely to keep everything in one file.

Before committing, verify that no confidential names, values, screenshots, drawings or contractual text have entered the repository.
