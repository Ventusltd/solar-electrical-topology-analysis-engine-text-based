# Quantum Spawn

**Title:** Microbuild Continuity and Product Visibility Law

**File:** `202608010240-microbuild-continuity-and-product-visibility-law.md`

**Timestamp:** 2026-08-01 02:40 Europe/London

**Version:** 1.0

**Status:** Canonical

**Authority:** Product Owner direction interpreted through the existing geometry-authoritative architecture

**Supersedes:** No engineering architecture

**Refines:**
- `202608010120-amnesia-resilience-and-continuity-law.md`
- `202608010151-bounded-observation-and-truncation-law.md`

**Dependencies:**
- `202607311609-mission-and-philosophy.md`
- `202607311619-system-architecture.md`
- `202607311624-geometry-authority.md`
- `../trueself/202608010104-complete-352-kva-inverter-block-plan.md`
- `../trueself/202608010226-ts-003-exact-equipment-contract-authority.md`

**Restore Point:** `restore/2026-08-01-0240-pre-microbuild-law`

---

## 1. Purpose

The programme has repeatedly attempted work units that were too long for one reliable context window.

The consequence was predictable:

- implementation began;
- validation, documentation and programme updates accumulated behind it;
- context was lost before closure;
- the next intelligence had to reconstruct an unfinished chain;
- more writing was produced to compensate for the risk of forgetting.

This law changes the unit of work.

The project shall continue through short executable microbuilds while Quantum Spawn and Trueself carry only the logic required to preserve direction.

## 2. Memory allocation

The repository shall use four different memory mechanisms for four different purposes.

### Quantum Spawn

Quantum Spawn records only durable mission, architecture and operating law.

It shall not be used as a diary of ordinary implementation steps.

### Trueself

Trueself records the current execution plan, present boundary, completed integration checkpoints and exact next action.

One active Trueself execution file may cover several microbuild commits.

A new Trueself file is required when a material integration goal passes, the active goal changes or the current plan is superseded.

### Code and tests

Code and tests record implementation truth.

A passed focused test is better implementation memory than a prose description of what the code was intended to do.

### Commit history and validation artefacts

Commits record the ordered microbuild sequence.

CI and clean-wheel artefacts record integration proof.

The project shall not duplicate all of this implementation history into long capsules.

## 3. Microbuild definition

A microbuild shall:

1. change one explicit contract or behaviour;
2. normally touch no more than three implementation or test files;
3. introduce no second unresolved dependency;
4. have one focused acceptance test;
5. end in a committed, reloadable state;
6. fit within one active reasoning context.

A microbuild is not a material programme build and does not require a new Quantum Spawn or Trueself capsule.

Several microbuilds may form one material integration goal.

## 4. Required cycle

Each microbuild follows:

```text
Goal
→ Build
→ Focused test
→ Commit
→ stop or select the next listed microbuild
```

Each material integration goal follows:

```text
Completed microbuilds
→ full declared validation
→ clean installed-wheel validation
→ concise Trueself checkpoint
→ programme-state update
→ next integration goal
```

A failed focused test stops the current microbuild only.

A failed full validation stops the integration goal.

No later feature begins while the current integration goal is red.

## 5. Context-loss stop rule

When remaining context, tool state or repository state becomes uncertain, the intelligence shall not begin another change.

It shall stop at the latest committed microbuild and state only:

- current head;
- completed microbuild;
- focused test result;
- exact next microbuild;
- any known failure.

The next intelligence must be able to continue from that five-line state plus the active Trueself plan.

## 6. Documentation budget

Ordinary implementation shall not generate long checkpoint prose.

A normal passed integration checkpoint should contain only:

- Goal;
- Build;
- Test;
- Result;
- unresolved facts;
- next goal.

Long-form capsules are reserved for mission, architecture, evidence corrections or a genuinely new reasoning law.

The quality standard remains stone-carved recoverability, not stone-carved length.

## 7. Product visibility law

The project has one engineering authority and two legitimate interface modes.

### Playground mode

Playground mode may calculate locally in the browser for exploration.

It must be visibly labelled:

```text
INDICATIVE — NON-AUTHORITATIVE
```

It may not issue engineering receipts, standards conclusions or compliance claims.

Its calculations are not regression authority for the Python kernel.

### Authority mode

Authority mode may display only Python-owned outputs, evidence states and receipt hashes.

It shall not recalculate authoritative routes, lengths, resistance, voltage drop, loss, fault current, EMC, lightning or standards conclusions in JavaScript.

The same Studio may contain both modes if their state and outputs are clearly separated.

The playground is a user-experience laboratory, not a competing engineering engine.

## 8. Vertical product priority

After the current inverter-block aggregate is closed, the next visible product goal shall be one narrow authoritative Studio slice.

The first slice shall load or request the complete reference inverter block:

```text
660 Wp bifacial modules
30 modules per string
24 strings
720 modules
475.2 kWp DC
352 kVA inverter block
```

It shall render kernel-owned geometry, routing, physical-input allocation, evidence gaps and hashes.

It shall display unresolved MPPT mapping, internal DC topology, reverse-current blocking and PCE backfeed as unresolved.

It shall not wait for those later evidence questions before proving the kernel-to-screen path.

## 9. Immediate integration sequence

The active material goal remains:

```text
TS-004 — Complete inverter-block aggregate and receipt
```

TS-004 is divided into:

```text
TS-004.1  Explicit provisional public-API classification
TS-004.2  Clean-wheel inverter-block probe
TS-004.3  Full validation and compact checkpoint
```

The next material goal becomes:

```text
TS-005 — First authoritative Studio slice
```

TS-005 is divided into:

```text
TS-005.1  One local command returning reference-block JSON
TS-005.2  One committed response bundle and schema
TS-005.3  Authority-mode Studio renders the bundle without calculations
TS-005.4  Local bridge replaces the committed bundle
TS-005.5  End-to-end reference-block validation
```

Physical-input-to-MPPT evidence completion follows the first visible slice rather than blocking it.

## 10. Protection of prior work

This law does not weaken:

- geometry authority;
- Python engineering authority;
- evidence provenance;
- deterministic receipts;
- restore points;
- focused tests;
- full integration validation;
- clean-wheel verification;
- compatibility preservation.

It changes only the size of the implementation unit and the amount of prose attached to it.

## 11. Final instruction

Build the smallest next contract.

Test it immediately.

Commit it before beginning the next contract.

Use Quantum Spawn and Trueself to preserve logic, not to reproduce the repository in prose.

Make the product visible as soon as one truthful vertical path exists.
