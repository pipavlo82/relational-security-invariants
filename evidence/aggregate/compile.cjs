// Exact reference source, plus explicit mutation-only builds.
const fs=require('node:fs'),path=require('node:path');
const modules=path.resolve('artifacts/aggregate-phase3f/runtime/node_modules');
const solc=require(path.join(modules,'solc')),esbuild=require(path.join(modules,'esbuild'));
const base='evidence/aggregate/reference/';
const raw=fs.readFileSync(base+'src/AggregateBudgetCursor.sol','utf8');
const changes={root:['if (rs + amount > root.cap) revert RootBoundExceeded();',''],refund:['node.revoked = true;','node.revoked = true; spentRoot[rootId][_periodIndex(root)] = 0;'],period:['return uint64((block.timestamp - root.periodAnchor) / root.periodLength);','return 0;'],delegate:['if (parent.nodeCap != 0) revert CappedNodeCannotDelegate();',''],revoked:['if (node.revoked) revert PathRevoked();',''],nodecap:['if (ns + amount > node.nodeCap) revert NodeBoundExceeded();','']};
const settings={evmVersion:'cancun',optimizer:{enabled:true,runs:200},outputSelection:{'*':{'*':['abi','evm.bytecode.object']}}};
function compile(sources,file,name){const r=JSON.parse(solc.compile(JSON.stringify({language:'Solidity',sources,settings})));if(r.errors?.some(e=>e.severity==='error'))throw Error(JSON.stringify(r.errors));const c=r.contracts[file][name];return {compiler:solc.version(),settings,abi:c.abi,bytecode:'0x'+c.evm.bytecode.object};}
for(const variant of ['cursor',...Object.keys(changes)]){
 let content=raw;if(variant!=='cursor'){const [a,b]=changes[variant];if(content.split(a).length!==2)throw Error('mutation anchor');content=content.replace(a,b);}
 const sources={'AggregateBudgetCursor.sol':{content}};for(const n of ['IAggregateBudget.sol','IERC165.sol'])sources[n]={content:fs.readFileSync(base+'src/'+n,'utf8')};
 fs.writeFileSync('evidence/aggregate/'+variant+'.json',JSON.stringify(compile(sources,'AggregateBudgetCursor.sol','AggregateBudgetCursor'))+'\n');
}
// Extract the exact standalone counterexample contract; omit only the Forge test imports/class.
const test=fs.readFileSync(base+'test/AggregateBudgetCursor.t.sol','utf8');
const edge='// SPDX-License-Identifier: CC0-1.0\npragma solidity ^0.8.24;\n'+test.slice(test.indexOf('contract PerEdgeBudgetMock {'),test.indexOf('contract AggregateBudgetCursorTest'));
fs.writeFileSync('evidence/aggregate/edge.json',JSON.stringify(compile({'PerEdgeBudgetMock.sol':{content:edge}},'PerEdgeBudgetMock.sol','PerEdgeBudgetMock'))+'\n');
// Export bridge only; the original Bun CLI/self-check branch is not executed under Node.
const gate=fs.readFileSync('evidence/aggregate/recompute-kit/gate.ts','utf8')+'\nexport {valueFor};\n';
fs.writeFileSync('evidence/aggregate/gate.mjs',esbuild.transformSync(gate,{loader:'ts',format:'esm',target:'node22',legalComments:'inline'}).code);
console.log('8 Solidity artifacts and source gate built');
