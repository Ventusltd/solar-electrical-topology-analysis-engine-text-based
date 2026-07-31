# Refinement 07 — Build 025.5 Implementation Status

Timestamp: 2026-07-31 21:30 +0100

## Purpose

This file records implementation progress against `202607312059-build-025-5-authority-consolidation.md`. It is a status receipt for the refinement programme, not a replacement for the governing Build 025.5 requirements.

## Completed implementation

### 025.5A — V8 truth boundary

Implemented on `main`.

V8 now identifies itself as a historical/reference field-installed external-cable comparison. It no longer presents its result as total copper saving. The public page displays together:

- field-installed conductor reduction;
- factory-fitted conductor increase;
- total circuit conductor change;
- absolute winding-area reduction;
- plan-coordinate and unresolved-terminal evidence limitations.

A dedicated reconciliation module and Node regression tests preserve the Build 025 reference values and prevent the external-cable result from being promoted as complete-circuit performance.

### Execution-envelope separation

Implemented on `main`.

Routine validation no longer creates GridBot commits containing mutable timestamps and command output. GitHub Actions now retains commit-specific validation artifacts. The committed `V10_VALIDATION_LATEST` files are repository pointers rather than claims about the latest execution.

The validation workflow has read-only repository permission and preserves execution evidence separately from deterministic engineering receipts.

### 025.5B — Installable Build 025 authority

Implementation migration completed on `main`.

The Build 025 modules now live under:

```text
src/solar_topology/array/
```

The supported API is:

```python
import solar_topology.array
```

Repository-root module names remain compatibility imports only. Their implementation bodies were copied into the package by exact Git blob identity before the root files were replaced with shims.

The package initialiser loads dependencies in a declared order and maps legacy module names to the same packaged module objects. Existing callers therefore retain compatibility without creating a second implementation authority.

Tests now enforce that:

- legacy and packaged imports resolve to identical module objects;
- public classes and functions retain identity;
- root compatibility files contain no independent authority logic;
- source-layout compatibility files included in the wheel also contain no independent authority logic;
- the reference 24 by 30 accounting remains unchanged.

### 025.5C — Clean wheel gate

Gate implemented on `main`.

The project version is now `0.4.0`. Setuptools is explicitly configured with the `src` package root, packaged Build 025 implementations and wheel-level compatibility modules.

The clean-wheel probe:

1. builds a wheel;
2. creates a new virtual environment;
3. installs the wheel outside the repository;
4. removes repository `PYTHONPATH` influence;
5. imports both the public package API and legacy module names;
6. proves that imports resolve inside `solar_topology/array` rather than the checkout;
7. executes the 24 by 30 comparison twice;
8. verifies deterministic hashes;
9. verifies the field-installed, factory-fitted and total-conductor reference values.

The probe is both a separate visible GitHub Actions job and a suite inside the consolidated validation execution envelope.

## Validation state

The code and workflow gates are committed. The authoritative execution result for any commit is its GitHub Actions check and commit-specific artifact named:

```text
v10-validation-<commit-sha>
```

This status file does not substitute for that execution evidence and does not claim a workflow result that has not been read from the exact commit artifact.

## Remaining Build 025.5 work

### 025.5D — Resistance evidence authority

Next implementation target.

Required outcome:

- controlled resistance-basis vocabulary;
- source and revision metadata;
- manufacturer nominal versus maximum distinction;
- standard-maximum and independently measured cases;
- temperature-coefficient evidence;
- deterministic resistance-evidence hashing;
- V10 receipt integration;
- visible ideal-bulk warnings in V6 and V9.

### 025.5E — Evidenced dimensional geometry

Pending after resistance authority.

### 025.5F — Electromagnetic quantity boundary

Pending after dimensional geometry.

## Next action

Implement `ResolvedConductorResistance` and its evidence registry in the packaged kernel, migrate existing `ConductorSpec` values into explicit evidence records, and add tests proving that resistance, voltage drop and loss track the selected evidence case without changing geometry or topology receipts.
