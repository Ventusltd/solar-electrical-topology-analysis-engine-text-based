# Quantum Spawn

**Title:** Mission and Philosophy

**File:** `202607311609-mission-and-philosophy.md`

**Timestamp:** 2026-07-31 16:09 (Local)

**Version:** 1.0

**Status:** Canonical

**Authority:** Engineering Design Authority

**Supersedes:** None

**Superseded By:** None

**Dependencies:** None

**Referenced By:** All subsequent Quantum Spawn modules.

**Current Build:** Build 025

---

# 1. Purpose

This document is the first module of the Quantum Spawn engineering authority.

It is intended to completely reload the architectural philosophy of the Solar Electrical Topology Analysis Engine into a future engineering discussion or future AI instance without requiring access to previous conversations.

This document is not a conversation log.

It is not meeting minutes.

It is not project documentation.

It is the engineering philosophy that governs every future design decision.

Whenever implementation decisions conflict with convenience, this document takes precedence.

---

# 2. Mission

The project exists to create the world's first deterministic, geometry-authoritative engineering computation engine for photovoltaic DC systems.

The objective is not simply to calculate electrical quantities.

The objective is to model physical reality sufficiently accurately that electrical behaviour naturally emerges from the geometry rather than being approximated from simplified assumptions.

The finished platform should be capable of predicting installation quantities, electrical performance, protection behaviour, standards compliance, surge behaviour, EMC characteristics and engineering evidence from one canonical model.

Everything begins with geometry.

---

# 3. The Problem with Existing Software

Nearly every PV design package begins from an electrical abstraction.

Designers specify:

- module count
- strings
- inverter
- cable size

The software then estimates cable lengths.

Those estimates become voltage drop.

Voltage drop becomes protection.

Protection becomes compliance.

Reality is introduced only at installation.

This workflow is backwards.

A cable does not exist because Ohm's Law requires it.

A cable exists because somebody physically installed it between two physical objects.

Electrical engineering cannot be separated from physical geometry.

The industry has largely ignored this relationship.

This project does not.

---

# 4. Reality Before Standards

Engineering exists independently of standards.

Physics existed before IEC.

Standards document accepted engineering practice.

They do not define physical behaviour.

The computational engine therefore models reality first.

Standards become validation layers applied afterwards.

For example:

The software does not route cables according to IEC.

The software routes cables according to geometry.

It then evaluates whether the resulting installation satisfies IEC 62548.

That distinction is fundamental.

---

# 5. Geometry Before Physics

The project adopts one immutable principle.

**Physics cannot be computed until geometry exists.**

Everything downstream depends on physical placement.

Examples include:

- cable resistance
- voltage drop
- fault current
- loop inductance
- surge coupling
- magnetic field
- capacitive coupling
- installation quantity

Without conductor routes these quantities are only estimates.

The kernel therefore refuses to calculate physics from imaginary cable lengths.

---

# 6. Deterministic Engineering

Engineering must be repeatable.

Identical inputs shall produce identical outputs.

Every authoritative computation therefore generates deterministic objects and deterministic receipts.

Receipts include:

- geometry hash
- topology hash
- calculation hash
- equipment profile
- kernel version
- validation status

The purpose is complete engineering traceability.

Nothing should depend upon user interface state.

Nothing should depend upon browser behaviour.

Nothing should depend upon execution order.

---

# 7. Browser Philosophy

The browser exists to present engineering information.

It is not an engineering engine.

The browser shall never:

- estimate cable lengths
- create topology
- calculate voltage drop
- compute EMC
- validate standards
- optimise routes

Instead it renders geometry supplied by the kernel.

This architecture guarantees that engineering authority exists only once.

---

# 8. Kernel Authority

The Python kernel owns:

- geometry
- topology
- routing
- validation
- physics
- optimisation
- receipts

Future additions including EMC modelling, surge analysis and transmission-line calculations also belong exclusively within the kernel.

The browser is intentionally computationally incapable of replacing the kernel.

---

# 9. Canonical Object Hierarchy

Every calculation originates from physical objects.

The hierarchy is:

Module

↓

String

↓

Table

↓

Inverter

↓

Power Block

↓

Plant

Every engineering quantity ultimately traces back to individual module placement.

Nothing bypasses this hierarchy.

---

# 10. Engineering, Not Graphics

The project deliberately avoids becoming another CAD package.

Three-dimensional graphics are valuable only when they improve engineering accuracy.

The canonical representation remains engineering geometry.

Height is introduced only when it materially changes calculations.

The browser visualises engineering.

It does not invent it.

---

# 11. Whole-Table Computation

The first authoritative computational boundary is a complete table.

The initial production target is:

- 24 strings
- 30 modules per string
- 720 modules

The engine must support arbitrary string layouts, arbitrary MPPT allocation and movable inverter locations.

Sequential and leapfrog routing are geometry-generation strategies operating on the same physical table.

Changing routing changes geometry.

Geometry changes physics.

---

# 12. Installed Reality

The project models installed systems rather than theoretical systems.

Cable length therefore exists in three forms.

Geometric length.

Installed length.

Procurement length.

Each is independently receipted.

Engineering decisions should never rely on hidden allowances.

---

# 13. Future Standards

Standards are layered onto the geometry.

Current priorities include:

- IEC 62548-1:2023
- IEC TS 62738
- IEC 61730
- IEC 60364
- IEC 61643

The standards engine validates geometry.

It never generates geometry.

Future revisions of standards must therefore require updates only to the validation layer rather than to the underlying computational model.

---

# 14. Research Philosophy

Every major architectural decision should be supported by engineering evidence.

Research conclusions become design rules only after they are technically justified.

The project values measured engineering over convention.

Where existing industry practice conflicts with physical reality, the model follows physical reality and records the standards implications separately.

---

# 15. Project North Star

The ultimate objective is to create a deterministic computational model that predicts the behaviour of an installed photovoltaic DC system directly from its physical arrangement.

Geometry produces topology.

Topology enables physics.

Physics enables validation.

Validation produces engineering evidence.

Engineering evidence supports decisions.

Every future build should strengthen this sequence.

No future feature should weaken kernel authority, duplicate engineering logic outside the kernel, or replace physical modelling with assumptions for the sake of convenience.

This document is therefore the philosophical foundation upon which every subsequent Quantum Spawn module is built.
