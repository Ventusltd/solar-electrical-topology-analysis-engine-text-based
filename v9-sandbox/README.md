# V9 Multi-Array Electrical Sandbox

V9 is the strategic development architecture for the generic solar DC string topology engine.

The version lineage is:

- V6: complete-circuit calculator.
- V7: electromagnetic foundations workbench.
- V8: sequential versus leapfrog external-cable workbench.
- V9: multi-array electrical sandbox and common topology architecture.

## Current migration slice

The public `v9-sandbox/index.html` entry point is live and temporarily reuses the proven B9 renderer and styles so the browser remains operational while the code is extracted safely.

New V9 work has started in independent files:

- `schema.js`: typed canonical stores, evidence classes, object types and segment types.
- `state.js`: deterministic state, bounded history, undo, redo and stable serialisation.

The historical `b9-sandbox/` directory is retained as migration evidence. It must not be treated as the current version name and must not be extended with new architecture.

## Architecture

The governing chain is:

Mechanical cartridge → electrical cartridge → ordered conductor segments → physics studies → exports and reports.

Downstream studies consume ordered segments. They must not branch on topology names.

## Next build steps

1. Extract the renderer, cartridges and current model into V9-owned files.
2. Connect the V9 state store to the browser controls.
3. Add undo and redo controls and tests.
4. Replace the transitional B9 imports.
5. Generate typed terminals, connectivity and ordered conductor segments.
6. Add snapping and route-anchor editing.

## Public boundary

V9 is generic engineering development only. Do not add confidential, client-specific or project-identifying material.
