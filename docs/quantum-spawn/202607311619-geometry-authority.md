# Quantum Spawn

**Title:** Geometry Authority

**File:** `202607311619-geometry-authority.md`

**Timestamp:** 2026-07-31 16:19 (Device local time)

**Version:** 1.0

**Status:** Canonical

**Authority:** Engineering Design Authority

**Supersedes:** None

**Superseded By:** None

**Dependencies:**
- `202607311609-mission-and-philosophy.md`
- `202607311615-system-architecture.md`

**Current Build:** Build 025

---

# 1. Purpose

This document defines geometry as the authoritative foundation of the Solar Electrical Topology Analysis Engine.

Geometry is not decoration, an approximate drawing or merely a visual layer. It is the physical source of truth from which routing, installed cable quantities, loop area, coupling, surge exposure and later electrical behaviour are derived.

Every future subsystem must consume geometry rather than recreate it.

# 2. Geometry as Engineering Authority

A photovoltaic array is a physical installation before it is an electrical abstraction. Modules occupy space. Tables have dimensions. Inverters have locations. Conductors follow routes. Supports, ducts, trenches and structures constrain those routes. Positive and negative poles may remain paired or separate and enclose large conductive loops.

The geometry engine owns the question: **Where does every physical object and every conductor exist?**

Topology answers what connects. Geometry answers where that connection is physically realised. Neither may substitute for the other.

# 3. Canonical Coordinate System

The authoritative model uses site-local Cartesian coordinates. Large geographic coordinates shall not be passed directly into detailed rendering or route calculations. Each geometry cartridge uses a local origin so coordinates remain numerically stable and Float32 rendering precision remains adequate over kilometre-scale plants.

The model is primarily two-dimensional plan geometry. Height is introduced only where it materially changes routing, cable quantity, separation, containment or physical behaviour.

The project must not drift into unnecessary three-dimensional modelling. The objective is engineering accuracy, not visual spectacle.

# 4. Canonical Geometry Objects

The geometry layer shall contain immutable, validated objects including `Point2D`, optional `Point3D`, `ModuleDimensions`, `ModulePlacement`, `TableLayout`, `InverterPlacement`, `Route`, `RouteSegment`, `SupportPath`, `Duct`, `Trench`, `StructureEnvelope` and `GeometryReceipt`.

Every object shall have stable identifiers and deterministic serialisation. Identical requests must generate identical coordinates and geometry hashes.

# 5. Whole-Table Geometry Boundary

The first authoritative geometry boundary is one complete table. The initial production fixture is 24 strings, 30 modules per string, 720 modules total and one movable inverter.

These are the first validated production values, not universal hard limits. A table request shall allow sensible row and column selection, portrait or landscape orientation, configurable dimensions and gaps, origin, rotation, arbitrary string allocation and inverter placement.

# 6. Deterministic Module Placement

Every module placement shall include module identifier, table identifier, row index, column index, centre point, corner vertices, orientation, rotation and dimensions.

The placement engine must reject duplicate identifiers, impossible dimensions, invalid orientation values and non-finite coordinates.

Repeated generation with identical inputs must reproduce the same placement order, coordinates, bounds and hash. Changing origin or rotation must change the geometry hash without changing module identity.

# 7. Geometry and Topology Separation

String membership is not embedded in module coordinates. A module may retain exactly the same physical position while its string assignment changes. Moving an inverter changes conductor geometry without changing which modules belong to each string.

This allows controlled comparison of sequential and leapfrog stringing, MPPT allocations and inverter locations.

Hashes remain layered: geometry hash, topology hash and routing hash. A change in one layer must not falsely imply a change in another.

# 8. Explicit Conductor Geometry

No cable length may be calculated from a guessed distance. Each conductor is represented by explicit route segments.

Every segment records at minimum segment identifier, string identifier, polarity, start point, end point, route class, geometric length, installation method, containment, burial state, screening state, bonded-screen state and support-path identifier.

The total route length is the sum of explicit segment lengths. The browser may display these segments but may not create or modify them independently.

# 9. Sequential and Leapfrog Routing

Sequential and leapfrog are topology-aware route generators operating on the same physical modules. They are not visual styles.

They may produce different positive and negative lengths, total circuit length, separation, loop area, home-run position, crossing count, parallel-run distance and surge exposure.

Both strategies must be generated deterministically from identical physical inputs. A route using less cable is not automatically superior. Cable quantity and electromagnetic geometry remain separate outputs.

# 10. Movable Inverter Geometry

Inverter placement is an explicit geometry object. Moving it recomputes positive and negative home runs, route vertices, route lengths, affected routing hash and total table cable length.

It must not alter module coordinates, module identities, string membership or MPPT assignments unless explicitly requested.

# 11. Loop Geometry

The geometry engine shall preserve enough information to calculate the conductive loop formed by both poles of every string.

Future metrics include maximum and mean pole separation, signed and absolute enclosed loop area, crossings, structure encirclement and parallel-run length.

Same-string positive and negative conductors must remain identifiable as a pair throughout the route. Specifications based only on counts of positive and negative conductors are insufficient.

# 12. Ducts, Trenches and Structures

Ducts and trenches are engineering objects, not coloured lines. Segments may be exposed, buried, screened, armoured or contained in bonded metallic conduit or trunking.

The engine must identify when a conductor loop encloses a bonded torque tube or other conductive structure. This information is required later for surge and EMC modelling.

# 13. Installed-Length Layers

Pure geometric length is not installed cable length. Later models shall preserve connector approach, harness offset, support offset, bend allowance, service loop, termination allowance and construction tolerance.

The engine distinguishes geometric route length, installed length and procurement length. No hidden percentage silently converts one into another.

# 14. Geometry Receipts

Every geometry calculation produces a receipt containing schema version, table identifier, module count, row and column configuration, orientation, origin, rotation, bounds, module-placement hash, route hash, kernel version and validation state.

The receipt is evidence that later topology and physics calculations used a known physical arrangement.

# 15. Browser Rendering Contract

The browser receives precomputed geometry. Preferred future rendering includes deck.gl with WebGL2 and an orthographic view, binary vertex arrays through Arrow or Parquet, optional Three.js instancing, PMTiles overviews and Flatbush or KDBush indexing.

These technologies are replaceable. The contract is not: **the browser receives vertices and scalar results, never electrical routing rules or engineering formulae.**

# 16. Definition of Geometry Authority

Geometry authority is achieved when a caller can request a complete table, receive deterministic module placements, allocate strings, select sequential or leapfrog routing, move the inverter and receive explicit conductor polylines with recomputed lengths and receipts.

No voltage drop, fault current, surge result or standards pass is authoritative before this condition is met. Geometry is the first engineering result.