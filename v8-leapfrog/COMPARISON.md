# V8 comparison against V6 and V7

Status: development comparison note.

## V6 root engine

V6 remains the complete-circuit calculator. It models external positive length, external negative length, module leads, connectors, resistance, voltage drop, loop inductance, common-mode quantities and capacitance outputs. It remains useful for complete-circuit electrical review.

V6 does not yet have a separate topology switch proving whether the external positive and negative coordinates came from sequential wiring or leapfrog wiring. Where one external polarity is one row span longer than the other, V6 is effectively showing the sequential home-run consequence.

## V7 FEED I electromagnetic workbench

V7 remains the isolated electromagnetic foundations page. It tests unit discipline, two-wire differential parameters, rise-time classification, capacitance aggregation and evidence gates.

V7 is not a generated string-layout schedule. Its role is to test physics once a topology supplies route segments.

## V8 leapfrog cable-schedule workbench

V8 narrows the problem to one quantity class: external EPC-installed DC string cable / home-run cable.

V8 compares:

- conventional sequential wiring;
- leapfrog wiring;
- per-band external positive and negative lengths;
- per-inverter external cable total;
- fleet external cable total;
- resistance, voltage drop and loss effect from the avoided conductor length.

## Key design rule

A string always has one free positive terminal and one free negative terminal.

Sequential wiring places those free terminals at opposite physical ends of the row.

Leapfrog wiring brings both free terminals to the inverter-side end of the row.

Therefore:

`sequential external cable per string = 2(D + O) + R`

`leapfrog external cable per string = 2(D + O)`

`difference per string = R`

where:

- `D` is the inverter distance from the near string-terminal end;
- `O` is the band offset;
- `R` is the row span.

## Why V8 is separate

The V8 page was created independently so the V6 root tool and V7 electromagnetic workbench are not destabilised. Once the V8 schedule is stable, later work can convert its row and band schedules into the segment-chain or netlist objects required by the electromagnetic model.
