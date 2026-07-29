import { deriveQuantity, intervalBounds } from "./quantity.mjs";

function requireUnit(q, unit, name) {
  if (!q || q.unit !== unit) throw new TypeError(`${name} must use unit ${unit}`);
}

export function conductorResistance({ resistancePerMetre, length, circuitFactor = 1, id = "conductorResistance" }) {
  requireUnit(resistancePerMetre, "ohmPerMetre", "resistancePerMetre");
  requireUnit(length, "m", "length");
  if (!Number.isFinite(circuitFactor) || circuitFactor <= 0) {
    throw new TypeError("circuitFactor must be a finite positive number");
  }

  const value = resistancePerMetre.value * length.value * circuitFactor;
  const [rLo, rHi] = intervalBounds(resistancePerMetre);
  const [lLo, lHi] = intervalBounds(length);
  return deriveQuantity({
    id,
    value,
    unit: "ohm",
    inputs: [resistancePerMetre, length],
    equationId: "V10-R-001:R=Rprime*L*circuitFactor",
    uncertainty: { kind: "interval", lo: rLo * lLo * circuitFactor, hi: rHi * lHi * circuitFactor },
  });
}

export function voltageDrop({ current, resistance, id = "voltageDrop" }) {
  requireUnit(current, "A", "current");
  requireUnit(resistance, "ohm", "resistance");
  const value = current.value * resistance.value;
  const [iLo, iHi] = intervalBounds(current);
  const [rLo, rHi] = intervalBounds(resistance);
  return deriveQuantity({
    id,
    value,
    unit: "V",
    inputs: [current, resistance],
    equationId: "V10-V-001:dV=I*R",
    uncertainty: { kind: "interval", lo: iLo * rLo, hi: iHi * rHi },
  });
}

export function resistivePowerLoss({ current, resistance, id = "powerLoss" }) {
  requireUnit(current, "A", "current");
  requireUnit(resistance, "ohm", "resistance");
  const value = current.value ** 2 * resistance.value;
  const [iLo, iHi] = intervalBounds(current);
  const [rLo, rHi] = intervalBounds(resistance);
  return deriveQuantity({
    id,
    value,
    unit: "W",
    inputs: [current, resistance],
    equationId: "V10-P-001:Ploss=I^2*R",
    uncertainty: { kind: "interval", lo: iLo ** 2 * rLo, hi: iHi ** 2 * rHi },
  });
}

export function coldCorrectedModuleVoc({ vocStc, betaPercentPerKelvin, minimumCellTemperature, id = "moduleVocCold" }) {
  requireUnit(vocStc, "V", "vocStc");
  requireUnit(betaPercentPerKelvin, "1", "betaPercentPerKelvin");
  requireUnit(minimumCellTemperature, "K", "minimumCellTemperature");
  const referenceTemperatureKelvin = 298.15;
  const factor = 1 + (betaPercentPerKelvin.value / 100) * (minimumCellTemperature.value - referenceTemperatureKelvin);
  if (factor <= 0) throw new RangeError("temperature correction produced a non-positive voltage factor");

  const value = vocStc.value * factor;
  const [vocLo, vocHi] = intervalBounds(vocStc);
  const [betaLo, betaHi] = intervalBounds(betaPercentPerKelvin);
  const [tempLo, tempHi] = intervalBounds(minimumCellTemperature);
  const candidates = [];
  for (const v of [vocLo, vocHi]) {
    for (const beta of [betaLo, betaHi]) {
      for (const temp of [tempLo, tempHi]) {
        candidates.push(v * (1 + (beta / 100) * (temp - referenceTemperatureKelvin)));
      }
    }
  }

  return deriveQuantity({
    id,
    value,
    unit: "V",
    inputs: [vocStc, betaPercentPerKelvin, minimumCellTemperature],
    equationId: "V10-VOC-001:VocT=VocSTC*(1+betaPercent*(T-298.15)/100)",
    uncertainty: { kind: "interval", lo: Math.min(...candidates), hi: Math.max(...candidates) },
    evidenceStatus: "candidate-needs-standards-verification",
  });
}

export function seriesStringVoltage({ moduleVoltage, moduleCount, id = "stringVoltage" }) {
  requireUnit(moduleVoltage, "V", "moduleVoltage");
  if (!Number.isInteger(moduleCount) || moduleCount < 1) throw new TypeError("moduleCount must be a positive integer");
  const [lo, hi] = intervalBounds(moduleVoltage);
  return deriveQuantity({
    id,
    value: moduleVoltage.value * moduleCount,
    unit: "V",
    inputs: [moduleVoltage],
    equationId: "V10-V-002:Vstring=N*Vmodule",
    uncertainty: { kind: "interval", lo: lo * moduleCount, hi: hi * moduleCount },
  });
}
