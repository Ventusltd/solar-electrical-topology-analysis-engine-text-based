# Refinement 05 — Packaging, Legacy Reconciliation and Release Governance

Timestamp: 2026-07-31 19:30 +0100

## Purpose

The repository now contains several useful generations of the engine, but their authority boundaries are not sufficiently visible. A passing legacy suite can still present a result that appears to contradict the current Build 025 accounting, while the flagship Build 025 modules are not yet part of the normal installable package.

This refinement establishes one production authority chain while preserving older versions for reproducibility.

## V8 and Build 025 reconciliation

V8 reports an external or field-installed cable saving by comparing the home-run arrangement. Build 025 adds the factory-fitted interconnect consequence and reports total circuit conductor.

For the current 24 by 30 reference fixture, the accepted interpretation is:

```text
field-installed conductor:
sequential 1710.144 m
leapfrog    911.856 m
change     -798.288 m

factory-fitted conductor:
sequential  803.184 m
leapfrog   1648.272 m
change     +845.088 m

total circuit conductor:
sequential 2513.328 m
leapfrog   2560.128 m
change      +46.800 m
```

These values mean leapfrog materially reduces EPC-installed cable while increasing total conductor in this fixture. Neither statement cancels the other.

V8 shall therefore be refined as follows:

- rename any unqualified `cable saving` to `field-installed external cable reduction`;
- display the ownership and scope boundary beside the result;
- add a warning that factory-fitted interconnect length is excluded from the V8 quantity;
- link or reproduce a Build 025 reconciliation panel showing total circuit conductor;
- prevent the V8 result from being promoted as total copper saving;
- retain the historical V8 calculation and tests for reproducibility.

A legacy test passing means that the historical implementation remains reproducible. It does not make that implementation the current engineering authority.

## Canonical authority chain

The repository shall identify one current authority chain:

```text
geometry receipt
-> string membership receipt
-> topology receipt
-> physical input allocation receipt
-> routing receipt
-> installed/procurement length receipt
-> standards or physics calculation receipt
-> report/export receipt
```

The browser is an editor and renderer. It shall not independently recompute authoritative quantities.

The JavaScript V10 prototype, packaged Python kernel and root-level Build 025 modules shall not remain three competing production authorities. Their status shall be declared as:

```text
reference
prototype
candidate
canonical
superseded
```

## Package structure

Move the Build 025 authority into the installable `src/solar_topology` package. A suitable target structure is:

```text
src/solar_topology/array/
    geometry.py
    assignment.py
    topology.py
    input_allocation.py
    route_types.py
    route_geometry.py
    routing.py
    installed_length.py
    engine.py
```

Root-level modules may remain temporarily as compatibility shims that import and re-export the packaged implementation. They shall contain no independent formulas or logic.

The package configuration shall explicitly identify the source layout and included packages. Package discovery shall not depend on the repository working directory being present on `sys.path`.

## Clean installation gate

Add a CI job that:

1. builds a wheel and source distribution;
2. installs the wheel into a clean environment;
3. changes to a temporary directory outside the repository;
4. imports the public Build 025 API;
5. runs the reference 24 by 30 comparison;
6. verifies deterministic receipt hashes or approved golden values;
7. confirms no import resolves from the repository root;
8. runs a minimal exported-report generation.

An editable install alone is insufficient because it can conceal undeclared root-level imports.

## Module refinement

Large modules shall be divided before Build 027 introduces further physics. Refactoring shall preserve public behaviour and receipt hashes unless a deliberate method-version change is recorded.

Priority candidates include:

- topology construction versus topology validation;
- route construction versus geometric metrics;
- intersection and winding-area algorithms;
- installed-length policy and procurement rounding;
- payload serialisation and hashing;
- reference-fixture creation versus public orchestration.

The objective is not a line-count target by itself. The objective is that each module has one coherent authority responsibility and can be independently tested.

## CI requirements

Authoritative workflows shall run on both pull requests and protected-branch updates where appropriate. Path filters must not allow a dependency change to bypass relevant tests.

Required visible gates:

```text
syntax and import
unit and invariant tests
legacy reproducibility tests
Build 025 geometry and routing tests
exact-uncertainty regression
clean wheel installation
cross-language fixture comparison
public-page authority and warning checks
receipt determinism
```

The current head shall expose successful GitHub checks rather than relying only on a committed validation receipt.

## Release and branch governance

Calculation-authority changes should be developed through reviewable branches and pull requests. Direct commits to `main` may remain available for emergency recovery documentation, but formula, schema and receipt changes should normally require:

- a calculation-change note;
- source and evidence references;
- deterministic tests;
- an explicit method or schema version decision;
- review of changed public outputs;
- successful required status checks.

High-frequency validation receipts should be consolidated where possible. A receipt commit is useful when it establishes a meaningful restore point, not when it obscures the substantive history.

## Public version presentation

The repository and browser landing pages shall display a version-status matrix such as:

```text
V6  reference: ideal-bulk complete-string prototype
V7  reference: array overview and route visualisation
V8  reference: field-installed external-cable comparison
V9  reference/candidate: inverter-block sandbox and deterministic tests
V10 canonical candidate: evidence-bound topology, routing and receipt kernel
```

The exact labels shall follow the release state. No legacy page shall be described as canonical merely because its tests pass.

## Build sequence after documentation

The recommended implementation sequence is:

1. numerical-stability correction and tests;
2. V8 scope annotation and reconciliation output;
3. packaged Build 025 migration with compatibility shims;
4. clean wheel-install CI gate;
5. evidence-bound resistance registry and legacy warning updates;
6. evidenced terminal and three-dimensional geometry;
7. Build 027 electromagnetic source and flux models;
8. protected release candidate with visible required checks.

## Acceptance gate

This refinement is complete only when:

1. V8 explicitly reports field-installed scope and no longer implies total copper saving;
2. Build 025 is importable from the installed package outside the repository root;
3. root-level modules contain no independent authority logic;
4. one canonical public API and authority chain are documented;
5. GitHub exposes required passing checks on the release commit;
6. legacy versions remain reproducible but are visibly classified as non-canonical where applicable.
