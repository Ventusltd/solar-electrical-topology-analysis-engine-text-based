import assert from 'node:assert/strict';
import { readFileSync } from 'node:fs';
import { fileURLToPath } from 'node:url';
import { dirname, resolve } from 'node:path';

const here = dirname(fileURLToPath(import.meta.url));
const shellPath = resolve(here, '../authority/index.html');
const html = readFileSync(shellPath, 'utf8');
const mode = process.argv[2];

function testModeSeparation() {
  assert.match(html, /INDICATIVE — NON-AUTHORITATIVE/);
  assert.match(html, /data-authority-state="non-authoritative"/);
  assert.match(html, /src="\.\.\/topology-studio\.html"/);
  assert.match(html, /data-mode="playground"/);
  assert.match(html, /data-mode="authority"/);
  assert.match(html, /data-authority-state="empty"/);
  assert.match(html, /PYTHON AUTHORITY — NO VERIFIED BUNDLE LOADED/);
  assert.match(html, /Authority mode is intentionally empty\./);
  assert.match(html, /no authoritative result or receipt is displayed/i);

  const script = html.match(/<script>([\s\S]*?)<\/script>/)?.[1] ?? '';
  assert.doesNotMatch(script, /Math\./);
  assert.doesNotMatch(script, /resistance|voltage drop|cable length|routing hash/i);
  assert.doesNotMatch(script, /response_hash|receipt_hash/);
  assert.match(script, /selectMode/);
}

switch (mode) {
  case 'mode':
    testModeSeparation();
    break;
  default:
    throw new Error(`unknown studio-authority test mode: ${mode}`);
}

console.log(`studio authority ${mode}: PASS`);
