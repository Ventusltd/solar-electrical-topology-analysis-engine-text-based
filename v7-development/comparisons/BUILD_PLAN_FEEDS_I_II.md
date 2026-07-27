# V7 electromagnetic build plan — FEED I foundation and FEED II extension

## Build objective

Create a new, independent V7 electromagnetic workbench that converts physical PV string topology into frequency-aware differential-mode and common-mode models while preserving the working root engine and the earlier V7 page as comparison references.

## Repository safety architecture

- Stable working application: `/`
- Previous V7 comparison reference: `/v7-development/`
- New FEED I executable build: `/v7-development/feed-i/`
- Comparison and governance files: `/v7-development/comparisons/`
- Recovery record: `/restore_points/2026-07-27-pre-feed-i-electromagnetic-build/`

No root application file is modified by this build.

## Phase 0 — evidence and dimensional discipline

Create a parameter registry in which every value has:

- name;
- numerical value;
- unit;
- physical mode: differential, common mode, thermal, geometric or environmental;
- evidence status;
- source note;
- uncertainty or range;
- frequency basis where relevant;
- validation requirement.

Allowed evidence states:

- `MEASURED`
- `OEM_DECLARED`
- `STANDARD_REQUIRED`
- `LITERATURE_MODEL`
- `FIRST_PRINCIPLES_DERIVED`
- `FINITE_ELEMENT_REQUIRED`
- `ASSUMED`
- `UNKNOWN`

Acceptance test: a quantity with incompatible dimensions cannot be multiplied, added or exported without an explicit conversion.

## Phase 1 — geometry and topology

Represent each string as an ordered segment chain. Preserve the proven physical module arrangement. Add route generators without changing the module field:

- sequential/far return;
- leapfrog/both terminals near;
- mirrored balanced return;
- custom route;
- single-pole coil;
- paired/bifilar coil;
- structure drop;
- tray, conduit, duct, trench and free-air segments.

Acceptance tests:

- topology changes routes but never rearranges modules;
- positive and negative conductor paths are separately enumerable;
- loop area is derived from coordinates;
- user-entered route length cannot replace generated geometry.

## Phase 2 — differential-mode solver

Implement closed-form two-wire parameters for long straight paired sections:

- conductor diameter derived from CSA;
- external inductance using the round-conductor `acosh` geometry;
- internal inductance included at low frequency and removed at high frequency;
- differential capacitance from conductor geometry and dielectric state;
- propagation velocity and surge impedance;
- magnetic and electric stored energy.

Irregular coils and transitions are represented as discrete objects and marked for PEEC or measurement validation.

Acceptance tests:

- cable outside diameter never substitutes for conductor diameter in the inductance geometry term;
- low-frequency and high-frequency inductance differ only by the internal contribution unless another frequency model is selected;
- a single-pole coil and a bifilar coil produce different differential and common-mode outcomes.

## Phase 3 — event classifier

For every event, calculate one-way and round-trip propagation delay and compare with rise time.

Initial configurable classification:

- `LUMPED`: rise time greater than ten times one-way delay;
- `TRANSITIONAL`: rise time between two and ten times one-way delay;
- `DISTRIBUTED`: rise time no greater than two times one-way delay.

Events include:

- steady DC;
- inverter switching edge;
- lightning surge front;
- connector opening;
- arc initiation/restrike;
- diagnostic pulse.

Acceptance test: faster events can never be classified as more lumped solely because their rise time decreases.

## Phase 4 — common-mode and earth-reference network

Create separate objects for:

- positive conductor to frame/earth;
- negative conductor to frame/earth;
- cell circuit to frame;
- frame to rail;
- rail to pile;
- pile to lossy soil;
- inverter common-mode termination;
- high-ohmic functional earthing or PID mitigation;
- insulation monitoring device.

Initial earth-return equations remain bounded to their stated frequency range. Carson/Pollaczek-style approximations are not silently extended into the MHz region.

Acceptance test: no differential inductance or differential capacitance is substituted for a common-mode quantity.

## Phase 5 — capacitance and environmental model

Implement unit-safe aggregation:

- module;
- string;
- MPPT boundary;
- inverter boundary;
- plant inventory.

The initial build supports evidence-labelled placeholder or literature ranges but must not claim a measured glass-glass bifacial value.

Environmental states:

- dry;
- clean rain;
- condensation/dew;
- brackish contamination;
- salt film;
- custom conductivity.

Governing rule:

`C_total(f) = C_dry(f) + C_film(f, conductivity)`

The film model remains disabled or explicitly marked research-only until an accepted equation, finite-element result or measurement dataset is committed.

Acceptance tests:

- dry capacitance remains as the floor under every wet condition;
- conductivity increase cannot reduce participation in the same RC-sheet model;
- DC capacitance cannot be inserted into a kHz resonance calculation without frequency-consistent iteration.

## Phase 6 — module frequency-response object

Add a frequency-band module model informed by the research feed:

- low-frequency operating-point model;
- `Rs–Rp–Cp` arc-detection band model;
- cell and interconnect series inductance;
- bypass-diode parasitics;
- cabling-dominated distributed region;
- explicit distinction between internal differential capacitance and common-mode cell-to-earth capacitance.

Acceptance test: the tool does not claim that the complete module filters 1 Hz–100 kHz arc signatures unless a selected measured model says so.

## Phase 7 — standards and evidence map

Each technical statement is classified as:

- normative requirement;
- standards-guided calculation;
- application guidance;
- first-principles engineering;
- research hypothesis;
- measurement requirement.

The build must not present:

- 0.5 m² as a PV-standard limit;
- 1.10 m module lead length as a normative requirement;
- a fixed SPD distance without the applicable standard context;
- an arc-fault mandate where the governing installation code does not impose one.

## Phase 8 — validation programme

Prepare hooks and records for:

- impedance spectroscopy;
- controlled wetting by known conductivity;
- full-string inverter-terminal impedance sweep;
- TDR/SSTDR;
- residual-current logging versus weather;
- IMD response-time testing with realistic capacitance;
- side-by-side sequential/leapfrog induced-voltage testing;
- PEEC reference geometry;
- structure/pile earth-impedance measurement.

## Phase 9 — export and digital-twin identity

Export every object with stable identifiers:

- module;
- junction box;
- module lead;
- connector;
- segment;
- coil;
- string;
- MPPT;
- inverter input;
- frame/rail/pile node;
- SPD;
- IMD.

The browser view, calculation result and JSON export must derive from the same object graph.

## Immediate launch increment

The first executable increment will provide:

1. evidence-status inputs;
2. unit-safe capacitance aggregation;
3. two-wire differential parameters;
4. low/high-frequency inductance split;
5. event rise-time classifier;
6. explicit unresolved common-mode and water-film gates;
7. FEED I/FEED II comparison panel.

It will not yet claim validated wet-film capacitance, full PEEC, full inverter impedance, standards compliance or site-specific design approval.
