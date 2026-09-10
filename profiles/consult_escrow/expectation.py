"""Independent cryptographic and escrow-state obligations from pinned source."""
from pathlib import Path
from runner.expectation_registry import ExpectationProfile,FixtureSource
from runner.relation_runtime import validate_envelope,plan
from rsi.codec import load
from profiles.consult_escrow.source import verify_source
from profiles.consult_escrow.crypto import signer,commitment
EXPECTATION_ID='consult-escrow.release-binding.v0'
def derive(v,relation):
    valid=signer(v['job_id'],v['result_hash'],v['signature'])==v['attestor']
    error='not open' if v['prior']=='release' else (None if valid else 'bad attestor sig')
    executed=error is None and v['mode']=='execute'
    event=None
    if executed:event=dict(job_id=v['job_id'],result_hash=v['result_hash'],commitment_hash='0x'+commitment(v['job_id'],v['result_hash']).hex(),provider=v['provider'],amount=v['amount'])
    outputs=dict(release_eligible=error is None,error=error,escrow_status='Released' if executed or v['prior']=='release' else 'Open',provider_delta=v['amount'] if executed else '0',released_event=event,execution_occurrence='LOCAL_EVM' if executed else 'UNSUPPORTED')
    return dict(relation_id=relation,relation_state='release_observed',outputs=outputs)
def predict(f):return {f['id']+'/'+c['case_id']:{'local_validity':True,'observation':derive(c['inputs'],f['relation_id'])} for c in f['cases']}
def validate_prediction(v):
    if type(v) is not dict or not v:raise ValueError('prediction')
    for row in v.values():
        if set(row)!={'local_validity','observation'} or row['local_validity'] is not True:raise ValueError('row')
def make_profile(root):
    m=load(Path(root)/'profiles/consult_escrow/expectation-profile.v0.json')
    if m['profile_id']!=EXPECTATION_ID or m['version']!='0':raise ValueError('identity')
    return ExpectationProfile(EXPECTATION_ID,'0',tuple(FixtureSource(**r) for r in m['fixture_scope']),predict,m['expectations_path'],m['expectations_digest'],validate_envelope,validate_prediction,lambda f:plan(f,'binding'),lambda r:verify_source(r))
