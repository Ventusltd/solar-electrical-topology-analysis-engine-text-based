const byId = (id) => document.getElementById(id);
const SVG_NS = "http://www.w3.org/2000/svg";
const MAX_MPPTS = 100;
const MAX_INPUTS_PER_MPPT = 4;
const MAX_ACTIVE_STRINGS = 24;
const MAX_MODULES_PER_STRING = 30;

function clampInteger(value, minimum, maximum, fallback) {
  const parsed = Math.round(Number(value));
  return Number.isFinite(parsed)
    ? Math.min(maximum, Math.max(minimum, parsed))
    : fallback;
}

function numberValue(id, fallback) {
  const parsed = Number(byId(id)?.value);
  return Number.isFinite(parsed) ? parsed : fallback;
}

function parseAllocationText(value) {
  return value
    .split(/[^0-9]+/)
    .filter(Boolean)
    .map(Number)
    .filter(Number.isFinite)
    .map((count) => clampInteger(count, 0, MAX_INPUTS_PER_MPPT, 0));
}

function allocationModel() {
  const requestedMppts = clampInteger(byId("mpptQuantity").value, 1, MAX_MPPTS, 12);
  const defaultInputs = clampInteger(
    byId("defaultInputsPerMppt").value,
    0,
    MAX_INPUTS_PER_MPPT,
    2,
  );
  const override = parseAllocationText(byId("mpptInputs").value.trim());
  const allocation = override.length
    ? Array.from({ length: requestedMppts }, (_, index) => override[index] ?? 0)
    : Array(requestedMppts).fill(defaultInputs);

  let remaining = MAX_ACTIVE_STRINGS;
  const limited = allocation.map((count) => {
    const accepted = Math.min(count, remaining);
    remaining -= accepted;
    return accepted;
  });

  return {
    requestedMppts,
    defaultInputs,
    requestedAllocation: allocation,
    allocation: limited,
    requestedStrings: allocation.reduce((sum, count) => sum + count, 0),
    activeStrings: limited.reduce((sum, count) => sum + count, 0),
    truncated: allocation.some((count, index) => count !== limited[index]),
  };
}

function svgElement(name, attributes = {}) {
  const element = document.createElementNS(SVG_NS, name);
  Object.entries(attributes).forEach(([key, value]) => element.setAttribute(key, String(value)));
  return element;
}

function addSvgText(parent, x, y, text, className = "module-label", anchor = "start") {
  const element = svgElement("text", { x, y, class: className, "text-anchor": anchor });
  element.textContent = text;
  parent.appendChild(element);
  return element;
}

function topologyOrder(count, topology) {
  const sequential = Array.from({ length: count }, (_, index) => index + 1);
  if (topology === "mirrored-sequential") return [...sequential].reverse();
  if (topology === "alternating-return") {
    const result = [];
    let low = 1;
    let high = count;
    while (low <= high) {
      result.push(low);
      if (low !== high) result.push(high);
      low += 1;
      high -= 1;
    }
    return result;
  }
  if (topology === "leapfrog") {
    return sequential.filter((number) => number % 2 === 1)
      .concat(sequential.filter((number) => number % 2 === 0).reverse());
  }
  if (topology === "custom") {
    const custom = parseAllocationText(byId("customOrder")?.value || "")
      .filter((number) => number >= 1 && number <= count);
    if (custom.length === count && new Set(custom).size === count) return custom;
  }
  return sequential;
}

function voltageModel(modules) {
  const voc = Math.max(0, numberValue("moduleVoc", 50));
  const coefficientPercent = numberValue("vocTempCoefficient", -0.24);
  const temperature = numberValue("designTemperature", 20);
  const limit = Math.max(1, numberValue("systemVoltageLimit", 1500));
  const correctedVoc = voc * (1 + (coefficientPercent / 100) * (temperature - 25));
  const stringVoc = correctedVoc * modules;
  const utilisation = stringVoc / limit;
  return { voc, correctedVoc, stringVoc, utilisation, limit, temperature };
}

function cableModel(strings, modules, topology) {
  const routeOneWay = Math.max(0, numberValue("inverterDistance", 10));
  const positiveLead = Math.max(0, numberValue("positiveLead", 1.4));
  const negativeLead = Math.max(0, numberValue("negativeLead", 1.4));
  const moduleWidth = Math.max(0.1, numberValue("moduleWidth", 1.303));
  const gap = Math.max(0, numberValue("moduleGap", 0));
  const rowSpan = modules * moduleWidth + Math.max(0, modules - 1) * gap;
  const farEndReturnPerString = topology === "sequential" ? rowSpan : 0;
  const externalPerString = 2 * routeOneWay + farEndReturnPerString;
  const factoryPerString = modules * (positiveLead + negativeLead);
  return {
    rowSpan,
    farEndReturnPerString,
    externalPerString,
    externalTotal: strings * externalPerString,
    factoryTotal: strings * factoryPerString,
    totalConductor: strings * (externalPerString + factoryPerString),
  };
}

function buildStringSchedule() {
  const allocation = allocationModel();
  const modules = clampInteger(
    byId("modulesPerString").value,
    1,
    MAX_MODULES_PER_STRING,
    30,
  );
  const topology = byId("topology").value;
  const order = topologyOrder(modules, topology);
  const rows = [];
  let stringNumber = 1;
  allocation.allocation.forEach((inputs, mpptIndex) => {
    for (let input = 1; input <= inputs; input += 1) {
      rows.push({
        mppt: mpptIndex + 1,
        input,
        string: stringNumber,
        id: `S-${String(stringNumber).padStart(4, "0")}`,
        modules,
        topology,
        order: [...order],
      });
      stringNumber += 1;
    }
  });
  return {
    allocation,
    rows,
    modules,
    topology,
    order,
    voltage: voltageModel(modules),
    cable: cableModel(rows.length, modules, topology),
  };
}

function syncAllocation() {
  const model = allocationModel();
  byId("mpptQuantity").value = String(model.requestedMppts);
  byId("defaultInputsPerMppt").value = String(model.defaultInputs);
  byId("stringCount").value = String(Math.max(1, model.activeStrings));
  byId("mpptCount").textContent = String(model.requestedMppts);
  byId("derivedStringCount").textContent = String(model.activeStrings);

  const list = byId("mpptSummary");
  list.replaceChildren();
  model.allocation.forEach((count, index) => {
    if (count === 0 && model.requestedMppts > 24) return;
    const item = document.createElement("li");
    item.textContent = `MPPT ${index + 1}: ${count} active string input${count === 1 ? "" : "s"}`;
    list.appendChild(item);
  });

  byId("stringCount").dispatchEvent(new Event("input", { bubbles: true }));
}

function ensureSchedulePanel() {
  if (byId("inverterBlockSchedule")) return;
  const section = document.createElement("section");
  section.className = "panel";
  section.innerHTML = `
    <h2>Inverter input schedule</h2>
    <p class="help">One row per active physical string input.</p>
    <div style="overflow:auto;max-height:440px">
      <table id="inverterBlockSchedule" style="width:100%;border-collapse:collapse;font-size:0.82rem">
        <thead><tr><th>MPPT</th><th>Input</th><th>String</th><th>Modules</th><th>Order</th></tr></thead>
        <tbody></tbody>
      </table>
    </div>`;
  document.querySelector(".inspector").insertBefore(section, document.querySelector(".inspector").children[2]);
}

function renderSchedule(model) {
  ensureSchedulePanel();
  const tbody = byId("inverterBlockSchedule").querySelector("tbody");
  tbody.replaceChildren();
  model.rows.forEach((row) => {
    const tr = document.createElement("tr");
    [row.mppt, row.input, row.id, row.modules, row.topology].forEach((value) => {
      const td = document.createElement("td");
      td.textContent = String(value);
      td.style.padding = "0.35rem 0.25rem";
      td.style.borderBottom = "1px solid rgba(120,150,170,0.25)";
      tr.appendChild(td);
    });
    tbody.appendChild(tr);
  });
}

function setComputedResults(model) {
  const activeMppts = model.allocation.allocation.filter((count) => count > 0).length;
  byId("computedVoltage").textContent = `${model.voltage.stringVoc.toFixed(1)} V @ ${model.voltage.temperature.toFixed(0)}°C`;
  byId("computedVoltageUse").textContent = `${(model.voltage.utilisation * 100).toFixed(1)}% of ${model.voltage.limit.toFixed(0)} V`;
  byId("computedActiveMppts").textContent = `${activeMppts} / ${model.allocation.requestedMppts}`;
  byId("computedTotalModules").textContent = String(model.rows.length * model.modules);
  byId("computedExternalCable").textContent = `${model.cable.externalTotal.toFixed(1)} m`;
  byId("computedTotalCable").textContent = `${model.cable.totalConductor.toFixed(1)} m`;

  const warnings = [];
  if (model.allocation.truncated) {
    warnings.push(`RED: requested ${model.allocation.requestedStrings} strings; V9 east-west phase is capped at ${MAX_ACTIVE_STRINGS}.`);
  }
  if (model.voltage.utilisation >= 1) {
    warnings.push(`RED: calculated open-circuit string voltage ${model.voltage.stringVoc.toFixed(1)} V meets or exceeds the ${model.voltage.limit.toFixed(0)} V system limit.`);
  } else if (model.voltage.utilisation >= 0.95) {
    warnings.push(`RED: calculated open-circuit string voltage is ${(model.voltage.utilisation * 100).toFixed(1)}% of the ${model.voltage.limit.toFixed(0)} V system limit.`);
  }
  if (model.voltage.limit === 3000) {
    warnings.push("3 kV is shown as a future-study mode only; component, connector, cable, clearance and standards validation is not yet implemented.");
  }
  if (model.topology === "sequential") {
    warnings.push(`Sequential topology adds an estimated ${model.cable.farEndReturnPerString.toFixed(2)} m far-end return conductor per string.`);
  }
  if (!warnings.length) warnings.push("No V9 allocation or voltage-gate warning.");
  const list = byId("v9WarningList");
  list.replaceChildren();
  warnings.forEach((warning) => {
    const item = document.createElement("li");
    item.textContent = warning;
    if (warning.startsWith("RED:")) item.className = "fail";
    list.appendChild(item);
  });
}

function drawTopologyPath(stage, points, order, y, moduleWidth, moduleGap, startX) {
  const terminals = new Map(points.map((point) => [point.number, point]));
  for (let index = 0; index < order.length - 1; index += 1) {
    const from = terminals.get(order[index]);
    const to = terminals.get(order[index + 1]);
    const fromX = from.x + moduleWidth * 0.68;
    const toX = to.x + moduleWidth * 0.32;
    const lift = Math.max(7, Math.abs(toX - fromX) * 0.12);
    const direction = index % 2 === 0 ? -1 : 1;
    stage.appendChild(svgElement("path", {
      d: `M ${fromX} ${y} C ${fromX} ${y + direction * lift}, ${toX} ${y + direction * lift}, ${toX} ${y}`,
      class: "connection",
    }));
  }
  const first = terminals.get(order[0]);
  const last = terminals.get(order[order.length - 1]);
  stage.appendChild(svgElement("path", {
    d: `M ${startX} ${y - 5} L ${first.x + moduleWidth * 0.32} ${y}`,
    class: "connection",
  }));
  stage.appendChild(svgElement("path", {
    d: `M ${startX} ${y + 5} L ${last.x + moduleWidth * 0.68} ${y}`,
    class: "connection",
  }));
}

function circuitViewActive() {
  return document.querySelector('[data-view="circuit"]')?.classList.contains("active");
}

function renderFullInverterBlock() {
  const model = buildStringSchedule();
  setComputedResults(model);
  renderSchedule(model);
  if (!circuitViewActive()) return;

  const stage = byId("stage");
  const orientation = byId("orientation").value;
  const cartridge = byId("cartridge").selectedOptions[0]?.textContent || "East-west";
  const moduleWidth = orientation === "portrait" ? 15 : 23;
  const moduleHeight = orientation === "portrait" ? 25 : 15;
  const moduleGap = 4;
  const left = 176;
  const rowHeight = Math.max(42, moduleHeight + 17);
  const mpptGap = 18;
  const width = Math.max(1180, left + model.modules * (moduleWidth + moduleGap) + 100);
  const height = Math.max(620, 130 + model.rows.length * rowHeight + model.allocation.requestedMppts * mpptGap);

  stage.replaceChildren();
  stage.setAttribute("viewBox", `0 0 ${width} ${height}`);
  addSvgText(stage, 28, 32, "EAST-WEST FULL DC BLOCK · AUTO-COMPUTED CIRCUIT", "view-title");
  addSvgText(stage, 28, 58, `${cartridge} · ${model.allocation.requestedMppts} MPPT · ${model.rows.length} active strings · ${model.modules} modules/string`);
  addSvgText(stage, 28, 82, `${model.topology} · ${model.voltage.stringVoc.toFixed(1)} V @ ${model.voltage.temperature.toFixed(0)}°C · ${model.cable.totalConductor.toFixed(1)} m estimated DC conductor`);

  let y = 120;
  let rowIndex = 0;
  model.allocation.allocation.forEach((inputCount, mpptIndex) => {
    const groupRows = Math.max(1, inputCount);
    const groupHeight = groupRows * rowHeight + 12;
    stage.appendChild(svgElement("rect", {
      x: 18, y: y - 18, width: width - 36, height: groupHeight, rx: 8,
      fill: "none", stroke: "currentColor", "stroke-opacity": 0.16,
    }));
    addSvgText(stage, 32, y, `MPPT ${mpptIndex + 1}`, "view-title");
    if (inputCount === 0) {
      addSvgText(stage, 110, y, "unused");
      y += rowHeight + mpptGap;
      return;
    }

    for (let input = 1; input <= inputCount; input += 1) {
      const row = model.rows[rowIndex];
      const cy = y + (input - 1) * rowHeight + 15;
      stage.appendChild(svgElement("rect", { x: 26, y: cy - 14, width: 126, height: 28, rx: 5, class: "inverter" }));
      addSvgText(stage, 89, cy + 4, `IN ${input} · ${row.id}`, "module-label", "middle");
      const points = [];
      for (let moduleIndex = 0; moduleIndex < model.modules; moduleIndex += 1) {
        const x = left + moduleIndex * (moduleWidth + moduleGap);
        points.push({ number: moduleIndex + 1, x });
        stage.appendChild(svgElement("rect", {
          x, y: cy - moduleHeight / 2, width: moduleWidth, height: moduleHeight, rx: 1.5, class: "module-rect",
        }));
        if (model.modules <= 30) addSvgText(stage, x + moduleWidth / 2, cy + 3, String(moduleIndex + 1), "module-label", "middle");
      }
      drawTopologyPath(stage, points, row.order, cy, moduleWidth, moduleGap, 152);
      addSvgText(stage, left + model.modules * (moduleWidth + moduleGap) + 8, cy + 4, `${model.modules}S`);
      rowIndex += 1;
    }
    y += inputCount * rowHeight + mpptGap;
  });

  addSvgText(stage, 28, height - 24, `Cable basis: ${model.cable.externalTotal.toFixed(1)} m external + ${model.cable.factoryTotal.toFixed(1)} m factory leads. Sequential far-end return is included automatically.`);
}

function installPresetControls() {
  const panel = byId("mpptQuantity").closest("section");
  const actions = document.createElement("div");
  actions.className = "actions";
  actions.innerHTML = `
    <button type="button" data-mppt="12" data-inputs="2">24 strings · 12 MPPT</button>
    <button type="button" data-mppt="8" data-inputs="3">24 strings · 8 MPPT</button>
    <button type="button" data-mppt="6" data-inputs="4">24 strings · 6 MPPT</button>
    <button type="button" data-allocation="1,2,4,1,2,4,1,2,4,1,1,1">Mixed allocation</button>`;
  panel.appendChild(actions);
  actions.querySelectorAll("button").forEach((button) => {
    button.addEventListener("click", () => {
      if (button.dataset.allocation) {
        byId("mpptQuantity").value = String(button.dataset.allocation.split(",").length);
        byId("mpptInputs").value = button.dataset.allocation;
      } else {
        byId("mpptQuantity").value = button.dataset.mppt;
        byId("defaultInputsPerMppt").value = button.dataset.inputs;
        byId("mpptInputs").value = "";
      }
      syncAllocation();
      queueMicrotask(renderFullInverterBlock);
    });
  });
}

let customRendering = false;
function installObservers() {
  const stage = byId("stage");
  const observer = new MutationObserver(() => {
    if (customRendering || !circuitViewActive()) return;
    customRendering = true;
    queueMicrotask(() => {
      renderFullInverterBlock();
      customRendering = false;
    });
  });
  observer.observe(stage, { childList: true, subtree: true });

  document.querySelectorAll("input, select, textarea, [data-view]").forEach((control) => {
    const update = () => {
      if (["mpptQuantity", "defaultInputsPerMppt", "mpptInputs"].includes(control.id)) syncAllocation();
      if (control.id === "modulesPerString") {
        control.value = String(clampInteger(control.value, 1, MAX_MODULES_PER_STRING, 30));
      }
      queueMicrotask(renderFullInverterBlock);
    };
    control.addEventListener("input", update);
    control.addEventListener("change", update);
    control.addEventListener("click", update);
  });
}

await import("../b9-sandbox/app.js");
installPresetControls();
ensureSchedulePanel();
syncAllocation();
renderFullInverterBlock();
installObservers();