# Quantum Spawn

**Title:** Standards and Validation

**File:** `202607311628-standards-validation.md`

**Timestamp:** 2026-07-31 16:28 (Device local time)

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
- `202607311627-physics-emc-lightning.md`

**Current Build:** Build 025, preparing Build 026

---

# 1. Purpose

This module defines the standards-validation philosophy and the first rules to be encoded in the Solar Electrical Topology Analysis Engine.

The kernel models physical reality first. Standards are applied afterwards as versioned validation layers. A standard may constrain a design, require evidence or declare a condition unacceptable, but it must never silently generate geometry or alter the contracted design.

The validation engine exposes findings, quantifies consequences and preserves evidence. Major design changes remain subject to engineer, client and site approval.

# 2. Standards Are Versioned Authorities

A clause is not meaningful without its document, edition and amendment state. Each encoded rule identifies standard title, publication identifier, edition, amendment, clause or annex, rule identifier, rule status and source provenance.

IEC 62548-1:2023 and IEC TS 62738:2018 must not be blended into one anonymous rule set. Where authorities disagree, the receipt shows the conflict rather than choosing silently.

# 3. Validation States

A binary pass or fail is insufficient. Supported states include PASS, PASS_WITH_WARNINGS, FAIL, INCOMPLETE_EVIDENCE, OUTSIDE_SCOPE, ENGINEERING_REVIEW_REQUIRED and CLIENT_APPROVAL_REQUIRED.

Missing manufacturer backfeed data is not automatically a failure and must not become an assumed clean pass. It is incomplete evidence. A design above the supported voltage scope may be technically possible but remains outside the authority of a specific standard.

# 4. IEC 62548-1 Overcurrent Model

The current baseline is IEC 62548-1:2023 with amendment state recorded where applicable.

The string overcurrent trigger is based on the sum of string fault current and total external backfeed compared with the module maximum overcurrent protection rating:

`I_F_STRING + I_BF_TOTAL > I_MOD_MAX_OCPR`

The canonical variables include fault current from other paralleled strings, PCE backfeed, external battery backfeed, total backfeed and module maximum overcurrent protection rating.

PCE and battery backfeed are explicit inputs with provenance. Zero is allowed only when supported by manufacturer evidence or shown as a visible engineering assumption.

# 5. String Maximum Current

The design current is not simply module Isc at standard test conditions:

`I_STRING_MAX = K_I × I_SC_MOD`

with:

`K_I = 1.25 × K_Corr`

The receipt shows each factor independently. Hidden multipliers prevent audit and make standards updates difficult.

# 6. K_Corr Provenance

`K_Corr` is a first-class engineering value. For ordinary monofacial, optimally oriented arrays within the covered envelope, 1.0 may be valid but the basis must be recorded.

For non-optimally oriented monofacial arrays, the geometry engine can support the prescribed relationship using the minimum annual angle between sun beam and array normal.

For bifacial arrays, where rear irradiance can exceed the relevant threshold, a project-specific simulation value is required. The engine must not silently default a modern bifacial utility array to 1.0.

Required provenance includes method, simulation tool, model version, weather dataset, albedo, rear-irradiance basis, bifaciality, responsible engineer and supporting-document reference.

# 7. Fault-Current Family

Validation must compute the fault-current family at string, grouped-string, sub-array, array and inverter-input levels, including external battery contribution where applicable.

Topology determines which strings are actually paralleled. Strings on separate isolated MPPT channels must not be treated as one parallel group unless the equipment profile proves an internal shared path.

# 8. Individual and Grouped Protection

The kernel distinguishes individual string fusing from several strings beneath one shared device.

An individual fuse carries normal design current while remaining at or below the module protection rating and satisfying equipment limits.

A grouped device must account for healthy strings inside the protected group feeding a faulted member. Applicable lower and upper inequalities are evaluated explicitly. For crystalline modules, grouped protection often has no valid solution at higher group counts. The engine calculates the permitted interval and fails when it is empty.

# 9. Restricted-Access Engineering Relaxations

IEC TS 62738 engineering-analysis pathways are conditional evidence routes, not universal exceptions.

Where a design relies on such a relaxation, the receipt requires documented failure-mode analysis, identified backfeed magnitudes and durations, module testing, explicit module-manufacturer approval, warranty implications and responsible-engineer acceptance.

Absence of a required condition means the relaxation is not demonstrated.

# 10. Wiring Loops and Conductor Pairing

The standards layer consumes loop geometry produced by the array engine. It verifies that same-string positive and negative conductors are routed to minimise loop area and associated bonding conductors are considered where required.

Compliance evidence includes absolute loop area, maximum pole separation, paired-route percentage, unpaired segments, loops enclosing bonded structures and cross-table transitions.

A strategy label alone is not evidence.

# 11. Long DC Routes and Installation Reinforcement

The route model distinguishes exposed unshielded cable from burial, bonded metallic conduit, bonded trunking, armoured cable, screened cable with documented bonding and SPD-protected routes.

A screen or metallic enclosure cannot be credited merely because it exists. Bonding and continuity must be evidenced.

# 12. SPD Critical-Length Check

The SPD trigger based on route length and ground flash density is one of the highest-value geometry-derived rules.

The engine calculates the critical length for the installation type and compares it with the maximum counted route from PCE to module connection point. Only qualifying buried or earthed-screened segments are excluded, and each exclusion is itemised.

Required inputs include ground flash density and provenance, installation classification, route segments, qualifying exclusions, SPD election and location.

Even when SPDs are fitted regardless, the normative calculation still appears on the receipt.

# 13. Voltage Scope

IEC 62548-1 defines the low-voltage DC boundary at 1500 V. A design above this value must not receive a clean certification under that standard.

The correct state is outside scope, accompanied by the evidence path used instead. The engine must avoid casually relabelling 2 kV DC as medium voltage. The standards landscape contains a gap rather than a universally accepted replacement regime.

Equipment, cable, connector, insulation, national-law and insurer acceptance must be evaluated separately.

# 14. Equipment Profiles and Ambient Derating

Inverter, module, fuse, connector, cable and SPD ratings belong in versioned equipment profiles.

Inverter power must not be represented by one ambient-independent number. Apparent and active power limits may derate significantly in hot climates. Missing curves generate visible assumptions rather than silent extrapolation.

The same principle applies to fuse enclosure-temperature derating, cable current-carrying capacity and connector temperature limits.

# 15. Standards Do Not Redesign the Project

The kernel may identify a better route, inverter position, fuse arrangement or duct allocation. It may quantify the opportunity and produce a recommendation. It must not assume the contracted design has changed.

Project state distinguishes modelled contracted design, proposed optimisation, engineering recommendation, client-approved change, site-approved implementation and as-built evidence.

# 16. Validation Receipt Structure

Every rule result includes rule identity, standard and edition, clause, input values and units, provenance, formula or algorithm version, threshold, result, status, warnings, missing evidence, recommended action and relevant geometry, topology and calculation hashes.

The purpose is not merely to declare compliance but to show why the declaration is justified.

# 17. Build 026 Priorities

Build 026 should implement standards-rule and provenance schemas, validation states, `K_I` and `K_Corr` receipts, backfeed inputs, string overcurrent requirement, fuse sizing, grouped-device inequalities, loop-geometry evidence, SPD `L` versus `L_crit`, voltage-scope gate, edition-conflict reporting and deterministic validation receipts.

# 18. Governing Principle

Standards validation is evidence applied to a physical model. It is not a disconnected spreadsheet check and not permission to invent missing facts.

Where data is missing, the kernel says so. Where standards disagree, the kernel shows the disagreement. Where optimisation requires approval, the kernel preserves the contracted design and presents the alternative separately.