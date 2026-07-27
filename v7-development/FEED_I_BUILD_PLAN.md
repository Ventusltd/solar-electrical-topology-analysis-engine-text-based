# FEED I Build Plan — Electromagnetic Foundations

## Purpose

FEED I converts the current V7 research direction into a controlled implementation programme. It does not replace the working root engine and it does not yet replace the present V7 page. It creates a new isolated build under `v7-development/feed-i/` so that electrical theory, units, epistemic status and validation gates can be tested before integration into the graphical workbench.

## Governing principles

1. Geometry remains the source of electrical parameters.
2. Differential mode and common mode remain separate first-class models.
3. Frequency, environment and termination state must travel with every result.
4. Every value carries an epistemic status.
5. No scalar result may lose its unit during aggregation.
6. No standards compliance verdict is produced from research-mode calculations.
7. The working root engine remains unchanged.

## Corrections incorporated before coding

### Capacitance aggregation

A per-kilowatt capacitance must aggregate with dimensional units. For example:

`250 kW × 60–110 nF/kW = 15–27.5 µF`

not 15–30 nF. The build shall contain explicit unit conversions and self-checks to prevent this class of error.

### RC-sheet participation direction

For an edge-bonded distributed RC sheet, the characteristic participation distance is treated as increasing with conductivity and decreasing with frequency. The implementation shall use a declared model form equivalent in direction to:

`participation length ∝ sqrt(conductivity / frequency)`

The proportionality constant and exact sheet formulation remain research inputs until validated.

### Lumped versus distributed language

The engine shall not describe sub-microsecond behaviour as lumped. The initial configurable classification is:

- rise time greater than 10 times one-way delay: lumped normally acceptable;
- rise time between 2 and 10 times one-way delay: transitional;
- rise time less than or equal to 2 times one-way delay: distributed treatment required.

These are screening thresholds, not universal physical boundaries.

### Multi-MPPT common-mode coupling

The engine shall not apply a binary assumption that every string is simply paralleled at all frequencies. It shall represent coupling state as one of:

- isolated or independently bounded;
- common DC-link, frequency-dependent coupling;
- directly paralleled;
- unknown, requiring bounding cases.

## Epistemic status model

Every input and result shall carry one of:

- `MEASURED`
- `OEM_DECLARED`
- `STANDARD_REQUIRED`
- `LITERATURE_MODEL`
- `FIRST_PRINCIPLES_DERIVED`
- `FINITE_ELEMENT_REQUIRED`
- `ASSUMED`
- `UNKNOWN`

A result inherits the weakest load-bearing status unless an explicit validation record upgrades it.

## Phase sequence

### Phase 0 — isolated executable foundation

Create `v7-development/feed-i/` containing:

- an independent browser harness;
- a unit-safe calculation library;
- epistemic-status propagation;
- two-wire differential parameter calculations;
- event-model classification;
- capacitance aggregation checks;
- water-film participation scaling as an explicitly unvalidated research model;
- visible self-tests.

### Phase 1 — capacitance network

Add separate quantities for:

- dry module-to-frame floor;
- frequency-dependent film contribution;
- total module capacitance as dry plus film;
- string, MPPT and inverter aggregation;
- positive-to-earth and negative-to-earth branches;
- inverter participation boundary.

No glass-glass value shall be treated as measured unless a measurement record is attached.

### Phase 2 — inductance hierarchy

Implement:

- straight paired-route closed forms;
- low-frequency internal inductance;
- high-frequency removal of internal inductance;
- discrete single-pole coil objects;
- bifilar coil classification;
- PEEC-required flags for irregular three-dimensional transitions.

### Phase 3 — inverter termination and common mode

Represent:

- MPPT front-end topology;
- common DC-link coupling;
- EMI capacitors and common-mode chokes where known;
- SPD, IMD and high-ohmic earthing branches;
- unknown OEM impedance as a bounded or measured requirement.

### Phase 4 — validation programme

Add records for:

- impedance spectroscopy;
- controlled wetting by conductivity class;
- TDR or SSTDR;
- residual-current logging;
- IMD response-time testing;
- PEEC or finite-element reference models.

### Phase 5 — graphical integration

Only after the isolated model passes self-checks shall selected FEED I capabilities be integrated into the main V7 graphical workbench. The working root engine remains the regression reference.

## Acceptance gates

1. All capacitance aggregation examples pass dimensional self-tests.
2. Conductor diameter, not cable outside diameter, drives the two-wire geometry term.
3. Differential and common-mode outputs cannot overwrite one another.
4. Dry capacitance remains present when film capacitance is added.
5. Event classification responds correctly to rise time and propagation delay.
6. The RC-sheet model reports itself as unvalidated.
7. Unknown inverter topology produces bounding cases, not a silent assumption.
8. Every exported value includes unit, status, method and dependencies.
9. No root application file changes during FEED I development.

## Deferred pending FEED II

FEED II may refine or replace:

- water-film equations;
- inverter topology assumptions;
- common-mode earth-return method;
- validation priorities;
- standards mappings;
- device-selection logic.

Therefore Phase 0 is deliberately modular and does not freeze those unresolved choices.
