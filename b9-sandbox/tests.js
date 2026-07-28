import { getCartridge } from "./cartridges.js";
import {
  buildScene,
  deriveSummary,
  rowSpan,
  topologyOrder,
} from "./model.js";

const results = [];

function assertEqual(name, actual, expected) {
  const pass = actual === expected;
  results.push({ name, pass, actual, expected });
}

function assertClose(name, actual, expected, tolerance = 1e-9) {
  const pass = Math.abs(actual - expected) <= tolerance;
  results.push({ name, pass, actual, expected });
}

function baseInput(overrides = {}) {
  return {
    moduleWidthM: 1.303,
    moduleHeightM: 2.384,
    moduleGapM: 0,
    orientation: "portrait",
    positiveLeadM: 1.4,
    negativeLeadM: 1.4,
    junctionBoxMode: "split",
    lowEdgeM: 1,
    highEdgeM: 4,
    ridgeGapM: 0.3,
    rowPitchM: 3,
    trackerAngleDeg: 0,
    inverterDistanceM: 10,
    modulesPerString: 30,
    stringCount: 24,
    topology: "leapfrog",
    customOrder: "",
    externalCableCsaMm2: 6,
    factoryLeadCsaMm2: 4,
    ...overrides,
  };
}

const cartridge = getCartridge("fixed-1p");
const leapfrogScene = buildScene(baseInput(), cartridge);
const leapfrogSummary = deriveSummary(leapfrogScene);

assertClose(
  "Thirty modules at 1.303 m and zero gap span 39.09 m",
  rowSpan(leapfrogScene),
  39.09,
  1e-12,
);

assertEqual(
  "Leapfrog order begins with odd modules",
  topologyOrder(30, "leapfrog").slice(0, 5).join(","),
  "1,3,5,7,9",
);

assertEqual(
  "Leapfrog turnaround is M29 to M30",
  topologyOrder(30, "leapfrog").slice(14, 17).join(","),
  "29,30,28",
);

assertEqual(
  "Leapfrog free negative is M1 negative",
  leapfrogSummary.freeNegative,
  "S-0001-M1-NEG",
);

assertEqual(
  "Leapfrog free positive is M2 positive",
  leapfrogSummary.freePositive,
  "S-0001-M2-POS",
);

assertEqual(
  "Twenty-four strings contain 720 modules",
  leapfrogSummary.moduleCount,
  720,
);

assertEqual(
  "Two 1.4 m leads pass the 2.606 m zero-gap reach screen",
  leapfrogScene.feasibility.passes,
  true,
);

const shortLeadScene = buildScene(
  baseInput({ positiveLeadM: 0.35, negativeLeadM: 0.28 }),
  cartridge,
);
assertClose(
  "Standard short leads fail by 1.976 m at zero gap",
  shortLeadScene.feasibility.shortfallM,
  1.976,
  1e-12,
);

const sequentialScene = buildScene(
  baseInput({ topology: "sequential" }),
  cartridge,
);
const sequentialSummary = deriveSummary(sequentialScene);
assertClose(
  "Sequential external cable exceeds leapfrog by one row span per string",
  sequentialSummary.externalCableM - leapfrogSummary.externalCableM,
  39.09 * 24,
  1e-9,
);

const customOrder = Array.from({ length: 30 }, (_, index) => index + 1)
  .reverse()
  .join(",");
assertEqual(
  "Valid custom order is accepted",
  topologyOrder(30, "custom", customOrder).length,
  30,
);

assertEqual(
  "Duplicate custom module numbers are rejected",
  topologyOrder(30, "custom", "1,1,2").length,
  0,
);

const root = document.getElementById("results");
let failures = 0;
results.forEach((result) => {
  const row = document.createElement("tr");
  const status = document.createElement("td");
  const name = document.createElement("td");
  const detail = document.createElement("td");

  status.textContent = result.pass ? "PASS" : "FAIL";
  status.className = result.pass ? "pass" : "fail";
  name.textContent = result.name;
  detail.textContent = result.pass
    ? String(result.actual)
    : `actual ${result.actual}; expected ${result.expected}`;

  row.append(status, name, detail);
  root.appendChild(row);
  if (!result.pass) {
    failures += 1;
  }
});

document.getElementById("overall").textContent = failures === 0
  ? `PASS · ${results.length} checks`
  : `FAIL · ${failures} of ${results.length} checks failed`;
document.getElementById("overall").className = failures === 0
  ? "pass"
  : "fail";
