# Build Receipt 009 — Contradiction Register

Date: 2026-07-30
Branch: `main`
Pre-build recovery commit: `0989c5e9f4db87b8936cf8fe684c06441a3e5af2`

## Scope

Add an immutable, deterministic register for conflicts between evidence-bearing engineering claims.

## Delivered

- canonical claims bound to subject identifiers, predicates, values, units and source identifiers;
- contradiction severity and lifecycle status;
- validation that claims concern the same subject, predicate and unit but contain different values;
- mandatory resolution notes for closed items;
- duplicate claim-pair rejection;
- deterministic JSON and SHA-256 hashing;
- unresolved contradiction filtering by minimum severity;
- focused contract tests;
- public package exports.

## Engineering boundary

The register records disagreement without deciding which source is correct. Resolution remains a separate evidence and verification act. Confidential source content is not copied into the record; only controlled source identifiers are stored.

## Validation status

Focused tests were authored but not executed by the GitHub connector. No fresh pass is claimed in this receipt.
