import assert from 'node:assert/strict';
import { readFileSync } from 'node:fs';
import { fileURLToPath } from 'node:url';
import { dirname, resolve } from 'node:path';

import {
  AUTHORITY_BUNDLE_URL,
  authorityGeometry,
  authoritySummary,
  renderAuthorityBundle,
  renderAuthorityGeometry
} from '../authority/authority-view.js';

const here = dirname(fileURLToPath(import.meta.url));
const shellPath = resolve(here, '../authority/index.html');
const modulePath = resolve(here, '../authority/authority-view.js');
const bundlePath = resolve(here, '../../authority-bundles/reference-inverter-block.json');
const html = readFileSync(shellPath, 'utf8');
const projectionSource = readFileSync(modulePath, 'utf8');
const bundle = JSON.parse(readFileSync(bundlePath, 'utf8'));
const mode = process.argv[2];

function testModeSeparation() {
  assert.match(html, /INDICATIVE — NON-AUTHORITATIVE/);
  assert.match(html, /data-authority-state="non-authoritative"/);
  assert.match(html, /src="\.\.\/topology-studio\.html"/);
  assert.match(html, /data-mode="playground"/);
  assert.match(html, /data-mode="authority"/);
  assert.match(html, /data-authority-state="loading"/);
  assert.match(html, /PYTHON AUTHORITY — LOADING VERIFIED BUNDLE/);
  assert.match(html, /type="module" src="\.\/authority-view\.js"/);

  const inlineScript = html.match(/<script>([\s\S]*?)<\/script>/)?.[1] ?? '';
  assert.doesNotMatch(inlineScript, /Math\./);
  assert.doesNotMatch(inlineScript, /resistance|voltage drop|cable length|routing hash/i);
  assert.doesNotMatch(inlineScript, /response_hash|receipt_hash/);
  assert.match(inlineScript, /selectMode/);
}

class FakeNode {
  constructor(id = '') {
    this.id = id;
    this.textContent = '';
    this.dataset = {};
    this.attributes = new Map();
    this.children = [];
  }

  setAttribute(name, value) {
    this.attributes.set(name, String(value));
  }

  appendChild(child) {
    this.children.push(child);
    return child;
  }

  replaceChildren(...children) {
    this.children = [...children];
  }
}

function fakeDocument() {
  const ids = [
    'authority-view',
    'authority-banner',
    'authority-strategy',
    'authority-module-power',
    'authority-modules-per-string',
    'authority-string-count',
    'authority-module-count',
    'authority-dc-power',
    'authority-inverter-power',
    'authority-dc-ac-ratio',
    'authority-evidence-state',
    'authority-missing-evidence',
    'authority-rendered-modules',
    'authority-rendered-routes',
    'authority-response-hash',
    'authority-block-hash',
    'authority-build025-hash',
    'authority-geometry',
    'authority-route-layer',
    'authority-module-layer'
  ];
  const elements = new Map(ids.map((id) => [id, new FakeNode(id)]));
  return {
    elements,
    getElementById(id) {
      return elements.get(id) ?? null;
    },
    createElementNS(_namespace, tagName) {
      const node = new FakeNode();
      node.tagName = tagName;
      return node;
    }
  };
}

function testBundleProjection() {
  assert.equal(AUTHORITY_BUNDLE_URL, '../../authority-bundles/reference-inverter-block.json');
  const summary = authoritySummary(bundle);
  const boundary = bundle.inverter_block.product_boundary;

  assert.equal(summary.modulePowerWp, boundary.module_rated_power_wp);
  assert.equal(summary.modulesPerString, boundary.modules_per_string);
  assert.equal(summary.stringCount, boundary.string_count);
  assert.equal(summary.moduleCount, boundary.module_count);
  assert.equal(summary.dcPowerKwp, boundary.dc_nameplate_power_kwp);
  assert.equal(summary.inverterPowerKva, boundary.inverter_apparent_power_kva);
  assert.equal(summary.dcAcRatio, boundary.dc_ac_nameplate_ratio);
  assert.equal(summary.responseHash, bundle.response_hash);
  assert.equal(summary.blockReceiptHash, bundle.inverter_block.receipt_hash);
  assert.equal(summary.build025ReceiptHash, bundle.build025.receipt_hash);

  const documentRef = fakeDocument();
  const rendered = renderAuthorityBundle(documentRef, bundle);
  assert.deepEqual(rendered, summary);
  assert.equal(documentRef.elements.get('authority-view').dataset.authorityState, 'verified-bundle');
  assert.equal(
    documentRef.elements.get('authority-banner').textContent,
    'PYTHON AUTHORITY — VERIFIED COMMITTED BUNDLE'
  );
  assert.equal(documentRef.elements.get('authority-module-power').textContent, '660 Wp');
  assert.equal(documentRef.elements.get('authority-modules-per-string').textContent, '30');
  assert.equal(documentRef.elements.get('authority-string-count').textContent, '24');
  assert.equal(documentRef.elements.get('authority-module-count').textContent, '720');
  assert.equal(documentRef.elements.get('authority-dc-power').textContent, '475.2 kWp');
  assert.equal(documentRef.elements.get('authority-inverter-power').textContent, '352 kVA');
  assert.equal(documentRef.elements.get('authority-dc-ac-ratio').textContent, '1.35');
  assert.equal(documentRef.elements.get('authority-response-hash').textContent, bundle.response_hash);

  assert.doesNotMatch(projectionSource, /Math\.|reduce\(|resistance|voltageDrop|powerLoss/i);
  assert.match(projectionSource, /boundary\.module_rated_power_wp/);
  assert.match(projectionSource, /response\.response_hash/);
}

function expectedRouteCount() {
  let count = 0;
  for (const stringRoute of bundle.build025.routing.strings) {
    count += 2;
    count += stringRoute.interconnect_routes.length;
  }
  return count;
}

function testGeometryProjection() {
  const projection = authorityGeometry(bundle);
  const placements = bundle.build025.geometry.placements;
  const strings = bundle.build025.routing.strings;

  assert.equal(projection.modules.length, placements.length);
  assert.equal(projection.modules.length, 720);
  assert.equal(projection.routes.length, expectedRouteCount());
  assert.equal(projection.routes.length, 744);
  assert.deepEqual(projection.bounds_m, bundle.build025.geometry.bounds_m);
  assert.deepEqual(projection.modules[0], {
    moduleId: placements[0].module_id,
    x_m: placements[0].centre_m[0],
    y_m: placements[0].centre_m[1]
  });
  assert.deepEqual(projection.routes[0].vertices, strings[0].positive_route.vertices);
  assert.deepEqual(projection.routes[1].vertices, strings[0].negative_route.vertices);
  assert.deepEqual(
    projection.routes[2].vertices,
    strings[0].interconnect_routes[0].vertices
  );

  const documentRef = fakeDocument();
  const rendered = renderAuthorityGeometry(documentRef, bundle);
  const moduleNodes = documentRef.elements.get('authority-module-layer').children;
  const routeNodes = documentRef.elements.get('authority-route-layer').children;

  assert.equal(rendered, projection);
  assert.equal(moduleNodes.length, placements.length);
  assert.equal(routeNodes.length, expectedRouteCount());
  assert.equal(moduleNodes[0].tagName, 'circle');
  assert.equal(moduleNodes[0].attributes.get('cx'), String(placements[0].centre_m[0]));
  assert.equal(moduleNodes[0].attributes.get('cy'), String(placements[0].centre_m[1]));
  assert.equal(routeNodes[0].tagName, 'polyline');
  assert.equal(
    routeNodes[0].attributes.get('points'),
    strings[0].positive_route.vertices
      .map((point) => `${point.x_m},${point.y_m}`)
      .join(' ')
  );
  assert.equal(documentRef.elements.get('authority-rendered-modules').textContent, '720');
  assert.equal(documentRef.elements.get('authority-rendered-routes').textContent, '744');

  assert.match(html, /id="authority-geometry"/);
  assert.match(html, /id="authority-route-layer"/);
  assert.match(html, /id="authority-module-layer"/);
  assert.doesNotMatch(
    projectionSource,
    /Math\.|hypot|sqrt|geometric_length_m|route_length|cable_length|resistance|voltageDrop|powerLoss/i
  );
  assert.match(projectionSource, /placement\.centre_m/);
  assert.match(projectionSource, /route\.vertices/);
}

switch (mode) {
  case 'mode':
    testModeSeparation();
    break;
  case 'bundle':
    testBundleProjection();
    break;
  case 'geometry':
    testGeometryProjection();
    break;
  default:
    throw new Error(`unknown studio-authority test mode: ${mode}`);
}

console.log(`studio authority ${mode}: PASS`);
