# Restore point — V8 leapfrog build

Date: 2026-07-27
Branch: main
Purpose: recovery marker before adding the independent V8 leapfrog cable-schedule workbench and related technical commentary.

## Pre-change file references

The following existing application files were not to be functionally changed by this build.

- `README.md` — pre-change blob SHA: `994bb2e5fce77bf356a6f17ae1a32a2591fd0f41`
- `index.html` — V6/root pre-change blob SHA: `8738e2e0aa0d2dfbd8409287e18351b10c841dc6`
- `app.js` — V6/root pre-change blob SHA: `89e8923bb006d12765be7a20edca0e9f9f94f8e1`
- `v7-development/feed-i/index.html` — V7 FEED I pre-change blob SHA: `88c8f7bcde7c17566acf4881384eafe194d4699a`

## Recovery intent

This restore point deliberately records the stable root V6 and independent V7 FEED I references before V8 was added.

V8 is intended to be a new independent folder. V6 and V7 should remain available as comparison versions.

To recover the pre-V8 public documentation state, restore `README.md` from `README.before-v8-leapfrog.md` in this folder and remove the new V8/commentary files added after this restore point.
