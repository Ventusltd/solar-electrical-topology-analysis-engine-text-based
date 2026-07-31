# Quantum Spawn

**Title:** Respawn Instructions and Operating Protocol

**File:** `202607311652-respawn-instructions.md`

**Timestamp:** 2026-07-31 16:52 (Device local time)

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
- `202607311628-standards-validation.md`
- `202607311640-commercial-strategy.md`

**Current Build:** Build 025, preparing Builds 026 and 027

---

# 1. Purpose

This document defines how a future engineering discussion, software agent or AI instance must reload the Solar Electrical Topology Analysis Engine without relying on prior chat history.

The Quantum Spawn folder is the canonical restart mechanism. Its files are timestamped engineering knowledge objects, not transcripts. A future session should read the relevant files directly from the repository and treat them as the governing authority until a later timestamped file explicitly supersedes them.

The folder is designed to grow indefinitely. New topics are added as new Markdown files using the naming convention:

`YYYYMMDDHHMM-title.md`

The timestamp must come from the user’s device-local time or another explicitly agreed authoritative clock. It must never be invented for convenience.

# 2. Mandatory Reload Order

For a complete project respawn, read the current canonical files in chronological order:

1. Mission and Philosophy
2. System Architecture
3. Geometry Authority
4. Array Engine and Topology Authority
5. Physics, EMC and Lightning
6. Standards and Validation
7. Commercial Strategy and Product Positioning
8. Respawn Instructions and Operating Protocol

Later files may extend, correct or supersede parts of this sequence. Chronology alone does not make a file authoritative; each file’s metadata must state its status and supersession relationship.

# 3. First Response After Respawn

After reading the referenced Quantum Spawn files, the new instance should summarise the project in a few sentences and identify the current build boundary.

The correct starting position is:

- geometry is authoritative;
- the Python kernel is the sole engineering authority;
- the browser renders but does not calculate engineering;
- topology states what connects;
- geometry states where it exists;
- routing creates explicit conductor paths;
- physics is downstream of those paths;
- standards validate the physical model;
- receipts preserve deterministic evidence.

The current implementation focus is Build 025: one complete table capable of supporting 24 strings of 30 modules, arbitrary sensible table arrangement, explicit sequential and leapfrog connections, movable inverter placement and geometry-derived positive and negative conductor lengths.

# 4. Non-Negotiable Invariants

A respawned instance must not weaken the following rules:

1. The browser never invents a cable route.
2. The browser never computes authoritative cable length, voltage drop, fault current, EMC or standards compliance.
3. Physics is not calculated before explicit conductor geometry exists.
4. Module, string, MPPT input, MPPT and inverter relationships remain explicit.
5. An MPPT is not treated as identical to a physical string input.
6. Electrically isolated inputs are not treated as parallel merely because they share an MPPT label.
7. Sequential and leapfrog are topology-aware route strategies, not visual themes.
8. Same-string positive and negative conductor identity is preserved through all route segments.
9. Cable length and loop area remain separate engineering outputs.
10. Standards do not silently redesign a contracted project.
11. Missing manufacturer or project evidence remains visible.
12. Large plants are created through deterministic replication of validated tables and inverter blocks, not through separate large-project algorithms.

# 5. Immediate Engineering Target

The next useful milestone is not a million-module renderer and not ornamental three-dimensional graphics.

The target is a complete, inspectable, deterministic table engine that allows the user to:

- choose a sensible table geometry;
- place 720 modules or another supported quantity;
- form any valid number of ordered strings within equipment and software limits;
- assign strings to physical inverter inputs and MPPTs;
- switch between sequential and leapfrog routing;
- move the inverter;
- recompute every affected positive and negative route;
- compare total cable length and loop geometry;
- receive geometry, topology and routing receipts.

This milestone establishes the physical array engine required before serious electrical physics can be trusted.

# 6. Deferred Work

The respawned instance must resist skipping ahead.

Build 026 standards validation and Build 027 EMC, lightning and distributed-line modelling are important, but they depend upon Build 025 outputs.

The array engine must first preserve route coordinates, conductor pairing, containment, burial, screening, bonded structures and installation classifications. Those fields later support resistance, voltage drop, fault-current neighbourhoods, capacitance, inductance, surge exposure, SPD critical-length checks and first- and second-fault paths.

A formula applied to an abstract string count is not an authoritative substitute for a physical model.

# 7. Visualisation Direction

The accepted visual language is the existing V7 overview and V8 detailed connection style.

V7 provides table, inverter, MPPT and string overview. V8 provides module-terminal and detailed conductor connection maps. V10 should consume the same authoritative geometry and offer these modes rather than invent a new symbolic or decorative cable language.

Scalable rendering technologies such as deck.gl, WebGL2, Arrow, Parquet, PMTiles and spatial indexing are implementation mechanisms only. They must preserve the existing engineering language and must never become a second routing engine.

No compute budget should be wasted on photorealistic or ornamental 3D. Height or 3D coordinates are introduced only when required by actual routing, separation, capacitance, inductance, shielding or structural interaction.

# 8. Standards and Evidence Protocol

A future instance must identify standards by title, edition, amendment and clause. IEC 62548-1:2023 and IEC TS 62738:2018 are separate authorities and may not be blended anonymously.

Validation outputs require provenance and may return PASS, PASS_WITH_WARNINGS, FAIL, INCOMPLETE_EVIDENCE, OUTSIDE_SCOPE, ENGINEERING_REVIEW_REQUIRED or CLIENT_APPROVAL_REQUIRED.

Backfeed current, `K_Corr`, bifacial simulation, equipment ratings, ambient derating, ground flash density, screen bonding and SPD properties must never be silently guessed.

Where a rule or project fact is uncertain, the instance should say so and preserve the uncertainty in the receipt.

# 9. Contractual and Confidentiality Discipline

The engine may expose problems and propose better arrangements. Massive changes must not be treated as adopted without engineer, client and site approval.

The model must preserve separate states for contracted design, proposed optimisation, engineering recommendation, client-approved change, site-approved implementation and as-built evidence.

Confidential project details must not be published in the public repository. Public code and Quantum Spawn documents should contain generic engineering architecture, anonymised examples and standards-derived rules. Client-specific geometry, contracts, equipment schedules and failure records belong in private project data or controlled evidence stores.

# 10. Commercial Discipline

The platform is sold on engineering evidence, not graphics or hype.

Its strongest propositions are deterministic cable quantities, connection-integrity validation, route and loop-area comparison, standards provenance, design-to-as-built traceability and warranty defence against installation-induced stress.

Protection and monitoring remain separate. Monitoring does not replace local, fail-safe and communications-independent protection.

# 11. How to Extend Quantum Spawn

When a new subject becomes important, create a new timestamped file in `docs/quantum-spawn/`.

Each file should include title, filename, device-local timestamp, version, status, authority, supersedes, superseded-by and dependencies.

Do not overwrite prior history merely to make the folder appear tidy. Corrections should either be performed immediately with traceable commits or expressed through a new file that explicitly supersedes the old one.

A future user can respawn only the required topic by pointing to its exact path. A full respawn reads the canonical dependency chain.

# 12. Governing Instruction

When future conversation memory, model recollection, convenience or an attractive new technology conflicts with the canonical Quantum Spawn files, the files take precedence until explicitly superseded.

The project North Star remains:

**Build a deterministic, geometry-authoritative engineering engine for photovoltaic DC systems in which physical layout produces explicit topology and routing, those routes enable electrical and electromagnetic physics, standards validate the result, and receipts preserve evidence suitable for design, construction, compliance, warranty and forensic use.**