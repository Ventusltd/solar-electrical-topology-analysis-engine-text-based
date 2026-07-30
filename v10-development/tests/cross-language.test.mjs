import assert from "node:assert/strict";
import { readFileSync } from "node:fs";
import test from "node:test";
import { fileURLToPath } from "node:url";

import {
  conductorResistance,
  resistivePowerLoss,
  voltageDrop,
} from "../src/electrical.mjs";
import { quantity } from "../src/quantity.mjs";


const fixturePath = fileURLToPath(
  new URL("../fixtures/steady_state_cross_language_v1.json", import.meta.url),
);
const fixture = JSON.parse(readFileSync(fixturePath, "utf8"));

function close(actual, expected, tolerance = 1e-12) {
  assert.ok(
    Math.abs(actual - expected) <= tolerance * Math.max(1, Math.abs(expected)),
    `expected ${actual} to be within ${tolerance} of ${expected}`,
  );
}

test("JavaScript matches the shared 20 C steady-state formula fixture", () => {
  for (const item of fixture.cases) {
    const resistancePerMetre = quantity({
      id: `${item.id}.r20`,
      value: item.resistance_ohm_per_m,
      unit: "ohmPerMetre",
      provenance: "datasheet",
    });
    const length = quantity({
      id: `${item.id}.length`,
      value: item.length_m,
      unit: "m",
      provenance: "geometryDerived",
    });
    const current = quantity({
      id: `${item.id}.current`,
      value: item.current_a,
      unit: "A",
      provenance: "datasheet",
    });

    const resistance = conductorResistance({
      resistancePerMetre,
      length,
      circuitFactor: item.circuit_factor,
    });
    const drop = voltageDrop({ current, resistance });
    const loss = resistivePowerLoss({ current, resistance });

    close(resistance.value, item.expected.resistance_ohm);
    close(drop.value, item.expected.voltage_drop_v);
    close(loss.value, item.expected.resistive_loss_w);
  }
});
