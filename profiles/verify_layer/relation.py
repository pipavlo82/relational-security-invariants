"""Account MPT/root and RPC balance binding; header authority not established."""
import re
from runner.relation_profile import Relation,RelationProfile
from rsi.codec import domain
from profiles.verify_layer.source import verify_source,SOURCE_PIN_SHA256
PROFILE_ID='verify-layer.proof-context.v0';VERSION='0';RELATION_ID='account-proof-root-balance'
REQUIRED=('address','header','response')
def validate_inputs(v):
    domain(v)
    if type(v) is not dict or set(v)!=set(REQUIRED):raise ValueError('slots')
    def hx(x,n=None):
        if type(x) is not str or re.fullmatch('0x[0-9a-fA-F]+',x) is None:raise ValueError('hex')
        if n is not None and len(x)!=2+n:raise ValueError('hex width')
    hx(v['address'],40)
    h=v['header'];r=v['response']
    if type(h) is not dict or set(h)!={'stateRoot','number'}:raise ValueError('header projection')
    hx(h['stateRoot'],64);hx(h['number'])
    if int(h['number'],16)>=2**256:raise ValueError('block range')
    if type(r) is not dict or set(r)!={'address','balance','accountProof'}:raise ValueError('response projection')
    hx(r['address'],40);hx(r['balance'])
    if int(r['balance'],16)>=2**256:raise ValueError('balance range')
    if type(r['accountProof']) is not list or not 1<=len(r['accountProof'])<=65:raise ValueError('proof size')
    for p in r['accountProof']:
        hx(p)
        if len(p)%2 or len(p)>32770:raise ValueError('proof bytes')
def validate_outputs(r):
    o=r['outputs']
    if set(o)!={'verified','boundToHeader','claimMatchesProof','provenBalanceWei','accountExists','stateTrust','headerTrust','overall','headerAuthority','downstreamAuthority'}:raise ValueError('outputs')
    for k in ('verified','boundToHeader','claimMatchesProof','accountExists'):
        if o[k] is not None and type(o[k]) is not bool:raise ValueError('boolean result')
    for k in set(o)-{'verified','boundToHeader','claimMatchesProof','accountExists'}:
        if o[k] is not None and type(o[k]) is not str:raise ValueError('string result')
def make_profile(root):
    def validate(v):verify_source(root);validate_inputs(v)
    def evaluate(v,c):
        from adapters.verify_layer.model import evaluate
        return evaluate(root,{'inputs':v})
    return RelationProfile(PROFILE_ID,VERSION,(Relation(RELATION_ID,REQUIRED,(),validate,evaluate,validate_outputs),),SOURCE_PIN_SHA256)
