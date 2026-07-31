# Quantum Spawn

**Title:** Geometry Authority

**File:** `202607311640-geometry-authority.md`

**Timestamp:** 2026-07-31 16:40 (Local)

**Version:** 1.0

**Status:** Canonical

**Authority:** Engineering Design Authority

**Supersedes:** None

**Superseded By:** None

**Dependencies:**
- `202607311609-mission-and-philosophy.md`
- `202607311620-system-architecture.md`

**Referenced By:**
- Array Engine
- Physics, EMC and Lightning
- Standards Validation
- Browser Visualisation

**Current Build:** Build 025

---

# 1. Purpose

This document defines geometry as the authoritative foundation of the Solar Electrical Topology Analysis Engine.

Geometry is not decoration. It is not merely a visual layer and it is not an approximate drawing used to make calculations easier to understand. Geometry is the physical source of truth from which routing, installed cable quantities, loop area, coupling, surge exposure and later electrical behaviour are derived.

Every future subsystem must consume geometry rather than recreate it.

---

# 2. Geometry as Engineering Authority

A photovoltaic array is a physical installation before it is an electrical abstraction.

Modules occupy space. Tables have dimensions. Inverters have locations. Conductors follow routes. Supports, ducts, trenches and structures constrain those routes. Positive and negative poles may remain paired or may separate and enclose large conductive loops.

The geometry engine therefore owns the question:

**Where does every physical object and every conductor exist?**

Topology answers what connects. Geometry answers where that connection is physically realised.

Neither may substitute for the other.

---

# 3. Canonical Coordinate System

The authoritative model uses site-local Cartesian coordinates.

Large geographic coordinates shall not be passed directly into detailed rendering or route calculations. Each geometry cartridge uses a local origin so that coordinates remain numerically stable and Float32 rendering precision remains adequate over kilometre-scale plants.

The model is primarily two-dimensional plan geometry. Height is introduced only where it materially changes routing, cable quantity, separation, containment or physical behaviour.

The project must not drift into unnecessary three-dimensional modelling. The objective is engineering accuracy, not visual spectacle.

---

# 4. Canonical Geometry Objects

The geometry layer shall contain immutable, validated objects including:

- `Point2D`
- optional `Point3D` where height is materially required
- `ModuleDimensions`
- `ModulePlacement`
- `TableLayout`
- `InverterPlacement`
- `Route`
- `RouteSegment`
- `SupportPath`
- `Duct`
- `Trench`
- `StructureEnvelope`
- `GeometryReceipt`

Every object shall have stable identifiers and deterministic serialisation.

Identical requests must generate identical coordinates and identical geometry hashes.

---

# 5. Whole-Table Geometry Boundary

The first authoritative geometry boundary is one complete table.

The initial production fixture is:

- 24 strings
- 30 modules per string
- 720 modules total
- one movable inverter

The engine must not assume that a table always has 24 strings or 30 modules per string. These values are the first validated production target, not universal limits.

A table request shall allow:

- arbitrary sensible row and column selection
- portrait or landscape module orientation
- configurable module width and height
- configurable row and column gaps
- configurable origin
- configurable rotation
- arbitrary string allocation over placed modules
- inverter placement anywhere permitted by the engineering model

---

# 6. Deterministic Module Placement

Every module placement shall include:

- module identifier
- table identifier
- row index
- column index
- centre point
- corner vertices
- orientation
- rotation
- dimensions

The placement engine must reject duplicate identifiers, impossible dimensions, invalid orientation values and non-finite coordinates.

Repeated generation with identical inputs must reproduce the same placement order, coordinates, bounds and hash.

Changing origin or table rotation must change the geometry hash without changing module identity.

---

# 7. Geometry and Topology Separation

String membership is not embedded in module coordinates.

A module may retain exactly the same physical position while its string assignment changes. Similarly, moving an inverter changes conductor geometry without changing which modules belong to each string.

This separation enables controlled engineering comparison.

Examples:

- sequential and leapfrog stringing may use the same module placement
- two MPPT allocation plans may use the same table geometry
- several inverter locations may be tested without rebuilding the table

Hashes shall therefore remain layered:

- geometry hash
- topology hash
- routing hash

A change in one layer must not falsely imply a change in another.

---

# 8. Explicit Conductor Geometry

No cable length may be calculated from a guessed distance.

Each conductor shall be represented by explicit route segments. Every segment must record at minimum:

- segment identifier
- string identifier
- polarity
- start point
- end point
- route class
- geometric length
- installation method
- containment
- burial state
- screening state
- bonded-screen state
- support path identifier

The total route length is the sum of explicit segment lengths.

The browser may display these segments but may not create or modify them independently.

---

# 9. Sequential and Leapfrog Routing

Sequential and leapfrog are topology-aware route generators operating on the same physical modules.

They are not visual styles.

They produce different conductor paths and therefore may produce different:

- positive cable length
- negative cable length
- total circuit length
- conductor separation
- loop area
- home-run position
- crossing count
- parallel-run distance
- induced surge exposure

The geometry engine must produce both strategies deterministically so they can be compared from identical physical inputs.

A route that uses less cable is not automatically superior. A longer route may preserve same-string pole pairing and dramatically reduce loop area. Cable quantity and electromagnetic geometry must remain separate outputs.

---

# 10. Movable Inverter Geometry

Inverter placement is an explicit geometry object.

Moving the inverter must recompute:

- string positive home runs
- string negative home runs
- route vertices
- route lengths
- affected routing hash
- total table cable length

It must not alter:

- module coordinates
- module identities
- string membership
- MPPT assignments unless explicitly requested

This rule is essential for optimisation studies. The engine must be able to compare inverter locations without introducing hidden topology changes.

---

# 11. Loop Geometry

The geometry engine shall preserve enough information to calculate the conductive loop formed by the positive and negative poles of every string.

Required future metrics include:

- maximum pole separation
- mean pole separation
- signed enclosed loop area
- absolute enclosed loop area
- crossings
- structure encirclement
- parallel-run length

Same-string positive and negative conductors should be identifiable as a pair throughout the route.

Specifications based only on counts of positive and negative cables are insufficient. Six positives and six negatives in a duct are not necessarily safe geometry unless each positive is paired with the corresponding negative of the same string.

---

# 12. Ducts, Trenches and Structures

Ducts and trenches are engineering objects, not coloured lines.

A route segment may belong to:

- exposed support routing
- buried routing
- screened routing
- bonded metallic conduit
- armoured cable
- earthed metallic trunking

The engine must also identify when a conductor loop encloses a bonded torque tube or other conductive structure. Cross-table routing around a bonded structure can create a much larger effective loop than ordinary cable separation suggests.

This information is required later for surge and EMC modelling.

---

# 13. Installed-Length Layers

Pure geometric length is not installed cable length.

The later installed-length model shall preserve individual additions such as:

- connector approach
- harness offset
- support offset
- bend allowance
- service loop
- termination allowance
- construction tolerance

These allowances must remain visible and separately receipted.

The engine shall distinguish:

1. geometric route length
2. installed length
3. procurement length

No hidden percentage shall silently convert one into another.

---

# 14. Geometry Receipts

Every authoritative geometry calculation shall produce a receipt containing:

- schema version
- table identifier
- module count
- row and column configuration
- orientation
- origin
- rotation
- bounds
- module placement hash
- route hash where routes exist
- kernel version
- validation state

The receipt is the evidence that later topology and physics calculations used a known physical arrangement.

---

# 15. Browser Rendering Contract

The browser shall receive precomputed geometry.

Preferred future rendering includes deck.gl with WebGL2 and an orthographic view, using binary vertex arrays delivered through Apache Arrow or Parquet. Three.js instancing may be used for specialised geometry cartridges. PMTiles may serve plant-level overview data, while Flatbush or KDBush may support spatial indexing.

These technologies are replaceable.

The contract is not replaceable:

**The browser receives vertices and scalar results, never electrical routing rules or engineering formulae.**

This structural restriction prevents the browser from inventing cable paths or electrical quantities.

---

# 16. Definition of Geometry Authority

Geometry authority is achieved when a kernel caller can request a complete table, receive deterministic module placements, allocate strings, select sequential or leapfrog routing, move the inverter and receive explicit conductor polylines with recomputed lengths and geometry receipts.

No voltage drop, fault current, surge result or standards pass is authoritative before this condition is met.

Geometry is therefore not the first picture in the workflow.

It is the first engineering result.
