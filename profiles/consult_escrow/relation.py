"""ConsultEscrow job-state-bound outcome-attestation release profile."""
import re
from runner.relation_profile import Relation,RelationProfile
from rsi.codec import domain
from profiles.consult_escrow.source import verify_source,SOURCE_PIN_SHA256
PROFILE_ID='consult-escrow.release-binding.v0';VERSION='0';RELATION_ID='job-bound-release'
REQUIRED=('consumer','provider','relayer','attestor','amount','deadline','open_jobs','job_id','result_hash','signature','mode','prior')
def validate_inputs(v):
    domain(v)
    if type(v) is not dict or set(v)!=set(REQUIRED):raise ValueError('input slots')
    def hx(s,n):
        if type(s) is not str or re.fullmatch('0x[0-9a-f]{'+str(n)+'}',s) is None:raise ValueError('canonical hex')
    for k in ('consumer','provider','relayer','attestor'):
        hx(v[k],40)
        if int(v[k],16)<256:raise ValueError('EOA fixture address must exclude precompiles')
    if len({v[k] for k in ('consumer','provider','relayer','attestor')})!=4:raise ValueError('distinct fixture accounts')
    for k in ('amount','deadline'):
        if type(v[k]) is not str or re.fullmatch('[1-9][0-9]*',v[k]) is None or not 0<int(v[k])<2**256:raise ValueError('uint256 decimal string')
    if int(v['amount'])*2>10**30:raise ValueError('isolated funding bound')
    if type(v['open_jobs']) is not list or len(v['open_jobs'])!=2 or len(set(v['open_jobs']))!=2:raise ValueError('two distinct funded jobs')
    for x in v['open_jobs']+[v['job_id'],v['result_hash']]:hx(x,64)
    hx(v['signature'],130)
    if v['job_id'] not in v['open_jobs']:raise ValueError('opened target required')
    if v['mode'] not in ('execute','simulate') or v['prior'] not in ('none','release'):raise ValueError('harness mode')
def validate_outputs(r):
    if set(r['outputs'])!={'release_eligible','error','escrow_status','provider_delta','released_event','execution_occurrence'}:raise ValueError('outputs')
    if type(r['outputs']['release_eligible']) is not bool:raise ValueError('eligibility')
def make_profile(root):
    def validate(v):verify_source(root);validate_inputs(v)
    def evaluate(v,c):
        from adapters.consult_escrow.model import evaluate
        return evaluate(root,{'inputs':v})
    return RelationProfile(PROFILE_ID,VERSION,(Relation(RELATION_ID,REQUIRED,(),validate,evaluate,validate_outputs),),SOURCE_PIN_SHA256)
