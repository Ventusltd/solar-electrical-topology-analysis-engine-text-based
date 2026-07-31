# Quantum Spawn

**Title:** Physics, EMC and Lightning

**File:** `202607311627-physics-emc-lightning.md`

**Timestamp:** 2026-07-31 16:27 (Device local time)

**Version:** 1.0

**Status:** Canonical

**Authority:** Engineering Design Authority

**Supersedes:** None

**Superseded By:** None

**Dependencies:**
- `202607311609-mission-and-philosophy.md`
- `202607311615-system-architecture.md`
- `202607311619-geometry-authority.md`
- `202607311624-array-engine.md`

**Current Build:** Build 025, preparing Builds 026 and 027

---

# 1. Purpose

This module defines how electrical physics, electromagnetic compatibility, lightning interaction and surge behaviour are added to the Solar Electrical Topology Analysis Engine.

The central rule remains: physics is downstream of geometry. No electromagnetic quantity is authoritative unless it is derived from explicit conductor routes, conductor pairing, containment, bonding and installation geometry.

The project does not treat a PV array as a set of idealised one-dimensional circuits. A utility-scale array is a spatially distributed, floating, capacitively referenced structure whose behaviour depends on the route of each pole, the relationship between conductors, bonded steel, duct separation, SPD location and disturbance time scale.

# 2. Physics Handover Boundary

Build 025 must first establish deterministic module positions, string order, explicit positive and negative paths, inverter position, segment classifications, duct and structure relationships, route hashes and geometry receipts.

Only then may the physics engine calculate resistance, voltage drop, loop area, inductance, capacitance, surge coupling or fault behaviour. The physics engine consumes geometry and never invents it.

# 3. DC Steady-State Physics

For each conductor segment the kernel derives length, cross-sectional area, material resistivity and temperature basis. Segment resistance is aggregated into positive, negative and total loop resistance.

Outputs include conductor resistance, string loop resistance, voltage drop, power loss, thermal basis, conductor mass and geometry-derived procurement quantities.

Geometric length, installed length and procurement length must never be silently merged.

# 4. Floating Array Behaviour

Modern PV arrays are often electrically floating with respect to earth except through distributed capacitance, insulation monitoring, surge devices and inverter circuitry.

Double-glass modules, long DC conductors, metallic supports and inverter filters collectively create significant capacitance to earth. Tens of nanofarads per module can aggregate into microfarads across a large block.

The kernel must eventually represent module-to-frame, conductor-to-earth, conductor-to-conductor, array-to-structure and inverter-input capacitance, plus SPD and monitoring paths.

This is essential for understanding leakage current, common-mode transients and first- and second-earth-fault behaviour.

# 5. First and Second Faults

Like-polarity conductors grouped together can acquire a silent fault. Positive-to-positive contact may produce little differential current and no useful insulation-monitoring signature. The system continues operating while fault tolerance has been lost.

The dangerous condition appears when a second fault occurs on the opposite polarity elsewhere. Earth and bonded structure can then complete a current path never intended to carry operational fault current.

The topology model must distinguish conductor-to-conductor, conductor-to-earth and conductor-to-structure faults, first-fault and second-fault states, and paths through bonded steel and soil.

# 6. Loop Geometry

The most important EMC quantity available directly from Build 025 is enclosed loop area.

Sequential and leapfrog wiring can have similar cable lengths while producing dramatically different loop areas. A far-end return can span most of the table. Leapfrog can reduce that area by keeping outgoing and returning paths closer.

Per-string outputs include signed and absolute loop area, maximum and mean pole separation, parallel-run distance, crossings, structure-enclosing loops and duct-to-duct return geometry.

Cable length and loop area are separate outputs. A shorter route is not automatically electromagnetically better.

# 7. Same-String Pairing

Where positive and negative conductors share containment, pairing must be defined by string identity rather than conductor count.

A rule stating six positives and six negatives per duct is incomplete. It can pass inspection while placing the actual return in a separate duct.

The correct requirement is that both poles of each string travel together as an identified pair wherever practicable. The route model preserves pair identity through every segment and transition.

# 8. Bonded Structures and Cross-Table Routes

A loop surrounding a torque tube, pile line, cable tray or bonded metallic structure can couple strongly to lightning current carried by that structure.

Cross-table routing is therefore not merely another length optimisation. It can create a loop around a deliberate strike-current path.

The geometry engine must identify when routes enclose bonded steel and expose that relationship to the EMC engine. Future calculations should include mutual inductance between conductor loops and structural current paths.

# 9. Lightning-Induced Voltage

An initial screening model may estimate induced voltage from loop area, distance from a lightning channel and current steepness. This is useful for ranking layouts and identifying dangerous geometry.

However, long PV runs are electrically long on lightning time scales. Once routes extend into tens of metres, a lumped model becomes progressively less accurate.

Receipts should state whether a result is lumped and valid, lumped but approximate, requires a distributed model or lies outside the supported range.

# 10. Distributed Transmission-Line Modelling

Build 027 should introduce a distributed representation for long conductors. Each route may be divided into segments with per-unit-length resistance, inductance, capacitance and conductance.

The model can evaluate travelling waves, reflections, delay, common-mode and differential-mode behaviour.

Inputs include conductor geometry, separation, height, containment, dielectric environment, bonding, source and termination impedance, and SPD locations and dynamic characteristics.

The engine should begin with validated simplified line models before attempting full-wave electromagnetic simulation.

# 11. Screening, Burial and Metallic Containment

Installation method materially changes surge exposure. Segment classifications for buried, screened, armoured and bonded metallic containment feed both standards validation and physical modelling.

A screen is not merely a Boolean property. Its effectiveness depends on continuity, bonding points, transfer impedance and termination quality. Early builds may use conservative categorical models, but the schema must permit measured equipment data later.

# 12. Surge Protective Devices

SPDs are circuit elements with location-dependent performance. Effectiveness depends on lead length, loop inductance, earthing and coordination with equipment withstand.

The engine must never treat an SPD as a universal protection flag.

Future SPD objects include technology, maximum continuous voltage, nominal and maximum discharge current, voltage protection level, lead geometry, earth geometry, coordination and degradation state.

An SPD at the inverter does not automatically protect remote modules from all induced differential voltage.

# 13. Model Confidence and Evidence

EMC and lightning calculations require explicit confidence levels. The kernel distinguishes measured data, manufacturer data, standards-based assumptions, engineering estimates and unsupported defaults.

Every result states model, assumptions and validity envelope. The purpose is not false precision but visible assumptions and appropriate use for screening, design or certification.

# 14. Build Sequence

Build 027 should proceed through loop geometry and route-pair metrics, steady-state resistance and voltage drop, lumped surge screening, capacitance and common-mode representation, first- and second-fault modelling, SPD lead-inductance modelling, distributed line models and validation against measured or published cases.

# 15. Governing Principle

The project’s electromagnetic advantage comes from computing what conventional PV tools discard: the actual geometry of the complete current loop.

The platform must resist any simplification that discards pole identity, route pairing, bonded structures, containment or segment-level installation method. These are physical inputs, not rendering metadata.