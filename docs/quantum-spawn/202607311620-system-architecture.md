# Quantum Spawn

**Title:** System Architecture

**File:** `202607311620-system-architecture.md`

**Timestamp:** 2026-07-31 16:20 (Local)

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

Every subsystem exists for one reason only:

To preserve a single engineering authority throughout the entire software stack.

The architecture deliberately separates engineering from presentation.

This separation is not an implementation detail.

It is the defining characteristic of the platform.

---

# 2. System Overview

The system is divided into five layers.

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

Every calculation flows downward.

Nothing authoritative flows upward.

---

# 3. Browser

The browser is deliberately passive.

Its responsibilities are limited to

- rendering
- interaction
- editing requests
- camera control
- user experience

The browser never owns engineering.

The browser never creates electrical data.

It never estimates.

It never interpolates.

It never optimises.

It never validates.

Instead it displays exactly what the kernel provides.

---

# 4. Presentation Layer

The presentation layer translates engineering objects into visual objects.

Examples include

Module polygons

Cable polylines

Labels

Dimensions

Tables

Receipts

Nothing is invented.

Every displayed vertex originates from the kernel.

---

# 5. Python Kernel

The kernel is the only engineering authority.

It owns

geometry

topology

routing

validation

physics

future optimisation

future standards

future EMC

future surge analysis

future transmission-line modelling

Every engineering decision originates here.

---

# 6. Canonical Objects

Everything is represented by immutable engineering objects.

Examples include

Module

String

Table

MPPT

Inverter

Power Block

Plant

Route

Segment

Receipt

No browser object is authoritative.

---

# 7. Data Flow

Engineering proceeds in one direction.

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

Physics never creates geometry.

Validation never changes topology.

The browser never recalculates receipts.

---

# 8. Geometry

Geometry is the physical truth.

Geometry describes

location

orientation

rotation

spacing

dimensions

support structure

ducts

containment

routes

Geometry contains no electrical assumptions.

---

# 9. Topology

Topology describes connectivity.

It answers

What is connected?

Geometry answers

Where is it connected?

These two concepts remain independent.

Changing inverter position changes geometry.

It does not change topology.

Changing string assignment changes topology.

It does not necessarily change geometry.

---

# 10. Routing

Routing converts topology into physical conductors.

Routes consist of explicit segments.

Each segment records

start point

end point

length

installation method

containment

screening

burial

bonding

support system

These become inputs to later physics.

---

# 11. Physics

Physics is intentionally downstream.

It consumes geometry.

It never creates geometry.

Future modules include

resistance

voltage drop

fault current

capacitance

inductance

surge propagation

EMC

distributed transmission-line behaviour

Every result is derived from explicit conductor geometry.

---

# 12. Validation

Validation compares engineering against standards.

Examples include

IEC 62548

IEC TS 62738

IEC 61730

IEC 60364

Validation never changes the engineering model.

It reports compliance.

It does not redesign installations.

---

# 13. Engineering Receipts

Every authoritative calculation produces evidence.

Receipts contain

geometry hash

topology hash

routing hash

calculation hash

equipment profile

kernel version

validation state

timestamp

Receipts allow complete engineering traceability.

---

# 14. Equipment Profiles

Equipment is never hard coded.

Every inverter is represented by a profile.

Every module is represented by a profile.

Every connector is represented by a profile.

This allows future hardware to be introduced without changing computational architecture.

---

# 15. Browser Technology

Current preferred technologies include

deck.gl

WebGL2

Apache Arrow

DuckDB

Flatbush

PMTiles

Three.js instancing where appropriate

These are implementation choices.

They are not architectural authority.

Should better rendering technology appear, only the presentation layer changes.

The kernel remains untouched.

---

# 16. Scaling

Large projects are built by replication.

Validated table

↓

Validated inverter block

↓

Validated power block

↓

Validated plant

The software should never require different algorithms simply because a project grows.

Scale is achieved through deterministic replication.

---

# 17. Failure Philosophy

The system fails safely.

Missing geometry blocks routing.

Missing routing blocks physics.

Missing physics blocks validation.

Missing validation blocks authoritative receipts.

Unknown information is never silently assumed.

---

# 18. Future Expansion

Future capabilities should plug into existing architecture rather than replacing it.

Expected future modules include

EMC

Lightning

Arc behaviour

Distributed transmission-line analysis

Digital twin integration

Protection optimisation

AI-assisted engineering review

None of these should require redesign of the kernel.

---

# 19. Architectural Invariants

The following rules are immutable.

Geometry is authoritative.

Topology is independent of geometry.

Routing is explicit.

Physics is downstream.

Standards validate engineering.

Receipts are deterministic.

The browser never computes engineering.

The kernel is the single source of engineering truth.

---

# 20. Conclusion

The architecture deliberately separates engineering from presentation.

This allows every engineering discipline to build upon one canonical model.

Instead of maintaining independent geometry, electrical, compliance and visual representations, the platform maintains one authoritative engineering model.

Everything else becomes a projection of that model.

This architecture is expected to remain valid for the lifetime of the project and should not be altered unless a future design demonstrably strengthens engineering authority without compromising determinism.
