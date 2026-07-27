# V8 Leapfrog Cable Schedule Workbench

Status: independent development build. Use at your own risk.

This is an indicative screening tool, not a design approval, as-built
record, procurement instruction or compliance certificate.

## Purpose

V8 isolates one question before deeper electromagnetic modelling:

What is the difference in EPC-installed external DC string cable when a
thirty-module string is wired conventionally versus leapfrog?

The root V6 engine and the independent V7 FEED I workbench remain
untouched as comparison versions. V8 is a standalone cable-schedule and
visual-explanation workbench.

## Electrical principle

A string always has one free positive terminal and one free negative
terminal.

Conventional sequential wiring places those terminals at opposite
physical ends of the module row. If the inverter is near one end, one
external conductor is short and the other external conductor must return
from the far end.

Leapfrog wiring uses sufficiently long factory module leads to skip
alternate modules outward and return through the skipped modules. Both
free string terminals then appear near the same physical end. The far end
becomes a turn-around point, not the origin of a separate external return.

Leapfrog does not remove both home-runs. It removes the additional
full-row return conductor that appears in the conventional layout.

## External cable formula

Let:

- `R` be the row span of one thirty-module string;
- `D` be the distance from the near string terminal to the inverter;
- `B` be the band index beginning at zero;
- `G` be the gap or routing allowance between adjacent bands;
- `O = B × (R + G)` be the band offset.

Sequential external 6 mm² cable per string:

`total = 2(D + O) + R`

Leapfrog external 6 mm² cable per string:

`total = 2(D + O)`

Theoretical difference per string:

`R`

Distance to the inverter changes the unavoidable positive-and-negative
base pair in both cases. It does not change the one-row-span difference.

## Lead-length feasibility gate

Leapfrog saving is not automatically available.

The default geometric screening reach is:

`required reach = 2 × module pitch`

where:

`module pitch = module width + inter-module gap`

An entered measured routed connector-to-connector span may override the
geometric screening reach.

Available reach is:

`positive factory lead + negative factory lead`

The screen reports:

- required reach;
- available reach;
- margin;
- extension length required when the result fails;
- evidence provenance.

When the lead-length screen fails, V8 still displays the theoretical
sequential-versus-leapfrog difference but refuses to label it as an
available saving.

For the default geometry:

- module pitch is 1.323 m;
- required two-pitch reach is 2.646 m;
- catalogue leads of 0.350 m and 0.280 m fail;
- two 1.2 m leads fail by 0.246 m;
- two 1.4 m leads pass the length screen.

Bend radius, connector orientation, support and usable slack remain
separate checks.

## Fleet aggregation correction

The 24-string inverter is an archetype. It is not treated as the exact
string count of every inverter in the fleet.

V8 now carries separately:

- archetype strings per inverter;
- inverter count;
- actual total site string count;
- average strings per inverter.

The default site comparison uses 18,918 strings.

Theoretical site cable difference is calculated as:

`row span × actual total site strings`

not:

`24 strings × inverter count × row span`

For a 39.67 m row span and 18,918 strings, the theoretical difference is
approximately 750.48 km of external 6 mm² cable.

The default catalogue leads fail the feasibility screen, so this number is
shown as theoretical rather than available until custom or measured lead
evidence passes.

## Copper invariant

Factory module-lead conductor exists under both sequential and leapfrog
wiring. It may be coiled or deployed, but it is still purchased with the
module and remains electrically in circuit.

Therefore the basic topology comparison changes only the external
EPC-installed DC string cable. A later cartridge model must assert that
factory module-lead conductor and ordinary connector count remain equal
between topologies unless explicit extension segments are introduced.

## Current validation

V8 includes browser and Node regression tests covering:

- module pitch;
- row span;
- two-pitch lead reach;
- failing and passing lead scenarios;
- 24-string archetype;
- 18,918-string site total;
- inverter-distance invariance;
- mirrored polarity labelling;
- refusal to claim available saving when infeasible.

## Next architecture

The binding continuation brief is:

[`../BUILD_RECOVERY_INSTRUCTIONS_CHATGPT.md`](
../BUILD_RECOVERY_INSTRUCTIONS_CHATGPT.md
)

The next stage is a topology-cartridge and segment-data architecture using
Python, DuckDB and zstd-compressed Parquet for the fleet build. The browser
will remain the interactive archetype and presentation layer; it will not
hold approximately 1.9 million site segment rows as one JSON document.

## Evidence discipline

Manufacturer-derived defaults are starting points. Module lead length,
connector position, routed span, route geometry, service loops, as-built
wiring order, cable temperature and actual site string count require
controlled evidence before engineering reliance.
