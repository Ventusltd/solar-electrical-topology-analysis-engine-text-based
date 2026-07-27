# Restore point — V6, V7 and V8 leapfrog build

Date: 2026-07-27
Branch: main

## Purpose

This folder provides direct file recovery before the existing V6 and V7 interfaces were changed to add selectable sequential/leapfrog wiring and before the independent V8 workbench was taken forward.

## Exact pre-change copies

- `index-v6-before-leapfrog.html` — exact root V6 `index.html` before the leapfrog controls and diagram.
- `app-v6-before-leapfrog.js` — exact root V6 `app.js` used by that interface.
- `index-v7-before-leapfrog.html` — exact earlier `/v7-development/index.html`.
- `index-v8-initial.html` — exact first independent V8 leapfrog workbench.
- `README.before-v8-leapfrog.md` — repository README before V8 documentation was added.

The pre-change source blob references were:

- V6 root `index.html`: `8738e2e0aa0d2dfbd8409287e18351b10c841dc6`
- V6 root `app.js`: `89e8923bb006d12765be7a20edca0e9f9f94f8e1`
- V7 `v7-development/index.html`: `e55babbdf44c8c5a911ee01fce3ad36931bbe3ed`
- Initial V8 `v8-leapfrog/index.html`: `4eab2b3c2428f302f2be7192a86fe99ffbb21460`

## Build state after the restore point

Commit `8e30b379b742f1d5d8837fd6117e32173a8caf6c` introduced:

- V6 sequential/leapfrog mode;
- an editable distance from inverter to the nearest string terminals;
- V6 sequential-versus-leapfrog comparison diagram;
- corrected V7 terminal coordinates and selectable wiring mode;
- V7 drag, wheel/pinch zoom, string selection, schedule and MPPT pairing review;
- geometry-derived external positive and negative cable lengths.

The independent V8 workbench remains under `/v8-leapfrog/`.

## Recovery procedure

To recover an earlier file without branches, copy the corresponding file from this restore folder back to its original path on `main`. Do not copy the restore-point filename itself into the live application without renaming it to the original path.
