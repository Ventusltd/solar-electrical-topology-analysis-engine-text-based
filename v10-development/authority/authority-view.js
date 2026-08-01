export const AUTHORITY_BUNDLE_URL = '../../authority-bundles/reference-inverter-block.json';

function requireObject(value, name) {
  if (value === null || typeof value !== 'object' || Array.isArray(value)) {
    throw new TypeError(`${name} must be an object`);
  }
  return value;
}

function requireValue(value, name) {
  if (value === undefined) throw new TypeError(`${name} is required`);
  return value;
}

export function authoritySummary(bundle) {
  const response = requireObject(bundle, 'authority response');
  const block = requireObject(response.inverter_block, 'inverter_block');
  const boundary = requireObject(block.product_boundary, 'product_boundary');
  const evidence = requireObject(block.equipment_evidence, 'equipment_evidence');
  const build025 = requireObject(response.build025, 'build025');

  return Object.freeze({
    schemaVersion: requireValue(response.schema_version, 'schema_version'),
    strategy: requireValue(response.strategy, 'strategy'),
    modulePowerWp: requireValue(boundary.module_rated_power_wp, 'module_rated_power_wp'),
    modulesPerString: requireValue(boundary.modules_per_string, 'modules_per_string'),
    stringCount: requireValue(boundary.string_count, 'string_count'),
    moduleCount: requireValue(boundary.module_count, 'module_count'),
    dcPowerKwp: requireValue(boundary.dc_nameplate_power_kwp, 'dc_nameplate_power_kwp'),
    inverterPowerKva: requireValue(boundary.inverter_apparent_power_kva, 'inverter_apparent_power_kva'),
    dcAcRatio: requireValue(boundary.dc_ac_nameplate_ratio, 'dc_ac_nameplate_ratio'),
    evidenceState: requireValue(evidence.state, 'equipment evidence state'),
    missingEvidenceCount: requireValue(evidence.missing_evidence_count, 'missing evidence count'),
    responseHash: requireValue(response.response_hash, 'response_hash'),
    blockReceiptHash: requireValue(block.receipt_hash, 'inverter block receipt_hash'),
    build025ReceiptHash: requireValue(build025.receipt_hash, 'Build 025 receipt_hash')
  });
}

function setText(documentRef, id, value) {
  const element = documentRef.getElementById(id);
  if (!element) throw new Error(`authority projection element is missing: ${id}`);
  element.textContent = String(value);
}

export function renderAuthorityBundle(documentRef, bundle) {
  const summary = authoritySummary(bundle);
  const view = documentRef.getElementById('authority-view');
  const banner = documentRef.getElementById('authority-banner');
  if (!view || !banner) throw new Error('authority view shell is incomplete');

  const values = {
    'authority-strategy': summary.strategy,
    'authority-module-power': `${summary.modulePowerWp} Wp`,
    'authority-modules-per-string': summary.modulesPerString,
    'authority-string-count': summary.stringCount,
    'authority-module-count': summary.moduleCount,
    'authority-dc-power': `${summary.dcPowerKwp} kWp`,
    'authority-inverter-power': `${summary.inverterPowerKva} kVA`,
    'authority-dc-ac-ratio': summary.dcAcRatio,
    'authority-evidence-state': summary.evidenceState,
    'authority-missing-evidence': summary.missingEvidenceCount,
    'authority-response-hash': summary.responseHash,
    'authority-block-hash': summary.blockReceiptHash,
    'authority-build025-hash': summary.build025ReceiptHash
  };
  for (const [id, value] of Object.entries(values)) setText(documentRef, id, value);

  view.dataset.authorityState = 'verified-bundle';
  banner.textContent = 'PYTHON AUTHORITY — VERIFIED COMMITTED BUNDLE';
  return summary;
}

export async function loadAuthorityBundle({
  fetchImpl = globalThis.fetch,
  documentRef = globalThis.document
} = {}) {
  if (typeof fetchImpl !== 'function') throw new TypeError('fetch implementation is required');
  if (!documentRef) throw new TypeError('document is required');

  const response = await fetchImpl(AUTHORITY_BUNDLE_URL, { cache: 'no-store' });
  if (!response.ok) throw new Error(`authority bundle request failed: ${response.status}`);
  const bundle = await response.json();
  renderAuthorityBundle(documentRef, bundle);
  return bundle;
}

if (typeof window !== 'undefined' && typeof document !== 'undefined') {
  loadAuthorityBundle().catch((error) => {
    const view = document.getElementById('authority-view');
    const banner = document.getElementById('authority-banner');
    if (view) view.dataset.authorityState = 'load-failed';
    if (banner) banner.textContent = `PYTHON AUTHORITY — BUNDLE LOAD FAILED: ${error.message}`;
  });
}
