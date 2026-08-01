# Trueself

**Title:** Study and Repair the Continuity Defects Before Product Work

**File:** `202608011401-study-and-repair-continuity-defects-trueself-ChatGPT.md`

**Timestamp:** 2026-08-01 14:01 Europe/London

**Version:** 2.0

**Status:** Current ChatGPT continuity-defect repair control; engineering-programme activation remains pending machine-state reconciliation

**Authority:** Explicit Product Owner instruction to identify, study and repair the defects in the preceding ChatGPT Trueself, interpreted against authenticated repository state and the completed TS-005 evidence chain

**Supersedes:** `202608011316-lead-engineer-inverter-studio-continuity-trueself-ChatGPT.md` as the active ChatGPT continuity instruction

**Does Not Supersede:** `programme-state.json`, `microbuild-plan.json`, deterministic engineering receipts, tests, workflow artefacts, manufacturer source documents, the TS-005 closure or later explicit Product Owner instruction

**Dependencies:**
- `../../programme-state.json`
- `../../microbuild-plan.json`
- `20260801-ts-005-authoritative-slice-closure.md`
- `202608011225-part-ii-quantum-spawn-authenticity-audit.md`
- `202608011316-lead-engineer-inverter-studio-continuity-trueself-ChatGPT.md`
- `../quantum-spawn/202607311609-mission-and-philosophy.md`
- `../quantum-spawn/202607311615-system-architecture.md`
- `../quantum-spawn/202607311619-geometry-authority.md`
- `../quantum-spawn/202608010120-amnesia-resilience-and-continuity-law.md`
- `../quantum-spawn/202608010151-bounded-observation-and-truncation-law.md`
- `../quantum-spawn/202608010240-microbuild-continuity-and-product-visibility-law.md`

**Confidentiality Boundary:** No confidential third-party construction drawing, project identity, site identity, private capacity, drawing reference, route length, contract detail or reconstruction from private construction evidence may enter the public repository. Public manufacturer evidence may be recorded with exact source provenance. Private photographs may be represented only by controlled non-identifying evidence handles, hashes and custodial references.

---

## 1. Purpose

This file instructs a future ChatGPT or other builder model to study and repair the defects in the preceding Trueself before beginning user-facing Studio development.

The preceding file contains valuable engineering synthesis, the correct product boundary, a verified repository load order and important manufacturer and field observations. It is not discarded. It is superseded as the active control because it declared a new programme authorised while the machine programme state still said that the next controlled programme had not been defined; it described a programme too broad to be one active tranche; it relied on manufacturer and photographic evidence without an independently reloadable evidence register; and it compared module short-circuit current with an inverter operating-input-current rating too conclusively.

These are continuity and evidence defects. They are not permission to reopen the constitutional architecture or to discard the engineering findings. The first future model shall repair the defects explicitly and preserve the valid content.

The repository remains the court of evidence. This file states the repair obligation. It does not declare that the repair has already happened.

## 2. Present machine-state conflict

At the time this repair instruction was written, `programme-state.json` still declared:

- `active_gate`: `TS-005 — Complete`;
- `next_single_goal`: `Define the next controlled programme`;
- `current_trueself`: `docs/trueself/20260801-ts-005-authoritative-slice-closure.md`.

The preceding ChatGPT Trueself said that the next controlled programme was authorised and described eight stages. Because it also stated that it did not supersede `programme-state.json`, the prose and machine authority disagreed.

A future model must not silently choose one. It must first inspect the current `main` head, current programme state, current Trueself pointers, current tests and latest required workflow results. It must then reconcile the conflict through one explicit, reviewable change.

The preferred resolution, subject to current evidence and Product Owner instruction, is to define a named programme for the Working Inverter Studio while activating only one bounded first tranche. The machine programme state should then identify the new current Trueself, the programme name, the active tranche and its single next goal. If current repository evidence makes activation unsafe, the model must instead leave TS-005 terminal state intact, mark this repair control as pending activation and report the blocking evidence.

No future model may claim that programme activation is complete merely because this file exists.

## 3. Defect register

### Defect D1 — prose and machine authority disagree

The prior Trueself authorised work that `programme-state.json` had not activated.

**Required repair:** inspect and reconcile `programme-state.json`, its schema, generated README/dashboard projections, current Trueself pointer and any tests binding these fields. The repair must state whether the new programme is activated or remains pending, and why.

### Defect D2 — the active work unit is too broad

The prior Trueself combined validation repair, `.gitignore`, startup documentation, directory classification, equipment-profile redesign, new electrical inputs, project-command generalisation and editable Studio work into one authorised programme section. This is a valid roadmap but not one bounded builder tranche.

**Required repair:** preserve the roadmap, but activate only the first coherent tranche. The first tranche should be limited to establishing current repository truth and a clean entry path. It may include resolving any red or unexplained required validation state, adding a deliberate root `.gitignore`, and documenting one clean installation and startup path. It must not also change equipment schemas, calculation methods, receipt semantics or the browser product.

### Defect D3 — manufacturer and photographic evidence is not reloadable

The prior Trueself named two public datasheets and first-hand photographs as evidence but did not provide exact controlled identifiers, source locators, revisions, hashes or private evidence handles.

**Required repair:** create or identify a non-confidential evidence register that distinguishes governance authority from technical evidence. It shall record, where accessible and legally permitted:

- exact inverter manufacturer and model or a controlled public profile identifier;
- exact public datasheet title, version 19 and 2023 revision identity;
- exact module manufacturer and model;
- exact public datasheet title and `2024_A` revision identity;
- public source locator or controlled repository reference;
- document hash where a controlled copy exists;
- a non-identifying private photographic evidence-set identifier;
- image hashes or a manifest hash;
- evidence custodian and access boundary;
- the exact nameplate-image identifier supporting the module-profile match.

If the source files or photographs are unavailable to the future model, it must record failed access and leave the evidence link incomplete. It may not reconstruct source identity from numerical values alone.

### Defect D4 — unlike current ratings were compared too conclusively

The arithmetic in the prior Trueself is correct: two published module short-circuit currents are 36.9 A at front-side standard conditions, 38.74 A at the published five per cent rear-gain case and 40.6 A at the published ten per cent rear-gain case.

The forty-ampere inverter figure is described as maximum PV input current, while the directly corresponding published short-circuit-current ceiling is sixty amperes per MPPT. A comparison between module `Isc` and an inverter operating-input-current rating is a useful screening signal but is not yet a definitive compatibility conclusion.

**Required repair:** retain the arithmetic and revise the conclusion. The corrected interpretation shall say that the ten per cent rear-gain `Isc` screening value exceeds the published forty-ampere maximum PV input-current figure, while remaining below the sixty-ampere short-circuit limit. Before issuing a definitive compatibility result, the model must establish the manufacturer’s exact rating definitions and the corresponding rear-gain maximum-power current or other applicable design-current method. Rear-side gain remains a first-class electrical input because it consumes current headroom; the final pass/fail rule remains evidence-dependent.

### Defect D5 — repository observation needs an explicit date and head boundary

The prior Trueself referred to current authenticated inspection without binding that statement to an inspection date and repository head.

**Required repair:** record the exact current `main` head inspected, the inspection date and the status of required checks. Distinguish the latest documentation head from the last fully validated engineering commit. Do not present historical TS-005 evidence as validation of later code changes.

### Defect D6 — legal and hygiene facts must be rechecked rather than inherited

At the preceding inspection, no root `LICENSE` and no root `.gitignore` were found. These are bounded observations at that time, not eternal facts.

**Required repair:** recheck both paths on the current head. A future model may add a deliberate `.gitignore` within the first bounded tranche after understanding tracked and generated artefacts. It may not select, add or announce an open-source licence autonomously. Licence choice and confirmation of Ventus Ltd’s rights to release remain reserved to the Product Owner and company-level decision. The model may prepare a decision note and identify third-party, confidential or licensed-standards risks.

## 4. Mandatory study order

The first future model shall study the defects before editing. The minimum order is:

1. `programme-state.json` and its schema;
2. `microbuild-plan.json` and the TS-005 closure;
3. the preceding ChatGPT Trueself;
4. this defect-repair Trueself;
5. the latest `main` head and required workflow checks;
6. `.github/workflows/v10-validation.yml`;
7. `scripts/run_v10_validation.py`;
8. the latest generated validation JSON and Markdown reports;
9. `scripts/check_capsule_links.py`;
10. `scripts/sync_programme_state.py` and its tests;
11. any existing evidence registry, manufacturer-profile source files or controlled source references;
12. only the tests and implementation files directly implicated by a discovered failure.

Do not load the entire repository before identifying the current defect boundary. Do not dump the multi-megabyte authority bundle into model context. Inspect its schema, validator output, targeted fields and hashes.

## 5. First authorised repair tranche

The only active work authorised by this file is continuity and clean-entry repair.

### Goal

Make the repository’s prose control, machine programme state and present validation status agree, while creating a reproducible entry path for the next builder.

### Permitted changes

The tranche may change:

- the current Trueself and programme-state pointer;
- `programme-state.json`, its schema, synchroniser and directly related tests;
- capsule-link references and directly related tests;
- validation repair files only where a currently reproduced failure requires them;
- a root `.gitignore` after tracked/generated classifications are understood;
- one concise clean-install and startup instruction;
- a non-confidential manufacturer/private-evidence register or its schema.

### Prohibited changes

The tranche must not change:

- authoritative geometry, topology or routing behaviour;
- resistance, voltage-drop, loss or uncertainty methods;
- deterministic receipt semantics or method versions;
- equipment-profile values beyond documentation/evidence references needed to repair the register;
- the authority-response schema;
- the local bridge product behaviour;
- Authority Studio functionality;
- standards, EMC or lightning calculations;
- licence choice or licence text.

### Acceptance

The repair tranche passes only when:

- the current `main` head and latest required checks are stated exactly;
- any red or unexplained required validation state is reproduced and either repaired or explicitly recorded as blocking;
- the programme state and current Trueself pointer agree;
- only one bounded active tranche is named;
- the evidence register identifies accessible public sources and controlled private evidence without disclosing confidential project information;
- the bifacial-current conclusion is qualified correctly;
- capsule-link and programme-state drift gates pass;
- the full declared validation envelope passes for the changed state;
- both clean installed-wheel gates pass;
- the handback states every unresolved defect and the Product Owner decision required next.

If the full envelope cannot pass, do not activate the product programme. Leave the repair tranche open and record the exact failure.

## 6. Product target preserved but not yet active

The intended later product remains one inverter-centred DC block with twelve MPPT control groups, two physical string inputs per MPPT, twenty-four strings, thirty modules in series per string, 720 modules, 475.2 kWp DC and forty-eight external inverter terminations.

The later roadmap remains valid in principle: exact module profiles below whole-project level; cold-voltage cases; rear-side current gain; separate positive and negative factory leads; declared slack geometry; a validated project command; and one editable Authority Studio workflow returning Python-owned receipts.

None of that product work begins under this file. It begins only after the continuity repair tranche passes and the Product Owner or reconciled machine programme state activates the next tranche.

## 7. Required handback from the future model

The future model shall return:

- the inspected `main` head;
- the last fully validated engineering commit;
- the latest required workflow result;
- the exact defects confirmed, rejected or newly discovered;
- the branch and pull request used for repair;
- every file changed;
- focused test results;
- full validation and both clean-wheel results;
- the revised programme-state fields;
- the evidence-register identifiers created or still missing;
- the corrected bifacial-current interpretation;
- confirmation that no confidential evidence entered the public repository;
- the single next decision reserved to the Product Owner.

The model must distinguish what it inspected, what it inferred and what it could not access.

## 8. Stop conditions

Stop and report rather than continue when:

- current repository state cannot be authenticated;
- workflow output is truncated or inaccessible;
- the public datasheets cannot be identified exactly;
- private photograph evidence cannot be accessed or hashed;
- programme-state reconciliation would require inventing Product Owner intent;
- a required test remains red for an unexplained reason;
- a proposed change would alter engineering authority outside the permitted tranche;
- a licence decision is required.

Failed access is not absence. A plausible source identity is not a verified source. A passing focused test is not a passing integration envelope.

## 9. Enduring instruction

Study the defects before fixing them. Fix the continuity system before building the product. Preserve valid engineering content while correcting authority, scope and provenance.

The prior Trueself was not wrong in its mission. It was premature in its activation, too broad in its work unit, incomplete in its evidence reload chain and too definite in one rating comparison. The next model must make those distinctions executable.

Precision is not authority. The physical system is the only thing that does not negotiate.
