# Build 025 - V10 geometry workbench

## Purpose

Make the browser repeatable and geometry-led without replacing the V7 and V8 visual language.

## View cartridges

- **V7 overview** renders all 24 strings, east/west faces, 12 MPPT allocations, table positions and external home-run routes.
- **V8 detail** renders one selected string with fixed M1-M30 physical positions, explicit terminals and the established sequential/leapfrog connection arcs.

Both views consume the same in-memory geometry study. They are views, not separate calculation engines.

## Geometry rules

1. Physical module order remains fixed left-to-right.
2. Electrical order changes with the topology cartridge.
3. Row span is derived from module count, module width and module gaps.
4. Table width is derived from row span, strings per row and gaps between string blocks.
5. Each string receives a deterministic face, row and column position.
6. External routes are orthogonal polylines: free terminal -> shared trench X -> inverter input Y -> inverter.
7. Cable length is calculated from the rendered polyline, then route slack and termination allowance are applied.
8. Moving the array changes coordinates and quantities automatically.
9. The user does not hand-draw cable.
10. The browser export contains the complete geometry study and all per-string route coordinates.

## Default arrangement

- 24 strings
- 12 MPPTs, two strings per MPPT
- 12 east-face and 12 west-face strings
- four rows per face
- three string blocks per row
- 30 modules per string

## Spreadsheet reconciliation

The uploaded Leapfrogv2 quantity sheet used band-level near/far endpoint totals and multiplied them by string counts. The V10 workbench generalises that idea: near/far distances are no longer typed into a table; they are derived independently for every string from its table position and the inverter/trench coordinates.

## Non-authority boundary

This browser cartridge is a deterministic geometry and quantity projection. The Python `CircuitModel`, topology validation, ordered traversal, geometry receipt and calculation receipt remain the target authority chain. Browser output must not be described as a validated engineering receipt until it is bound to that chain.
