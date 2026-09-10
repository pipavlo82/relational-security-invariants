import fs from 'node:fs';
import {observe} from '../../evidence/verify-layer/proof-runtime.mjs';
const v=JSON.parse(fs.readFileSync(0,'utf8'));
const r=await observe(v,process.argv[2]);
function canonical(x){if(Array.isArray(x))return x.map(canonical);if(x && typeof x==='object')return Object.fromEntries(Object.keys(x).sort().map(k=>[k,canonical(x[k])]));return x;}
process.stdout.write(JSON.stringify(canonical(r))+'\n');
