// Fixed harness for captured, digest-verified producer bytes. No fixture-selected code.
import { readFileSync } from 'node:fs';
import { createHash } from 'node:crypto';
import { encodeJsonUtf8LfV0, encodeJsonUtf8LfV0Transport } from './producer.ts';
const request = JSON.parse(readFileSync(0, 'utf8'));
const digest = b => createHash('sha256').update(b).digest('hex');
const vectors = JSON.parse(readFileSync(new URL('./vectors.json', import.meta.url), 'utf8')).vectors;
let qualified = 0;
for (const v of vectors) {
  let actual;
  try {
    const b = encodeJsonUtf8LfV0Transport(v.input);
    actual = {status: 'success', bytes_hex: b.toString('hex'), byte_length: b.length, sha256: digest(b)};
  } catch (e) { actual = {status: 'rejection', error: e.category}; }
  if (JSON.stringify(actual) !== JSON.stringify(v.expect)) {
    // Compare fields independent of JSON object insertion order.
    if (Object.keys(actual).length !== Object.keys(v.expect).length || Object.keys(actual).some(k => actual[k] !== v.expect[k]))
      throw new Error('producer qualification mismatch: ' + v.id + ' ' + JSON.stringify(actual));
  }
  qualified++;
}
const bytes = encodeJsonUtf8LfV0(request.artifact);
process.stdout.write(JSON.stringify({qualified, artifact_serialized_sha256: digest(bytes)}));
