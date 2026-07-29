# Claude Deep-Research Brief — Interactive String and Table Layout Automation

## Mission

Research the governing formulas, algorithms and software architecture needed to make V10 a plug-and-play solar DC layout instrument where a user can drag modules, tables, strings, routes, connectors, SPDs and inverter inputs onto a canvas, connect them visually, and receive deterministic engineering results from a separate computation kernel.

Do not name or reproduce any person, client, project, site or confidential source. Convert all useful evidence into generic topology classes, parameter ranges, test cases and source references.

## Non-negotiable architecture

The visual editor must never contain hidden engineering formulas. It emits a canonical JSON graph. The computation kernel consumes that graph and returns canonical JSON results. The renderer displays those results without independently recomputing them.

Required chain:

user action -> geometry graph -> electrical connectivity graph -> validation -> kernel request -> kernel result -> visual and tabular rendering

## Research questions

### 1. Layout geometry

Derive robust methods for:

- rectangular, staggered, east-west, portrait, landscape and tracker table generation;
- module-centre, edge, junction-box and connector-terminal coordinates;
- row pitch, table pitch, clamp gaps, inter-module gaps, tilt projection and terrain offsets;
- snapping, alignment, collision detection, overlap detection and minimum-clearance constraints;
- affine transforms for drag, rotate, mirror, duplicate and array operations;
- physical route length through polyline segments, bend allowance, vertical drops, service loops and slack factors;
- distinction between plan distance, surface distance, cable-centreline distance and conductor length.

Identify exact formulas, computational-geometry algorithms and suitable primary references.

### 2. Electrical topology construction

Research methods to convert visual connections into an ordered DC circuit graph that can:

- identify positive and negative terminals;
- generate sequential, mirrored, leapfrog, serpentine and custom module orders;
- detect open circuits, shorts, polarity reversals, duplicate terminal use and disconnected objects;
- separate physical adjacency from electrical connectivity;
- distinguish factory leads, extension leads, field-installed string cables, harnesses and home runs;
- determine ordered current paths and conductor counts automatically;
- support multiple strings per MPPT and multiple MPPTs per inverter.

Compare graph-theory approaches including directed multigraphs, typed property graphs, union-find for connectivity, topological traversal and cycle detection.

### 3. Automatic stringing and table allocation

Research optimisation formulations for automatically assigning modules to strings and strings to MPPTs while respecting:

- minimum and maximum modules per string;
- cold Voc and hot Vmp limits;
- inverter MPPT current and short-circuit limits;
- module-bin compatibility;
- table boundaries, row geometry and cable reach;
- minimised field-installed conductor length;
- minimised connector count and route crossings;
- balanced MPPT loading and string-length ratios;
- user-locked modules, routes or inverter assignments.

Evaluate deterministic heuristics, shortest-path methods, minimum-cost flow, bipartite matching, integer linear programming, constraint programming and mixed-integer optimisation. State which problems are NP-hard, what scale each method can handle in-browser, and when a server-side or Web Worker solver is required.

### 4. Drag-and-drop interaction model

Research an interaction contract suitable for engineering software:

- every drag is a geometry edit, not an electrical calculation;
- undo/redo through immutable commands or event sourcing;
- stable object IDs and deterministic serialization;
- snapping tolerances expressed in screen pixels but resolved in model units;
- selection, grouping, locking, cloning, mirroring and bulk-edit behaviour;
- visual distinction between valid, incomplete, warning and invalid states;
- incremental kernel recomputation after local edits;
- performance methods for thousands of modules, including spatial indexes, R-trees, quadtrees and viewport culling.

Compare SVG, Canvas, WebGL and hybrid rendering for large utility-scale layouts.

### 5. Computation-kernel boundary

Define the exact canonical request and result schemas required for a kernel component.

The request must include:

- schema version;
- typed objects and terminals;
- physical coordinates and route polylines;
- electrical edges;
- component-library references;
- environmental and operating cases;
- source provenance and uncertainty;
- requested calculations.

The result must include:

- validation errors and warnings;
- ordered circuit paths;
- conductor schedule by ownership/type;
- length, resistance, voltage drop, power loss and energy loss;
- connector and termination resistance;
- cold Voc, hot Vmp, current and protection checks;
- loop area, inductance, capacitance and transmission-line applicability screens;
- surge and induced-voltage bounds;
- per-string, per-MPPT, per-inverter and plant totals;
- formula trace, assumptions, source references and uncertainty;
- deterministic hash excluding timestamps.

Recommend whether the first kernel should be pure JavaScript/TypeScript, WebAssembly, Python service or a dual implementation. The browser renderer must remain a thin client.

### 6. Incremental recomputation

Research dependency-graph and memoisation approaches so moving one module or route only invalidates affected quantities. Define dependency keys for geometry, connectivity, component data, temperature cases and electromagnetic cases. Compare structural hashing, content-addressed caching and reactive DAG execution.

### 7. Formula validation

For every proposed formula:

1. derive it from first principles;
2. state units, assumptions and validity range;
3. compare against authoritative standards, textbooks, peer-reviewed papers or OEM primary documents;
4. provide at least one hand-calculated reference case;
5. provide limiting-case and dimensional checks;
6. identify where the engine must return a bound or warning rather than a precise answer.

Do not treat previous engine values, AI output, vendor claims or supplied plots as proof.

## Required deliverables

1. A formula and algorithm register.
2. A canonical editor-to-kernel JSON schema proposal.
3. A canonical kernel-result JSON schema proposal.
4. A layout-object and terminal taxonomy.
5. An automatic-stringing optimisation comparison.
6. A rendering technology comparison for 100, 1,000, 10,000 and 100,000 modules.
7. An incremental-recomputation architecture.
8. A deterministic test catalogue with numeric expected values.
9. A phased implementation roadmap from basic drag-and-drop through automatic stringing and full engineering reports.
10. A source matrix limited to authoritative primary writing wherever possible.

## Acceptance standard

The research is not complete unless a developer can implement the editor, kernel interface and first automatic-stringing solver directly from the deliverables without inventing missing definitions. All outputs must remain generic and publishable.