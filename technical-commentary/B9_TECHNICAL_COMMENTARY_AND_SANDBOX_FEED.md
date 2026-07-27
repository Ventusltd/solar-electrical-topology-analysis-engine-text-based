# B9 technical commentary and multi-array sandbox FEED

Status: public technical development note. No confidential project data, employer requirements, customer drawings, as-built records, NDA material or proprietary calibration is included.

## 1. Purpose

B9 is the next independent development space for the Solar Electrical Topology Analysis Engine. It is not a replacement for V6, V7 or V8. It is a public sandbox architecture intended to let a competent user construct many PV array geometries, assign wiring topologies, derive ordered conductor paths and then run electrical studies from those paths.

The governing sequence remains:

`physical objects → geometry → ordered conductor segments → electrical model → studies → exports`

The renderer is a view of the topology. It is never the source of electrical truth.

## 2. What must be inherited

### From V6

B9 shall inherit the complete-series-circuit discipline: separate external positive and negative conductors, module factory leads, extension leads, connector contacts, terminations, conductor temperatures, cable-only and complete-circuit resistance, voltage drop, power loss, loop geometry, differential inductance, common-mode quantities, propagation delay, capacitance and JSON traceability.

### From V7

B9 shall inherit dimensional safety, evidence status, uncertainty, differential/common-mode separation, frequency-aware capacitance, event-rise-time versus propagation-delay screening, transmission-line quantities, distributed-network classification and explicit measurement gates.

### From V8

B9 shall inherit topology as a selectable state. Sequential, leapfrog, mirrored, alternating, split-return and custom wiring must produce different ordered paths rather than merely different labels. External EPC-installed cable must remain separate from factory-fitted module leads.

## 3. Array cartridges

A cartridge is a reusable physical-and-electrical archetype. It contains module geometry, orientation, rank count, face count, pitch, tilt, height, junction-box location, module lead geometry, stringing rules, cable-management assumptions and compatible views.

Initial public cartridges shall include:

- one module in portrait fixed-tilt;
- two modules in portrait fixed-tilt;
- three modules in portrait fixed-tilt;
- four, five and six modules in portrait fixed-tilt;
- one module in landscape;
- two, three, four, five and six modules in landscape;
- legacy six-in-landscape tables for smaller approximately 250–330 W modules;
- east-west one-in-portrait per face;
- east-west two-in-portrait per face;
- east-west five-in-portrait per face;
- single-axis tracker one-in-portrait;
- single-axis tracker two-in-portrait;
- long-row tracker cartridges with configurable module count;
- custom cartridge assembled from modules, rails, piles, faces and routing anchors.

No module power class shall be hard-coded into geometry. A legacy 300 W module is represented by its dimensions, electrical data and lead arrangement, not by a generic decade label.

## 4. Views

B9 shall provide three linked views.

### Plan view

Shows rows, tables, faces, inverter positions, trench routes, string terminal locations, cable anchors and ordered conductor paths. It is optimised for long arrays and route editing.

### Side view

A new `Side view` button shall show elevation. East-west arrays appear as a house-of-cards profile with editable tilt, ridge gap, low-edge height, high-edge height and face separation. Tracker cartridges show torque tube, rotation axis, module chord, stow angle and operating angle. Fixed-tilt cartridges show rows, module count in portrait or landscape, rails, piles and cable height above ground.

The side view is not decorative. It supplies conductor-to-earth height, conductor-to-frame distance, local separation, structure drops and cable-management geometry to the electrical model.

### Circuit view

Shows electrical order, polarity, module numbers, junction boxes, connectors, free string terminals, MPPT allocation and inverter termination. Physical and electrical order may differ under leapfrog or custom topologies.

All three views shall resolve to the same object IDs and ordered segment graph.

## 5. Interaction design

The design target is an engineering sandbox inspired by the direct manipulation of Unreal Engine and Kerbal Space Program, without copying either product. The user should be able to place, duplicate, rotate, mirror, group and connect array cartridges, then inspect consequences.

Required interaction concepts:

- object palette for modules, tables, rows, trackers, inverters, combiner boxes, trenches, cable trays, junctions, coils, SPDs, frames, rails, piles and earth nodes;
- transform controls for move, rotate, mirror, duplicate and array-repeat;
- snapping to module edges, junction boxes, row axes, cable anchors and trench centre-lines;
- hierarchy tree for site, block, inverter, MPPT, string, module, conductor and segment;
- property inspector with units, provenance, uncertainty and validation state;
- topology cartridge selector independent of mechanical cartridge selector;
- plan, side and circuit view buttons;
- layer manager for geometry, wiring, earth, structures, route environment, warnings, calculated fields and user-defined layers;
- undo/redo and transaction history;
- deterministic object IDs and stable export order;
- no silent geometry repair.

## 6. Long-array rendering

The browser must not attempt to render every object at full detail at every zoom level. It shall use level-of-detail rules:

- site scale: blocks, rows, inverters and route envelopes;
- block scale: tables, strings and main conductor paths;
- table scale: modules, junction boxes and local leads;
- module scale: connectors, factory tails and segment anchors.

Viewport culling, spatial indexing and worker-based calculations are required. The visible canvas is a projection of the canonical model, not the database itself.

## 7. Canonical data model

B9 shall use an object-and-edge model with immutable IDs and versioned schemas.

Core entities:

- `site`
- `block`
- `array_cartridge_instance`
- `table`
- `face`
- `tracker`
- `module`
- `junction_box`
- `connector`
- `terminal`
- `cable_anchor`
- `conductor`
- `conductor_segment`
- `coil`
- `route_environment`
- `frame`
- `rail`
- `pile`
- `earth_node`
- `spd`
- `combiner`
- `mppt`
- `inverter`
- `measurement`
- `assumption`
- `study_run`
- `warning`

Topology edges shall record ordered connectivity, pole, direction, source object, target object and sequence index. Geometry and connectivity are separate tables joined by stable IDs.

## 8. GeoJSON, Parquet and DuckDB

GeoJSON is an interchange and map-rendering format, not the sole source of truth. Use it for spatial features that benefit from standard geometry: site boundaries, block polygons, row centre-lines, trench routes, inverter points, cable-route lines and optional module footprints at detailed export levels.

Parquet is the durable analytical store. Partition large datasets by project, block and entity class where useful. Keep typed columns, schema version, units, provenance and source revision. Avoid storing large repeated JSON blobs where relational columns are possible.

DuckDB is the local analytical engine. It shall query Parquet directly for geometry summaries, cable schedules, segment aggregation, array statistics, study inputs and report generation. It is not the interactive scene graph. Browser state may use an in-memory indexed object graph and persist snapshots to Parquet through an export/build step.

Suggested public datasets:

- `objects.parquet`
- `geometries.parquet`
- `terminals.parquet`
- `connectivity.parquet`
- `segments.parquet`
- `materials.parquet`
- `environments.parquet`
- `measurements.parquet`
- `assumptions.parquet`
- `study_runs.parquet`
- `study_results.parquet`
- `warnings.parquet`

GeoJSON exports:

- `site.geojson`
- `arrays.geojson`
- `routes.geojson`
- `electrical_paths.geojson`
- `warnings.geojson`

## 9. Segment derivation

Every conductor path shall be converted into ordered piecewise segments. A segment records length, start and end coordinates, local tangent, polarity, conductor material, CSA, temperature, separation from the return conductor, height above earth, distance to frame, route environment, formation, connector boundary, coil attributes and evidence state.

For segment `i`, resistance is:

`R_i(T_i) = ρ_20 × l_i / A_i × [1 + α(T_i - 20 °C)]`

The complete circuit is:

`R_total = ΣR_positive + ΣR_negative + ΣR_factory_leads + ΣR_connectors + ΣR_terminations + ΣR_series_devices`

Commercial copper mass and physical copper mass shall remain separate:

`m_commercial = A_nominal × L_km × 9.6 kg/(km·mm²)`

`m_physical = A_actual × L_km × ρ_Cu`

with the physical density basis and conductor construction explicitly stated.

## 10. Inductive-loop study scope

B9 shall derive loop geometry from the ordered positive and negative paths. It shall not assume one constant spacing for a whole string.

For paired straight cylindrical conductors with centre spacing `D` and radius `r`, a first-order differential inductance per unit length is:

`L'_diff ≈ (μ0/π) acosh(D/(2r))`

for an appropriate two-wire approximation and stated validity limits. At low frequency, internal inductance may be included. At high frequency it shall be removed or replaced by a frequency-dependent conductor model.

The study shall calculate:

- signed loop area from ordered projected paths;
- absolute local loop-area contribution;
- maximum local positive-negative separation;
- percentage of route tightly paired;
- differential inductance by segment;
- common-mode inductance against frame/earth;
- concentrated coil inductance with explicit diameter, turns, pitch and whether both poles are coiled together;
- mutual coupling where positive and negative conductors share a route;
- SPD lead inductance;
- magnetic stored energy `W_L = 0.5 L I²`;
- interruption estimate `V = L di/dt` only where lumped treatment is valid;
- characteristic impedance and travelling-wave estimate where the event is distributed.

## 11. Module and array capacitance study scope

The model shall never merge differential module capacitance with module-to-frame or module-to-earth common-mode capacitance.

A module shall support a layer-stack representation including cells, encapsulant, front glass, rear glass or backsheet, frame, rails, water film and soil/earth coupling. A simple parallel-plate estimate may be used only as a visible bounding calculation:

`C = ε0 εr A / d`

The dry capacitance remains the floor. Wet-state behaviour is additive and frequency dependent:

`C_total(f) = C_dry(f) + C_film(f, σ, geometry, contamination)`

The water film is not assumed equipotential over the full module at every frequency. A resistive-sheet participation model shall determine effective area as a function of sheet conductivity, contact paths and angular frequency. The study must expose the difference between a local film, a frame-connected film and a continuous film spanning multiple modules.

Capacitance shall be aggregated at the actual electrical monitoring boundary: string, MPPT, inverter input group, common DC link or insulation-monitoring device. Unknown inverter topology shall produce bounding cases rather than a false single answer.

## 12. Distributed network model

For each route class, derive or accept per-unit-length `R'`, `L'`, `C'` and `G'`.

`Z0(f) = sqrt((R' + jωL') / (G' + jωC'))`

`γ(f) = sqrt((R' + jωL')(G' + jωC'))`

`v_p = ω / Im(γ)` where meaningful.

`τ = l / v_p`

The event classifier shall compare rise time with route delay and wavelength. A complete utility string must not be assigned one universal resonance. Segment transitions, branches, module shunts, inverter termination and common-mode earth paths produce multiple modes.

## 13. Study outputs

Each study output shall carry:

- value and unit;
- method;
- equations or solver name;
- input object IDs;
- provenance;
- evidence class;
- uncertainty or range;
- validation status;
- warnings;
- schema and engine version.

Initial studies:

- complete-circuit resistance and voltage drop;
- copper mass on commercial and physical bases;
- cable schedule by polarity and segment class;
- sequential versus leapfrog comparison;
- loop area and differential inductance;
- common-mode path summary;
- dry/wet capacitance bounds;
- capacitance seen by each monitoring boundary;
- propagation delay and distributed-model screening;
- characteristic impedance and travelling-wave bounds;
- cold Voc and system-voltage margin;
- SPD electrical distance and lead-inductance contribution;
- uncertainty and missing-data report.

## 14. Layer and cartridge extension API

User development shall be additive. A cartridge package shall declare:

- package ID and semantic version;
- schema compatibility;
- object templates;
- editable parameters and units;
- geometry generator;
- terminal generator;
- topology constraints;
- validation rules;
- icons and view renderers;
- migrations;
- public licence and attribution.

A study cartridge shall declare inputs, equations or solver, output schema, evidence class and validation tests. A visual layer shall consume canonical objects or study results without rewriting them.

No cartridge may modify core objects silently. Extensions must create explicit derived objects, properties or study results.

## 15. Technician summary requirement

B9 begins with a technician-summary placeholder. The eventual technician view shall answer, without marketing:

- what physical array was modelled;
- how modules were electrically ordered;
- where positive and negative terminals emerge;
- cable lengths by class and polarity;
- module-lead feasibility warnings;
- connector count and compatibility status;
- loop-separation hotspots;
- coils and surplus cable;
- route environments;
- missing measurements;
- resistance, voltage drop and copper mass;
- capacitance and insulation-monitoring boundary;
- distributed-model warning;
- exact inputs requiring site verification.

## 16. Public-data boundary

The repository may use public manufacturer datasheets, public standards commentary, generic dimensions, user-entered measurements and synthetic examples. It shall not publish confidential employer requirements, private drawings, customer cable schedules, as-built photographs, serial-number registers, proprietary plant calibration or conclusions traceable to a protected project.

Project documents may inform the recognition that professional work requires dimensioned plans, elevations, sections, cable schedules, calculations, commissioning records and auditable revision control, but their wording, tables, identities and project values shall not be reproduced.

## 17. Acceptance gates for B9 implementation

B9 shall not be called an engine release until:

1. V6, V7 and V8 remain independently accessible and unmodified.
2. The canonical schema is versioned and validated.
3. At least four mechanical cartridges and four topology cartridges work in plan, side and circuit views.
4. Object IDs remain stable through save/export/import.
5. A 100,000-module synthetic scene can be stored and queried without requiring full-detail rendering.
6. DuckDB can aggregate Parquet cable schedules and study inputs deterministically.
7. GeoJSON exports preserve IDs and coordinate reference metadata.
8. Loop and capacitance studies show assumptions and bounds.
9. Unit tests independently verify geometry, lengths, resistance, loop area and aggregation.
10. No confidential data is present.
