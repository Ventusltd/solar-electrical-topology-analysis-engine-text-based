# Build Receipt 008 — Public Topology Evidence Manifest

Date: 2026-07-30
Status: Implemented on `main`; execution validation pending

## Recovery point

Pre-build immutable commit:

`ea5471fc2d824e577e0ddb9625e5d51131ac0752`

No branch or pull request was created.

## Scope

This build adds a deterministic public topology manifest that binds canonical engineering identifiers to explicitly public evidence sources.

## Delivered

- `src/solar_topology/public_topology.py`
- `tests/test_public_topology.py`
- package-level API exports

## Boundary enforced

A public topology record is rejected when:

- it references an unknown evidence source;
- any referenced source is confidential, internal-only or otherwise restricted;
- it belongs to a different canonical project;
- source identifiers or attributes are non-deterministic;
- duplicate canonical identifiers occur.

The module intentionally contains no Employer's Requirements, SLD content or NDA-derived project facts.

## Outputs

- deterministic manifest payload;
- canonical compact JSON;
- SHA-256 manifest hash;
- sorted public source register.

## Validation declaration

Five focused tests were added but have not been executed by this connector session. No pass count is claimed until a runner records it.

## Next bounded build

Build 009 should add a contradiction register linking claims, sources and resolutions, followed by persistence only after its deterministic laws are established.
