const fs=require('node:fs'),path=require('node:path');
const modules=path.resolve('artifacts/ce-phase3b/runtime/node_modules');
const solc=require(path.join(modules,'solc')), {id}=require(path.join(modules,'ethers'));
const base=fs.readFileSync('evidence/consult-escrow/ConsultEscrow.sol','utf8');
const variants={canonical:base,job:base.replace('abi.encode(jobId, resultHash)',`abi.encode(bytes32(${id('jobA')}), resultHash)`),signature:base.replace('require(_recover(commitmentHash, signature) == j.attestor, "bad attestor sig");',''),replay:base.replace('require(j.status == Status.Open, "not open");','')};
for(const [name,source] of Object.entries(variants)) {
 const input={language:'Solidity',sources:{'ConsultEscrow.sol':{content:source},'IConsultEscrow.sol':{content:fs.readFileSync('evidence/consult-escrow/IConsultEscrow.sol','utf8')}},settings:{evmVersion:'cancun',optimizer:{enabled:false,runs:200},outputSelection:{'*':{'*':['abi','evm.bytecode.object']}}}};
 const output=JSON.parse(solc.compile(JSON.stringify(input)));if(output.errors?.some(x=>x.severity==='error'))throw Error(JSON.stringify(output.errors));
 const c=output.contracts['ConsultEscrow.sol'].ConsultEscrow;fs.writeFileSync(`evidence/consult-escrow/${name}.json`,JSON.stringify({compiler:solc.version(),settings:input.settings,abi:c.abi,bytecode:'0x'+c.evm.bytecode.object})+'\n');
}
