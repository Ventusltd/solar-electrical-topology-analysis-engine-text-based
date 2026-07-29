# 2026 PV DC Modelling — Fact-Checked Evidence Note for V10

Status: evidence note for V10 recovery. This document records only the most consequential findings that could be verified from primary publisher or standards sources on 29 July 2026. It is not a compliance certificate and does not reproduce licensed standards text.

## Executive findings

1. **IEC 62548-1 Edition 1.1 is current and directly relevant to V10.** IEC published IEC 62548-1:2023/AMD1:2025 on 15 December 2025 and the consolidated IEC 62548-1:2023+AMD1:2025 CSV as Edition 1.1 on the same date. The standard covers PV array DC wiring, protection, switching and earthing. V10 should version every standards-derived rule against the exact edition used.

2. **Correction: bifacial K_I, anti-PID and arc-flash content were not shown by the available official evidence to be newly introduced by AMD1 alone.** The IEC product page for the original 2023 Edition 1.0 already lists provisions for bifacial and non-optimally oriented modules and a new Annex F containing K_I calculations, anti-PID equipment and arc flash among the significant changes from IEC 62548:2016. The amendment page confirms AMD1 exists but its public abstract does not establish which of those items were added or altered by AMD1. The engine must therefore compare the licensed 2023 and AMD1 texts before attributing a particular rule to the amendment.

3. **Loop geometry is a standards-facing engineering quantity.** The inspected licensed IEC 62548-1:2023 text identifies wiring-loop minimisation and close routing of bonding conductors with live conductors as design measures against lightning-induced voltage. V10 should calculate ordered positive, negative and bonding paths, local conductor separation and enclosed loop geometry. It must not invent a universal numerical loop-area pass/fail limit where the standard gives none.

4. **Array capacitance to earth is an expected design estimate for applicable large arrays, but the calculation remains evidence-sensitive.** The inspected IEC text requires an estimate for comparison with the insulation-monitoring device capability in the stated large-array case. V10 must distinguish conductor-to-earth, module/frame-to-earth, positive-to-earth and negative-to-earth networks and the effective capacitance visible at the actual IMD boundary. Dry and wet cases must not be collapsed into one unqualified number.

5. **The current V10 standards model must separate physical models from prescribed design methods.** A first-principles cell-temperature Voc calculation and an IEC Annex F maximum-voltage method using prescribed environmental data are different named cases. Neither should silently replace the other.

## Verified 2026 and 2026-relevant research

### Common-mode leakage current

Orfanoudakis, Koutroulis, Foteinopoulos and Wu analyse common-mode ground leakage current in a specific class of transformerless PV inverters with rectified-sine-wave DC-link voltage. The article was published online on 30 June 2025 and appears in Journal of Power Electronics volume 26, pages 227–241, issue year 2026. It derives RMS common-mode current expressions, identifies the role of the DC-link capacitor and reports that a split-inductor arrangement can reduce common-mode current by up to 70% in the studied topology, with simulation and laboratory verification.

**V10 consequence:** this supports explicit common-mode source, parasitic-capacitance, switching-frequency and inverter-topology inputs. It does not justify applying one DC-link-capacitance rule to all inverter architectures.

### PID leakage-current equivalent circuits

TamizhMani et al., first published 5 May 2026 in Progress in Photovoltaics, develop an electrochemical RC-equivalent model for PID leakage current. The paper distinguishes dry-surface and wet-surface governing mechanisms and includes glass bulk capacitance, interface double-layer capacitance and resistive paths.

**V10 consequence:** wet and dry environmental states should alter the network structure and evidence assumptions, not merely multiply one dry capacitance by a universal factor.

### Dry versus wet insulation resistance

Poulek, Beranek, Finsterle and Kozelka, published 25 January 2026 in Sustainability, compare dry and IEC-wet testing of 37 field-aged crystalline-silicon modules. The published dataset reports a large reduction from dry to wet insulation resistance and shows that some modules pass dry screening but fail wet testing.

**V10 consequence:** dry insulation resistance cannot stand in for wet-condition behaviour. This is resistance evidence, not a measured wet/dry capacitance ratio; it must not be used to scale capacitance directly.

### Lightning coupling

Chen et al., Electric Power Systems Research 257 (2026), article 112926, propose a hybrid PEEC–multi-conductor-transmission-line method for tower/transmission-line lightning coupling. The publisher abstract reports validation against rocket-triggered lightning data with peak-overvoltage prediction error below 5%.

**V10 consequence:** the method is relevant as adjacent electromagnetic research, not as direct validation of a PV string model. Any PEEC or transmission-line cartridge remains sandboxed until its geometry, terminations, dielectric assumptions and validation range are declared.

### DC arc-fault research

Jalil, Samet and Ghanbari, first published 6 January 2026, use experimental data with machine-learning methods to model DC series arc faults. A separate 2026 Fire paper reports a WDCNN–BiLSTM–cross-attention detection model with 99.89% accuracy on its reported experimental dataset.

**V10 consequence:** these papers show an active research field but do not convert the deterministic topology engine into an arc-fault detector. V10 may expose connector resistance, insulation condition, current, route and event inputs for research cases while keeping ML detection outside the certifiable calculation path.

### PV fire statistics

Wahlström et al., available online 15 July 2026 in Fire Safety Journal, analyse national statistics from the UK, Italy, Sweden and Slovenia. The abstract confirms that DC cables and connectors are the most frequently identified ignition source in the Swedish dataset and stresses that cross-country rates depend strongly on reporting methodology. It reports that about 68% of fires remain confined to PV equipment, 24% damage adjacent surfaces, 5% have significant fire spread and 3% destroy the building.

**Correction:** the accessible primary abstract did not establish the exact claim that DC cables/connectors account for 25% of all PV fires. That precise percentage should not be encoded or repeated without checking the full table and its denominator.

## Standards status verified from IEC

- IEC 62548-1:2023, Edition 1.0, published 7 December 2023.
- IEC 62548-1:2023/AMD1:2025, published 15 December 2025.
- IEC 62548-1:2023+AMD1:2025 CSV, Edition 1.1, published 15 December 2025.
- IEC 63027:2023 remains the published IEC standard for PV DC arc detection and optional interruption, covering systems up to 1,500 V DC.
- IEC 63112:2021 remains the published IEC standard for PV-array earth-fault protection equipment.
- IEC 61643-31:2018 remains the PV DC SPD product standard listed by IEC; its page includes the 2022 corrigendum and describes application up to 1,500 V DC.

No claim that these standards had no later amendment should be made without checking each IEC lifecycle page at the time of use.

## Claims not yet safe to encode

The following remain unresolved or require licensed primary-text review:

- the exact changes introduced by AMD1:2025 to Annex F, anti-PID, arc-flash and isolation provisions;
- the exact bifacial K_I formula, BNPI fallback and any irradiance trigger in the consolidated Edition 1.1;
- the exact force and applicability of every IEC 62548-1 loop-routing, IMD-capacitance and SPD critical-length clause;
- exact 0.5 m SPD lead definitions and any voltage-per-length rule of thumb;
- universal module-to-earth capacitance values or wet/dry capacitance ratios;
- any universal loop-area threshold;
- a universal transmission-line crossover criterion for all PV strings;
- exact 2026 absence claims, which are search findings rather than proof that no paper exists.

## Required V10 implementation response

1. Add standards-edition identity to every standards-derived result.
2. Implement separate named voltage cases: physical temperature-coefficient case and IEC-prescribed design case.
3. Implement bifacial current logic only after licensed Edition 1.1 clause comparison and regression vectors.
4. Make loop geometry, conductor pairing and routed distance first-class outputs without inventing numerical compliance thresholds.
5. Model common-mode and differential-mode networks separately.
6. Treat wet/dry insulation and capacitance states as separate evidence cases; never infer a capacitance multiplier from an insulation-resistance ratio.
7. Keep PEEC, distributed-line, lightning and arc-event models in the research sandbox until independently validated.
8. Record every promoted claim in the migration ledger with source, edition, validity boundary, uncertainty and test evidence.

## Primary sources checked

- IEC, IEC 62548-1:2023: https://webstore.iec.ch/en/publication/64171
- IEC, IEC 62548-1:2023/AMD1:2025: https://webstore.iec.ch/en/publication/98955
- IEC, IEC 62548-1:2023+AMD1:2025 CSV: https://webstore.iec.ch/en/publication/110893
- IEC, IEC 63027:2023: https://webstore.iec.ch/en/publication/27362
- IEC, IEC 63112:2021: https://webstore.iec.ch/en/publication/59647
- IEC, IEC 61643-31:2018: https://webstore.iec.ch/en/publication/26931
- Orfanoudakis et al.: https://doi.org/10.1007/s43236-025-01106-1
- TamizhMani et al.: https://doi.org/10.1002/pip.70113
- Poulek et al.: https://doi.org/10.3390/su18031212
- Chen et al.: https://doi.org/10.1016/j.epsr.2026.112926
- Jalil et al.: https://doi.org/10.1155/etep/6629476
- DC arc detection paper: https://doi.org/10.3390/fire9020084
- Wahlström et al.: https://doi.org/10.1016/j.firesaf.2026.104936
