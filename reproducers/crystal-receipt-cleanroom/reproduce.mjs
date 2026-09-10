// Definition-derived flat string-map subset. See DERIVATION.md.
// This process receives only input bytes and the pinned definition file.
import { readFileSync } from 'node:fs';
import { createHash } from 'node:crypto';

const definitionSha256 = '9c17bd826c4a789464dab80c78a136153f3d9ce2f253198d0cf386bdef3a6d0b';

// Deliberately restricted transport: objects and printable ASCII strings only.
// Duplicate keys are rejected before constructing a map. No JSON.parse, shared
// codec, number coercion, descriptor inspection, or hidden default projection.
function parse(text) {
  let at = 0;
  function bad() { throw new Error(`unsupported or malformed transport at ${at}`); }
  function white() { while (at < text.length && ' \r\n\t'.includes(text[at])) at++; }
  function string() {
    if (text[at++] !== '"') bad();
    let value = '';
    while (at < text.length) {
      let c = text[at++];
      if (c === '"') return value;
      if (c === '\\') {
        c = text[at++];
        if (c === 'u') {
          const hex = text.slice(at, at + 4);
          if (!/^[0-9a-fA-F]{4}$/.test(hex)) bad();
          c = String.fromCharCode(Number.parseInt(hex, 16)); at += 4;
        } else if (!['"', '\\', '/'].includes(c)) bad();
      }
      if (c === undefined || c.charCodeAt(0) < 32 || c.charCodeAt(0) > 126) bad();
      value += c;
    }
    bad();
  }
  function value() {
    white();
    if (text[at] === '"') return string();
    if (text[at++] !== '{') bad();
    const map = Object.create(null);
    white();
    if (text[at] === '}') { at++; return map; }
    while (at < text.length) {
      white(); const key = string(); white();
      if (Object.hasOwn(map, key) || text[at++] !== ':') bad();
      map[key] = value(); white();
      const end = text[at++];
      if (end === '}') return map;
      if (end !== ',') bad();
    }
    bad();
  }
  const result = value(); white();
  if (at !== text.length) bad();
  return result;
}

function object(value) { return value !== null && typeof value === 'object'; }
function exactKeys(value, keys) {
  if (!object(value) || Object.keys(value).sort().join('\0') !== keys.slice().sort().join('\0')) {
    throw new Error('explicit bounded envelope required');
  }
}
function quote(value) {
  let token = '"';
  for (const c of value) token += (c === '"' || c === '\\' ? '\\' : '') + c;
  return token + '"';
}
function snapshot(endpoint) {
  exactKeys(endpoint, ['semantic_artifact', 'manifest']);
  const semantic = endpoint.semantic_artifact;
  if (!object(semantic) || !Object.keys(semantic).length || Object.hasOwn(semantic, 'audit_timestamp')) {
    throw new Error('nonempty semantic map without reserved audit metadata required');
  }
  if (!object(endpoint.manifest) || Object.keys(endpoint.manifest).some(k => k !== 'audit_timestamp') ||
      Object.values(endpoint.manifest).some(v => typeof v !== 'string')) {
    throw new Error('bounded external manifest required');
  }
  // Definition: retain each semantic key/value; order keys lexicographically.
  const tokens = [];
  for (const key of Object.keys(semantic).sort()) {
    if (typeof semantic[key] !== 'string') throw new Error('flat string map required');
    tokens.push(quote(key) + ':' + quote(semantic[key]));
  }
  return '{' + tokens.join(',') + '}';
}

try {
  const args = process.argv.slice(2);
  if (args.length !== 0 && (args.length !== 2 || args[0] !== '--definition')) {
    throw new Error('usage: node reproduce.mjs [--definition SPEC.md] < input.json');
  }
  const definition = args.length ? args[1] : new URL('../../evidence/crystal-receipt/SPEC.md', import.meta.url);
  const digest = createHash('sha256').update(readFileSync(definition)).digest('hex');
  if (digest !== definitionSha256) throw new Error('DEFINITION_PIN_DRIFT');
  const input = parse(readFileSync(0, 'utf8'));
  exactKeys(input, ['baseline', 'candidate']);
  const left = snapshot(input.baseline), right = snapshot(input.candidate);
  process.stdout.write(JSON.stringify({canonical_baseline: left, canonical_candidate: right,
    semantic_identity_preserved: left === right}) + '\n');
} catch (error) {
  process.stderr.write(String(error.message) + '\n');
  process.exitCode = 1;
}
