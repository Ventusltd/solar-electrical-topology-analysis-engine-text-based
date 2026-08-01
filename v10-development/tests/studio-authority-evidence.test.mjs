import assert from 'node:assert/strict';
import { readFileSync } from 'node:fs';
import { fileURLToPath } from 'node:url';
import { dirname, resolve } from 'node:path';

import {
  authorityEvidence,
  renderAuthorityEvidence
} from '../authority/authority-evidence.js';

const here = dirname(fileURLToPath(import.meta.url));
const shellPath = resolve(here, '../authority/index.html');
const modulePath = resolve(here, '../authority/authority-evidence.js');
const bundlePath = resolve(here, '../../authority-bundles/reference-inverter-block.json');
const html = readFileSync(shellPath, 'utf8');
const source = readFileSync(modulePath, 'utf8');
const bundle = JSON.parse(readFileSync(bundlePath, 'utf8'));

function fakeDocument() {
  const ids = [
    'authority-physical-input-count',
    'authority-allocated-input-count',
    'authority-equipment-mppt-count',
    'authority-equipment-mppt-state',
    'authority-internal-topology',
    'authority-reverse-blocking',
    'authority-pce-backfeed',
    'authority-fixture-label-evidence',
    'authority-input-lines',
    'authority-evidence-lines'
  ];
  const elements = new Map(ids.map((id) => [id, { id, textContent: '' }]));
  return {
    elements,
    getElementById(id) {
      return elements.get(id) ?? null;
    }
  };
}

function testEvidenceProjection() {
  const projection = authorityEvidence(bundle);
  const authority = bundle.inverter_block.input_authority;
  const evidence = bundle.inverter_block.equipment_evidence;
  const assignments = bundle.build025.input_allocation.assignments;

  assert.equal(projection.physicalInputCount, 24);
  assert.equal(projection.allocatedInputCount, 24);
  assert.equal(projection.physicalInputs.length, 24);
  assert.equal(projection.equipmentMpptCount, null);
  assert.equal(projection.equipmentMpptState, 'unknown');
  assert.equal(projection.internalDcTopology, 'unknown');
  assert.equal(projection.internalDcTopologyState, 'unknown');
  assert.equal(projection.reverseCurrentBlocking, 'unknown');
  assert.equal(projection.reverseCurrentBlockingState, 'unknown');
  assert.equal(projection.pceBackfeedCurrentA, null);
  assert.equal(projection.pceBackfeedState, 'unknown');
  assert.equal(projection.fixtureMpptLabelsAreEquipmentEvidence, false);
  assert.equal(projection.evidenceState, 'incomplete_evidence');
  assert.equal(projection.missingEvidenceCount, 47);
  assert.deepEqual(projection.missingEvidence, evidence.missing_evidence);

  assert.deepEqual(projection.physicalInputs[0], {
    ordinal: 1,
    fixtureInputId: assignments[0].input_id,
    stringId: assignments[0].string_id,
    equipmentMpptId: null,
    equipmentMpptState: 'unknown'
  });
  assert.deepEqual(projection.physicalInputs[23], {
    ordinal: 24,
    fixtureInputId: assignments[23].input_id,
    stringId: assignments[23].string_id,
    equipmentMpptId: null,
    equipmentMpptState: 'unknown'
  });
  assert.ok(projection.physicalInputs.every((item) => item.equipmentMpptId === null));
  assert.ok(projection.physicalInputs.every((item) => item.equipmentMpptState === 'unknown'));
  assert.equal(authority.routing_fixture_mppt_labels_are_equipment_evidence, false);

  const documentRef = fakeDocument();
  const rendered = renderAuthorityEvidence(documentRef, bundle);
  assert.deepEqual(rendered, projection);
  assert.equal(documentRef.elements.get('authority-physical-input-count').textContent, '24');
  assert.equal(documentRef.elements.get('authority-allocated-input-count').textContent, '24');
  assert.equal(documentRef.elements.get('authority-equipment-mppt-count').textContent, 'UNRESOLVED');
  assert.equal(documentRef.elements.get('authority-equipment-mppt-state').textContent, 'unknown');
  assert.equal(documentRef.elements.get('authority-internal-topology').textContent, 'unknown');
  assert.equal(documentRef.elements.get('authority-reverse-blocking').textContent, 'unknown');
  assert.equal(documentRef.elements.get('authority-pce-backfeed').textContent, 'UNRESOLVED');
  assert.equal(documentRef.elements.get('authority-fixture-label-evidence').textContent, 'false');

  const inputLines = documentRef.elements.get('authority-input-lines').textContent.split('\n');
  assert.equal(inputLines.length, 24);
  assert.match(inputLines[0], /^01 \| .* \| .* \| UNRESOLVED$/);
  assert.match(inputLines[23], /^24 \| .* \| .* \| UNRESOLVED$/);
  assert.equal(
    documentRef.elements.get('authority-evidence-lines').textContent,
    evidence.missing_evidence.join('\n')
  );

  assert.match(html, /Routing-fixture labels are not equipment evidence\./);
  assert.match(html, /id="authority-input-lines"/);
  assert.match(html, /id="authority-evidence-lines"/);
  assert.match(html, /src="\.\/authority-evidence\.js"/);

  assert.doesNotMatch(source, /assignment\.mppt_id/);
  assert.doesNotMatch(source, /physicalInput\.mppt_id/);
  assert.doesNotMatch(source, /equipment_profile\.mppt_ids/);
  assert.doesNotMatch(source, /parallel_node_id|dc_bus_node_id/);
  assert.doesNotMatch(source, /Math\.|reduce\(|resistance|voltageDrop|powerLoss/i);
  assert.match(source, /assignment\.input_id/);
  assert.match(source, /assignment\.string_id/);
  assert.match(source, /equipmentMpptId: null/);
}

testEvidenceProjection();
console.log('studio authority evidence: PASS');
