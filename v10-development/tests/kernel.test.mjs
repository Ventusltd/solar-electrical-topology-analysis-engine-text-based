import assert from "node:assert/strict";
import test from "node:test";

import { runKernel } from "../src/kernel.mjs";
import { quantity, weakestProvenance } from "../src/quantity.mjs";

const closeTo = (actual, expected, tolerance = 1e-9) => {
  assert.ok(Math.abs(actual - expected) <= tolerance, `${actual} not within ${tolerance} of ${expected}`);
};

test("quantity rejects unsupported units and propagates weakest provenance", () => {
  assert.throws(() => quantity({ id: "x", value: 1, unit: "bananas", provenance: "measured" }));
  const measured = quantity({ id: "m", value: 1, unit: "m", provenance: "measured" });
  const assumed = quantity({ id: "a", value: 1, unit: "m", provenance: "assumed" });
  assert.equal(weakestProvenance([measured, assumed]), "assumed");
});

test("kernel computes geometry-derived resistance, voltage drop and power loss", () => {
  const output = runKernel({
    documentId: "golden-sequential-4",
    layout: { moduleCount: 4, pitchMetres: 2, topology: "sequential" },
    electrical: {
      resistanceOhmPerMetre: 0.003,
      currentAmps: 10,
      circuitFactor: 1,
    },
  });

  closeTo(output.geometry.pathLengthMetres, 6);
  closeTo(output.results.resistance.value, 0.018);
  closeTo(output.results.voltageDrop.value, 0.18);
  closeTo(output.results.resistivePowerLoss.value, 1.8);
  assert.equal(output.results.resistance.provenance, "datasheet");
  assert.equal(output.schemaVersion, "globalgrid2050.solar-dc-computation.v10.kernel.1");
});

test("kernel preserves uncertainty intervals through resistance and voltage drop", () => {
  const output = runKernel({
    layout: { moduleCount: 3, pitchMetres: 1, topology: "sequential" },
    electrical: {
      resistanceOhmPerMetre: 0.01,
      resistanceIntervalOhmPerMetre: { lo: 0.009, hi: 0.011 },
      currentAmps: 5,
      currentIntervalAmps: { lo: 4.5, hi: 5.5 },
      lengthUncertaintyMetres: 0.1,
    },
  });

  const resistanceInterval = output.results.resistance.uncertainty;
  closeTo(resistanceInterval.lo, 0.009 * 1.9);
  closeTo(resistanceInterval.hi, 0.011 * 2.1);
  const dropInterval = output.results.voltageDrop.uncertainty;
  closeTo(dropInterval.lo, 4.5 * resistanceInterval.lo);
  closeTo(dropInterval.hi, 5.5 * resistanceInterval.hi);
});

test("cold Voc candidate calculation is traceable and interval bounded", () => {
  const output = runKernel({
    layout: { moduleCount: 30, pitchMetres: 1.3, topology: "sequential" },
    electrical: {
      resistanceOhmPerMetre: 0.003,
      currentAmps: 17,
      vocStcVolts: 50,
      betaVocPercentPerKelvin: -0.29,
      minimumCellTemperatureKelvin: 263.15,
      minimumCellTemperatureIntervalKelvin: { lo: 261.15, hi: 265.15 },
    },
  });

  closeTo(output.results.voltageLimits.moduleVocCold.value, 55.075);
  closeTo(output.results.voltageLimits.stringVocCold.value, 1652.25);
  assert.equal(
    output.results.voltageLimits.moduleVocCold.evidenceStatus,
    "candidate-needs-standards-verification",
  );
  assert.equal(output.results.voltageLimits.stringVocCold.source.inputIds[0], "moduleVocCold");
});

test("kernel output is deterministic for identical JSON input", () => {
  const input = {
    layout: { moduleCount: 8, pitchMetres: 1.2, topology: "leapfrog" },
    electrical: { resistanceOhmPerMetre: 0.0031, currentAmps: 12.5 },
  };
  assert.deepEqual(runKernel(input), runKernel(input));
});
