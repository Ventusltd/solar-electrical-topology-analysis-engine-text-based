# Work Card 003 — Cartridge Adapter and Ordered Traversal

## Status

Second executable V10 build slice after the canonical circuit foundation.

Restore point created before this slice:

- branch: `restore/2026-07-30-pre-v10-cartridge-adapter-traversal`
- commit: `2e14b87db26c6de0ad7d175135a1ef166a8b0717`

All implementation work is committed directly to `main` under the binding main-branch-only rule.

## Objective

Connect the established Python sequential and leapfrog cartridge chains to the canonical V10 physical-object, terminal and connection model without changing the source calculations, then verify the resulting electrical order independently from the generated graph.

## Deliverables

### `src/solar_topology/circuit_adapters.py`

- accepts exactly one validated cartridge string chain;
- preserves each `SegmentRow` as evidence-bearing object attributes;
- creates inverter, MPPT and string hierarchy objects;
- creates explicit logical node objects and terminals;
- creates one physical object with two terminals for every source segment;
- connects source nodes to segment terminals and represents segment continuity through a separate internal connection;
- preserves source geometry, conductor data, temperatures, connector values, feasibility, warnings and provenance;
- rejects mixed chains, duplicate source segment identifiers and inconsistent coordinates for a shared source node;
- records deterministic source-chain metadata and SHA-256 hash;
- provides direct sequential and leapfrog build helpers.

### `src/solar_topology/circuit_traversal.py`

- validates the canonical circuit before traversal;
- derives order from the terminal graph rather than record or browser order;
- requires exactly two declared circuit boundaries;
- rejects branches, extra endpoints, disconnected components, cycles or excess edges;
- requires every source `segment_id` to appear exactly once on an internal connection;
- consumes the complete connection graph from start to end;
- optionally compares the graph-derived segment order with an external expected sequence;
- returns deterministic ordered terminal, connection and segment identifiers.

### `tests/test_circuit_adapters.py`

- sequential cartridge adaptation;
- leapfrog cartridge adaptation;
- deterministic adaptation under reversed input records;
- preservation of source numerical values and evidence references;
- rejection of inconsistent source-node coordinates;
- rejection of mixed cartridge chains;
- independent branch detection even where base circuit validation passes;
- segment-order mismatch detection;
- disconnected-component detection.

## Authority decision

The Python cartridge segment schema remains the provisional source for existing sequential and leapfrog numerical behaviour.

The canonical circuit model owns physical objects, terminals and explicit connections.

The traversal verifier is logically separate from the adapter and derives order only from the resulting terminal graph.

No capability is promoted beyond provisional authority until the full baseline suite and independent verification receipt pass.

## Non-goals

This slice does not:

- change sequential or leapfrog geometry or numerical results;
- attach resistance, voltage-drop, loss, inductance or capacitance calculations to the circuit;
- reconcile the separate `topology.py` geometry model;
- create harness, common-bus or parallel-branch traversal;
- add standards compliance logic;
- change V6, V7, V8, V9 or the browser;
- treat generic inputs as approved project data.

## Declared invariants

- one adapter call represents exactly one topology, run, inverter, MPPT, string, cartridge version and source schema;
- source segment order remains contiguous and node-continuous;
- one source node has one consistent coordinate;
- every source segment becomes one physical segment object and one internal segment connection;
- source numerical fields remain unchanged in the canonical object attributes;
- start and end boundaries derive from the first and last source nodes;
- the canonical graph is one connected simple path for sequential and leapfrog strings;
- graph-derived segment order equals cartridge segment order;
- topology-dependent calculation remains forbidden after either circuit or traversal validation fails.

## Validation required

Run and record:

1. complete Python `pytest` suite;
2. V8 JavaScript regression test;
3. V9 deterministic engine test runner;
4. existing V10 JavaScript tests.

The build is not complete merely because the new focused tests pass.

## Exact next work after this slice

1. Produce the baseline execution receipt for Python, V8, V9 and V10.
2. Reconcile Python provenance vocabulary with the V10 evidence vocabulary.
3. Define the canonical ordered-circuit result contract.
4. Attach complete-circuit resistance and loss only through validated graph traversal.
5. Add known-answer and cross-language comparison receipts before authority promotion.
6. Keep the browser last.
