# Quantum Spawn

**Title:** Employer Requirements Part 3 — Electrical Engineering and Site Diagnosis

**File:** `202607312340-employer-requirements-part-3-electrical-diagnosis.md`

**Timestamp:** 2026-07-31 23:40 Europe/London

**Version:** 1.0

**Status:** Canonical employer requirement

**Authority:** Product Owner and Engineering Design Authority

**Supersedes:** None

**Superseded By:** None

**Dependencies:**
- `202607311624-array-engine.md`
- `202607311627-physics-emc-lightning.md`
- `202607311628-standards-validation.md`
- `202607312336-employer-requirements-part-1-mission-public-value.md`
- `202607312338-employer-requirements-part-2-architecture-open-standards.md`

**Current Build Relevance:** Build 025.5, Builds 026 and 027, and plant-scale diagnostic development

---

## 1. Purpose

This module defines the employer’s required electrical-engineering functionality and diagnostic depth. The platform shall not stop at drawing strings or calculating a generic voltage drop. It shall progressively become a defensible diagnostic system that connects physical geometry, equipment, topology, environmental state, evidence and calculation validity.

The engine must distinguish what is already authoritative from what remains a future study. No interface, report or development agent may imply that an unimplemented physics or standards layer exists merely because a placeholder field or visual component is present.

## 2. Canonical electrical hierarchy

The diagnostic model shall preserve the hierarchy:

```text
module
→ factory lead
→ connector
→ string
→ field conductor
→ junction or combiner
→ protective device
→ physical inverter input
→ MPPT
→ inverter DC bus where evidenced
→ inverter
→ power block
→ plant
→ fleet
```

Each physical conductor and connection shall retain pole identity, string identity, source and destination terminals, route geometry, product reference, installation class and evidence state.

An MPPT label is not proof that inputs are electrically isolated. Common-bus, reverse-current-blocking and backfeed behaviour shall come from equipment evidence or remain explicitly unresolved.

## 3. Geometry-derived steady-state diagnosis

The first complete diagnostic vertical slice shall support arbitrary sensible string, module, MPPT and inverter-input counts. It shall calculate complete-series-circuit resistance from explicit factory leads, field conductors, connectors, terminations and supported series devices.

Outputs shall include route length, installed length, procurement allowance, conductor resistance, contact resistance, total circuit resistance, voltage drop, percentage voltage drop against a declared operating voltage, I²R loss, temperature basis, uncertainty and evidence status.

Field-installed conductor and factory-fitted conductor must remain separate. Cable-only reductions shall never be described as total copper savings. Geometric, installed and procurement lengths shall not be silently merged.

The engine shall identify worst-performing strings, outlying route lengths, unusual positive-negative imbalance, elevated losses and inputs whose results depend on assumed or unresolved evidence.

## 4. Topology and assignment diagnosis

The engine shall detect duplicate identifiers, duplicate module use, omitted modules, invalid terminal direction, open strings, branches, repeated inverter-input occupation, assignments to nonexistent MPPTs, excess input use and non-deterministic ordering.

Sequential, leapfrog, mirrored and custom arrangements shall use one canonical connection schema. Strategy names may generate candidate topology, but downstream calculations shall consume explicit connections and routes.

The platform shall allow comparison between contracted, proposed, approved and as-built states without overwriting one with another. A proposed optimisation shall have its own receipt and consequence summary.

## 5. Product and evidence diagnosis

Modules, conductors, connectors, inverters, protective devices and SPDs shall be represented by versioned equipment profiles rather than hard-coded constants.

Resistance evidence shall distinguish measured, manufacturer-declared, standard-maximum, ideal-bulk estimate, assumed and unresolved bases. Source qualification shall remain separate from calculation arithmetic. A candidate or rejected source must remain visible wherever its value contributes to a result.

The next evidence domains shall include connector resistance, module terminal coordinates, factory-lead length, inverter input topology, maximum backfeed current, module maximum overcurrent protection rating, impulse withstand, SPD characteristics and insulation-monitoring limits.

## 6. Standards diagnostic programme

Build 026 shall add versioned rule schemas, validation states and deterministic rule receipts. Initial priorities are string maximum current, `K_I`, `K_Corr`, backfeed evidence, overcurrent-protection requirement, fuse intervals, grouped-device inequalities, voltage scope and SPD route-length checks.

Supported rule outcomes shall include PASS, PASS_WITH_WARNINGS, FAIL, INCOMPLETE_EVIDENCE, OUTSIDE_SCOPE, ENGINEERING_REVIEW_REQUIRED and CLIENT_APPROVAL_REQUIRED.

Standards shall validate the model rather than redesign it. Conflicts between editions or authorities shall be exposed. Missing manufacturer data shall not become zero unless evidence supports zero or the assumption is visibly declared.

The platform shall not issue a general compliance certificate. It shall produce traceable diagnostics suitable for competent-person review.

## 7. Environmental and installation diagnosis

Every route segment shall eventually carry an installation class, including under-module, open air, metallic tray, insulating tray, conduit, duct, direct buried, wet trench, floodable transition and enclosure entry.

Environmental state affects temperature, resistance, capacitance, insulation resistance, corrosion, mechanical exposure and maintenance risk. Early categorical models may be conservative, but the schema must permit measured and project-specific inputs.

Routes through separate ducts, around bonded steel, across tables or through floodable areas shall remain explicit diagnostic facts rather than drawing decoration.

## 8. EMC, lightning and distributed physics

Build 027 shall remain downstream of evidenced spatial geometry. It shall distinguish signed loop area, absolute winding area, oriented area vector, field projection, magnetic flux and induced voltage.

The engine shall preserve same-string pole pairing, local separation, crossings, bonded structures, SPD lead geometry and propagation delay. It shall classify whether an event may be treated as lumped, approximate, distributed or unsupported.

Future capabilities include differential and common-mode inductance, conductor-to-conductor and conductor-to-earth capacitance, insulation-monitoring boundaries, first and second faults, surge screening, SPD coordination, travelling waves and reflections.

A single generic lightning multiplier applied to one loop-area number is prohibited as an authoritative model.

## 9. Plant and fleet scale

A site above 30 kWp shall be diagnosable as one project containing one or more array sections and inverters. Larger plants shall aggregate validated children without destroying string-level traceability.

Performance and storage methods may use hash deduplication, columnar tables, lazy loading and spatial indexes, but the underlying engineering object semantics shall remain identical.

Reference performance fixtures shall include approximately 30 kWp, 1 MWp, 100 MWp and 1 GWp systems. The platform shall demonstrate that these sizes use one engineering algorithm and differ only in composition and computational strategy.

## 10. Required diagnostic answer

Every supported finding shall communicate:

```text
condition
location
electrical consequence
evidence status
calculation or rule basis
uncertainty
required next action
affected object and receipt identifiers
```

A user shall be able to move from plant summary to inverter, string, segment, connector or evidence source without losing context.

## 11. Engineering success

This requirement is satisfied when the platform can reconstruct and diagnose a real installation above 30 kWp, reproduce complete steady-state results, expose unsupported evidence, identify topology and assignment defects, issue standards-ready diagnostic dependencies and export a package that another engineer can independently verify.

The governing electrical principle is:

**Model the complete physical current path and its evidence first; allow every supported electrical conclusion to emerge from that explicit reality.**
