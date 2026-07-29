export const TOPOLOGY_SCHEMA = "globalgrid2050.solar-dc-computation.v10.topology.1";

function assertPositiveInteger(value, name) {
  if (!Number.isInteger(value) || value < 1) {
    throw new TypeError(`${name} must be a positive integer`);
  }
}

function assertFiniteNonNegative(value, name) {
  if (!Number.isFinite(value) || value < 0) {
    throw new TypeError(`${name} must be a finite non-negative number`);
  }
}

export function sequentialOrder(moduleCount) {
  assertPositiveInteger(moduleCount, "moduleCount");
  return Array.from({ length: moduleCount }, (_, index) => index + 1);
}

export function mirroredSequentialOrder(moduleCount) {
  return sequentialOrder(moduleCount).reverse();
}

export function canonicalLeapfrogOrder(moduleCount) {
  assertPositiveInteger(moduleCount, "moduleCount");

  const odd = [];
  const even = [];
  for (let moduleNumber = 1; moduleNumber <= moduleCount; moduleNumber += 1) {
    (moduleNumber % 2 === 1 ? odd : even).push(moduleNumber);
  }

  return odd.concat(even.reverse());
}

export function validateCustomOrder(order, moduleCount) {
  assertPositiveInteger(moduleCount, "moduleCount");
  if (!Array.isArray(order) || order.length !== moduleCount) {
    throw new TypeError("custom order must contain exactly moduleCount entries");
  }

  const expected = new Set(sequentialOrder(moduleCount));
  const actual = new Set(order);
  if (actual.size !== moduleCount) {
    throw new TypeError("custom order contains duplicate module numbers");
  }

  for (const moduleNumber of actual) {
    if (!expected.has(moduleNumber)) {
      throw new TypeError("custom order must be an exact permutation of 1..moduleCount");
    }
  }

  return [...order];
}

export function linearModuleCoordinates(moduleCount, pitchMetres, originMetres = 0) {
  assertPositiveInteger(moduleCount, "moduleCount");
  assertFiniteNonNegative(pitchMetres, "pitchMetres");
  if (!Number.isFinite(originMetres)) {
    throw new TypeError("originMetres must be finite");
  }

  return Array.from({ length: moduleCount }, (_, index) => ({
    moduleNumber: index + 1,
    xMetres: originMetres + index * pitchMetres,
    yMetres: 0,
  }));
}

export function deriveOrderedSegments(order, coordinates) {
  if (!Array.isArray(order) || order.length < 1) {
    throw new TypeError("order must contain at least one module");
  }
  if (!Array.isArray(coordinates) || coordinates.length < 1) {
    throw new TypeError("coordinates must contain at least one module");
  }

  const coordinateByModule = new Map(
    coordinates.map((coordinate) => [coordinate.moduleNumber, coordinate]),
  );

  return order.slice(0, -1).map((fromModule, index) => {
    const toModule = order[index + 1];
    const from = coordinateByModule.get(fromModule);
    const to = coordinateByModule.get(toModule);
    if (!from || !to) {
      throw new TypeError("order references a module without coordinates");
    }

    const dx = to.xMetres - from.xMetres;
    const dy = to.yMetres - from.yMetres;
    return {
      segmentIndex: index + 1,
      fromModule,
      toModule,
      dxMetres: dx,
      dyMetres: dy,
      lengthMetres: Math.hypot(dx, dy),
    };
  });
}

export function computeTopologyGeometry({
  moduleCount,
  pitchMetres,
  topology,
  customOrder,
  originMetres = 0,
}) {
  const coordinates = linearModuleCoordinates(moduleCount, pitchMetres, originMetres);

  let order;
  switch (topology) {
    case "sequential":
      order = sequentialOrder(moduleCount);
      break;
    case "mirrored-sequential":
      order = mirroredSequentialOrder(moduleCount);
      break;
    case "leapfrog":
      order = canonicalLeapfrogOrder(moduleCount);
      break;
    case "custom":
      order = validateCustomOrder(customOrder, moduleCount);
      break;
    default:
      throw new TypeError(`unsupported topology: ${topology}`);
  }

  const segments = deriveOrderedSegments(order, coordinates);
  const pathLengthMetres = segments.reduce((sum, segment) => sum + segment.lengthMetres, 0);
  const firstTerminal = coordinates.find((item) => item.moduleNumber === order[0]);
  const lastTerminal = coordinates.find((item) => item.moduleNumber === order.at(-1));

  return {
    schemaVersion: TOPOLOGY_SCHEMA,
    moduleCount,
    pitchMetres,
    topology,
    order,
    coordinates,
    segments,
    pathLengthMetres,
    terminalSeparationMetres: Math.hypot(
      lastTerminal.xMetres - firstTerminal.xMetres,
      lastTerminal.yMetres - firstTerminal.yMetres,
    ),
    firstTerminalModule: order[0],
    lastTerminalModule: order.at(-1),
  };
}
