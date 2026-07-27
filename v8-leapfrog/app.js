(function () {
  'use strict';

  const Model = window.V8LeapfrogModel;
  if (!Model) throw new Error('V8LeapfrogModel failed to load.');

  const $ = (id) => document.getElementById(id);
  const inputIds = [
    'modulesPerString', 'moduleWidthM', 'alongRowGapM', 'bandGapM',
    'eastBands', 'westBands', 'inverterDistanceM', 'scenarioDistancesM',
    'polarityConvention', 'cableR20MilliOhmPerM', 'cableTemperatureC',
    'stringCurrentA', 'moduleVmpV', 'inverterCount', 'installedCableRatePerM',
    'positiveFactoryLeadM', 'negativeFactoryLeadM', 'measuredLeapfrogSpanM',
    'leadEvidence'
  ];

  const valueMap = {
    modulesPerString: 'modulesPerString',
    moduleWidthM: 'moduleWidthM',
    alongRowGapM: 'alongRowGapM',
    bandGapM: 'bandGapM',
    eastBands: 'eastBands',
    westBands: 'westBands',
    inverterDistanceM: 'inverterDistanceM',
    scenarioDistancesM: 'scenarioDistancesM',
    polarityConvention: 'polarityConvention',
    cableR20MilliOhmPerM: 'cableR20MilliOhmPerM',
    cableTemperatureC: 'cableTemperatureC',
    stringCurrentA: 'stringCurrentA',
    moduleVmpV: 'moduleVmpV',
    inverterCount: 'inverterCount',
    installedCableRatePerM: 'installedCableRatePerM',
    positiveFactoryLeadM: 'positiveFactoryLeadM',
    negativeFactoryLeadM: 'negativeFactoryLeadM',
    measuredLeapfrogSpanM: 'measuredLeapfrogSpanM',
    leadEvidence: 'leadEvidence'
  };

  function fmt(value, decimals = 2) {
    return Number.isFinite(value)
      ? value.toLocaleString('en-GB', {
          minimumFractionDigits: decimals,
          maximumFractionDigits: decimals
        })
      : '—';
  }

  function setText(id, value) {
    const element = $(id);
    if (element) element.textContent = value;
  }

  function readInputs() {
    const raw = {};
    Object.entries(valueMap).forEach(([key, id]) => {
      const element = $(id);
      if (!element) return;
      raw[key] = element.value;
    });
    return raw;
  }

  function setInputValues(values) {
    Object.entries(valueMap).forEach(([key, id]) => {
      const element = $(id);
      if (!element || values[key] == null) return;
      element.value = Array.isArray(values[key]) ? values[key].join(',') : String(values[key]);
    });
  }

  function groupBands(strings) {
    const groups = new Map();
    strings.forEach((string) => {
      const key = `${string.face}-${string.band}`;
      if (!groups.has(key)) groups.set(key, []);
      groups.get(key).push(string);
    });
    return [...groups.values()];
  }

  function renderMetrics(study) {
    const totals = study.totals;
    const electrical = study.electrical;
    setText('metricRowSpan', `${fmt(study.geometry.rowSpanM, 2)} m`);
    setText('metricStrings', String(totals.stringsPerInverter));
    setText('metricSequential', `${fmt(totals.sequentialExternalM / 1000, 3)} km`);
    setText('metricLeapfrog', `${fmt(totals.leapfrogExternalM / 1000, 3)} km`);
    setText('metricSavingInverter', `${fmt(totals.externalCableSavingM / 1000, 3)} km`);
    setText('metricSavingFleet', `${fmt(totals.fleetExternalCableSavingKm, 1)} km`);
    setText('metricResistanceSaving', `${fmt(electrical.resistanceSavingOhmPerString, 4)} Ω`);
    setText('metricVoltageSaving', `${fmt(electrical.voltageDropSavingVPerString, 2)} V · ${fmt(electrical.voltageDropSavingPercentOfStringVmp, 3)}%`);
    setText('metricLossSaving', `${fmt(totals.powerLossSavingW / 1000, 3)} kW`);
    setText('metricFleetLossSaving', `${fmt(totals.fleetPowerLossSavingKWAtEnteredCurrent, 1)} kW`);

    const basePairM = totals.leapfrogExternalM;
    setText('decompBasePair', `${fmt(basePairM, 1)} m`);
    setText('decompSequentialReturn', `${fmt(totals.externalCableSavingM, 1)} m`);
    setText('decompLeapfrogReturn', '0.0 m');
    setText('decompSequentialTotal', `${fmt(totals.sequentialExternalM, 1)} m`);
    setText('decompLeapfrogTotal', `${fmt(totals.leapfrogExternalM, 1)} m`);
    setText('decompDifference', `${fmt(totals.externalCableSavingM, 1)} m`);

    const rate = study.input.installedCableRatePerM;
    setText('metricCostSaving', rate > 0
      ? `£${fmt(totals.fleetInstalledCostSaving, 0)}`
      : 'Not priced');
  }

  function renderLeadScreen(study) {
    const lead = study.leadFeasibility;
    setText('leadPositive', `${fmt(study.input.positiveFactoryLeadM, 3)} m`);
    setText('leadNegative', `${fmt(study.input.negativeFactoryLeadM, 3)} m`);
    setText('leadCombined', `${fmt(lead.availableCombinedLeadM, 3)} m`);
    setText('leadRequired', lead.requiredMeasuredSpanM == null ? 'Not entered' : `${fmt(lead.requiredMeasuredSpanM, 3)} m`);
    const status = $('leadStatus');
    if (status) {
      status.textContent = lead.status;
      status.className = lead.status === 'PASSES_LENGTH_SCREEN'
        ? 'green'
        : lead.status === 'FAILS_LENGTH_SCREEN'
          ? 'red'
          : 'amber';
    }
    setText('leadMessage', `${lead.message} Evidence: ${lead.evidence}.`);
  }

  function renderBandSchedule(study) {
    const tbody = $('bandSchedule');
    if (!tbody) return;
    tbody.innerHTML = groupBands(study.strings).map((group) => {
      const first = group[0];
      const count = group.length;
      const seqTotal = group.reduce((sum, string) => sum + string.sequential.totalExternalM, 0);
      const leapTotal = group.reduce((sum, string) => sum + string.leapfrog.totalExternalM, 0);
      const saving = group.reduce((sum, string) => sum + string.saving.externalCableM, 0);
      return `<tr>
        <td>${first.face}</td>
        <td>${first.band}</td>
        <td>${count}</td>
        <td>${fmt(first.nearRouteM, 2)}</td>
        <td>${fmt(first.sequential.positiveM, 2)}</td>
        <td>${fmt(first.sequential.negativeM, 2)}</td>
        <td>${fmt(seqTotal, 2)}</td>
        <td>${fmt(first.leapfrog.positiveM, 2)}</td>
        <td>${fmt(first.leapfrog.negativeM, 2)}</td>
        <td>${fmt(leapTotal, 2)}</td>
        <td class="good-cell">${fmt(saving, 2)}</td>
      </tr>`;
    }).join('');

    const foot = $('bandScheduleFoot');
    if (foot) {
      foot.innerHTML = `<tr>
        <th colspan="6">Per inverter</th>
        <td>${fmt(study.totals.sequentialExternalM, 2)}</td>
        <td colspan="2"></td>
        <td>${fmt(study.totals.leapfrogExternalM, 2)}</td>
        <td class="good-cell">${fmt(study.totals.externalCableSavingM, 2)}</td>
      </tr>`;
    }
  }

  function renderStringSchedule(study) {
    const tbody = $('stringSchedule');
    if (!tbody) return;
    tbody.innerHTML = study.strings.map((string) => `<tr>
      <td>${string.number}</td>
      <td>${string.positiveId} / ${string.negativeId}</td>
      <td>${string.face}</td>
      <td>${string.band}</td>
      <td>${fmt(string.nearRouteM, 2)}</td>
      <td>${fmt(string.sequential.positiveM, 2)}</td>
      <td>${fmt(string.sequential.negativeM, 2)}</td>
      <td>${fmt(string.leapfrog.positiveM, 2)}</td>
      <td>${fmt(string.leapfrog.negativeM, 2)}</td>
      <td class="good-cell">${fmt(string.saving.externalCableM, 2)}</td>
      <td>${fmt(string.saving.resistanceOhmPerString, 4)}</td>
      <td>${fmt(string.saving.voltageDropVPerString, 2)}</td>
      <td>${fmt(string.saving.powerLossWPerString, 1)}</td>
    </tr>`).join('');
  }

  function renderScenarios(raw) {
    const tbody = $('scenarioSchedule');
    if (!tbody) return;
    tbody.innerHTML = Model.scenarioStudies(raw).map((scenario) => `<tr>
      <td>${fmt(scenario.distanceM, 1)}</td>
      <td>${fmt(scenario.leapfrogExternalM, 1)}</td>
      <td>${fmt(scenario.externalCableSavingM, 1)}</td>
      <td>${fmt(scenario.sequentialExternalM, 1)}</td>
      <td>${fmt(scenario.leapfrogExternalM, 1)}</td>
      <td class="good-cell">${fmt(scenario.externalCableSavingM, 1)}</td>
      <td class="good-cell">${fmt(scenario.fleetExternalCableSavingKm, 1)}</td>
      <td class="good-cell">${fmt(scenario.inverterPowerLossSavingKW, 3)}</td>
    </tr>`).join('');
  }

  function svgLine(points, className, width) {
    const path = points.map((point, index) => `${index ? 'L' : 'M'} ${point[0]} ${point[1]}`).join(' ');
    return `<path d="${path}" class="${className}" stroke-width="${width}"/>`;
  }

  function cable(points, width = 4) {
    return svgLine(points, 'svg-cable-halo', width + 3) + svgLine(points, 'svg-cable', width);
  }

  function moduleRects(y, count, x0, moduleW, gap) {
    let html = '';
    for (let index = 0; index < count; index += 1) {
      const x = x0 + index * (moduleW + gap);
      html += `<rect x="${x}" y="${y}" width="${moduleW}" height="52" rx="1" class="svg-module-east"/>`;
      html += `<rect x="${x + moduleW / 2 - 2}" y="${y + 19}" width="4" height="4" fill="#000"/>`;
    }
    return html;
  }

  function renderDiagram(study) {
    const svg = $('topologyDiagram');
    if (!svg) return;
    const modules = Math.min(study.input.modulesPerString, 30);
    const x0 = 225;
    const moduleW = 23;
    const gap = 5;
    const pitch = moduleW + gap;
    const xLast = x0 + (modules - 1) * pitch + moduleW / 2;
    const invX = 65;
    const invW = 48;
    const seqY = 92;
    const leapY = 328;
    const topCentre = seqY + 26;
    const bottomCentre = leapY + 26;
    let html = '';

    html += `<rect x="${invX}" y="54" width="${invW}" height="154" rx="3" class="svg-inverter"/>`;
    html += `<rect x="${invX}" y="290" width="${invW}" height="154" rx="3" class="svg-inverter"/>`;
    html += `<text x="30" y="42" class="svg-label" font-size="18" font-weight="800">SEQUENTIAL</text>`;
    html += `<text x="30" y="278" class="svg-label" font-size="18" font-weight="800">LEAPFROG</text>`;
    html += `<text x="44" y="138" class="svg-label" font-size="12" transform="rotate(-90 44 138)">INVERTER INPUTS</text>`;
    html += `<text x="44" y="374" class="svg-label" font-size="12" transform="rotate(-90 44 374)">INVERTER INPUTS</text>`;
    html += moduleRects(seqY, modules, x0, moduleW, gap);
    html += moduleRects(leapY, modules, x0, moduleW, gap);

    const nearX = x0 + moduleW / 2;
    html += cable([[invX + invW, topCentre - 9], [nearX, topCentre - 9]], 4);
    html += cable([[nearX, topCentre], [xLast, topCentre]], 3);
    html += cable([[xLast, topCentre + 9], [xLast, seqY + 102], [invX + invW, seqY + 102]], 4);
    html += `<path d="M ${xLast} ${topCentre + 9} L ${xLast} ${seqY + 102} L ${invX + invW} ${seqY + 102}" class="svg-saving"/>`;
    html += `<text x="${invX + invW + 10}" y="${topCentre - 14}" class="svg-label" font-size="14">+</text>`;
    html += `<text x="${invX + invW + 10}" y="${seqY + 120}" class="svg-label" font-size="14">−</text>`;
    html += `<text x="${x0}" y="${seqY + 140}" class="svg-label" font-size="14" fill="#ff6170">Additional external return = ${fmt(study.geometry.rowSpanM, 2)} m per string</text>`;

    html += cable([[invX + invW, bottomCentre - 11], [nearX, bottomCentre - 11]], 4);
    html += cable([[invX + invW, bottomCentre + 11], [x0 + pitch + moduleW / 2, bottomCentre + 11]], 4);
    html += `<text x="${invX + invW + 10}" y="${bottomCentre - 16}" class="svg-label" font-size="14">+</text>`;
    html += `<text x="${invX + invW + 10}" y="${bottomCentre + 31}" class="svg-label" font-size="14">−</text>`;

    const upperY = bottomCentre - 11;
    const lowerY = bottomCentre + 11;
    for (let index = 0; index < modules - 2; index += 2) {
      const x1 = x0 + index * pitch + moduleW / 2;
      const x2 = x0 + (index + 2) * pitch + moduleW / 2;
      html += cable([[x1, upperY], [x2, upperY]], 2.5);
    }
    for (let index = 1; index < modules - 2; index += 2) {
      const x1 = x0 + index * pitch + moduleW / 2;
      const x2 = x0 + (index + 2) * pitch + moduleW / 2;
      html += cable([[x1, lowerY], [x2, lowerY]], 2.5);
    }
    if (modules >= 2) {
      const xOddLast = x0 + (modules - 2) * pitch + moduleW / 2;
      const xEvenLast = x0 + (modules - 1) * pitch + moduleW / 2;
      html += cable([[xOddLast, upperY], [xEvenLast, lowerY]], 2.5);
    }
    html += `<text x="${x0}" y="${leapY + 92}" class="svg-label" font-size="14" fill="#53e28b">Both free terminals emerge at inverter-side end · external row return = 0 m</text>`;
    html += `<text x="${x0}" y="488" class="svg-muted" font-size="13">Black = electrical conductor. Diagram is topological, not an as-built routing drawing.</text>`;
    html += `<text x="760" y="42" class="svg-muted" font-size="13">D = ${fmt(study.input.inverterDistanceM, 1)} m · R = ${fmt(study.geometry.rowSpanM, 2)} m</text>`;

    svg.setAttribute('viewBox', '0 0 1160 510');
    svg.innerHTML = html;
  }

  function renderTrace(study) {
    const first = study.strings[0];
    const trace = [
      `MODEL VERSION = ${study.modelVersion}`,
      `FORMULA ID = ${study.formulaId}`,
      `ROW SPAN R = N × module width + (N − 1) × gap`,
      `R = ${study.input.modulesPerString} × ${fmt(study.input.moduleWidthM, 3)} + ${study.input.modulesPerString - 1} × ${fmt(study.input.alongRowGapM, 3)} = ${fmt(study.geometry.rowSpanM, 3)} m`,
      `BAND PITCH = R + band gap = ${fmt(study.geometry.bandPitchM, 3)} m`,
      `SEQUENTIAL PER STRING = base pair 2(D + O) + additional row return R`,
      `LEAPFROG PER STRING = base pair 2(D + O) + additional row return 0`,
      `CABLE SAVING PER STRING = R = ${fmt(study.geometry.rowSpanM, 3)} m`,
      `DEFAULT FIRST STRING SEQUENTIAL +/− = ${fmt(first?.sequential.positiveM, 3)} / ${fmt(first?.sequential.negativeM, 3)} m`,
      `DEFAULT FIRST STRING LEAPFROG +/− = ${fmt(first?.leapfrog.positiveM, 3)} / ${fmt(first?.leapfrog.negativeM, 3)} m`,
      `OPERATING CABLE R′ = ${fmt(study.electrical.cableResistanceOperatingOhmPerM * 1000, 5)} mΩ/m at ${fmt(study.input.cableTemperatureC, 1)} °C`,
      `ΔR PER STRING = ${fmt(study.electrical.resistanceSavingOhmPerString, 6)} Ω`,
      `ΔV PER STRING = ${fmt(study.electrical.voltageDropSavingVPerString, 4)} V = ${fmt(study.electrical.voltageDropSavingPercentOfStringVmp, 4)}% of string Vmp`,
      `ΔP PER STRING AT ENTERED CURRENT = ${fmt(study.electrical.powerLossSavingWPerString, 3)} W`,
      `TOTAL EXTERNAL CABLE SAVED PER INVERTER = ${fmt(study.totals.externalCableSavingM, 3)} m`,
      `TOTAL EXTERNAL CABLE SAVED ACROSS ${study.input.inverterCount} INVERTERS = ${fmt(study.totals.fleetExternalCableSavingKm, 3)} km`,
      `IMPORTANT: the inverter distance changes the unavoidable base pair, not the one-row-span saving.`
    ];
    setText('calculationTrace', trace.join('\n'));
  }

  function renderSummaryText(study) {
    const text = [
      `V8 leapfrog cable comparison`,
      `Row span: ${fmt(study.geometry.rowSpanM, 2)} m`,
      `Strings per inverter: ${study.totals.stringsPerInverter}`,
      `Sequential external cable: ${fmt(study.totals.sequentialExternalM, 1)} m/inverter`,
      `Leapfrog external cable: ${fmt(study.totals.leapfrogExternalM, 1)} m/inverter`,
      `Additional row-return eliminated: ${fmt(study.totals.externalCableSavingM, 1)} m/inverter`,
      `Fleet saving: ${fmt(study.totals.fleetExternalCableSavingKm, 1)} km`,
      `Resistance reduction: ${fmt(study.electrical.resistanceSavingOhmPerString, 4)} Ω/string`,
      `Voltage-drop reduction: ${fmt(study.electrical.voltageDropSavingVPerString, 2)} V/string`,
      `Loss reduction at entered current: ${fmt(study.totals.powerLossSavingW / 1000, 3)} kW/inverter`,
      `Reliance: indicative screening only; not an as-built quantity or design approval.`
    ].join('\n');
    const element = $('plainSummary');
    if (element) element.value = text;
    return text;
  }

  function renderComparison() {
    setText('v6Comparison', 'V6 remains the complete-circuit and interactive geometry workbench. It includes module leads, connectors, temperature, loop area, inductance and capacitance.');
    setText('v7Comparison', 'V7 remains the independent electromagnetic foundations workbench. It separates external/internal inductance, uses external L for propagation, and labels evidence status.');
    setText('v8Comparison', 'V8 now owns the sequential-versus-leapfrog external cable schedule, all-string comparison, diagram, lead-length screen and golden tests.');
  }

  function setTestStatus() {
    const tests = Model.runGoldenTests();
    const status = $('selfTestStatus');
    if (!status) return tests;
    status.textContent = tests.allPassed
      ? `${tests.passed}/${tests.total} GOLDEN TESTS PASSED`
      : `${tests.passed}/${tests.total} GOLDEN TESTS PASSED`;
    status.className = `status-badge testing${tests.allPassed ? '' : ' error'}`;
    return tests;
  }

  function showError(error) {
    const box = $('runtimeError');
    if (box) {
      box.classList.add('visible');
      box.textContent = `${error.name || 'Error'}: ${error.message || error}`;
    }
    const status = $('runtimeStatus');
    if (status) {
      status.textContent = 'RUNTIME ERROR';
      status.className = 'status-badge error';
    }
  }

  function clearError() {
    const box = $('runtimeError');
    if (box) {
      box.classList.remove('visible');
      box.textContent = '';
    }
    const status = $('runtimeStatus');
    if (status) {
      status.textContent = `V8.${Model.VERSION} LIVE`;
      status.className = 'status-badge';
    }
  }

  function render() {
    try {
      clearError();
      const raw = readInputs();
      const study = Model.calculate(raw);
      renderMetrics(study);
      renderLeadScreen(study);
      renderBandSchedule(study);
      renderStringSchedule(study);
      renderScenarios(raw);
      renderDiagram(study);
      renderTrace(study);
      renderSummaryText(study);
      renderComparison();
      setTestStatus();
      window.__V8_LAST_STUDY__ = study;
    } catch (error) {
      console.error(error);
      showError(error);
    }
  }

  function downloadJson() {
    const raw = readInputs();
    const study = Model.calculate(raw);
    const payload = {
      schema: 'globalgrid2050-v8-leapfrog-cable-comparison',
      schemaVersion: '1.0.0',
      generatedAt: new Date().toISOString(),
      reliance: 'Indicative engineering screening only. Not an as-built quantity, procurement instruction, design approval or compliance certificate.',
      study,
      scenarios: Model.scenarioStudies(raw),
      goldenTests: Model.runGoldenTests()
    };
    const link = document.createElement('a');
    link.href = URL.createObjectURL(new Blob([JSON.stringify(payload, null, 2)], { type: 'application/json' }));
    link.download = 'v8-leapfrog-cable-comparison.json';
    link.click();
    setTimeout(() => URL.revokeObjectURL(link.href), 1000);
  }

  async function copySummary() {
    const text = renderSummaryText(Model.calculate(readInputs()));
    try {
      await navigator.clipboard.writeText(text);
      setText('copyStatus', 'Copied');
    } catch (error) {
      const textarea = $('plainSummary');
      textarea?.select();
      document.execCommand('copy');
      setText('copyStatus', 'Copied');
    }
    setTimeout(() => setText('copyStatus', 'Copy summary'), 1400);
  }

  function initialiseTabs() {
    document.querySelectorAll('.tab').forEach((button) => {
      button.addEventListener('click', () => {
        document.querySelectorAll('.tab').forEach((candidate) => candidate.classList.remove('active'));
        document.querySelectorAll('.tabpane').forEach((pane) => pane.classList.remove('active'));
        button.classList.add('active');
        $(button.dataset.tab)?.classList.add('active');
        if (button.dataset.tab === 'diagramTab') renderDiagram(Model.calculate(readInputs()));
      });
    });
  }

  function initialise() {
    setInputValues(Model.DEFAULTS);
    inputIds.forEach((id) => $(id)?.addEventListener('input', render));
    $('resetBtn')?.addEventListener('click', () => {
      setInputValues(Model.DEFAULTS);
      render();
    });
    $('exportBtn')?.addEventListener('click', downloadJson);
    $('copyBtn')?.addEventListener('click', copySummary);
    initialiseTabs();
    render();
  }

  if (document.readyState === 'loading') {
    document.addEventListener('DOMContentLoaded', initialise, { once: true });
  } else {
    initialise();
  }
})();
