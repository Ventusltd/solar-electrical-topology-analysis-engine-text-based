import { computeProject, parseIntegerList } from "./debug/engine.js";
import { runDebugTests } from "./debug/tests.js";

const byId = (id) => document.getElementById(id);
let latestProject = null;
let latestTests = null;

function value(id) {
  return byId(id).value;
}

function numeric(id) {
  return Number(value(id));
}

function collectInput() {
  return {
    mpptCount: numeric("mpptCount"),
    defaultInputsPerMppt: numeric("defaultInputsPerMppt"),
    allocationOverride: parseIntegerList(value("allocationOverride")),
    modulesPerString: numeric("modulesPerString"),
    topology: value("topology"),
    customOrder: parseIntegerList(value("customOrder")),
    moduleWidthM: numeric("moduleWidthM"),
    moduleGapM: numeric("moduleGapM"),
    positiveLeadM: numeric("positiveLeadM"),
    negativeLeadM: numeric("negativeLeadM"),
    routeOneWayM: numeric("routeOneWayM"),
    externalCableCsaMm2: numeric("externalCableCsaMm2"),
    factoryLeadCsaMm2: numeric("factoryLeadCsaMm2"),
    conductorTemperatureC: numeric("conductorTemperatureC"),
    moduleVocStcV: numeric("moduleVocStcV"),
    vocTempCoefficientPercentPerC: numeric("vocTempCoefficientPercentPerC"),
    cellTemperatureC: numeric("cellTemperatureC"),
    systemVoltageLimitV: numeric("systemVoltageLimitV"),
    operatingCurrentA: numeric("operatingCurrentA"),
  };
}

function downloadJson(filename, data) {
  const blob = new Blob([JSON.stringify(data, null, 2)], { type: "application/json" });
  const url = URL.createObjectURL(blob);
  const link = document.createElement("a");
  link.href = url;
  link.download = filename;
  link.click();
  URL.revokeObjectURL(url);
}

function renderTests(report) {
  const tbody = byId("tests");
  tbody.replaceChildren();
  report.results.forEach((result) => {
    const row = document.createElement("tr");
    row.innerHTML = `<td>${result.name}</td><td class="${result.status}">${result.status.toUpperCase()}</td><td>${result.detail}</td>`;
    tbody.appendChild(row);
  });
}

function renderWarnings(project) {
  const host = byId("warnings");
  host.replaceChildren();
  project.warnings.forEach((warning) => {
    const paragraph = document.createElement("p");
    paragraph.className = warning.severity === "error" ? "fail" : warning.severity;
    paragraph.textContent = `${warning.code}: ${warning.message}`;
    host.appendChild(paragraph);
  });
  const assumptions = document.createElement("ol");
  project.assumptions.forEach((assumption) => {
    const item = document.createElement("li");
    item.textContent = assumption;
    assumptions.appendChild(item);
  });
  host.appendChild(assumptions);
}

function renderString(project) {
  const selector = byId("selectedString");
  const previous = selector.value;
  selector.replaceChildren();
  project.strings.forEach((string) => {
    const option = document.createElement("option");
    option.value = string.id;
    option.textContent = `${string.id} · MPPT ${string.mppt} / input ${string.input}`;
    selector.appendChild(option);
  });
  if (project.strings.some((string) => string.id === previous)) selector.value = previous;
  const selected = project.strings.find((string) => string.id === selector.value) ?? project.strings[0];
  byId("stringReport").textContent = selected
    ? JSON.stringify({ id: selected.id, electricalOrder: selected.electricalOrder, calculations: selected.calculations, segments: selected.segments }, null, 2)
    : "No active string.";
}

function renderProject(project, tests) {
  const summary = byId("summary");
  const entries = [
    ["Requested strings", project.allocation.requestedStrings],
    ["Active strings", project.allocation.activeStrings],
    ["Total modules", project.totals.modules],
    ["Corrected module Voc", `${project.voltage.moduleVocCorrectedV.toFixed(2)} V`],
    ["String Voc", `${project.voltage.stringVocV.toFixed(2)} V`],
    ["Voltage utilisation", `${(project.voltage.utilisation * 100).toFixed(1)}%`],
    ["Home-run conductor", `${project.totals.homeRunLengthM.toFixed(2)} m`],
    ["Provisional extensions", `${project.totals.extensionLengthM.toFixed(2)} m`],
    ["Calculated resistive loss", `${project.totals.lossW.toFixed(2)} W`],
  ];
  summary.innerHTML = entries.map(([term, detail]) => `<dt>${term}</dt><dd>${detail}</dd>`).join("");
  renderWarnings(project);
  renderTests(tests);
  renderString(project);
  byId("reportPreview").textContent = JSON.stringify({ schema: project.schema, input: project.input, allocation: project.allocation, voltage: project.voltage, totals: project.totals, warnings: project.warnings }, null, 2);
  const status = byId("engineStatus");
  if (tests.failed > 0) {
    status.className = "status fail";
    status.textContent = `BLOCKED: ${tests.failed} deterministic test(s) failed.`;
  } else {
    status.className = "status pass";
    status.textContent = `ENGINE RUNNING: ${tests.passed} deterministic tests passed.`;
  }
}

function rebuild() {
  latestTests = runDebugTests();
  try {
    latestProject = computeProject(collectInput());
    renderProject(latestProject, latestTests);
  } catch (error) {
    latestProject = null;
    renderTests(latestTests);
    const status = byId("engineStatus");
    status.className = "status fail";
    status.textContent = `INPUT ERROR: ${error.message}`;
    byId("reportPreview").textContent = JSON.stringify({ error: error.message, field: error.field ?? null }, null, 2);
  }
}

document.querySelectorAll("input, select, textarea").forEach((control) => {
  if (control.id === "selectedString") return;
  control.addEventListener("input", rebuild);
  control.addEventListener("change", rebuild);
});
byId("selectedString").addEventListener("change", () => latestProject && renderString(latestProject));
byId("downloadReport").addEventListener("click", () => latestProject && downloadJson("v9-solar-dc-computation-report.json", { project: latestProject, tests: latestTests }));
byId("downloadTests").addEventListener("click", () => latestTests && downloadJson("v9-solar-dc-test-report.json", latestTests));

rebuild();
