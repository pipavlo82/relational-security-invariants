import {EVM} from '@ethereumjs/evm';
import {Common,Chain,Hardfork} from '@ethereumjs/common';
import {Address,Account,hexToBytes,bytesToHex} from '@ethereumjs/util';
import {Interface} from 'ethers';
export async function run(verdict,key,proof,artifact,gen){
 const evm=await EVM.create({common:new Common({chain:Chain.Mainnet,hardfork:Hardfork.Cancun})});
 const caller=Address.fromString('0x0000000000000000000000000000000000000001');
 await evm.stateManager.putAccount(caller,new Account(0n,10n**30n));
 const gasLimit=10000000n;
 async function deploy(c,args=[]){const abi=new Interface(c.abi);const r=await evm.runCall({caller,data:hexToBytes(c.bytecode+abi.encodeDeploy(args).slice(2)),gasLimit});if(r.execResult.exceptionError||!r.createdAddress)throw Error('deployment failed');return r.createdAddress;}
 const contracts=artifact.contracts;
 let honk=gen==='fixed'?await deploy(contracts.HonkVerifier):null;
 const probe=await deploy(contracts.ProjectionProbe,gen==='fixed'?[honk.toString(),artifact.vk_hash]:[]);
 const api=new Interface(contracts.ProjectionProbe.abi);
 const call=async(to,abi,name,args)=>evm.runCall({caller,to,data:hexToBytes(abi.encodeFunctionData(name,args)),gasLimit});
 if(gen==='sdk'){const r=await call(probe,api,'honk',[]);if(r.execResult.exceptionError)throw Error('honk getter');honk=Address.fromString(api.decodeFunctionResult('honk',bytesToHex(r.execResult.returnValue))[0]);}
 const projected=await call(probe,api,'project',[verdict]);if(projected.execResult.exceptionError)throw Error('projection failed');
 const pi=Array.from(api.decodeFunctionResult('project',bytesToHex(projected.execResult.returnValue))[0]);
 const hk=new Interface(contracts.HonkVerifier.abi);
 const crypt=await call(honk,hk,'verify',[proof,pi]);
 // abi.encode(Verdict) is the parameter encoding of project(Verdict), without the selector.
 const envelope='0x'+api.encodeFunctionData('project',[verdict]).slice(10);
 const gate=await call(probe,api,'verifyProof',[key,envelope,proof]);
 function observed(r,abi,name){if(r.execResult.exceptionError){if(r.execResult.exceptionError.error!=='revert')throw Error('non-verifier EVM failure: '+r.execResult.exceptionError.error);return {valid:false,status:'REVERT',data:bytesToHex(r.execResult.returnValue)};}return {valid:Boolean(abi.decodeFunctionResult(name,bytesToHex(r.execResult.returnValue))[0]),status:'RETURN',data:bytesToHex(r.execResult.returnValue)};}
 return {public_inputs:pi,cryptographic:observed(crypt,hk,'verify'),adapter:observed(gate,api,'verifyProof')};
}
