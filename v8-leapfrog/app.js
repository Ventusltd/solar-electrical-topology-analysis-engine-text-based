(function startV8Application() {
  'use strict';

  const Model = window.V8LeapfrogModel;

  if (!Model) {
    throw new Error('V8LeapfrogModel failed to load.');
  }

  const $ = (id) => document.getElementById(id);

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
    totalSiteStringCount: 'totalSiteStringCount',
    installedCableRatePerM: 'installedCableRatePerM',
    positiveFactoryLeadM: 'positiveFactoryLeadM',
    negativeFactoryLeadM: 'negativeFactoryLeadM',
    measuredLeapfrogSpanM: 'measuredLeapfrogSpanM',
    leadEvidence: 'leadEvidence'
  };

  function fmt(value, decimals = 2) {
    if (!Number.isFinite(value)) {
      return '—';
    }

    return value.toLocaleString('en-GB', {
      minimumFractionDigits: decimals,
      maximumFractionDigits: decimals
    });
  }

  function available(value, suffix, decimals = 2) {
    if (value == null || !Number.isFinite(value)) {
      return 'UNAVAILABLE';
    }

    return `${fmt(value, decimals)}${suffix}`;
  }

  function setText(id, value) {
    const element = $(id);

    if (element) {
      element.textContent = value;
    }
  }

  function readInputs() {
    const raw = {};

    Object.entries(valueMap).forEach(([key, id]) => {
      const element = $(id);

      if (element) {
        raw[key] = element.value;
      }
    });

    return raw;
  }

  function setInputValues(values) {
    Object.entries(valueMap).forEach(([key, id]) => {
      const element = $(id);
      const value = values[key];

      if (!element || value == null) {
        return;
      }

      element.value = Array.isArray(value)
        ? value.join(',')
        : String(value);
    });
  }

  function groupBands(strings) {
    const groups = new Map();

    strings.forEach((string) => {
      const key = `${string.face}-${string.band}`;

      if (!groups.has(key)) {
        groups.set(key, []);
      }

      groups.get(key).push(string);
    });

    return [...groups.values()];
  }

  function renderFeasibilityBanner(study) {
    const banner = $('feasibilityBanner');

    if (!banner) {
      return;
    }

    if (study.feasibility.feasible) {
      banner.style.borderColor = '#205838';
      banner.style.background = '#062014';
      banner.style.color = '#bdf5d4';
      banner.innerHTML =
        '<strong>LEAPFROG LENGTH SCREEN PASSED</strong>' +
        `${study.feasibility.message}`;
      return;
    }

    banner.style.borderColor = '#8b3038';
    banner.style.background = '#2a0b0f';
    banner.style.color = '#ffbec4';
    banner.innerHTML =
      '<strong>LEAPFROG SAVING NOT AVAILABLE</strong>' +
      `${study.feasibility.message}`;
  }

  function renderMetrics(study) {
    const totals = study.totals;
    const electrical = study.electrical;

    setText(
      'metricModulePitch',
      `${fmt(study.geometry.modulePitchM, 3)} m`
    );
    setText(
      'metricRowSpan',
      `${fmt(study.geometry.rowSpanM, 2)} m`
    );
    setText(
      'metricStrings',
      String(totals.stringsPerArchetypeInverter)
    );
    setText(
      'metricSiteStrings',
      totals.totalSiteStringCount.toLocaleString('en-GB')
    );
    setText(
      'metricAverageStrings',
      `${fmt(totals.averageSiteStringsPerInverter, 2)} average/inverter`
    );
    setText(
      'metricSequential',
      `${fmt(
        totals.sequentialExternalMPerArchetypeInverter / 1000,
        3
      )} km`
    );
    setText(
      'metricLeapfrog',
      `${fmt(
        totals.leapfrogExternalMPerArchetypeInverter / 1000,
        3
      )} km theoretical`
    );
    setText(
      'metricSavingInverter',
      available(
        totals.availableSavingMPerArchetypeInverter == null
          ? null
          : totals.availableSavingMPerArchetypeInverter / 1000,
        ' km',
        3
      )
    );
    setText(
      'metricSavingFleet',
      available(totals.availableSiteSavingKm, ' km', 1)
    );
    setText(
      'metricResistanceSaving',
      available(
        electrical.availableResistanceSavingOhmPerString,
        ' Ω',
        4
      )
    );
    setText(
      'metricVoltageSaving',
      electrical.availableVoltageDropSavingVPerString == null
        ? 'UNAVAILABLE'
        : `${fmt(
            electrical.availableVoltageDropSavingVPerString,
            2
          )} V · ${fmt(
            electrical.voltageDropSavingPercentOfStringVmp,
            3
          )}%`
    );
    setText(
      'metricLossSaving',
      available(
        totals.availablePowerLossSavingWPerArchetypeInverter == null
          ? null
          : totals.availablePowerLossSavingWPerArchetypeInverter /
              1000,
        ' kW',
        3
      )
    );
    setText(
      'metricFleetLossSaving',
      available(totals.availableSitePowerLossSavingKW, ' kW', 1)
    );

    const rate = study.input.installedCableRatePerM;
    const cost = totals.availableSiteInstalledCostSaving;

    setText(
      'metricCostSaving',
      rate > 0 && cost != null
        ? `£${fmt(cost, 0)}`
        : rate > 0
          ? 'UNAVAILABLE'
          : 'Not priced'
    );

    setText(
      'decompBasePair',
      `${fmt(
        totals.leapfrogExternalMPerArchetypeInverter,
        1
      )} m`
    );
    setText(
      'decompSequentialReturn',
      `${fmt(
        totals.theoreticalSavingMPerArchetypeInverter,
        1
      )} m`
    );
    setText(
      'decompLeapfrogReturn',
      study.feasibility.feasible ? '0.0 m' : 'UNAVAILABLE'
    );
    setText(
      'decompSequentialTotal',
      `${fmt(
        totals.sequentialExternalMPerArchetypeInverter,
        1
      )} m`
    );
    setText(
      'decompLeapfrogTotal',
      `${fmt(
        totals.leapfrogExternalMPerArchetypeInverter,
        1
      )} m theoretical`
    );
    setText(
      'decompDifference',
      available(
        totals.availableSavingMPerArchetypeInverter,
        ' m',
        1
      )
    );
  }

  function renderLeadScreen(study) {
    const lead = study.feasibility;

    setText(
      'leadPositive',
      `${fmt(study.input.positiveFactoryLeadM, 3)} m`
    );
    setText(
      'leadNegative',
      `${fmt(study.input.negativeFactoryLeadM, 3)} m`
    );
    setText(
      'leadCombined',
      `${fmt(lead.availableLeadReachM, 3)} m`
    );
    setText(
      'leadRequired',
      `${fmt(lead.requiredReachM, 3)} m`
    );
    setText('leadBasis', lead.basis);
    setText(
      'leadMargin',
      `${fmt(lead.marginM, 3)} m`
    );
    setText(
      'leadExtension',
      `${fmt(lead.extensionRequiredM, 3)} m`
    );

    const status = $('leadStatus');

    if (status) {
      status.textContent = lead.status;
      status.className = lead.feasible ? 'green' : 'red';
    }

    setText(
      'leadMessage',
      `${lead.message} Evidence: ${lead.evidence}.`
    );
  }

  function renderBandSchedule(study) {
    const body = $('bandSchedule');
    const foot = $('bandScheduleFoot');

    if (!body) {
      return;
    }

    body.innerHTML = groupBands(study.strings)
      .map((group) => {
        const first = group[0];
        const count = group.length;
        const sequentialTotal = group.reduce(
          (sum, string) =>
            sum + string.sequential.totalExternalM,
          0
        );
        const leapfrogTotal = group.reduce(
          (sum, string) =>
            sum + string.leapfrog.totalExternalM,
          0
        );
        const theoreticalDifference =
          count * study.geometry.rowSpanM;
        const availableDifference = study.feasibility.feasible
          ? theoreticalDifference
          : null;

        return `
          <tr>
            <td>${first.face}</td>
            <td>${first.band}</td>
            <td>${count}</td>
            <td>${fmt(first.nearRouteM, 2)}</td>
            <td>${fmt(first.sequential.positiveM, 2)}</td>
            <td>${fmt(first.sequential.negativeM, 2)}</td>
            <td>${fmt(sequentialTotal, 2)}</td>
            <td>${fmt(first.leapfrog.positiveM, 2)}</td>
            <td>${fmt(first.leapfrog.negativeM, 2)}</td>
            <td>${fmt(leapfrogTotal, 2)}</td>
            <td class="warning-cell">
              ${fmt(theoreticalDifference, 2)}
            </td>
            <td class="good-cell">
              ${available(availableDifference, '', 2)}
            </td>
          </tr>
        `;
      })
      .join('');

    if (foot) {
      foot.innerHTML = `
        <tr>
          <th colspan="6">Per archetype inverter</th>
          <td>
            ${fmt(
              study.totals
                .sequentialExternalMPerArchetypeInverter,
              2
            )}
          </td>
          <td colspan="2"></td>
          <td>
            ${fmt(
              study.totals
                .leapfrogExternalMPerArchetypeInverter,
              2
            )}
          </td>
          <td class="warning-cell">
            ${fmt(
              study.totals
                .theoreticalSavingMPerArchetypeInverter,
              2
            )}
          </td>
          <td class="good-cell">
            ${available(
              study.totals
                .availableSavingMPerArchetypeInverter,
              '',
              2
            )}
          </td>
        </tr>
      `;
    }
  }

  function renderStringSchedule(study) {
    const body = $('stringSchedule');

    if (!body) {
      return;
    }

    body.innerHTML = study.strings
      .map((string) => `
        <tr>
          <td>${string.number}</td>
          <td>${string.positiveId} / ${string.negativeId}</td>
          <td>${string.face}</td>
          <td>${string.band}</td>
          <td>${fmt(string.nearRouteM, 2)}</td>
          <td>${fmt(string.sequential.positiveM, 2)}</td>
          <td>${fmt(string.sequential.negativeM, 2)}</td>
          <td>${fmt(string.leapfrog.positiveM, 2)}</td>
          <td>${fmt(string.leapfrog.negativeM, 2)}</td>
          <td class="warning-cell">
            ${fmt(
              string.saving.theoreticalExternalCableM,
              2
            )}
          </td>
          <td class="good-cell">
            ${available(
              string.saving.availableExternalCableM,
              '',
              2
            )}
          </td>
          <td>
            ${available(
              string.saving.availableResistanceOhmPerString,
              '',
              4
            )}
          </td>
          <td>
            ${available(
              string.saving.availableVoltageDropVPerString,
              '',
              2
            )}
          </td>
          <td>
            ${available(
              string.saving.availablePowerLossWPerString,
              '',
              1
            )}
          </td>
        </tr>
      `)
      .join('');
  }

  function renderScenarios(raw) {
    const body = $('scenarioSchedule');

    if (!body) {
      return;
    }

    body.innerHTML = Model.scenarioStudies(raw)
      .map((scenario) => `
        <tr>
          <td>${fmt(scenario.distanceM, 1)}</td>
          <td>
            ${fmt(
              scenario.basePairMPerArchetypeInverter,
              1
            )}
          </td>
          <td>
            ${fmt(
              scenario
                .sequentialExternalMPerArchetypeInverter,
              1
            )}
          </td>
          <td>
            ${fmt(
              scenario
                .leapfrogExternalMPerArchetypeInverter,
              1
            )}
          </td>
          <td class="warning-cell">
            ${fmt(
              scenario
                .theoreticalSavingMPerArchetypeInverter,
              1
            )}
          </td>
          <td class="good-cell">
            ${available(
              scenario
                .availableSavingMPerArchetypeInverter,
              '',
              1
            )}
          </td>
          <td class="good-cell">
            ${available(
              scenario.availableSiteSavingKm,
              '',
              1
            )}
          </td>
          <td class="good-cell">
            ${available(
              scenario
                .availablePowerLossSavingKWPerArchetypeInverter,
              '',
              3
            )}
          </td>
        </tr>
      `)
      .join('');
  }

  function svgPath(points, className, width) {
    const path = points
      .map(
        (point, index) =>
          `${index ? 'L' : 'M'} ${point[0]} ${point[1]}`
      )
      .join(' ');

    return (
      `<path d="${path}" ` +
      `class="${className}" ` +
      `stroke-width="${width}"/>`
    );
  }

  function cable(points, width = 4) {
    return (
      svgPath(points, 'svg-cable-halo', width + 3) +
      svgPath(points, 'svg-cable', width)
    );
  }

  function moduleRectangles(y, count, x0, width, gap) {
    let html = '';

    for (let index = 0; index < count; index += 1) {
      const x = x0 + index * (width + gap);

      html += `
        <rect
          x="${x}"
          y="${y}"
          width="${width}"
          height="52"
          rx="1"
          class="svg-module-east"
        />
      `;
      html += `
        <rect
          x="${x + width / 2 - 2}"
          y="${y + 19}"
          width="4"
          height="4"
          fill="#000"
        />
      `;
    }

    return html;
  }

  function renderDiagram(study) {
    const svg = $('topologyDiagram');

    if (!svg) {
      return;
    }

    const count = Math.min(study.input.modulesPerString, 30);
    const x0 = 225;
    const moduleWidth = 23;
    const gap = 5;
    const pitch = moduleWidth + gap;
    const lastX =
      x0 + (count - 1) * pitch + moduleWidth / 2;
    const nearX = x0 + moduleWidth / 2;
    const inverterX = 65;
    const inverterWidth = 48;
    const sequentialY = 92;
    const leapfrogY = 328;
    const sequentialCentre = sequentialY + 26;
    const leapfrogCentre = leapfrogY + 26;
    let html = '';

    html += `
      <rect
        x="${inverterX}"
        y="54"
        width="${inverterWidth}"
        height="154"
        rx="3"
        class="svg-inverter"
      />
      <rect
        x="${inverterX}"
        y="290"
        width="${inverterWidth}"
        height="154"
        rx="3"
        class="svg-inverter"
      />
      <text
        x="30"
        y="42"
        class="svg-label"
        font-size="18"
        font-weight="800"
      >SEQUENTIAL</text>
      <text
        x="30"
        y="278"
        class="svg-label"
        font-size="18"
        font-weight="800"
      >LEAPFROG</text>
    `;

    html += moduleRectangles(
      sequentialY,
      count,
      x0,
      moduleWidth,
      gap
    );
    html += moduleRectangles(
      leapfrogY,
      count,
      x0,
      moduleWidth,
      gap
    );

    html += cable(
      [
        [inverterX + inverterWidth, sequentialCentre - 9],
        [nearX, sequentialCentre - 9]
      ],
      4
    );
    html += cable(
      [
        [nearX, sequentialCentre],
        [lastX, sequentialCentre]
      ],
      3
    );
    html += cable(
      [
        [lastX, sequentialCentre + 9],
        [lastX, sequentialY + 102],
        [inverterX + inverterWidth, sequentialY + 102]
      ],
      4
    );
    html += `
      <path
        d="M ${lastX} ${sequentialCentre + 9}
           L ${lastX} ${sequentialY + 102}
           L ${inverterX + inverterWidth} ${sequentialY + 102}"
        class="svg-saving"
      />
      <text
        x="${x0}"
        y="${sequentialY + 140}"
        class="svg-label"
        font-size="14"
        fill="#ff6170"
      >
        Additional external return =
        ${fmt(study.geometry.rowSpanM, 2)} m per string
      </text>
    `;

    html += cable(
      [
        [inverterX + inverterWidth, leapfrogCentre - 11],
        [nearX, leapfrogCentre - 11]
      ],
      4
    );
    html += cable(
      [
        [inverterX + inverterWidth, leapfrogCentre + 11],
        [x0 + pitch + moduleWidth / 2, leapfrogCentre + 11]
      ],
      4
    );

    for (let index = 0; index < count - 2; index += 2) {
      const start = x0 + index * pitch + moduleWidth / 2;
      const end = x0 + (index + 2) * pitch + moduleWidth / 2;

      html += cable(
        [
          [start, leapfrogCentre - 11],
          [end, leapfrogCentre - 11]
        ],
        2.5
      );
    }

    for (let index = 1; index < count - 2; index += 2) {
      const start = x0 + index * pitch + moduleWidth / 2;
      const end = x0 + (index + 2) * pitch + moduleWidth / 2;

      html += cable(
        [
          [start, leapfrogCentre + 11],
          [end, leapfrogCentre + 11]
        ],
        2.5
      );
    }

    if (count >= 2) {
      const penultimate =
        x0 + (count - 2) * pitch + moduleWidth / 2;
      const final =
        x0 + (count - 1) * pitch + moduleWidth / 2;

      html += cable(
        [
          [penultimate, leapfrogCentre - 11],
          [final, leapfrogCentre + 11]
        ],
        2.5
      );
    }

    html += `
      <text
        x="${x0}"
        y="${leapfrogY + 92}"
        class="svg-label"
        font-size="14"
        fill="#53e28b"
      >
        Both free terminals emerge at the inverter-side end.
      </text>
      <text
        x="${x0}"
        y="${leapfrogY + 117}"
        class="svg-muted"
        font-size="13"
      >
        Feasibility: ${study.feasibility.status} · required reach
        ${fmt(study.feasibility.requiredReachM, 3)} m
      </text>
      <text
        x="30"
        y="492"
        class="svg-muted"
        font-size="13"
      >
        Black = conductor. Diagram is topological, not as-built routing.
      </text>
    `;

    svg.setAttribute('viewBox', '0 0 1160 510');
    svg.innerHTML = html;
  }

  function renderTrace(study) {
    const totals = study.totals;
    const trace = [
      `MODEL VERSION = ${study.modelVersion}`,
      `FORMULA ID = ${study.formulaId}`,
      `MODULE PITCH = width + gap = ` +
        `${fmt(study.geometry.modulePitchM, 3)} m`,
      `LEAPFROG REACH = 2 × module pitch, unless measured override`,
      `REQUIRED REACH = ` +
        `${fmt(study.feasibility.requiredReachM, 3)} m`,
      `AVAILABLE FACTORY LEAD = ` +
        `${fmt(study.feasibility.availableLeadReachM, 3)} m`,
      `LEAD MARGIN = ${fmt(study.feasibility.marginM, 3)} m`,
      `FEASIBILITY = ${study.feasibility.status}`,
      `ROW SPAN R = N × module width + (N − 1) × gap`,
      `R = ${fmt(study.geometry.rowSpanM, 3)} m`,
      `SEQUENTIAL PER STRING = 2(D + O) + R`,
      `LEAPFROG PER STRING = 2(D + O)`,
      `THEORETICAL DIFFERENCE PER STRING = R`,
      `ARCHETYPE STRINGS = ` +
        `${totals.stringsPerArchetypeInverter}`,
      `ACTUAL SITE STRINGS = ${totals.totalSiteStringCount}`,
      `AVERAGE SITE STRINGS/INVERTER = ` +
        `${fmt(totals.averageSiteStringsPerInverter, 3)}`,
      `THEORETICAL SITE DIFFERENCE = ` +
        `${fmt(totals.theoreticalSiteSavingKm, 3)} km`,
      `AVAILABLE SITE DIFFERENCE = ` +
        `${available(totals.availableSiteSavingKm, ' km', 3)}`,
      `Fleet values use actual site strings, not 24 × inverter count.`
    ];

    setText('calculationTrace', trace.join('\n'));
  }

  function renderSummary(study) {
    const text = [
      'V8.2 sequential versus leapfrog cable comparison',
      `Module pitch: ${fmt(study.geometry.modulePitchM, 3)} m`,
      `Row span: ${fmt(study.geometry.rowSpanM, 2)} m`,
      `Lead screen: ${study.feasibility.status}`,
      `Required reach: ` +
        `${fmt(study.feasibility.requiredReachM, 3)} m`,
      `Available lead: ` +
        `${fmt(study.feasibility.availableLeadReachM, 3)} m`,
      `Archetype strings/inverter: ` +
        `${study.totals.stringsPerArchetypeInverter}`,
      `Actual site strings: ${study.totals.totalSiteStringCount}`,
      `Sequential external cable/archetype: ` +
        `${fmt(
          study.totals
            .sequentialExternalMPerArchetypeInverter,
          1
        )} m`,
      `Theoretical leapfrog external cable/archetype: ` +
        `${fmt(
          study.totals
            .leapfrogExternalMPerArchetypeInverter,
          1
        )} m`,
      `Available site saving: ` +
        `${available(
          study.totals.availableSiteSavingKm,
          ' km',
          2
        )}`,
      'Reliance: indicative screening only.'
    ].join('\n');

    const element = $('plainSummary');

    if (element) {
      element.value = text;
    }

    return text;
  }

  function renderComparison() {
    setText(
      'v6Comparison',
      'V6 remains the complete-circuit geometry and electrical ' +
        'workbench, including module leads, connectors, loop area, ' +
        'inductance and capacitance.'
    );
    setText(
      'v7Comparison',
      'V7 remains the electromagnetic foundations workbench, ' +
        'separating propagation inductance from low-frequency ' +
        'internal inductance and exposing evidence status.'
    );
    setText(
      'v8Comparison',
      'V8 owns the sequential-versus-leapfrog external cable ' +
        'comparison, lead feasibility gate, actual site string count ' +
        'and all-string schedule.'
    );
  }

  function renderSelfTests() {
    const tests = Model.runGoldenTests();
    const status = $('selfTestStatus');

    if (status) {
      status.textContent =
        `${tests.passed}/${tests.total} GOLDEN TESTS PASSED`;
      status.className = tests.allPassed
        ? 'status-badge testing'
        : 'status-badge error';
    }

    return tests;
  }

  function showError(error) {
    const box = $('runtimeError');
    const status = $('runtimeStatus');

    if (box) {
      box.classList.add('visible');
      box.textContent =
        `${error.name || 'Error'}: ${error.message || error}`;
    }

    if (status) {
      status.textContent = 'RUNTIME ERROR';
      status.className = 'status-badge error';
    }
  }

  function clearError() {
    const box = $('runtimeError');
    const status = $('runtimeStatus');

    if (box) {
      box.classList.remove('visible');
      box.textContent = '';
    }

    if (status) {
      status.textContent = `V${Model.VERSION} LIVE`;
      status.className = 'status-badge';
    }
  }

  function render() {
    try {
      clearError();

      const raw = readInputs();
      const study = Model.calculate(raw);

      renderFeasibilityBanner(study);
      renderMetrics(study);
      renderLeadScreen(study);
      renderBandSchedule(study);
      renderStringSchedule(study);
      renderScenarios(raw);
      renderDiagram(study);
      renderTrace(study);
      renderSummary(study);
      renderComparison();
      renderSelfTests();

      window.__V8_LAST_STUDY__ = study;
    } catch (error) {
      console.error(error);
      showError(error);
    }
  }

  function exportJson() {
    const raw = readInputs();
    const study = Model.calculate(raw);
    const payload = {
      schema: 'globalgrid2050-v8-leapfrog-cable-comparison',
      schemaVersion: '2.0.0',
      generatedAt: new Date().toISOString(),
      reliance:
        'Indicative engineering screening only. Not an as-built ' +
        'quantity, procurement instruction, design approval or ' +
        'compliance certificate.',
      study,
      scenarios: Model.scenarioStudies(raw),
      goldenTests: Model.runGoldenTests()
    };
    const url = URL.createObjectURL(
      new Blob(
        [JSON.stringify(payload, null, 2)],
        { type: 'application/json' }
      )
    );
    const link = document.createElement('a');

    link.href = url;
    link.download = 'v8-leapfrog-cable-comparison.json';
    link.click();

    setTimeout(() => URL.revokeObjectURL(url), 1000);
  }

  async function copySummary() {
    const text = renderSummary(Model.calculate(readInputs()));

    try {
      await navigator.clipboard.writeText(text);
    } catch (error) {
      const textarea = $('plainSummary');

      if (textarea) {
        textarea.select();
        document.execCommand('copy');
      }
    }

    setText('copyStatus', 'Copied');
    setTimeout(() => setText('copyStatus', 'Copy summary'), 1400);
  }

  function initialiseTabs() {
    document.querySelectorAll('.tab').forEach((button) => {
      button.addEventListener('click', () => {
        document
          .querySelectorAll('.tab')
          .forEach((candidate) => {
            candidate.classList.remove('active');
          });
        document
          .querySelectorAll('.tabpane')
          .forEach((pane) => {
            pane.classList.remove('active');
          });

        button.classList.add('active');
        $(button.dataset.tab)?.classList.add('active');

        if (button.dataset.tab === 'diagramTab') {
          renderDiagram(Model.calculate(readInputs()));
        }
      });
    });
  }

  function initialise() {
    setInputValues(Model.DEFAULTS);

    Object.values(valueMap).forEach((id) => {
      $(id)?.addEventListener('input', render);
      $(id)?.addEventListener('change', render);
    });

    $('resetBtn')?.addEventListener('click', () => {
      setInputValues(Model.DEFAULTS);
      render();
    });
    $('exportBtn')?.addEventListener('click', exportJson);
    $('copyBtn')?.addEventListener('click', copySummary);

    initialiseTabs();
    render();
  }

  if (document.readyState === 'loading') {
    document.addEventListener(
      'DOMContentLoaded',
      initialise,
      { once: true }
    );
  } else {
    initialise();
  }
})();
