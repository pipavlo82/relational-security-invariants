"""Observed EVM verifier results plus explicitly bounded source annotations."""
from pathlib import Path
import json,subprocess,shutil,re
from rsi.codec import encode
from profiles.capv.source import verify_source,SDK,OLD,FIXED
ADAPTER_ID='capv.expiry-generation.v0'
def evaluate(root,request):
    root=Path(root);verify_source(root);v=request['inputs']
    generation=v['program_generation']  # CAPV-M3
    if v['consumer_pin']==SDK:
        consumer_generation='sdk'  # CAPV-M4
    else:consumer_generation=generation
    variant=generation  # CAPV-M2
    key=v['program_key']  # CAPV-M5
    d=v['verdict'];order=('agentId','domainId','policyRoot','actionCommitment','executor','expiry','nullifier','decision','policyKind')
    payload={'variant':variant,'proof_generation':v['proof_generation'],'program_key':key,'verdict':[d[k] for k in order]}
    p=subprocess.run([shutil.which('node') or 'node',str(root/'adapters/capv/execute.mjs')],input=encode(payload),capture_output=True,timeout=45)
    if p.returncode:raise RuntimeError('EVM setup/execution failed: '+p.stderr.decode(errors='replace')[-500:])
    raw=json.loads(p.stdout)
    artifact=json.loads((root/('evidence/capv/'+generation+'.json')).read_bytes())
    pi=raw['public_inputs'];expiry_public=len(pi)==40 and int(pi[39],16)==int(d['expiry'])
    crypt=raw['cryptographic']['valid'];adapter=raw['adapter']['valid']
    fresh=int(v['observation_time'])<int(d['expiry'])
    bound=expiry_public and crypt  # CAPV-M1
    crypt=crypt  # CAPV-M6
    normative=(root/'evidence/capv/canonical/erc-8354.md').read_text(encoding='utf-8')
    asset=(root/'evidence/capv/canonical/main.nr').read_text(encoding='utf-8').split('// ---- private witness ----')[0]
    required='Every field of `Verdict` MUST be a public input' in normative
    asset_expiry=re.search(r'expiry\s*:\s*pub',asset) is not None
    outputs=dict(program_generation={'sdk':OLD,'fixed':FIXED}[generation],vk_hash=artifact['vk_hash'],public_input_count=len(pi),expiry_public=expiry_public,proof_verifies=crypt,adapter_verifies=adapter,program_key_matches_vk=key==artifact['vk_hash'],proof_program_matches=generation==v['proof_generation'],consumer_generation_matches=generation==consumer_generation,expiry_fresh=fresh,expiry_bound_to_this_proof=bound,normative_expiry_public=required,canonical_asset_expiry_public=asset_expiry,canonical_asset_alignment='MISMATCH' if required!=asset_expiry else 'ALIGNED',guard_acceptance='UNSUPPORTED',domain_root_acceptability='UNSUPPORTED',executor_authorization='UNSUPPORTED',execution_occurrence='UNSUPPORTED')
    outputs['verifier_result']='REVERT' if raw['cryptographic']['status']=='REVERT' else ('TRUE' if raw['cryptographic']['valid'] else 'FALSE')
    outputs['adapter_result']='REVERT' if raw['adapter']['status']=='REVERT' else ('TRUE' if raw['adapter']['valid'] else 'FALSE')
    return {'relation_id':'proof-public-input-generation-binding','relation_state':'generation_observed','outputs':outputs}
