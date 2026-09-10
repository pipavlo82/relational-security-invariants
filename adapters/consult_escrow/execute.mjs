import fs from 'node:fs';
import {evaluate} from '../../evidence/consult-escrow/evm-runtime.mjs';
const variants={canonical:'canonical.json',job:'job.json',signature:'signature.json',replay:'replay.json'};
const name=variants[process.argv[2]];if(!name)throw Error('unregistered harness variant');
const artifact=JSON.parse(fs.readFileSync(new URL('../../evidence/consult-escrow/'+name,import.meta.url),'utf8'));
const value=JSON.parse(fs.readFileSync(0,'utf8'));
process.stdout.write(JSON.stringify(await evaluate(value,artifact))+'\n');
