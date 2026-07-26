'use strict';

const DEFAULT_MODEL = `# SOLAR ELECTRICAL TOPOLOGY MODEL V1
# Generic reproducible example. Units are explicit.

MODEL_NAME = Generic_30_Module_String
MODULE_COUNT = 30
MODULE_VMP_V = 38.1
MODULE_IMP_A = 17.35
MODULE_FRAME_CAP_NF = 100

CABLE_LENGTH_M = 200
CABLE_CSA_MM2 = 6
CABLE_MATERIAL = copper
CONDUCTOR_OD_MM = 6.4
CONDUCTOR_CENTRE_SPACING_MM = 20
RELATIVE_PERMITTIVITY = 2.3

FRAME_BONDED = true
INVERTER_INPUT_CAP_NF = 0
`;

const RHO = Object.freeze({
  copper: 0.017241,
  aluminium: 0.028264
});

const MU0 = 4 * Math.PI * 1e-7;
const EPS0 = 8.8541878128e-12;

const REQUIRED_KEYS = [
  'MODULE_COUNT',
  'MODULE_VMP_V',
  'MODULE_IMP_A',
  'MODULE_FRAME_CAP_NF',
  'CABLE_LENGTH_M',
  'CABLE_CSA_MM2',
  'CABLE_MATERIAL',
  'CONDUCTOR_OD_MM',
  'CONDUCTOR_CENTRE_SPACING_MM',
  'RELATIVE_PERMITTIVITY'
];

let latest = null;

const el = id => document.getElementById(id);
const fmt = (value, decimals = 3) => Number.isFinite(value)
  ? value.toLocaleString('en-GB', { minimumFractionDigits: decimals, maximumFractionDigits: decimals })
  : '0';

function parseModel(text) {
  const data = {};
  const errors = [];
  const warnings = [];

  text.split(/\r?\n/).forEach((raw, index) => {
    const line = raw.trim();
    if (!line || line.startsWith('#')) return;
    const eq = line.indexOf('=');
    if (eq < 1) {
      errors.push(`Line ${index + 1}: expected KEY = VALUE`);
      return;
    }
    const key = line.slice(0, eq).trim().toUpperCase();
    const value = line.slice(eq + 1).trim();
    if (!key) errors.push(`Line ${index + 1}: missing key`);
    else data[key] = value;
  });

  REQUIRED_KEYS.forEach(key => {
    if (!(key in data)) errors.push(`Missing required key: ${key}`);
  });

  const number = (key, minExclusive = null) => {
    const value = Number(data[key]);
    if (!Number.isFinite(value)) {
      errors.push(`${key} must be numeric`);
      return 0;
    }
    if (minExclusive !== null && value <= minExclusive) {
      errors.push(`${key} must be greater than ${minExclusive}`);
    }
    return value;
  };

  const model = {
    modelName: data.MODEL_NAME || 'Unnamed_Model',
    moduleCount: Math.round(number('MODULE_COUNT', 0)),
    moduleVmpV: number('MODULE_VMP_V', 0),
    moduleImpA: number('MODULE_IMP_A', 0),
    moduleFrameCapNf: number('MODULE_FRAME_CAP_NF', -1),
    cableLengthM: number('CABLE_LENGTH_M', 0),
    cableCsaMm2: number('CABLE_CSA_MM2', 0),
    cableMaterial: String(data.CABLE_MATERIAL || '').toLowerCase(),
    conductorOdMm: number('CONDUCTOR_OD_MM', 0),
    conductorSpacingMm: number('CONDUCTOR_CENTRE_SPACING_MM', 0),
    relativePermittivity: number('RELATIVE_PERMITTIVITY', 0),
    frameBonded: String(data.FRAME_BONDED || 'false').toLowerCase() === 'true',
    inverterInputCapNf: Number(data.INVERTER_INPUT_CAP_NF || 0)
  };

  if (!(model.cableMaterial in RHO)) errors.push('CABLE_MATERIAL must be copper or aluminium');
  if (model.conductorSpacingMm <= model.conductorOdMm) {
    errors.push('CONDUCTOR_CENTRE_SPACING_MM must exceed CONDUCTOR_OD_MM');
  }
  if (model.moduleFrameCapNf === 0) warnings.push('Module-to-frame capacitance is zero, so electric stored energy is suppressed.');
  if (!model.frameBonded) warnings.push('Frame is declared unbonded. Earth-referenced interpretation requires care.');
  if (model.inverterInputCapNf < 0) errors.push('INVERTER_INPUT_CAP_NF cannot be negative');

  return { model, errors, warnings };
}

function calculate(model) {
  const rho = RHO[model.cableMaterial];
  const stringVmp = model.moduleCount * model.moduleVmpV;
  const stringPowerW = stringVmp * model.moduleImpA;
  const loopResistance = 2 * model.cableLengthM * rho / model.cableCsaMm2;
  const voltageDrop = model.moduleImpA * loopResistance;
  const voltageDropPct = stringVmp > 0 ? voltageDrop / stringVmp * 100 : 0;
  const cableLossW = model.moduleImpA ** 2 * loopResistance;
  const cableLossPct = stringPowerW > 0 ? cableLossW / stringPowerW * 100 : 0;

  const radiusM = model.conductorOdMm / 2000;
  const spacingM = model.conductorSpacingMm / 1000;
  const geometryRatio = spacingM / (2 * radiusM);
  const acoshTerm = Math.acosh(geometryRatio);

  const loopInductancePerM = MU0 / Math.PI * acoshTerm;
  const pairCapacitancePerM = Math.PI * EPS0 * model.relativePermittivity / acoshTerm;
  const loopInductanceH = loopInductancePerM * model.cableLengthM;
  const pairCapacitanceF = pairCapacitancePerM * model.cableLengthM;

  const moduleEarthCapF = model.moduleCount * model.moduleFrameCapNf * 1e-9;
  const inverterCapF = model.inverterInputCapNf * 1e-9;
  const totalEarthCapF = moduleEarthCapF + inverterCapF;

  const magneticEnergyJ = 0.5 * loopInductanceH * model.moduleImpA ** 2;
  const electricEnergyJ = 0.5 * totalEarthCapF * stringVmp ** 2;
  const characteristicImpedance = Math.sqrt(loopInductancePerM / pairCapacitancePerM);
  const propagationVelocity = 1 / Math.sqrt(loopInductancePerM * pairCapacitancePerM);
  const oneWayDelayS = model.cableLengthM / propagationVelocity;

  const warnings = [];
  if (voltageDropPct > 1) warnings.push(`Voltage drop is ${fmt(voltageDropPct, 2)}%, above a 1% screening marker.`);
  if (cableLossPct > 1) warnings.push(`Cable loss is ${fmt(cableLossPct, 2)}% of string operating power.`);
  if (model.moduleFrameCapNf > 1000) warnings.push('Declared module-to-frame capacitance is unusually high and should be verified by measurement or manufacturer evidence.');
  if (model.conductorSpacingMm / model.conductorOdMm < 1.2) warnings.push('Conductors are very close. Confirm that centre spacing exceeds physical cable diameter in the actual route.');

  return {
    stringVmp,
    stringPowerW,
    loopResistance,
    voltageDrop,
    voltageDropPct,
    cableLossW,
    cableLossPct,
    loopInductancePerM,
    pairCapacitancePerM,
    loopInductanceH,
    pairCapacitanceF,
    moduleEarthCapF,
    inverterCapF,
    totalEarthCapF,
    magneticEnergyJ,
    electricEnergyJ,
    characteristicImpedance,
    propagationVelocity,
    oneWayDelayS,
    acoshTerm,
    warnings
  };
}

function setText(id, value) {
  const node = el(id);
  if (node) node.textContent = value;
}

function renderNetwork(model, result) {
  el('network-view').innerHTML = `
    <article class="net-block module">
      <h3>PV String</h3>
      <p>${model.moduleCount} modules in series</p>
      <p>${fmt(result.stringVmp, 1)} Vmp</p>
      <p>${fmt(model.moduleImpA, 2)} A</p>
    </article>
    <div class="net-arrow">→</div>
    <article class="net-block cable">
      <h3>DC Loop</h3>
      <p>${fmt(model.cableLengthM, 1)} m one-way</p>
      <p>${fmt(model.cableCsaMm2, 1)} mm² ${model.cableMaterial}</p>
      <p>${fmt(model.conductorSpacingMm, 1)} mm centres</p>
    </article>
    <div class="net-arrow">→</div>
    <article class="net-block inverter">
      <h3>MPPT Input</h3>
      <p>One string input</p>
      <p>${fmt(model.inverterInputCapNf, 1)} nF declared input C</p>
      <p>V1 steady-state and geometry model</p>
    </article>
    <div class="earth-row">
      <article class="net-block earth">
        <h3>Frame / Earth Path</h3>
        <p>${fmt(model.moduleCount * model.moduleFrameCapNf, 1)} nF module contribution</p>
        <p>Frame bonded: ${model.frameBonded ? 'YES' : 'NO'}</p>
      </article>
    </div>`;
}

function buildTrace(model, result, warnings) {
  return [
    'SOLAR ELECTRICAL TOPOLOGY ANALYSIS ENGINE V1',
    `MODEL          ${model.modelName}`,
    `STATUS         ${warnings.length ? 'CHECK WARNINGS' : 'CALCULATED'}`,
    '',
    '01 STRING OPERATING POINT',
    `Vmp            ${model.moduleCount} × ${fmt(model.moduleVmpV, 3)} V = ${fmt(result.stringVmp, 3)} V`,
    `Power          ${fmt(result.stringVmp, 3)} V × ${fmt(model.moduleImpA, 3)} A = ${fmt(result.stringPowerW, 3)} W`,
    '',
    '02 LOOP RESISTANCE',
    `ρ              ${fmt(RHO[model.cableMaterial], 6)} Ω·mm²/m`,
    `Rloop          2 × ${fmt(model.cableLengthM, 3)} × ρ / ${fmt(model.cableCsaMm2, 3)}`,
    `Rloop          ${fmt(result.loopResistance, 6)} Ω`,
    `ΔV             ${fmt(model.moduleImpA, 3)} × ${fmt(result.loopResistance, 6)} = ${fmt(result.voltageDrop, 3)} V`,
    `Loss           I²R = ${fmt(result.cableLossW, 3)} W`,
    '',
    '03 TWO-CONDUCTOR GEOMETRY',
    `Cable radius   ${fmt(model.conductorOdMm / 2, 3)} mm`,
    `Centre spacing ${fmt(model.conductorSpacingMm, 3)} mm`,
    `acosh(D/2r)    ${fmt(result.acoshTerm, 6)}`,
    `L′ loop        ${fmt(result.loopInductancePerM * 1e6, 6)} µH/m`,
    `C′ pair        ${fmt(result.pairCapacitancePerM * 1e12, 6)} pF/m`,
    `L total        ${fmt(result.loopInductanceH * 1e6, 3)} µH`,
    `C pair total   ${fmt(result.pairCapacitanceF * 1e9, 3)} nF`,
    `Z0             ${fmt(result.characteristicImpedance, 3)} Ω`,
    `Velocity       ${fmt(result.propagationVelocity / 1e6, 3)} Mm/s`,
    `Delay          ${fmt(result.oneWayDelayS * 1e6, 3)} µs one-way`,
    '',
    '04 STORED ENERGY',
    `Magnetic       ½LI² = ${fmt(result.magneticEnergyJ * 1000, 3)} mJ`,
    `Earth C        ${fmt(result.totalEarthCapF * 1e9, 3)} nF declared total`,
    `Electric       ½CV² = ${fmt(result.electricEnergyJ, 6)} J`,
    '',
    'WARNINGS',
    ...(warnings.length ? warnings.map((w, i) => `${String(i + 1).padStart(2, '0')} ${w}`) : ['NONE']),
    '',
    'BOUNDARY',
    'The inductance and pair-capacitance formulas are idealised two-round-conductor estimates.',
    'Module-to-frame and inverter capacitances are declared inputs, not inferred measurements.',
    'No transient solver, protection verdict or design approval is included in V1.'
  ].join('\n');
}

function buildReport(model, result, warnings) {
  return [
    'SOLAR ELECTRICAL TOPOLOGY ANALYSIS ENGINE',
    'V1 CALCULATION RECORD',
    '',
    `Model: ${model.modelName}`,
    `Generated: ${new Date().toISOString()}`,
    '',
    'INPUT SUMMARY',
    `Modules in series: ${model.moduleCount}`,
    `Module Vmp: ${model.moduleVmpV} V`,
    `Module Imp: ${model.moduleImpA} A`,
    `Cable one-way length: ${model.cableLengthM} m`,
    `Cable conductor: ${model.cableCsaMm2} mm² ${model.cableMaterial}`,
    `Cable outside diameter: ${model.conductorOdMm} mm`,
    `Conductor centre spacing: ${model.conductorSpacingMm} mm`,
    `Relative permittivity: ${model.relativePermittivity}`,
    `Module-to-frame capacitance: ${model.moduleFrameCapNf} nF per module`,
    '',
    'RESULT SUMMARY',
    `String Vmp: ${fmt(result.stringVmp, 3)} V`,
    `String power: ${fmt(result.stringPowerW / 1000, 3)} kW`,
    `Loop resistance: ${fmt(result.loopResistance, 6)} Ω`,
    `Voltage drop: ${fmt(result.voltageDrop, 3)} V (${fmt(result.voltageDropPct, 3)}%)`,
    `Cable loss: ${fmt(result.cableLossW, 3)} W (${fmt(result.cableLossPct, 3)}%)`,
    `Loop inductance: ${fmt(result.loopInductanceH * 1e6, 3)} µH`,
    `Pair capacitance: ${fmt(result.pairCapacitanceF * 1e9, 3)} nF`,
    `Total declared capacitance to frame/earth: ${fmt(result.totalEarthCapF * 1e9, 3)} nF`,
    `Magnetic stored energy: ${fmt(result.magneticEnergyJ * 1000, 3)} mJ`,
    `Electric stored energy: ${fmt(result.electricEnergyJ, 6)} J`,
    `Characteristic impedance: ${fmt(result.characteristicImpedance, 3)} Ω`,
    `One-way propagation delay: ${fmt(result.oneWayDelayS * 1e6, 3)} µs`,
    '',
    'WARNINGS',
    ...(warnings.length ? warnings : ['None']),
    '',
    'DISCLAIMER',
    'Research and screening calculation only. Verify all inputs, formulas and assumptions before engineering use.'
  ].join('\n');
}

function render(model, result, warnings) {
  setText('out-vmp', `${fmt(result.stringVmp, 1)} V`);
  setText('out-power', `${fmt(result.stringPowerW / 1000, 3)} kW`);
  setText('out-r', `${fmt(result.loopResistance, 4)} Ω`);
  setText('out-vdrop', `${fmt(result.voltageDrop, 2)} V`);
  setText('out-vdrop-pct', `${fmt(result.voltageDropPct, 3)} %`);
  setText('out-loss', `${fmt(result.cableLossW, 1)} W`);
  setText('out-loss-pct', `${fmt(result.cableLossPct, 3)} %`);
  setText('out-l', `${fmt(result.loopInductanceH * 1e6, 2)} µH`);
  setText('out-cpair', `${fmt(result.pairCapacitanceF * 1e9, 3)} nF`);
  setText('out-cearth', `${fmt(result.totalEarthCapF * 1e9, 1)} nF`);
  setText('out-emag', `${fmt(result.magneticEnergyJ * 1000, 3)} mJ`);
  setText('out-eelec', `${fmt(result.electricEnergyJ, 4)} J`);
  setText('out-z0', `${fmt(result.characteristicImpedance, 2)} Ω`);
  setText('out-delay', `${fmt(result.oneWayDelayS * 1e6, 3)} µs`);

  renderNetwork(model, result);
  const trace = buildTrace(model, result, warnings);
  const report = buildReport(model, result, warnings);
  setText('calculation-trace', trace);
  setText('report-preview', report);
  setText('parse-status', warnings.length ? `Calculated with ${warnings.length} warning(s).` : 'Model parsed and calculated successfully.');
  setText('model-status', warnings.length ? 'MODEL CHECK' : 'MODEL READY');

  latest = { model, result, warnings, trace, report };
}

function runModel() {
  try {
    const parsed = parseModel(el('model-input').value);
    if (parsed.errors.length) {
      setText('parse-status', parsed.errors.join(' | '));
      setText('model-status', 'MODEL ERROR');
      el('calculation-trace').textContent = ['MODEL PARSE FAILED', '', ...parsed.errors].join('\n');
      return;
    }
    const result = calculate(parsed.model);
    render(parsed.model, result, [...parsed.warnings, ...result.warnings]);
  } catch (error) {
    el('fatal-banner').style.display = 'block';
    el('fatal-banner').textContent = `CALCULATION ERROR: ${error.message}`;
    console.error(error);
  }
}

function download(filename, content, type) {
  const blob = new Blob([content], { type });
  const url = URL.createObjectURL(blob);
  const link = document.createElement('a');
  link.href = url;
  link.download = filename;
  document.body.appendChild(link);
  try { link.click(); } finally {
    link.remove();
    setTimeout(() => URL.revokeObjectURL(url), 1000);
  }
}

function exportJSON() {
  if (!latest) return;
  download('solar_electrical_model_v1.json', JSON.stringify({
    schema: 'solar-electrical-topology-analysis-engine/v1',
    generatedAt: new Date().toISOString(),
    model: latest.model,
    result: latest.result,
    warnings: latest.warnings
  }, null, 2), 'application/json');
}

function exportCSV() {
  if (!latest) return;
  const rows = [['parameter', 'value', 'unit'],
    ['string_vmp', latest.result.stringVmp, 'V'],
    ['string_power', latest.result.stringPowerW, 'W'],
    ['loop_resistance', latest.result.loopResistance, 'ohm'],
    ['voltage_drop', latest.result.voltageDrop, 'V'],
    ['voltage_drop_percent', latest.result.voltageDropPct, '%'],
    ['cable_loss', latest.result.cableLossW, 'W'],
    ['loop_inductance', latest.result.loopInductanceH, 'H'],
    ['pair_capacitance', latest.result.pairCapacitanceF, 'F'],
    ['earth_capacitance_declared', latest.result.totalEarthCapF, 'F'],
    ['magnetic_energy', latest.result.magneticEnergyJ, 'J'],
    ['electric_energy', latest.result.electricEnergyJ, 'J'],
    ['characteristic_impedance', latest.result.characteristicImpedance, 'ohm'],
    ['one_way_delay', latest.result.oneWayDelayS, 's']
  ];
  const csv = rows.map(row => row.map(v => `"${String(v).replace(/"/g, '""')}"`).join(',')).join('\n');
  download('solar_electrical_results_v1.csv', '\ufeff' + csv, 'text/csv;charset=utf-8');
}

function exportText() {
  if (!latest) return;
  download('solar_electrical_report_v1.txt', latest.report, 'text/plain;charset=utf-8');
}

function initModes() {
  document.querySelectorAll('.mode-btn').forEach(button => {
    button.addEventListener('click', () => {
      document.querySelectorAll('.mode-btn').forEach(b => b.classList.remove('active'));
      button.classList.add('active');
      const target = document.querySelector(`[data-panel="${button.dataset.view}"]`);
      if (target) target.scrollIntoView({ behavior: 'smooth', block: 'start' });
    });
  });
}

function boot() {
  el('model-input').value = DEFAULT_MODEL;
  el('btn-load-example').addEventListener('click', () => { el('model-input').value = DEFAULT_MODEL; runModel(); });
  el('btn-run').addEventListener('click', runModel);
  el('btn-copy-trace').addEventListener('click', async () => {
    if (!latest) return;
    try {
      await navigator.clipboard.writeText(latest.trace);
      setText('parse-status', 'Calculation trace copied.');
    } catch {
      setText('parse-status', 'Clipboard unavailable. Select the trace manually.');
    }
  });
  el('btn-export-json').addEventListener('click', exportJSON);
  el('btn-export-csv').addEventListener('click', exportCSV);
  el('btn-export-txt').addEventListener('click', exportText);
  el('model-input').addEventListener('keydown', event => {
    if ((event.ctrlKey || event.metaKey) && event.key === 'Enter') runModel();
  });
  initModes();
  runModel();
}

document.addEventListener('DOMContentLoaded', boot);
