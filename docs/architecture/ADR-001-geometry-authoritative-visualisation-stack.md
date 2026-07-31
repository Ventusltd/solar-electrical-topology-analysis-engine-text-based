# ADR-001 — Geometry-authoritative visualisation stack

Status: accepted for implementation spike

Date: 2026-07-31

## Decision

The Solar DC browser shall be a thin presentation layer over the authoritative Python kernel.

The kernel owns:

- physical geometry;
- topology;
- conductor routes;
- geometric, installed and procurement cable lengths;
- electrical physics;
- validation and evidence receipts.

The browser shall receive explicit, versioned, content-addressed results. It shall not contain cable-routing algorithms, cable-length estimation rules or electrical formulae that can silently diverge from the kernel.

## Primary rendering stack

Use deck.gl v9.x on WebGL2 for the first production-capable renderer spike, using:

- `OrthographicView`;
- site-local Cartesian coordinates in metres;
- binary typed-array layer attributes;
- GPU colour picking;
- precomputed level-of-detail data;
- cartridge/tile-local coordinate origins.

WebGPU is an acceleration path, not a Phase-1 dependency. A WebGL2 fallback remains mandatory.

Three.js `InstancedMesh`/`BatchedMesh` remains the named alternative where true 3D terminal inspection or assembly-oriented scene graphs prove materially better.

Graph-layout engines shall not position site objects. Geometry is authoritative. Graphology or rustworkx may represent and query connectivity, while ELK/dagre may only be considered for a separate logical schematic view.

## Kernel-to-browser contract

The kernel shall emit immutable artefacts identified by canonical hashes:

- `GeometryReceipt`;
- `TopologyReceipt`;
- `ConstructionLengthReceipt`;
- `CalculationReceipt`;
- `ValidationReceipt`.

Each artefact shall include at least:

- schema version;
- kernel version;
- canonical input hash;
- canonical output hash;
- object identifiers;
- evidence references;
- uncertainty or status where applicable.

Conductors shall be delivered as explicit polyline vertex arrays plus authoritative scalar results. The browser renders those arrays; it does not derive their routes.

## Data formats

Phase 0 shall use canonical JSON for the schema and golden fixtures while preserving a direct migration path to:

- Apache Arrow IPC for in-flight columnar geometry and attributes;
- Parquet/GeoParquet for compressed at-rest artefacts and bills of materials;
- FlatBuffers only where nested, random-access receipt data demonstrates a real need.

DuckDB-Wasm is reserved for browser-side querying and aggregation of authoritative BOM and receipt data, not engineering calculation.

## Geometry hierarchy and instancing

The reusable physical hierarchy is:

`Project → power block → inverter → MPPT → input → string → table/assembly → module → terminal → conductor segment`.

Repeated tables, tracker blocks and inverter arrangements shall be represented as local-origin geometry assemblies with per-instance transforms. The renderer shall avoid duplicating full repeated geometry.

## Level of detail

- LOD 0: project and power-block overview;
- LOD 1: inverter, MPPT and string footprints;
- LOD 2: selected strings, modules and authoritative conductors;
- LOD 3: terminals, connectors and factory leads;
- LOD 4: evidence, receipts and physics overlays.

Detailed connectors shall not be rendered for an entire utility-scale plant simultaneously. LOD transitions shall use hysteresis and swap prebuilt buffers rather than regenerate million-object layers during interaction.

## Coordinate precision

Use local origins for every cartridge or spatial tile. Store small local float32 coordinates for GPU rendering and keep large site offsets in higher-precision metadata/transforms. Do not adopt expensive fp64 shaders by default.

## Spatial indexing and workers

Static receipt geometry should use prebuilt Flatbush indexes for object bounds and KDBush for point-like terminals where appropriate. Interactive editing may use RBush.

Renderer and data preparation should move to workers/OffscreenCanvas when benchmarks demonstrate benefit. GitHub Pages remains acceptable until custom COOP/COEP headers, static-site size, bandwidth or build limits become material.

## Authoritative cable-length stack

Every cable result shall distinguish:

1. geometric minimum length;
2. topology route length;
3. constructed/installed length;
4. procurement length.

Installed length may include explicit, evidence-backed components such as factory lead use, support routing, bend allowance, strain relief, termination allowance, service loops, tracker or thermal movement and installation tolerance. Procurement length adds drum rounding, spare and waste policy. Physics uses the constructed length unless an explicitly named study uses another evidence state.

## Python implementation direction

The initial kernel remains dependency-light. Candidate libraries shall only be adopted behind tests and benchmarks:

- NumPy for vectorised geometry and electrical arrays;
- Shapely for route corridors, obstacles and offsets;
- rustworkx for large deterministic topology/trench graphs;
- SciPy spatial structures where justified;
- pyarrow for browser artefacts.

Shortest-path algorithms are tools, not authority. Every tie-breaking rule and input ordering must be canonical and regression tested.

## Phased build

### Phase 0 — contract and benchmark harness

1. Freeze receipt schema v1 in canonical JSON.
2. Add golden byte/hash fixtures.
3. Define synthetic scale fixtures: 1 string, 24 strings, one large inverter, and approximately one million modules.
4. Record memory, build time, first render, frame rate and picking latency.

Exit criterion: repeated kernel runs produce identical canonical hashes.

### Phase 1 — V7/V8 renderer spike

1. Reproduce one V7 overview and one V8 detailed connection view in deck.gl.
2. Feed them from kernel-emitted arrays only.
3. Preserve the current pages as visual references.
4. Prove picking and LOD for one full inverter.

Exit criterion: geometry and cabling match authoritative fixtures; no browser routing code exists.

### Phase 2 — site-scale LOD

Add instancing, chunking, spatial indexes, tile/local origins, worker rendering and artefact caching. Benchmark to the target utility-scale fixture.

### Phase 3 — hosting migration trigger

Move from GitHub Pages only when custom headers, SharedArrayBuffer, artefact size, bandwidth or build constraints require it. Cloudflare Pages, Netlify or Vercel are candidates.

### Phase 4 — interactive authoritative recomputation

Add a stateless FastAPI calculation service when users require edited geometry to generate immediate authoritative receipts. Static immutable artefacts remain the normal read path. Pyodide may support small offline demonstrations but is not the large-site compute engine.

## Immediate build increments

1. Define receipt-schema v1 and golden fixtures.
2. Define construction-length objects and evidence fields.
3. Add sequential and leapfrog geometry fixtures with explicit polylines.
4. Add a browser fixture loader that renders supplied geometry without routing.
5. Build the V8 detailed deck.gl spike first; then V7 overview.
6. Add benchmark fixtures before introducing Arrow, rustworkx or Shapely.

## Non-negotiable rule

> Topology chooses what connects. Geometry determines where objects exist and the minimum valid route. Installation rules determine the constructed route. Physics computes from the constructed route. The browser only presents authoritative results.
