export const AUTHORITY_BUNDLE_URL = '../../authority-bundles/reference-inverter-block.json';

const SVG_NS = 'http://www.w3.org/2000/svg';

function requireObject(value, name) {
  if (value === null || typeof value !== 'object' || Array.isArray(value)) {
    throw new TypeError(`${name} must be an object`);
  }
  return value;
}

function requireArray(value, name) {
  if (!Array.isArray(value)) throw new TypeError(`${name} must be an array`);
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

function projectedPoint(value, name) {
  const point = requireObject(value, name);
  return Object.freeze({
    x_m: requireValue(point.x_m, `${name}.x_m`),
    y_m: requireValue(point.y_m, `${name}.y_m`)
  });
}

function projectedRoute(value, kind, name) {
  const route = requireObject(value, name);
  const vertices = requireArray(route.vertices, `${name}.vertices`).map((point, index) =>
    projectedPoint(point, `${name}.vertices[${index}]`)
  );
  return Object.freeze({
    routeId: requireValue(route.route_id, `${name}.route_id`),
    stringId: requireValue(route.string_id, `${name}.string_id`),
    kind,
    vertices: Object.freeze(vertices)
  });
}

export function authorityGeometry(bundle) {
  const response = requireObject(bundle, 'authority response');
  const build025 = requireObject(response.build025, 'build025');
  const geometry = requireObject(build025.geometry, 'build025.geometry');
  const routing = requireObject(build025.routing, 'build025.routing');
  const bounds = requireArray(geometry.bounds_m, 'build025.geometry.bounds_m');
  const placements = requireArray(geometry.placements, 'build025.geometry.placements');
  const strings = requireArray(routing.strings, 'build025.routing.strings');

  const modules = placements.map((value, index) => {
    const placement = requireObject(value, `placement[${index}]`);
    const centre = requireArray(placement.centre_m, `placement[${index}].centre_m`);
    return Object.freeze({
      moduleId: requireValue(placement.module_id, `placement[${index}].module_id`),
      x_m: requireValue(centre[0], `placement[${index}].centre_m[0]`),
      y_m: requireValue(centre[1], `placement[${index}].centre_m[1]`)
    });
  });

  const routes = [];
  for (const [stringIndex, value] of strings.entries()) {
    const stringRoute = requireObject(value, `routing.strings[${stringIndex}]`);
    routes.push(
      projectedRoute(
        stringRoute.positive_route,
        'positive-home-run',
        `routing.strings[${stringIndex}].positive_route`
      )
    );
    routes.push(
      projectedRoute(
        stringRoute.negative_route,
        'negative-home-run',
        `routing.strings[${stringIndex}].negative_route`
      )
    );
    for (const [routeIndex, route] of requireArray(
      stringRoute.interconnect_routes,
      `routing.strings[${stringIndex}].interconnect_routes`
    ).entries()) {
      routes.push(
        projectedRoute(
          route,
          'series-interconnect',
          `routing.strings[${stringIndex}].interconnect_routes[${routeIndex}]`
        )
      );
    }
  }

  return Object.freeze({
    bounds_m: Object.freeze([...bounds]),
    modules: Object.freeze(modules),
    routes: Object.freeze(routes)
  });
}

function setText(documentRef, id, value) {
  const element = documentRef.getElementById(id);
  if (!element) throw new Error(`authority projection element is missing: ${id}`);
  element.textContent = String(value);
}

function pointsAttribute(vertices) {
  return vertices.map((point) => `${point.x_m},${point.y_m}`).join(' ');
}

export function renderAuthorityGeometry(documentRef, bundle) {
  const projection = authorityGeometry(bundle);
  const moduleLayer = documentRef.getElementById('authority-module-layer');
  const routeLayer = documentRef.getElementById('authority-route-layer');
  if (!moduleLayer || !routeLayer) throw new Error('authority geometry shell is incomplete');

  moduleLayer.replaceChildren();
  routeLayer.replaceChildren();

  for (const module of projection.modules) {
    const circle = documentRef.createElementNS(SVG_NS, 'circle');
    circle.setAttribute('class', 'authority-module-point');
    circle.setAttribute('data-module-id', String(module.moduleId));
    circle.setAttribute('cx', String(module.x_m));
    circle.setAttribute('cy', String(module.y_m));
    circle.setAttribute('r', '0.12');
    moduleLayer.appendChild(circle);
  }

  for (const route of projection.routes) {
    const polyline = documentRef.createElementNS(SVG_NS, 'polyline');
    polyline.setAttribute('class', `authority-route ${route.kind}`);
    polyline.setAttribute('data-route-id', String(route.routeId));
    polyline.setAttribute('data-string-id', String(route.stringId));
    polyline.setAttribute('data-route-kind', route.kind);
    polyline.setAttribute('points', pointsAttribute(route.vertices));
    routeLayer.appendChild(polyline);
  }

  setText(documentRef, 'authority-rendered-modules', projection.modules.length);
  setText(documentRef, 'authority-rendered-routes', projection.routes.length);
  return projection;
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
  renderAuthorityGeometry(documentRef, bundle);
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
