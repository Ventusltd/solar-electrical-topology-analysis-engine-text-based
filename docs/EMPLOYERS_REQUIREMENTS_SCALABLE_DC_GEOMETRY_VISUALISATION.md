# Employer's Requirements — Scalable DC Geometry Visualisation and Physics Platform

## 1. Purpose

The employer requires a DC-side photovoltaic engineering platform that can represent, validate, calculate and visualise layouts ranging from a single string to utility-scale plants containing hundreds of thousands of modules. The current work has established the essential foundations: geometry-derived string placement, deterministic terminal coordinates, configurable sequential, leapfrog and custom electrical orders, arbitrary MPPT and string allocation, V7-style inverter overview drawings, V8-style detailed module connection drawings, and automatic derivation of positive and negative external cable lengths from the physical arrangement.

The next stage must convert this into a scalable engineering system rather than a large browser drawing. The platform shall preserve the existing principle that geometry is authoritative: module, terminal, string, route, trench, combiner and inverter coordinates shall drive cable quantities and electrical calculations. The browser shall not invent decorative or approximate cabling. Every rendered line shall correspond to a defined physical or electrical object, a validated route, or an explicitly labelled illustrative projection.

## 2. Existing capability to be retained

The V10 geometry visualiser currently enables users to configure module count, topology, MPPT count, inputs per MPPT, string assignments, string positions, east and west faces, table rows and columns, row pitch, module dimensions, gaps, inverter position, trench position, routing slack and termination allowances. It computes free terminal locations from the selected electrical order and derives orthogonal routes to the inverter. It then calculates positive cable length, negative cable length, total circuit length, temperature-corrected resistance, voltage drop and resistive loss.

Two visual cartridges have been established. V7 overview mode shows the inverter and many complete strings together, allowing the user to understand MPPT allocation, face, row, column and overall cable routing. V8 detail mode keeps physical modules fixed and displays the actual connector order, terminal polarity, module-to-module links, turnaround and free terminals. These modes shall remain complementary views of one common geometry and topology model.

## 3. Scale target

The system shall support plant-scale studies without requiring every module to be rendered simultaneously. A representative 1,350 kVA inverter may have 32 MPPTs and potentially two or more string inputs per MPPT. A plant may contain hundreds of such inverters, tens of thousands of strings and several hundred thousand modules. The data model, calculation pipeline and visualisation architecture shall therefore operate at multiple levels of detail.

At minimum, the following hierarchy shall be supported:

- project;
- inverter block;
- inverter;
- MPPT;
- input;
- string;
- table or tracker row;
- module;
- terminal;
- connection;
- external conductor route;
- trench, tray or containment segment;
- connector, extension and termination.

The user shall be able to move smoothly between project overview, inverter overview, selected-string detail and individual-terminal inspection without duplicating or changing the underlying engineering data.

## 4. Geometry and topology authority

Physical geometry and electrical topology shall be stored separately but linked by stable identifiers. Physical positions shall not change merely because the electrical order changes. Sequential, leapfrog and custom connection orders shall operate on the same fixed module positions.

Geometry shall support points, polylines and reusable route corridors. Cable lengths shall be derived from route geometry rather than typed as totals. Shared trench and containment sections shall be represented once and referenced by many circuits. Where a routing method is assumed rather than surveyed, the evidence state shall be explicit.

The topology model shall permit arbitrary MPPT counts, arbitrary input counts, arbitrary string counts and valid custom module sequences. Invalid connections, duplicate module visits, omitted modules, reversed or incompatible terminal connections and impossible terminal capacities shall be rejected before calculation.

## 5. Physics requirements

The physics engine shall consume validated geometry and topology. Initial calculations shall include conductor length, resistance at operating temperature, connector resistance, voltage drop and I²R loss. The architecture shall permit later addition of inductance, capacitance, loop area, propagation delay, transient screening, EMC studies, stored energy, cold open-circuit voltage, fault studies and uncertainty intervals.

Calculations shall be hierarchical. Module and segment results shall aggregate to string, MPPT, inverter and plant totals without recalculating unchanged geometry. Repeated strings and repeated inverter blocks shall support archetype-based computation, provided each instance retains its own identity, location and route references.

Every authoritative result shall produce a deterministic receipt containing input identifiers, geometry hash, topology hash, method version, formula identifiers, evidence floor, warnings and calculated totals.

## 6. Visualisation requirements

The browser shall be a thin, interactive renderer over prepared geometry and results. It shall support pan, zoom, fit, selection, filtering, search, hover inspection and drill-down. It shall not attempt to render hundreds of thousands of individual modules at project scale.

The visualisation shall use level-of-detail rules:

- project scale: inverter blocks, routes, capacity, cable totals and heatmaps;
- inverter scale: MPPTs, string groups, table rows and trunk routes;
- string scale: full module row and free-terminal geometry;
- terminal scale: connectors, leads, extensions and detailed module order.

At low zoom levels, repeated modules shall be represented by aggregated glyphs, instanced geometry or density tiles. Detailed terminal and connector geometry shall load only for selected strings or visible regions. Off-screen geometry shall not be created in the document object model.

The system shall preserve V7 as the overview visual language and V8 as the detailed connection visual language. V10 shall add scale, receipts, physics overlays and evidence rather than inventing a third unrelated drawing style.

## 7. Performance and data handling

The platform shall use spatial indexing, chunked data loading, immutable identifiers and deterministic partitions. Calculations shall support incremental recomputation so that moving one table or rerouting one corridor does not force the entire plant to be recalculated.

The browser shall receive compact machine-readable geometry, preferably indexed arrays or binary-friendly structures for large projects. Large plant datasets shall be partitioned by project, inverter block, inverter and string. The system shall support worker threads or WebAssembly for local interaction where appropriate, while authoritative calculations remain available through the Python kernel and validation pipeline.

Target interaction performance shall be approximately 60 frames per second for ordinary navigation, sub-second selection and filtering, and progressive loading for large projects. Memory use shall remain bounded by the visible region and selected detail level rather than total plant size.

## 8. Open-source research brief for Claude

Claude is requested to research current open-source methods and provide a cited architecture recommendation for implementing this system at utility scale. The research shall compare WebGL, WebGPU, Canvas, SVG, scene graphs, graph visualisation libraries, geospatial tiling, spatial indexes, binary columnar formats, instancing and level-of-detail techniques.

The review shall specifically examine suitable open-source projects and patterns such as deck.gl, luma.gl, regl, PixiJS, Three.js, MapLibre GL JS, OpenLayers, Cytoscape.js, Sigma.js, Graphology, Apache Arrow, DuckDB-Wasm, FlatGeobuf, PMTiles, GeoParquet, Zarr, H3, RBush, Web Workers, OffscreenCanvas, Comlink and Pyodide. It shall not assume these are all appropriate; it shall assess strengths, weaknesses, licensing, maintenance status, mobile performance, accessibility, deterministic rendering and integration with a Python engineering kernel.

Claude shall answer the following questions:

1. What rendering architecture best supports hundreds of thousands of modules while retaining selectable inverter, string and module detail?
2. Should the project overview be geospatial tiles, a WebGL scene, or a hybrid?
3. How should repeated module and string geometry be instanced rather than duplicated?
4. How should geometry, topology and calculation receipts be partitioned and streamed?
5. Which spatial index and binary formats are most suitable for browser delivery?
6. How should V7 overview and V8 detail cartridges share one scene and one data model?
7. What calculations can safely run in the browser, and which should remain authoritative in Python?
8. How can incremental recalculation be implemented when users move tables, trenches or inverters?
9. What open-source architecture offers the best route from the existing static GitHub Pages workbench to a production multi-user application?
10. What benchmark plan should be used at 10,000, 100,000, 500,000 and 1,000,000 modules?

The required output is a decision paper with citations, a recommended component stack, at least two credible alternative architectures, a data-flow diagram, a level-of-detail strategy, a benchmark plan, principal risks, licensing considerations and a phased implementation roadmap. The recommendation must remain DC-side only and must preserve the governing rule: topology and physics follow validated geometry; the renderer does not invent cable routes.
