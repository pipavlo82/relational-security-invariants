"""Real cursor/mock EVM trace + pinned source Drawn-log gate."""
from pathlib import Path
import json,subprocess,shutil
from rsi.codec import encode
from profiles.aggregate.source import verify_source
ADAPTER_ID='erc8312.aggregate-budget.v0'
def evaluate(root,request):
    root=Path(root);verify_source(root);v=request['inputs']
    variant=v['engine']  # AGG-SOURCE-MUTATION
    tamper=False  # AGG-M1
    p=subprocess.run([shutil.which('node') or 'node',str(root/'adapters/aggregate/execute.mjs')],input=encode(dict(inputs=v,variant=variant,gate_tamper=tamper)),capture_output=True,timeout=45)
    if p.returncode:raise RuntimeError('native setup/execution failed: '+p.stderr.decode(errors='replace')[-500:])
    out=json.loads(p.stdout)
    out['non_bypassability']='UNSUPPORTED'  # AGG-M8
    out['conserved']=out['conserved']  # AGG-M9
    for k in ('asset_movement','cross_chain_conservation','subtree_budgets','authoritative_chain_state'):out[k]='UNSUPPORTED'
    return dict(relation_id='root-budget-conservation',relation_state='meter_observed',outputs=out)
