# Build Receipt 007 — Canonical Hierarchical Identifiers

Date: 2026-07-30
Status: Implemented on `main`; execution validation pending

## Recovery point

Pre-build immutable commit:

`acb66f3fae11ba7e451ce724a6f40327c6577a71`

No branch or pull request was created.

## Scope

This build establishes deterministic identifiers for the V10 engineering hierarchy:

`project / site / system / equipment / circuit / object`

## Delivered

- `src/solar_topology/identifiers.py`
- `tests/test_identifiers.py`
- package-level API exports

## Invariants

- identifiers begin at project level;
- hierarchy is contiguous and cannot skip levels;
- local tokens are lowercase kebab-case;
- complete identifier values are deterministic;
- parsing round-trips without information loss;
- complete identifiers must be unique;
- identical local tokens are permitted beneath different parents;
- confidential source names need not appear in canonical identifiers.

## Validation declaration

Seven focused tests were added but have not been executed by this connector session. No pass count is claimed until a runner records it.

## Next bounded build

Build 008 will introduce an evidence-bearing public topology manifest that binds canonical identifiers to public source records without importing Employer’s Requirements, SLD content or confidential project naming.
