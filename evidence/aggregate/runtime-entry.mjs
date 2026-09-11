import {EVM} from '@ethereumjs/evm';
import {Common,Chain,Hardfork} from '@ethereumjs/common';
import {Address,Account,hexToBytes,bytesToHex} from '@ethereumjs/util';
import {Interface} from 'ethers';
export async function executeTrace(v,artifact){
 const evm=await EVM.create({common:new Common({chain:Chain.Mainnet,hardfork:Hardfork.Cancun})});
 const addr=s=>Address.fromString(s),gasLimit=10000000n;
 const senders=new Set([...v.roots.flatMap(r=>[r.issuer,r.agent]),...v.steps.map(s=>s.caller)]);
 for(const a of senders)await evm.stateManager.putAccount(addr(a),new Account(0n,10n**30n));
 const deployed=await evm.runCall({caller:addr(v.roots[0].issuer),data:hexToBytes(artifact.bytecode),gasLimit});
 if(deployed.execResult.exceptionError||!deployed.createdAddress)throw Error('deployment');
 const to=deployed.createdAddress,abi=new Interface(artifact.abi),roots=[],log=[],steps=[];
 const block=time=>({header:{number:1n,timestamp:BigInt(time),coinbase:Address.zero(),difficulty:0n,prevRandao:new Uint8Array(32),gasLimit:30000000n,baseFeePerGas:0n,cliqueSigner:()=>Address.zero(),getBlobGasPrice:()=>undefined}});
 async function call(name,args,caller,time){const r=await evm.runCall({caller:addr(caller),to,block:block(time),data:hexToBytes(abi.encodeFunctionData(name,args)),gasLimit});if(r.execResult.exceptionError){if(r.execResult.exceptionError.error!=='revert')throw Error('VM '+r.execResult.exceptionError.error);const e=abi.parseError(bytesToHex(r.execResult.returnValue));if(!e)throw Error('unmapped revert');return {status:'REVERT',error:e.name,logs:[]};}return {status:'RETURN',error:null,values:abi.decodeFunctionResult(name,bytesToHex(r.execResult.returnValue)),logs:r.execResult.logs??[]};}
 async function view(name,args){const r=await call(name,args,v.roots[0].issuer,v.observation_time);if(r.error)throw Error('view '+r.error);return r.values;}
 for(const root of v.roots){const r=await call(v.engine==='edge'?'grantRoot':'createRoot',v.engine==='edge'?[root.agent,root.cap]:[root.agent,root.cap,root.period_length,root.period_anchor,root.salt],root.issuer,v.observation_time);if(r.error)throw Error('root setup '+r.error);roots.push(r.values[0]);}
 for(const s of v.steps){const id=roots[s.root];let name,args;
  if(s.op==='delegate'){name=v.engine==='edge'?'subDelegate':'delegate';args=v.engine==='edge'?[s.node,s.agent,s.amount]:[id,s.node,s.agent,s.amount];}
  else if(s.op==='draw'){name='draw';args=v.engine==='edge'?[s.node,s.amount]:[id,s.node,s.amount];}
  else{name='revoke';args=[id,s.node];}
  const r=await call(name,args,s.caller,s.time);let emitted=0;
  for(const [,topics,data] of r.logs){const e=abi.parseLog({topics:topics.map(bytesToHex),data:bytesToHex(data)});if(e?.name==='Drawn'){if(e.args[0].toLowerCase()!==id.toLowerCase())throw Error('event root binding');const p=Number(e.args[2]);if(!Number.isSafeInteger(p))throw Error('period transport');log.push({root:s.root,period:p,edge:e.args[1].toString(),amount:e.args[3].toString(),admitted:true});emitted++;}}
  if(v.engine==='edge'&&s.op==='draw'&&!r.error)log.push({root:s.root,period:0,edge:String(s.node),amount:s.amount,admitted:true});
  const meters=[];for(let i=0;i<roots.length;i++)for(const period of v.periods)meters.push(v.engine==='edge'?'UNSUPPORTED':(await view('spentRoot',[roots[i],period]))[0].toString());
  steps.push({op:s.op,status:r.status,error:r.error,local_draw_valid:s.op==='draw'?(r.error===null||r.error==='RootBoundExceeded'):null,drawn_events:emitted,meters});
 }
 const meters=[];for(let i=0;i<roots.length;i++)for(const period of v.periods)meters.push({root:i,period,cap:v.engine==='edge'?v.roots[i].cap:(await view('rootOf',[roots[i]]))[1].toString(),spent_root:v.engine==='edge'?'UNSUPPORTED':(await view('spentRoot',[roots[i],period]))[0].toString()});
 return {steps,meters,log,realized:v.engine==='edge'?(await view('totalRealized',[]))[0].toString():null,log_origin:v.engine==='edge'?'SUCCESSFUL_SOURCE_CALLS':'SOURCE_DRAWN_EVENTS'};
}
