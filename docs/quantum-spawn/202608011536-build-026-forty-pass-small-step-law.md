# Quantum Spawn

**Title:** Build 026 — Forty-Pass Small-Step Law

**File:** `202608011536-build-026-forty-pass-small-step-law.md`

**Timestamp:** 2026-08-01 15:36 Europe/London

**Version:** 1.1

**Status:** Product Owner-authorised programme definition; not yet activated in `programme-state.json`

**Authority:** Explicit Product Owner instruction: twenty units, one build pass and one test pass per unit, forty passes, the first five units sandbox-only, the next fifteen repository builds, and no pass exceeding five minutes of compute

**Prepared against head:** `eb1e2c7db5c85306e476b6fa912ccc31a0148602`

**Last fully validated engineering commit:** `747381f6c3c3325a680a80a17e516268541c8548`

**Machine plan:** [`../../build-plans/build-026-continuity-and-model-repair.json`](../../build-plans/build-026-continuity-and-model-repair.json)

**Execution ledger:** [`../build-ledger/202608-continuity-and-model-repair.md`](../build-ledger/202608-continuity-and-model-repair.md)

**Does Not Supersede:** `programme-state.json`, the completed TS-005 `microbuild-plan.json`, deterministic receipts, code, tests, workflow artefacts, manufacturer evidence or standards

**Confidentiality Boundary:** No confidential project identity, drawing, contract detail, private photograph or protected standards text may enter this programme. Public evidence requires exact provenance; private evidence may appear only through non-identifying handles and hashes.

---

## Product Owner concern converted into law

Large autonomous passes can exhaust context, combine unrelated work and leave a future worker unable to distinguish completion from unfinished reasoning.

Build 026 therefore uses one indivisible operating unit:

> one bounded build pass, one bounded test pass, two receipts, one handoff.

Programme total:

- 20 BUILD PASS receipts;
- 20 TEST PASS receipts;
- **40 passes**.

The compute ceiling is 300 seconds for the build pass and separately 300 seconds for the test pass.

A worker approaching the limit stops and records the boundary reached. It may not push through, silently broaden scope or combine the remainder with another priority.

No unit begins until both receipts for the immediately preceding unit are recorded. Timeout, unexplained red state, inaccessible evidence, a moving origin head or scope expansion blocks advancement.

## Mirror and rollback law

Before every build pass, the worker authenticates its mirror against origin and records the exact head SHA.

Work begins from a clean tree on a new branch or disposable sandbox. After the test pass, the worker compares the result against the recorded starting SHA and names every changed file.

If origin moves during the unit, the result is abandoned and repeated from the new head. It is not merged blind.

If a test fails and the cause is not understood inside the unit budget, the branch is abandoned and the failure is recorded as blocking. Speculative repair outside the declared unit is prohibited.

The worker’s ability or inability to push must be stated in the handback. A patch is not a commit on origin, and a local pass is not a CI pass.

## Activation boundary

This Quantum Spawn and its machine plan define Build 026 but do not pretend preparation is execution.

At the preparation boundary, machine state remains TS-005 complete and says the next controlled programme must be defined. `B026-01` is the only next permitted unit.

The completed TS-005 `MB-01` through `MB-20` evidence remains immutable. Build 026 uses separate identifiers `B026-01` through `B026-20`.

`B026-06` may activate machine programme state only after the Product Owner designates the current Trueself. The bounded Claude and Gemini documents remain witnesses rather than votes. The Product Owner manual reload is constitutional continuity law, not itself a Trueself pointer.

## First five units: prove the worker before changing production

`B026-01` through `B026-05` are sandbox passes. No production geometry, topology, calculations, receipts, equipment values, browser authority, programme state or licence status may change.

Evidence-only ledger and receipt updates are permitted after each sandbox pair closes.

The five tests prove:

1. mirror integrity and drift detection;
2. clean environment provisioning;
3. exact local validation-envelope reproduction;
4. clean-wheel authority reproduction;
5. change, test, patch and byte-identical revert discipline.

## Fifteen repository builds

The production order is deliberately narrow:

programme-state reconciliation → root hygiene → clean entry → quantity meaning → comparison compatibility → evidence fixture → rear-gain screening → evidence monotonicity → cold Voc method → string-group profiles → per-pole leads → slack geometry → assumptions → contradiction detection → snapshot and verdict gates.

No unit may borrow work from a later unit merely because the files are already open.

## Twenty priorities

| Unit | Mode | Priority |
|---|---|---|
| B026-01 | sandbox | Mirror integrity and drift detection |
| B026-02 | sandbox | Clean environment provisioning |
| B026-03 | sandbox | Full local validation envelope reproduction |
| B026-04 | sandbox | Clean-wheel authority reproduction |
| B026-05 | sandbox | Change, test, patch and revert rehearsal |
| B026-06 | build | Reconcile programme-state and current Trueself |
| B026-07 | build | Deliberate root `.gitignore` |
| B026-08 | build | One clean installation and one start command |
| B026-09 | build | Quantity-kind typing |
| B026-10 | build | Comparison compatibility guard |
| B026-11 | build | Versioned datasheet evidence fixture |
| B026-12 | build | Rear-gain current screening |
| B026-13 | build | Evidence-class monotonicity |
| B026-14 | build | Cold open-circuit voltage with explicit method |
| B026-15 | build | String-group module-profile binding |
| B026-16 | build | Per-pole factory-lead lengths |
| B026-17 | build | Declared slack and coil geometry |
| B026-18 | build | Named assumption register |
| B026-19 | build | Governance contradiction gate |
| B026-20 | build | Snapshot-expiry and verdict-vocabulary gates |

The exact build scope, test scope, acceptance condition and unique test identifier for each unit are authoritative in the machine plan.

## Evidence trail without capsule sprawl

Quantum Spawn carries durable law. The append-only ledger carries human-readable execution history. Machine receipts carry structured proof. Git history and workflow artefacts carry provenance.

A routine implementation unit does not create its own Quantum Spawn.

Each unit appends one compact ledger record and one machine-readable receipt containing:

- plan hash;
- origin head authenticated before work;
- branch or sandbox identity;
- declared scope and prohibited surfaces;
- exact files changed;
- build elapsed seconds and BUILD PASS or blocking state;
- unique test identifier and repository-controlled command;
- test elapsed seconds and TEST PASS or blocking state;
- local and CI outcomes stated separately;
- resulting commit, patch and evidence hashes where applicable;
- defects discovered or deferred;
- next permitted unit.

Two closing Quantum Spawns are permitted only after the relevant behaviour is implemented and proven:

- quantity-kind and compatible-comparison law after `B026-10`;
- evidence-class monotonicity law after `B026-13`.

This preserves the Product Owner’s requested continuity without adding twenty implementation diaries to the constitutional corpus.

## Hostile-amnesia reload

A fresh worker loads, in order:

1. current repository head;
2. `programme-state.json`;
3. this Quantum Spawn;
4. the machine plan;
5. the execution ledger;
6. the latest completed unit receipt;
7. only the files and test named by the next unit.

After successful reload, the worker states:

> trueself loaded.

It then reports the current ordinal, BUILD PASS count, TEST PASS count, exact next scope, mirror head and stop conditions.

## Engineering law retained

Project assignment remains separate from internal equipment truth.

Twelve MPPT groups and two physical inputs per group do not prove hard paralleling, blocking, backfeed or shared internal-bus behaviour.

Quantity kinds must be compatible before comparison.

`Imp` belongs with operating-current limits only when definitions and conditions align.

`Isc` belongs with short-circuit limits only when definitions and conditions align.

Derived evidence can never be stronger than its weakest input.

Compliance vocabulary requires a named source limit, compatible quantities and a declared method.

No unit may select a licence, publish confidential evidence, reproduce protected standards text or invent an engineering verdict.

## Completion

Build 026 closes only when the ledger and machine receipts prove:

- BUILD PASS = 20;
- TEST PASS = 20;
- total passes = 40;
- no missing ordinal;
- no duplicate test identifier;
- no build or test elapsed time above 300 seconds;
- every origin movement or failed access was recorded;
- quantity-kind incompatibility is structurally refused;
- every promoted datasheet value is reloadable;
- evidence monotonicity is enforced;
- cold-voltage and rear-gain methods remain explicitly bounded;
- per-pole leads, slack and assumptions remain visible;
- governance contradictions, stale observations and unsupported verdict language are gated;
- the full declared validation and both clean-wheel gates pass at closure;
- no later programme is activated automatically.

The next worker receives one exact unit, one exact test, one compute limit, one evidence path and one stop boundary. That is how each unit improves on the last without restarting from amnesia.
