# B9 Multi-Array Electrical Sandbox

Status: first working public development slice.

B9 is independent. It does not replace or modify V6, V7 or V8.

## What works now

The browser now provides:

- a mechanical cartridge palette;
- fixed tilt one in portrait;
- fixed tilt two in portrait;
- east-west one in portrait per face;
- east-west five in portrait per face;
- legacy six in landscape;
- one- and two-in-portrait tracker cartridges;
- sequential, leapfrog, mirrored sequential, alternating-return and custom electrical orders;
- exact editable module width, module height and gap;
- editable positive and negative factory-lead length;
- editable modules per string and parallel-string count;
- plan, side and circuit views using one canonical model;
- fixed physical module numbering in circuit view;
- lead-reach feasibility screening;
- technician summary;
- commercial copper screen using `CSA × km × 9.6`;
- browser scene JSON export;
- GeoJSON module-footprint export;
- hand-calculated browser fixtures.

## Current canaries

The browser tests assert:

- 30 modules × 1.303 m with zero gap = 39.09 m row span;
- the leapfrog order reaches `M29 → M30 → M28` at the far-end turnaround;
- the free string terminals are `M1−` and `M2+`;
- 24 strings × 30 modules = 720 modules;
- two 1.4 m leads pass the conservative zero-gap leapfrog reach screen;
- 0.350 m plus 0.280 m leads fail that screen by 1.976 m;
- sequential external cable exceeds leapfrog by one row span per string.

Open [`tests.html`](tests.html) to run the fixtures in the browser.

## Current boundary

This first slice is a geometry and topology authoring proof. It does not yet calculate:

- conductor resistance from declared cable records;
- voltage drop and power loss;
- signed or absolute loop area;
- differential or common-mode inductance;
- dry or wet capacitance;
- propagation delay or characteristic impedance;
- SPD, insulation-monitoring or protection settings;
- Parquet and DuckDB fleet outputs.

Those calculations must consume ordered conductor segments generated from the canonical scene rather than being hard-coded inside a topology renderer.

## Planned data path

`scene objects → geometry → terminals/connectivity → ordered conductor segments → studies → Parquet/DuckDB/GeoJSON`

## Public boundary

No confidential project information, NDA material, employer requirements, as-built drawings, private photographs or proprietary calibration belongs in B9.

See:

- [`CLAUDE_IMPLEMENTATION_WORK_ORDER.md`](CLAUDE_IMPLEMENTATION_WORK_ORDER.md)
- [`../technical-commentary/B9_TECHNICAL_COMMENTARY_AND_SANDBOX_FEED.md`](../technical-commentary/B9_TECHNICAL_COMMENTARY_AND_SANDBOX_FEED.md)
