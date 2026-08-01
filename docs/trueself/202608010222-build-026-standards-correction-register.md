# Trueself

**Title:** Build 026 Standards Correction Register

**File:** `202608010222-build-026-standards-correction-register.md`

**Timestamp:** 2026-08-01 02:22 Europe/London

**Version:** 1.0

**Status:** Active evidence correction and future implementation gate

**Authority:** Direct review of controlled primary standards material supplied by the Product Owner, reconciled against the canonical Quantum Spawn standards philosophy

**Supersedes:** Any external-feed or conversational claim inconsistent with this register

**Dependencies:**
- `../quantum-spawn/202607311609-mission-and-philosophy.md`
- `../quantum-spawn/202607311615-system-architecture.md`
- `../quantum-spawn/202607311619-geometry-authority.md`
- `../quantum-spawn/202607311624-array-engine.md`
- `../quantum-spawn/202607311627-physics-emc-lightning.md`
- `../quantum-spawn/202607311628-standards-validation.md`
- `../quantum-spawn/202607311652-respawn-instructions.md`
- `../quantum-spawn/202608010151-bounded-observation-and-truncation-law.md`
- `202608010104-complete-352-kva-inverter-block-plan.md`
- `202608010117-civilisational-consciousness-and-amnesia-covenant.md`

**Current Build Relevance:** Hard evidence gate before Build 026 standards implementation; no effect on Build 025 geometry, topology, routing, resistance, voltage-drop or loss authority

**Copyright Boundary:** This public record contains paraphrased engineering conclusions, document editions and clause locators only. It does not reproduce licensed standards text, tables or figures.

---

## 1. Purpose

This register prevents incorrect standards interpretations from entering Build 026 merely because they were previously stated confidently by an external research agent.

The relevant external feed later acknowledged that it had not read the supplied body of IEC 62548-1:2023 before publishing several claims. Direct review of the controlled source corrected those claims.

This document records the corrections independently of the originating conversation so a future AI instance cannot accidentally recover the retracted interpretation from an older summary and implement it as authority.

No engineering calculation is changed by this record.

## 2. Governing edition separation

The future validation engine shall treat the following as separate versioned authorities:

- IEC 62548-1:2023;
- IEC TS 62738:2018, including its explicit relationship to the older IEC 62548 edition against which it was written;
- IEC 60364-7-712:2017 where applicable;
- later amendments only after their exact text and effect are reviewed.

Rules from different editions shall not be blended into one anonymous IEC rule set.

When editions disagree, the engine shall expose the disagreement with document, edition, clause, inputs and result state.

## 3. Correction KI-01 — the 1.25 factor is inside K_I

### Retracted interpretation

```text
I_STRING_MAX = 1.25 × K_I × I_SC_MOD
K_I defaults to 1.0 for an ordinary monofacial case
```

This interpretation applies the 1.25 factor twice when `K_I` is already defined by the 2023 standard.

### Correct 2023 relationship

IEC 62548-1:2023 Annex F defines:

```text
I_STRING_MAX = K_I × I_SC_MOD
K_I = 1.25 × K_Corr
```

For a case where `K_Corr = 1.0`, the resulting `K_I` is 1.25.

### Build 026 guard

The standards implementation shall contain a test that rejects any formula equivalent to:

```text
1.25 × K_I × I_SC_MOD
```

when `K_I` is the Annex F quantity.

The receipt shall expose `K_Corr`, the universal 1.25 factor and the resulting `K_I` separately.

## 4. Correction KI-02 — no universal bifacial value of 1.125

### Retracted interpretation

A fixed bifacial default of `K_I = 1.125` or a generic bifacial multiplier of 1.125 was previously presented as standards authority.

### Correct 2023 treatment

For the applicable bifacial route, Annex F requires a correction based on the relationship between bifacial nameplate short-circuit current and ordinary module short-circuit current, or a project-specific simulation where required.

The public engine shall therefore require evidence for quantities such as:

```text
I_SC_MOD
I_SC_BNPI
bifaciality or rear-response basis
front and rear irradiance assumptions
simulation method and revision where used
```

Where rear irradiance can exceed the Annex F threshold under the stated front irradiance condition, simulation is mandatory rather than optional.

### Build 026 guard

The engine shall not derive 1.125 merely from the word `bifacial`.

The generic 660 Wp bifacial reference profile shall remain blocked or provisional for this calculation until the required current and installation evidence exists.

## 5. Correction KI-03 — K_Corr can decrease or increase current

### Retracted interpretation

`K_Corr` was described only as an uplift factor.

### Correct 2023 treatment

For non-optimally oriented monofacial arrays, Annex F provides a geometry-dependent route in which `K_Corr` may be below 1.0. The standard examples include materially reduced values for unfavourable orientation.

`K_Corr` is therefore bidirectional within its applicable method. It is not constrained by the engine to be at least 1.0.

### Build 026 guard

Tests shall reject:

- a lower bound of 1.0 imposed without authority;
- language describing every correction as an uplift;
- use of the orientation equation without the required geometric inputs and applicability state.

## 6. Correction KI-04 — cloud enhancement is not an extra hidden multiplier

Annex F identifies ordinary cloud-enhancement effects as covered within the case where `K_Corr = 1.0`, with the universal 1.25 factor incorporated through `K_I`.

Measured high-irradiance events may remain relevant to research, nuisance operation and the adequacy of standard safety factors. They do not authorise adding another concealed multiplier to the Annex F formula.

Any separate fuse-operation or nuisance-tripping consideration shall remain a separate rule with its own source and receipt.

## 7. Correction OCP-01 — no generic 2.4-times ceiling in IEC 62548-1:2023

### Retracted interpretation

The 2023 edition was described as retaining a generic upper fuse bound of `2.4 × I_SC`.

### Correct edition treatment

The 2023 string-protection interval is expressed using `I_STRING_MAX` and the module maximum overcurrent-protection rating. The former 2.4-times ceiling is not part of that 2023 interval.

IEC TS 62738:2018 discusses omission of the 2.4 multiplier because it was written against an older IEC 62548 edition.

### Build 026 guard

The rule registry shall prevent the 62738 historical statement from being injected into the 2023 rule set.

Each fuse interval shall carry its edition and clause identity.

## 8. Correction OCP-02 — protection triggers remain separate

IEC 62548-1:2023 evaluates the string fault-current neighbourhood together with total external backfeed, including power-conversion-equipment and other applicable sources.

IEC TS 62738:2018 uses an older parallel-string expression based on the number of strings and maximum string short-circuit current.

These are separate rule families.

A simple statement such as `three or more parallel strings require fuses` is not a substitute for the 2023 evidence model.

### Build 026 guard

The engine shall:

- model actual parallel nodes rather than infer them from an MPPT label;
- keep PCE backfeed explicit and evidence-qualified;
- keep battery or other external contributions explicit;
- report incomplete evidence where backfeed data is absent;
- never silently replace the 2023 trigger with the older string-count heuristic.

## 9. Correction SPD-01 — critical length has two IEC 62548-1:2023 cases

The confirmed 2023 critical-length relationships are:

```text
attached installation:     L_crit = 115 / N_g
non-attached installation: L_crit = 200 / N_g
```

A previously reported `450 / N_g` service or industrial case is not part of IEC 62548-1:2023 Table 5 and shall not be attributed to that table.

The counted `L` is the maximum routed distance between the power-conversion equipment and module connection points, excluding only route portions that satisfy the standard's qualifying buried or earthed metallic sheath, armour, screen or enclosure conditions.

### Build 026 guard

The diagnostic shall operate on explicit route segments.

It shall not:

- use straight-line site distance where routed geometry exists;
- exclude a complete route because one segment is buried or screened;
- credit a metallic screen without evidence of the required earthing or bonding condition;
- expose the `450 / N_g` case as an IEC 62548-1:2023 rule.

This remains one of the cleanest geometry-derived standards diagnostics available to the project.

## 10. Correction VOC-01 — cold-voltage arithmetic survives; evidence policy changes

The implemented crystalline-silicon temperature-coefficient relationship is algebraically compatible with the reviewed 2023 Annex F method when units are expressed consistently.

The future standards receipt must additionally identify the required temperature statistic and the selected low-irradiance treatment.

IEC 62548-1:2023 and IEC TS 62738:2018 use differing low-irradiance thresholds in their respective methods. The difference shall be reported as an edition conflict rather than silently harmonised.

Below the stated extreme-temperature boundary, or for technologies outside the supported crystalline method, manufacturer instructions become required evidence.

## 11. Correction CABLE-01 — no universal 1.4 × K_I string-cable rule

A later external-feed claim stated that every string cable requires a current rating of at least:

```text
1.4 × K_I × I_SC_MOD
```

That is not a universal IEC 62548-1:2023 string-cable requirement.

The 2023 cable-current requirement depends on the actual topology, protection state, reverse-current neighbourhood and external backfeed conditions. A 1.4 multiplier appears in other component contexts and shall not be transplanted into a blanket string-cable rule.

### Build 026 guard

Tests shall reject a universal string-cable rule of `1.4 × K_I × I_SC_MOD` unless a separately identified authority and applicable component context explicitly require it.

## 12. Current-engine consequence

These corrections do not alter the current authoritative implementation of:

- module placement;
- string topology;
- physical input assignment;
- explicit routing;
- conductor length;
- resistance;
- voltage drop;
- resistive loss;
- uncertainty;
- deterministic receipts;
- resistance-source qualification.

Build 025 and Build 025.5 remain valid within their declared scope.

The corrections affect planned Build 026 standards logic only.

## 13. Required Build 026 acceptance tests

Before Build 026 can claim the relevant rule family, tests shall prove that the engine rejects or distinguishes all of the following:

1. double application of the 1.25 factor;
2. a hard-coded bifacial value of 1.125;
3. a universal lower bound of `K_Corr = 1.0`;
4. a generic 2.4-times ceiling attributed to the 2023 edition;
5. blending the 2018 restricted-access trigger with the 2023 backfeed trigger;
6. implicit paralleling from shared MPPT labels;
7. silent zero PCE backfeed without evidence;
8. a `450 / N_g` case attributed to IEC 62548-1:2023 Table 5;
9. route-wide exclusion where only individual SPD-length segments qualify;
10. silent resolution of the differing low-irradiance thresholds;
11. a universal `1.4 × K_I × I_SC_MOD` string-cable rating rule;
12. a standards conclusion without document, edition, clause and evidence provenance.

## 14. Evidence and copyright discipline

The controlled primary documents may be used to verify algorithms and clause locators.

The public repository shall store:

- paraphrased rule meaning;
- document identifier and edition;
- clause or annex locator;
- algorithm version;
- provenance status;
- deterministic test fixtures created from permitted derived values.

The repository shall not store substantial licensed text, copied tables, copied figures or confidential project-report passages.

## 15. Final correction statement

External research feeds are useful discovery inputs, not engineering authority.

A confident citation does not compensate for failure to read the governing edition.

Build 026 shall be implemented only from directly reviewed, versioned primary text, with conflicts and uncertainty made visible.

The next active product build remains TS-004. This correction register is a hard gate for the later standards build and shall not divert the programme into premature compliance logic.
