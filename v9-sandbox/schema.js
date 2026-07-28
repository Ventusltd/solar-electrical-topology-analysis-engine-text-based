export const V9_SCHEMA_VERSION = "v9-scene-0.1.0";

export const EVIDENCE_CLASSES = Object.freeze([
  "measured",
  "declared",
  "derived",
  "assumed",
  "defaulted",
  "research-model",
  "measurement-required",
]);

export const OBJECT_TYPES = Object.freeze([
  "site",
  "block",
  "cartridge-instance",
  "table",
  "face",
  "tracker",
  "module",
  "junction-box",
  "connector",
  "terminal",
  "cable-anchor",
  "conductor",
  "segment",
  "coil",
  "route-environment",
  "frame",
  "rail",
  "pile",
  "earth-node",
  "spd",
  "combiner",
  "mppt",
  "inverter",
  "assumption",
  "measurement",
  "study-run",
  "result",
  "warning",
]);

export const SEGMENT_TYPES = Object.freeze([
  "module-interconnect",
  "factory-lead",
  "extension-lead",
  "coil",
  "along-rank",
  "across-table",
  "structure-drop",
  "trench",
  "termination",
  "device",
  "bonding",
  "earth-return",
]);

export function createEmptyScene() {
  return {
    schemaVersion: V9_SCHEMA_VERSION,
    id: "site-0001",
    units: {
      length: "m",
      area: "m2",
      resistance: "ohm",
      inductance: "H",
      capacitance: "F",
      mass: "kg",
    },
    objects: [],
    geometries: [],
    terminals: [],
    connectivity: [],
    segments: [],
    materials: [],
    environments: [],
    assumptions: [],
    measurements: [],
    studyRuns: [],
    studyResults: [],
    warnings: [],
  };
}

export function validateStableId(id) {
  return typeof id === "string" && /^[a-z0-9][a-z0-9-]*$/.test(id);
}

export function assertSceneShape(scene) {
  if (!scene || scene.schemaVersion !== V9_SCHEMA_VERSION) {
    throw new Error("Scene does not use the current V9 schema version.");
  }

  const stores = [
    "objects",
    "geometries",
    "terminals",
    "connectivity",
    "segments",
    "materials",
    "environments",
    "assumptions",
    "measurements",
    "studyRuns",
    "studyResults",
    "warnings",
  ];

  stores.forEach((store) => {
    if (!Array.isArray(scene[store])) {
      throw new Error(`Scene store ${store} must be an array.`);
    }
  });

  return true;
}
