# Quantum Spawn

**Title:** Standards and Validation

**File:** `202607311740-standards-validation.md`

**Timestamp:** 2026-07-31 17:40 (Local)

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
- `202607311720-physics-emc-lightning.md`

**Current Build:** Build 025, preparing Build 026

---

# 1. Purpose

This module defines the standards-validation philosophy and the first rules to be encoded in the Solar Electrical Topology Analysis Engine.

The kernel models physical reality first. Standards are applied afterwards as versioned validation layers. A standard may constrain a design, require evidence or declare a condition unacceptable, but it must never silently generate geometry or alter the contracted design.

The validation engine shall expose findings, quantify consequences and preserve evidence. Major design changes remain subject to engineer, client and site approval.

# 2. Standards Are Versioned Authorities

A clause is not meaningful without its document, edition and amendment state.

Each encoded rule must therefore identify:

- standard title;
- publication identifier;
- edition;
- amendment or consolidated edition;
- clause or annex;
- rule identifier;
- rule status;
- source provenance.

For example, IEC 62548-1:2023 and IEC TS 62738:2018 must not be blended into one anonymous “IEC rule set.” The latter normatively references an older edition and contains requirements that may not align with the newer array standard.

Where two authorities disagree, the receipt shall show the conflict rather than choosing silently.

# 3. Validation States

A binary pass or fail is insufficient.

The validation engine should support at least:

- PASS;
- PASS_WITH_WARNINGS;
- FAIL;
- INCOMPLETE_EVIDENCE;
- OUTSIDE_SCOPE;
- ENGINEERING_REVIEW_REQUIRED;
- CLIENT_APPROVAL_REQUIRED.

Missing manufacturer backfeed data, for example, is not automatically a fail and must not become an assumed clean pass. It is incomplete evidence.

A design above the supported voltage scope may be technically possible but remains outside the authority of a specific standard.

# 4. IEC 62548-1 Overcurrent Model

The current array-validation baseline is IEC 62548-1:2023, with amendment state recorded where applicable.

The string overcurrent trigger is based on the sum of string fault current and total external backfeed compared with the module maximum overcurrent protection rating.

The canonical variables are:

- `I_F_STRING` — fault current contributed by other paralleled strings;
- `I_BF_PCE` — backfeed contribution from power conversion equipment;
- `I_BF_EXT_BAT` — contribution from an external DC-connected battery;
- `I_BF_TOTAL` — total backfeed from outside the array;
- `I_MOD_MAX_OCPR` — module maximum overcurrent protection rating.

The validation test is:

`I_F_STRING + I_BF_TOTAL > I_MOD_MAX_OCPR`

The engine must treat PCE and battery backfeed as explicit inputs with provenance. Zero is allowed only when supported by manufacturer evidence or shown as a visible engineering assumption.

# 5. String Maximum Current

The design current is not simply the module short-circuit current at standard test conditions.

The canonical relationship is:

`I_STRING_MAX = K_I × I_SC_MOD`

with:

`K_I = 1.25 × K_Corr`

The receipt must show each factor independently. Hidden multiplication factors are unacceptable because they prevent audit and make standards updates difficult.

# 6. K_Corr Provenance

`K_Corr` is a first-class engineering value.

For an ordinary monofacial, optimally oriented array within the covered environmental envelope, a value of 1.0 may be valid. The basis must still be recorded.

For non-optimally oriented monofacial arrays, the geometry engine can support the prescribed geometric relationship using the minimum annual angle between the sun beam and array normal.

For bifacial arrays, where rear irradiance can exceed the relevant threshold, a project-specific simulation value is required. The engine must not silently default a modern bifacial utility array to 1.0.

Required provenance fields should include:

- method;
- simulation tool;
- model version;
- weather dataset;
- albedo;
- rear irradiance basis;
- bifaciality;
- engineer or source;
- supporting document reference.

If a required simulation is absent, the result is incomplete evidence.

# 7. Fault-Current Family

Validation must not stop at a single string inequality.

The engine should compute and receipt the fault-current family at:

- string level;
- grouped-string level;
- sub-array level;
- array level;
- inverter input level;
- external battery contribution where applicable.

The topology determines which strings are actually paralleled. Strings assigned to separate isolated MPPT channels must not be treated as one parallel group unless the equipment profile proves an internal shared path.

Equipment topology therefore matters as much as the labelled MPPT count.

# 8. Individual and Grouped Protection

The kernel must distinguish individual string fusing from multiple strings placed beneath one shared overcurrent device.

An individual string fuse must carry normal design current while remaining at or below the module protection rating and satisfying equipment constraints.

A grouped device must also account for healthy strings inside the protected group feeding a faulted member. The applicable lower and upper inequalities must be evaluated explicitly.

For crystalline modules, grouped protection often has no valid solution at higher group counts. The engine should not hard-code an arbitrary string-count ban, but it should calculate the permitted interval and fail when the interval is empty.

Module technology must be a declared equipment property. Thin-film and crystalline devices cannot be treated identically.

# 9. Restricted-Access Engineering Relaxations

IEC TS 62738 contains power-plant provisions and engineering-analysis pathways that must be treated as conditional evidence routes, not universal exceptions.

Where a design relies on a restricted-access relaxation, the receipt should require evidence such as:

- documented failure-mode analysis;
- identified backfeed magnitudes and durations;
- module testing against those conditions;
- explicit module-manufacturer approval;
- warranty implications;
- responsible engineer acceptance.

Absence of one required condition means the relaxation is not demonstrated.

# 10. Wiring Loops and Conductor Pairing

The standards layer shall consume the loop geometry produced by the array engine.

It should verify that same-string positive and negative conductors are routed to minimise loop area and that associated bonding conductors are considered where required.

A compliance receipt should report physical metrics rather than merely saying “leapfrog selected.” The implementation may still be poor even when the strategy label sounds correct.

Relevant evidence includes:

- absolute loop area;
- maximum pole separation;
- paired-route percentage;
- unpaired segments;
- loops enclosing bonded structures;
- cross-table transitions.

# 11. Long DC Routes and Installation Reinforcement

Long DC routes require explicit installation classification.

The route model must distinguish exposed unshielded cable from:

- burial;
- bonded metallic conduit;
- bonded trunking;
- armoured cable;
- screened cable with documented bonding;
- SPD-protected routes.

The validation engine should assess the applicable long-route reinforcement requirement and preserve the selected compliance route.

A screen or metallic enclosure cannot be credited merely because it exists. Bonding and continuity must be evidenced.

# 12. SPD Critical-Length Check

The SPD trigger based on route length and ground flash density is one of the highest-value geometry-derived rules.

The engine shall calculate the critical length for the applicable installation type and compare it with the maximum counted route from PCE to module connection point.

The counted route must exclude only those segments that qualify under the standard, such as properly buried or earthed-screened sections.

Each exclusion must be itemised. The software shall not subtract an entire route merely because one part is screened.

Required inputs include:

- ground flash density `N_g`;
- source and provenance of `N_g`;
- installation classification;
- route segments;
- qualifying exclusions;
- SPD election and location.

Even when the designer elects to install SPDs regardless, the normative calculation should still appear on the receipt.

# 13. Voltage Scope

IEC 62548-1 defines the low-voltage DC boundary at 1500 V. A design above this value must not receive a clean certification under that standard.

The appropriate state is outside scope, accompanied by the evidence path being used instead.

The engine must avoid casually relabelling 2 kV DC as medium voltage. The standards landscape contains a gap rather than a universally accepted replacement regime.

Equipment certification, cable ratings, connector ratings, insulation coordination, national law and insurer acceptance must be evaluated separately.

Three-kilovolt commercial PV arrays are not part of the current baseline.

# 14. Equipment Profiles and Ambient Derating

Inverter, module, fuse, connector, cable and SPD ratings belong in versioned equipment profiles.

Inverter power must not be represented by one ambient-independent number. Apparent and active power limits may derate significantly in hot climates.

Profiles should include rating curves or discrete manufacturer data where available. Missing curves should generate visible assumptions rather than silent extrapolation.

The same principle applies to fuse enclosure-temperature derating, cable current-carrying capacity and connector temperature limits.

# 15. Standards Do Not Redesign the Project

The kernel may identify that another route, inverter position, fuse arrangement or duct allocation performs better.

It may quantify the opportunity and produce a recommendation.

It must not assume the contracted design has changed.

The project state should distinguish:

- modelled contracted design;
- proposed optimisation;
- engineer-reviewed option;
- client-approved change;
- site-approved implementation;
- as-built evidence.

This separation protects contractual relevance and auditability.

# 16. Validation Receipt Structure

Every rule result should include:

- rule identity;
- standard and edition;
- clause;
- input values and units;
- input provenance;
- formula or algorithm version;
- computed threshold;
- computed result;
- status;
- warnings;
- missing evidence;
- recommended action;
- geometry, topology and calculation hashes.

The purpose is not merely to declare compliance. It is to show why the declaration is justified.

# 17. Build 026 Priorities

Build 026 should implement, in order:

1. standards-rule and provenance schemas;
2. validation-state model;
3. `K_I` and `K_Corr` derivation receipt;
4. string and external backfeed inputs;
5. string overcurrent requirement;
6. individual fuse sizing;
7. grouped-device inequality;
8. loop-geometry compliance evidence;
9. SPD `L` versus `L_crit` check;
10. voltage-scope gate;
11. edition-conflict reporting;
12. deterministic validation receipt.

# 18. Governing Principle

Standards validation is evidence applied to a physical model.

It is not a collection of disconnected spreadsheet checks and it is not permission for the software to invent missing facts.

Where data is missing, the kernel says so. Where standards disagree, the kernel shows the disagreement. Where an optimisation requires approval, the kernel preserves the contracted design and presents the alternative separately.

This approach turns compliance from a final checkbox into a traceable engineering discipline grounded in geometry, topology, equipment evidence and versioned authority.