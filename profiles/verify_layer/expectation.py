"""Independent Python MPT/root/balance obligations from pinned source."""
from pathlib import Path
from runner.expectation_registry import ExpectationProfile,FixtureSource
from runner.relation_runtime import validate_envelope,plan
from rsi.codec import load
from profiles.verify_layer.source import verify_source
from profiles.verify_layer.oracle import derive
EXPECTATION_ID='verify-layer.proof-context.v0'
def predict(f):return {f['id']+'/'+c['case_id']:{'local_validity':True,'observation':derive(c['inputs'],f['relation_id'])} for c in f['cases']}
def validate_prediction(v):
    if type(v) is not dict or not v:raise ValueError('prediction')
    for row in v.values():
        if set(row)!={'local_validity','observation'} or row['local_validity'] is not True:raise ValueError('row')
def make_profile(root):
    m=load(Path(root)/'profiles/verify_layer/expectation-profile.v0.json')
    if m['profile_id']!=EXPECTATION_ID or m['version']!='0':raise ValueError('identity')
    return ExpectationProfile(EXPECTATION_ID,'0',tuple(FixtureSource(**r) for r in m['fixture_scope']),predict,m['expectations_path'],m['expectations_digest'],validate_envelope,validate_prediction,lambda f:plan(f,'binding'),lambda r:verify_source(r))
