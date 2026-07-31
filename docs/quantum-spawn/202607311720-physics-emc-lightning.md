# Quantum Spawn

**Title:** Physics, EMC and Lightning

**File:** `202607311720-physics-emc-lightning.md`

**Timestamp:** 2026-07-31 17:20 (Local)

**Version:** 1.0

**Status:** Canonical

**Authority:** Engineering Design Authority

**Supersedes:** None

**Superseded By:** None

**Dependencies:**
- `202607311609-mission-and-philosophy.md`
- `202607311620-system-architecture.md`
- `202607311640-geometry-authority.md`
- `202607311700-array-engine.md`

**Current Build:** Build 025, preparing Builds 026 and 027

---

# 1. Purpose

This module defines how electrical physics, electromagnetic compatibility, lightning interaction and surge behaviour shall be added to the Solar Electrical Topology Analysis Engine.

The central rule is unchanged: physics is downstream of geometry. No electromagnetic quantity is authoritative unless it is derived from explicit conductor routes, conductor pairing, containment, bonding and installation geometry.

The project does not treat a PV array as a collection of idealised one-dimensional circuits. A utility-scale array is a spatially distributed, floating, capacitively referenced electrical structure. Its behaviour depends on the route of each pole, the relationship between conductors, the geometry of bonded steel, the separation between ducts, the location of surge protective devices and the time scale of the disturbance.

# 2. Physics Handover Boundary

Build 025 must first establish:

- deterministic module positions;
- deterministic string order;
- explicit positive and negative conductor paths;
- inverter position;
- route segment classifications;
- duct, trench and structure relationships;
- route hashes and geometry receipts.

Only then may the physics engine calculate resistance, voltage drop, loop area, inductance, capacitance, surge coupling or fault behaviour.

The physics engine consumes geometry. It never invents geometry.

# 3. DC Steady-State Physics

The first physics layer is conventional DC engineering. For each conductor segment the kernel shall derive length, cross-sectional area, material resistivity and temperature basis. Segment resistance is then aggregated into positive, negative and total loop resistance.

Outputs include:

- conductor resistance;
- string loop resistance;
- voltage drop;
- power loss;
- thermal loss basis;
- conductor mass;
- geometry-derived procurement quantities.

These calculations remain explicit and receipted. Geometric length, installed length and procurement length must never be silently merged.

# 4. Floating Array Behaviour

A modern PV array is often electrically floating with respect to earth except through distributed capacitance, insulation monitoring, surge devices and inverter circuitry.

Double-glass modules, long DC conductors, metallic supports and inverter filters collectively create significant capacitance to earth. Tens of nanofarads per module can aggregate into microfarads across a large block. The array therefore possesses a dynamic reference to earth even when there is no intentional galvanic connection.

The kernel must eventually represent:

- module-to-frame capacitance;
- conductor-to-earth capacitance;
- conductor-to-conductor capacitance;
- array-to-structure capacitance;
- inverter input capacitance;
- SPD and monitoring paths.

This is essential for understanding leakage current, insulation monitoring thresholds, common-mode transients and the behaviour of first and second earth faults.

# 5. First and Second Faults

Like-polarity conductors grouped together can acquire a silent fault. Positive-to-positive contact causes little or no differential current and may not produce a useful insulation-monitoring signature. The system continues operating while fault tolerance has been lost.

The dangerous condition appears when a second fault occurs on the opposite polarity elsewhere. The earth and bonded structure can then complete a current path that was never intended to carry operational fault current.

The topology model must therefore distinguish:

- conductor-to-conductor faults;
- conductor-to-earth faults;
- conductor-to-structure faults;
- first-fault states;
- second-fault states;
- fault paths through bonded steel and soil.

Fault analysis shall be performed on the canonical topology, not inferred from string counts alone.

# 6. Loop Geometry

The most important EMC quantity available directly from Build 025 is enclosed loop area.

Sequential and leapfrog wiring can have similar cable lengths while producing dramatically different loop areas. A far-end return can create a loop spanning most of the table. Leapfrog wiring can reduce that area by keeping the outgoing and returning electrical paths closer together.

The engine shall calculate, per string:

- signed loop area;
- absolute enclosed loop area;
- maximum pole separation;
- mean pole separation;
- parallel-run distance;
- conductor crossings;
- structure-enclosing loops;
- duct-to-duct return geometry.

Cable length and loop area are separate outputs. A shorter route is not automatically electromagnetically better.

# 7. Same-String Pairing

Where positive and negative conductors share containment, pairing must be defined by string identity rather than by conductor count.

A rule stating “six positives and six negatives per duct” is physically incomplete. It can pass visual inspection while placing the positive pole of one string beside the negative pole of another, leaving the actual circuit return in a separate duct.

The correct requirement is that both poles of each string travel together as an identified pair wherever practicable.

The route model must therefore preserve pair identity through every segment, duct and transition.

# 8. Bonded Structures and Cross-Table Routes

A loop that surrounds a torque tube, pile line, cable tray or other bonded metallic structure can couple strongly to lightning current carried by that structure.

Cross-table routing is therefore not merely another length optimisation. It can create a loop around a deliberate strike-current path.

The geometry engine must identify when a positive and negative route enclose bonded steel and expose that relationship to the EMC engine.

Future calculations should include mutual inductance between conductor loops and structural current paths.

# 9. Lightning-Induced Voltage

For an initial screening model, induced voltage may be estimated from loop area, distance from the lightning channel and current steepness. Such a model is useful for ranking layouts and identifying clearly dangerous geometry.

However, long PV runs are electrically long on lightning time scales. Once routes extend into tens of metres, a purely lumped model becomes progressively less accurate. The engine must therefore preserve model validity states.

A receipt should declare whether a result is:

- lumped and valid;
- lumped but approximate;
- distributed model required;
- outside supported model range.

Ordering can remain useful even when absolute magnitude is approximate.

# 10. Distributed Transmission-Line Modelling

Build 027 should introduce a distributed representation for long conductors.

Each route may be divided into segments with per-unit-length resistance, inductance, capacitance and conductance. The resulting model can evaluate travelling waves, reflections, propagation delay, common-mode and differential-mode behaviour.

Required inputs include:

- conductor geometry;
- conductor separation;
- height above ground;
- containment material;
- dielectric environment;
- bonding conditions;
- source and termination impedance;
- SPD locations and dynamic characteristics.

The engine should begin with validated simplified line models before attempting full-wave electromagnetic simulation.

# 11. Screening, Burial and Metallic Containment

Installation method materially changes surge exposure.

The route segment schema already reserves classifications for buried, screened, armoured and bonded metallic containment. These properties must feed both standards validation and physical modelling.

A screen is not merely a Boolean property. Its effectiveness depends on continuity, bonding points, transfer impedance and termination quality. Early builds may use conservative categorical models, but the schema must permit future measured equipment data.

# 12. Surge Protective Devices

SPDs are circuit elements with location-dependent performance. Their effectiveness depends on lead length, loop inductance, earthing and coordination with equipment withstand.

The engine must never treat an SPD as a universal Boolean protection flag.

Future SPD objects should include:

- type and technology;
- maximum continuous operating voltage;
- nominal and maximum discharge current;
- voltage protection level;
- lead geometry;
- earth connection geometry;
- coordination with upstream and downstream devices;
- degradation or end-of-life state where known.

An SPD at the inverter does not automatically protect remote modules from all induced differential voltage.

# 13. Model Confidence and Evidence

EMC and lightning calculations require explicit confidence levels. The kernel shall distinguish measured equipment data, manufacturer data, standards-based assumptions, engineering estimates and unsupported defaults.

Every result must state its model, assumptions and validity envelope.

The purpose is not to manufacture false precision. It is to make hidden assumptions visible and allow the engineer to understand whether a result is suitable for screening, design or certification.

# 14. Build Sequence

Build 027 should proceed in stages:

1. loop geometry and route-pair metrics;
2. steady-state resistance and voltage drop;
3. lumped inductive surge screening;
4. capacitance and common-mode representation;
5. first- and second-fault path modelling;
6. SPD placement and lead-inductance modelling;
7. distributed transmission-line models;
8. validation against measured or published cases.

# 15. Governing Principle

The project’s electromagnetic advantage comes from computing what conventional PV design tools do not preserve: the actual geometry of the complete current loop.

That geometry makes previously invisible failure mechanisms measurable.

The platform should therefore resist any simplification that discards pole identity, route pairing, bonded structures, containment or segment-level installation method. Those details are not rendering metadata. They are the physical inputs from which EMC, lightning and fault behaviour emerge.