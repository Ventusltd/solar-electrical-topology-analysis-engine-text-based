import { AUTHORITY_BUNDLE_URL } from './authority-view.js';

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

export function authorityEvidence(bundle) {
  const response = requireObject(bundle, 'authority response');
  const block = requireObject(response.inverter_block, 'inverter_block');
  const build025 = requireObject(response.build025, 'build025');
  const inputAuthority = requireObject(block.input_authority, 'input_authority');
  const equipmentEvidence = requireObject(block.equipment_evidence, 'equipment_evidence');
  const inputAllocation = requireObject(build025.input_allocation, 'build025.input_allocation');
  const assignments = requireArray(inputAllocation.assignments, 'input_allocation.assignments');
  const mappingStates = requireArray(
    inputAuthority.mppt_mapping_verification_states,
    'mppt_mapping_verification_states'
  );
  const equipmentMpptState = requireValue(mappingStates[0], 'equipment MPPT state');

  const physicalInputs = assignments.map((value, index) => {
    const assignment = requireObject(value, `input_allocation.assignments[${index}]`);
    return Object.freeze({
      ordinal: index + 1,
      fixtureInputId: requireValue(assignment.input_id, `assignment[${index}].input_id`),
      stringId: requireValue(assignment.string_id, `assignment[${index}].string_id`),
      equipmentMpptId: null,
      equipmentMpptState
    });
  });

  const physicalInputCount = requireValue(
    inputAuthority.physical_dc_input_count,
    'physical_dc_input_count'
  );
  const allocatedInputCount = requireValue(
    inputAuthority.allocated_physical_input_count,
    'allocated_physical_input_count'
  );
  if (physicalInputs.length !== physicalInputCount || physicalInputs.length !== allocatedInputCount) {
    throw new Error('physical input allocation count does not match the authority response');
  }

  const missingEvidence = requireArray(
    equipmentEvidence.missing_evidence,
    'equipment_evidence.missing_evidence'
  );
  const missingEvidenceCount = requireValue(
    equipmentEvidence.missing_evidence_count,
    'equipment_evidence.missing_evidence_count'
  );
  if (missingEvidence.length !== missingEvidenceCount) {
    throw new Error('missing-evidence count does not match the authority response');
  }

  return Object.freeze({
    physicalInputCount,
    allocatedInputCount,
    physicalInputs: Object.freeze(physicalInputs),
    equipmentMpptCount: requireValue(inputAuthority.mppt_count, 'equipment MPPT count'),
    equipmentMpptState,
    internalDcTopology: requireValue(
      inputAuthority.internal_dc_topology,
      'internal DC topology'
    ),
    internalDcTopologyState: requireValue(
      inputAuthority.internal_dc_topology_verification_state,
      'internal DC topology state'
    ),
    reverseCurrentBlocking: requireValue(
      inputAuthority.reverse_current_blocking,
      'reverse-current blocking'
    ),
    reverseCurrentBlockingState: requireValue(
      inputAuthority.reverse_current_blocking_verification_state,
      'reverse-current blocking state'
    ),
    pceBackfeedCurrentA: requireValue(
      inputAuthority.pce_backfeed_current_a,
      'PCE backfeed current'
    ),
    pceBackfeedState: requireValue(
      inputAuthority.pce_backfeed_verification_state,
      'PCE backfeed state'
    ),
    fixtureMpptLabelsAreEquipmentEvidence: requireValue(
      inputAuthority.routing_fixture_mppt_labels_are_equipment_evidence,
      'routing fixture MPPT evidence flag'
    ),
    evidenceState: requireValue(equipmentEvidence.state, 'equipment evidence state'),
    missingEvidenceCount,
    missingEvidence: Object.freeze([...missingEvidence])
  });
}

function setText(documentRef, id, value) {
  const element = documentRef.getElementById(id);
  if (!element) throw new Error(`authority evidence element is missing: ${id}`);
  element.textContent = String(value);
}

function inputLines(projection) {
  return projection.physicalInputs
    .map((input) => [
      String(input.ordinal).padStart(2, '0'),
      input.fixtureInputId,
      input.stringId,
      'UNRESOLVED'
    ].join(' | '))
    .join('\n');
}

export function renderAuthorityEvidence(documentRef, bundle) {
  const projection = authorityEvidence(bundle);
  const values = {
    'authority-physical-input-count': projection.physicalInputCount,
    'authority-allocated-input-count': projection.allocatedInputCount,
    'authority-equipment-mppt-count': 'UNRESOLVED',
    'authority-equipment-mppt-state': projection.equipmentMpptState,
    'authority-internal-topology': projection.internalDcTopology,
    'authority-reverse-blocking': projection.reverseCurrentBlocking,
    'authority-pce-backfeed': 'UNRESOLVED',
    'authority-fixture-label-evidence': String(
      projection.fixtureMpptLabelsAreEquipmentEvidence
    ),
    'authority-input-lines': inputLines(projection),
    'authority-evidence-lines': projection.missingEvidence.join('\n')
  };
  for (const [id, value] of Object.entries(values)) setText(documentRef, id, value);
  return projection;
}

export async function loadAuthorityEvidence({
  fetchImpl = globalThis.fetch,
  documentRef = globalThis.document
} = {}) {
  if (typeof fetchImpl !== 'function') throw new TypeError('fetch implementation is required');
  if (!documentRef) throw new TypeError('document is required');

  const response = await fetchImpl(AUTHORITY_BUNDLE_URL, { cache: 'no-store' });
  if (!response.ok) throw new Error(`authority bundle request failed: ${response.status}`);
  const bundle = await response.json();
  renderAuthorityEvidence(documentRef, bundle);
  return bundle;
}

if (typeof window !== 'undefined' && typeof document !== 'undefined') {
  loadAuthorityEvidence().catch((error) => {
    const evidenceState = document.getElementById('authority-equipment-mppt-state');
    if (evidenceState) evidenceState.textContent = `LOAD FAILED: ${error.message}`;
  });
}
