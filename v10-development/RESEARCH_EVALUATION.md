# V10 Research Evaluation

Status: controlled engineering review of an external research input.

## Confidentiality treatment

All personal names, project names, site names, client identities and place references have been excluded. The research input is retained only as a source of generic hypotheses, proposed tests, architecture ideas and calculation questions.

## Overall verdict

The research is valuable as a roadmap, but it is not suitable for direct implementation without correction. It correctly identifies the need to separate physical topology, electrical connectivity, component evidence and calculation provenance. It also correctly argues that field-installed conductor, factory lead conductor, loop geometry and labour exposure must be reported separately.

Several numerical claims are not yet proven and some are internally inconsistent. They are therefore quarantined rather than adopted.

## Accepted directions

1. Build V10 around typed components and an ordered connectivity graph.
2. Keep factory leads, extension leads, home-run conductors and return conductors as separate quantities.
3. Derive conductor length from terminal coordinates and connection order rather than from a single typed total.
4. Restore loop-area, inductance and transient-screen outputs only after geometry and boundary conditions are explicit.
5. Add component libraries with evidence class, version, source date and uncertainty.
6. Preserve earlier versions and develop V10 in an isolated branch and directory.
7. Add deterministic tests, independent reference calculations and schema-versioned JSON output.
8. Treat standards clauses, manufacturer data and research papers as evidence inputs, not executable truth.

## Corrected or rejected claims

### Leapfrog internal path length

The proposed value `29 × 2 × pitch` is not generally valid for a 30-module leapfrog sequence. For the canonical order `1,3,5,...,29,30,28,...,2`, the centre-to-centre path is derived from every consecutive pair:

- odd-side jumps: 14 × 2 pitches;
- crossover: 1 × 1 pitch;
- even-side jumps: 14 × 2 pitches;
- total: 57 pitches, not 58 pitches.

At a pitch of 1.303 m this is 74.271 m. This is a geometric path between terminal reference points, not automatically the factory-copper requirement. Actual conductor requirement depends on junction-box positions, lead exit directions, slack, connector geometry and routing constraints.

### Copper equivalence

The statement that total copper is approximately equal between topologies is plausible but not yet proven. It depends on conductor cross-sections, actual lead lengths, return routing, slack factors and whether factory leads replace field cable one-for-one. V10 will calculate mass by component rather than assert equivalence.

### Lightning-induced voltage

`U = A × dB/dt` is a useful first-order screen, not a complete lightning model. It requires an explicit magnetic-field model, strike geometry, distance, waveform, bonding arrangement and effective loop definition. No fixed voltage-per-square-metre value will be embedded until independently derived and bounded.

### Standards and market claims

All clause interpretations, target loop areas, failure percentages, project deployment claims and supplier specifications remain unverified until checked against controlled primary sources. They may inform research tasks but cannot become defaults or compliance statements.

## First implementation purchase order

P0 is limited to a pure topology computation core. It will:

- generate sequential, mirrored-sequential and canonical leapfrog orders;
- validate custom orders as exact permutations;
- derive consecutive geometric segment lengths from module coordinates;
- expose terminal positions and path length;
- keep field and factory conductor classes separate;
- contain no confidential data, manufacturer defaults, site values or compliance conclusions.

Electrical resistance, mass, cost, loop area and transient calculations will follow only after this core passes deterministic tests.