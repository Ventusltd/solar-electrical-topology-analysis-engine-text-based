export const SCHEMA_VERSION = "b9-scene-0.1.0";

export function makeId(prefix, index) {
  return `${prefix}-${String(index).padStart(4, "0")}`;
}

export function modulePitch(scene) {
  const alongRow = scene.module.orientation === "portrait"
    ? scene.module.widthM
    : scene.module.heightM;
  return alongRow + scene.module.gapM;
}

export function rowSpan(scene) {
  const count = scene.electrical.modulesPerString;
  const alongRow = scene.module.orientation === "portrait"
    ? scene.module.widthM
    : scene.module.heightM;
  return count * alongRow + Math.max(0, count - 1) * scene.module.gapM;
}

export function topologyOrder(moduleCount, topology, customText = "") {
  if (topology === "sequential") {
    return Array.from({ length: moduleCount }, (_, index) => index + 1);
  }

  if (topology === "leapfrog") {
    const odd = [];
    const even = [];
    for (let number = 1; number <= moduleCount; number += 1) {
      if (number % 2 === 1) {
        odd.push(number);
      } else {
        even.push(number);
      }
    }
    return odd.concat(even.reverse());
  }

  if (topology === "mirrored-sequential") {
    return Array.from({ length: moduleCount }, (_, index) => moduleCount - index);
  }

  if (topology === "alternating-return") {
    const first = [];
    const second = [];
    for (let number = 1; number <= moduleCount; number += 1) {
      if (number <= Math.ceil(moduleCount / 2)) {
        first.push(number);
      } else {
        second.unshift(number);
      }
    }
    return first.concat(second);
  }

  const custom = customText
    .split(/[^0-9]+/)
    .map((value) => Number(value))
    .filter((value) => Number.isInteger(value));

  if (custom.length !== moduleCount) {
    return [];
  }

  const unique = new Set(custom);
  if (unique.size !== moduleCount) {
    return [];
  }

  const valid = custom.every((value) => value >= 1 && value <= moduleCount);
  return valid ? custom : [];
}

export function buildScene(input, cartridge) {
  const scene = {
    schemaVersion: SCHEMA_VERSION,
    cartridge: {
      id: cartridge.id,
      name: cartridge.name,
      version: cartridge.version,
      faces: cartridge.faces,
      modulesHigh: cartridge.modulesHigh,
      tracker: cartridge.tracker,
      eastWest: cartridge.eastWest,
    },
    module: {
      widthM: input.moduleWidthM,
      heightM: input.moduleHeightM,
      gapM: input.moduleGapM,
      orientation: input.orientation,
      positiveLeadM: input.positiveLeadM,
      negativeLeadM: input.negativeLeadM,
      junctionBoxMode: input.junctionBoxMode,
    },
    geometry: {
      lowEdgeM: input.lowEdgeM,
      highEdgeM: input.highEdgeM,
      ridgeGapM: input.ridgeGapM,
      rowPitchM: input.rowPitchM,
      trackerAngleDeg: input.trackerAngleDeg,
      inverterDistanceM: input.inverterDistanceM,
    },
    electrical: {
      modulesPerString: input.modulesPerString,
      stringCount: input.stringCount,
      topology: input.topology,
      customOrder: input.customOrder,
      externalCableCsaMm2: input.externalCableCsaMm2,
      factoryLeadCsaMm2: input.factoryLeadCsaMm2,
    },
    modules: [],
    strings: [],
    warnings: [],
  };

  const pitch = modulePitch(scene);
  const order = topologyOrder(
    scene.electrical.modulesPerString,
    scene.electrical.topology,
    scene.electrical.customOrder,
  );

  if (order.length === 0) {
    scene.warnings.push("Custom electrical order is invalid or incomplete.");
  }

  const modulesPerString = scene.electrical.modulesPerString;
  const stringCount = scene.electrical.stringCount;

  for (let stringIndex = 0; stringIndex < stringCount; stringIndex += 1) {
    const stringId = makeId("S", stringIndex + 1);
    const stringModules = [];

    for (let moduleIndex = 0; moduleIndex < modulesPerString; moduleIndex += 1) {
      const moduleNumber = moduleIndex + 1;
      const moduleId = `${stringId}-M${moduleNumber}`;
      const x = moduleIndex * pitch;
      const y = stringIndex * scene.geometry.rowPitchM;
      const moduleRecord = {
        id: moduleId,
        stringId,
        moduleNumber,
        xM: x,
        yM: y,
        widthM: scene.module.orientation === "portrait"
          ? scene.module.widthM
          : scene.module.heightM,
        heightM: scene.module.orientation === "portrait"
          ? scene.module.heightM
          : scene.module.widthM,
        negativeTerminalId: `${moduleId}-NEG`,
        positiveTerminalId: `${moduleId}-POS`,
      };
      scene.modules.push(moduleRecord);
      stringModules.push(moduleRecord);
    }

    const connections = [];
    for (let index = 0; index < order.length - 1; index += 1) {
      const fromNumber = order[index];
      const toNumber = order[index + 1];
      connections.push({
        id: `${stringId}-C${String(index + 1).padStart(2, "0")}`,
        fromTerminalId: `${stringId}-M${fromNumber}-POS`,
        toTerminalId: `${stringId}-M${toNumber}-NEG`,
        fromModule: fromNumber,
        toModule: toNumber,
      });
    }

    scene.strings.push({
      id: stringId,
      moduleIds: stringModules.map((module) => module.id),
      order,
      connections,
      freeNegativeTerminalId: order.length
        ? `${stringId}-M${order[0]}-NEG`
        : null,
      freePositiveTerminalId: order.length
        ? `${stringId}-M${order[order.length - 1]}-POS`
        : null,
    });
  }

  const requiredReachM = scene.electrical.topology === "leapfrog"
    ? 2 * pitch
    : pitch;
  const availableReachM = scene.module.positiveLeadM
    + scene.module.negativeLeadM;

  scene.feasibility = {
    requiredReachM,
    availableReachM,
    passes: availableReachM + 1e-9 >= requiredReachM,
    shortfallM: Math.max(0, requiredReachM - availableReachM),
  };

  if (!scene.feasibility.passes) {
    scene.warnings.push(
      `Factory leads are short by ${scene.feasibility.shortfallM.toFixed(3)} m.`,
    );
  }

  return scene;
}

export function deriveSummary(scene) {
  const spanM = rowSpan(scene);
  const strings = scene.electrical.stringCount;
  const sequentialExtraM = scene.electrical.topology === "sequential"
    ? spanM * strings
    : 0;
  const baseHomeRunM = 2 * scene.geometry.inverterDistanceM * strings;
  const externalCableM = baseHomeRunM + sequentialExtraM;
  const factoryLeadM = scene.electrical.modulesPerString
    * strings
    * (scene.module.positiveLeadM + scene.module.negativeLeadM);
  const connectorCount = scene.strings.reduce(
    (total, stringRecord) => total + stringRecord.connections.length + 2,
    0,
  );
  const commercialExternalCopperKg =
    scene.electrical.externalCableCsaMm2 * (externalCableM / 1000) * 9.6;
  const commercialFactoryCopperKg =
    scene.electrical.factoryLeadCsaMm2 * (factoryLeadM / 1000) * 9.6;

  return {
    moduleCount: scene.modules.length,
    stringCount: strings,
    rowSpanM: spanM,
    connectionCount: connectorCount,
    externalCableM,
    factoryLeadM,
    commercialExternalCopperKg,
    commercialFactoryCopperKg,
    totalCommercialCopperKg:
      commercialExternalCopperKg + commercialFactoryCopperKg,
    freeNegative: scene.strings[0]?.freeNegativeTerminalId ?? "—",
    freePositive: scene.strings[0]?.freePositiveTerminalId ?? "—",
  };
}

export function toGeoJson(scene) {
  const features = scene.modules.map((module) => {
    const x0 = module.xM;
    const y0 = module.yM;
    const x1 = x0 + module.widthM;
    const y1 = y0 + module.heightM;
    return {
      type: "Feature",
      id: module.id,
      properties: {
        schema_version: scene.schemaVersion,
        object_type: "module",
        string_id: module.stringId,
        module_number: module.moduleNumber,
      },
      geometry: {
        type: "Polygon",
        coordinates: [[
          [x0, y0],
          [x1, y0],
          [x1, y1],
          [x0, y1],
          [x0, y0],
        ]],
      },
    };
  });

  return {
    type: "FeatureCollection",
    name: "b9-array-scene",
    crs: {
      type: "name",
      properties: { name: "LOCAL_ENGINEERING_METRES" },
    },
    features,
  };
}
