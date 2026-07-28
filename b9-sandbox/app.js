import { CARTRIDGES, getCartridge } from "./cartridges.js";
import {
  buildScene,
  deriveSummary,
  modulePitch,
  rowSpan,
  toGeoJson,
} from "./model.js";

const SVG_NS = "http://www.w3.org/2000/svg";

const state = {
  view: "plan",
  scene: null,
  summary: null,
};

function byId(id) {
  return document.getElementById(id);
}

function numberValue(id, fallback) {
  const value = Number(byId(id).value);
  return Number.isFinite(value) ? value : fallback;
}

function integerValue(id, fallback) {
  return Math.max(1, Math.round(numberValue(id, fallback)));
}

function textValue(id) {
  return byId(id).value.trim();
}

function svgElement(name, attributes = {}) {
  const element = document.createElementNS(SVG_NS, name);
  Object.entries(attributes).forEach(([key, value]) => {
    element.setAttribute(key, String(value));
  });
  return element;
}

function addText(parent, x, y, text, className = "module-label") {
  const element = svgElement("text", { x, y, class: className });
  element.textContent = text;
  parent.appendChild(element);
  return element;
}

function clearSvg(svg) {
  while (svg.firstChild) {
    svg.removeChild(svg.firstChild);
  }
}

function inputModel() {
  return {
    moduleWidthM: numberValue("moduleWidth", 1.303),
    moduleHeightM: numberValue("moduleHeight", 2.384),
    moduleGapM: numberValue("moduleGap", 0),
    orientation: textValue("orientation"),
    positiveLeadM: numberValue("positiveLead", 1.4),
    negativeLeadM: numberValue("negativeLead", 1.4),
    junctionBoxMode: textValue("junctionBoxMode"),
    lowEdgeM: numberValue("lowEdge", 1),
    highEdgeM: numberValue("highEdge", 4),
    ridgeGapM: numberValue("ridgeGap", 0.3),
    rowPitchM: numberValue("rowPitch", 3),
    trackerAngleDeg: numberValue("trackerAngle", 0),
    inverterDistanceM: numberValue("inverterDistance", 10),
    modulesPerString: integerValue("modulesPerString", 30),
    stringCount: integerValue("stringCount", 24),
    topology: textValue("topology"),
    customOrder: textValue("customOrder"),
    externalCableCsaMm2: numberValue("externalCableCsa", 6),
    factoryLeadCsaMm2: numberValue("factoryLeadCsa", 4),
  };
}

function syncOrientationFromCartridge(cartridge) {
  if (cartridge.orientation) {
    byId("orientation").value = cartridge.orientation;
  }
}

function rebuild() {
  const cartridge = getCartridge(textValue("cartridge"));
  syncOrientationFromCartridge(cartridge);
  state.scene = buildScene(inputModel(), cartridge);
  state.summary = deriveSummary(state.scene);
  render();
}

function terminalPosition(module, polarity, scale, originX, originY) {
  const x = originX + module.xM * scale;
  const y = originY + module.yM * scale;
  const width = module.widthM * scale;
  const height = module.heightM * scale;
  const yTerminal = y + height * 0.35;
  return {
    x: polarity === "negative" ? x + width * 0.34 : x + width * 0.66,
    y: yTerminal,
  };
}

function drawModule(svg, module, scale, originX, originY, compact = false) {
  const x = originX + module.xM * scale;
  const y = originY + module.yM * scale;
  const width = Math.max(8, module.widthM * scale);
  const height = Math.max(12, module.heightM * scale);

  svg.appendChild(svgElement("rect", {
    x,
    y,
    width,
    height,
    rx: compact ? 1 : 3,
    class: "module-rect",
  }));

  if (!compact && width >= 24) {
    addText(
      svg,
      x + width / 2,
      y + height / 2 + 4,
      `M${module.moduleNumber}`,
    ).setAttribute("text-anchor", "middle");
  }

  const negative = terminalPosition(
    module,
    "negative",
    scale,
    originX,
    originY,
  );
  const positive = terminalPosition(
    module,
    "positive",
    scale,
    originX,
    originY,
  );

  svg.appendChild(svgElement("circle", {
    cx: negative.x,
    cy: negative.y,
    r: compact ? 1.5 : 3.5,
    class: "terminal-neg",
  }));
  svg.appendChild(svgElement("circle", {
    cx: positive.x,
    cy: positive.y,
    r: compact ? 1.5 : 3.5,
    class: "terminal-pos",
  }));
}

function renderPlan(svg) {
  const scene = state.scene;
  const maxWidthM = rowSpan(scene);
  const maxHeightM = Math.max(
    scene.module.heightM,
    (scene.electrical.stringCount - 1) * scene.geometry.rowPitchM
      + scene.module.heightM,
  );
  const scale = Math.min(950 / maxWidthM, 560 / maxHeightM, 24);
  const originX = 90;
  const originY = 70;
  const compact = scene.modules.length > 240;

  svg.setAttribute(
    "viewBox",
    `0 0 ${Math.max(1200, maxWidthM * scale + 180)} `
      + `${Math.max(700, maxHeightM * scale + 150)}`,
  );

  addText(svg, 36, 38, "PLAN VIEW", "view-title");
  addText(
    svg,
    36,
    62,
    `${scene.cartridge.name} · ${scene.electrical.stringCount} strings`,
  );

  scene.modules.forEach((module) => {
    drawModule(svg, module, scale, originX, originY, compact);
  });

  const inverterX = 20;
  const inverterY = originY;
  svg.appendChild(svgElement("rect", {
    x: inverterX,
    y: inverterY,
    width: 48,
    height: 88,
    rx: 6,
    class: "inverter",
  }));
  addText(svg, inverterX + 24, inverterY + 48, "INV").setAttribute(
    "text-anchor",
    "middle",
  );

  scene.strings.forEach((stringRecord, index) => {
    const y = originY + index * scene.geometry.rowPitchM * scale + 8;
    const route = svgElement("path", {
      d: `M ${inverterX + 48} ${inverterY + 22} `
        + `L ${originX - 14} ${y}`,
      class: "connection",
    });
    svg.appendChild(route);
  });

  addText(
    svg,
    originX,
    maxHeightM * scale + originY + 38,
    `Row span ${state.summary.rowSpanM.toFixed(2)} m · `
      + `local engineering coordinates`,
  );
}

function drawCircuitConnection(svg, from, to, isTurnaround) {
  const lift = Math.max(18, Math.abs(to.x - from.x) * 0.18);
  const direction = isTurnaround ? 1 : -1;
  const midY = Math.min(from.y, to.y) + direction * lift;
  const path = svgElement("path", {
    d: `M ${from.x} ${from.y} `
      + `C ${from.x} ${midY}, ${to.x} ${midY}, ${to.x} ${to.y}`,
    class: isTurnaround ? "connection turnaround" : "connection",
  });
  svg.appendChild(path);
}

function renderCircuit(svg) {
  const scene = state.scene;
  const selectedString = scene.strings[0];
  const modules = scene.modules.filter(
    (module) => module.stringId === selectedString.id,
  );
  const moduleWidthPx = 34;
  const moduleHeightPx = 62;
  const gapPx = 10;
  const originX = 150;
  const originY = 180;
  const scale = moduleWidthPx / modules[0].widthM;
  const totalWidth = modules.length * (moduleWidthPx + gapPx);

  svg.setAttribute(
    "viewBox",
    `0 0 ${Math.max(1350, totalWidth + 260)} 520`,
  );

  addText(svg, 36, 38, "CIRCUIT VIEW", "view-title");
  addText(
    svg,
    36,
    64,
    `${selectedString.id} · ${scene.electrical.topology} · `
      + `${selectedString.order.join(" → ")}`,
  );

  const physicalModules = modules.map((module, index) => ({
    ...module,
    xM: index * (moduleWidthPx + gapPx) / scale,
    yM: 0,
    widthM: moduleWidthPx / scale,
    heightM: moduleHeightPx / scale,
  }));

  physicalModules.forEach((module) => {
    drawModule(svg, module, scale, originX, originY, false);
  });

  const byNumber = new Map(
    physicalModules.map((module) => [module.moduleNumber, module]),
  );

  selectedString.connections.forEach((connection) => {
    const fromModule = byNumber.get(connection.fromModule);
    const toModule = byNumber.get(connection.toModule);
    const from = terminalPosition(
      fromModule,
      "positive",
      scale,
      originX,
      originY,
    );
    const to = terminalPosition(
      toModule,
      "negative",
      scale,
      originX,
      originY,
    );
    const isTurnaround = Math.abs(connection.toModule - connection.fromModule) === 1
      && scene.electrical.topology === "leapfrog"
      && connection.fromModule === Math.max(...selectedString.order.slice(0, -1));
    drawCircuitConnection(svg, from, to, isTurnaround);
  });

  const firstModule = byNumber.get(selectedString.order[0]);
  const finalModule = byNumber.get(
    selectedString.order[selectedString.order.length - 1],
  );
  const freeNegative = terminalPosition(
    firstModule,
    "negative",
    scale,
    originX,
    originY,
  );
  const freePositive = terminalPosition(
    finalModule,
    "positive",
    scale,
    originX,
    originY,
  );

  svg.appendChild(svgElement("rect", {
    x: 24,
    y: 150,
    width: 82,
    height: 120,
    rx: 8,
    class: "inverter",
  }));
  addText(svg, 65, 212, "INVERTER").setAttribute("text-anchor", "middle");

  svg.appendChild(svgElement("path", {
    d: `M 106 182 L ${freeNegative.x} ${freeNegative.y}`,
    class: "connection",
  }));
  svg.appendChild(svgElement("path", {
    d: `M 106 238 L ${freePositive.x} ${freePositive.y}`,
    class: "connection",
  }));
  addText(svg, 112, 176, "−");
  addText(svg, 112, 254, "+");

  const status = scene.feasibility.passes
    ? `Lead reach passes with ${(scene.feasibility.availableReachM
      - scene.feasibility.requiredReachM).toFixed(3)} m spare.`
    : `Lead reach fails by ${scene.feasibility.shortfallM.toFixed(3)} m.`;
  addText(svg, 36, 440, status);
}

function renderFixedSide(svg, scene) {
  const width = 920;
  const groundY = 500;
  const lowY = groundY - scene.geometry.lowEdgeM * 75;
  const highY = groundY - scene.geometry.highEdgeM * 75;
  const x0 = 150;
  const x1 = 900;

  svg.appendChild(svgElement("path", {
    d: `M 40 ${groundY} L 1120 ${groundY}`,
    class: "ground-line",
  }));
  svg.appendChild(svgElement("path", {
    d: `M ${x0} ${lowY} L ${x1} ${highY}`,
    class: "structure-line",
  }));

  const count = scene.cartridge.modulesHigh;
  for (let index = 0; index < count; index += 1) {
    const fraction0 = index / count;
    const fraction1 = (index + 1) / count;
    const sx = x0 + (x1 - x0) * fraction0;
    const ex = x0 + (x1 - x0) * fraction1;
    const sy = lowY + (highY - lowY) * fraction0;
    const ey = lowY + (highY - lowY) * fraction1;
    svg.appendChild(svgElement("path", {
      d: `M ${sx} ${sy} L ${ex} ${ey}`,
      class: "module-rect",
    }));
  }

  addText(svg, x0 - 70, lowY, `${scene.geometry.lowEdgeM.toFixed(2)} m`);
  addText(svg, x1 + 12, highY, `${scene.geometry.highEdgeM.toFixed(2)} m`);
}

function renderEastWestSide(svg, scene) {
  const groundY = 500;
  const centreX = 620;
  const ridgeY = groundY - scene.geometry.highEdgeM * 75;
  const lowY = groundY - scene.geometry.lowEdgeM * 75;
  const halfWidth = 360;

  svg.appendChild(svgElement("path", {
    d: `M 40 ${groundY} L 1200 ${groundY}`,
    class: "ground-line",
  }));
  svg.appendChild(svgElement("path", {
    d: `M ${centreX - halfWidth} ${lowY} L ${centreX} ${ridgeY} `
      + `L ${centreX + halfWidth} ${lowY}`,
    class: "structure-line",
  }));

  const count = scene.cartridge.modulesHigh;
  [-1, 1].forEach((direction) => {
    for (let index = 0; index < count; index += 1) {
      const f0 = index / count;
      const f1 = (index + 1) / count;
      const sx = centreX + direction * halfWidth * f0;
      const ex = centreX + direction * halfWidth * f1;
      const sy = ridgeY + (lowY - ridgeY) * f0;
      const ey = ridgeY + (lowY - ridgeY) * f1;
      svg.appendChild(svgElement("path", {
        d: `M ${sx} ${sy} L ${ex} ${ey}`,
        class: "module-rect",
      }));
    }
  });

  addText(svg, centreX - 40, ridgeY - 18, "RIDGE");
  addText(svg, centreX - halfWidth - 70, lowY, "EAST");
  addText(svg, centreX + halfWidth + 18, lowY, "WEST");
}

function renderTrackerSide(svg, scene) {
  const groundY = 500;
  const axisX = 620;
  const axisY = groundY - scene.geometry.highEdgeM * 75;
  const angle = scene.geometry.trackerAngleDeg * Math.PI / 180;
  const halfChord = 390;
  const dx = Math.cos(angle) * halfChord;
  const dy = Math.sin(angle) * halfChord;

  svg.appendChild(svgElement("path", {
    d: `M 40 ${groundY} L 1200 ${groundY}`,
    class: "ground-line",
  }));
  svg.appendChild(svgElement("path", {
    d: `M ${axisX} ${groundY} L ${axisX} ${axisY}`,
    class: "structure-line",
  }));
  svg.appendChild(svgElement("path", {
    d: `M ${axisX - dx} ${axisY + dy} L ${axisX + dx} ${axisY - dy}`,
    class: "structure-line",
  }));
  svg.appendChild(svgElement("circle", {
    cx: axisX,
    cy: axisY,
    r: 8,
    class: "terminal-pos",
  }));
  addText(svg, axisX + 16, axisY - 12, `${scene.geometry.trackerAngleDeg}°`);
}

function renderSide(svg) {
  const scene = state.scene;
  svg.setAttribute("viewBox", "0 0 1240 620");
  addText(svg, 36, 38, "SIDE VIEW", "view-title");
  addText(svg, 36, 64, scene.cartridge.name);

  if (scene.cartridge.tracker) {
    renderTrackerSide(svg, scene);
  } else if (scene.cartridge.eastWest) {
    renderEastWestSide(svg, scene);
  } else {
    renderFixedSide(svg, scene);
  }
}

function renderStage() {
  const svg = byId("stage");
  clearSvg(svg);

  if (state.view === "plan") {
    renderPlan(svg);
  } else if (state.view === "side") {
    renderSide(svg);
  } else {
    renderCircuit(svg);
  }
}

function setText(id, value, className = "") {
  const element = byId(id);
  element.textContent = value;
  element.className = className;
}

function renderSummary() {
  const scene = state.scene;
  const summary = state.summary;
  setText("summaryCartridge", scene.cartridge.name);
  setText("summaryOrientation", scene.module.orientation);
  setText("summaryModules", summary.moduleCount.toLocaleString("en-GB"));
  setText("summaryStrings", summary.stringCount.toLocaleString("en-GB"));
  setText("summaryRowSpan", `${summary.rowSpanM.toFixed(2)} m`);
  setText("summaryTopology", scene.electrical.topology);
  setText("summaryFreeNegative", summary.freeNegative);
  setText("summaryFreePositive", summary.freePositive);
  setText("summaryConnections", summary.connectionCount.toLocaleString("en-GB"));
  setText("summaryExternal", `${summary.externalCableM.toFixed(2)} m`);
  setText("summaryFactory", `${summary.factoryLeadM.toFixed(2)} m`);
  setText(
    "summaryCopper",
    `${summary.totalCommercialCopperKg.toFixed(2)} kg`,
  );

  const feasibilityClass = scene.feasibility.passes ? "pass" : "fail";
  const feasibilityText = scene.feasibility.passes
    ? `PASS · ${scene.feasibility.availableReachM.toFixed(3)} m available`
    : `FAIL · ${scene.feasibility.shortfallM.toFixed(3)} m short`;
  setText("summaryFeasibility", feasibilityText, feasibilityClass);

  const warningList = byId("warningList");
  warningList.replaceChildren();
  const warnings = scene.warnings.length
    ? scene.warnings
    : ["No blocking geometry or topology warnings in this first-pass screen."];
  warnings.forEach((warning) => {
    const item = document.createElement("li");
    item.textContent = warning;
    warningList.appendChild(item);
  });
}

function render() {
  renderStage();
  renderSummary();
  document.querySelectorAll("[data-view]").forEach((button) => {
    button.classList.toggle("active", button.dataset.view === state.view);
  });
}

function downloadJson(filename, payload) {
  const blob = new Blob([JSON.stringify(payload, null, 2)], {
    type: "application/json",
  });
  const link = document.createElement("a");
  link.href = URL.createObjectURL(blob);
  link.download = filename;
  link.click();
  URL.revokeObjectURL(link.href);
}

function populateCartridges() {
  const select = byId("cartridge");
  CARTRIDGES.forEach((cartridge) => {
    const option = document.createElement("option");
    option.value = cartridge.id;
    option.textContent = cartridge.name;
    select.appendChild(option);
  });
}

function installEvents() {
  document.querySelectorAll("input, select, textarea").forEach((control) => {
    control.addEventListener("input", rebuild);
    control.addEventListener("change", rebuild);
  });

  document.querySelectorAll("[data-view]").forEach((button) => {
    button.addEventListener("click", () => {
      state.view = button.dataset.view;
      render();
    });
  });

  byId("exportScene").addEventListener("click", () => {
    downloadJson("b9-scene.json", state.scene);
  });

  byId("exportGeoJson").addEventListener("click", () => {
    downloadJson("b9-scene.geojson", toGeoJson(state.scene));
  });

  byId("resetScene").addEventListener("click", () => {
    window.location.reload();
  });
}

populateCartridges();
installEvents();
rebuild();
