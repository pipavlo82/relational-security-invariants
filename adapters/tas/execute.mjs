import {readFileSync} from 'node:fs';
import {createWorkflowSourceGate,createWorkflowOperationService,createWorkflowContractAddressResolver} from '../../evidence/tas/source-runtime.mjs';
const v=JSON.parse(readFileSync(0,'utf8'));
const gate=createWorkflowSourceGate({resolveCurrent:async()=>v.current});
if(v.accepted!==null)gate.accept(v.accepted);
let dispatched=null, error=null;
const manifest=JSON.parse(readFileSync(new URL('../../evidence/tas/agent-sdk.v1.json',import.meta.url),'utf8'));
const tool=manifest.tools.find(t=>t.name==='workflow.execution.erc8301.agent_workflow.get_task');
const service=createWorkflowOperationService({agentId:v.agent_id,gate,registry:{get:name=>name===tool.name?tool:undefined},contractAddressResolver:createWorkflowContractAddressResolver(),memberResolver:{getAgent:async()=>({data:{agent_id:v.member.agent_id,is_member:v.member.is_member,authentication_wallet:v.member.wallet},resolution:{chain:{block_hash:v.member.block_hash}}})},client:{accountFromAddress:address=>({address}),accountFromPrivateKey:()=>{throw Error('outside read lane')},invoke:async(entry,args,context)=>{dispatched={target:entry.binding.target,arguments:args,chainId:context.chainId,rpcUrl:context.rpcUrl,contractAddress:context.contractAddress,wallet:context.account.address};throw Error('controlled SDK port: execution not performed');}}});
try{await service.invoke({toolName:v.tool_name,arguments:{taskHash:v.task_hash}});}catch(e){if(typeof e.code!=='string')throw e;error=e.code;}
process.stdout.write(JSON.stringify({error,dispatched}));
