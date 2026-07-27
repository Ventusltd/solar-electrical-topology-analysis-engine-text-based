# V8 Leapfrog Cable Schedule Workbench

Status: independent development build. Use at your own risk. This is an indicative screening tool, not a design approval, as-built record, procurement instruction or compliance certificate.

## Purpose

V8 isolates one question before deeper electromagnetic modelling:

What is the difference in EPC-installed external DC string cable when a thirty-module string is wired conventionally versus leapfrog?

The root V6 engine and the independent V7 FEED I workbench remain untouched as comparison versions. V8 is a new standalone calculator focused on cable schedule and visual explanation.

## Electrical principle

A string always has one free positive terminal and one free negative terminal.

Conventional sequential wiring places those terminals at opposite physical ends of the module row. If the inverter is near one end, one external conductor is short and the other external conductor must return from the far end.

Leapfrog wiring uses longer factory module leads to skip alternate modules outward and return through the skipped modules. Both free string terminals appear near the same physical end. The far end becomes a turn-around point, not the origin of a separate home-run conductor.

Therefore leapfrog does not remove both home-runs. It removes the additional full-row return conductor that appears in the conventional layout.

## Formula

Let:

- `R` = row span of one thirty-module string;
- `D` = distance from the near string terminal to the inverter inputs;
- `B` = band index beginning at zero;
- `G` = optional gap or routing allowance between adjacent bands.

Band offset:

`O = B × (R + G)`

Sequential external 6 mm² cable per string:

`short polarity = D + O`

`long polarity = D + O + R`

`total = 2(D + O) + R`

Leapfrog external 6 mm² cable per string:

`positive ≈ D + O`

`negative ≈ D + O`

`total = 2(D + O)`

Saving per string:

`R`

## Default example

The default example uses:

- 30 modules per string;
- module width along row 1.303 m;
- inter-module gap 0.020 m;
- row span 39.67 m;
- east bands 5,5,2;
- west bands 5,5,2;
- 24 strings per inverter;
- editable inverter distance, default 10 m;
- editable fleet count, default 795 inverters.

With these values, leapfrog avoids approximately one row span per string, or about 952 m of 6 mm² external DC string cable per inverter and about 757 km over 795 inverters.

## Evidence discipline

Manufacturer-derived defaults may be useful, but V8 still treats all values as editable evidence inputs. Module lead length, connector count, exact terminal positions, installation route, service loops, as-built wiring sequence and cable temperature must be confirmed before engineering use.
