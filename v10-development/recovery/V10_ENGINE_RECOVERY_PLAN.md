# V10 Authoritative Engine Recovery Plan

## Status

Execution plan for recovering the Solar DC topology engine. The browser is not the authority. The recovered and tested computation kernel is the authority. Browser work remains downstream until the kernel, evidence model and report schema are stable.

## Governing build order

Physics → physical objects → terminals and connectivity → ordered electrical topology → computation → evidence → reporting → browser visualisation.

## Phase 0 — Repository reconciliation

Purpose: establish what already exists before rebuilding anything.

Deliverables:

- inventory of Python, V8, V9 and V10 computation paths;
- test inventory and current pass/fail state;
- file-level ownership map for geometry, topology, calculations, reporting and browser rendering;
- identification of duplicated, abandoned and browser-only logic;
- corrected documentation acknowledging the Python engine and all legitimate historical directories.

Exit criterion: every known computation capability has one migration-ledger row and one declared source path.

## Phase 1 — Canonical physical object model

Recover or implement first-class objects for:

- module;
- positive and negative factory flying leads;
- connector and mating pair;
- string;
- string wiring harness branch;
- harness aggregation node;
- harness main conductor;
- field-installed string cable;
- transition conductor;
- combiner or junction object;
- MPPT input;
- internally common DC bus;
- inverter or PCE block;
- cable tray segment;
- duct segment;
- direct-burial segment;
- tracker moving section;
- earth and bonding conductor;
- SPD location;
- protective device;
- measurement and evidence object.

Each object must support, where applicable:

- stable identifier;
- type and subtype;
- terminals;
- ordered geometry;
- dimensions;
- material;
- installation environment;
- manufacturer-declared data;
- user-entered data;
- provenance;
- uncertainty;
- validation state.

Exit criterion: a complete module-to-inverter circuit can be represented without using one assumed total cable length.

## Phase 2 — Canonical topology engine

Recover or implement:

- terminal graph;
- conductor ordering;
- polarity;
- series connectivity;
- parallel aggregation;
- independent MPPT boundaries;
- internally common DC-bus boundaries;
- harness branch and trunk connectivity;
- reverse-current paths;
- protection boundaries;
- earth-reference topology;
- complete circuit traversal in both directions.

Rules:

- never infer internal commoning from input count alone;
- never collapse harnesses into a single length;
- never calculate against browser drawing order unless topology validation has succeeded;
- topology errors must stop dependent calculations.

Exit criterion: deterministic traversal returns the complete positive and negative conductor schedules for every string.

## Phase 3 — Authoritative steady-state kernel

Recover, reconcile and test:

- conductor resistance at reference temperature;
- temperature correction;
- connector and termination resistance;
- string operating current;
- voltage drop by conductor segment;
- power loss by segment and complete circuit;
- current-carrying capacity inputs and derating boundaries;
- maximum string voltage;
- minimum MPPT voltage;
- reverse-current and OCPD logic;
- unequal-string and optimiser exception handling;
- copper versus aluminium conductors;
- complete conductor schedule and material totals.

The Python engine should be treated as the leading recovery candidate because it already contains unit handling and temperature-corrected formulae. JavaScript kernels must be compared against it, not silently treated as co-equal authorities.

Exit criterion: one canonical result schema and one authoritative implementation pass the recovered regression suite.

## Phase 4 — Route and installation physics

Recover or implement route-segment treatment for:

- free air;
- bundled conductors;
- trays;
- covered trays;
- ducts;
- trenches;
- direct burial;
- soil thermal resistivity;
- cable spacing;
- crossings;
- tracker movement;
- bend radius;
- tension and support;
- water exposure;
- UV exposure;
- rodent and mechanical-damage exposure.

Exit criterion: every electrical conductor segment can reference a physical route segment and installation environment.

## Phase 5 — Distributed and transient models

Recover and validate separately from the steady-state kernel:

- loop geometry;
- capacitance;
- inductance;
- characteristic impedance;
- propagation velocity;
- attenuation;
- reflections at discontinuities;
- conductor-size transitions;
- open, capacitive and matched terminations;
- arc interruption and restrike scenarios;
- surge propagation and sharing;
- SPD electrical distance;
- common-mode and earth-reference behaviour.

These models must declare their validity range and assumptions. They must not be represented as standards compliance calculations unless a separate standards cartridge makes that determination.

Exit criterion: every transient result records geometry, termination, frequency range, assumptions and numerical-convergence evidence.

## Phase 6 — Standards and evidence cartridges

Standards are constraints and evidence, not ownership of the engineering model.

Build versioned cartridges for:

- IEC 62548;
- IEC TS 62738;
- IEC 63027;
- IEC 63112;
- IEC 61643-32 where SPD selection is addressed;
- applicable cable and installation standards;
- manufacturer instructions;
- project-specific Employer's Requirements.

Every rule must record:

- source identity and edition;
- clause reference;
- normative strength where known;
- paraphrased engineering meaning;
- required inputs;
- implemented test;
- exception route;
- evidence needed;
- validity boundary.

No standard text, protected figure or table is to be reproduced. Clause references exist for traceability only.

Exit criterion: standards checks can be enabled, disabled and version-selected without changing the physics kernel.

## Phase 7 — Evidence-aware result schema

Every calculated result must carry:

- calculation identifier;
- kernel version;
- input snapshot hash;
- units;
- formula or method identifier;
- source objects;
- assumptions;
- provenance;
- uncertainty;
- standards references where applicable;
- warning and exception state;
- validation state;
- reviewer state.

Exit criterion: no important number can appear in a report without a trace back to its inputs and method.

## Phase 8 — Reporting engine

Produce reproducible reports containing:

- project and design basis;
- topology hierarchy;
- object and conductor schedules;
- route schedule;
- voltage and loss results;
- protection results;
- standards checks;
- assumptions and exceptions;
- uncertainty and validity boundaries;
- evidence register;
- test and validation summary.

Reports are kernel outputs. Browser screenshots are not engineering reports.

Exit criterion: the same input model produces the same machine-readable result and human-readable report independent of browser state.

## Phase 9 — Tests and validation

Immediate test work:

- fix the Python exact-float assertion by using tolerance-based comparison where mathematically appropriate;
- investigate the single terminal-geometry branch failure;
- run and record all current JS and Python tests in CI;
- add known-answer tests for resistance, temperature correction, voltage drop and complete circuit loss;
- add topology fixtures for sequential, leapfrog, harness, independent MPPT and common-bus arrangements;
- add invalid-topology tests;
- add route and transient regression cases;
- retain hand calculations and measurement comparisons as evidence artefacts.

Exit criterion: CI runs every authoritative test path and blocks regressions.

## Phase 10 — Browser rebuild

Only after the authoritative interfaces are stable:

- browser edits canonical physical objects;
- browser visualises validated topology;
- browser calls the computation kernel;
- browser renders evidence-aware results;
- browser cannot contain hidden engineering formulae;
- browser geometry cannot override electrical topology;
- Atlas, Spider and other GlobalGrid2050 tools consume published result interfaces rather than browser internals.

## Immediate execution queue

1. Complete the migration ledger from repository inspection.
2. Correct the reboot documentation to include the Python engine and the three computation paths.
3. Add CI for Python and JavaScript tests.
4. Fix the two known test failures without weakening valid assertions.
5. Define canonical object, topology and result schemas.
6. Select the authoritative steady-state kernel after capability comparison.
7. Recover complete conductor traversal and temperature-corrected loss calculations.
8. Add standards cartridges only after the corresponding physics capability is tested.
9. Build the first reproducible engineering report.
10. Rebuild browser functions last.

## Non-negotiable controls

- No browser-first engineering.
- No invented default presented as a standard requirement.
- No automatic approval of a standards exception.
- No confidential project drawing published as a generic example.
- No copied IEC text, figures or tables.
- No calculation without units.
- No result without provenance.
- No topology-dependent calculation after a topology validation failure.
