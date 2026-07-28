const byId = (id) => document.getElementById(id);
const SVG_NS = "http://www.w3.org/2000/svg";

function parseAllocation(value) {
  const counts = value
    .split(/[^0-9]+/)
    .map((item) => Number(item))
    .filter((item) => Number.isInteger(item) && item >= 0);
  return counts.length ? counts : [2];
}

function totalInputs(counts) {
  return counts.reduce((total, count) => total + count, 0);
}

function integerValue(id, fallback) {
  const value = Math.round(Number(byId(id)?.value));
  return Number.isFinite(value) && value > 0 ? value : fallback;
}

function svgElement(name, attributes = {}) {
  const element = document.createElementNS(SVG_NS, name);
  Object.entries(attributes).forEach(([key, value]) => {
    element.setAttribute(key, String(value));
  });
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
  if (topology === "mirrored-sequential") return sequential.reverse();
  if (topology === "alternating-return") {
    const order = [];
    let low = 1;
    let high = count;
    while (low <= high) {
      order.push(low);
      if (low !== high) order.push(high);
      low += 1;
      high -= 1;
    }
    return order;
  }
  if (topology === "leapfrog") {
    const odds = sequential.filter((number) => number % 2 === 1);
    const evens = sequential.filter((number) => number % 2 === 0).reverse();
    return odds.concat(evens);
  }
  if (topology === "custom") {
    const custom = (byId("customOrder")?.value || "")
      .split(/[^0-9]+/)
      .map(Number)
      .filter((number) => Number.isInteger(number) && number >= 1 && number <= count);
    if (custom.length === count && new Set(custom).size === count) return custom;
  }
  return sequential;
}

function buildStringSchedule() {
  const allocation = parseAllocation(byId("mpptInputs").value);
  const modules = integerValue("modulesPerString", 30);
  const topology = byId("topology").value;
  const order = topologyOrder(modules, topology);
  const rows = [];
  let stringNumber = 1;
  allocation.forEach((inputs, mpptIndex) => {
    for (let inputIndex = 1; inputIndex <= inputs; inputIndex += 1) {
      rows.push({
        mppt: mpptIndex + 1,
        input: inputIndex,
        string: stringNumber,
        id: `S-${String(stringNumber).padStart(4, "0")}`,
        modules,
        topology,
        order,
      });
      stringNumber += 1;
    }
  });
  return { allocation, rows, modules, topology };
}

function renderMpptSummary(counts) {
  const list = byId("mpptSummary");
  list.replaceChildren();
  counts.forEach((count, index) => {
    const item = document.createElement("li");
    item.textContent = `MPPT ${index + 1}: ${count} input${count === 1 ? "" : "s"}`;
    list.appendChild(item);
  });
  byId("mpptCount").textContent = String(counts.length);
  byId("derivedStringCount").textContent = String(totalInputs(counts));
}

function syncStringsFromMppts() {
  const counts = parseAllocation(byId("mpptInputs").value);
  const total = Math.max(1, totalInputs(counts));
  byId("stringCount").value = String(total);
  renderMpptSummary(counts);
  byId("stringCount").dispatchEvent(new Event("input", { bubbles: true }));
}

function installPresetControls() {
  const panel = byId("mpptInputs").closest("section");
  const actions = document.createElement("div");
  actions.className = "actions";
  actions.innerHTML = `
    <button type="button" data-allocation="2,2,2,2,2,2,2,2,2,2,2,2">24 strings · 12 MPPT</button>
    <button type="button" data-allocation="2,2,2,2,2,2,2,2,2,2,2,2,2,2,2,2">32 strings · 16 MPPT</button>
    <button type="button" data-allocation="1,2,4">Mixed 1/2/4</button>
  `;
  panel.appendChild(actions);
  actions.querySelectorAll("button").forEach((button) => {
    button.addEventListener("click", () => {
      byId("mpptInputs").value = button.dataset.allocation;
      syncStringsFromMppts();
    });
  });
}

function ensureSchedulePanel() {
  if (byId("inverterBlockSchedule")) return;
  const inspector = document.querySelector(".inspector");
  const section = document.createElement("section");
  section.className = "panel";
  section.innerHTML = `
    <h2>Inverter block schedule</h2>
    <p class="help">One row per physical inverter input. String quantity is derived from the MPPT allocation.</p>
    <div style="overflow:auto;max-height:440px">
      <table id="inverterBlockSchedule" style="width:100%;border-collapse:collapse;font-size:0.82rem">
        <thead><tr><th>MPPT</th><th>Input</th><th>String</th><th>Modules</th><th>Topology</th></tr></thead>
        <tbody></tbody>
      </table>
    </div>
  `;
  inspector.insertBefore(section, inspector.firstChild.nextSibling);
}

function renderSchedule() {
  ensureSchedulePanel();
  const { rows } = buildStringSchedule();
  const tbody = byId("inverterBlockSchedule").querySelector("tbody");
  tbody.replaceChildren();
  rows.forEach((row) => {
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

function circuitViewActive() {
  return document.querySelector('[data-view="circuit"]')?.classList.contains("active");
}

function renderFullInverterBlock() {
  if (!circuitViewActive()) return;
  const stage = byId("stage");
  const { allocation, rows, modules, topology } = buildStringSchedule();
  const orientation = byId("orientation").value;
  const cartridgeLabel = byId("cartridge").selectedOptions[0]?.textContent || "Array";
  const moduleWidth = orientation === "portrait" ? 13 : 22;
  const moduleHeight = orientation === "portrait" ? 22 : 13;
  const moduleGap = 3;
  const labelWidth = 150;
  const rowHeight = Math.max(34, moduleHeight + 12);
  const mpptGap = 18;
  const maxInputs = Math.max(1, ...allocation);
  const canvasWidth = Math.max(1100, labelWidth + modules * (moduleWidth + moduleGap) + 90);
  const canvasHeight = Math.max(520, 120 + rows.length * rowHeight + allocation.length * mpptGap);

  stage.replaceChildren();
  stage.setAttribute("viewBox", `0 0 ${canvasWidth} ${canvasHeight}`);
  addSvgText(stage, 28, 32, "FULL INVERTER BLOCK · CIRCUIT VIEW", "view-title");
  addSvgText(stage, 28, 58, `${cartridgeLabel} · ${orientation} · ${allocation.length} MPPT · ${rows.length} strings · ${modules} modules/string`);
  addSvgText(stage, 28, 82, `Topology: ${topology} · total modules: ${rows.length * modules}`);

  let y = 112;
  let rowIndex = 0;
  allocation.forEach((inputCount, mpptIndex) => {
    const groupHeight = Math.max(1, inputCount) * rowHeight + 10;
    stage.appendChild(svgElement("rect", {
      x: 20,
      y: y - 18,
      width: canvasWidth - 40,
      height: groupHeight + 14,
      rx: 8,
      class: "mppt-group",
      fill: "none",
      stroke: "currentColor",
      "stroke-opacity": 0.18,
    }));
    addSvgText(stage, 34, y, `MPPT ${mpptIndex + 1}`, "view-title");
    if (inputCount === 0) {
      addSvgText(stage, labelWidth, y, "unused MPPT");
      y += rowHeight + mpptGap;
      return;
    }

    for (let inputIndex = 1; inputIndex <= inputCount; inputIndex += 1) {
      const row = rows[rowIndex];
      const cy = y + (inputIndex - 1) * rowHeight + 14;
      const mpptX = 92;
      stage.appendChild(svgElement("rect", {
        x: 28,
        y: cy - 13,
        width: 106,
        height: 27,
        rx: 5,
        class: "inverter",
      }));
      addSvgText(stage, 81, cy + 4, `IN ${inputIndex} · ${row.id}`, "module-label", "middle");
      stage.appendChild(svgElement("path", {
        d: `M 134 ${cy} L ${labelWidth - 7} ${cy}`,
        class: "connection",
      }));

      for (let moduleIndex = 0; moduleIndex < modules; moduleIndex += 1) {
        const x = labelWidth + moduleIndex * (moduleWidth + moduleGap);
        stage.appendChild(svgElement("rect", {
          x,
          y: cy - moduleHeight / 2,
          width: moduleWidth,
          height: moduleHeight,
          rx: 1.5,
          class: "module-rect",
        }));
        if (modules <= 40 && moduleIndex % Math.max(1, Math.ceil(modules / 10)) === 0) {
          addSvgText(stage, x + moduleWidth / 2, cy + 3, String(moduleIndex + 1), "module-label", "middle");
        }
      }
      addSvgText(stage, labelWidth + modules * (moduleWidth + moduleGap) + 8, cy + 4, `${modules}S`);
      rowIndex += 1;
    }
    y += inputCount * rowHeight + mpptGap;
  });

  addSvgText(stage, 28, canvasHeight - 22, `Each row is one independent string input. MPPT groups share tracking but strings remain electrically parallel at the MPPT.`);
  renderSchedule();
}

let renderingCustom = false;
function installCircuitObserver() {
  const stage = byId("stage");
  const observer = new MutationObserver(() => {
    if (renderingCustom || !circuitViewActive()) return;
    renderingCustom = true;
    queueMicrotask(() => {
      renderFullInverterBlock();
      renderingCustom = false;
    });
  });
  observer.observe(stage, { childList: true, subtree: true });
  document.querySelectorAll("input, select, textarea, [data-view]").forEach((control) => {
    control.addEventListener("input", () => queueMicrotask(renderFullInverterBlock));
    control.addEventListener("change", () => queueMicrotask(renderFullInverterBlock));
    control.addEventListener("click", () => queueMicrotask(renderFullInverterBlock));
  });
}

byId("mpptInputs").addEventListener("input", syncStringsFromMppts);
byId("mpptInputs").addEventListener("change", syncStringsFromMppts);

await import("../b9-sandbox/app.js");
installPresetControls();
ensureSchedulePanel();
syncStringsFromMppts();
renderSchedule();
installCircuitObserver();
