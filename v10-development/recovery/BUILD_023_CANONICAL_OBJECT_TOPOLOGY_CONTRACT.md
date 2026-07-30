# Build 023 — Canonical Object and Topology Contract

Date: 2026-07-30
Branch: `main`

## Status

First contract-freeze increment complete. Numerical physics is unchanged.

## Canonical source modules

- `src/solar_topology/circuit.py` — physical objects, terminals, connections and deterministic payload.
- `src/solar_topology/circuit_validation.py` — independent structural validation.
- `src/solar_topology/circuit_traversal.py` — ordered circuit verification.
- `src/solar_topology/circuit_adapters.py` — compatibility conversion from segment chains.

## Frozen representation contract

### CircuitModel

A circuit is identified by `model_id` and contains immutable tuples of physical objects and connections. `schema_version` identifies the representation contract. Metadata is descriptive only and cannot create electrical connectivity.

### PhysicalObject

Every physical object has:

- one globally unique `object_id` within the model;
- one declared `ObjectKind`;
- zero or more owned terminals;
- optional parent identity;
- evidence class and optional source reference;
- deterministic scalar attributes.

An object cannot be electrically connected directly. All connectivity occurs through terminals.

### Terminal

Every terminal has:

- one globally unique `terminal_id` within the model;
- exactly one owning `object_id`;
- declared polarity;
- optional physical position;
- explicit connection requirement;
- explicit maximum connection count;
- evidence class and optional source reference.

Terminal position is geometry evidence. Absence of position does not invent a zero coordinate.

### Connection

Every connection has:

- one globally unique `connection_id`;
- one existing source terminal;
- one existing destination terminal;
- declared connection kind;
- optional segment identity;
- evidence class and optional source reference.

A connection records adjacency only. It does not imply route length, conductor product, resistance, polarity correctness or study acceptance.

## Frozen invariants

1. Object, terminal and connection identifiers are unique within the model.
2. Every terminal owner exists and agrees with the object that contains it.
3. Every connection endpoint exists.
4. A connection cannot join a terminal to itself.
5. Terminal connection count cannot exceed `max_connections`.
6. Required terminals without the required connectivity are validation failures.
7. Parent object references must resolve and cannot create parent cycles.
8. Attributes and metadata must use deterministic unique keys.
9. Canonical payload ordering is identifier-based and independent of input tuple order.
10. Model construction does not prove validity; independent validation is mandatory.
11. Ordered traversal does not trust builder order.
12. Branches, disconnected islands, repeated use and incomplete start-to-end traversal are explicit failures.
13. Topology validation blocks dependent calculations.
14. Segment identity cannot substitute for terminal connectivity.
15. Geometry, evidence and numerical calculation remain separate layers.

## Sequential and leapfrog cartridge invariants

Both cartridges must:

- include every declared module exactly once in electrical series order;
- create exactly one valid path between declared string boundary terminals;
- preserve terminal polarity and connector adjacency;
- create no hidden branch, loop or disconnected island;
- expose every field and factory-lead segment separately;
- produce deterministic identifiers and payloads for identical inputs.

The topology cartridge is not authoritative merely because it generated the model. The resulting circuit must pass independent validation and traversal.

## Authority rule

The authoritative topology artefact is:

```text
CircuitModel
+ non-blocking CircuitValidationResult
+ complete OrderedCircuitTraversal
+ deterministic model hash
```

No calculation may consume an unvalidated model as authoritative input.

## Compatibility boundary

`circuit_adapters.py` remains compatibility-only. Adapter output must satisfy the same independent validation as a natively constructed circuit. Legacy segment order, UI order or builder order is not accepted as proof.

## Remaining Build 023 increments

1. Verify the current validator covers every frozen invariant.
2. Add missing invariant tests without changing physics.
3. Add an independent topology-verification fixture for sequential and leapfrog cartridges.
4. Bind calculation entry points to a validated topology receipt.
5. Rebind public topology projection to the authoritative circuit hash.
6. Run complete validation and record a Build 023 restore point.

## Exact next executable task

Compare `circuit_validation.py` and `circuit_traversal.py` against the fifteen frozen invariants. Implement only missing structural checks and tests. Do not modify resistance, voltage, temperature, transient or standards calculations in that increment.
