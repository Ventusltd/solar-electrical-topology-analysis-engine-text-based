# Quantum Spawn

**Title:** System Architecture

**File:** `202607311615-system-architecture.md`

**Timestamp:** 2026-07-31 16:15 (Device local time)

**Version:** 1.0

**Status:** Canonical

**Authority:** Engineering Design Authority

**Supersedes:** None

**Superseded By:** None

**Dependencies:**
- 202607311609-mission-and-philosophy.md

**Referenced By:**
- Geometry Authority
- Array Engine
- Physics
- Validation

**Current Build:** Build 025

---

# 1. Purpose

This document defines the canonical architecture of the Solar Electrical Topology Analysis Engine.

Every subsystem exists for one reason only: to preserve a single engineering authority throughout the entire software stack.

The architecture deliberately separates engineering from presentation. This separation is not an implementation detail. It is the defining characteristic of the platform.

# 2. System Overview

The system is divided into five layers:

```text
Browser
↓
Presentation API
↓
Python Kernel
↓
Engineering Objects
↓
Engineering Receipts
```

Every calculation flows downward. Nothing authoritative flows upward.

# 3. Browser

The browser is deliberately passive. Its responsibilities are limited to rendering, interaction, editing requests, camera control and user experience.

The browser never owns engineering. It never creates electrical data, estimates, interpolates, optimises or validates. Instead it displays exactly what the kernel provides.

# 4. Presentation Layer

The presentation layer translates engineering objects into visual objects such as module polygons, cable polylines, labels, dimensions, tables and receipts.

Nothing is invented. Every displayed vertex originates from the kernel.

# 5. Python Kernel

The kernel is the only engineering authority. It owns geometry, topology, routing, validation, physics, future optimisation, future standards, future EMC, future surge analysis and future transmission-line modelling.

Every engineering decision originates here.

# 6. Canonical Objects

Everything is represented by immutable engineering objects, including Module, String, Table, MPPT, Inverter, Power Block, Plant, Route, Segment and Receipt.

No browser object is authoritative.

# 7. Data Flow

Engineering proceeds in one direction:

```text
Geometry
↓
Topology
↓
Routing
↓
Physics
↓
Validation
↓
Receipt
↓
Browser
```

Physics never creates geometry. Validation never changes topology. The browser never recalculates receipts.

# 8. Geometry

Geometry is the physical truth. It describes location, orientation, rotation, spacing, dimensions, support structure, ducts, containment and routes.

Geometry contains no electrical assumptions.

# 9. Topology

Topology describes connectivity. It answers what is connected. Geometry answers where it is connected.

These concepts remain independent. Changing inverter position changes geometry but not topology. Changing string assignment changes topology but does not necessarily change geometry.

# 10. Routing

Routing converts topology into physical conductors. Routes consist of explicit segments. Each segment records start point, end point, length, installation method, containment, screening, burial, bonding and support system.

These become inputs to later physics.

# 11. Physics

Physics is intentionally downstream. It consumes geometry and never creates it.

Future modules include resistance, voltage drop, fault current, capacitance, inductance, surge propagation, EMC and distributed transmission-line behaviour.

Every result is derived from explicit conductor geometry.

# 12. Validation

Validation compares engineering against standards including IEC 62548, IEC TS 62738, IEC 61730 and IEC 60364.

Validation never changes the engineering model. It reports compliance. It does not redesign installations.

# 13. Engineering Receipts

Every authoritative calculation produces evidence. Receipts contain geometry hash, topology hash, routing hash, calculation hash, equipment profile, kernel version, validation state and timestamp.

Receipts allow complete engineering traceability.

# 14. Equipment Profiles

Equipment is never hard coded. Every inverter, module and connector is represented by a profile.

This allows future hardware to be introduced without changing computational architecture.

# 15. Browser Technology

Current preferred technologies include deck.gl, WebGL2, Apache Arrow, DuckDB, Flatbush, PMTiles and Three.js instancing where appropriate.

These are implementation choices, not architectural authority. Should better rendering technology appear, only the presentation layer changes. The kernel remains untouched.

# 16. Scaling

Large projects are built by replication:

```text
Validated table
↓
Validated inverter block
↓
Validated power block
↓
Validated plant
```

The software should never require different algorithms simply because a project grows. Scale is achieved through deterministic replication.

# 17. Failure Philosophy

The system fails safely. Missing geometry blocks routing. Missing routing blocks physics. Missing physics blocks validation. Missing validation blocks authoritative receipts.

Unknown information is never silently assumed.

# 18. Future Expansion

Future capabilities should plug into existing architecture rather than replacing it. Expected modules include EMC, lightning, arc behaviour, distributed transmission-line analysis, digital twin integration, protection optimisation and AI-assisted engineering review.

None should require redesign of the kernel.

# 19. Architectural Invariants

The following rules are immutable:

- Geometry is authoritative.
- Topology is independent of geometry.
- Routing is explicit.
- Physics is downstream.
- Standards validate engineering.
- Receipts are deterministic.
- The browser never computes engineering.
- The kernel is the single source of engineering truth.

# 20. Conclusion

The architecture deliberately separates engineering from presentation. This allows every engineering discipline to build upon one canonical model.

Instead of maintaining independent geometry, electrical, compliance and visual representations, the platform maintains one authoritative engineering model. Everything else becomes a projection of that model.

This architecture should not be altered unless a future design demonstrably strengthens engineering authority without compromising determinism.