import assert from "node:assert/strict";
import test from "node:test";

import {
  canonicalLeapfrogOrder,
  computeTopologyGeometry,
  mirroredSequentialOrder,
  sequentialOrder,
  validateCustomOrder,
} from "../src/topology.mjs";

const closeTo = (actual, expected, tolerance = 1e-9) => {
  assert.ok(
    Math.abs(actual - expected) <= tolerance,
    `expected ${actual} to be within ${tolerance} of ${expected}`,
  );
};

test("sequential order is deterministic", () => {
  assert.deepEqual(sequentialOrder(5), [1, 2, 3, 4, 5]);
});

test("mirrored sequential order is deterministic", () => {
  assert.deepEqual(mirroredSequentialOrder(5), [5, 4, 3, 2, 1]);
});

test("canonical leapfrog order is a complete permutation", () => {
  const order = canonicalLeapfrogOrder(30);
  assert.equal(order.length, 30);
  assert.equal(new Set(order).size, 30);
  assert.deepEqual(order.slice(0, 5), [1, 3, 5, 7, 9]);
  assert.deepEqual(order.slice(-5), [10, 8, 6, 4, 2]);
});

test("custom order rejects duplicates and omissions", () => {
  assert.throws(() => validateCustomOrder([1, 2, 2], 3));
  assert.throws(() => validateCustomOrder([1, 2], 3));
  assert.deepEqual(validateCustomOrder([2, 3, 1], 3), [2, 3, 1]);
});

test("sequential path for 30 modules equals 29 pitches", () => {
  const result = computeTopologyGeometry({
    moduleCount: 30,
    pitchMetres: 1.303,
    topology: "sequential",
  });

  closeTo(result.pathLengthMetres, 29 * 1.303);
  closeTo(result.terminalSeparationMetres, 29 * 1.303);
  assert.equal(result.segments.length, 29);
});

test("canonical leapfrog path for 30 modules equals 57 pitches", () => {
  const result = computeTopologyGeometry({
    moduleCount: 30,
    pitchMetres: 1.303,
    topology: "leapfrog",
  });

  closeTo(result.pathLengthMetres, 57 * 1.303);
  closeTo(result.pathLengthMetres, 74.271);
  closeTo(result.terminalSeparationMetres, 1.303);
  assert.equal(result.segments.length, 29);
});

test("geometry output is deterministic", () => {
  const input = {
    moduleCount: 8,
    pitchMetres: 1.2,
    topology: "leapfrog",
  };
  assert.deepEqual(computeTopologyGeometry(input), computeTopologyGeometry(input));
});
