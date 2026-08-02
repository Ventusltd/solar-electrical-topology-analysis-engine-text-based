# Quantum Spawn

**Title:** Build 026 — Coherence Recovery and 300-Second Operator Protocol

**File:** `202608021544-build-026-coherence-recovery-and-operator-protocol-chatgpt.md`

**Timestamp:** 2026-08-02 15:44 Europe/London

**Version:** 1.0

**Status:** Product Owner-requested coherence plan committed before execution; execution remains pending explicit Product Owner instruction

**Prepared against repository head:** `db66e290b80e0615177d31740c702e0c6070c0b0`

**Governing predecessor:** [`202608011536-build-026-forty-pass-small-step-law.md`](202608011536-build-026-forty-pass-small-step-law.md)

**Machine plan:** [`../../build-plans/build-026-continuity-and-model-repair.json`](../../build-plans/build-026-continuity-and-model-repair.json)

**Execution ledger:** [`../build-ledger/202608-continuity-and-model-repair.md`](../build-ledger/202608-continuity-and-model-repair.md)

**B026-07 receipt:** [`../../evidence/build-026/B026-07.json`](../../evidence/build-026/B026-07.json)

**Authority boundary:** This Quantum Spawn records the reviewed coherence defects, corrected control model, corrected remaining-unit scopes and exact execution sequence. It does not by itself mark B026-07 passed in the machine plan, advance the programme to B026-08, alter programme state, change engineering calculations, or authorise any unit after B026-08.

---

## Product Owner instruction converted into operating law

The Product Owner requires work to occur in short, bounded launches because long AI sessions can hang, exhaust context, blur completed and incomplete work, and create uncertainty about what reached the repository.

The operating model is therefore:

> work for no more than 300 seconds, hard-stop, report exactly what happened and what did not, review with the Product Owner, then launch the next bounded session from repository evidence.

The 300-second session is a safety and supervision boundary. It is not automatically one of the forty final Build 026 passes.

This distinction is required to preserve the original twenty-unit and forty-pass law while allowing a unit to be developed over several short sessions.

---

# 1. Reconstructed repository state

At the preparation head, B026-07 has three distinct layers of completion:

1. implementation and focused tests merged through PR 78;
2. the full validation and clean-wheel gates passed through workflow run `30750263458` and artefact `8834225463`;
3. the verified machine receipt merged through PR 79 at `db66e290b80e0615177d31740c702e0c6070c0b0`.

The repository also records:

- implementation merge: `744d85e22fc2b505a535e40e376b0d6f2a101f76`;
- implementation branch head: `3df03958a76a14e7692997f4d07f391eb456f53e`;
- artefact digest: `sha256:22dd20c85918ee01b1ff021482e0275264190720e12b2303c75ca6b588104ca5`;
- merge-test SHA: `d9c3e1fbff0f29e231763218a9196ca3ad4f793c`;
- Python suite: 390 passed;
- focused root-hygiene test count: 11 generated-path checks, one tracked-file integrity gate and one clean-tree gate, totalling 13 tests;
- V8, V9, V10 JavaScript and clean-wheel gates passed.

The implementation and receipt exist, but the authority surfaces remain out of sync:

| Surface | Current repository statement |
|---|---|
| B026-07 receipt | B026-07 completed; B026-08 next |
| Build 026 machine plan | B026-07 still planned and next |
| `programme-state.json` | B026-07 still next |
| README and dashboard | B026-07 still next |
| execution ledger | ends at B026-06 |
| current Quantum Spawn pointer | points to completed TS-005 autopilot document |
| Build 026 predecessor Quantum Spawn header | says Build 026 is not yet activated |

The repository is therefore incomplete but not corrupted. The engineering result is present and evidenced. The coherence seal has not been completed.

## Current ruling

B026-08 is not yet authorised.

B026-07 becomes fully closed only when the machine plan, ledger, programme state and deterministic public projections agree with the already merged implementation and receipt.

---

# 2. Corrected control vocabulary

## 2.1 Operator session

An operator session is one supervised period of work lasting no more than 300 seconds.

An operator session:

- begins from an authenticated repository head;
- has one narrow objective;
- may finish incomplete;
- hard-stops at or before 300 seconds;
- reports completed work, incomplete work, changed repository state, tests performed, pending CI, problems found and the safest next launch;
- requires Product Owner review before the next launch;
- does not by itself advance the programme;
- does not automatically count as a BUILD PASS or TEST PASS.

Each future receipt should record:

- `operator_session_count`;
- `operator_session_elapsed_seconds`;
- session objectives and outcomes;
- final BUILD PASS duration;
- final TEST PASS duration.

## 2.2 BUILD PASS

A BUILD PASS is the final acceptance event proving that the entire declared build scope for one unit exists on the review branch.

Only one final BUILD PASS counts for each unit.

Preparatory operator sessions are not additional BUILD PASS events.

## 2.3 TEST PASS

A TEST PASS is the final repository-controlled validation event proving that the unit acceptance conditions passed.

Only one final TEST PASS counts for each unit.

## 2.4 Programme arithmetic retained

- operator sessions: variable in number, each no more than 300 seconds;
- final BUILD PASS events: exactly 20;
- final TEST PASS events: exactly 20;
- final programme passes: exactly 40;
- no final BUILD PASS or TEST PASS exceeds 300 seconds;
- no unit advances until both final passes are recorded.

---

# 3. Authority hierarchy

The programme authority chain is:

1. code and tests define implemented behaviour;
2. CI artefacts prove an execution result;
3. machine receipts record the result and provenance;
4. the Build 026 machine plan grants permission to begin the next unit;
5. `programme-state.json` projects current programme authority;
6. README, dashboard and V11 communicate that state;
7. the append-only ledger explains execution history.

A lower layer may not contradict a higher layer.

A receipt may report what passed, but the next unit does not become authorised until the machine plan advances.

README, dashboard and V11 are presentation layers. They may explain authority but may never create it.

---

# 4. Immediate coherence recovery unit

The next repository action is one ordinary PR from current `main`:

`governance/build-026-coherence-seal`

It must not be stacked on another branch. It must not use a workflow that writes its own commits. It must not begin B026-08 implementation.

## Exact purpose

1. seal B026-07;
2. reconcile every Build 026 authority surface;
3. formalise the operator-session versus final-pass distinction;
4. correct the remaining-unit descriptions to match the code already present;
5. add one durable Build 026 control gate;
6. authorise B026-08 and nothing beyond it.

---

# 5. Exact coherence PR scope

## 5.1 Machine plan

File: `build-plans/build-026-continuity-and-model-repair.json`

Required changes:

- advance the Build 026 plan schema to `globalgrid2050.solar-dc.build-plan.v2`;
- mark B026-07 BUILD PASS as passed;
- mark B026-07 TEST PASS as passed;
- bind both passes to `evidence/build-026/B026-07.json`;
- set `next_unit` to `B026-08`;
- retain `active_unit: null` until B026-08 is explicitly launched;
- add the operator-session protocol;
- retain exactly twenty units and forty final passes;
- move resolved Product Owner decisions out of `reserved_decisions`;
- preserve the existing unit identifiers and order;
- refine B026-08 through B026-20 descriptions without changing their ordinals.

Proposed machine field:

```json
{
  "operator_protocol": {
    "session_limit_seconds": 300,
    "review_required_after_every_session": true,
    "session_advances_programme": false,
    "session_counts_as_build_or_test_pass": false,
    "final_build_passes_required": 20,
    "final_test_passes_required": 20,
    "final_pass_compute_limit_seconds": 300
  }
}
```

Resolved decisions should include:

- Product Owner designation of the current Trueself applied in B026-06;
- GPL-3.0 selected by the Product Owner and present in both repositories.

The remaining reserved decision is:

- authorisation of any programme after B026-20.

## 5.2 Execution ledger

File: `docs/build-ledger/202608-continuity-and-model-repair.md`

Append one B026-07 section. Do not rewrite earlier records.

The record must include:

- origin head `deef5545996dc068e054e6cb14204d30541ffe61`;
- implementation branch `build/07-deliberate-gitignore`;
- build commits `6f32324e`, `06e45cf9` and `3df03958`;
- implementation PR 78;
- workflow run `30750263458`;
- artefact `8834225463`;
- artefact digest `sha256:22dd20c85918ee01b1ff021482e0275264190720e12b2303c75ca6b588104ca5`;
- merge-test SHA `d9c3e1fbff0f29e231763218a9196ca3ad4f793c`;
- implementation merge `744d85e22fc2b505a535e40e376b0d6f2a101f76`;
- receipt merge `db66e290b80e0615177d31740c702e0c6070c0b0`;
- 11 generated-path checks;
- one tracked-file integrity gate;
- one clean-tree gate;
- 390 Python tests;
- wider V8, V9, V10 JavaScript and clean-wheel passes;
- no tracked file removed;
- no engineering calculation, topology or equipment value changed;
- B026-08 as the sole next unit.

## 5.3 Programme state

File: `programme-state.json`

Change only the fields required to report current programme truth.

Proposed values:

- `programme_stage`: `B026-07 root repository hygiene completed; clean installation and start contract next`;
- `current_quantum_spawn`: `docs/quantum-spawn/202608011536-build-026-forty-pass-small-step-law.md` until this coherence Quantum Spawn is formally selected during the seal, after which the current pointer may be this file if the Product Owner chooses;
- `active_gate`: `Build 026 — Active`;
- `next_single_goal`: `B026-08 — One clean installation and one start command`.

Preserve:

- package version;
- reference inverter block;
- capabilities;
- known unresolved equipment evidence;
- TS-005 canonical engineering validation baseline;
- comparison hash.

The TS-005 validation record must not be silently replaced by the B026-07 infrastructure run. Public presentation must label it as the canonical engineering baseline rather than implying it is the latest repository execution.

## 5.4 Predecessor Build 026 Quantum Spawn

File: `docs/quantum-spawn/202608011536-build-026-forty-pass-small-step-law.md`

Required changes:

- version `1.1` to `1.2`;
- status updated from not activated to active since B026-06;
- add the operator-session versus final-pass distinction;
- retain the forty-pass arithmetic;
- retain stable B026-01 through B026-20 numbering;
- record B026-07 complete and B026-08 next;
- clarify that derived values retain derivation identity and source lineage while never claiming support stronger than their weakest required inputs.

This coherence Quantum Spawn remains the detailed execution briefing. The predecessor remains the compact governing law.

## 5.5 Deterministic public projections

Regenerate:

- `README.md`;
- `progress-dashboard.html`.

Change the presentation labels:

- `Last validated engineering commit` to `Canonical engineering baseline commit`;
- `Latest declared validation envelope` to `Canonical engineering baseline validation`.

This explains why TS-005 validation remains visible while Build 026 infrastructure work progresses.

## 5.6 Existing tests to update

Files:

- `tests/test_programme_state.py`;
- `tests/test_ts005_handoff.py`.

The tests must prove:

- TS-005 remains completed historical authority;
- Build 026 is the current active programme;
- the current Build 026 Quantum Spawn exists;
- B026-08 is the sole next goal;
- programme state and generated public outputs remain byte-synchronised.

The TS-005 handoff test must no longer require the current active gate to begin with `TS-005`.

## 5.7 New Build 026 control test

Add:

`tests/test_build026_control.py`

It must verify:

1. Build 026 plan schema is v2;
2. there are exactly twenty units;
3. unit IDs are exactly B026-01 through B026-20;
4. ordinals are exactly 1 through 20;
5. test identifiers are unique;
6. every final pass limit is 300 seconds;
7. passed units form one contiguous prefix;
8. planned units form the remaining suffix;
9. `next_unit` is the first planned unit;
10. every passed unit references an existing receipt;
11. receipt unit ID, ordinal and title match the plan;
12. receipt BUILD PASS and TEST PASS are passed;
13. receipt `next_permitted_unit` matches the following unit;
14. the ledger contains every passed unit;
15. programme-state next goal matches the plan;
16. programme-state current Quantum Spawn matches the selected Build 026 spawn;
17. operator sessions do not increment the forty final passes.

## 5.8 Workflow triggers

File: `.github/workflows/v10-validation.yml`

Add these paths under both pull-request and `main` push triggers:

```yaml
- "build-plans/**"
- "docs/build-ledger/**"
- "evidence/build-026/**"
```

Do not create a second validation workflow. Do not create a workflow that commits its own results.

---

# 6. Corrected interpretation of remaining units

The unit identifiers, ordinals and order remain unchanged.

## B026-08 — One clean installation and one start command

Existing foundation:

- the local authority bridge already exists;
- it supports port zero;
- it prints the actual bound host, port and Studio URL;
- the installed package has no console entry point;
- Studio assets currently remain checkout assets rather than wheel assets.

Correct scope:

Add one checkout-backed installed command, proposed as:

`solar-topology-studio --port 0`

The command must:

- locate a compatible repository checkout;
- invoke the existing authority bridge;
- reuse Python-owned calculations;
- print the actual Studio URL;
- fail clearly outside a compatible checkout;
- make no claim that the wheel independently contains the Studio.

Acceptance:

A clean archived checkout can create an isolated environment, install the package, invoke one documented command, read the printed URL, receive `ready` from `/health`, load the Studio and terminate the service cleanly.

## B026-09 — Quantity-kind typing

Existing foundation:

`QualifiedValue` already carries value, unit, evidence class, verification state, source reference, source revision and note. It lacks quantity kind.

Correct scope:

- add `QuantityKind`;
- attach it to relevant qualified values;
- add unresolved inverter operating-current and short-circuit-limit fields;
- update deterministic serialisation;
- enumerate hash changes;
- add no comparison behaviour.

## B026-10 — Comparison compatibility guard

Correct scope:

Add an explicit comparison function requiring:

- compatible quantity kinds;
- compatible units;
- stated comparison conditions;
- a named source limit.

The unit prevents a future software form of the unlike-rating reasoning error. It must not claim Python rich-comparison behaviour caused the original prose error.

## B026-11 — Versioned datasheet evidence fixture

Existing foundation:

The equipment contract and evidence register already exist.

Correct scope:

Extend those contracts rather than creating a parallel provenance system.

Before execution, the Product Owner must designate:

- exact module model;
- exact module datasheet revision;
- exact inverter model;
- exact inverter datasheet revision.

The fixture records:

- document identity;
- revision and date;
- source location;
- PDF SHA-256;
- every promoted field;
- evidence class;
- verification state.

## B026-12 — Rear-gain current screening

Dependencies:

- B026-09 quantity kinds;
- B026-10 comparison compatibility;
- B026-11 evidence fixture.

Correct scope:

- load values only from the fixture;
- keep Imp and Isc channels separate;
- calculate margin;
- retain source identity;
- return unresolved where evidence is absent;
- emit no unsupported compliance, clipping or thermal verdict.

## B026-13 — Evidence-class monotonicity

Existing foundation:

The repository already contains an evidence-strength mapping and `weakest_evidence_class()`.

Correct scope:

Audit and repair propagation semantics rather than creating a greenfield helper.

A derived output must:

- retain that it is derived;
- retain source lineage;
- state the weakest required input support;
- never claim stronger verification than its weakest required input.

Do not blindly collapse all provenance categories into one total ordering. Begin with exhaustive table-driven tests rather than introducing a property-testing dependency merely because the old scope mentioned property-based tests.

## B026-14 — Cold open-circuit voltage with explicit method

Existing foundation:

`cold_string_voc()` already performs the basic linear calculation.

Correct scope:

Build an evidence-qualified method and receipt around the existing formula:

- explicit temperature case;
- explicit tolerance policy;
- no default tolerance;
- source-bound inputs;
- reproducible method identity;
- monotonic temperature test;
- no automatic compliance verdict.

## B026-15 — String-group module-profile binding

Current inverter-block authority binds one equipment contract across the whole block.

Correct scope:

Use the resolution chain:

`project default → string-group override → string override`

The narrowest declared scope wins. The receipt records the source of every binding. A profile change affects only its own receipt branch.

## B026-16 — Per-pole factory-lead lengths

Existing foundation:

Positive and negative factory-lead fields already exist but remain unresolved and are not consumed by routing.

Correct scope:

- bind both fields to the datasheet fixture;
- consume them in installed-length calculations;
- preserve each pole separately;
- enumerate every changed receipt hash.

## B026-17 — Declared slack and coil geometry

Existing foundation:

Installed-length policy already contains `service_loop_m_per_route`, currently defaulting silently to zero.

Correct scope:

- replace silent zero with declared, explicitly absent or unresolved state;
- record straight, looped or coiled geometry state;
- add slack to conductor length only where declared;
- avoid inventing inductance from unevidenced geometry.

## B026-18 — Named assumption register

Correct scope:

Create a register without seeding assumptions merely because they appeared in discussion.

Every entry requires:

- ID;
- statement;
- owner;
- status;
- evidence;
- review date;
- references from dependent receipts.

B026-14 remains coherent before B026-18 only because its temperature and tolerance choices are explicit inputs rather than standing hidden defaults.

## B026-19 — Governance contradiction gate

Existing foundation:

The repository already has deterministic `Claim`, `Contradiction` and `ContradictionRegister` objects.

Correct scope:

- reuse that core;
- add structured governance claim documents;
- compare only named and typed claims;
- require explicit supersession;
- do not extract supposed facts from arbitrary prose.

## B026-20 — Snapshot expiry and verdict vocabulary gates

Snapshot validity must bind:

- repository;
- commit;
- path or object;
- content hash;
- observed statement;
- rule determining whether it is still presented as current.

Commit ancestry alone is insufficient.

Verdict vocabulary should use a repository-local Python validator. No Vale dependency is required.

---

# 7. Standard execution model after coherence repair

Every remaining unit uses no more than two substantive PRs.

## PR A — Build

Contains:

- implementation;
- focused tests;
- necessary documentation;
- strictly necessary workflow trigger changes.

It may require several reviewed 300-second operator sessions.

It merges only after the full declared validation envelope passes.

## PR B — Seal

Contains together:

- machine receipt;
- ledger entry;
- machine-plan advancement;
- programme-state advancement;
- generated README/dashboard projections;
- state and control tests.

There is no separate receipt-only PR, no stacked PR and no self-writing workflow.

---

# 8. Product Owner review checkpoints

The Product Owner reviews after every 300-second operator session, but there are only three constitutional decision types.

## Scope checkpoint

Before repository changes:

- exact objective;
- exact expected files;
- prohibited surfaces;
- starting head;
- intended acceptance test.

## Build checkpoint

Before merging PR A:

- complete diff;
- focused test result;
- full CI result;
- changed hashes;
- unresolved findings.

## Seal checkpoint

Before merging PR B:

- receipt;
- ledger;
- plan advancement;
- public-state projection;
- exact next unit.

Intermediate operator sessions report progress but do not create new constitutional decisions.

---

# 9. Syntactic sugar and load-bearing authority

## Syntactic sugar

Useful but not authoritative:

- branch names;
- PR titles;
- Markdown table styling;
- dashboard colours;
- friendly aliases wrapping commands;
- short unit titles;
- PASS badges;
- historical branch cleanup;
- whether several commits are used inside one coherent PR.

## Controlled presentation

Required to stay synchronised but not itself calculation authority:

- README programme block;
- progress dashboard;
- V11 status cards;
- human ledger wording.

## Load-bearing

- unit identifiers and order;
- build and test scope;
- 300-second boundaries;
- operator-session versus final-pass distinction;
- receipt identities;
- CI artefact identities;
- machine-plan `next_unit`;
- plan and programme-state consistency;
- evidence provenance;
- quantity kinds;
- comparison compatibility;
- explicit unresolved states;
- workflow triggers covering authority files;
- Build 026 control tests.

Governing rule:

> syntactic sugar may explain, shorten or display authority; it may never create authority.

---

# 10. Exact execution sessions after Product Owner approval

No execution begins until the Product Owner states `execute`.

## Session C01 — branch boundary

Maximum duration: 300 seconds.

- authenticate current `main`;
- create `governance/build-026-coherence-seal`;
- record the exact starting SHA;
- make no content changes;
- hard-stop and report.

## Session C02 — machine plan

Maximum duration: 300 seconds.

- amend the Build 026 plan to v2;
- seal B026-07;
- add the operator-session protocol;
- refine B026-08 through B026-20 descriptions;
- hard-stop and report.

## Session C03 — ledger and governing law

Maximum duration: 300 seconds.

- append the B026-07 ledger record;
- update the predecessor Build 026 Quantum Spawn to v1.2;
- hard-stop and report.

## Session C04 — public programme state

Maximum duration: 300 seconds.

- update `programme-state.json`;
- regenerate README and dashboard;
- update programme-state and TS-005 handoff tests;
- hard-stop and report.

## Session C05 — durable control gate

Maximum duration: 300 seconds.

- add `tests/test_build026_control.py`;
- add workflow paths for plan, ledger and evidence;
- run focused governance tests;
- hard-stop and report.

## Session C06 — one coherence PR

Maximum duration: 300 seconds.

- inspect the complete diff;
- open one PR;
- start CI;
- hard-stop if CI remains pending.

## Session C07 — validation and merge

Maximum duration: 300 seconds.

- inspect CI and retained artefact;
- repair only an understood coherence failure within scope;
- otherwise merge the exact tested head;
- confirm B026-08 is the sole next unit;
- hard-stop and report.

No B026-08 implementation begins during the coherence recovery sequence.

---

# 11. Completion conditions for coherence recovery

The coherence recovery is complete only when:

- B026-07 is marked passed in the machine plan;
- the ledger contains B026-07;
- programme state reports Build 026 active and B026-08 next;
- README and dashboard are deterministic projections of that state;
- the selected current Quantum Spawn is a Build 026 document rather than the completed TS-005 autopilot document;
- Build 026 control tests pass;
- workflow path filters cover Build 026 plan, ledger and evidence;
- exactly twenty final BUILD PASS events and twenty final TEST PASS events remain required;
- operator sessions are explicitly excluded from the forty-pass arithmetic;
- the full declared validation and clean-wheel gates pass;
- B026-08 and no later unit is authorised.

This Quantum Spawn is the restart point for the coherence recovery work. Conversation is disposable. The repository and its evidence remain authoritative.