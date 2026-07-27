# Leapfrog topology commentary for V6 and V7

Status: technical commentary only. This note does not alter the root V6 app or the independent V7 FEED I app.

## Core distinction

A thirty-module string still has one positive free terminal and one negative free terminal. Leapfrog does not change string voltage, current, module count, MPPT allocation or polarity. It changes where the two free terminals appear in physical space.

In a conventional sequential string the physical order is also the electrical order. If the modules are arranged 1 to 30 along a rank, the free terminals normally appear at opposite physical ends of the row. If the inverter is at the near end, one home-run conductor is short and the other home-run conductor must return from the far end. That adds roughly one complete row span of EPC-installed 6 mm² DC string cable per string.

In a leapfrog string the electrical order skips alternate modules on the outward run and returns through the skipped modules. Both free string terminals appear at the same physical end of the row. The far end is a turn-around point, not a home-run origin. The factory-fitted module leads must be long enough to make the skipped-module links without being stretched, sharply bent or extended with unnecessary connector interfaces.

## What V6 currently represents

The root V6 complete-circuit engine already separates external positive length, external negative length, module leads, connectors, resistance, voltage drop, inductance, delay and common-mode capacitance. It remains a useful complete-circuit calculator.

However, its generated topology should not be read as an as-built leapfrog proof. Where one external polarity is approximately one full row span longer than the other, the generated geometry is effectively conventional/sequential for that string. V6 therefore needs a future selectable topology flag before its generated external lengths can be used to distinguish sequential from leapfrog.

## What V7 currently represents

The independent V7 FEED I page is an electromagnetic foundations workbench. It is not a string-layout scheduler. It helps test two-wire geometry, propagation, event classification and capacitance aggregation. It should remain isolated from the V8 leapfrog schedule until the V8 schedule is converted into a node-and-branch netlist that V7 can consume.

## Formula for the V8 schedule

Let:

- `R` = physical row span for one 30-module string;
- `D` = distance from the near string-terminal end to the inverter inputs;
- `B` = band index beginning at zero;
- `G` = optional gap or allowance between adjacent 30-module bands.

For a band at offset:

`O = B × (R + G)`

Sequential external cable per string:

`short polarity = D + O`

`long polarity = D + O + R`

`total external 6 mm² = 2(D + O) + R`

Leapfrog external cable per string:

`positive ≈ D + O`

`negative ≈ D + O`

`total external 6 mm² = 2(D + O)`

Saving per string:

`R`

The saving is independent of the inverter-distance input. Increasing the inverter distance from 10 m to 20 m to 30 m raises both cases by the same amount. Leapfrog does not remove both home-runs; it removes the additional far-end return conductor that exists in the sequential layout.

## Required V8 outputs

V8 shall therefore report:

- row span from module width and along-row gap;
- string count per face and per inverter;
- external positive and negative length for each band in sequential mode;
- external positive and negative length for each band in leapfrog mode;
- total external 6 mm² cable per inverter in both modes;
- total external 6 mm² cable across a chosen inverter fleet in both modes;
- difference in metres and kilometres;
- resistance, voltage drop and I²R loss difference using the selected cable resistance and operating temperature;
- a diagram showing why both free terminals are near the inverter end under leapfrog;
- JSON export carrying all input values and this topology assumption.

## Evidence and caution

Public manufacturer data supports the default numerical inputs: the Trina module data gives a 1.303 m width, 2.384 m length, 4 mm² module cables, 350/280 mm standard portrait leads and customisable lead length; the SG350HX data gives 12 MPPT inputs with two connectors per MPPT in the relevant configuration; Studer data gives 6 mm² tinned copper string cable at 3.39 mΩ/m at 20°C and 4 mm² module cable at 5.09 mΩ/m; Stäubli MC4-Evo 2 data gives plug-connector contact resistance below 0.2 mΩ.

Private or project-specific employer requirements, drawings, continuity records and as-built photographs should be used only as evidence inputs and should not be reproduced in the public repo. The public model must stay generic: it can calculate sequential versus leapfrog consequences, but it cannot certify that a particular installation was actually wired in either pattern.
