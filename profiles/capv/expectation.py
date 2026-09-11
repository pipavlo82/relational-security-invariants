"""Separately implemented predictor: Noir signature + fixture PI obligations, not a Honk implementation."""
from pathlib import Path
import re
from rsi.codec import load
from profiles.capv.source import verify_source,SDK,OLD,FIXED
from runner.expectation_registry import ExpectationProfile,FixtureSource
from runner.relation_runtime import validate_envelope,plan
EXPECTATION_ID='capv.expiry-generation.v0'
def derive(root,v):
    root=Path(root);g=v['program_generation'];pg=v['proof_generation'];d=v['verdict']
    circuit=root/('evidence/capv/'+('old' if g=='sdk' else 'fixed')+'/noir/src/main.nr')
    signature=circuit.read_text(encoding='utf-8').split('fn main(',1)[1].split(') {',1)[0]
    names=re.findall(r'(\w+)\s*:\s*pub\s+',signature)
    expiry='expiry' in names
    proof_dir=root/('evidence/capv/sdk/fixtures' if pg=='sdk' else 'evidence/capv/fixed/test/fixtures')
    raw=(proof_dir/'allowlist.public_inputs').read_bytes()
    known=[int.from_bytes(raw[i:i+32],'big') for i in range(0,len(raw),32)]
    supplied=[int(d['agentId']),int(d['domainId'],16),int(d['policyRoot'],16),*bytes.fromhex(d['actionCommitment'][2:]),int(d['nullifier'],16),int(d['decision']),int(d['policyKind']),int(d['executor'],16)]
    if expiry:supplied.append(int(d['expiry']))
    # This predicts this pinned fixture pair's relation; it does not independently verify arbitrary proofs.
    valid=(pg==g and supplied==known)
    verifier=root/('evidence/capv/sdk/HonkVerifier.sol' if g=='sdk' else 'evidence/capv/fixed/src/verifier/HonkVerifier.sol')
    vk=re.search(r'VK_HASH\s*=\s*(0x[0-9a-f]+)',verifier.read_text(encoding='utf-8')).group(1)
    key_ok=v['program_key']==vk
    # Definition-derived normative obligation and canonical-asset signature, separately read.
    text=(root/'evidence/capv/canonical/erc-8354.md').read_text(encoding='utf-8')
    obligation='Every field of `Verdict` MUST be a public input of the proving program.' in text
    canon=(root/'evidence/capv/canonical/main.nr').read_text(encoding='utf-8').split('fn main(',1)[1].split(') {',1)[0]
    canonical_expiry='expiry' in re.findall(r'(\w+)\s*:\s*pub\s+',canon)
    out=dict(program_generation=OLD if g=='sdk' else FIXED,vk_hash=vk,public_input_count=len(supplied),expiry_public=expiry,proof_verifies=valid,adapter_verifies=valid and key_ok,program_key_matches_vk=key_ok,proof_program_matches=pg==g,consumer_generation_matches=v['consumer_pin']=='direct' or g=='sdk',expiry_fresh=int(d['expiry'])>int(v['observation_time']),expiry_bound_to_this_proof=expiry and valid,normative_expiry_public=obligation,canonical_asset_expiry_public=canonical_expiry,canonical_asset_alignment='MISMATCH' if obligation!=canonical_expiry else 'ALIGNED',guard_acceptance='UNSUPPORTED',domain_root_acceptability='UNSUPPORTED',executor_authorization='UNSUPPORTED',execution_occurrence='UNSUPPORTED')
    out['verifier_result']='TRUE' if valid else 'REVERT'
    out['adapter_result']='FALSE' if not key_ok else ('TRUE' if valid else 'REVERT')
    return {'relation_id':'proof-public-input-generation-binding','relation_state':'generation_observed','outputs':out}
def predict_at(root,f):return {f['id']+'/'+c['case_id']:{'local_validity':True,'observation':derive(root,c['inputs'])} for c in f['cases']}
def predict(f):return predict_at(Path(__file__).resolve().parents[2],f)
def validate_prediction(v):
    if type(v) is not dict or not v:raise ValueError('prediction')
    for row in v.values():
        if set(row)!={'local_validity','observation'} or row['local_validity'] is not True:raise ValueError('row')
def make_profile(root):
    m=load(Path(root)/'profiles/capv/expectation-profile.v0.json')
    if m['profile_id']!=EXPECTATION_ID or m['version']!='0':raise ValueError('profile identity')
    return ExpectationProfile(EXPECTATION_ID,'0',tuple(FixtureSource(**r) for r in m['fixture_scope']),lambda f:predict_at(root,f),m['expectations_path'],m['expectations_digest'],validate_envelope,validate_prediction,lambda f:plan(f,'binding'),lambda r:verify_source(r))
