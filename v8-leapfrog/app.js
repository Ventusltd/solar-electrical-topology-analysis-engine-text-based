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
        study.feasibility.message;
      return;
    }

    banner.style.borderColor = '#8b3038';
    banner.style.background = '#2a0b0f';
    banner.style.color = '#ffbec4';
    banner.innerHTML =
      '<strong>LEAPFROG SAVING NOT AVAILABLE</strong>' +
      study.feasibility.message;
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
      `${fmt(totals.sequentialExternalMPerArchetypeInverter / 1000, 3)} km`
    );
    setText(
      'metricLeapfrog',
      `${fmt(totals.leapfrogExternalMPerArchetypeInverter / 1000, 3)} km theoretical`
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
        : `${fmt(electrical.availableVoltageDropSavingVPerString, 2)} V · ` +
          `${fmt(electrical.voltageDropSavingPercentOfStringVmp, 3)}%`
    );
    setText(
      'metricLossSaving',
      available(
        totals.availablePowerLossSavingWPerArchetypeInverter == null
          ? null
          : totals.availablePowerLossSavingWPerArchetypeInverter / 1000,
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
      `${fmt(totals.leapfrogExternalMPerArchetypeInverter, 1)} m`
    );
    setText(
      'decompSequentialReturn',
      `${fmt(totals.theoreticalSavingMPerArchetypeInverter, 1)} m`
    );
    setText(
      'decompLeapfrogReturn',
      study.feasibility.feasible ? '0.0 m' : 'UNAVAILABLE'
    );
    setText(
      'decompSequentialTotal',
      `${fmt(totals.sequentialExternalMPerArchetypeInverter, 1)} m`
    );
    setText(
      'decompLeapfrogTotal',
      `${fmt(totals.leapfrogExternalMPerArchetypeInverter, 1)} m theoretical`
    );
    setText(
      'decompDifference',
      available(totals.availableSavingMPerArchetypeInverter, ' m', 1)
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
    setText('leadMargin', `${fmt(lead.marginM, 3)} m`);
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
          (sum, string) => sum + string.sequential.totalExternalM,
          0
        );
        const leapfrogTotal = group.reduce(
          (sum, string) => sum + string.leapfrog.totalExternalM,
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
              study.totals.sequentialExternalMPerArchetypeInverter,
              2
            )}
          </td>
          <td colspan="2"></td>
          <td>
            ${fmt(
              study.totals.leapfrogExternalMPerArchetypeInverter,
              2
            )}
          </td>
          <td class="warning-cell">
            ${fmt(
              study.totals.theoreticalSavingMPerArchetypeInverter,
              2
            )}
          </td>
          <td class="good-cell">
            ${available(
              study.totals.availableSavingMPerArchetypeInverter,
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
            ${fmt(string.saving.theoreticalExternalCableM, 2)}
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
            ${fmt(scenario.basePairMPerArchetypeInverter, 1)}
          </td>
          <td>
            ${fmt(
              scenario.sequentialExternalMPerArchetypeInverter,
              1
            )}
          </td>
          <td>
            ${fmt(
              scenario.leapfrogExternalMPerArchetypeInverter,
              1
            )}
          </td>
          <td class="warning-cell">
            ${fmt(
              scenario.theoreticalSavingMPerArchetypeInverter,
              1
            )}
          </td>
          <td class="good-cell">
            ${available(
              scenario.availableSavingMPerArchetypeInverter,
              '',
              1
            )}
          </td>
          <td class="good-cell">
            ${available(scenario.availableSiteSavingKm, '', 1)}
          </td>
          <td class="good-cell">
            ${available(
              scenario.availablePowerLossSavingKWPerArchetypeInverter,
              '',
              3
            )}
          </td>
        </tr>
      `)
      .join('');
  }

  function svgPath(path, className, width, extra = '') {
    return (
      `<path d="${path}" class="${className}" ` +
      `stroke-width="${width}" ${extra}/>`
    );
  }

  function cablePath(path, width = 3, extra = '') {
    return (
      svgPath(path, 'svg-cable-halo', width + 3, extra) +
      svgPath(path, 'svg-cable', width, extra)
    );
  }

  function svgText(x, y, text, className = 'svg-label', size = 12) {
    return (
      `<text x="${x}" y="${y}" class="${className}" ` +
      `font-size="${size}">${text}</text>`
    );
  }

  function buildSequentialSequence(count) {
    return Array.from({ length: count }, (_, index) => index + 1);
  }

  function buildLeapfrogSequence(count) {
    if (count <= 1) {
      return [1];
    }

    const outward = [];
    const returning = [];

    for (let module = 1; module <= count; module += 2) {
      outward.push(module);
    }

    let returnStart = count % 2 === 0 ? count : count - 1;

    for (; returnStart >= 2; returnStart -= 2) {
      returning.push(returnStart);
    }

    return outward.concat(returning);
  }

  function sequenceConnections(sequence) {
    return sequence.slice(0, -1).map((from, index) => ({
      from,
      to: sequence[index + 1]
    }));
  }

  function moduleGeometry(count, x0, y, moduleWidth, moduleHeight, gap) {
    const modules = new Map();

    for (let number = 1; number <= count; number += 1) {
      const x = x0 + (number - 1) * (moduleWidth + gap);
      const centreX = x + moduleWidth / 2;
      const terminalY = y + 30;

      modules.set(number, {
        number,
        x,
        y,
        centreX,
        terminalY,
        negativeX: centreX - 11,
        positiveX: centreX + 11
      });
    }

    return modules;
  }

  function terminalPoint(modules, moduleNumber, polarity) {
    const module = modules.get(moduleNumber);

    return {
      x: polarity === '+' ? module.positiveX : module.negativeX,
      y: module.terminalY
    };
  }

  function moduleRowHtml(modules, moduleWidth, moduleHeight) {
    let html = '';

    modules.forEach((module) => {
      html += `
        <g data-module="M${module.number}">
          <rect
            x="${module.x}"
            y="${module.y}"
            width="${moduleWidth}"
            height="${moduleHeight}"
            rx="2"
            class="svg-module-east"
          />
          <rect
            x="${module.negativeX - 7}"
            y="${module.terminalY - 7}"
            width="14"
            height="14"
            rx="2"
            fill="#0a0e12"
            stroke="#eef7ff"
            stroke-width="1"
          />
          <rect
            x="${module.positiveX - 7}"
            y="${module.terminalY - 7}"
            width="14"
            height="14"
            rx="2"
            fill="#0a0e12"
            stroke="#eef7ff"
            stroke-width="1"
          />
          <text
            x="${module.negativeX}"
            y="${module.terminalY + 4}"
            text-anchor="middle"
            class="svg-label"
            font-size="11"
          >−</text>
          <text
            x="${module.positiveX}"
            y="${module.terminalY + 4}"
            text-anchor="middle"
            class="svg-label"
            font-size="11"
          >+</text>
          <text
            x="${module.centreX}"
            y="${module.y + moduleHeight + 18}"
            text-anchor="middle"
            class="svg-label"
            font-size="12"
          >M${module.number}</text>
        </g>
      `;
    });

    return html;
  }

  function connectionArc(modules, connection, rowY, side, index) {
    const start = terminalPoint(modules, connection.from, '+');
    const end = terminalPoint(modules, connection.to, '−');
    const distance = Math.abs(end.x - start.x);
    const direction = side === 'above' ? -1 : 1;
    const lane = Math.min(42, 22 + distance * 0.12 + (index % 2) * 3);
    const controlY = rowY + 30 + direction * lane;
    const path =
      `M ${start.x} ${start.y} ` +
      `C ${start.x} ${controlY}, ${end.x} ${controlY}, ` +
      `${end.x} ${end.y}`;

    return cablePath(path, 2.4);
  }

  function externalCable(start, endX, endY, laneY) {
    const path =
      `M ${start.x} ${start.y} ` +
      `L ${start.x} ${laneY} ` +
      `L ${endX} ${laneY} ` +
      `L ${endX} ${endY}`;

    return cablePath(path, 4);
  }

  function drawInverter(x, y, height, negativeY, positiveY) {
    return `
      <rect
        x="${x}"
        y="${y}"
        width="74"
        height="${height}"
        rx="4"
        class="svg-inverter"
      />
      ${svgText(x + 8, y + 22, 'INVERTER', 'svg-label', 13)}
      <circle
        cx="${x + 74}"
        cy="${negativeY}"
        r="5"
        fill="#05070a"
        stroke="#eef7ff"
        stroke-width="2"
      />
      <circle
        cx="${x + 74}"
        cy="${positiveY}"
        r="5"
        fill="#05070a"
        stroke="#eef7ff"
        stroke-width="2"
      />
      ${svgText(x + 48, negativeY + 4, '−', 'svg-label', 14)}
      ${svgText(x + 48, positiveY + 4, '+', 'svg-label', 14)}
    `;
  }

  function renderSequentialGeometry(options) {
    const {
      count,
      modules,
      rowY,
      inverterX,
      inverterY,
      moduleWidth,
      moduleHeight,
      study
    } = options;
    const sequence = buildSequentialSequence(count);
    const connections = sequenceConnections(sequence);
    const freeNegative = terminalPoint(modules, sequence[0], '−');
    const freePositive = terminalPoint(
      modules,
      sequence[sequence.length - 1],
      '+'
    );
    const inverterNegativeY = rowY + 18;
    const inverterPositiveY = rowY + 58;
    const returnLaneY = rowY + moduleHeight + 48;
    let html = '';

    html += drawInverter(
      inverterX,
      inverterY,
      126,
      inverterNegativeY,
      inverterPositiveY
    );
    html += moduleRowHtml(modules, moduleWidth, moduleHeight);

    connections.forEach((connection, index) => {
      html += connectionArc(modules, connection, rowY, 'above', index);
    });

    html += externalCable(
      freeNegative,
      inverterX + 74,
      inverterNegativeY,
      rowY + 4
    );
    html += externalCable(
      freePositive,
      inverterX + 74,
      inverterPositiveY,
      returnLaneY
    );
    html += svgText(
      freeNegative.x - 16,
      freeNegative.y - 16,
      'FREE − M1−',
      'svg-label',
      12
    );
    html += svgText(
      freePositive.x - 30,
      returnLaneY - 8,
      `FREE + M${count}+`,
      'svg-label',
      12
    );
    html += svgText(
      modules.get(1).x,
      rowY + moduleHeight + 82,
      `Additional far-end return ≈ ${fmt(study.geometry.rowSpanM, 2)} m`,
      'svg-label',
      14
    );

    return html;
  }

  function renderLeapfrogGeometry(options) {
    const {
      count,
      modules,
      rowY,
      inverterX,
      inverterY,
      moduleWidth,
      moduleHeight,
      study
    } = options;
    const sequence = buildLeapfrogSequence(count);
    const connections = sequenceConnections(sequence);
    const freeNegative = terminalPoint(modules, sequence[0], '−');
    const freePositive = terminalPoint(
      modules,
      sequence[sequence.length - 1],
      '+'
    );
    const inverterNegativeY = rowY + 18;
    const inverterPositiveY = rowY + 58;
    let html = '';

    html += drawInverter(
      inverterX,
      inverterY,
      126,
      inverterNegativeY,
      inverterPositiveY
    );
    html += moduleRowHtml(modules, moduleWidth, moduleHeight);

    connections.forEach((connection, index) => {
      const isOutward = connection.from % 2 === 1 && connection.to % 2 === 1;
      const isTurnaround =
        Math.abs(connection.from - connection.to) === 1 &&
        Math.max(connection.from, connection.to) === count;
      const side = isOutward ? 'above' : 'below';

      html += connectionArc(modules, connection, rowY, side, index);

      if (isTurnaround) {
        const start = terminalPoint(modules, connection.from, '+');
        const end = terminalPoint(modules, connection.to, '−');
        const labelX = (start.x + end.x) / 2;

        html += svgText(
          labelX - 72,
          rowY - 42,
          `TURNAROUND M${connection.from}+ → M${connection.to}−`,
          'svg-label',
          12
        );
      }
    });

    html += externalCable(
      freeNegative,
      inverterX + 74,
      inverterNegativeY,
      rowY + 4
    );
    html += externalCable(
      freePositive,
      inverterX + 74,
      inverterPositiveY,
      rowY + moduleHeight + 42
    );
    html += svgText(
      freeNegative.x - 18,
      freeNegative.y - 17,
      'FREE − M1−',
      'svg-label',
      12
    );
    html += svgText(
      freePositive.x - 20,
      rowY + moduleHeight + 68,
      'FREE + M2+',
      'svg-label',
      12
    );
    html += svgText(
      modules.get(1).x,
      rowY + moduleHeight + 96,
      'Same physical M1–M30 row. Only the connection order changes.',
      'svg-label',
      14
    );
    html += svgText(
      modules.get(1).x,
      rowY + moduleHeight + 120,
      `Electrical order: ${sequence.map((item) => `M${item}`).join(' → ')}`,
      'svg-muted',
      11
    );
    html += svgText(
      modules.get(1).x,
      rowY + moduleHeight + 143,
      `Feasibility: ${study.feasibility.status} · required reach ` +
        `${fmt(study.feasibility.requiredReachM, 3)} m`,
      'svg-muted',
      12
    );

    return html;
  }

  function renderDiagram(study) {
    const svg = $('topologyDiagram');

    if (!svg) {
      return;
    }

    const count = Math.min(study.input.modulesPerString, 30);
    const moduleHeightM = 2.384;
    const scale = 42;
    const moduleWidth = study.input.moduleWidthM * scale;
    const moduleHeight = moduleHeightM * scale;
    const gap = Math.max(5, study.input.alongRowGapM * scale);
    const x0 = 180;
    const inverterX = 28;
    const sequentialY = 88;
    const leapfrogY = 445;
    const sequentialModules = moduleGeometry(
      count,
      x0,
      sequentialY,
      moduleWidth,
      moduleHeight,
      gap
    );
    const leapfrogModules = moduleGeometry(
      count,
      x0,
      leapfrogY,
      moduleWidth,
      moduleHeight,
      gap
    );
    const rowWidth =
      count * moduleWidth + Math.max(0, count - 1) * gap;
    const viewWidth = Math.max(1280, x0 + rowWidth + 90);
    const viewHeight = 760;
    let html = '';

    html += svgText(
      28,
      30,
      'PHYSICAL MODULE POSITIONS ARE IDENTICAL IN BOTH VIEWS',
      'svg-label',
      18
    );
    html += svgText(
      28,
      55,
      'M1, M2, M3 … M30 stay fixed left-to-right. The panels do not move.',
      'svg-muted',
      13
    );
    html += svgText(28, 82, 'SEQUENTIAL', 'svg-label', 18);
    html += renderSequentialGeometry({
      count,
      modules: sequentialModules,
      rowY: sequentialY,
      inverterX,
      inverterY: sequentialY - 12,
      moduleWidth,
      moduleHeight,
      study
    });
    html += svgText(28, 438, 'LEAPFROG', 'svg-label', 18);
    html += renderLeapfrogGeometry({
      count,
      modules: leapfrogModules,
      rowY: leapfrogY,
      inverterX,
      inverterY: leapfrogY - 12,
      moduleWidth,
      moduleHeight,
      study
    });

    svg.setAttribute('viewBox', `0 0 ${viewWidth} ${viewHeight}`);
    svg.setAttribute('width', String(viewWidth));
    svg.setAttribute('height', String(viewHeight));
    svg.style.width = `${viewWidth}px`;
    svg.style.minWidth = `${viewWidth}px`;
    svg.style.maxWidth = 'none';
    svg.innerHTML = html;

    window.__V8_GEOMETRY__ = {
      physicalOrder: Array.from({ length: count }, (_, index) => index + 1),
      sequentialOrder: buildSequentialSequence(count),
      leapfrogOrder: buildLeapfrogSequence(count),
      moduleWidthM: study.input.moduleWidthM,
      moduleHeightM,
      moduleGapM: study.input.alongRowGapM,
      panelsMove: false
    };
  }

  function renderTrace(study) {
    const totals = study.totals;
    const trace = [
      `MODEL VERSION = ${study.modelVersion}`,
      `FORMULA ID = ${study.formulaId}`,
      `MODULE PITCH = width + gap = ` +
        `${fmt(study.geometry.modulePitchM, 3)} m`,
      'PHYSICAL MODULE ORDER = M1, M2, M3 ... M30',
      'LEAPFROG CHANGES CONNECTION ORDER ONLY; PANELS DO NOT MOVE',
      'LEAPFROG REACH = 2 × module pitch, unless measured override',
      `REQUIRED REACH = ${fmt(study.feasibility.requiredReachM, 3)} m`,
      `AVAILABLE FACTORY LEAD = ` +
        `${fmt(study.feasibility.availableLeadReachM, 3)} m`,
      `LEAD MARGIN = ${fmt(study.feasibility.marginM, 3)} m`,
      `FEASIBILITY = ${study.feasibility.status}`,
      'ROW SPAN R = N × module width + (N − 1) × gap',
      `R = ${fmt(study.geometry.rowSpanM, 3)} m`,
      'SEQUENTIAL PER STRING = 2(D + O) + R',
      'LEAPFROG PER STRING = 2(D + O)',
      'THEORETICAL DIFFERENCE PER STRING = R',
      `ARCHETYPE STRINGS = ${totals.stringsPerArchetypeInverter}`,
      `ACTUAL SITE STRINGS = ${totals.totalSiteStringCount}`,
      `AVERAGE SITE STRINGS/INVERTER = ` +
        `${fmt(totals.averageSiteStringsPerInverter, 3)}`,
      `THEORETICAL SITE DIFFERENCE = ` +
        `${fmt(totals.theoreticalSiteSavingKm, 3)} km`,
      `AVAILABLE SITE DIFFERENCE = ` +
        `${available(totals.availableSiteSavingKm, ' km', 3)}`,
      'Fleet values use actual site strings, not 24 × inverter count.'
    ];

    setText('calculationTrace', trace.join('\n'));
  }

  function renderSummary(study) {
    const text = [
      'V8.2 sequential versus leapfrog cable comparison',
      'Physical panels remain M1 to M30 from left to right.',
      'Leapfrog changes electrical connection order only.',
      `Module pitch: ${fmt(study.geometry.modulePitchM, 3)} m`,
      `Row span: ${fmt(study.geometry.rowSpanM, 2)} m`,
      `Lead screen: ${study.feasibility.status}`,
      `Required reach: ${fmt(study.feasibility.requiredReachM, 3)} m`,
      `Available lead: ` +
        `${fmt(study.feasibility.availableLeadReachM, 3)} m`,
      `Archetype strings/inverter: ` +
        `${study.totals.stringsPerArchetypeInverter}`,
      `Actual site strings: ${study.totals.totalSiteStringCount}`,
      `Sequential external cable/archetype: ` +
        `${fmt(
          study.totals.sequentialExternalMPerArchetypeInverter,
          1
        )} m`,
      `Theoretical leapfrog external cable/archetype: ` +
        `${fmt(
          study.totals.leapfrogExternalMPerArchetypeInverter,
          1
        )} m`,
      `Available site saving: ` +
        `${available(study.totals.availableSiteSavingKm, ' km', 2)}`,
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
        'comparison, fixed physical module geometry, lead feasibility ' +
        'gate, actual site string count and all-string schedule.'
    );
  }

  function geometrySelfTests() {
    const sequence = buildLeapfrogSequence(30);
    const connections = sequenceConnections(sequence);
    const physical = Array.from({ length: 30 }, (_, index) => index + 1);

    return [
      {
        name: 'Physical modules remain M1 to M30',
        pass: physical.every((item, index) => item === index + 1)
      },
      {
        name: 'Thirty modules create twenty-nine series connections',
        pass: connections.length === 29
      },
      {
        name: 'Leapfrog turnaround is M29+ to M30−',
        pass: connections.some(
          (connection) => connection.from === 29 && connection.to === 30
        )
      },
      {
        name: 'Leapfrog return begins M30+ to M28−',
        pass: connections.some(
          (connection) => connection.from === 30 && connection.to === 28
        )
      },
      {
        name: 'Leapfrog free terminals are M1− and M2+',
        pass: sequence[0] === 1 && sequence[sequence.length - 1] === 2
      }
    ];
  }

  function renderSelfTests() {
    const modelTests = Model.runGoldenTests();
    const geometryTests = geometrySelfTests();
    const geometryPassed = geometryTests.filter((test) => test.pass).length;
    const passed = modelTests.passed + geometryPassed;
    const total = modelTests.total + geometryTests.length;
    const allPassed = modelTests.allPassed &&
      geometryTests.every((test) => test.pass);
    const status = $('selfTestStatus');

    if (status) {
      status.textContent = `${passed}/${total} TESTS PASSED`;
      status.className = allPassed
        ? 'status-badge testing'
        : 'status-badge error';
    }

    window.__V8_GEOMETRY_TESTS__ = geometryTests;

    return {
      modelTests,
      geometryTests,
      passed,
      total,
      allPassed
    };
  }

  function showError(error) {
    const box = $('runtimeError');
    const status = $('runtimeStatus');

    if (box) {
      box.classList.add('visible');
      box.textContent = `${error.name || 'Error'}: ${error.message || error}`;
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
      schemaVersion: '2.1.0',
      generatedAt: new Date().toISOString(),
      reliance:
        'Indicative engineering screening only. Not an as-built ' +
        'quantity, procurement instruction, design approval or ' +
        'compliance certificate.',
      geometry: window.__V8_GEOMETRY__,
      study,
      scenarios: Model.scenarioStudies(raw),
      tests: renderSelfTests()
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
        document.querySelectorAll('.tab').forEach((candidate) => {
          candidate.classList.remove('active');
        });
        document.querySelectorAll('.tabpane').forEach((pane) => {
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
    document.addEventListener('DOMContentLoaded', initialise, { once: true });
  } else {
    initialise();
  }
})();
