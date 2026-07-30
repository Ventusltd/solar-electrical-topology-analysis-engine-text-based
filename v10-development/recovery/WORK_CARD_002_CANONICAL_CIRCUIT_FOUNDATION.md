# Work Card 002 — Canonical Circuit Foundation

## Status

First executable V10 build slice after Pass 1 engine inventory.

This work card creates the physical-object, terminal and connection contract required before topology-dependent calculation. It does not promote the existing browser or JavaScript candidate kernel to engineering authority.

## Objective

Establish one deterministic, renderer-independent representation for:

- physical and logical engineering objects;
- globally identified terminals;
- explicit terminal-to-terminal connections;
- object hierarchy;
- evidence class and source reference;
- terminal coordinates where known;
- deterministic canonical serialisation and hashing;
- independent validation before later topology traversal or calculation.

## Authority decision for this slice

The Python package remains the provisional owner of the canonical headless circuit model.

`src/solar_topology/segments.py::Point3D` is reused as the provisional shared coordinate type so this slice does not introduce a third geometry representation. Its final ownership remains subject to the wider `segments.py` / `cartridges.py` / `topology.py` reconciliation.

The V10 JavaScript quantity and evidence interfaces remain migration sources. They are not used as the physical-circuit authority in this slice.

## Deliverables

1. `src/solar_topology/circuit.py`
   - versioned circuit schema identifier;
   - controlled object, terminal, connection and evidence vocabularies;
   - immutable `Terminal`, `PhysicalObject`, `Connection` and `CircuitModel` records;
   - deterministic canonical JSON independent of input record order.

2. `src/solar_topology/circuit_validation.py`
   - logically separate verifier;
   - duplicate object, terminal and connection detection;
   - terminal ownership validation;
   - terminal-reference resolution;
   - required-terminal and connection-capacity checks;
   - parent resolution and cycle detection;
   - finite coordinate and scalar metadata checks;
   - deterministic issue ordering;
   - SHA-256 authority hash available only after validation succeeds.

3. `tests/test_circuit.py`
   - complete two-module series-circuit fixture;
   - record-order-independent JSON and hash test;
   - unresolved terminal rejection;
   - global terminal-key uniqueness;
   - dangling required-terminal rejection;
   - terminal-capacity enforcement;
   - parent-cycle rejection;
   - non-finite coordinate rejection;
   - prohibition on hashing an invalid model.

4. Package exports through `src/solar_topology/__init__.py`.

## Declared invariants

- object identifiers are globally unique within a circuit model;
- terminal identifiers are globally unique within a circuit model;
- every terminal declares and is stored under the same owner object;
- every connection endpoint resolves to a declared terminal;
- a required terminal cannot remain unconnected;
- terminal connection count cannot exceed its declared capacity;
- object-parent references resolve and contain no cycles;
- duplicate connection identifiers and duplicate terminal pairs are rejected;
- terminal coordinates and numeric metadata are finite;
- canonical JSON and SHA-256 hash are independent of object and connection input order;
- an invalid model cannot receive a validated authority hash.

## Explicit non-goals

This slice does not yet:

- generate sequential, leapfrog, harness or common-bus topology;
- traverse the complete positive-to-negative circuit;
- calculate resistance, voltage drop, loss, inductance or capacitance;
- reconcile `topology.py` with `segments.py` and `cartridges.py`;
- encode standards compliance;
- define manufacturer-specific module, connector or inverter products;
- change V6, V7, V8, V9 or the existing V10 browser;
- claim that current generic defaults are approved project data.

## Validation receipt

The new focused test module was executed against a local package harness using the repository's existing `Point3D` contract.

Result:

```text
8 passed
```

The full repository Python, V8, V9 and V10 baseline suites remain a separate required receipt and must run on the landed branch before authority promotion.

## Acceptance criteria

This work card may close when:

- the focused circuit tests pass in the repository environment;
- the full existing Python suite remains green;
- object, terminal and connection records can represent a complete series circuit without a free total-length input;
- invalid topology foundation data fails before calculation;
- the canonical payload and hash remain deterministic under record reordering;
- review confirms that no browser or standards logic has entered the physical model.

## Exact next work after this slice

1. Build adapters from `SequentialCartridge` and `LeapfrogCartridge` segment chains into the canonical circuit model without changing their numerical behaviour.
2. Create a separate ordered-circuit traversal verifier.
3. Run and receipt the Python, V8, V9 and V10 baselines.
4. Reconcile provenance vocabularies.
5. Compare the canonical Python evidence fields against the V10 JavaScript quantity contract.
6. Promote capabilities individually only after independent verification.

## Governing rule

```text
Physical objects
→ terminals
→ explicit connections
→ independent validation
→ ordered topology
→ calculation
→ evidence
→ reports
→ browser
```

No topology-dependent calculation may proceed after a failed circuit validation.
