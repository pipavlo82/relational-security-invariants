"""Source actual: BIP340 event verification and supplied-record joins, not occurrence."""
from pathlib import Path
import json,subprocess,sys
from rsi.codec import encode
from profiles.judgment.source import verify_source
ADAPTER_ID='erc8299.judgment-record-binding.v0'
def evaluate(root,request):
    root=Path(root);verify_source(root);v=request['inputs']['record']
    p=subprocess.run([sys.executable,'-B','-X','utf8',str(root/'adapters/judgment/execute.py')],input=encode(v),capture_output=True,timeout=30)
    if p.returncode:raise RuntimeError('SOURCE_EXECUTION: '+p.stderr.decode(errors='replace')[-300:])
    out=json.loads(p.stdout);c=out['source_checks']
    out['binding_established']=all(c[k]['pass'] is True for k in ('canonical_envelope','chain_invariant','admission_invariant'))  # J-M1
    out['verdict_decision']=json.loads(v['admission']['verdict_event']['content']).get('verdict')
    out['chain_bound']=c['chain_invariant']['pass']  # J-M2
    out['admission_bound']=c['admission_invariant']['pass']  # J-M3
    out['ordering_established_under_declared_anchor']=c['anchoring_precedence']['pass']  # J-M4
    out['execution_occurrence']='UNSUPPORTED'  # J-M5
    out['action_authorization']='UNSUPPORTED'  # J-M6
    out['anchor_authority']='UNSUPPORTED'  # J-M7
    out['binding_established']=out['binding_established']  # J-M8
    out['judgment_soundness']='UNSUPPORTED'
    out['raw_to_canonical_derivation']='UNSUPPORTED'
    return dict(relation_id='signed-verdict-terminal-record-binding',relation_state='records_observed',outputs=out)
