import {EVM} from '@ethereumjs/evm';
import {Common,Chain,Hardfork} from '@ethereumjs/common';
import {Address,Account,hexToBytes,bytesToHex} from '@ethereumjs/util';
import {Interface} from 'ethers';
export async function evaluate(v,artifact){
 const evm=await EVM.create({common:new Common({chain:Chain.Mainnet,hardfork:Hardfork.Cancun})});
 const addr=s=>Address.fromString(s);const consumer=addr(v.consumer),provider=addr(v.provider),relayer=addr(v.relayer);
 for(const a of [consumer,provider,relayer])await evm.stateManager.putAccount(a,new Account(0n,10n**30n));
 const gasLimit=10000000n;
 const created=await evm.runCall({caller:consumer,data:hexToBytes(artifact.bytecode),gasLimit});
 if(created.execResult.exceptionError||!created.createdAddress)throw Error('deployment');
 const to=created.createdAddress,abi=new Interface(artifact.abi);
 const call=async(name,args,caller=relayer,value=0n)=>evm.runCall({caller,to,value,data:hexToBytes(abi.encodeFunctionData(name,args)),gasLimit});
 for(const job of v.open_jobs){const r=await call('open',[job,v.provider,v.attestor,v.deadline],consumer,BigInt(v.amount));if(r.execResult.exceptionError)throw Error('open setup');}
 const release=()=>call('release',[v.job_id,v.result_hash,v.signature]);
 if(v.prior==='release'){const r=await release();if(r.execResult.exceptionError)throw Error('prior release setup');}
 const before=(await evm.stateManager.getAccount(provider)).balance;
 if(v.mode==='simulate')await evm.stateManager.checkpoint();
 const r=await release();let error=null;
 if(r.execResult.exceptionError){try{error=abi.parseError(bytesToHex(r.execResult.returnValue)).args[0];}catch{throw Error('unexpected EVM failure');}}
 const logs=r.execResult.logs??[];let event=null;
 for(const [,topics,data] of logs){const e=abi.parseLog({topics:topics.map(bytesToHex),data:bytesToHex(data)});if(e?.name==='Released')event={job_id:e.args[0].toLowerCase(),result_hash:e.args[1].toLowerCase(),commitment_hash:e.args[2].toLowerCase(),provider:e.args[3].toLowerCase(),amount:e.args[4].toString()};}
 if(v.mode==='simulate'){await evm.stateManager.revert();event=null;}
 const state=await call('jobs',[v.job_id]);if(state.execResult.exceptionError)throw Error('state read');
 const status=Number(abi.decodeFunctionResult('jobs',bytesToHex(state.execResult.returnValue))[5]);
 const delta=(await evm.stateManager.getAccount(provider)).balance-before;
 return {release_eligible:error===null,error,escrow_status:['None','Open','Released','Refunded'][status],provider_delta:delta.toString(),released_event:event,execution_occurrence:v.mode==='execute'&&error===null?'LOCAL_EVM':'UNSUPPORTED'};
}
