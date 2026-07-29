const assertFinite = (value, name) => {
  if (!Number.isFinite(value)) throw new TypeError(`${name} must be finite`);
};

const rotate = (x, y, angleRad) => ({
  x: x * Math.cos(angleRad) - y * Math.sin(angleRad),
  y: x * Math.sin(angleRad) + y * Math.cos(angleRad),
});

export function buildModuleTerminalGeometry({
  moduleNumber,
  centreXMetres,
  centreYMetres,
  widthMetres,
  heightMetres,
  rotationDegrees = 0,
  junctionBoxOffsetXMetres = 0,
  junctionBoxOffsetYMetres = 0,
  positiveExitOffsetXMetres = 0,
  positiveExitOffsetYMetres = 0,
  negativeExitOffsetXMetres = 0,
  negativeExitOffsetYMetres = 0,
  positiveLeadLengthMetres,
  negativeLeadLengthMetres,
}) {
  for (const [name, value] of Object.entries({
    centreXMetres, centreYMetres, widthMetres, heightMetres, rotationDegrees,
    junctionBoxOffsetXMetres, junctionBoxOffsetYMetres,
    positiveExitOffsetXMetres, positiveExitOffsetYMetres,
    negativeExitOffsetXMetres, negativeExitOffsetYMetres,
    positiveLeadLengthMetres, negativeLeadLengthMetres,
  })) assertFinite(value, name);
  if (!Number.isInteger(moduleNumber) || moduleNumber < 1) throw new TypeError('moduleNumber must be a positive integer');
  if (widthMetres <= 0 || heightMetres <= 0) throw new TypeError('module dimensions must be positive');
  if (positiveLeadLengthMetres < 0 || negativeLeadLengthMetres < 0) throw new TypeError('lead lengths must be non-negative');

  const angle = rotationDegrees * Math.PI / 180;
  const world = (localX, localY) => {
    const p = rotate(localX, localY, angle);
    return { xMetres: centreXMetres + p.x, yMetres: centreYMetres + p.y };
  };
  const junctionBox = world(junctionBoxOffsetXMetres, junctionBoxOffsetYMetres);
  const positiveExit = world(junctionBoxOffsetXMetres + positiveExitOffsetXMetres, junctionBoxOffsetYMetres + positiveExitOffsetYMetres);
  const negativeExit = world(junctionBoxOffsetXMetres + negativeExitOffsetXMetres, junctionBoxOffsetYMetres + negativeExitOffsetYMetres);

  return {
    moduleNumber,
    centre: { xMetres: centreXMetres, yMetres: centreYMetres },
    dimensions: { widthMetres, heightMetres, rotationDegrees },
    junctionBox,
    terminals: {
      positive: { ...positiveExit, leadLengthMetres: positiveLeadLengthMetres },
      negative: { ...negativeExit, leadLengthMetres: negativeLeadLengthMetres },
    },
  };
}

export function requiredConnectionSpan(fromTerminal, toTerminal) {
  return Math.hypot(toTerminal.xMetres - fromTerminal.xMetres, toTerminal.yMetres - fromTerminal.yMetres);
}

export function validateLeadReach({ fromTerminal, toTerminal, routingAllowanceMetres = 0 }) {
  assertFinite(routingAllowanceMetres, 'routingAllowanceMetres');
  if (routingAllowanceMetres < 0) throw new TypeError('routingAllowanceMetres must be non-negative');
  const directSpanMetres = requiredConnectionSpan(fromTerminal, toTerminal);
  const requiredMetres = directSpanMetres + routingAllowanceMetres;
  const availableMetres = fromTerminal.leadLengthMetres + toTerminal.leadLengthMetres;
  return {
    directSpanMetres,
    routingAllowanceMetres,
    requiredMetres,
    availableMetres,
    marginMetres: availableMetres - requiredMetres,
    feasible: availableMetres + 1e-12 >= requiredMetres,
    status: availableMetres + 1e-12 >= requiredMetres ? 'PASS' : 'FAIL',
  };
}

export function buildLinearTerminalModules({
  moduleCount,
  pitchMetres,
  originXMetres = 0,
  originYMetres = 0,
  ...moduleTemplate
}) {
  if (!Number.isInteger(moduleCount) || moduleCount < 1) throw new TypeError('moduleCount must be a positive integer');
  assertFinite(pitchMetres, 'pitchMetres');
  if (pitchMetres < 0) throw new TypeError('pitchMetres must be non-negative');
  return Array.from({ length: moduleCount }, (_, index) => buildModuleTerminalGeometry({
    ...moduleTemplate,
    moduleNumber: index + 1,
    centreXMetres: originXMetres + index * pitchMetres,
    centreYMetres: originYMetres,
  }));
}

export function deriveSeriesLeadConnections(order, modulesByNumber, routingAllowanceMetres = 0) {
  const map = modulesByNumber instanceof Map ? modulesByNumber : new Map(modulesByNumber.map(module => [module.moduleNumber, module]));
  return order.slice(0, -1).map((fromModuleNumber, index) => {
    const toModuleNumber = order[index + 1];
    const fromModule = map.get(fromModuleNumber);
    const toModule = map.get(toModuleNumber);
    if (!fromModule || !toModule) throw new TypeError('order references missing module geometry');
    const reach = validateLeadReach({
      fromTerminal: fromModule.terminals.positive,
      toTerminal: toModule.terminals.negative,
      routingAllowanceMetres,
    });
    return { connectionIndex: index + 1, fromModuleNumber, toModuleNumber, ...reach };
  });
}