import { computeTopologyGeometry } from "./topology.mjs";
import { quantity } from "./quantity.mjs";
import {
  coldCorrectedModuleVoc,
  conductorResistance,
  resistivePowerLoss,
  seriesStringVoltage,
  voltageDrop,
} from "./electrical.mjs";

export const KERNEL_SCHEMA = "globalgrid2050.solar-dc-computation.v10.kernel.1";

function requireObject(value, name) {
  if (!value || typeof value !== "object" || Array.isArray(value)) {
    throw new TypeError(`${name} must be an object`);
  }
}

export function runKernel(document) {
  requireObject(document, "document");
  requireObject(document.layout, "document.layout");
  requireObject(document.electrical, "document.electrical");

  const geometry = computeTopologyGeometry(document.layout);
  const q = document.electrical;
  const conductorLength = quantity({
    id: "geometry.pathLength",
    value: geometry.pathLengthMetres,
    unit: "m",
    provenance: "geometryDerived",
    uncertainty: q.lengthUncertaintyMetres
      ? {
          kind: "interval",
          lo: Math.max(0, geometry.pathLengthMetres - q.lengthUncertaintyMetres),
          hi: geometry.pathLengthMetres + q.lengthUncertaintyMetres,
        }
      : { kind: "none" },
    source: { equationId: "V10-GEO-001:sum(segment.length)", inputIds: [] },
    evidenceStatus: "candidate",
  });

  const resistancePerMetre = quantity({
    id: "input.resistancePerMetre",
    value: q.resistanceOhmPerMetre,
    unit: "ohmPerMetre",
    provenance: q.resistanceProvenance ?? "datasheet",
    uncertainty: q.resistanceIntervalOhmPerMetre
      ? { kind: "interval", ...q.resistanceIntervalOhmPerMetre }
      : { kind: "none" },
    source: q.resistanceSource ?? null,
    evidenceStatus: q.resistanceEvidenceStatus ?? "unverified",
  });
  const current = quantity({
    id: "input.current",
    value: q.currentAmps,
    unit: "A",
    provenance: q.currentProvenance ?? "datasheet",
    uncertainty: q.currentIntervalAmps
      ? { kind: "interval", ...q.currentIntervalAmps }
      : { kind: "none" },
    source: q.currentSource ?? null,
    evidenceStatus: q.currentEvidenceStatus ?? "unverified",
  });

  const resistance = conductorResistance({
    resistancePerMetre,
    length: conductorLength,
    circuitFactor: q.circuitFactor ?? 1,
  });
  const drop = voltageDrop({ current, resistance });
  const loss = resistivePowerLoss({ current, resistance });

  let voltageLimits = null;
  if (q.vocStcVolts != null && q.betaVocPercentPerKelvin != null && q.minimumCellTemperatureKelvin != null) {
    const vocStc = quantity({
      id: "input.vocStc",
      value: q.vocStcVolts,
      unit: "V",
      provenance: q.vocProvenance ?? "datasheet",
      uncertainty: q.vocIntervalVolts ? { kind: "interval", ...q.vocIntervalVolts } : { kind: "none" },
      source: q.vocSource ?? null,
      evidenceStatus: q.vocEvidenceStatus ?? "unverified",
    });
    const beta = quantity({
      id: "input.betaVoc",
      value: q.betaVocPercentPerKelvin,
      unit: "1",
      provenance: q.betaVocProvenance ?? "datasheet",
      uncertainty: q.betaVocIntervalPercentPerKelvin
        ? { kind: "interval", ...q.betaVocIntervalPercentPerKelvin }
        : { kind: "none" },
      source: q.betaVocSource ?? null,
      evidenceStatus: q.betaVocEvidenceStatus ?? "unverified",
    });
    const minimumTemperature = quantity({
      id: "input.minimumCellTemperature",
      value: q.minimumCellTemperatureKelvin,
      unit: "K",
      provenance: q.temperatureProvenance ?? "assumed",
      uncertainty: q.minimumCellTemperatureIntervalKelvin
        ? { kind: "interval", ...q.minimumCellTemperatureIntervalKelvin }
        : { kind: "none" },
      source: q.temperatureSource ?? null,
      evidenceStatus: q.temperatureEvidenceStatus ?? "unverified",
    });
    const moduleVocCold = coldCorrectedModuleVoc({
      vocStc,
      betaPercentPerKelvin: beta,
      minimumCellTemperature: minimumTemperature,
    });
    voltageLimits = {
      moduleVocCold,
      stringVocCold: seriesStringVoltage({ moduleVoltage: moduleVocCold, moduleCount: geometry.moduleCount }),
    };
  }

  return {
    schemaVersion: KERNEL_SCHEMA,
    documentId: document.documentId ?? null,
    geometry,
    results: {
      conductorLength,
      resistance,
      voltageDrop: drop,
      resistivePowerLoss: loss,
      voltageLimits,
    },
    warnings: [
      "Candidate kernel: outputs are not compliance conclusions.",
      "Path length currently follows module-centre geometry and does not yet include terminal offsets, lead slack or routed field cable.",
    ],
  };
}
