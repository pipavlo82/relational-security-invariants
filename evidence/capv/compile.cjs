// Compile exact pinned sources and explicit test-only mutants. No source rewriting on disk.
const fs=require('node:fs'),path=require('node:path');
const modules=path.resolve('artifacts/capv-phase3e/runtime/node_modules');
const solc=require(path.join(modules,'solc'));
for(const variant of ['sdk','fixed','fixed-drop','sdk-key']){
 const gen=variant.startsWith('sdk')?'sdk':'fixed';
 const dir='evidence/capv/'+gen+(gen==='fixed'?'/src':'');
 const sources={};
 for(const n of ['HonkVerifierAdapter.sol','IVerifier.sol','IConfidentialPolicyVerdict.sol'])sources[n]={content:fs.readFileSync(dir+'/'+n,'utf8')};
 sources['HonkVerifier.sol']={content:fs.readFileSync(dir+(gen==='fixed'?'/verifier':'')+'/HonkVerifier.sol','utf8')};
 sources['@openzeppelin/contracts/utils/introspection/IERC165.sol']={content:fs.readFileSync('evidence/capv/IERC165.sol','utf8')};
 const a=sources['HonkVerifierAdapter.sol'];
 if(variant==='fixed-drop')a.content=a.content.replace('new bytes32[](40)','new bytes32[](39)').replace('pi[39] = bytes32(uint256(v.expiry));','');
 if(variant==='sdk-key')a.content=a.content.replace('if (programKey != expectedProgramKey) return false;','');
 const ctor=gen==='sdk'?'constructor() HonkVerifierAdapter() {}':'constructor(IHonkVerifier h, bytes32 k) HonkVerifierAdapter(h,k) {}';
 sources['ProjectionProbe.sol']={content:`pragma solidity ^0.8.27; import {HonkVerifierAdapter,IHonkVerifier} from "./HonkVerifierAdapter.sol"; import {Verdict} from "./IConfidentialPolicyVerdict.sol"; contract ProjectionProbe is HonkVerifierAdapter { ${ctor} function project(Verdict memory v) external pure returns(bytes32[] memory) { return _toPublicInputs(v); } }`};
 const settings={evmVersion:'cancun',optimizer:{enabled:true,runs:200},outputSelection:{'*':{'*':['abi','evm.bytecode.object']}}};
 const result=JSON.parse(solc.compile(JSON.stringify({language:'Solidity',sources,settings})));
 if(result.errors?.some(x=>x.severity==='error'))throw Error(JSON.stringify(result.errors));
 const contracts={};for(const [file,name] of [['HonkVerifier.sol','HonkVerifier'],['ProjectionProbe.sol','ProjectionProbe']]){const c=result.contracts[file][name];contracts[name]={abi:c.abi,bytecode:'0x'+c.evm.bytecode.object};}
 const vk_hash=sources['HonkVerifier.sol'].content.match(/VK_HASH = (0x[0-9a-f]+);/)[1];
 fs.writeFileSync('evidence/capv/'+variant+'.json',JSON.stringify({compiler:solc.version(),settings,vk_hash,contracts})+'\n');
 console.log(variant,'compiled');
}
