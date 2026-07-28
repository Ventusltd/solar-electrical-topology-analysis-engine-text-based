# Restore point: before V9 computation engine rebuild

Date: 28 July 2026

Restore commit immediately before this file: `254be20f6c86415d8be9768acc47722cdebca1a6`.

Purpose: preserve the merged V9 graphical inverter-block sandbox before removing plan and side views and moving all governing logic into `v9-sandbox/debug/`.

Recovery:

```bash
git checkout 254be20f6c86415d8be9768acc47722cdebca1a6 -- v9-sandbox
```

This restore point records the boundary between the graphical prototype and the computation-first engine.