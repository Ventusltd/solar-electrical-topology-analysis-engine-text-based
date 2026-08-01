# Trueself

**Title:** Complete 352 kVA Inverter-Block Completion Plan

**File:** `202608010104-complete-352-kva-inverter-block-plan.md`

**Timestamp:** 2026-08-01 01:04 Europe/London

**Version:** 1.0

**Status:** Active execution control

**Authority:** Product Owner instruction interpreted through the canonical Quantum Spawn architecture and verified repository state

**Supersedes:** None

**Extends:**
- `docs/quantum-spawn/202607311609-mission-and-philosophy.md`
- `docs/quantum-spawn/202607311620-system-architecture.md`
- `docs/quantum-spawn/202607311640-geometry-authority.md`
- `docs/quantum-spawn/202607311700-array-engine.md`
- `docs/quantum-spawn/202607311720-physics-emc-lightning.md`
- `docs/quantum-spawn/202607311740-standards-validation.md`
- `docs/quantum-spawn/202607311820-respawn-instructions.md`
- `docs/quantum-spawn/202607312348-trueself-full-reload-tablet.md`
- `docs/refinement/202607312059-build-025-5-authority-consolidation.md`
- `docs/refinement/202607312344-employer-requirements-development-control.md`
- `docs/builds/BUILD-025-WHOLE-TABLE-GEOMETRY-FIRST.md`
- `v7-development/comparisons/BUILD_PLAN_FEEDS_I_II.md`
- `v8-leapfrog/README.md`
- `BUILD_RECOVERY_INSTRUCTIONS_CHATGPT.md`

**Current Build Relevance:** Build 025.5D1 and all later builds

**Restore Point:** `restore/2026-08-01-0104-pre-trueself-plan`

---

## 1. Purpose

This document defines the small-step route from the current verified repository state to the first complete product boundary.

It does not replace Quantum Spawn, erase the V6, V7 or V8 workbenches, reopen settled architecture or authorise a broad rewrite.

It adds an operational Trueself execution layer whose only purpose is to finish the original job without losing the engineering history that made the current package possible.

No engineering code is changed by this planning record.

## 2. Correct first product boundary

The first complete product is one full inverter DC block comprising:

```text
module rated power                 660 Wp bifacial
modules per string                  30
string rated power                  19.800 kWp
strings                              24
module count                        720
total DC input power                475.200 kWp
inverter apparent-power rating      352 kVA
DC-to-AC nameplate ratio              1.350
```

This is the permanent first completion fixture.

The twenty-four-by-thirty fixture is not merely a module table, a cable comparison or a scale test. It is the complete electrical boundary from every module and factory lead through twenty-four ordered string circuits and physical inverter inputs to one inverter.

The existing term `whole table` shall not be destructively renamed in current code or historical documents. The semantic clarification is:

- the reference fixture is one complete inverter block;
- the 720 modules may occupy one or more physical tables, ranks or array sections;
- physical tables are geometry objects within the inverter block;
- the inverter block is the first complete diagnostic and computation boundary;
- later plants replicate validated inverter blocks without changing engineering semantics.

Any future object migration from a broad historical `table` meaning to explicit physical tables plus an inverter-block aggregate requires a separate restore point, compatibility plan and full validation.

## 3. What must be preserved

The following work is valuable and shall not be discarded:

- the V6 complete-circuit reference, including external conductors, factory leads, connectors, resistance, voltage drop, loss, loop geometry, inductance, capacitance and propagation concepts;
- the V7 electromagnetic and evidence-discipline foundations, including ordered segments, differential and common-mode separation, frequency applicability and explicit unresolved states;
- the V8 sequential-versus-leapfrog cable schedule, feasibility gate, actual-site aggregation and the correction separating field-installed, factory-fitted and total circuit conductor;
- the V9 and V10 deterministic engines and their regression value;
- Build 025 geometry, topology, assignment and routing authority;
- Build 025.5 resistance evidence, uncertainty, qualification and deterministic serialisation;
- the installed `solar_topology` package, clean-wheel gate, compatibility shims and historical workbenches;
- every restore point, failure record, correction record and validation checkpoint.

No root shim, `src` module, historical browser workbench or duplicate-looking path may be deleted merely because an external audit calls it redundant.

Before any consolidation, the build must first prove:

1. which file is canonical;
2. which file is an intentional compatibility layer;
3. which file is historical evidence;
4. which imports external consumers still use;
5. that the clean wheel and repository checkout remain equivalent;
6. that removal does not break a declared public contract.

Deletion or migration is always a separate bounded build.

## 4. Trueself operating cycle

Every material step follows exactly this sequence:

### Goal

State one bounded engineering outcome and its authority boundary.

### Build

Make only the changes required for that outcome. Create a restore-point branch before the material change.

### Test

Run focused tests first, then the full declared validation envelope and the clean installed-wheel gate. Inspect every failure. Do not stack another build over an unresolved result.

### Write next spawn when passed

Only after the tests pass, write one new timestamped file in:

```text
docs/trueself/YYYYMMDDHHMM-title.md
```

The record shall state:

```text
goal attempted
build completed
files changed
authority classification
focused tests
full validation
clean-wheel result
known limitations
next single goal
```

When a step changes canonical architectural or engineering truth, also add the appropriate Quantum Spawn checkpoint. Trueself execution records do not compete with or silently supersede Quantum Spawn.

If a test fails, write a bounded failure record and stop. The next file addresses only the first understood failure category.

## 5. Definition of the finished inverter-block job

The first product milestone is complete when a clean installed package can construct, diagnose and export the reference inverter block and prove all of the following:

- exactly 720 uniquely identified module placements;
- exactly 24 ordered strings containing 30 modules each;
- exactly one positive and one negative free terminal per string;
- explicit factory leads, connectors and module-to-module connections;
- explicit physical inverter inputs distinct from MPPT control identities;
- evidence-bound mapping of physical inputs to MPPTs and any shared DC bus;
- no assumed internal paralleling or reverse-current blocking without equipment evidence;
- sequential, leapfrog, mirrored and custom strategies producing the same canonical connection and segment schema;
- explicit positive and negative routes retaining same-string identity;
- movable inverter geometry without silent topology changes;
- geometric, installed and procurement conductor lengths kept separate;
- field-installed and factory-fitted conductor quantities kept separate;
- evidence-qualified resistance, voltage drop, resistive loss and uncertainty;
- visible blocked, provisional and incomplete-evidence diagnostics;
- deterministic geometry, topology, assignment, routing, evidence, calculation and diagnostic receipts;
- one portable project model and reproducible diagnostic export;
- one local offline command path operating from a clean installation;
- one browser workflow that sends commands and renders kernel results without calculating engineering in JavaScript.

The 30 kWp, 1 MWp, 100 MWp and 1 GWp fixtures are later semantic and performance proofs. They do not replace the first complete 475.2 kWp DC inverter-block milestone.

## 6. Immediate small-step build sequence

### TS-001 — Close the current resistance public contract

**Goal**

Finish the already-started Build 025.5D1 boundary.

**Build**

Expose these existing functions through the explicitly provisional top-level package API:

```text
resistance_source_assessment_payload
resistance_source_assessment_json
resistance_source_assessment_hash
```

Extend the clean-wheel consumer probe to call all three functions and reproduce the same payload, canonical JSON and hash outside the repository checkout.

Do not integrate qualification assessments into calculation receipts in this step.

**Test**

- import identity tests;
- explicit public-classification tests;
- exact payload and canonical JSON tests;
- repeated hash determinism;
- clean-wheel hash equality;
- full Python, V8, V8 reconciliation, V9, V10 JavaScript and clean-wheel validation.

**Write next spawn when passed**

Record ER-01 as complete and name TS-002 as the only next goal.

### TS-002 — Establish one programme truth manifest

**Goal**

Remove manually duplicated build, test and progress claims without changing engineering.

**Build**

Create a versioned machine-readable programme-state manifest containing at minimum:

```text
current_build
validated_commit
package_version
validation_suites
restore_point
reference_inverter_block
canonical_capabilities
provisional_capabilities
historical_workbenches
active_gate
next_single_goal
known_limitations
```

The reference block entry shall state 660 Wp bifacial modules, 30 modules per string, 24 strings, 720 modules, 475.2 kWp DC and 352 kVA.

Generate or validate public status sections from the manifest. Do not manually invent a completion percentage.

**Test**

- schema validation;
- exact reference-block arithmetic;
- README/dashboard drift gate;
- stale Build 024 and 176-test claims absent from generated current status;
- full validation and clean wheel unchanged.

**Write next spawn when passed**

Record the manifest as programme truth and name TS-003.

### TS-003 — Freeze the generic reference equipment contract

**Goal**

Represent the reference block without using confidential project information or manufacturer names.

**Build**

Create or refine versioned generic profiles for:

- a 660 Wp bifacial module;
- a 352 kVA inverter;
- 24 physical DC string inputs;
- the evidenced MPPT/input arrangement;
- the evidenced or unresolved DC-bus and reverse-current-blocking behaviour;
- factory leads, connectors and field conductors.

Only populate values supported by controlled evidence. Missing values remain missing. Licensed standards text, tables and figures shall not be copied into the public repository. Store paraphrased rule logic, clause locators, edition metadata, provenance and hashes only.

**Test**

- profile schema tests;
- exact 720-module and 475.2 kWp assembly arithmetic;
- missing-evidence states;
- no silent internal-parallel assumption;
- no confidential names or project identifiers;
- deterministic profile hashes;
- full validation and clean wheel.

**Write next spawn when passed**

Record the accepted reference profiles and name TS-004.

### TS-004 — Add the complete inverter-block aggregate and receipt

**Goal**

Make the reference inverter block a first-class kernel object rather than an interpretation assembled only by tests or browser pages.

**Build**

Add a typed inverter-block aggregate above its physical tables or array sections and below the later power-block level. Preserve existing identifiers and compatibility contracts.

The deterministic block receipt shall bind:

```text
block identifier
module profile and revision
inverter profile and revision
module count
string count
modules per string
DC nameplate power
inverter apparent power
physical input count
MPPT evidence state
geometry receipt
assignment receipt
topology receipt
routing receipt
equipment-evidence receipt
```

Do not add standards or EMC calculations in this step.

**Test**

- exact reference fixture creation;
- duplicate and omission failures;
- deterministic block receipt and hash;
- compatibility with the existing 24-by-30 fixture;
- no changes to historical receipt hashes unless the new aggregate is explicitly requested;
- full validation and clean wheel.

**Write next spawn when passed**

Record inverter-block authority and name TS-005.

### TS-005 — Complete physical input and MPPT authority

**Goal**

Prove how all 24 strings terminate electrically without equating a physical input, an MPPT and an inverter DC bus.

**Build**

Represent every physical input, its terminal pair, assigned string, MPPT control relationship and equipment-evidence state. Shared paths, backfeed paths and reverse-current blocking remain unresolved until supported by evidence.

**Test**

- 24 unique occupied physical inputs;
- no duplicate input occupation;
- no string assigned to two inputs;
- unused inputs allowed and visible for other profiles;
- MPPT labels do not create implicit electrical parallel nodes;
- invalid or incomplete equipment evidence produces the correct diagnostic state;
- deterministic assignment and equipment-topology receipts;
- full validation and clean wheel.

**Write next spawn when passed**

Record input/MPPT authority and name TS-006.

### TS-006 — Complete all 24 string paths from modules to inverter

**Goal**

Produce one continuous, inspectable electrical path for every string.

**Build**

For each of the 24 strings, materialise:

```text
module terminals
factory positive and negative leads
mated connectors
ordered inter-module links
turnaround where applicable
positive field conductor
negative field conductor
inverter approach
physical input terminals
```

Sequential, leapfrog, mirrored and custom strategies generate explicit connections and segments. Downstream physics consumes segments and never branches on the strategy name.

**Test**

- 24 continuous non-branched paths;
- 30 modules used once per string;
- 720 modules used once in the block;
- explicit positive and negative free ends;
- same-string pole identity through every field route;
- cartridge invariants for factory leads and ordinary connector count;
- no user-entered derived route length;
- route length equals ordered segment sum;
- full validation and clean wheel.

**Write next spawn when passed**

Record complete-path authority and name TS-007.

### TS-007 — Finish geometry and installed-length truth

**Goal**

Make conductor quantity respond only to explicit physical placement, support paths and visible installation allowances.

**Build**

Complete physical table/array-section composition, terminal coordinates where evidenced, movable inverter routes and separately receipted allowances for connector approach, support offsets, bends, service loops, terminations and construction tolerance.

Do not use a universal tilt multiplier. Do not rename historical objects without a migration build.

**Test**

- moving the inverter changes only dependent routes and hashes;
- module placement and string membership remain stable;
- geometric, installed and procurement lengths remain distinct;
- field-installed and factory-fitted conductor remain distinct;
- sequential/leapfrog total-conductor reconciliation remains correct;
- unavailable geometry produces blocked rather than invented routes;
- full validation and clean wheel.

**Write next spawn when passed**

Record installed-length authority and name TS-008.

### TS-008 — Produce the complete steady-state inverter-block diagnosis

**Goal**

Calculate and diagnose the entire 475.2 kWp DC block through one shared physics authority.

**Build**

Aggregate evidence-qualified segment results to string, physical input, MPPT control group and inverter-block levels. Include resistance, voltage drop, voltage-drop percentage, resistive loss, conductor quantity and uncertainty. Keep design targets separate from standards requirements.

The generic metal-coated conductor sources remain candidates until their exact edition, table and verification state are encoded. No source is promoted because tests are green.

**Test**

- segment-to-string-to-block aggregation laws;
- exact inputs collapse to exact intervals;
- candidate evidence remains visibly provisional;
- plain, metal-coated, measured and manufacturer-declared bases remain distinguishable;
- blocked evidence never produces a clean authoritative result;
- receipt hashes change only when their dependency domains change;
- full validation and clean wheel.

**Write next spawn when passed**

Record the first complete steady-state inverter-block diagnosis and name TS-009.

### TS-009 — Define the portable project and command boundary

**Goal**

Allow a clean local installation to reconstruct and operate the reference inverter block without direct Python object manipulation.

**Build**

Define versioned project, command and response schemas for the reference block. Implement the smallest deterministic local CLI or file protocol for:

```text
create project
place physical tables or array sections
create inverter block
assign strings to physical inputs
select topology strategy
move inverter
generate routes
calculate steady state
run diagnostics
export project
```

Transport remains separate from engineering logic.

**Test**

- schema round-trip without identifier loss;
- invalid-input diagnostics;
- repeated command determinism;
- runtime metadata isolated from engineering hashes;
- complete offline reference-block workflow from a clean wheel;
- full validation and clean wheel.

**Write next spawn when passed**

Record the local authority bridge and name TS-010.

### TS-010 — Export the reproducible inverter-block diagnostic package

**Goal**

Make the first complete job independently inspectable and transferable.

**Build**

Export one package containing:

```text
project model
physical geometry
electrical topology
ordered routes
equipment profiles
evidence records
steady-state calculations
uncertainty
diagnostics
limitations
deterministic receipts and hashes
human-readable report
machine-readable files
```

Canonical sorted text is the receipt authority. Columnar files may be included for scale but are not assumed byte-stable without pinned writer settings and independent hash checks.

**Test**

- clean export/import round-trip;
- no lost identifiers, evidence or units;
- canonical receipt byte stability;
- confidential and licensed source-content exclusion;
- deterministic package manifest;
- full validation and clean wheel.

**Write next spawn when passed**

Declare the backend inverter-block product complete and name TS-011.

### TS-011 — Replace one browser workflow with the real block authority

**Goal**

Project the completed inverter-block kernel through a calculation-free browser workflow.

**Build**

Replace one existing browser-owned path with commands and kernel responses. Preserve historical workbenches as labelled references until migration is proven. Do not remove browser calculations before their replacement is tested and available.

**Test**

- no route, resistance, voltage-drop or loss formula in the production path;
- command-to-render tests;
- receipt and diagnostic rendering;
- keyboard and accessibility checks;
- offline local operation;
- full validation and clean wheel.

**Write next spawn when passed**

Record the first genuine thin-client inverter-block workflow and name TS-012.

## 7. Later gated work

Only after TS-001 through TS-011 are complete may the programme treat the following as primary work:

### TS-012 — Standards diagnostics for the complete inverter block

Implement rule schemas and deterministic states first, followed by evidence-bound current factors, backfeed, overcurrent protection, voltage scope, insulation monitoring and SPD critical length in separate sub-builds.

### TS-013 — EMC, surge and distributed physics

Derive loop-area vectors, pairing, inductance, capacitance, propagation delay, model applicability and SPD lead effects from the explicit routes. Do not use generic lightning multipliers or graphics as a substitute for field models.

### TS-014 — Replication and scale

Prove that validated inverter blocks compose into power blocks, plants and fleets while preserving drill-down. The 30 kWp and 1 MWp cases prove downward flexibility; the 100 MWp and 1 GWp cases prove upward scale. None may introduce a second engineering model.

## 8. Copyright, confidentiality and evidence control

The public repository shall not contain:

- copied licensed standards clauses, tables or figures;
- complete proprietary reports;
- confidential project names, drawings, photographs or quantities not approved for publication;
- manufacturer or project names in the generic reference fixture;
- unsupported claims promoted as verified evidence.

The repository may contain:

- original algorithms;
- engineering equations expressed independently;
- paraphrased rule descriptions;
- document, edition and clause locators;
- source metadata and hashes;
- generic, anonymised test fixtures;
- derived values whose derivation and provenance are explicit.

## 9. Governing priority

The governing priority is now:

**Finish one complete, deterministic and evidence-bound 352 kVA inverter block containing 720 bifacial modules and 475.2 kWp DC input, preserve every useful layer of the work already completed, and advance only through Goal → Build → Test → next spawn when passed.**
