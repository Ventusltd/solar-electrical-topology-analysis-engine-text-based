# External Audit Access Reconciliation

Date: 2026-07-30
Branch: `main`
Repository: `Ventusltd/solar-electrical-topology-analysis-engine-text-based`

## Decision

The external feed is retained as an access-limited observation, not as repository authority.

Its central conclusion that current `main` has no Python engine, no V9/V10, no tests, no validation receipts and no public-API manifest is false for the repository state visible through the authenticated GitHub connector.

## Current verified paths on `main`

The following paths have been fetched directly from the repository during the current build sequence:

- `src/solar_topology/__init__.py`
- `src/solar_topology/circuit.py`
- `src/solar_topology/circuit_validation.py`
- `src/solar_topology/formulas.py`
- `src/solar_topology/public_api.py`
- `src/solar_topology/study_registry.py`
- `tests/test_diagnostics_and_studies.py`
- `v10-development/recovery/validation/V10_VALIDATION_LATEST.json`
- `v10-development/recovery/RECOVERY_POINT_2026-07-30_POST_REGISTRY_REPAIR_AND_NEXT_BUILD_ORDER.md`
- `v10-development/recovery/AUTONOMOUS_RESPAWN_202607301522.md`
- `v10-development/recovery/BUILD_022_INDEPENDENT_CAPABILITY_AUDIT.md`
- `v10-development/recovery/BUILD_023_CANONICAL_OBJECT_AND_TOPOLOGY_CONTRACT.md`

The repository metadata also identifies `main` as the default branch.

## Verified implementation facts

Current Python source includes:

- canonical physical objects, terminals, connections and circuit models;
- independent structural validation;
- ordered circuit traversal;
- evidence, diagnostics, persistence and study registries;
- temperature-corrected DC resistance;
- cold-string Voc;
- two-wire inductance and capacitance;
- characteristic impedance and propagation velocity;
- stored magnetic and electric energy;
- uncertainty and calculation receipts;
- deterministic public-API classification.

The current validation history includes machine-readable receipts recording Python, V8, V9 and V10 JavaScript test results.

## Why the external feed diverged

The feed itself records that it relied on unauthenticated rendered pages of a noindex repository and that commit, branch, raw, tree and several file endpoints were blocked. It therefore observed only a partial historical browser-facing surface.

Rendered GitHub page extraction is not authoritative for this repository because dynamic directory trees, noindex behaviour and robots restrictions can hide current paths and commits.

## Binding rule

Repository authority is determined in this order:

1. authenticated repository file fetch;
2. exact commit contents;
3. current validation receipt;
4. recovery and contract documents;
5. rendered public browser pages only as a downstream observation.

External audits remain useful for identifying discoverability problems and stale public surfaces, but they do not override authenticated source evidence.

## Useful finding retained from the feed

The public browser-facing repository can present a misleading historical view to unauthenticated tools. A later reporting/browser build must therefore:

- expose the current engine architecture clearly from the root README;
- link directly to Python, V9, V10, tests and receipts;
- distinguish historical V6/V7/V8 workbenches from the authoritative engine;
- publish a compact current-state manifest that static crawlers can read without dynamic tree rendering.

This is assigned to Build 027 and Build 035.

## Current executable state

Build 023 remains active.

Continue structural invariant verification and testing. Do not divert into browser repair until canonical topology and kernel authority are complete.
