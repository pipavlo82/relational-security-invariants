"""Source-defined Workflow gate applicability, not a signed call intent."""
from runner.relation_profile import Relation,RelationProfile
from rsi.codec import domain
import re
from profiles.tas.source import verify_source,SOURCE_PIN_SHA256
PROFILE_ID='tas.context-invocation.v0';VERSION='0';RELATION_ID='verified-workflow-dispatch'
REQUIRED=('accepted','current','agent_id','member','tool_name','task_hash')
def exact(v,fields):
    if type(v) is not dict or set(v)!=set(fields):raise ValueError('shape')
def context(v):
    exact(v,('chainId','rpcUrl','workflowAddress','blockSelector','fingerprint'))
    for k in ('chainId','rpcUrl','workflowAddress','fingerprint'):
        if type(v[k]) is not str or not v[k]:raise ValueError('context string')
    exact(v['blockSelector'],('kind','blockHash'))
    if v['blockSelector']['kind']!='block_hash':raise ValueError('exact block required')
    if type(v['blockSelector']['blockHash']) is not str:raise ValueError('block hash')
def validate_inputs(v):
    domain(v);exact(v,REQUIRED);context(v['current'])
    if v['accepted'] is not None:context(v['accepted'])
    exact(v['member'],('agent_id','is_member','wallet','block_hash'))
    for address in [v['current']['workflowAddress'],v['member']['wallet']]+([] if v['accepted'] is None else [v['accepted']['workflowAddress']]):
        if type(address) is not str or re.fullmatch(r'0x[0-9]{40}',address) is None or int(address[2:])==0:raise ValueError('profile uses nonzero digit-only source-test addresses')
    if type(v['member']['is_member']) is not bool:raise ValueError('membership flag')
    for x in [v[k] for k in ('agent_id','tool_name','task_hash')]+[v['member'][k] for k in ('agent_id','wallet','block_hash')]:
        if type(x) is not str or not x:raise ValueError('string input')
def validate_outputs(r):
    exact(r['outputs'],('native','invocation_admitted','execution_occurrence','context_authenticity'))
    exact(r['outputs']['native'],('error','dispatched'))
    if type(r['outputs']['invocation_admitted']) is not bool:raise ValueError('admission shape')
def make_profile(root):
    def validate(v):verify_source(root);validate_inputs(v)
    def evaluate(v,c):
        from adapters.tas.model import evaluate
        return evaluate(root,{'inputs':v})
    return RelationProfile(PROFILE_ID,VERSION,(Relation(RELATION_ID,REQUIRED,(),validate,evaluate,validate_outputs),),SOURCE_PIN_SHA256)
