"""Independent tuple and membership obligations. No TAS execution/helper calls."""
from pathlib import Path
from rsi.codec import load
from runner.expectation_registry import ExpectationProfile,FixtureSource
from runner.relation_runtime import validate_envelope,plan
from profiles.tas.source import verify_source
EXPECTATION_ID='tas.context-invocation.v0'
def derive(v,relation):
    a,c,m=v['accepted'],v['current'],v['member']
    same=a is not None and all(a[k]==c[k] for k in ('chainId','rpcUrl','fingerprint')) and a['workflowAddress'].lower()==c['workflowAddress'].lower()
    error=None;dispatch=None
    if not same:error='WORKFLOW_SOURCE_VERIFICATION_REQUIRED'
    elif v['tool_name']!='workflow.execution.erc8301.agent_workflow.get_task':error='MANIFEST_BINDING_UNSUPPORTED'
    elif m['block_hash'].lower()!=c['blockSelector']['blockHash'].lower() or m['agent_id']!=v['agent_id'] or not m['is_member']:error='AUTHORIZATION_DENIED'
    else:dispatch={'target':'AgentWorkflowClient.getTask','arguments':[v['task_hash']],'chainId':c['chainId'],'rpcUrl':c['rpcUrl'],'contractAddress':c['workflowAddress'],'wallet':m['wallet']}
    if dispatch is not None:error='EXTERNAL_UNAVAILABLE'
    return {'relation_id':relation,'relation_state':'conditional_dispatch_observed','outputs':{'native':{'error':error,'dispatched':dispatch},'invocation_admitted':dispatch is not None,'execution_occurrence':'UNSUPPORTED','context_authenticity':'SUPPLIED_NOT_RECOMPUTED'}}
def predict(f):
    return {f['id']+'/'+c['case_id']:{'local_validity':True,'observation':derive(c['inputs'],f['relation_id'])} for c in f['cases']}
def validate_prediction(v):
    if type(v) is not dict or not v:raise ValueError('prediction')
    for row in v.values():
        if set(row)!= {'local_validity','observation'} or row['local_validity'] is not True:raise ValueError('row')
def make_profile(root):
    m=load(Path(root)/'profiles/tas/expectation-profile.v0.json')
    if m['profile_id']!=EXPECTATION_ID or m['version']!='0':raise ValueError('identity')
    return ExpectationProfile(EXPECTATION_ID,'0',tuple(FixtureSource(**r) for r in m['fixture_scope']),predict,m['expectations_path'],m['expectations_digest'],validate_envelope,validate_prediction,lambda f:plan(f,'binding'),lambda r:verify_source(r))
