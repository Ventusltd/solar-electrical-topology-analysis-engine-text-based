import assert from 'node:assert/strict';
import { readFileSync } from 'node:fs';
import { fileURLToPath } from 'node:url';
import { dirname, resolve } from 'node:path';

import {
  AUTHORITY_BUNDLE_URL,
  authoritySummary,
  renderAuthorityBundle
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
    'authority-response-hash',
    'authority-block-hash',
    'authority-build025-hash'
  ];
  const elements = new Map(ids.map((id) => [id, { id, textContent: '', dataset: {} }]));
  return {
    elements,
    getElementById(id) {
      return elements.get(id) ?? null;
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

  assert.doesNotMatch(projectionSource, /Math\.|reduce\(|route\(|resistance|voltageDrop|powerLoss/i);
  assert.match(projectionSource, /boundary\.module_rated_power_wp/);
  assert.match(projectionSource, /response\.response_hash/);
}

switch (mode) {
  case 'mode':
    testModeSeparation();
    break;
  case 'bundle':
    testBundleProjection();
    break;
  default:
    throw new Error(`unknown studio-authority test mode: ${mode}`);
}

console.log(`studio authority ${mode}: PASS`);
