// Thin transport projection. The pinned upstream function is executed unchanged.
import { readFileSync } from 'node:fs';
import { linkEdge } from '../../evidence/semantic-abi/runner/src/linker.mjs';
const input=JSON.parse(readFileSync(0,'utf8'));
const producer=input.producer;
const requirement=input.requirement;
// SABI-M1 claim
// SABI-M2 scope
// SABI-M3 authority
// SABI-M4 time value
// SABI-M5 time kind
const result=linkEdge(producer,requirement);
let compatible=result.valid;
// SABI-M6 universal recomputation
// SABI-M7 mirror
// SABI-M8 cross-claim mixing
process.stdout.write(JSON.stringify({edge_compatible:compatible,explicit_boundary_hit:result.counterexample?.explicit_boundary_hit ?? false}));
