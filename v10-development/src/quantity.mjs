export const PROVENANCE_RANK = Object.freeze({
  measured: 4,
  datasheet: 3,
  standardsDerived: 3,
  geometryDerived: 3,
  inherited: 2,
  assumed: 1,
  researchHypothesis: 0,
});

const DIMENSIONS = Object.freeze({
  "1": {},
  m: { length: 1 },
  m2: { length: 2 },
  A: { current: 1 },
  V: { mass: 1, length: 2, time: -3, current: -1 },
  ohm: { mass: 1, length: 2, time: -3, current: -2 },
  W: { mass: 1, length: 2, time: -3 },
  K: { temperature: 1 },
  ohmPerMetre: { mass: 1, length: 1, time: -3, current: -2 },
});

function assertFinite(value, name) {
  if (!Number.isFinite(value)) throw new TypeError(`${name} must be finite`);
}

function normaliseInterval(value, uncertainty) {
  if (!uncertainty) return { kind: "none" };
  if (uncertainty.kind === "none") return uncertainty;
  if (uncertainty.kind === "interval") {
    assertFinite(uncertainty.lo, "uncertainty.lo");
    assertFinite(uncertainty.hi, "uncertainty.hi");
    if (uncertainty.lo > uncertainty.hi) throw new RangeError("interval lo must not exceed hi");
    if (value < uncertainty.lo || value > uncertainty.hi) {
      throw new RangeError("quantity value must lie inside its uncertainty interval");
    }
    return { kind: "interval", lo: uncertainty.lo, hi: uncertainty.hi };
  }
  throw new TypeError(`unsupported uncertainty kind: ${uncertainty.kind}`);
}

export function quantity({
  id,
  value,
  unit,
  provenance,
  uncertainty = { kind: "none" },
  source = null,
  evidenceStatus = "unverified",
}) {
  if (typeof id !== "string" || id.length === 0) throw new TypeError("quantity id is required");
  assertFinite(value, "value");
  if (!Object.hasOwn(DIMENSIONS, unit)) throw new TypeError(`unsupported unit: ${unit}`);
  if (!Object.hasOwn(PROVENANCE_RANK, provenance)) {
    throw new TypeError(`unsupported provenance: ${provenance}`);
  }
  return Object.freeze({
    id,
    value,
    unit,
    dimension: DIMENSIONS[unit],
    provenance,
    uncertainty: normaliseInterval(value, uncertainty),
    source,
    evidenceStatus,
  });
}

export function weakestProvenance(inputs) {
  if (!Array.isArray(inputs) || inputs.length === 0) throw new TypeError("inputs are required");
  return inputs.reduce((weakest, item) =>
    PROVENANCE_RANK[item.provenance] < PROVENANCE_RANK[weakest] ? item.provenance : weakest,
  inputs[0].provenance);
}

export function intervalBounds(q) {
  return q.uncertainty.kind === "interval"
    ? [q.uncertainty.lo, q.uncertainty.hi]
    : [q.value, q.value];
}

export function deriveQuantity({ id, value, unit, inputs, equationId, uncertainty, evidenceStatus = "candidate" }) {
  return quantity({
    id,
    value,
    unit,
    provenance: weakestProvenance(inputs),
    uncertainty,
    source: {
      equationId,
      inputIds: inputs.map((input) => input.id),
    },
    evidenceStatus,
  });
}
