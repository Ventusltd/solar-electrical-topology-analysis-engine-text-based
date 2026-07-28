import {
  EngineInputError,
  allocateMppts,
  computeProject,
  conductorResistanceOhm,
  topologyOrder,
} from "./engine.js";

function close(actual, expected, tolerance = 1e-9) {
  return Math.abs(actual - expected) <= tolerance;
}

function test(name, fn) {
  try {
    const detail = fn();
    return {
      name,
      status: "pass",
      detail: detail ?? "ok",
    };
  } catch (error) {
    return {
      name,
      status: "fail",
      detail: error instanceof Error ? error.message : String(error),
    };
  }
}

function assert(condition, message) {
  if (!condition) {
    throw new Error(message);
  }
}

export function runDebugTests() {
  const results = [
    test("sequential order", () => {
      const actual = JSON.stringify(topologyOrder(5, "sequential"));
      assert(actual === "[1,2,3,4,5]", "unexpected sequential order");
    }),
    test("leapfrog order for 30 modules", () => {
      const order = topologyOrder(30, "leapfrog");
      assert(order.length === 30, "wrong order length");
      assert(new Set(order).size === 30, "duplicate module");
      const turningSequenceIsCorrect = (
        order[14] === 29
        && order[15] === 30
        && order.at(-1) === 2
      );
      assert(turningSequenceIsCorrect, "wrong leapfrog turning sequence");
    }),
    test("custom order accepts module numbers above four", () => {
      const order = topologyOrder(
        6,
        "custom",
        [1, 3, 5, 6, 4, 2],
      );
      const preserved = order[2] === 5 && order[3] === 6;
      assert(preserved, "custom order was clamped or altered");
    }),
    test("invalid custom order is rejected", () => {
      let rejected = false;
      try {
        topologyOrder(4, "custom", [1, 2, 2, 4]);
      } catch (error) {
        rejected = error instanceof EngineInputError;
      }
      assert(rejected, "duplicate custom module was not rejected");
    }),
    test("MPPT allocation caps active strings at 24", () => {
      const allocation = allocateMppts({
        mpptCount: 100,
        defaultInputsPerMppt: 4,
      });
      assert(allocation.requestedStrings === 400, "wrong requested count");
      assert(allocation.activeStrings === 24, "active string cap failed");
      assert(allocation.truncated, "truncation flag missing");
    }),
    test("12 MPPT by two inputs produces 24 strings", () => {
      const project = computeProject({
        mpptCount: 12,
        defaultInputsPerMppt: 2,
        modulesPerString: 30,
      });
      assert(project.strings.length === 24, "wrong string count");
      assert(project.totals.modules === 720, "wrong module total");
    }),
    test("corrected Voc default exceeds 1500 V", () => {
      const project = computeProject({
        modulesPerString: 30,
        moduleVocStcV: 50,
        vocTempCoefficientPercentPerC: -0.24,
        cellTemperatureC: 20,
      });
      assert(
        close(project.voltage.moduleVocCorrectedV, 50.6),
        "wrong corrected module Voc",
      );
      assert(
        close(project.voltage.stringVocV, 1518),
        "wrong string Voc",
      );
      const hasLimitWarning = project.warnings.some(
        (warning) => warning.code === "VOLTAGE_LIMIT",
      );
      assert(hasLimitWarning, "missing voltage-limit warning");
    }),
    test("copper resistance at 20 C", () => {
      const resistance = conductorResistanceOhm({
        lengthM: 100,
        csaMm2: 10,
        conductorTemperatureC: 20,
      });
      assert(
        close(resistance, 0.17241, 1e-8),
        `unexpected resistance ${resistance}`,
      );
    }),
    test("segment count is modules plus one", () => {
      const project = computeProject({
        mpptCount: 1,
        defaultInputsPerMppt: 1,
        modulesPerString: 6,
      });
      assert(
        project.strings[0].segments.length === 7,
        "expected two home runs and five interconnects",
      );
    }),
    test("deterministic result excluding timestamp", () => {
      const input = {
        mpptCount: 2,
        defaultInputsPerMppt: 1,
        modulesPerString: 8,
      };
      const first = computeProject(input);
      const second = computeProject(input);
      delete first.generatedAt;
      delete second.generatedAt;
      assert(
        JSON.stringify(first) === JSON.stringify(second),
        "same input produced different output",
      );
    }),
  ];

  return {
    schema: "globalgrid2050.solar-dc-debug-test-report.v1",
    generatedAt: new Date().toISOString(),
    passed: results.filter((result) => result.status === "pass").length,
    failed: results.filter((result) => result.status === "fail").length,
    results,
    reviewQuestions: [
      "Does each formula use the correct physical quantity and temperature basis?",
      "Does the electrical order pass through every module exactly once?",
      "Are known routes, factory leads and provisional extensions separated?",
      "Are screening estimates clearly distinguished from construction quantities?",
      "Which missing physical objects block trusted EMC or transient studies?",
    ],
  };
}
