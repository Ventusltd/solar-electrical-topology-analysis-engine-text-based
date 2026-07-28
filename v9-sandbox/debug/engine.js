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
  const invalid = (
    !Number.isInteger(parsed)
    || parsed < minimum
    || parsed > maximum
  );
  if (invalid) {
    const message = (
      `${field} must be an integer from ${minimum} to ${maximum}.`
    );
    throw new EngineInputError(message, field);
  }
  return parsed;
}

function finite(value, field, minimum = -Infinity) {
  const parsed = Number(value);
  if (!Number.isFinite(parsed) || parsed < minimum) {
    const message = (
      `${field} must be a finite number not less than ${minimum}.`
    );
    throw new EngineInputError(message, field);
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

export function topologyOrder(
  moduleCount,
  topology,
  customOrder = [],
) {
  const count = integer(
    moduleCount,
    "moduleCount",
    1,
    LIMITS.maxModulesPerString,
  );
  const sequential = Array.from(
    { length: count },
    (_, index) => index + 1,
  );

  if (topology === "sequential") {
    return sequential;
  }
  if (topology === "mirrored-sequential") {
    return [...sequential].reverse();
  }
  if (topology === "alternating-return") {
    const order = [];
    let low = 1;
    let high = count;
    while (low <= high) {
      order.push(low);
      if (low !== high) {
        order.push(high);
      }
      low += 1;
      high -= 1;
    }
    return order;
  }
  if (topology === "leapfrog") {
    const odds = sequential.filter((number) => number % 2 === 1);
    const evens = sequential
      .filter((number) => number % 2 === 0)
      .reverse();
    return odds.concat(evens);
  }
  if (topology === "custom") {
    const parsed = Array.isArray(customOrder)
      ? customOrder.map(Number)
      : parseIntegerList(customOrder);
    const complete = parsed.length === count;
    const unique = new Set(parsed).size === parsed.length;
    const inRange = parsed.every((number) => (
      Number.isInteger(number)
      && number >= 1
      && number <= count
    ));
    if (!complete || !unique || !inRange) {
      throw new EngineInputError(
        "customOrder must contain every module number exactly once.",
        "customOrder",
      );
    }
    return parsed;
  }

  throw new EngineInputError(
    `Unsupported topology: ${topology}`,
    "topology",
  );
}

export function allocateMppts({
  mpptCount,
  defaultInputsPerMppt,
  allocationOverride = [],
}) {
  const count = integer(
    mpptCount,
    "mpptCount",
    1,
    LIMITS.maxMppts,
  );
  const defaultInputs = integer(
    defaultInputsPerMppt,
    "defaultInputsPerMppt",
    0,
    LIMITS.maxInputsPerMppt,
  );
  const override = Array.isArray(allocationOverride)
    ? allocationOverride.map(Number)
    : parseIntegerList(allocationOverride);
  const requested = override.length
    ? Array.from(
      { length: count },
      (_, index) => override[index] ?? 0,
    )
    : Array(count).fill(defaultInputs);

  requested.forEach((value, index) => {
    integer(
      value,
      `allocationOverride[${index}]`,
      0,
      LIMITS.maxInputsPerMppt,
    );
  });

  let remaining = LIMITS.maxActiveStrings;
  const accepted = requested.map((value) => {
    const result = Math.min(value, remaining);
    remaining -= result;
    return result;
  });

  return {
    requested,
    accepted,
    requestedStrings: requested.reduce(
      (sum, value) => sum + value,
      0,
    ),
    activeStrings: accepted.reduce(
      (sum, value) => sum + value,
      0,
    ),
    truncated: requested.some(
      (value, index) => value !== accepted[index],
    ),
  };
}

export function correctedVoc({
  vocStc,
  vocTempCoefficientPercentPerC,
  cellTemperatureC,
}) {
  const voc = finite(vocStc, "vocStc", 0);
  const coefficient = finite(
    vocTempCoefficientPercentPerC,
    "vocTempCoefficientPercentPerC",
  );
  const temperature = finite(
    cellTemperatureC,
    "cellTemperatureC",
  );
  return voc * (1 + (coefficient / 100) * (temperature - 25));
}

export function conductorResistanceOhm({
  lengthM,
  csaMm2,
  conductorTemperatureC = 20,
}) {
  const length = finite(lengthM, "lengthM", 0);
  const csa = finite(csaMm2, "csaMm2", Number.EPSILON);
  const temperature = finite(
    conductorTemperatureC,
    "conductorTemperatureC",
  );
  const resistivity = (
    COPPER_RESISTIVITY_20C_OHM_MM2_PER_M
    * (
      1
      + COPPER_TEMP_COEFFICIENT_PER_C
      * (temperature - 20)
    )
  );
  return resistivity * length / csa;
}

function buildModules(moduleCount, modulePitchM) {
  return Array.from(
    { length: moduleCount },
    (_, index) => {
      const number = index + 1;
      const id = `M-${String(number).padStart(2, "0")}`;
      return {
        id,
        number,
        physicalIndex: index,
        centreXM: index * modulePitchM,
        terminals: {
          negative: `${id}:NEG`,
          positive: `${id}:POS`,
        },
      };
    },
  );
}

function buildStringSegments({
  stringId,
  modules,
  order,
  routeOneWayM,
  positiveLeadM,
  negativeLeadM,
  externalCableCsaMm2,
  factoryLeadCsaMm2,
}) {
  const byNumber = new Map(
    modules.map((module) => [module.number, module]),
  );
  const firstModule = byNumber.get(order[0]);
  const lastModule = byNumber.get(order.at(-1));
  const segments = [
    {
      id: `${stringId}:HOME_NEG`,
      type: "home-run",
      from: `${stringId}:MPPT_NEG`,
      to: firstModule.terminals.negative,
      lengthM: routeOneWayM,
      csaMm2: externalCableCsaMm2,
      basis: "user route",
    },
  ];

  for (let index = 0; index < order.length - 1; index += 1) {
    const fromModule = byNumber.get(order[index]);
    const toModule = byNumber.get(order[index + 1]);
    const physicalSeparationM = Math.abs(
      toModule.centreXM - fromModule.centreXM,
    );
    const availableFactoryLeadM = positiveLeadM + negativeLeadM;
    segments.push({
      id: `${stringId}:LINK_${index + 1}`,
      type: "module-interconnect",
      from: fromModule.terminals.positive,
      to: toModule.terminals.negative,
      physicalSeparationM,
      availableFactoryLeadM,
      extensionRequiredM: Math.max(
        0,
        physicalSeparationM - availableFactoryLeadM,
      ),
      csaMm2: factoryLeadCsaMm2,
      basis: (
        "centre-to-centre screening estimate; "
        + "terminal coordinates not yet modelled"
      ),
    });
  }

  segments.push({
    id: `${stringId}:HOME_POS`,
    type: "home-run",
    from: lastModule.terminals.positive,
    to: `${stringId}:MPPT_POS`,
    lengthM: routeOneWayM,
    csaMm2: externalCableCsaMm2,
    basis: "user route",
  });

  return segments;
}

function sumSegments(segments, type, field) {
  return segments
    .filter((segment) => segment.type === type)
    .reduce((sum, segment) => sum + segment[field], 0);
}

function buildString({
  stringNumber,
  mpptNumber,
  inputNumber,
  modulesPerString,
  modulePitchM,
  order,
  input,
  operatingCurrentA,
}) {
  const stringId = `S-${String(stringNumber).padStart(4, "0")}`;
  const modules = buildModules(modulesPerString, modulePitchM);
  const segments = buildStringSegments({
    stringId,
    modules,
    order,
    routeOneWayM: finite(input.routeOneWayM, "routeOneWayM", 0),
    positiveLeadM: finite(input.positiveLeadM, "positiveLeadM", 0),
    negativeLeadM: finite(input.negativeLeadM, "negativeLeadM", 0),
    externalCableCsaMm2: finite(
      input.externalCableCsaMm2,
      "externalCableCsaMm2",
      Number.EPSILON,
    ),
    factoryLeadCsaMm2: finite(
      input.factoryLeadCsaMm2,
      "factoryLeadCsaMm2",
      Number.EPSILON,
    ),
  });
  const homeRunLengthM = sumSegments(
    segments,
    "home-run",
    "lengthM",
  );
  const extensionLengthM = sumSegments(
    segments,
    "module-interconnect",
    "extensionRequiredM",
  );
  const externalResistanceOhm = conductorResistanceOhm({
    lengthM: homeRunLengthM + extensionLengthM,
    csaMm2: input.externalCableCsaMm2,
    conductorTemperatureC: input.conductorTemperatureC,
  });
  const voltageDropV = operatingCurrentA * externalResistanceOhm;
  const lossW = operatingCurrentA ** 2 * externalResistanceOhm;

  return {
    id: stringId,
    number: stringNumber,
    mppt: mpptNumber,
    input: inputNumber,
    modules,
    electricalOrder: [...order],
    segments,
    calculations: {
      homeRunLengthM,
      extensionLengthM,
      externalResistanceOhm,
      voltageDropV,
      lossW,
    },
  };
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
    vocTempCoefficientPercentPerC: (
      rawInput.vocTempCoefficientPercentPerC ?? -0.24
    ),
    cellTemperatureC: rawInput.cellTemperatureC ?? 20,
    systemVoltageLimitV: rawInput.systemVoltageLimitV ?? 1500,
    operatingCurrentA: rawInput.operatingCurrentA ?? 17.31,
    conductorTemperatureC: rawInput.conductorTemperatureC ?? 70,
  };

  const modulesPerString = integer(
    input.modulesPerString,
    "modulesPerString",
    1,
    LIMITS.maxModulesPerString,
  );
  const moduleWidthM = finite(
    input.moduleWidthM,
    "moduleWidthM",
    Number.EPSILON,
  );
  const moduleGapM = finite(
    input.moduleGapM,
    "moduleGapM",
    0,
  );
  const modulePitchM = moduleWidthM + moduleGapM;
  const allocation = allocateMppts(input);
  const order = topologyOrder(
    modulesPerString,
    input.topology,
    input.customOrder,
  );
  const moduleVocCorrectedV = correctedVoc({
    vocStc: input.moduleVocStcV,
    vocTempCoefficientPercentPerC: (
      input.vocTempCoefficientPercentPerC
    ),
    cellTemperatureC: input.cellTemperatureC,
  });
  const stringVocV = moduleVocCorrectedV * modulesPerString;
  const systemVoltageLimitV = finite(
    input.systemVoltageLimitV,
    "systemVoltageLimitV",
    Number.EPSILON,
  );
  const operatingCurrentA = finite(
    input.operatingCurrentA,
    "operatingCurrentA",
    0,
  );

  const mppts = [];
  const strings = [];
  let stringNumber = 1;

  allocation.accepted.forEach((inputCount, mpptIndex) => {
    const mpptNumber = mpptIndex + 1;
    const mppt = {
      id: `MPPT-${String(mpptNumber).padStart(3, "0")}`,
      number: mpptNumber,
      inputs: [],
    };

    for (
      let inputNumber = 1;
      inputNumber <= inputCount;
      inputNumber += 1
    ) {
      const string = buildString({
        stringNumber,
        mpptNumber,
        inputNumber,
        modulesPerString,
        modulePitchM,
        order,
        input,
        operatingCurrentA,
      });
      strings.push(string);
      mppt.inputs.push({
        number: inputNumber,
        stringId: string.id,
      });
      stringNumber += 1;
    }
    mppts.push(mppt);
  });

  const warnings = [];
  if (allocation.truncated) {
    warnings.push({
      severity: "error",
      code: "ACTIVE_STRING_CAP",
      message: (
        `Requested ${allocation.requestedStrings} strings; `
        + `accepted ${allocation.activeStrings}.`
      ),
    });
  }

  const utilisation = stringVocV / systemVoltageLimitV;
  if (utilisation >= 1) {
    warnings.push({
      severity: "error",
      code: "VOLTAGE_LIMIT",
      message: (
        `Corrected string Voc ${stringVocV.toFixed(1)} V `
        + `meets or exceeds ${systemVoltageLimitV.toFixed(0)} V.`
      ),
    });
  } else if (utilisation >= 0.95) {
    warnings.push({
      severity: "error",
      code: "VOLTAGE_MARGIN",
      message: (
        `Corrected string Voc uses `
        + `${(utilisation * 100).toFixed(1)}% of the system limit.`
      ),
    });
  }

  const stringsRequiringExtensions = strings.filter(
    (string) => string.calculations.extensionLengthM > 0,
  ).length;
  if (stringsRequiringExtensions) {
    warnings.push({
      severity: "warning",
      code: "EXTENSION_SCREEN",
      message: (
        `${stringsRequiringExtensions} strings require extension cable `
        + "under the provisional centre-to-centre screen. Verify actual "
        + "junction-box and lead terminal coordinates."
      ),
    });
  }
  warnings.push({
    severity: "info",
    code: "TEMPERATURE_BASIS",
    message: (
      "Voc correction uses cell temperature, not ambient temperature. "
      + "The user must supply the governing minimum cell temperature."
    ),
  });

  const totals = strings.reduce(
    (accumulator, string) => {
      accumulator.modules += string.modules.length;
      accumulator.homeRunLengthM += (
        string.calculations.homeRunLengthM
      );
      accumulator.extensionLengthM += (
        string.calculations.extensionLengthM
      );
      accumulator.lossW += string.calculations.lossW;
      return accumulator;
    },
    {
      modules: 0,
      homeRunLengthM: 0,
      extensionLengthM: 0,
      lossW: 0,
    },
  );

  return {
    schema: "globalgrid2050.solar-dc-computation.v9.debug.1",
    generatedAt: new Date().toISOString(),
    input,
    assumptions: [
      "All active strings use one module count and topology in this phase.",
      "Modules occupy one straight row using module width plus gap.",
      (
        "Interconnect screening uses module-centre separation minus both "
        + "available factory leads."
      ),
      (
        "Exact terminal coordinates are absent; extension values are "
        + "screening estimates, not construction quantities."
      ),
      "Positive and negative home-run routes both equal routeOneWayM.",
      "Resistance currently uses copper conductor properties only.",
    ],
    allocation,
    voltage: {
      moduleVocCorrectedV,
      stringVocV,
      systemVoltageLimitV,
      utilisation,
    },
    mppts,
    strings,
    totals,
    warnings,
  };
}
