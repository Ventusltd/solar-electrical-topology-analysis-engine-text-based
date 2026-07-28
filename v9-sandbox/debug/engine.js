export const LIMITS = Object.freeze({
  maxMppts: 100,
  maxInputsPerMppt: 4,
  maxActiveStrings: 24,
  maxModulesPerString: 30,
});

const COPPER_RESISTIVITY_20C_OHM_MM2_PER_M = 0.017241;
const COPPER_TEMP_COEFFICIENT_PER_C = 0.00393;

export class EngineInputError extends Error {
  constructor(message, field) {
    super(message);
    this.name = "EngineInputError";
    this.field = field;
  }
}

function integer(value, field, minimum, maximum) {
  const parsed = Number(value);
  if (!Number.isInteger(parsed) || parsed < minimum || parsed > maximum) {
    throw new EngineInputError(`${field} must be an integer from ${minimum} to ${maximum}.`, field);
  }
  return parsed;
}

function finite(value, field, minimum = -Infinity) {
  const parsed = Number(value);
  if (!Number.isFinite(parsed) || parsed < minimum) {
    throw new EngineInputError(`${field} must be a finite number not less than ${minimum}.`, field);
  }
  return parsed;
}

export function parseIntegerList(value) {
  return String(value ?? "")
    .split(/[^0-9]+/)
    .filter(Boolean)
    .map(Number)
    .filter(Number.isInteger);
}

export function topologyOrder(moduleCount, topology, customOrder = []) {
  const count = integer(moduleCount, "moduleCount", 1, LIMITS.maxModulesPerString);
  const sequential = Array.from({ length: count }, (_, index) => index + 1);
  if (topology === "sequential") return sequential;
  if (topology === "mirrored-sequential") return [...sequential].reverse();
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
    return sequential.filter((n) => n % 2 === 1)
      .concat(sequential.filter((n) => n % 2 === 0).reverse());
  }
  if (topology === "custom") {
    const parsed = Array.isArray(customOrder) ? customOrder.map(Number) : parseIntegerList(customOrder);
    const complete = parsed.length === count;
    const unique = new Set(parsed).size === parsed.length;
    const inRange = parsed.every((n) => Number.isInteger(n) && n >= 1 && n <= count);
    if (!complete || !unique || !inRange) {
      throw new EngineInputError("customOrder must contain every module number exactly once.", "customOrder");
    }
    return parsed;
  }
  throw new EngineInputError(`Unsupported topology: ${topology}`, "topology");
}

export function allocateMppts({ mpptCount, defaultInputsPerMppt, allocationOverride = [] }) {
  const count = integer(mpptCount, "mpptCount", 1, LIMITS.maxMppts);
  const defaultInputs = integer(defaultInputsPerMppt, "defaultInputsPerMppt", 0, LIMITS.maxInputsPerMppt);
  const override = Array.isArray(allocationOverride)
    ? allocationOverride.map(Number)
    : parseIntegerList(allocationOverride);
  const requested = override.length
    ? Array.from({ length: count }, (_, index) => override[index] ?? 0)
    : Array(count).fill(defaultInputs);
  requested.forEach((value, index) => integer(value, `allocationOverride[${index}]`, 0, LIMITS.maxInputsPerMppt));

  let remaining = LIMITS.maxActiveStrings;
  const accepted = requested.map((value) => {
    const result = Math.min(value, remaining);
    remaining -= result;
    return result;
  });
  return {
    requested,
    accepted,
    requestedStrings: requested.reduce((sum, value) => sum + value, 0),
    activeStrings: accepted.reduce((sum, value) => sum + value, 0),
    truncated: requested.some((value, index) => value !== accepted[index]),
  };
}

export function correctedVoc({ vocStc, vocTempCoefficientPercentPerC, cellTemperatureC }) {
  const voc = finite(vocStc, "vocStc", 0);
  const coefficient = finite(vocTempCoefficientPercentPerC, "vocTempCoefficientPercentPerC");
  const temperature = finite(cellTemperatureC, "cellTemperatureC");
  return voc * (1 + (coefficient / 100) * (temperature - 25));
}

export function conductorResistanceOhm({ lengthM, csaMm2, conductorTemperatureC = 20 }) {
  const length = finite(lengthM, "lengthM", 0);
  const csa = finite(csaMm2, "csaMm2", Number.EPSILON);
  const temperature = finite(conductorTemperatureC, "conductorTemperatureC");
  const resistivity = COPPER_RESISTIVITY_20C_OHM_MM2_PER_M
    * (1 + COPPER_TEMP_COEFFICIENT_PER_C * (temperature - 20));
  return resistivity * length / csa;
}

function buildModules(moduleCount, modulePitchM) {
  return Array.from({ length: moduleCount }, (_, index) => ({
    id: `M-${String(index + 1).padStart(2, "0")}`,
    number: index + 1,
    physicalIndex: index,
    centreXM: index * modulePitchM,
    terminals: {
      negative: `M-${String(index + 1).padStart(2, "0")}:NEG`,
      positive: `M-${String(index + 1).padStart(2, "0")}:POS`,
    },
  }));
}

function buildStringSegments({ stringId, modules, order, routeOneWayM, positiveLeadM, negativeLeadM, externalCableCsaMm2, factoryLeadCsaMm2 }) {
  const byNumber = new Map(modules.map((module) => [module.number, module]));
  const segments = [];
  segments.push({ id: `${stringId}:HOME_NEG`, type: "home-run", from: `${stringId}:MPPT_NEG`, to: byNumber.get(order[0]).terminals.negative, lengthM: routeOneWayM, csaMm2: externalCableCsaMm2, basis: "user route" });
  for (let index = 0; index < order.length - 1; index += 1) {
    const fromModule = byNumber.get(order[index]);
    const toModule = byNumber.get(order[index + 1]);
    const physicalSeparationM = Math.abs(toModule.centreXM - fromModule.centreXM);
    segments.push({
      id: `${stringId}:LINK_${index + 1}`,
      type: "module-interconnect",
      from: fromModule.terminals.positive,
      to: toModule.terminals.negative,
      physicalSeparationM,
      availableFactoryLeadM: positiveLeadM + negativeLeadM,
      extensionRequiredM: Math.max(0, physicalSeparationM - positiveLeadM - negativeLeadM),
      csaMm2: factoryLeadCsaMm2,
      basis: "centre-to-centre screening estimate; terminal coordinates not yet modelled",
    });
  }
  segments.push({ id: `${stringId}:HOME_POS`, type: "home-run", from: byNumber.get(order.at(-1)).terminals.positive, to: `${stringId}:MPPT_POS`, lengthM: routeOneWayM, csaMm2: externalCableCsaMm2, basis: "user route" });
  return segments;
}

export function computeProject(rawInput = {}) {
  const input = {
    mpptCount: rawInput.mpptCount ?? 12,
    defaultInputsPerMppt: rawInput.defaultInputsPerMppt ?? 2,
    allocationOverride: rawInput.allocationOverride ?? [],
    modulesPerString: rawInput.modulesPerString ?? 30,
    topology: rawInput.topology ?? "leapfrog",
    customOrder: rawInput.customOrder ?? [],
    moduleWidthM: rawInput.moduleWidthM ?? 1.303,
    moduleGapM: rawInput.moduleGapM ?? 0,
    positiveLeadM: rawInput.positiveLeadM ?? 1.4,
    negativeLeadM: rawInput.negativeLeadM ?? 1.4,
    routeOneWayM: rawInput.routeOneWayM ?? 10,
    externalCableCsaMm2: rawInput.externalCableCsaMm2 ?? 6,
    factoryLeadCsaMm2: rawInput.factoryLeadCsaMm2 ?? 4,
    moduleVocStcV: rawInput.moduleVocStcV ?? 50,
    vocTempCoefficientPercentPerC: rawInput.vocTempCoefficientPercentPerC ?? -0.24,
    cellTemperatureC: rawInput.cellTemperatureC ?? 20,
    systemVoltageLimitV: rawInput.systemVoltageLimitV ?? 1500,
    operatingCurrentA: rawInput.operatingCurrentA ?? 17.31,
    conductorTemperatureC: rawInput.conductorTemperatureC ?? 70,
  };

  const modulesPerString = integer(input.modulesPerString, "modulesPerString", 1, LIMITS.maxModulesPerString);
  const moduleWidthM = finite(input.moduleWidthM, "moduleWidthM", Number.EPSILON);
  const moduleGapM = finite(input.moduleGapM, "moduleGapM", 0);
  const modulePitchM = moduleWidthM + moduleGapM;
  const allocation = allocateMppts(input);
  const order = topologyOrder(modulesPerString, input.topology, input.customOrder);
  const moduleVocCorrectedV = correctedVoc({
    vocStc: input.moduleVocStcV,
    vocTempCoefficientPercentPerC: input.vocTempCoefficientPercentPerC,
    cellTemperatureC: input.cellTemperatureC,
  });
  const stringVocV = moduleVocCorrectedV * modulesPerString;
  const systemVoltageLimitV = finite(input.systemVoltageLimitV, "systemVoltageLimitV", Number.EPSILON);
  const operatingCurrentA = finite(input.operatingCurrentA, "operatingCurrentA", 0);

  const mppts = [];
  const strings = [];
  let stringNumber = 1;
  allocation.accepted.forEach((inputCount, mpptIndex) => {
    const mppt = { id: `MPPT-${String(mpptIndex + 1).padStart(3, "0")}`, number: mpptIndex + 1, inputs: [] };
    for (let inputNumber = 1; inputNumber <= inputCount; inputNumber += 1) {
      const stringId = `S-${String(stringNumber).padStart(4, "0")}`;
      const modules = buildModules(modulesPerString, modulePitchM);
      const segments = buildStringSegments({
        stringId,
        modules,
        order,
        routeOneWayM: finite(input.routeOneWayM, "routeOneWayM", 0),
        positiveLeadM: finite(input.positiveLeadM, "positiveLeadM", 0),
        negativeLeadM: finite(input.negativeLeadM, "negativeLeadM", 0),
        externalCableCsaMm2: finite(input.externalCableCsaMm2, "externalCableCsaMm2", Number.EPSILON),
        factoryLeadCsaMm2: finite(input.factoryLeadCsaMm2, "factoryLeadCsaMm2", Number.EPSILON),
      });
      const homeRunLengthM = segments.filter((segment) => segment.type === "home-run").reduce((sum, segment) => sum + segment.lengthM, 0);
      const extensionLengthM = segments.filter((segment) => segment.type === "module-interconnect").reduce((sum, segment) => sum + segment.extensionRequiredM, 0);
      const externalResistanceOhm = conductorResistanceOhm({ lengthM: homeRunLengthM + extensionLengthM, csaMm2: input.externalCableCsaMm2, conductorTemperatureC: input.conductorTemperatureC });
      const voltageDropV = operatingCurrentA * externalResistanceOhm;
      const lossW = operatingCurrentA ** 2 * externalResistanceOhm;
      const string = { id: stringId, number: stringNumber, mppt: mppt.number, input: inputNumber, modules, electricalOrder: [...order], segments, calculations: { homeRunLengthM, extensionLengthM, externalResistanceOhm, voltageDropV, lossW } };
      strings.push(string);
      mppt.inputs.push({ number: inputNumber, stringId });
      stringNumber += 1;
    }
    mppts.push(mppt);
  });

  const warnings = [];
  if (allocation.truncated) warnings.push({ severity: "error", code: "ACTIVE_STRING_CAP", message: `Requested ${allocation.requestedStrings} strings; accepted ${allocation.activeStrings}.` });
  const utilisation = stringVocV / systemVoltageLimitV;
  if (utilisation >= 1) warnings.push({ severity: "error", code: "VOLTAGE_LIMIT", message: `Corrected string Voc ${stringVocV.toFixed(1)} V meets or exceeds ${systemVoltageLimitV.toFixed(0)} V.` });
  else if (utilisation >= 0.95) warnings.push({ severity: "error", code: "VOLTAGE_MARGIN", message: `Corrected string Voc uses ${(utilisation * 100).toFixed(1)}% of the system limit.` });
  const stringsRequiringExtensions = strings.filter((string) => string.calculations.extensionLengthM > 0).length;
  if (stringsRequiringExtensions) warnings.push({ severity: "warning", code: "EXTENSION_SCREEN", message: `${stringsRequiringExtensions} strings require extension cable under the provisional centre-to-centre screen. Verify actual junction-box and lead terminal coordinates.` });
  warnings.push({ severity: "info", code: "TEMPERATURE_BASIS", message: "Voc correction uses cell temperature, not ambient temperature. The user must supply the governing minimum cell temperature." });

  const totals = strings.reduce((acc, string) => {
    acc.modules += string.modules.length;
    acc.homeRunLengthM += string.calculations.homeRunLengthM;
    acc.extensionLengthM += string.calculations.extensionLengthM;
    acc.lossW += string.calculations.lossW;
    return acc;
  }, { modules: 0, homeRunLengthM: 0, extensionLengthM: 0, lossW: 0 });

  return {
    schema: "globalgrid2050.solar-dc-computation.v9.debug.1",
    generatedAt: new Date().toISOString(),
    input,
    assumptions: [
      "All active strings use the same module count and topology in this phase.",
      "Module physical positions are represented along one straight row using module width plus gap.",
      "Interconnect extension screening uses module centre separation minus both available factory leads.",
      "Exact junction-box and terminal coordinates are not yet represented; extension values are screening estimates, not construction quantities.",
      "Home-run positive and negative routes are assumed equal to routeOneWayM.",
      "Resistance calculation currently applies copper conductor properties only.",
    ],
    allocation,
    voltage: { moduleVocCorrectedV, stringVocV, systemVoltageLimitV, utilisation },
    mppts,
    strings,
    totals,
    warnings,
  };
}
