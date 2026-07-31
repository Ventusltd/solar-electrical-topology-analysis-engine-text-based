# Quantum Spawn

**Title:** Respawn Instructions and Canonical Reload Procedure

**File:** `202607311820-respawn-instructions.md`

**Timestamp:** 2026-07-31 18:20 (Local)

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
- `202607311740-standards-validation.md`
- `202607311800-commercial-strategy.md`

**Current Build:** Build 025, preparing Builds 026 and 027

---

# 1. Purpose

This module defines how a future engineer, AI instance or new project thread shall reload the Solar Electrical Topology Analysis Engine without relying on conversational memory.

Quantum Spawn is the canonical reload mechanism.

The documents in `docs/quantum-spawn/` are not informal notes. They are versioned engineering memory objects. A future session should read them in chronological order, treat them as authoritative, and continue from the latest non-superseded file relevant to the task.

The purpose is to prevent context loss, architectural drift, repeated research and invented assumptions.

# 2. Canonical Reload Order

For a full project respawn, read the following files in order:

1. `202607311609-mission-and-philosophy.md`
2. `202607311620-system-architecture.md`
3. `202607311640-geometry-authority.md`
4. `202607311700-array-engine.md`
5. `202607311720-physics-emc-lightning.md`
6. `202607311740-standards-validation.md`
7. `202607311800-commercial-strategy.md`
8. `202607311820-respawn-instructions.md`

Later timestamped Quantum Spawn files may refine, extend or supersede individual topics. When that occurs, the newest file with explicit supersession metadata takes precedence.

A partial respawn may load only the relevant topic file and its listed dependencies.

# 3. Authority Rules

The reload process must preserve the following hierarchy of authority:

1. explicit user instruction in the current thread;
2. latest non-superseded Quantum Spawn document;
3. committed build plans and validation receipts;
4. repository implementation and tests;
5. prior conversation memory;
6. unverified recollection.

Conversation memory is never sufficient evidence for repository state.

Before claiming that a file exists, a commit succeeded, a test passed or a build is complete, verify the repository or CI result directly.

Never invent commit hashes, file paths, test status, equipment data or standards wording.

# 4. Immediate Project State

The governing build order is:

Physics → Geometry → Objects → Topology → Computation → Evidence → Reporting → Visualisation

However, the current recovery and construction sequence is geometry-first because later physics requires explicit physical routes.

The active milestone is Build 025: one complete table containing up to twenty-four strings of thirty modules in series, with seven hundred and twenty modules in the reference fixture.

The required first capability is to:

- place all modules deterministically;
- allocate modules into explicit ordered strings;
- generate sequential and leapfrog routes;
- preserve positive and negative pole identity;
- move the inverter;
- recompute affected home-run geometry;
- calculate explicit geometric cable lengths;
- produce deterministic geometry, topology and route hashes.

Electrical physics is not authoritative until this milestone exists.

# 5. Build Sequence to Resume

## Build 025 — Whole-Table Geometry and Array Engine

Complete geometry primitives, string allocation, route generation, movable inverter routing, MPPT input allocation and installed-length layers.

The first acceptance fixture is twenty-four strings by thirty modules.

## Build 026 — Standards Validation

Implement versioned standards rules and provenance, including current derivation, backfeed evidence, overcurrent protection, grouped-device constraints, loop-geometry evidence, SPD critical-length checks, voltage-scope gates and edition conflicts.

## Build 027 — Physics, EMC and Lightning

Implement steady-state resistance and voltage drop, loop-area metrics, inductive surge screening, capacitance, first- and second-fault paths, SPD geometry and distributed transmission-line models.

Do not collapse these builds into one large implementation. Each must produce tests and deterministic receipts.

# 6. Non-Negotiable Architectural Invariants

A respawned session must preserve these rules:

- Geometry is authoritative.
- Topology describes connectivity and remains separate from geometry.
- Routing consists of explicit conductor segments.
- Physics consumes geometry and never invents it.
- Standards validate the physical model and never silently redesign it.
- The Python kernel is the only engineering authority.
- The browser renders kernel outputs and does not calculate electrical quantities.
- Equipment limits are versioned data, not hard-coded assumptions.
- Missing information remains visibly missing.
- Every authoritative output produces deterministic evidence.
- Large projects scale through replication of validated table and inverter-block objects.
- Contracted design, proposed optimisation, approved change and as-built state remain distinct.

Any proposed feature that violates one of these rules must be rejected or redesigned.

# 7. Browser and Data Contract

The browser receives precomputed vertices, identifiers, scalar results and receipts.

It must not receive routing algorithms or electrical formulae that allow it to create an alternative engineering truth.

Preferred rendering technologies may include deck.gl, WebGL2, Apache Arrow, Parquet, PMTiles, Flatbush, KDBush, Three.js instancing and DuckDB-Wasm. These are replaceable implementation choices.

The structural rule is permanent:

**The browser cannot invent conductor paths because the kernel ships only completed geometry.**

# 8. Standards Discipline

When resuming standards work, verify the licensed source text before hard-coding normative rules.

Each rule must record document, edition, amendment state, clause, inputs, provenance, algorithm version and result state.

IEC 62548-1:2023 and IEC TS 62738:2018 must remain separate authorities. Conflicts are surfaced rather than blended.

Missing inverter or battery backfeed data creates incomplete evidence, not an assumed pass.

Arrays above 1500 V DC are outside the low-voltage scope of IEC 62548-1 and must not receive a clean receipt under that standard.

# 9. Engineering Focus on Resume

Do not restart with commercial presentation, browser cosmetics or broad plant scaling.

Resume at the smallest authoritative calculation boundary: one complete physical table.

The immediate engineering question is not merely whether a table contains twenty-four strings. It is whether every one of the seven hundred and twenty modules has a deterministic position, string identity, terminal order, conductor route and valid inverter-input assignment.

Moving the inverter must alter route geometry and cable lengths without altering module placement or string topology.

Sequential and leapfrog must be compared using both cable quantity and loop geometry.

# 10. Evidence and Verification

Before moving to the next build, verify:

- deterministic repeated execution;
- invariant tests;
- no duplicate or omitted modules;
- no branched or open strings;
- no duplicate input assignments;
- explicit positive and negative free ends;
- route length equals the sum of explicit segments;
- inverter movement changes only dependent hashes;
- browser output matches the kernel receipt;
- CI status is known rather than assumed.

A commit is not a validation receipt. A passing test is not a standards certification. Keep these evidence types distinct.

# 11. Quantum Spawn File Convention

Future knowledge modules belong in:

`docs/quantum-spawn/`

The naming format is:

`YYYYMMDDHHMM-title.md`

Files are append-only unless correcting a clear error. Major revisions should create a new timestamped file and declare what it supersedes.

Every file should include title, timestamp, version, status, authority, dependencies, supersession state and current build relevance.

This allows the folder to grow indefinitely while preserving chronology and topic-level reload.

# 12. Final Respawn Instruction

After reading the required Quantum Spawn files, summarise the current authoritative state before making changes.

Then inspect the repository rather than trusting remembered implementation status.

Proceed directly with the next incomplete build step, commit to `main` unless explicitly instructed otherwise, test the work, and produce a real validation receipt.

Do not reopen settled architectural questions without new evidence.

Do not allow browser convenience to weaken kernel authority.

Do not calculate physics from geometry that does not yet exist.

The project North Star remains:

**Create a deterministic, geometry-authoritative, standards-aware computational engine for photovoltaic DC systems that predicts installed reality, electrical behaviour and engineering evidence from one canonical model.**