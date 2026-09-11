"""Bounded single-chain trace transport; no new universal schema fields."""
import re
from rsi.codec import domain
from runner.relation_profile import Relation,RelationProfile
from profiles.aggregate.source import verify_source,SOURCE_PIN_SHA256
PROFILE_ID='erc8312.aggregate-budget.v0';VERSION='0';RELATION_ID='root-budget-conservation'
REQUIRED=('engine','roots','steps','periods','observation_time')
def validate_inputs(v):
    domain(v)
    if type(v) is not dict or set(v)!=set(REQUIRED) or v['engine'] not in ('cursor','edge'):raise ValueError('slots')
    def uint(s,bits):
        if type(s) is not str or re.fullmatch('0|[1-9][0-9]*',s) is None or int(s)>=2**bits:raise ValueError('decimal string')
    def hx(s,width):
        if type(s) is not str or re.fullmatch('0x[0-9a-f]{'+str(width)+'}',s) is None:raise ValueError('hex')
    if type(v['roots']) is not list or not 1<=len(v['roots'])<=4 or type(v['steps']) is not list or not 1<=len(v['steps'])<=64:raise ValueError('trace bound')
    if type(v['periods']) is not list or not v['periods'] or v['periods']!=sorted(set(v['periods'])) or any(type(p) is not int or not 0<=p<=1024 for p in v['periods']):raise ValueError('period scope')
    uint(v['observation_time'],64)
    for r in v['roots']:
        if set(r)!={'issuer','agent','cap','period_length','period_anchor','salt'}:raise ValueError('root')
        for k in ('issuer','agent'):
            hx(r[k],40)
            if int(r[k],16)==0:raise ValueError('zero agent')
        hx(r['salt'],64);uint(r['cap'],256);uint(r['period_length'],64);uint(r['period_anchor'],64)
        if int(r['cap'])==0 or (int(r['period_length']) and int(r['period_anchor'])==0):raise ValueError('root setup')
    last=int(v['observation_time'])
    for s in v['steps']:
        if set(s)!={'root','op','node','caller','agent','amount','time'} or s['op'] not in ('delegate','draw','revoke'):raise ValueError('step')
        if type(s['root']) is not int or not 0<=s['root']<len(v['roots']) or type(s['node']) is not int or not 0<=s['node']<=255:raise ValueError('index')
        hx(s['caller'],40);hx(s['agent'],40);uint(s['amount'],256);uint(s['time'],64)
        if s['op']=='delegate' and int(s['agent'],16)==0:raise ValueError('zero child')
        if int(s['time'])<last:raise ValueError('time order')
        last=int(s['time']);r=v['roots'][s['root']];length=int(r['period_length']);p=(last-int(r['period_anchor']))//length if length else 0
        if s['op']=='draw' and p>=0 and p not in v['periods']:raise ValueError('draw period absent')
    if sum(int(s['amount']) for s in v['steps'] if s['op']=='draw')>=2**256:raise ValueError('aggregate arithmetic scope')
    if v['engine']=='edge' and (len(v['roots'])!=1 or v['periods']!=[0] or v['roots'][0]['period_length']!='0' or any(s['op']=='revoke' for s in v['steps'])):raise ValueError('counterexample source scope')
def validate_outputs(r):
    o=r['outputs'];domain(o)
    if set(o)!={'steps','meters','log_origin','realized','conserved','non_bypassability','asset_movement','cross_chain_conservation','subtree_budgets','authoritative_chain_state'} or type(o['conserved']) is not bool:raise ValueError('output')
def make_profile(root):
    def validate(v):verify_source(root);validate_inputs(v)
    def actual(v,c):
        from adapters.aggregate.model import evaluate
        return evaluate(root,{'inputs':v})
    return RelationProfile(PROFILE_ID,VERSION,(Relation(RELATION_ID,REQUIRED,(),validate,actual,validate_outputs),),SOURCE_PIN_SHA256)
